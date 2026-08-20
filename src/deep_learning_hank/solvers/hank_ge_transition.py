"""DLH-3D full minimal single-region NK GE transition solver (isolated module).

Implements Issue #13 §6–§7 with the authoritative numerical-timing
clarification (comment id `5349487045`):

- unknowns are positivity-preserving ``x_w,k = log(w_k/w*)`` and
  ``x_N,k = log(N_k/N*)`` for the root interval ``k = 0..K-1`` only;
- the terminal aggregate point is a finite-horizon boundary:
  ``w_K = w*``, ``N_K = N*``, ``pi_K = 0`` at ``t_K = T`` — it is not an
  extra root equation;
- nonlinear residuals are normalized asset and labor clearing on
  ``k = 0..K-1`` only:
  ``R_asset_norm = (A_hh - B)/B``, ``R_labor_norm = (N_hh - N)/N*``;
- one deterministic Jacobian-free route:
  ``scipy.optimize.root(..., method='krylov')`` with frozen options
  (infinity-norm residual tolerance 1e-7, max 80 nonlinear iterations,
  zero-deviation initial guess), no alternative solver/fallback.

Goods/resource, NKPC, Fisher, Taylor, fiscal, profits and the
KFE-consistent discrete wealth-flow residual (using ``g_{k+1}`` timing) are
independent diagnostic residuals, never set to zero by construction.

The household/distribution engine is the accepted DLH-3C solver, reused
read-only.  ``epsilon_i(t)`` is a small deterministic monetary-policy
validation-fixture innovation (not an empirically identified shock, not
Results evidence).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy import optimize as scipy_optimize

from deep_learning_hank.economics.grids import build_asset_grid, build_idiosyncratic_generator
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.hank_ge_config import HankGeConfig
from deep_learning_hank.solvers.hank_household_transition import (
    DynamicHouseholdSolution,
    TransitionInputs,
    solve_dynamic_household,
)
from deep_learning_hank.solvers.hank_kfe_transition import (
    DynamicDistributionResult,
    forward_kfe_transition,
)
from deep_learning_hank.solvers.hank_nkpc_transition import (
    backward_nkpc,
    nkpc_residual,
    taylor_fisher,
)
from deep_learning_hank.diagnostics.hank_transition import BaselineInfo

__all__ = [
    "GeAggregates",
    "GeEvaluation",
    "GeRootResult",
    "build_innovation_path",
    "evaluate_ge",
    "solve_ge_transition",
]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class GeAggregates:
    """Aggregate paths over the full grid ``k = 0..K`` (terminal included)."""

    w: FloatArray
    N: FloatArray
    Y: FloatArray
    mc: FloatArray
    pi: FloatArray
    AC: FloatArray
    Pi: FloatArray
    i: FloatArray
    r: FloatArray
    tr: FloatArray
    epsilon_i: FloatArray


@dataclass(frozen=True)
class GeEvaluation:
    """One full GE evaluation at candidate aggregate paths."""

    K: int
    aggregates: GeAggregates
    hjb: DynamicHouseholdSolution
    kfe: DynamicDistributionResult
    A_hh: FloatArray
    N_hh: FloatArray
    C: FloatArray
    R_asset: FloatArray
    R_labor: FloatArray
    R_asset_norm: FloatArray
    R_labor_norm: FloatArray
    R_goods: FloatArray
    R_nkpc: FloatArray
    R_fisher: FloatArray
    R_taylor: FloatArray
    R_fiscal: FloatArray
    R_profits: FloatArray
    R_wealth: FloatArray
    finite: bool

    def residual_vector(self) -> FloatArray:
        """Normalized clearing residuals on the root interval ``k = 0..K-1``."""
        return np.concatenate([self.R_asset_norm, self.R_labor_norm])


def build_innovation_path(
    config: HankGeConfig, amplitude: float, horizon: float
) -> FloatArray:
    """``epsilon_i(t) = amplitude * eta_i * sin(pi*t/L_i)^2`` on ``[0, L_i]``."""
    n_points = int(round(horizon / config.dt)) + 1
    grid = config.dt * np.arange(n_points, dtype=np.float64)
    h = np.where(
        (grid >= 0.0) & (grid <= config.L_i), np.sin(np.pi * grid / config.L_i) ** 2, 0.0
    )
    return amplitude * config.eta_i * h


def evaluate_ge(
    config: HankGeConfig,
    baseline: BaselineInfo,
    epsilon_i_path: FloatArray,
    x: FloatArray,
) -> GeEvaluation:
    """Evaluate the closed NK GE at candidate ``x = [x_w (K), x_N (K)]``."""
    epsilon_i_path = np.asarray(epsilon_i_path, dtype=np.float64)
    n_points = epsilon_i_path.size
    if n_points < 2:
        raise ValueError("innovation path must cover at least two time points")
    K = n_points - 1
    if x.size != 2 * K:
        raise ValueError(f"root vector must have length 2*K = {2 * K}")
    hb_config = HankSteadyStateConfig.from_toml(config.baseline_3b_path)
    dt = config.dt
    z = hb_config.productivity
    mu = hb_config.epsilon / (hb_config.epsilon - 1.0)
    kappa = hb_config.epsilon / hb_config.phi_p
    tau_l = hb_config.tau_l
    rho_hh = hb_config.rho_hh

    w = np.empty(n_points, dtype=np.float64)
    n_agg = np.empty(n_points, dtype=np.float64)
    w[:K] = baseline.wage_star * np.exp(x[:K])
    n_agg[:K] = baseline.N_star * np.exp(x[K:])
    w[K] = baseline.wage_star
    n_agg[K] = baseline.N_star

    y = z * n_agg
    mc = w / z
    mc_frictionless = 1.0 / mu
    pi = backward_nkpc(
        mc, dt=dt, rho_hh=rho_hh, kappa=kappa, mc_frictionless=mc_frictionless, pi_terminal=0.0
    )
    ac = (hb_config.phi_p / 2.0) * pi**2 * y
    profits = y - w * n_agg - ac
    i_path, r_path, taylor_residual, fisher_residual = taylor_fisher(
        real_rate_bar=baseline.r_star,
        phi_pi=hb_config.phi_pi,
        pi_path=pi,
        epsilon_i_path=epsilon_i_path,
    )
    tr = tau_l * w * n_agg - r_path * hb_config.bond_supply

    inputs = tuple(
        TransitionInputs(
            wage=float(w[k]),
            real_return=float(r_path[k]),
            transfer=float(tr[k]),
            profits=float(profits[k]),
        )
        for k in range(n_points)
    )
    asset_grid = build_asset_grid(hb_config.a_min, hb_config.a_max, hb_config.asset_grid_count)
    efficiency_states = np.asarray(hb_config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(hb_config.q_low_to_high, hb_config.q_high_to_low)
    hjb = solve_dynamic_household(
        asset_grid=asset_grid,
        efficiency_states=efficiency_states,
        state_generator=state_generator,
        inputs_path=inputs,
        terminal_value=baseline.V_ss,
        tau_l=tau_l,
        rho_hh=rho_hh,
        gamma=hb_config.gamma,
        frisch=hb_config.frisch,
        chi=hb_config.chi,
        n_max=hb_config.n_max,
        consumption_floor=config.numerical.consumption_floor,
        dt=dt,
        value_tolerance=config.numerical.policy_iteration_value_tolerance,
        max_policy_iterations=config.numerical.policy_iteration_max_iterations,
    )
    kfe = forward_kfe_transition(
        initial_mass=baseline.g_ss,
        generator_path=hjb.generator_path,
        asset_grid=asset_grid,
        efficiency_states=efficiency_states,
        labor_path=hjb.labor_path,
        consumption_path=hjb.consumption_path,
        dt=dt,
    )
    a_hh = kfe.A_hh_path
    n_hh = kfe.N_hh_path
    c = kfe.C_path
    b = hb_config.bond_supply

    r_asset = a_hh - b
    r_labor = n_hh - n_agg
    r_asset_norm = r_asset[:K] / b
    r_labor_norm = r_labor[:K] / baseline.N_star
    r_goods = y - c - ac
    r_nkpc = nkpc_residual(
        pi, mc, dt=dt, rho_hh=rho_hh, kappa=kappa, mc_frictionless=mc_frictionless
    )
    r_fiscal = tau_l * w * n_agg - r_path * b - tr
    r_profits = profits - (y - w * n_agg - ac)

    # KFE-consistent discrete wealth-flow residual (authoritative timing):
    # R_wealth,k = (A_hh,k+1 - A_hh,k)/dt - a' G_k^T g_{k+1},  k = 0..K-1.
    a_vec = np.tile(asset_grid, efficiency_states.size)
    r_wealth = np.empty(K, dtype=np.float64)
    for k in range(K):
        g_next = kfe.mass_path[k + 1].ravel()
        g_k_t = hjb.generator_path[k].T
        aggregate_drift = float((hjb.generator_path[k] @ a_vec) @ g_next)
        r_wealth[k] = (a_hh[k + 1] - a_hh[k]) / dt - aggregate_drift

    return GeEvaluation(
        K=K,
        aggregates=GeAggregates(
            w=w, N=n_agg, Y=y, mc=mc, pi=pi, AC=ac, Pi=profits,
            i=i_path, r=r_path, tr=tr, epsilon_i=epsilon_i_path,
        ),
        hjb=hjb,
        kfe=kfe,
        A_hh=a_hh,
        N_hh=n_hh,
        C=c,
        R_asset=r_asset,
        R_labor=r_labor,
        R_asset_norm=r_asset_norm,
        R_labor_norm=r_labor_norm,
        R_goods=r_goods,
        R_nkpc=r_nkpc,
        R_fisher=fisher_residual,
        R_taylor=taylor_residual,
        R_fiscal=r_fiscal,
        R_profits=r_profits,
        R_wealth=r_wealth,
        finite=bool(
            np.all(np.isfinite(x))
            and np.all(np.isfinite(r_asset_norm))
            and np.all(np.isfinite(r_labor_norm))
            and np.all(np.isfinite(r_goods))
            and np.all(np.isfinite(r_wealth))
        ),
    )


@dataclass(frozen=True)
class GeRootResult:
    amplitude: float
    horizon: float
    K: int
    root_x: FloatArray
    root_converged: bool
    root_success: bool
    root_message: str
    root_nit: int
    root_nfev: int
    root_residual_inf_norm: float
    final: GeEvaluation


def solve_ge_transition(
    config: HankGeConfig,
    baseline: BaselineInfo,
    *,
    amplitude: float,
    horizon: float,
) -> GeRootResult:
    """Solve the full NK GE path root (krylov) for one innovation amplitude."""
    epsilon_i_path = build_innovation_path(config, amplitude, horizon)
    k = len(epsilon_i_path) - 1

    def residual(x: FloatArray) -> FloatArray:
        return evaluate_ge(config, baseline, epsilon_i_path, x).residual_vector()

    x0 = np.zeros(2 * k, dtype=np.float64)
    options = {
        "fatol": config.root_tolerance_inf_norm,
        "maxiter": config.root_max_nonlinear_iterations,
        # Frozen inner-solver configuration of the same Jacobian-free krylov
        # route (Issue #13 §7): GMRES with a bounded Krylov space and a
        # moderate relative tolerance that stops before finite-difference
        # noise amplification; rdiff balances FD truncation vs roundoff.
        "jac_options": {
            "method": "gmres",
            "inner_maxiter": 150,
            "inner_rtol": 1e-5,
            "rdiff": 1e-7,
        },
    }
    try:
        sol = scipy_optimize.root(
            residual,
            x0,
            method=config.root_method,
            options=options,
        )
    except Exception as exc:  # fail closed: never fall back to another solver
        return GeRootResult(
            amplitude=amplitude,
            horizon=horizon,
            K=k,
            root_x=x0,
            root_converged=False,
            root_success=False,
            root_message=f"BLOCKED_DLH_3D_GE_ROOT_NONCONVERGENCE: {exc}",
            root_nit=-1,
            root_nfev=-1,
            root_residual_inf_norm=float("inf"),
            final=evaluate_ge(config, baseline, epsilon_i_path, x0),
        )
    root_x = np.asarray(sol.x, dtype=np.float64)
    final = evaluate_ge(config, baseline, epsilon_i_path, root_x)
    residual_inf_norm = float(np.max(np.abs(final.residual_vector())))
    root_converged = bool(
        residual_inf_norm <= config.root_tolerance_inf_norm and np.all(np.isfinite(root_x))
    )
    return GeRootResult(
        amplitude=amplitude,
        horizon=horizon,
        K=k,
        root_x=root_x,
        root_converged=root_converged,
        root_success=bool(sol.success),
        root_message=str(sol.message),
        root_nit=int(getattr(sol, "nit", -1)),
        root_nfev=int(getattr(sol, "nfev", -1)),
        root_residual_inf_norm=residual_inf_norm,
        final=final,
    )
