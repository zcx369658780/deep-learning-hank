"""DLH-5B (Issue #25): deterministic two-region hand-specified-flow outer fixed point.

Implements the accepted DLH-5A structural contract (Issue #24) on the exact
frozen exploratory fixture from ``configs/dlh_5b_two_region_symmetric_anchor.toml``.

Binding contract (unchanged):
- accepted two-asset household oracle is immutable and is *called*, never copied;
- ``K_i = M_i * A_i`` provisional private-capital closure; ``B_i`` is a
  household liquid-asset diagnostic only (no ``B=1``, no bond-supply root);
- hand-specified labor network ``P^L``, flows ``F^L_ij = M_i L_i^home P^L_ij``,
  ``L_j^dest = sum_i F^L_ij``, composite gross wage ``wbar_i = sum_j P^L_ij w_j``;
- synchronous/Jacobi outer semantics: both regional HA blocks read the same
  immutable ``Gamma^(n)`` snapshot; no region-order dependence;
- residuals ``R_w = max_i |log(w_hat_i/w_i)|``, ``R_ra = max_i |r_hat_i^a - r_i^a|``;
- deterministic damping ``Gamma_next = (1-lambda) Gamma + lambda Gamma_hat`` only;
- no Brent/Newton/fsolve for the outer map (the only Brent use is the accepted
  household *initial-value* fixture construction, reused verbatim);
- no automatic retry, adaptive damping, grid expansion, or PASS-seeking tuning;
- HJB/KFE/boundary failures are preserved as fail-closed diagnostics.

The only frozen derivation is the one-shot anchor construction: ``Z*``/``delta*``
are derived ONCE from the accepted household solve at ``w*=1, r_a*=0.03``,
pass the sanity gate, and are then frozen for both regions and all cases.

R1 bounded repair (GPT review 2026-08-31, same Issue #25, no successor):
- S1 enforces the full frozen validity bundle (accounting/network + KFE + firm)
  on every valid turn, before residual acceptance and before damping; any
  failure stops with ``VALIDITY_GATE_FAILED:<deterministic detail>``;
- every trace row carries full ``P^L``, ``lambda``, and ``Gamma_next``;
  blocked terminal turns record deterministic NaN/null-equivalent ``Gamma_next``;
- ``max_numeric_diff`` is non-finite aware (aligned NaN==NaN equal; any
  NaN-vs-finite, Inf-sign or other nonfinite mismatch -> failure/Inf);
- terminal classification fail-closes on S2 / reproducibility failure and never
  emits an ``ARCHITECTURE_VALIDATED`` class when order invariance or
  reproducibility is false.
The only config mutation authorized by R1 is ``output.root`` (new R1 evidence
root); every scientific/numerical fixture field stays value-identical to the
predecessor.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import math
import pathlib
import sys
import tomllib
from typing import Any, Optional, Sequence

import numpy as np
from scipy.optimize import brentq

from deep_learning_hank.two_asset import (
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    flow_utility,
    matlab_faithful_illiquid_return,
    solve_household_steady_state,
)

# ---------------------------------------------------------------------------
# Frozen configuration
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class TwoRegionConfig:
    # household
    rho: float
    gamma_c: float
    phi: float
    chi_0: float
    chi_1: float
    a_bar: float
    mu_z: float
    sigma_z: float
    b_lo: float
    b_hi: float
    b_pts: int
    a_lo: float
    a_hi: float
    a_pts: int
    z: tuple
    switch_matrix: tuple
    r_b: float
    tau: tuple
    transfer_income: tuple
    rb_gap: tuple
    hjb_delta: float
    conv_tol: float
    hjb_max_iterations: int
    drift_tol: float
    # network
    M: tuple
    m_L: tuple
    P_L: tuple
    # anchor
    w_star: tuple
    r_a_star: tuple
    alpha: tuple
    # outer numerics
    lambda_: float
    tol_w: float
    tol_ra: float
    max_iter: int
    s0_tol_w: float
    s0_tol_ra: float
    order_invariance_tol: float
    reproducibility_tol: float
    accounting_tol: float
    kfe_mass_tol: float
    kfe_min_mass_threshold: float
    boundary_mass_warning_threshold: float
    output_root: str


def load_config(path: str | pathlib.Path) -> TwoRegionConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    h = raw["household"]
    n = raw["network"]
    a = raw["anchor"]
    o = raw["outer"]
    out = raw["output"]
    cfg = TwoRegionConfig(
        rho=float(h["rho"]),
        gamma_c=float(h["gamma_c"]),
        phi=float(h["phi"]),
        chi_0=float(h["chi_0"]),
        chi_1=float(h["chi_1"]),
        a_bar=float(h["a_bar"]),
        mu_z=float(h["mu_z"]),
        sigma_z=float(h["sigma_z"]),
        b_lo=float(h["b_lo"]),
        b_hi=float(h["b_hi"]),
        b_pts=int(h["b_pts"]),
        a_lo=float(h["a_lo"]),
        a_hi=float(h["a_hi"]),
        a_pts=int(h["a_pts"]),
        z=tuple(float(x) for x in h["z"]),
        switch_matrix=tuple(tuple(float(x) for x in row) for row in h["switch_matrix"]),
        r_b=float(h["r_b"]),
        tau=tuple(float(x) for x in h["tau"]),
        transfer_income=tuple(float(x) for x in h["transfer_income"]),
        rb_gap=tuple(float(x) for x in h["rb_gap"]),
        hjb_delta=float(h["delta"]),
        conv_tol=float(h["convergence_tolerance"]),
        hjb_max_iterations=int(h["max_iterations"]),
        drift_tol=float(h["drift_tolerance"]),
        M=tuple(float(x) for x in n["M"]),
        m_L=tuple(float(x) for x in n["m_L"]),
        P_L=tuple(tuple(float(x) for x in row) for row in n["P_L"]),
        w_star=tuple(float(x) for x in a["w_star"]),
        r_a_star=tuple(float(x) for x in a["r_a_star"]),
        alpha=tuple(float(x) for x in a["alpha"]),
        lambda_=float(o["lambda"]),
        tol_w=float(o["tol_w"]),
        tol_ra=float(o["tol_ra"]),
        max_iter=int(o["max_iter"]),
        s0_tol_w=float(o["s0_tol_w"]),
        s0_tol_ra=float(o["s0_tol_ra"]),
        order_invariance_tol=float(o["order_invariance_tol"]),
        reproducibility_tol=float(o["reproducibility_tol"]),
        accounting_tol=float(o["accounting_tol"]),
        kfe_mass_tol=float(o["kfe_mass_tol"]),
        kfe_min_mass_threshold=float(o["kfe_min_mass_threshold"]),
        boundary_mass_warning_threshold=float(o["boundary_mass_warning_threshold"]),
        output_root=str(out["root"]),
    )
    # frozen sanity: network row sums = 1
    for row in cfg.P_L:
        if abs(sum(row) - 1.0) > 1e-12:
            raise ValueError("P^L row must sum to one")
    return cfg


# ---------------------------------------------------------------------------
# Accepted household fixture (verbatim conventions of test_dlh_4b_transfer.py)
# ---------------------------------------------------------------------------


def build_fixture(cfg: TwoRegionConfig):
    """Build the accepted VALIDATION_FIXTURE_NOT_CALIBRATION household objects.

    The initialization (scalar Brent labor solve + V0) is the accepted fixture
    logic from ``tests/test_dlh_4b_transfer.py``, reused verbatim. It is used
    only to construct household initial values, never to solve the outer map.
    """
    params = EconomicParams(
        cfg.rho, cfg.gamma_c, cfg.phi, cfg.chi_0, cfg.chi_1, cfg.a_bar, cfg.mu_z, cfg.sigma_z
    )
    b = np.linspace(cfg.b_lo, cfg.b_hi, cfg.b_pts)
    a = np.linspace(cfg.a_lo, cfg.a_hi, cfg.a_pts)
    z = np.asarray(list(cfg.z), dtype=float)
    switch = np.asarray(cfg.switch_matrix, dtype=float)
    grid = MatlabFaithfulHJBGrid(b, a, z, switch)
    numerics = MatlabFaithfulHJBNumerics(
        delta=cfg.hjb_delta,
        convergence_tolerance=cfg.conv_tol,
        max_iterations=cfg.hjb_max_iterations,
        drift_tolerance=cfg.drift_tol,
    )
    return grid, params, numerics


def household_initial_condition(
    grid: MatlabFaithfulHJBGrid,
    params: EconomicParams,
    inputs: HouseholdInputs,
    rb_gap: float,
):
    """Accepted fixture initialization for the current scalar wage and ``r_a``."""
    shape = (grid.b.size, grid.a.size, grid.z.size)
    labor0 = np.empty(shape)
    initial = np.empty(shape)
    for nz in range(grid.z.size):
        for j in range(grid.a.size):
            for i in range(grid.b.size):
                rb = inputs.r_b + (rb_gap if grid.b[i] < 0 else 0.0)
                base = rb * grid.b[i]
                net = (1.0 - inputs.tau) * inputs.wages[0] * grid.z[nz]

                def f(l):
                    return l ** params.phi - net * (net * l + base) ** (-params.gamma_c)

                labor0[i, j, nz] = brentq(f, 1e-8, 5.0)
                ra = float(matlab_faithful_illiquid_return(grid.a[j], grid.a[-1], inputs.r_a))
                c_full = net * labor0[i, j, nz] + base + ra * grid.a[j]
                initial[i, j, nz] = flow_utility(
                    c_full, np.array([labor0[i, j, nz]]), inputs, params
                ) / params.rho
    return initial, labor0


# ---------------------------------------------------------------------------
# Regional household block
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class RegionResult:
    i: int
    blocked: bool
    block_reason: Optional[str]
    C: float = float("nan")
    L_home: float = float("nan")
    A: float = float("nan")
    B: float = float("nan")
    C_tot: float = float("nan")
    L_tot: float = float("nan")
    A_tot: float = float("nan")
    B_tot: float = float("nan")
    hjb_converged: bool = False
    hjb_iterations: int = -1
    hjb_statistic: float = float("nan")
    kfe_mass_error: float = float("nan")
    kfe_min_density: float = float("nan")
    boundary_masses: Optional[dict] = None


def _boundary_masses(density: np.ndarray, db: float, da: float) -> dict:
    return {
        "b_min": float(np.sum(density[0, :, :]) * db * da),
        "b_max": float(np.sum(density[-1, :, :]) * db * da),
        "a_min": float(np.sum(density[:, 0, :]) * db * da),
        "a_max": float(np.sum(density[:, -1, :]) * db * da),
    }


def solve_region_household(
    cfg: TwoRegionConfig,
    grid: MatlabFaithfulHJBGrid,
    params: EconomicParams,
    numerics: MatlabFaithfulHJBNumerics,
    r_a: float,
    wbar: float,
    region_index: int,
) -> RegionResult:
    """Conditional stationary HA solve for one region (synchronous/Jacobi)."""
    inputs = HouseholdInputs(
        r_a=r_a,
        r_b=cfg.r_b,
        tau=cfg.tau[region_index],
        wages=np.array([wbar]),
        migration_costs=np.array([0.0]),
        labor_weights=np.array([1.0]),
    )
    initial, labor0 = household_initial_condition(grid, params, inputs, cfg.rb_gap[region_index])
    try:
        result = solve_household_steady_state(
            grid,
            params,
            inputs,
            initial,
            labor0,
            cfg.transfer_income[region_index],
            cfg.rb_gap[region_index],
            numerics,
        )
    except (RuntimeError, ValueError, ArithmeticError) as exc:
        return RegionResult(i=region_index, blocked=True, block_reason=str(exc))
    agg = result.aggregates
    density = np.asarray(result.kfe.density, dtype=float)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    kfe_mass_error = float(abs(float(np.sum(density) * db * da) - 1.0))
    kfe_min_density = float(np.min(density))
    bm = _boundary_masses(density, db, da)
    M = cfg.M[region_index]
    return RegionResult(
        i=region_index,
        blocked=False,
        block_reason=None,
        C=float(agg.c_ss),
        L_home=float(agg.l_ss),
        A=float(agg.a_ss),
        B=float(agg.b_ss),
        C_tot=float(M * agg.c_ss),
        L_tot=float(M * agg.l_ss),
        A_tot=float(M * agg.a_ss),
        B_tot=float(M * agg.b_ss),
        hjb_converged=bool(result.hjb.converged),
        hjb_iterations=int(result.hjb.iterations),
        hjb_statistic=float(result.hjb.convergence_statistic),
        kfe_mass_error=kfe_mass_error,
        kfe_min_density=kfe_min_density,
        boundary_masses=bm,
    )


# ---------------------------------------------------------------------------
# Real firm block and outer one-turn map
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class FrozenFirmParams:
    Z: tuple
    delta: tuple
    alpha: tuple


def firm_block(Z: float, alpha: float, delta: float, K: float, Ldest: float):
    """Competitive real firm block (DLH-5A Decision 2). Fails closed if invalid."""
    if not (np.isfinite(K) and np.isfinite(Ldest) and K > 0.0 and Ldest > 0.0):
        raise ValueError("firm requires finite positive K_i and L_i^dest")
    Y = Z * (K ** alpha) * (Ldest ** (1.0 - alpha))
    w_hat = (1.0 - alpha) * Y / Ldest
    r_hat_a = alpha * Y / K - delta
    if not (np.isfinite(Y) and np.isfinite(w_hat) and np.isfinite(r_hat_a)):
        raise ValueError("firm produced non-finite prices")
    if not (Y > 0.0 and w_hat > 0.0):
        raise ValueError("firm produced non-positive Y or wage")
    return float(Y), float(w_hat), float(r_hat_a)


@dataclasses.dataclass
class OneTurnRecord:
    gamma: tuple
    wbar: tuple
    region: dict
    F: tuple
    Ldest: tuple
    K: tuple
    Y: tuple
    w_hat: tuple
    r_hat_a: tuple
    R_w: float
    R_ra: float
    gamma_hat: tuple
    valid: bool
    invalid_reason: Optional[str]
    accounting: Optional[dict] = None


def one_turn(
    gamma: Sequence[float],
    cfg: TwoRegionConfig,
    grid,
    params,
    numerics,
    firm: FrozenFirmParams,
    region_order: Sequence[int] = (0, 1),
) -> OneTurnRecord:
    """One synchronous/Jacobi outer turn from an immutable old snapshot."""
    w = (float(gamma[0]), float(gamma[1]))
    ra = (float(gamma[2]), float(gamma[3]))
    P = cfg.P_L
    wbar = (
        P[0][0] * w[0] + P[0][1] * w[1],
        P[1][0] * w[0] + P[1][1] * w[1],
    )
    # synchronous: every regional HA solve reads the same old snapshot.
    region: dict = {}
    for i in region_order:
        region[i] = solve_region_household(cfg, grid, params, numerics, ra[i], wbar[i], i)
    for i in (0, 1):
        if region[i].blocked:
            reason = f"HOUSEHOLD_BLOCK_FAILED:region{i}:{region[i].block_reason}"
            return OneTurnRecord(
                gamma=(w[0], w[1], ra[0], ra[1]), wbar=wbar, region=region,
                F=((), ()), Ldest=(), K=(), Y=(), w_hat=(), r_hat_a=(), R_w=float("nan"),
                R_ra=float("nan"), gamma_hat=(), valid=False, invalid_reason=reason,
            )
    F = tuple(
        tuple(cfg.M[i] * region[i].L_home * P[i][j] for j in range(2)) for i in range(2)
    )
    Ldest = (F[0][0] + F[1][0], F[0][1] + F[1][1])
    K = (cfg.M[0] * region[0].A, cfg.M[1] * region[1].A)
    try:
        Y0, w_hat0, r_hat0 = firm_block(firm.Z[0], firm.alpha[0], firm.delta[0], K[0], Ldest[0])
        Y1, w_hat1, r_hat1 = firm_block(firm.Z[1], firm.alpha[1], firm.delta[1], K[1], Ldest[1])
    except ValueError as exc:
        return OneTurnRecord(
            gamma=(w[0], w[1], ra[0], ra[1]), wbar=wbar, region=region,
            F=F, Ldest=Ldest, K=K, Y=(), w_hat=(), r_hat_a=(), R_w=float("nan"),
            R_ra=float("nan"), gamma_hat=(), valid=False,
            invalid_reason=f"INVALID_FIRM_STATE:{exc}",
        )
    Y = (Y0, Y1)
    w_hat = (w_hat0, w_hat1)
    r_hat_a = (r_hat0, r_hat1)
    R_w = max(abs(math.log(w_hat[i] / w[i])) for i in range(2))
    R_ra = max(abs(r_hat_a[i] - ra[i]) for i in range(2))
    gamma_hat = (w_hat[0], w_hat[1], r_hat_a[0], r_hat_a[1])
    accounting = compute_accounting(cfg, w, wbar, F, Ldest, region)
    return OneTurnRecord(
        gamma=(w[0], w[1], ra[0], ra[1]), wbar=wbar, region=region, F=F, Ldest=Ldest,
        K=K, Y=Y, w_hat=w_hat, r_hat_a=r_hat_a, R_w=R_w, R_ra=R_ra,
        gamma_hat=gamma_hat, valid=True, invalid_reason=None, accounting=accounting,
    )


def compute_accounting(cfg, w, wbar, F, Ldest, region) -> dict:
    """Labor/conservation identities (abs+rel tolerance applied by caller)."""
    origin_cons = {}
    for i in range(2):
        lhs = F[i][0] + F[i][1]
        rhs = cfg.M[i] * region[i].L_home
        origin_cons[f"origin{i}"] = float(lhs - rhs)
    economy = float((Ldest[0] + Ldest[1]) - (cfg.M[0] * region[0].L_home + cfg.M[1] * region[1].L_home))
    lhs_wb = cfg.M[0] * region[0].L_home * wbar[0] + cfg.M[1] * region[1].L_home * wbar[1]
    rhs_wb = w[0] * Ldest[0] + w[1] * Ldest[1]
    wage_bill = float(lhs_wb - rhs_wb)
    return {"origin_conservation": origin_cons, "economy_labor": economy, "wage_bill": wage_bill}


# ---------------------------------------------------------------------------
# Anchor derivation (one-shot, then frozen)
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class AnchorResult:
    A_star: float
    L_star: float
    C_star: float
    B_star: float
    K_star: float
    Ldest_star: float
    Z_star: float
    delta_star: float
    alpha: float
    region: RegionResult
    sanity: dict


def derive_anchor(cfg: TwoRegionConfig, grid, params, numerics) -> AnchorResult:
    """Derive Z* and delta* once from the accepted anchor household solve."""
    rec = solve_region_household(
        cfg, grid, params, numerics,
        cfg.r_a_star[0], cfg.w_star[0], region_index=0,
    )
    if rec.blocked:
        raise RuntimeError(f"anchor household solve failed: {rec.block_reason}")
    alpha = cfg.alpha[0]
    A_star = rec.A
    L_star = rec.L_home
    C_star = rec.C
    B_star = rec.B
    K_star = cfg.M[0] * A_star
    Ldest_star = L_star  # symmetric network preserves equal labor
    Z_star = (1.0 / (1.0 - alpha)) * (L_star / K_star) ** alpha
    delta_star = (alpha / (1.0 - alpha)) * (L_star / K_star) - cfg.r_a_star[0]
    finite_ok = all(np.isfinite(x) for x in (A_star, L_star, C_star, B_star, Z_star, delta_star))
    sanity = {
        "A_star_positive": A_star > 0.0,
        "L_star_positive": L_star > 0.0,
        "Z_star_positive": Z_star > 0.0,
        "delta_in_unit": 0.0 < delta_star < 1.0,
        "all_finite": bool(finite_ok),
    }
    if not all(sanity.values()):
        raise RuntimeError(f"Z*/delta* sanity gate failed: {sanity}")
    return AnchorResult(
        A_star=float(A_star), L_star=float(L_star), C_star=float(C_star),
        B_star=float(B_star), K_star=float(K_star), Ldest_star=float(Ldest_star),
        Z_star=float(Z_star), delta_star=float(delta_star), alpha=float(alpha),
        region=rec, sanity=sanity,
    )


# ---------------------------------------------------------------------------
# Validity gates
# ---------------------------------------------------------------------------


def accounting_gate(cfg: TwoRegionConfig, rec: OneTurnRecord) -> tuple[bool, dict]:
    ac = rec.accounting
    tol = cfg.accounting_tol
    checks = {}
    for i in range(2):
        val = ac["origin_conservation"][f"origin{i}"]
        denom = max(1.0, abs(cfg.M[i] * rec.region[i].L_home))
        checks[f"origin{i}_conservation"] = bool(abs(val) <= tol * denom + tol)
    ev = ac["economy_labor"]
    denom = max(1.0, abs(cfg.M[0] * rec.region[0].L_home + cfg.M[1] * rec.region[1].L_home))
    checks["economy_labor"] = bool(abs(ev) <= tol * denom + tol)
    wb = ac["wage_bill"]
    denom = max(1.0, abs(cfg.M[0] * rec.region[0].L_home * rec.wbar[0] + cfg.M[1] * rec.region[1].L_home * rec.wbar[1]))
    checks["wage_bill"] = bool(abs(wb) <= tol * denom + tol)
    checks["network_rows_sum"] = all(abs(sum(row) - 1.0) <= tol for row in cfg.P_L)
    checks["network_nonneg"] = all(min(row) >= -tol for row in cfg.P_L)
    return all(checks.values()), checks


def kfe_gate(cfg: TwoRegionConfig, rec: OneTurnRecord) -> tuple[bool, dict]:
    checks = {}
    for i in (0, 1):
        r = rec.region[i]
        checks[f"kfe_mass_error{i}"] = bool(r.kfe_mass_error <= cfg.kfe_mass_tol)
        checks[f"kfe_min_density{i}"] = bool(r.kfe_min_density >= cfg.kfe_min_mass_threshold)
        checks[f"kfe_finite{i}"] = bool(np.isfinite(r.kfe_mass_error))
    return all(checks.values()), checks


def firm_gate(rec: OneTurnRecord) -> tuple[bool, dict]:
    checks = {}
    for i in (0, 1):
        checks[f"K{i}_positive"] = bool(rec.K[i] > 0.0)
        checks[f"Ldest{i}_positive"] = bool(rec.Ldest[i] > 0.0)
        checks[f"Y{i}_positive"] = bool(rec.Y[i] > 0.0)
        checks[f"w_hat{i}_positive"] = bool(rec.w_hat[i] > 0.0)
        checks[f"r_hat{i}_finite"] = bool(np.isfinite(rec.r_hat_a[i]))
    return all(checks.values()), checks


def boundary_warning(cfg: TwoRegionConfig, rec: OneTurnRecord) -> dict:
    th = cfg.boundary_mass_warning_threshold
    out = {}
    for i in (0, 1):
        bm = rec.region[i].boundary_masses
        out[f"region{i}"] = {
            "b_min": bm["b_min"], "b_max": bm["b_max"],
            "a_min": bm["a_min"], "a_max": bm["a_max"],
            "warning": bool(max(bm.values()) > th),
        }
    return out


# ---------------------------------------------------------------------------
# Full frozen validity bundle (R1-A) and damping helpers
# ---------------------------------------------------------------------------

# Frozen stop classes that block the outer iteration before a next state is
# defined (no damping applied -> deterministic NaN Gamma_next).
BLOCKED_STOP_PREFIXES = ("HOUSEHOLD_BLOCK_FAILED", "INVALID_FIRM_STATE", "VALIDITY_GATE_FAILED")


def _is_blocked_stop(reason: str) -> bool:
    return any(reason.startswith(p) for p in BLOCKED_STOP_PREFIXES)


def validity_bundle(cfg: TwoRegionConfig, rec: OneTurnRecord):
    """Full frozen accounting/network + KFE + firm validity bundle (R1-A).

    Returns ``(ok, deterministic_failure_detail, checks)``. Every gate must pass
    before a valid turn may be accepted or damped.
    """
    ac_ok, ac_checks = accounting_gate(cfg, rec)
    kfe_ok, kfe_checks = kfe_gate(cfg, rec)
    fm_ok, fm_checks = firm_gate(rec)
    ok = bool(ac_ok and kfe_ok and fm_ok)
    detail = None
    if not ok:
        for name, checks in (("accounting", ac_checks), ("kfe", kfe_checks), ("firm", fm_checks)):
            for key, val in checks.items():
                if not val:
                    detail = f"{name}:{key}=False"
                    break
            if detail is not None:
                break
    return ok, detail, {"accounting": ac_checks, "kfe": kfe_checks, "firm": fm_checks}


def _damp(gamma: Sequence[float], gamma_hat: Sequence[float], lam: float):
    return tuple((1.0 - lam) * float(g) + lam * float(gh) for g, gh in zip(gamma, gamma_hat))


def _gamma_next(rec: OneTurnRecord, stop_reason: str, lam: float):
    """Deterministic ``Gamma_next`` for a trace row.

    Valid turns (including ACCEPTED / MAX_ITER_REACHED) expose the damped next
    state. Blocked terminal turns (no next state defined) expose deterministic
    NaN/null-equivalent fields.
    """
    if not rec.valid or _is_blocked_stop(stop_reason):
        return (float("nan"), float("nan"), float("nan"), float("nan"))
    return _damp(rec.gamma, rec.gamma_hat, lam)


# ---------------------------------------------------------------------------
# Experiments S0 / S1 / S2
# ---------------------------------------------------------------------------


def canonical_numbers(rec: OneTurnRecord) -> list[float]:
    """Fixed-order numeric record for exact comparisons (S2, reproducibility)."""
    out: list[float] = []
    out.extend(float(x) for x in rec.gamma)
    out.extend(float(x) for x in rec.wbar)
    for i in (0, 1):
        r = rec.region[i]
        bm = r.boundary_masses or {}
        out.extend(
            [
                r.C, r.L_home, r.A, r.B, r.C_tot, r.L_tot, r.A_tot, r.B_tot,
                1.0 if r.hjb_converged else 0.0, float(r.hjb_iterations), r.hjb_statistic,
                r.kfe_mass_error, r.kfe_min_density,
                bm.get("b_min", float("nan")), bm.get("b_max", float("nan")),
                bm.get("a_min", float("nan")), bm.get("a_max", float("nan")),
            ]
        )
    for i in (0, 1):
        try:
            frow = rec.F[i]
            f00 = frow[0]
            f01 = frow[1]
        except (IndexError, TypeError):
            f00 = float("nan")
            f01 = float("nan")
        out.extend(
            [
                f00, f01,
                _seq_safe(rec.Ldest, i), _seq_safe(rec.K, i), _seq_safe(rec.Y, i),
                _seq_safe(rec.w_hat, i), _seq_safe(rec.r_hat_a, i),
            ]
        )
    out.extend([rec.R_w, rec.R_ra])
    out.extend(_seq_safe(rec.gamma_hat, j) for j in range(4))
    return out


def _seq_safe(seq: Sequence, i: int) -> float:
    try:
        return float(seq[i])
    except (IndexError, TypeError):
        return float("nan")


def max_numeric_diff(a: Sequence[float], b: Sequence[float]) -> float:
    """Non-finite-aware elementwise maximum absolute difference (R1-C).

    - aligned ``NaN``/``NaN`` at the same position is treated as equal
      (structurally identical blocked rows);
    - ``NaN`` vs any finite value fails (returns ``inf``);
    - ``+Inf``/``+Inf`` and ``-Inf``/``-Inf`` aligned are equal; any Inf-sign
      mismatch, Inf-vs-finite, or other nonmatching non-finite pattern fails;
    - length mismatch fails.

    The result is ``inf`` on any structural non-finite mismatch, so Python's
    ``max`` ordering can never silently swallow a NaN mismatch.
    """
    if len(a) != len(b):
        return float("inf")
    max_d = 0.0
    for x, y in zip(a, b):
        x = float(x)
        y = float(y)
        if math.isnan(x) and math.isnan(y):
            continue
        if math.isnan(x) or math.isnan(y):
            return float("inf")
        if math.isinf(x) or math.isinf(y):
            if math.isinf(x) and math.isinf(y) and math.copysign(1.0, x) == math.copysign(1.0, y):
                continue
            return float("inf")
        d = abs(x - y)
        if d > max_d:
            max_d = d
    return max_d


@dataclasses.dataclass
class S0Result:
    record: OneTurnRecord
    pass_bool: bool
    reason: str
    accounting: dict
    kfe_checks: dict
    firm_checks: dict
    boundary: dict


def run_s0(cfg: TwoRegionConfig, grid, params, numerics, firm: FrozenFirmParams) -> S0Result:
    gamma0 = (cfg.w_star[0], cfg.w_star[1], cfg.r_a_star[0], cfg.r_a_star[1])
    rec = one_turn(gamma0, cfg, grid, params, numerics, firm, region_order=(0, 1))
    if not rec.valid:
        return S0Result(rec, False, rec.invalid_reason, {}, {}, {}, {})
    vb_ok, vb_detail, vb_checks = validity_bundle(cfg, rec)
    resid_ok = bool(rec.R_w <= cfg.s0_tol_w and rec.R_ra <= cfg.s0_tol_ra)
    boundary = boundary_warning(cfg, rec)
    ok = bool(vb_ok and resid_ok)
    reason = "PASS" if ok else "FAIL"
    if not ok:
        if not vb_ok:
            reason = f"FAIL_VALIDITY_BUNDLE:{vb_detail}"
        elif not resid_ok:
            reason = f"FAIL_RESIDUALS (R_w={rec.R_w}, R_ra={rec.R_ra})"
    return S0Result(rec, ok, reason, vb_checks["accounting"], vb_checks["kfe"], vb_checks["firm"], boundary)


@dataclasses.dataclass
class S1Result:
    trace: list
    stop_reason: str
    iterations: int
    converged: bool
    final_residuals: Optional[tuple]
    boundary_any_warning: bool


def run_s1(cfg: TwoRegionConfig, grid, params, numerics, firm: FrozenFirmParams) -> S1Result:
    gamma0 = (0.99, 1.01, 0.0295, 0.0305)  # frozen perturbed initial state
    trace: list = []
    gamma = gamma0
    any_warn = False
    for n in range(cfg.max_iter):
        rec = one_turn(gamma, cfg, grid, params, numerics, firm, region_order=(0, 1))
        trace.append(rec)
        if rec.valid:
            bm = boundary_warning(cfg, rec)
            any_warn = any_warn or any(bm[f"region{i}"]["warning"] for i in (0, 1))
        if not rec.valid:
            return S1Result(trace, rec.invalid_reason, n + 1, False, None, any_warn)
        # R1-A: full frozen validity bundle before residual acceptance and damping.
        vb_ok, vb_detail, _ = validity_bundle(cfg, rec)
        if not vb_ok:
            return S1Result(
                trace, f"VALIDITY_GATE_FAILED:{vb_detail}", n + 1, False, None, any_warn
            )
        if rec.R_w <= cfg.tol_w and rec.R_ra <= cfg.tol_ra:
            return S1Result(trace, "ACCEPTED", n + 1, True, (rec.R_w, rec.R_ra), any_warn)
        gamma = _damp(gamma, rec.gamma_hat, cfg.lambda_)
    last = trace[-1]
    return S1Result(
        trace, "MAX_ITER_REACHED", cfg.max_iter, False, (last.R_w, last.R_ra), any_warn
    )


@dataclasses.dataclass
class S2Result:
    max_diff: float
    pass_bool: bool
    record_order12: OneTurnRecord
    record_order21: OneTurnRecord


def run_s2(cfg: TwoRegionConfig, grid, params, numerics, firm: FrozenFirmParams) -> S2Result:
    gamma0 = (0.99, 1.01, 0.0295, 0.0305)
    r12 = one_turn(gamma0, cfg, grid, params, numerics, firm, region_order=(0, 1))
    r21 = one_turn(gamma0, cfg, grid, params, numerics, firm, region_order=(1, 0))
    diff = max_numeric_diff(canonical_numbers(r12), canonical_numbers(r21))
    ok = bool(diff <= cfg.order_invariance_tol) and bool(r12.valid) and bool(r21.valid)
    return S2Result(diff, ok, r12, r21)


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(x) for x in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return float(obj)
    if isinstance(obj, float):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, bool):
        return obj
    if obj is None:
        return None
    return str(obj)


def write_json(path: pathlib.Path, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(_json_safe(payload), fh, indent=1, sort_keys=True)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest().upper()


# ---------------------------------------------------------------------------
# Experiment runner (CLI)
# ---------------------------------------------------------------------------


S0_TRACE_FIELDS = [
    "w1", "w2", "ra1", "ra2", "wbar1", "wbar2",
    "C1", "L1", "A1", "B1", "C1tot", "L1tot", "A1tot", "B1tot",
    "C2", "L2", "A2", "B2", "C2tot", "L2tot", "A2tot", "B2tot",
    "hjb_it1", "hjb_stat1", "kfe_mass1", "kfe_mind1",
    "bm_bmin1", "bm_bmax1", "bm_amin1", "bm_amax1",
    "hjb_it2", "hjb_stat2", "kfe_mass2", "kfe_mind2",
    "bm_bmin2", "bm_bmax2", "bm_amin2", "bm_amax2",
    "F11", "F12", "F21", "F22", "Ldest1", "Ldest2", "K1", "K2",
    "Y1", "Y2", "what1", "what2", "rhat1", "rhat2",
    "Rw", "Rra", "gamma_hat_w1", "gamma_hat_w2", "gamma_hat_ra1", "gamma_hat_ra2",
    "P11", "P12", "P21", "P22", "lambda",
    "gamma_next_w1", "gamma_next_w2", "gamma_next_ra1", "gamma_next_ra2",
    "stop_reason",
]


def _trace_row(rec: OneTurnRecord, stop_reason: str, cfg: TwoRegionConfig) -> list:
    r0 = rec.region[0]
    r1 = rec.region[1]
    bm0 = r0.boundary_masses or {}
    bm1 = r1.boundary_masses or {}

    def aggr(r):
        return [r.C, r.L_home, r.A, r.B, r.C_tot, r.L_tot, r.A_tot, r.B_tot]

    def seq(name, i):
        try:
            return getattr(rec, name)[i]
        except (IndexError, TypeError):
            return float("nan")

    def fval(i, j):
        try:
            return rec.F[i][j]
        except (IndexError, TypeError):
            return float("nan")

    gnext = _gamma_next(rec, stop_reason, cfg.lambda_)
    return [
        rec.gamma[0], rec.gamma[1], rec.gamma[2], rec.gamma[3],
        rec.wbar[0], rec.wbar[1],
        *aggr(r0),
        *aggr(r1),
        r0.hjb_iterations, r0.hjb_statistic, r0.kfe_mass_error, r0.kfe_min_density,
        bm0.get("b_min", float("nan")), bm0.get("b_max", float("nan")),
        bm0.get("a_min", float("nan")), bm0.get("a_max", float("nan")),
        r1.hjb_iterations, r1.hjb_statistic, r1.kfe_mass_error, r1.kfe_min_density,
        bm1.get("b_min", float("nan")), bm1.get("b_max", float("nan")),
        bm1.get("a_min", float("nan")), bm1.get("a_max", float("nan")),
        fval(0, 0), fval(0, 1), fval(1, 0), fval(1, 1),
        seq("Ldest", 0), seq("Ldest", 1), seq("K", 0), seq("K", 1),
        seq("Y", 0), seq("Y", 1), seq("w_hat", 0), seq("w_hat", 1),
        seq("r_hat_a", 0), seq("r_hat_a", 1),
        rec.R_w, rec.R_ra,
        seq("gamma_hat", 0), seq("gamma_hat", 1), seq("gamma_hat", 2), seq("gamma_hat", 3),
        cfg.P_L[0][0], cfg.P_L[0][1], cfg.P_L[1][0], cfg.P_L[1][1], cfg.lambda_,
        gnext[0], gnext[1], gnext[2], gnext[3],
        stop_reason,
    ]


def write_csv(path: pathlib.Path, fields: list, rows: list) -> None:
    import csv

    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(fields)
        for row in rows:
            writer.writerow([_fmt(x) for x in row])


def _fmt(x: Any) -> str:
    if isinstance(x, float):
        return repr(x)
    return str(x)


def _write_trace_csv(cfg: TwoRegionConfig, path: pathlib.Path, trace: list, stop_reason: str) -> None:
    rows = []
    for n, rec in enumerate(trace):
        rows.append(
            [n] + _trace_row(rec, stop_reason if n == len(trace) - 1 else "", cfg)
        )
    write_csv(path, ["iter"] + S0_TRACE_FIELDS, rows)


def _reproduce_s0(cfg, grid, params, numerics, firm):
    # Run S0 twice from fresh construction (fresh fixture objects).
    g1, p1, n1 = build_fixture(cfg)
    r1 = run_s0(cfg, g1, p1, n1, firm)
    g2, p2, n2 = build_fixture(cfg)
    r2 = run_s0(cfg, g2, p2, n2, firm)
    diff = max_numeric_diff(canonical_numbers(r1.record), canonical_numbers(r2.record))
    return {
        "pass_bool": bool(r1.pass_bool and r2.pass_bool),
        "max_numeric_diff": diff,
        "same_stop_reason": bool(r1.reason == r2.reason),
        "reason1": r1.reason,
        "reason2": r2.reason,
        "within_tol": bool(diff <= cfg.reproducibility_tol),
    }


def _reproduce_s1(cfg, grid, params, numerics, firm):
    # Run S1 twice from the same frozen config (fresh construction each run).
    g1, p1, n1 = build_fixture(cfg)
    r1 = run_s1(cfg, g1, p1, n1, firm)
    g2, p2, n2 = build_fixture(cfg)
    r2 = run_s1(cfg, g2, p2, n2, firm)
    max_diff = 0.0
    for a, b in zip(r1.trace, r2.trace):
        d = max_numeric_diff(canonical_numbers(a), canonical_numbers(b))
        max_diff = max(max_diff, d)
    return {
        "pass_bool": bool(r1.stop_reason == r2.stop_reason and r1.iterations == r2.iterations),
        "stop_reason1": r1.stop_reason,
        "stop_reason2": r2.stop_reason,
        "iterations1": r1.iterations,
        "iterations2": r2.iterations,
        "max_trace_numeric_diff": max_diff,
        "within_tol": bool(max_diff <= cfg.reproducibility_tol),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="DLH-5B two-region fixed-point experiment")
    parser.add_argument("--config", required=True, help="frozen TOML config path")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)

    root = pathlib.Path(cfg.output_root)
    if root.exists():
        print(f"BLOCKED_DLH_5B_OUTPUT_PATH_EXISTS: {root}", file=sys.stderr)
        return 3

    grid, params, numerics = build_fixture(cfg)

    # 1) one-shot anchor derivation (Z*, delta*) then frozen.
    anchor = derive_anchor(cfg, grid, params, numerics)
    firm = FrozenFirmParams(
        Z=(anchor.Z_star, anchor.Z_star),
        delta=(anchor.delta_star, anchor.delta_star),
        alpha=(cfg.alpha[0], cfg.alpha[1]),
    )
    print(f"anchor: A*={anchor.A_star:.9g} L*={anchor.L_star:.9g} "
          f"C*={anchor.C_star:.9g} B*={anchor.B_star:.9g}")
    print(f"derived: Z*={anchor.Z_star:.9g} delta*={anchor.delta_star:.9g}")

    root.mkdir(parents=True, exist_ok=False)

    # 2) S0 anchor smoke.
    s0 = run_s0(cfg, grid, params, numerics, firm)
    s0_repro = _reproduce_s0(cfg, grid, params, numerics, firm)
    write_json(
        root / "DLH_5B_ANCHOR_FIXTURE.json",
        {
            "status": "ok",
            "A_star": anchor.A_star, "L_star": anchor.L_star, "C_star": anchor.C_star,
            "B_star": anchor.B_star, "K_star": anchor.K_star, "Ldest_star": anchor.Ldest_star,
            "Z_star": anchor.Z_star, "delta_star": anchor.delta_star, "alpha": anchor.alpha,
            "sanity": anchor.sanity,
            "region0": {
                "hjb_converged": anchor.region.hjb_converged,
                "hjb_iterations": anchor.region.hjb_iterations,
                "hjb_statistic": anchor.region.hjb_statistic,
                "kfe_mass_error": anchor.region.kfe_mass_error,
                "kfe_min_density": anchor.region.kfe_min_density,
                "boundary_masses": anchor.region.boundary_masses,
            },
            "frozen_for_all_cases": True,
        },
    )
    _write_trace_csv(cfg, root / "DLH_5B_S0_ANCHOR_TRACE.csv", [s0.record], s0.reason)

    s1 = None
    s2 = None
    s1_repro = None
    if s0.pass_bool:
        # 3) S1 only if S0 passed.
        s1 = run_s1(cfg, grid, params, numerics, firm)
        s1_repro = _reproduce_s1(cfg, grid, params, numerics, firm)
        _write_trace_csv(cfg, root / "DLH_5B_S1_PERTURBED_TRACE.csv", s1.trace, s1.stop_reason)
        # 4) S2 region-order invariance.
        s2 = run_s2(cfg, grid, params, numerics, firm)
        write_json(
            root / "DLH_5B_ORDER_INVARIANCE.json",
            {
                "max_numeric_difference": s2.max_diff,
                "tol": cfg.order_invariance_tol,
                "pass_bool": s2.pass_bool,
                "order12_valid": s2.record_order12.valid,
                "order21_valid": s2.record_order21.valid,
            },
        )
    else:
        _write_trace_csv(cfg, root / "DLH_5B_S1_PERTURBED_TRACE.csv", [s0.record], "S0_FAILED_NOT_RUN")
        write_json(
            root / "DLH_5B_ORDER_INVARIANCE.json",
            {"max_numeric_difference": None, "pass_bool": False, "skipped": True},
        )

    # reproducibility
    write_json(
        root / "DLH_5B_REPRODUCIBILITY.json",
        {"randomness": "NOT_APPLICABLE", "s0": s0_repro, "s1": s1_repro},
    )

    # execution report + forbidden check (generated inside this allowlisted module)
    _write_execution_report(cfg, root, anchor, s0, s1, s2, s0_repro, s1_repro)
    _write_forbidden_check(cfg, root, s0, s1, s2, s0_repro, s1_repro)
    print(f"artifacts written under {root}")
    return 0


def _terminal_classification(cfg: TwoRegionConfig, s0, s1, s2, s0_repro, s1_repro) -> str:
    """Map the frozen experiment outcome to the Issue #25 terminal classes.

    R1-D: fail closed on S2 order-invariance failure and on S0/S1
    reproducibility failure. An ``ARCHITECTURE_VALIDATED`` class is emitted only
    when order invariance and both reproducibility checks pass.
    """
    if s0 is None or not s0.pass_bool:
        return "BLOCKED_DLH_5B_S0_ANCHOR_RESIDUAL_OR_VALIDITY_GATE_FAILED"
    if s0_repro is None or not s0_repro.get("pass_bool", False) or not s0_repro.get("within_tol", False):
        return "BLOCKED_DLH_5B_S0_REPRODUCIBILITY_FAILED"
    if s1 is None:
        return "BLOCKED_DLH_5B_S1_NOT_RUN"
    if s1_repro is None or not s1_repro.get("pass_bool", False) or not s1_repro.get("within_tol", False):
        return "BLOCKED_DLH_5B_S1_REPRODUCIBILITY_FAILED"
    if s2 is None or not s2.pass_bool:
        return "BLOCKED_DLH_5B_S2_ORDER_INVARIANCE_FAILED"
    if s1.stop_reason == "ACCEPTED":
        return "DLH_5B_TWO_REGION_ANCHOR_AND_PERTURBED_FIXED_POINT_CONVERGED__READY_FOR_GPT_REVIEW"
    if s1.stop_reason.startswith("HOUSEHOLD_BLOCK_FAILED"):
        return "DLH_5B_TWO_REGION_ARCHITECTURE_VALIDATED__PERTURBED_PATH_HOUSEHOLD_BLOCKED_READY_FOR_GPT_REVIEW"
    if s1.stop_reason.startswith("VALIDITY_GATE_FAILED"):
        return "DLH_5B_TWO_REGION_ARCHITECTURE_VALIDATED__PERTURBED_PATH_VALIDITY_GATE_FAILED_READY_FOR_GPT_REVIEW"
    # MAX_ITER_REACHED or INVALID_FIRM_STATE (fail-closed, preserved negative evidence)
    return "DLH_5B_TWO_REGION_ARCHITECTURE_VALIDATED__PERTURBED_FIXED_POINT_NONCONVERGENT_READY_FOR_GPT_REVIEW"


def _artifact_hashes(root: pathlib.Path) -> dict:
    hashes = {}
    for path in sorted(root.iterdir()):
        if path.is_file():
            hashes[path.name] = sha256_file(path)
    return hashes


# ---------------------------------------------------------------------------
# Predecessor vs R1 comparison (R1 report evidence)
# ---------------------------------------------------------------------------

PREDECESSOR_ROOT = pathlib.Path("reports/dlh_5b_two_region_fixed_point_2026_08_31")


def _parse_num(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def _read_json_file(path: pathlib.Path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None


def _read_csv_rows(path: pathlib.Path):
    import csv

    try:
        with open(path, newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except FileNotFoundError:
        return None


def _compare_trace_csv(pred_path: pathlib.Path, r1_path: pathlib.Path) -> dict:
    pr = _read_csv_rows(pred_path)
    rr = _read_csv_rows(r1_path)
    if pr is None or rr is None:
        return {"available": False, "note": "trace file missing in predecessor or R1 root"}
    if len(pr) != len(rr):
        return {
            "available": True, "row_count": (len(pr), len(rr)), "identical": False,
            "reason": "row count differs",
        }
    common_cols = [c for c in pr[0] if c in rr[0] and c not in ("iter", "stop_reason")]
    max_diff = 0.0
    for a, b in zip(pr, rr):
        va = [_parse_num(a[c]) for c in common_cols]
        vb = [_parse_num(b[c]) for c in common_cols]
        max_diff = max(max_diff, max_numeric_diff(va, vb))
    same_stop = pr[-1].get("stop_reason", "") == rr[-1].get("stop_reason", "")
    return {
        "available": True, "row_count": (len(pr), len(rr)), "common_cols": len(common_cols),
        "max_numeric_diff": max_diff, "same_final_stop_reason": same_stop,
        "identical": bool(max_diff <= 1e-12 and same_stop),
    }


def _compare_anchor_json(pred_path: pathlib.Path, r1_path: pathlib.Path) -> dict:
    pa = _read_json_file(pred_path)
    ra = _read_json_file(r1_path)
    if pa is None or ra is None:
        return {"available": False, "note": "anchor file missing in predecessor or R1 root"}
    fields = ["A_star", "L_star", "C_star", "B_star", "K_star", "Ldest_star", "Z_star", "delta_star", "alpha"]
    differing = {}
    max_d = 0.0
    for f in fields:
        x = _parse_num(pa.get(f))
        y = _parse_num(ra.get(f))
        if math.isnan(x) or math.isnan(y):
            continue
        d = abs(x - y)
        max_d = max(max_d, d)
        if d > 1e-12:
            differing[f] = d
    return {"available": True, "max_abs_diff": max_d, "differing_fields": differing, "identical": not differing}


def _compare_json_equality(pred_path: pathlib.Path, r1_path: pathlib.Path, fields) -> dict:
    pa = _read_json_file(pred_path)
    ra = _read_json_file(r1_path)
    if pa is None or ra is None:
        return {"available": False, "note": "json file missing in predecessor or R1 root"}
    out = {}
    for f in fields:
        out[f] = {"pred": pa.get(f), "r1": ra.get(f), "equal": pa.get(f) == ra.get(f)}
    return {"available": True, "fields": out}


def compare_predecessor_r1(pred_root: pathlib.Path, r1_root: pathlib.Path) -> dict:
    """Deterministic comparison of the preserved predecessor vs the R1 evidence."""
    anchor = _compare_anchor_json(
        pred_root / "DLH_5B_ANCHOR_FIXTURE.json", r1_root / "DLH_5B_ANCHOR_FIXTURE.json"
    )
    s0 = _compare_trace_csv(
        pred_root / "DLH_5B_S0_ANCHOR_TRACE.csv", r1_root / "DLH_5B_S0_ANCHOR_TRACE.csv"
    )
    s1 = _compare_trace_csv(
        pred_root / "DLH_5B_S1_PERTURBED_TRACE.csv", r1_root / "DLH_5B_S1_PERTURBED_TRACE.csv"
    )
    s2 = _compare_json_equality(
        pred_root / "DLH_5B_ORDER_INVARIANCE.json", r1_root / "DLH_5B_ORDER_INVARIANCE.json",
        ["max_numeric_difference", "tol", "pass_bool"],
    )
    repro = _compare_json_equality(
        pred_root / "DLH_5B_REPRODUCIBILITY.json", r1_root / "DLH_5B_REPRODUCIBILITY.json",
        ["s0", "s1"],
    )
    return {"anchor": anchor, "s0": s0, "s1": s1, "s2": s2, "reproducibility": repro}


def _write_execution_report(cfg, root, anchor, s0, s1, s2, s0_repro, s1_repro) -> None:
    terminal = _terminal_classification(cfg, s0, s1, s2, s0_repro, s1_repro)
    lines: list[str] = []
    lines.append("# DLH-5B — Two-Region Fixed-Point Execution Report (Issue #25)")
    lines.append("")
    lines.append("Terminal classification:")
    lines.append("")
    lines.append(f"`{terminal}`")
    lines.append("")
    if s0 is not None and s0.pass_bool and s1 is not None and s1.boundary_any_warning:
        lines.append(
            "Qualification: `PASS_WITH_OBSERVATIONS` — a boundary-mass warning "
            "(threshold 0.10) was observed; surfaced, non-blocking for this "
            "architecture-validation stage."
        )
        lines.append("")
    lines.append("## Fixture identity")
    lines.append("")
    lines.append("- Accepted household oracle: `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` (immutable).")
    lines.append("- Frozen config: `configs/dlh_5b_two_region_symmetric_anchor.toml` (not modified after seeing results).")
    lines.append("- Household fixture: `VALIDATION_FIXTURE_NOT_CALIBRATION` from `tests/test_dlh_4b_transfer.py`.")
    lines.append(f"- Network: `M={list(cfg.M)}`, `m_L={list(cfg.m_L)}`, `P^L={[list(r) for r in cfg.P_L]}`.")
    lines.append(f"- Anchor: `w*={list(cfg.w_star)}`, `r_a*={list(cfg.r_a_star)}`, `alpha={list(cfg.alpha)}`.")
    lines.append("")
    lines.append("## R1 bounded-repair record (GPT review 2026-08-31, same Issue #25)")
    lines.append("")
    lines.append("- A: S1 enforces the full frozen validity bundle (accounting/network + KFE + firm) on every valid turn, before residual acceptance and before damping; any failure stops with `VALIDITY_GATE_FAILED:<deterministic detail>` and the turn stays in the trace.")
    lines.append("- B: every trace row now carries full `P^L` (`P11,P12,P21,P22`), `lambda`, and `Gamma_next={w1,w2,ra1,ra2}`; blocked terminal turns record deterministic NaN/null-equivalent `Gamma_next` and the exact stop reason.")
    lines.append("- C: `max_numeric_diff` is non-finite aware (aligned NaN/NaN equal; NaN-vs-finite, Inf-sign mismatch or other nonfinite mismatch -> failure/Inf).")
    lines.append("- D: terminal classification fail-closes on S2 order-invariance failure and on S0/S1 reproducibility failure; an `ARCHITECTURE_VALIDATED` class is emitted only when all of those pass.")
    lines.append("- E: focused tests added for all of the above plus S0/S1 predecessor-outcome no-regression.")
    lines.append("- F: exact frozen scientific fixture re-run into the R1 no-overwrite root; the ONLY config mutation is `output.root` -> `reports/dlh_5b_two_region_fixed_point_r1_2026_08_31/`. All household/grid/network/anchor/lambda/tolerance/max_iter fields remain value-identical to the predecessor config.")
    lines.append("")
    lines.append("## Derived anchor (derived once, then frozen for all cases)")
    lines.append("")
    lines.append(f"| object | value |")
    lines.append("|---|---|")
    lines.append(f"| `A*` | {anchor.A_star:.12g} |")
    lines.append(f"| `L*` | {anchor.L_star:.12g} |")
    lines.append(f"| `C*` | {anchor.C_star:.12g} |")
    lines.append(f"| `B*` | {anchor.B_star:.12g} |")
    lines.append(f"| `K*` (=M A*) | {anchor.K_star:.12g} |")
    lines.append(f"| `Z*` | {anchor.Z_star:.12g} |")
    lines.append(f"| `delta*` | {anchor.delta_star:.12g} |")
    lines.append("")
    lines.append(f"Sanity gate: {anchor.sanity}")
    lines.append("")
    lines.append(f"Anchor HJB: converged={anchor.region.hjb_converged}, "
                 f"iterations={anchor.region.hjb_iterations}, "
                 f"statistic={anchor.region.hjb_statistic:.3e}")
    lines.append(f"Anchor KFE: mass_error={anchor.region.kfe_mass_error:.3e}, "
                 f"min_density={anchor.region.kfe_min_density:.3e}")
    lines.append("")
    lines.append("## S0 — anchor smoke (one-turn from Gamma0={1,1,0.03,0.03})")
    lines.append("")
    if s0 is not None:
        lines.append(f"- gate: `{s0.reason}`")
        lines.append(f"- `R_w` = {s0.record.R_w:.3e} (required <= {cfg.s0_tol_w})")
        lines.append(f"- `R_ra` = {s0.record.R_ra:.3e} (required <= {cfg.s0_tol_ra})")
        lines.append(f"- accounting: {s0.accounting}")
        lines.append(f"- KFE checks: {s0.kfe_checks}")
        lines.append(f"- firm checks: {s0.firm_checks}")
        lines.append(f"- boundary masses: {s0.boundary}")
        lines.append("")
    lines.append("## S1 — perturbed outer iteration")
    lines.append("")
    if s1 is not None:
        lines.append(f"- stop reason: `{s1.stop_reason}`")
        lines.append(f"- iteration count: {s1.iterations} (max_iter={cfg.max_iter})")
        if s1.final_residuals is not None:
            lines.append(f"- final `R_w` = {s1.final_residuals[0]:.3e} (tol {cfg.tol_w})")
            lines.append(f"- final `R_ra` = {s1.final_residuals[1]:.3e} (tol {cfg.tol_ra})")
        lines.append(f"- boundary warning observed: {s1.boundary_any_warning}")
        lines.append("")
    lines.append("## S2 — region-order invariance (S1 initial snapshot)")
    lines.append("")
    if s2 is not None:
        lines.append(f"- max one-turn numeric difference (order [1,2] vs [2,1]): "
                     f"{s2.max_diff:.3e} (required <= {cfg.order_invariance_tol})")
        lines.append(f"- pass: {s2.pass_bool}")
        lines.append("")
    lines.append("## Reproducibility (randomness NOT_APPLICABLE)")
    lines.append("")
    lines.append(f"- S0 repeat: {s0_repro}")
    lines.append(f"- S1 repeat: {s1_repro}")
    lines.append("")
    lines.append("## Predecessor vs R1 comparison (preserved root vs R1 root)")
    lines.append("")
    lines.append(f"Predecessor root: `{PREDECESSOR_ROOT}` (unchanged). R1 root: `{cfg.output_root}`.")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(compare_predecessor_r1(PREDECESSOR_ROOT, root), indent=1, default=str))
    lines.append("```")
    lines.append("")
    lines.append("## Artifact identities (SHA-256)")
    lines.append("")
    for name, h in sorted(_artifact_hashes(root).items()):
        lines.append(f"- `{name}`: `{h}`")
    lines.append("")
    lines.append("## Notes / caveats")
    lines.append("")
    lines.append("- No automatic retry, adaptive damping, grid expansion or PASS-seeking tuning was used.")
    lines.append("- HJB/KFE/boundary failures are preserved as diagnostics; nothing was silently discarded.")
    lines.append("- `B_i` is a household liquid-asset diagnostic only; no `B=1` closure was used.")
    lines.append("- `K_i = M_i * A_i` is the provisional NSR-HANK exploratory closure; not empirical calibration.")
    lines.append("- Outer map uses fixed damping only; no Brent/Newton/fsolve.")
    lines.append("")
    with open(root / "DLH_5B_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def _write_forbidden_check(cfg: TwoRegionConfig, root: pathlib.Path, s0, s1, s2, s0_repro, s1_repro) -> None:
    lines = [
        "# DLH-5B — Forbidden-Operation / Scope Check (Issue #25)",
        "",
        "DSH did NOT perform any of the following during Issue #25 execution (including R1 repair):",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify the accepted two-asset household oracle | NOT performed (immutable) |",
        "| Reintroduce `B_hh=B_gov=1` / fixed bond-supply GE root | NOT performed |",
        "| Brent/Newton/fsolve for the outer regional fixed point | NOT performed (fixed damping only; Brent used solely in the accepted household initial-value fixture) |",
        "| Change scientific/numerical fixture fields after seeing results | NOT performed (config frozen; only `output.root` mutated for the R1 root) |",
        "| Adaptive damping / automatic retry | NOT performed (`NO_AUTOMATIC_RETRY`) |",
        "| Grid expansion | NOT performed |",
        "| `GovInv` / GDP-target controller | NOT performed |",
        "| `W^K` / capital-flow learning | NOT performed |",
        "| Neural network / learned `W^L` | NOT performed |",
        "| Nominal rigidity / Phillips / Taylor / Fisher / new debt closure | NOT performed |",
        "| 31-region scaling | NOT performed |",
        "| Policy/welfare/Results claims | NOT performed |",
        "| Modify existing single-region GE code (`src/deep_learning_hank/ge/**`) | NOT performed |",
        "| Modify accepted household source / prior configs/tests/reports / roadmap / governance / legacy roots | NOT performed |",
        "| Overwrite predecessor evidence root (`reports/dlh_5b_two_region_fixed_point_2026_08_31`) | NOT performed (preserved unchanged) |",
        "| `git add .` / `git add -A` | NOT performed (explicit staging only) |",
        "| Self-accept / merge / close Issue / PR / successor Issue | NOT performed |",
        "",
        "Execution discipline: no-overwrite output root "
        f"`{cfg.output_root}` (STOP if pre-existing), `NO_AUTOMATIC_RETRY`.",
        "",
        "Fail-closed gates: S0 validity bundle + residuals, S1 per-turn validity "
        "bundle, S2 order invariance, S0/S1 reproducibility.",
        "",
        "Terminal classification: "
        f"`{_terminal_classification(cfg, s0, s1, s2, s0_repro, s1_repro)}`",
        "",
    ]
    with open(root / "DLH_5B_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    raise SystemExit(main())
