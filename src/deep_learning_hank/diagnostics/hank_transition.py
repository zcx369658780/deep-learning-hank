"""DLH-3C diagnostics layer: time-dependent household HJB/KFE validation gates.

Assembles the ``accepted DLH-3B steady state -> prescribed real paths ->
backward HJB -> policy generator path -> forward KFE -> response`` pipeline and
evaluates every Issue #12 gate:

- backward-HJB within-step/global gates (§6);
- forward-KFE mass/non-negativity gates (§7);
- zero-path invariance (§8);
- nontrivial-response + amplitude-to-zero/local-scaling (§9);
- horizon/terminal robustness at fixed ``dt`` (§10);
- deterministic reproducibility of the complete primary validation set (§11).

Evidence ceiling: ``D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY``.
The prescribed paths are ``EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK``,
never IRFs, with no policy interpretation.  No NK GE closure, no ``epsilon_i != 0``,
no NKPC/inflation feedback, no time-step robustness claim.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from deep_learning_hank.diagnostics.hank_steady_state import (
    HankSteadyStateDiagnostics,
    run_hank_steady_state_cached,
)
from deep_learning_hank.economics.grids import build_asset_grid, build_idiosyncratic_generator
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.hank_transition_config import HankTransitionConfig
from deep_learning_hank.solvers.hank_household_transition import (
    DynamicHouseholdSolution,
    TransitionInputs,
    solve_dynamic_household,
)
from deep_learning_hank.solvers.hank_kfe_transition import (
    DynamicDistributionResult,
    forward_kfe_transition,
)

__all__ = [
    "AmplitudeMetrics",
    "BaselineInfo",
    "PathRun",
    "TransitionValidationResult",
    "load_baseline",
    "run_path",
    "run_transition_validation",
    "run_transition_validation_cached",
]

FloatArray = npt.NDArray[np.float64]


@dataclass(frozen=True)
class BaselineInfo:
    """Accepted DLH-3B steady-state baseline (read-only provenance)."""

    dlh_3b_config_sha256: str
    r_star: float
    N_star: float
    wage_star: float
    transfer_star: float
    profits_star: float
    A_hh_star: float
    N_hh_star: float
    C_star: float
    V_ss: FloatArray
    g_ss: FloatArray
    c_ss: FloatArray
    n_ss: FloatArray
    drift_ss: FloatArray
    diagnostics: HankSteadyStateDiagnostics


def load_baseline(config: HankTransitionConfig) -> BaselineInfo:
    """Load the accepted DLH-3B steady state through the accepted interfaces."""
    config.verify_baseline_identity()
    hb_config = HankSteadyStateConfig.from_toml(config.baseline_config_path)
    diagnostics = run_hank_steady_state_cached(hb_config)
    final = diagnostics.result.final
    assert final.household is not None and final.distribution is not None
    return BaselineInfo(
        dlh_3b_config_sha256=hb_config.sha256(),
        r_star=diagnostics.result.root_r,
        N_star=diagnostics.result.root_N,
        wage_star=final.wage,
        transfer_star=final.transfer,
        profits_star=final.profits,
        A_hh_star=final.A_hh,
        N_hh_star=final.N_hh,
        C_star=final.C,
        V_ss=np.asarray(final.household.value, dtype=np.float64).copy(),
        g_ss=np.asarray(final.distribution.mass, dtype=np.float64).copy(),
        c_ss=np.asarray(final.household.consumption, dtype=np.float64).copy(),
        n_ss=np.asarray(final.household.labor, dtype=np.float64).copy(),
        drift_ss=np.asarray(final.household.drift, dtype=np.float64).copy(),
        diagnostics=diagnostics,
    )


def build_time_grid(config: HankTransitionConfig, horizon: float) -> FloatArray:
    n_points = int(round(horizon / config.dt)) + 1
    return config.dt * np.arange(n_points, dtype=np.float64)


def bump_function(t: FloatArray, length: float) -> FloatArray:
    """Compact-support smooth bump ``h(t) = sin(pi*t/L)^2`` on ``[0, L]``."""
    return np.where((t >= 0.0) & (t <= length), np.sin(np.pi * t / length) ** 2, 0.0)


def build_inputs_path(
    config: HankTransitionConfig,
    baseline: BaselineInfo,
    family: str,
    amplitude: float,
    horizon: float,
) -> tuple[TransitionInputs, ...]:
    grid = build_time_grid(config, horizon)
    h = bump_function(grid, config.bump_length_L)
    inputs: list[TransitionInputs] = []
    for k, t in enumerate(grid):
        if family == "zero":
            inputs.append(
                TransitionInputs(
                    wage=baseline.wage_star,
                    real_return=baseline.r_star,
                    transfer=baseline.transfer_star,
                    profits=baseline.profits_star,
                )
            )
        elif family == "W":
            wage_t = baseline.wage_star * (1.0 + config.eta_w * amplitude * h[k])
            inputs.append(
                TransitionInputs(
                    wage=wage_t,
                    real_return=baseline.r_star,
                    transfer=baseline.transfer_star,
                    profits=baseline.profits_star,
                )
            )
        elif family == "R":
            real_return_t = baseline.r_star + config.eta_r * amplitude * h[k]
            inputs.append(
                TransitionInputs(
                    wage=baseline.wage_star,
                    real_return=real_return_t,
                    transfer=baseline.transfer_star,
                    profits=baseline.profits_star,
                )
            )
        else:
            raise ValueError(f"unknown path family: {family}")
    return tuple(inputs)


@dataclass(frozen=True)
class PathRun:
    family: str
    amplitude: float
    horizon: float
    time_grid: FloatArray
    inputs: tuple[TransitionInputs, ...]
    hjb: DynamicHouseholdSolution
    kfe: DynamicDistributionResult
    hjb_gates_pass: bool
    kfe_gates_pass: bool


def _check_hjb_gates(
    config: HankTransitionConfig, hjb: DynamicHouseholdSolution
) -> tuple[bool, dict[str, float]]:
    n = config.numerical
    metrics = {
        "hjb_residual_max": hjb.hjb_residual_max,
        "min_consumption": float(np.min(hjb.consumption_path)),
        "lower_boundary_min_drift": float(np.min(hjb.drift_path[:, :, 0])),
        "upper_boundary_max_drift": float(np.max(hjb.drift_path[:, :, -1])),
        "generator_row_sum_max_abs": float(
            max(np.max(np.abs(np.asarray(g.sum(axis=1)).ravel())) for g in hjb.generator_path)
        ),
        "generator_min_off_diagonal": float(
            min(_generator_off_diagonal_min(g) for g in hjb.generator_path)
        ),
        "labor_kkt_max": hjb.labor_kkt_max,
        "consumption_foc_max": hjb.consumption_foc_max,
    }
    pass_ = bool(
        hjb.converged_all
        and hjb.hjb_residual_max <= n.hjb_residual_tolerance
        and metrics["min_consumption"] > 0.0
        and metrics["lower_boundary_min_drift"] >= -1e-12
        and metrics["upper_boundary_max_drift"] <= 1e-12
        and metrics["generator_row_sum_max_abs"] <= n.generator_row_sum_tolerance
        and metrics["generator_min_off_diagonal"] >= n.generator_min_off_diagonal_tolerance
        and hjb.labor_kkt_max <= n.kkt_tolerance
        and hjb.consumption_foc_max <= n.consumption_foc_tolerance
        and all(s.nan_inf_count == 0 for s in hjb.steps)
    )
    return pass_, metrics


def _generator_off_diagonal_min(generator) -> float:
    off_diagonal = generator - __import__("scipy").sparse.diags(
        generator.diagonal(), format="csr", dtype=np.float64
    )
    stored = float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
    return min(stored, 0.0)


def _check_kfe_gates(
    config: HankTransitionConfig, kfe: DynamicDistributionResult
) -> tuple[bool, dict[str, float]]:
    n = config.numerical
    metrics = {
        "mass_error_max": kfe.mass_error_max,
        "minimum_mass_min": kfe.minimum_mass_min,
        "negative_mass_count_max": float(kfe.negative_mass_count_max),
        "nan_inf_count_max": float(kfe.nan_inf_count_max),
    }
    pass_ = bool(
        kfe.mass_error_max <= n.kfe_mass_tolerance
        and kfe.minimum_mass_min >= n.minimum_mass_threshold
        and kfe.negative_mass_count_max == 0
        and kfe.nan_inf_count_max == 0
    )
    return pass_, metrics


def run_path(
    config: HankTransitionConfig,
    baseline: BaselineInfo,
    *,
    family: str,
    amplitude: float,
    horizon: float,
) -> PathRun:
    """Run one prescribed path: backward HJB + forward KFE + per-run gates."""
    hb_config = HankSteadyStateConfig.from_toml(config.baseline_config_path)
    asset_grid = build_asset_grid(hb_config.a_min, hb_config.a_max, hb_config.asset_grid_count)
    efficiency_states = np.asarray(hb_config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(hb_config.q_low_to_high, hb_config.q_high_to_low)
    inputs = build_inputs_path(config, baseline, family, amplitude, horizon)
    hjb = solve_dynamic_household(
        asset_grid=asset_grid,
        efficiency_states=efficiency_states,
        state_generator=state_generator,
        inputs_path=inputs,
        terminal_value=baseline.V_ss,
        tau_l=hb_config.tau_l,
        rho_hh=hb_config.rho_hh,
        gamma=hb_config.gamma,
        frisch=hb_config.frisch,
        chi=hb_config.chi,
        n_max=hb_config.n_max,
        consumption_floor=config.numerical.consumption_floor,
        dt=config.dt,
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
        dt=config.dt,
    )
    hjb_pass, _ = _check_hjb_gates(config, hjb)
    kfe_pass, _ = _check_kfe_gates(config, kfe)
    return PathRun(
        family=family,
        amplitude=amplitude,
        horizon=horizon,
        time_grid=hjb.time_grid,
        inputs=inputs,
        hjb=hjb,
        kfe=kfe,
        hjb_gates_pass=hjb_pass,
        kfe_gates_pass=kfe_pass,
    )


def _zero_path_invariance_metrics(
    config: HankTransitionConfig, zero: PathRun, baseline: BaselineInfo
) -> dict[str, float]:
    v_max = float(np.max(np.abs(zero.hjb.value_path - baseline.V_ss)))
    c_max = float(np.max(np.abs(zero.hjb.consumption_path - baseline.c_ss)))
    n_max = float(np.max(np.abs(zero.hjb.labor_path - baseline.n_ss)))
    drift_max = float(np.max(np.abs(zero.hjb.drift_path - baseline.drift_ss)))
    g_max = float(np.max(np.abs(zero.kfe.mass_path - baseline.g_ss)))
    A_max = float(np.max(np.abs(zero.kfe.A_hh_path - baseline.A_hh_star)))
    N_max = float(np.max(np.abs(zero.kfe.N_hh_path - baseline.N_hh_star)))
    C_max = float(np.max(np.abs(zero.kfe.C_path - baseline.C_star)))
    g = config.gates
    metrics = {
        "V_max": v_max,
        "c_max": c_max,
        "n_max": n_max,
        "drift_max": drift_max,
        "g_max": g_max,
        "A_hh_max": A_max,
        "N_hh_max": N_max,
        "C_max": C_max,
    }
    metrics["pass"] = float(
        v_max <= g.zero_path_V_tolerance
        and c_max <= g.zero_path_policy_tolerance
        and n_max <= g.zero_path_policy_tolerance
        and drift_max <= g.zero_path_policy_tolerance
        and g_max <= g.zero_path_mass_tolerance
        and A_max <= g.zero_path_aggregate_tolerance
        and N_max <= g.zero_path_aggregate_tolerance
        and C_max <= g.zero_path_aggregate_tolerance
    )
    return metrics


def _response_vector(full: PathRun, zero: PathRun) -> FloatArray:
    """x_eta = [A_hh-A_zero, N_hh-N_zero, C-C_zero] over the common grid."""
    return np.concatenate(
        [
            full.kfe.A_hh_path - zero.kfe.A_hh_path,
            full.kfe.N_hh_path - zero.kfe.N_hh_path,
            full.kfe.C_path - zero.kfe.C_path,
        ]
    )


def _amplitude_metrics(
    config: HankTransitionConfig, family: str, runs: dict[float, PathRun], zero: PathRun
) -> AmplitudeMetrics:
    x_full = _response_vector(runs[1.0], zero)
    x_half = _response_vector(runs[0.5], zero)
    x_quarter = _response_vector(runs[0.25], zero)
    m_full = float(np.max(np.abs(x_full)))
    m_half = float(np.max(np.abs(x_half)))
    m_quarter = float(np.max(np.abs(x_quarter)))
    g = config.gates
    nontrivial_ok = m_full > g.nontrivial_response_threshold
    monotone_ok = m_full > m_half > m_quarter > 0.0
    quarter_cap_ok = m_quarter <= g.quarter_amplitude_ratio_cap * m_full
    e_half = float(np.max(np.abs(x_half - 0.5 * x_full)) / max(m_full, 1e-14))
    half_linearity_ok = e_half <= g.half_linearity_metric_cap
    pass_ = bool(nontrivial_ok and monotone_ok and quarter_cap_ok and half_linearity_ok)
    return AmplitudeMetrics(
        family=family,
        M_full=m_full,
        M_half=m_half,
        M_quarter=m_quarter,
        nontrivial_ok=nontrivial_ok,
        monotone_ok=monotone_ok,
        quarter_cap_ok=quarter_cap_ok,
        E_half=e_half,
        half_linearity_ok=half_linearity_ok,
        pass_=pass_,
    )


@dataclass(frozen=True)
class AmplitudeMetrics:
    family: str
    M_full: float
    M_half: float
    M_quarter: float
    nontrivial_ok: bool
    monotone_ok: bool
    quarter_cap_ok: bool
    E_half: float
    half_linearity_ok: bool
    pass_: bool


def _horizon_robustness_metrics(
    config: HankTransitionConfig,
    primary: dict[str, PathRun],
    long: dict[str, PathRun],
) -> dict[str, float]:
    window = config.gates.horizon_window_T
    k_max = int(round(window / config.dt))
    metrics: dict[str, float] = {}
    ok = True
    for family in ("W", "R"):
        p = primary[family]
        l = long[family]
        for name, pa, la in (
            ("A_hh", p.kfe.A_hh_path, l.kfe.A_hh_path),
            ("N_hh", p.kfe.N_hh_path, l.kfe.N_hh_path),
            ("C", p.kfe.C_path, l.kfe.C_path),
        ):
            diff = float(np.max(np.abs(pa[: k_max + 1] - la[: k_max + 1])))
            metrics[f"{family}_{name}_diff"] = diff
            ok = ok and diff <= config.gates.horizon_aggregate_tolerance
    metrics["pass"] = float(ok and primary["W"].hjb_gates_pass and primary["R"].hjb_gates_pass
                            and long["W"].hjb_gates_pass and long["R"].hjb_gates_pass
                            and long["W"].kfe_gates_pass and long["R"].kfe_gates_pass)
    return metrics


@dataclass(frozen=True)
class TransitionValidationResult:
    config_sha256: str
    baseline: BaselineInfo
    runs: tuple[PathRun, ...]
    zero_invariance: dict[str, float]
    amplitude: tuple[AmplitudeMetrics, ...]
    horizon_robustness: dict[str, float]
    hjb_global: dict[str, float]
    kfe_global: dict[str, float]
    all_gates_pass: bool


def run_transition_validation(config: HankTransitionConfig) -> TransitionValidationResult:
    """Run the complete primary DLH-3C validation set and evaluate all gates."""
    config.validate()
    baseline = load_baseline(config)
    runs: list[PathRun] = []
    zero = run_path(config, baseline, family="zero", amplitude=0.0, horizon=config.T)
    runs.append(zero)
    primary: dict[str, dict[float, PathRun]] = {}
    for family in ("W", "R"):
        primary[family] = {}
        for amp in (1.0, 0.5, 0.25):
            run = run_path(config, baseline, family=family, amplitude=amp, horizon=config.T)
            primary[family][amp] = run
            runs.append(run)
    long: dict[str, PathRun] = {}
    for family in ("W", "R"):
        run = run_path(config, baseline, family=family, amplitude=1.0, horizon=config.T_long)
        long[family] = run
        runs.append(run)

    zero_invariance = _zero_path_invariance_metrics(config, zero, baseline)
    amplitude = (
        _amplitude_metrics(config, "W", primary["W"], zero),
        _amplitude_metrics(config, "R", primary["R"], zero),
    )
    horizon_robustness = _horizon_robustness_metrics(config, {f: primary[f][1.0] for f in ("W", "R")}, long)

    hjb_global: dict[str, float] = {"hjb_residual_max": 0.0, "labor_kkt_max": 0.0,
                                    "consumption_foc_max": 0.0, "nan_inf_max": 0.0}
    kfe_global: dict[str, float] = {"mass_error_max": 0.0, "minimum_mass_min": 0.0,
                                    "negative_mass_count_max": 0.0, "nan_inf_count_max": 0.0}
    for run in runs:
        hjb_global["hjb_residual_max"] = max(hjb_global["hjb_residual_max"], run.hjb.hjb_residual_max)
        hjb_global["labor_kkt_max"] = max(hjb_global["labor_kkt_max"], run.hjb.labor_kkt_max)
        hjb_global["consumption_foc_max"] = max(hjb_global["consumption_foc_max"], run.hjb.consumption_foc_max)
        hjb_global["nan_inf_max"] = max(hjb_global["nan_inf_max"], float(max(s.nan_inf_count for s in run.hjb.steps)))
        kfe_global["mass_error_max"] = max(kfe_global["mass_error_max"], run.kfe.mass_error_max)
        kfe_global["minimum_mass_min"] = min(kfe_global["minimum_mass_min"], run.kfe.minimum_mass_min)
        kfe_global["negative_mass_count_max"] = max(kfe_global["negative_mass_count_max"], float(run.kfe.negative_mass_count_max))
        kfe_global["nan_inf_count_max"] = max(kfe_global["nan_inf_count_max"], float(run.kfe.nan_inf_count_max))

    all_gates_pass = bool(
        zero_invariance["pass"] == 1.0
        and amplitude[0].pass_
        and amplitude[1].pass_
        and horizon_robustness["pass"] == 1.0
        and all(run.hjb_gates_pass and run.kfe_gates_pass for run in runs)
    )
    return TransitionValidationResult(
        config_sha256=config.sha256(),
        baseline=baseline,
        runs=tuple(runs),
        zero_invariance=zero_invariance,
        amplitude=amplitude,
        horizon_robustness=horizon_robustness,
        hjb_global=hjb_global,
        kfe_global=kfe_global,
        all_gates_pass=all_gates_pass,
    )


_CACHE: dict[str, TransitionValidationResult] = {}


def run_transition_validation_cached(config: HankTransitionConfig) -> TransitionValidationResult:
    """Test-level cached entry point (single primary validation set shared by
    the gate tests).  The reproducibility test intentionally bypasses this
    cache and re-runs the complete set, so non-determinism can never hide."""
    key = config.sha256()
    if key not in _CACHE:
        _CACHE[key] = run_transition_validation(config)
    return _CACHE[key]


def reproducibility_differences(
    config: HankTransitionConfig,
) -> dict[str, float]:
    """Run the complete primary validation set twice and report max repeat
    differences (Issue #12 §11)."""
    first = run_transition_validation(config)
    second = run_transition_validation(config)
    diffs: dict[str, float] = {}
    for a, b in zip(first.runs, second.runs):
        label = f"{a.family}_amp{a.amplitude}_T{a.horizon}"
        diffs[f"{label}_value"] = float(np.max(np.abs(a.hjb.value_path - b.hjb.value_path)))
        diffs[f"{label}_consumption"] = float(np.max(np.abs(a.hjb.consumption_path - b.hjb.consumption_path)))
        diffs[f"{label}_labor"] = float(np.max(np.abs(a.hjb.labor_path - b.hjb.labor_path)))
        diffs[f"{label}_drift"] = float(np.max(np.abs(a.hjb.drift_path - b.hjb.drift_path)))
        diffs[f"{label}_mass"] = float(np.max(np.abs(a.kfe.mass_path - b.kfe.mass_path)))
        diffs[f"{label}_A_hh"] = float(np.max(np.abs(a.kfe.A_hh_path - b.kfe.A_hh_path)))
        diffs[f"{label}_N_hh"] = float(np.max(np.abs(a.kfe.N_hh_path - b.kfe.N_hh_path)))
        diffs[f"{label}_C"] = float(np.max(np.abs(a.kfe.C_path - b.kfe.C_path)))
        diffs[f"{label}_inputs_w"] = float(max(abs(i1.wage - i2.wage) for i1, i2 in zip(a.inputs, b.inputs)))
        diffs[f"{label}_inputs_r"] = float(max(abs(i1.real_return - i2.real_return) for i1, i2 in zip(a.inputs, b.inputs)))
    diffs["zero_invariance"] = max(
        abs(a - b)
        for a, b in zip(
            [first.zero_invariance[k] for k in sorted(k for k in first.zero_invariance if k != "pass")],
            [second.zero_invariance[k] for k in sorted(k for k in second.zero_invariance if k != "pass")],
        )
    )
    for a, b in zip(first.amplitude, second.amplitude):
        diffs[f"amplitude_{a.family}_M"] = max(
            abs(a.M_full - b.M_full), abs(a.M_half - b.M_half), abs(a.M_quarter - b.M_quarter)
        )
        diffs[f"amplitude_{a.family}_E_half"] = abs(a.E_half - b.E_half)
    return diffs
