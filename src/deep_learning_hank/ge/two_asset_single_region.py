"""DLH-4D minimal single-region two-asset GE steady-state solver (Issue #20).

Implements the frozen Option A closure (Issue #19 contract, accepted commit
``7fcfd64``) around the IMMUTABLE two-asset household oracle:

- ``K = A_hh``; ``B_hh = B_gov`` (constant exogenous real bonds);
- competitive firm ``mu=1``: ``Y = Z*K^alpha*L^(1-alpha)``,
  ``w = (1-alpha)*Z*(K/L)^alpha``, ``r_a = alpha*Z*(K/L)^(alpha-1) - delta``;
- balanced transfer ``T = tau*w*L - r_b*B_gov``, ``G=0``;
- ordered unknowns ``x = (r_a, r_b, L)``; residuals
  ``R = (A_hh-K, B_hh-B_gov, L_hh-L)``;
- nested deterministic Brent solves (inner ``R2`` for ``r_b``, middle ``R3``
  for ``L``, outer ``R1`` for ``r_a``) with the frozen domains, a frozen
  bracketing protocol (full interval then one uniform 9-point scan; exactly
  one sign-changing interval or exact root; zero brackets or multiple distinct
  brackets fail closed), and deterministic ``scipy.optimize.brentq``
  (``xtol <= 1e-10``, ``maxiter <= 100``).

Faithful resource/accounting diagnostics (read-only from final HJB/KFE
outputs): ``AC``, ``W_taper``, ``R_resource_structural``,
``R_resource_faithful`` (the near-zero numerical gate applies to
``R_resource_faithful``, not to the structural gap), plus fiscal and
aggregate wealth-flow residuals.

No household mutation; no fixture/domain tuning; fail-closed on every gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import tomllib
from typing import Any

import numpy as np
from scipy.optimize import brentq

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    matlab_faithful_illiquid_return,
    solve_household_steady_state,
)
from deep_learning_hank.ge.two_asset_initialization import build_cold_initialization

__all__ = [
    "GeConfig",
    "GeDiagnostics",
    "GeEvaluation",
    "GeRootResult",
    "GeSolveError",
    "RootBracketError",
    "evaluate_ge",
    "solve_ge",
]

FloatArray = np.ndarray


class GeSolveError(RuntimeError):
    """Generic GE-layer failure (fail closed)."""


class RootBracketError(GeSolveError):
    """Zero sign-changing bracket or multiple distinct brackets detected."""


class MultipleSteadyStateBracketsError(RootBracketError):
    """More than one distinct sign-changing interval found in the scan."""


@dataclass(frozen=True)
class GeConfig:
    path: Path
    b_min: float
    b_max: float
    b_points: int
    a_min: float
    a_max: float
    a_points: int
    z_states: tuple[float, float]
    switch_matrix: tuple[tuple[float, float], tuple[float, float]]
    rho: float
    gamma_c: float
    phi: float
    chi_0: float
    chi_1: float
    a_bar: float
    mu_z: float
    sigma_z: float
    hjb_delta: float
    convergence_tolerance: float
    hjb_max_iterations: int
    drift_tolerance: float
    Z: float
    alpha: float
    delta_capital: float
    B_gov: float
    G: float
    tau: float
    rb_gap: float
    r_a_low: float
    r_a_high: float
    r_b_low: float
    r_b_high: float
    L_low: float
    L_high: float
    bracket_scan_points: int
    root_xtol: float
    root_rtol: float
    root_max_iterations: int
    normalized_root_tolerance: float
    raw_market_residual_tolerance: float
    resource_faithful_tolerance: float
    fiscal_tolerance: float
    wealth_flow_tolerance: float
    kfe_mass_tolerance: float
    kfe_min_mass_threshold: float
    reproducibility_tolerance: float
    immutable_oracle_sha256: str
    immutable_oracle_blob: str

    @classmethod
    def from_toml(cls, path: Path) -> "GeConfig":
        resolved = path.resolve()
        with resolved.open("rb") as handle:
            data: dict[str, Any] = tomllib.load(handle)
        hg = data["household_grid"]
        hp = data["household_params"]
        hn = data["household_numerics"]
        ff = data["firm_fiscal"]
        dom = data["ge_domains"]
        num = data["ge_numerics"]
        gates = data["gates"]
        return cls(
            path=resolved,
            b_min=float(hg["b_min"]),
            b_max=float(hg["b_max"]),
            b_points=int(hg["b_points"]),
            a_min=float(hg["a_min"]),
            a_max=float(hg["a_max"]),
            a_points=int(hg["a_points"]),
            z_states=tuple(float(x) for x in hg["z_states"]),
            switch_matrix=tuple(tuple(float(x) for x in row) for row in hg["switch_matrix"]),
            rho=float(hp["rho"]),
            gamma_c=float(hp["gamma_c"]),
            phi=float(hp["phi"]),
            chi_0=float(hp["chi_0"]),
            chi_1=float(hp["chi_1"]),
            a_bar=float(hp["a_bar"]),
            mu_z=float(hp["mu_z"]),
            sigma_z=float(hp["sigma_z"]),
            hjb_delta=float(hn["delta"]),
            convergence_tolerance=float(hn["convergence_tolerance"]),
            hjb_max_iterations=int(hn["max_iterations"]),
            drift_tolerance=float(hn["drift_tolerance"]),
            Z=float(ff["Z"]),
            alpha=float(ff["alpha"]),
            delta_capital=float(ff["delta_capital"]),
            B_gov=float(ff["B_gov"]),
            G=float(ff["G"]),
            tau=float(ff["tau"]),
            rb_gap=float(ff["rb_gap"]),
            r_a_low=float(dom["r_a_low"]),
            r_a_high=float(dom["r_a_high"]),
            r_b_low=float(dom["r_b_low"]),
            r_b_high=float(dom["r_b_high"]),
            L_low=float(dom["L_low"]),
            L_high=float(dom["L_high"]),
            bracket_scan_points=int(dom["bracket_scan_points"]),
            root_xtol=float(num["root_xtol"]),
            root_rtol=float(num["root_rtol"]),
            root_max_iterations=int(num["root_max_iterations"]),
            normalized_root_tolerance=float(num["normalized_root_tolerance"]),
            raw_market_residual_tolerance=float(num["raw_market_residual_tolerance"]),
            resource_faithful_tolerance=float(num["resource_faithful_tolerance"]),
            fiscal_tolerance=float(num["fiscal_tolerance"]),
            wealth_flow_tolerance=float(num["wealth_flow_tolerance"]),
            kfe_mass_tolerance=float(num["kfe_mass_tolerance"]),
            kfe_min_mass_threshold=float(num["kfe_min_mass_threshold"]),
            reproducibility_tolerance=float(num["reproducibility_tolerance"]),
            immutable_oracle_sha256=str(gates["immutable_oracle_sha256"]).upper(),
            immutable_oracle_blob=str(gates["immutable_oracle_blob"]),
        )

    def oracle_path(self) -> Path:
        return (
            Path(__file__).resolve().parents[2]
            / "deep_learning_hank"
            / "two_asset"
            / "matlab_faithful_two_asset_ha.py"
        )

    def verify_oracle_identity(self) -> str:
        observed = hashlib.sha256(self.oracle_path().read_bytes()).hexdigest().upper()
        if observed != self.immutable_oracle_sha256:
            raise GeSolveError(
                "BLOCKED_DLH_4D_IMMUTABLE_HOUSEHOLD_IDENTITY_MISMATCH: "
                f"observed {observed} != frozen {self.immutable_oracle_sha256}"
            )
        return observed


@dataclass(frozen=True)
class GeEvaluation:
    r_a: float
    r_b: float
    L: float
    finite: bool
    K: float
    w: float
    Y: float
    T: float
    A_hh: float
    B_hh: float
    L_hh: float
    C_hh: float
    AC: float
    W_taper: float
    R_resource_structural: float
    R_resource_faithful: float
    R1: float
    R2: float
    R3: float
    R_fiscal: float
    R_wealth_chain: float
    R_wealth_direct: float
    hjb_converged: bool
    hjb_statistic: float
    hjb_iterations: int
    kfe_mass_error: float
    kfe_min_mass: float
    nan_inf_count: int
    result: Any | None


@dataclass(frozen=True)
class GeDiagnostics:
    identity_ok: bool
    hjb_ok: bool
    kfe_ok: bool
    market_ok: bool
    resource_ok: bool
    fiscal_ok: bool
    wealth_ok: bool
    finite_ok: bool
    all_gates_pass: bool
    details: dict[str, float]


@dataclass(frozen=True)
class GeRootResult:
    config: GeConfig
    root_r_a: float
    root_r_b: float
    root_L: float
    evaluation: GeEvaluation
    diagnostics: GeDiagnostics
    outer_bracket: tuple[float, float] | None
    outer_from_scan: bool
    middle_bracket: tuple[float, float] | None
    middle_from_scan: bool
    inner_bracket: tuple[float, float] | None
    inner_from_scan: bool
    evaluations_count: int


def _grid(config: GeConfig) -> MatlabFaithfulHJBGrid:
    b = np.linspace(config.b_min, config.b_max, config.b_points)
    a = np.linspace(config.a_min, config.a_max, config.a_points)
    z = np.asarray(config.z_states, dtype=np.float64)
    switch = np.asarray(config.switch_matrix, dtype=np.float64)
    return MatlabFaithfulHJBGrid(b, a, z, switch)


def _numerics(config: GeConfig) -> MatlabFaithfulHJBNumerics:
    return MatlabFaithfulHJBNumerics(
        delta=config.hjb_delta,
        convergence_tolerance=config.convergence_tolerance,
        max_iterations=config.hjb_max_iterations,
        drift_tolerance=config.drift_tolerance,
    )


def _nonfinite(config: GeConfig, r_a: float, r_b: float, L: float) -> GeEvaluation:
    return GeEvaluation(
        r_a=float(r_a),
        r_b=float(r_b),
        L=float(L),
        finite=False,
        K=float("nan"),
        w=float("nan"),
        Y=float("nan"),
        T=float("nan"),
        A_hh=float("nan"),
        B_hh=float("nan"),
        L_hh=float("nan"),
        C_hh=float("nan"),
        AC=float("nan"),
        W_taper=float("nan"),
        R_resource_structural=float("nan"),
        R_resource_faithful=float("nan"),
        R1=float("nan"),
        R2=float("nan"),
        R3=float("nan"),
        R_fiscal=float("nan"),
        R_wealth_chain=float("nan"),
        R_wealth_direct=float("nan"),
        hjb_converged=False,
        hjb_statistic=float("nan"),
        hjb_iterations=-1,
        kfe_mass_error=float("nan"),
        kfe_min_mass=float("nan"),
        nan_inf_count=-1,
        result=None,
    )


def evaluate_ge(config: GeConfig, r_a: float, r_b: float, L: float) -> GeEvaluation:
    """Full GE evaluation at a candidate ``(r_a, r_b, L)`` (deterministic)."""
    if r_a + config.delta_capital <= 0.0:
        return _nonfinite(config, r_a, r_b, L)
    try:
        alpha = config.alpha
        Z = config.Z
        delta = config.delta_capital
        K = L * (alpha * Z / (r_a + delta)) ** (1.0 / (1.0 - alpha))
        w = (1.0 - alpha) * Z * (K / L) ** alpha
        Y = Z * (K ** alpha) * (L ** (1.0 - alpha))
        T = config.tau * w * L - r_b * config.B_gov

        grid = _grid(config)
        params = EconomicParams(
            rho=config.rho,
            gamma_c=config.gamma_c,
            phi=config.phi,
            chi_0=config.chi_0,
            chi_1=config.chi_1,
            a_bar=config.a_bar,
            mu_z=config.mu_z,
            sigma_z=config.sigma_z,
        )
        inputs = HouseholdInputs(
            r_a=r_a,
            r_b=r_b,
            tau=config.tau,
            wages=np.array([w]),
            migration_costs=np.array([0.0]),
            labor_weights=np.array([1.0]),
        )
        initial, baseline_labor = build_cold_initialization(
            grid,
            params,
            r_a=r_a,
            r_b=r_b,
            w=w,
            transfer_income=T,
            rb_gap=config.rb_gap,
            tau=config.tau,
        )
        result = solve_household_steady_state(
            grid,
            params,
            inputs,
            initial,
            baseline_labor,
            T,
            config.rb_gap,
            _numerics(config),
        )
        hjb = result.hjb
        kfe = result.kfe
        agg = result.aggregates
        db = float(grid.b[1] - grid.b[0])
        da = float(grid.a[1] - grid.a[0])
        AC = float(np.sum(hjb.adjustment_cost * kfe.density) * db * da)
        ra_grid = matlab_faithful_illiquid_return(grid.a, grid.a[-1], r_a)
        a_3d = np.broadcast_to(grid.a[None, :, None], hjb.value.shape)
        W_taper = float(
            np.sum((r_a - ra_grid[None, :, None]) * a_3d * kfe.density) * db * da
        )
        int_raeff = float(np.sum(ra_grid[None, :, None] * a_3d * kfe.density) * db * da)

        A_hh = float(agg.a_ss)
        B_hh = float(agg.b_ss)
        L_hh = float(agg.l_ss)
        C_hh = float(agg.c_ss)
        R1 = A_hh - K
        R2 = B_hh - config.B_gov
        R3 = L_hh - L
        R_resource_structural = Y - C_hh - delta * K - AC
        R_resource_faithful = R_resource_structural - W_taper
        R_fiscal = config.tau * w * L - r_b * config.B_gov - T
        R_wealth_chain = (
            (1.0 - config.tau) * w * L
            + r_b * config.B_gov
            + T
            - C_hh
            - AC
            + int_raeff
        )
        R_wealth_direct = float(np.sum((hjb.mu_a + hjb.mu_b) * kfe.density) * db * da)
        nan_inf_count = int(
            np.count_nonzero(~np.isfinite(hjb.value))
            + np.count_nonzero(~np.isfinite(hjb.consumption))
            + np.count_nonzero(~np.isfinite(kfe.density))
            + (0 if np.isfinite([A_hh, B_hh, L_hh, C_hh, AC, W_taper]).all() else 1)
        )
        return GeEvaluation(
            r_a=float(r_a),
            r_b=float(r_b),
            L=float(L),
            finite=True,
            K=float(K),
            w=float(w),
            Y=float(Y),
            T=float(T),
            A_hh=float(A_hh),
            B_hh=float(B_hh),
            L_hh=float(L_hh),
            C_hh=float(C_hh),
            AC=float(AC),
            W_taper=float(W_taper),
            R_resource_structural=float(R_resource_structural),
            R_resource_faithful=float(R_resource_faithful),
            R1=float(R1),
            R2=float(R2),
            R3=float(R3),
            R_fiscal=float(R_fiscal),
            R_wealth_chain=float(R_wealth_chain),
            R_wealth_direct=float(R_wealth_direct),
            hjb_converged=bool(hjb.converged),
            hjb_statistic=float(hjb.convergence_statistic),
            hjb_iterations=int(hjb.iterations),
            kfe_mass_error=abs(float(np.sum(kfe.density) * db * da) - 1.0),
            kfe_min_mass=float(np.min(kfe.density)),
            nan_inf_count=nan_inf_count,
            result=result,
        )
    except (RuntimeError, ValueError, ArithmeticError):
        return _nonfinite(config, r_a, r_b, L)


def _sign_change(a: float, b: float) -> bool:
    if not (np.isfinite(a) and np.isfinite(b)):
        return False
    if a == 0.0 or b == 0.0:
        return True
    return np.sign(a) != np.sign(b)


def _find_bracket(
    residual,
    low: float,
    high: float,
    scan_points: int,
    label: str,
) -> tuple[tuple[float, float], bool, list[tuple[float, float]]]:
    """Full interval first; else one uniform 9-point scan; exactly one bracket."""
    r_low = residual(low)
    r_high = residual(high)
    if _sign_change(r_low, r_high):
        return (low, high), False, [(low, high)]
    scan = np.linspace(low, high, scan_points)
    values = [residual(float(x)) for x in scan]
    brackets: list[tuple[float, float]] = []
    for idx in range(len(scan) - 1):
        if _sign_change(values[idx], values[idx + 1]):
            brackets.append((float(scan[idx]), float(scan[idx + 1])))
        elif values[idx] == 0.0:
            # exact grid root: bracket on the point itself via a tiny interval
            brackets.append((float(scan[idx]), float(scan[idx + 1])))
    if len(brackets) == 0:
        raise RootBracketError(f"{label}: zero sign-changing brackets in interval [{low}, {high}]")
    if len(brackets) > 1:
        raise MultipleSteadyStateBracketsError(
            f"{label}: multiple distinct brackets {brackets} (possible steady-state multiplicity)"
        )
    return brackets[0], True, brackets


def _brent_root(residual, bracket: tuple[float, float], config: GeConfig, label: str) -> float:
    try:
        root, info = brentq(
            residual,
            bracket[0],
            bracket[1],
            xtol=config.root_xtol,
            rtol=config.root_rtol,
            maxiter=config.root_max_iterations,
            full_output=True,
            disp=False,
        )
    except ValueError as exc:
        # Non-finite (NaN) residual inside the bracket (e.g., a singular
        # household KFE at some candidate): the evaluation is excluded from the
        # parent bracket logic, exactly like any other non-finite evaluation.
        # Fail-closed only if no bracket can be established anywhere.
        raise GeSolveError(f"{label}: brentq hit a non-finite evaluation ({exc})") from exc
    if not info.converged:
        raise GeSolveError(f"{label}: brentq did not converge")
    return float(root)


def solve_ge(config: GeConfig) -> GeRootResult:
    """Solve the nested Option A GE steady state (deterministic)."""
    config.verify_oracle_identity()
    count = [0]

    def residual_r2(r_b: float, r_a: float, L: float) -> float:
        count[0] += 1
        evaluation = evaluate_ge(config, r_a, float(r_b), L)
        return evaluation.R2 if evaluation.finite else float("nan")

    def solve_inner_rb(r_a: float, L: float) -> tuple[float, tuple[float, float], bool]:
        def resid(r_b: float) -> float:
            return residual_r2(r_b, r_a, L)

        bracket, from_scan, _ = _find_bracket(
            resid, config.r_b_low, config.r_b_high, config.bracket_scan_points, "R2(r_b)"
        )
        return _brent_root(resid, bracket, config, "R2"), bracket, from_scan

    def residual_r3(L: float, r_a: float) -> float:
        try:
            r_b_star, _, _ = solve_inner_rb(r_a, float(L))
        except (RootBracketError, GeSolveError):
            return float("nan")
        evaluation = evaluate_ge(config, r_a, r_b_star, float(L))
        return evaluation.R3 if evaluation.finite else float("nan")

    def solve_middle_L(r_a: float) -> tuple[float, tuple[float, float], bool]:
        def resid(L: float) -> float:
            return residual_r3(L, r_a)

        bracket, from_scan, _ = _find_bracket(
            resid, config.L_low, config.L_high, config.bracket_scan_points, "R3(L)"
        )
        return _brent_root(resid, bracket, config, "R3"), bracket, from_scan

    def residual_r1(r_a: float) -> float:
        try:
            L_star, _, _ = solve_middle_L(float(r_a))
            r_b_star, _, _ = solve_inner_rb(float(r_a), L_star)
        except (RootBracketError, GeSolveError):
            return float("nan")
        evaluation = evaluate_ge(config, float(r_a), r_b_star, L_star)
        return evaluation.R1 if evaluation.finite else float("nan")

    outer_bracket, outer_from_scan, _ = _find_bracket(
        residual_r1, config.r_a_low, config.r_a_high, config.bracket_scan_points, "R1(r_a)"
    )
    root_r_a = _brent_root(residual_r1, outer_bracket, config, "R1")
    L_star, middle_bracket, middle_from_scan = solve_middle_L(root_r_a)
    r_b_star, inner_bracket, inner_from_scan = solve_inner_rb(root_r_a, L_star)
    evaluation = evaluate_ge(config, root_r_a, r_b_star, L_star)

    diagnostics = build_diagnostics(config, evaluation)
    return GeRootResult(
        config=config,
        root_r_a=root_r_a,
        root_r_b=r_b_star,
        root_L=L_star,
        evaluation=evaluation,
        diagnostics=diagnostics,
        outer_bracket=outer_bracket,
        outer_from_scan=outer_from_scan,
        middle_bracket=middle_bracket,
        middle_from_scan=middle_from_scan,
        inner_bracket=inner_bracket,
        inner_from_scan=inner_from_scan,
        evaluations_count=count[0],
    )


def build_diagnostics(config: GeConfig, e: GeEvaluation) -> GeDiagnostics:
    """Evaluate the Issue #20 numerical gates at the final candidate."""
    details: dict[str, float] = {}
    if not e.finite:
        details["finite"] = 0.0
        return GeDiagnostics(
            identity_ok=False,
            hjb_ok=False,
            kfe_ok=False,
            market_ok=False,
            resource_ok=False,
            fiscal_ok=False,
            wealth_ok=False,
            finite_ok=False,
            all_gates_pass=False,
            details=details,
        )
    norm1 = abs(e.R1) / max(abs(e.K), 1e-14)
    norm2 = abs(e.R2) / max(abs(config.B_gov), 1e-14)
    norm3 = abs(e.R3) / max(abs(e.L), 1e-14)
    root_norm = max(norm1, norm2, norm3)
    details.update(
        {
            "root_norm_inf": root_norm,
            "R1": e.R1,
            "R2": e.R2,
            "R3": e.R3,
            "R_resource_structural": e.R_resource_structural,
            "W_taper": e.W_taper,
            "R_resource_faithful": e.R_resource_faithful,
            "R_fiscal": e.R_fiscal,
            "R_wealth_chain": e.R_wealth_chain,
            "R_wealth_direct": e.R_wealth_direct,
            "hjb_statistic": e.hjb_statistic,
            "kfe_mass_error": e.kfe_mass_error,
            "kfe_min_mass": e.kfe_min_mass,
            "nan_inf_count": float(e.nan_inf_count),
        }
    )
    identity_ok = True  # verified at load (GeConfig.verify_oracle_identity)
    hjb_ok = bool(
        e.hjb_converged and e.hjb_statistic <= config.convergence_tolerance
    )
    kfe_ok = bool(
        e.kfe_mass_error <= config.kfe_mass_tolerance
        and e.kfe_min_mass >= config.kfe_min_mass_threshold
    )
    market_ok = bool(
        root_norm <= config.normalized_root_tolerance
        and abs(e.R1) <= config.raw_market_residual_tolerance
        and abs(e.R2) <= config.raw_market_residual_tolerance
        and abs(e.R3) <= config.raw_market_residual_tolerance
    )
    resource_ok = bool(abs(e.R_resource_faithful) <= config.resource_faithful_tolerance)
    fiscal_ok = bool(abs(e.R_fiscal) <= config.fiscal_tolerance)
    wealth_ok = bool(abs(e.R_wealth_chain) <= config.wealth_flow_tolerance)
    finite_ok = bool(e.nan_inf_count == 0)
    return GeDiagnostics(
        identity_ok=identity_ok,
        hjb_ok=hjb_ok,
        kfe_ok=kfe_ok,
        market_ok=market_ok,
        resource_ok=resource_ok,
        fiscal_ok=fiscal_ok,
        wealth_ok=wealth_ok,
        finite_ok=finite_ok,
        all_gates_pass=bool(
            identity_ok
            and hjb_ok
            and kfe_ok
            and market_ok
            and resource_ok
            and fiscal_ok
            and wealth_ok
            and finite_ok
        ),
        details=details,
    )
