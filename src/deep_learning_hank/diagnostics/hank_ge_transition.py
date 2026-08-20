"""DLH-3D diagnostics layer: full NK GE closure validation gates.

Assembles the ``epsilon_i -> Taylor/Fisher -> r -> household HJB/KFE ->
A_hh/N_hh/C -> asset/labor clearing -> w,N -> firm/mc -> NKPC -> pi ->
Taylor/Fisher`` loop and evaluates every Issue #13 gate (with the
authoritative numerical-timing clarification):

- strict GE root/market-clearing gates on the root interval ``k = 0..K-1``;
- terminal ``A_hh,K - B`` and ``N_hh,K - N*`` reported as finite-horizon
  terminal-approximation diagnostics (not root equations);
- household/KFE gates (accepted DLH-3C semantics);
- NKPC / Fisher / Taylor / goods / KFE-consistent wealth-flow / fiscal /
  profit residual gates;
- zero-innovation invariance;
- nontrivial response + amplitude-to-zero / local scaling;
- horizon/terminal robustness at fixed ``dt``;
- deterministic reproducibility of the complete validation set.

Evidence ceiling:
``D2_MACHINE_DIAGNOSTIC__MINIMAL_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_FIXTURE``.
This is not empirical calibration, policy-effectiveness evidence, regional
NSR-HANK validation, or Results.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from deep_learning_hank.diagnostics.hank_transition import BaselineInfo, load_baseline
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.hank_ge_config import HankGeConfig
from deep_learning_hank.hank_transition_config import HankTransitionConfig
from deep_learning_hank.solvers.hank_ge_transition import GeRootResult, solve_ge_transition

__all__ = [
    "GeRun",
    "GeValidationResult",
    "load_baseline_3d",
    "run_ge",
    "run_ge_validation",
    "run_ge_validation_cached",
    "reproducibility_differences",
]

FloatArray = npt.NDArray[np.float64]


def load_baseline_3d(config: HankGeConfig) -> BaselineInfo:
    """Verify both accepted baseline identities and load the DLH-3B steady state
    through the accepted interfaces."""
    config.verify_baseline_identities()
    return load_baseline(HankTransitionConfig.from_toml(config.baseline_3c_path))


def _generator_off_diagonal_min(generator) -> float:
    off_diagonal = generator - __import__("scipy").sparse.diags(
        generator.diagonal(), format="csr", dtype=np.float64
    )
    stored = float(np.min(off_diagonal.data)) if off_diagonal.nnz else 0.0
    return min(stored, 0.0)


def _check_hjb_gates(
    config: HankGeConfig, hjb
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


def _check_kfe_gates(
    config: HankGeConfig, kfe
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


@dataclass(frozen=True)
class GeRun:
    amplitude: float
    horizon: float
    result: GeRootResult
    hjb_gates_pass: bool
    kfe_gates_pass: bool
    terminal_A_hh_minus_B: float
    terminal_N_hh_minus_N_star: float
    terminal_R_goods: float


def run_ge(
    config: HankGeConfig,
    baseline: BaselineInfo,
    *,
    amplitude: float,
    horizon: float,
) -> GeRun:
    """Run one GE innovation and evaluate the per-run household/KFE gates."""
    result = solve_ge_transition(config, baseline, amplitude=amplitude, horizon=horizon)
    hjb_pass, _ = _check_hjb_gates(config, result.final.hjb)
    kfe_pass, _ = _check_kfe_gates(config, result.final.kfe)
    final = result.final
    hb_config = HankSteadyStateConfig.from_toml(config.baseline_3b_path)
    b = hb_config.bond_supply
    return GeRun(
        amplitude=amplitude,
        horizon=horizon,
        result=result,
        hjb_gates_pass=hjb_pass,
        kfe_gates_pass=kfe_pass,
        terminal_A_hh_minus_B=float(final.A_hh[-1] - b),
        terminal_N_hh_minus_N_star=float(final.N_hh[-1] - baseline.N_star),
        terminal_R_goods=float(final.R_goods[-1]),
    )


def _zero_invariance_metrics(
    config: HankGeConfig, zero: GeRun, baseline: BaselineInfo
) -> dict[str, float]:
    agg = zero.result.final.aggregates
    final = zero.result.final
    g = config.gates
    metrics = {
        "w_max": float(np.max(np.abs(agg.w - baseline.wage_star))),
        "N_max": float(np.max(np.abs(agg.N - baseline.N_star))),
        "pi_max": float(np.max(np.abs(agg.pi))),
        "r_max": float(np.max(np.abs(agg.r - baseline.r_star))),
        "A_hh_max": float(np.max(np.abs(final.A_hh - baseline.A_hh_star))),
        "N_hh_max": float(np.max(np.abs(final.N_hh - baseline.N_hh_star))),
        "C_max": float(np.max(np.abs(final.C - baseline.C_star))),
    }
    metrics["pass"] = float(
        metrics["w_max"] <= g.zero_w_tolerance
        and metrics["N_max"] <= g.zero_N_tolerance
        and metrics["pi_max"] <= g.zero_pi_tolerance
        and metrics["r_max"] <= g.zero_r_tolerance
        and metrics["A_hh_max"] <= g.zero_A_hh_tolerance
        and metrics["N_hh_max"] <= g.zero_N_hh_tolerance
        and metrics["C_max"] <= g.zero_C_tolerance
        and zero.hjb_gates_pass
        and zero.kfe_gates_pass
    )
    return metrics


def _full_gates(
    config: HankGeConfig, full: GeRun, baseline: BaselineInfo
) -> dict[str, float]:
    final = full.result.final
    k = final.K
    g = config.gates
    metrics = {
        "root_residual_inf_norm": full.result.root_residual_inf_norm,
        "R_asset_max_k_lt_K": float(np.max(np.abs(final.R_asset[:k]))),
        "R_labor_max_k_lt_K": float(np.max(np.abs(final.R_labor[:k]))),
        "R_nkpc_max": float(np.max(np.abs(final.R_nkpc[:k]))),
        "R_fisher_max": float(np.max(np.abs(final.R_fisher[:k]))),
        "R_taylor_max": float(np.max(np.abs(final.R_taylor[:k]))),
        "R_goods_max": float(np.max(np.abs(final.R_goods[:k]))),
        "R_wealth_max": float(np.max(np.abs(final.R_wealth[:k]))),
        "R_fiscal_max": float(np.max(np.abs(final.R_fiscal[:k]))),
        "R_profits_max": float(np.max(np.abs(final.R_profits[:k]))),
        "nontrivial_max": float(
            max(
                np.max(np.abs(final.aggregates.pi)),
                np.max(np.abs(final.aggregates.r - baseline.r_star)),
                np.max(np.abs(final.aggregates.w - baseline.wage_star)),
                np.max(np.abs(final.aggregates.N - baseline.N_star)),
                np.max(np.abs(final.C - baseline.C_star)),
            )
        ),
    }
    market_ok = bool(
        full.result.root_converged
        and metrics["root_residual_inf_norm"] <= config.root_tolerance_inf_norm
        and metrics["R_asset_max_k_lt_K"] <= g.clearing_asset_tolerance
        and metrics["R_labor_max_k_lt_K"] <= g.clearing_labor_tolerance
    )
    aggregate_ok = bool(
        metrics["R_nkpc_max"] <= g.nkpc_tolerance
        and metrics["R_fisher_max"] <= g.fisher_tolerance
        and metrics["R_taylor_max"] <= g.taylor_tolerance
        and metrics["R_goods_max"] <= g.goods_tolerance
        and metrics["R_wealth_max"] <= g.wealth_flow_tolerance
        and metrics["R_fiscal_max"] <= g.fiscal_tolerance
        and metrics["R_profits_max"] <= g.profits_tolerance
    )
    nontrivial_ok = metrics["nontrivial_max"] > g.nontrivial_response_threshold
    metrics["market_ok"] = float(market_ok)
    metrics["aggregate_ok"] = float(aggregate_ok)
    metrics["nontrivial_ok"] = float(nontrivial_ok)
    metrics["pass"] = float(
        market_ok and aggregate_ok and nontrivial_ok and full.hjb_gates_pass and full.kfe_gates_pass
    )
    return metrics


def _amplitude_metrics(
    config: HankGeConfig, full: GeRun, half: GeRun, quarter: GeRun, zero: GeRun
) -> dict[str, float]:
    def response(run: GeRun) -> FloatArray:
        final = run.result.final
        zero_final = zero.result.final
        return np.concatenate(
            [
                final.aggregates.pi,
                final.aggregates.r - zero_final.aggregates.r,
                final.aggregates.w - zero_final.aggregates.w,
                final.aggregates.N - zero_final.aggregates.N,
                final.A_hh - zero_final.A_hh,
                final.C - zero_final.C,
            ]
        )

    x_full = response(full)
    x_half = response(half)
    x_quarter = response(quarter)
    m_full = float(np.max(np.abs(x_full)))
    m_half = float(np.max(np.abs(x_half)))
    m_quarter = float(np.max(np.abs(x_quarter)))
    g = config.gates
    monotone_ok = m_full > m_half > m_quarter > 0.0
    quarter_cap_ok = m_quarter <= g.quarter_amplitude_ratio_cap * m_full
    e_half = float(np.max(np.abs(x_half - 0.5 * x_full)) / max(m_full, 1e-14))
    half_linearity_ok = e_half <= g.half_linearity_metric_cap
    metrics = {
        "M_full": m_full,
        "M_half": m_half,
        "M_quarter": m_quarter,
        "monotone_ok": float(monotone_ok),
        "quarter_cap_ok": float(quarter_cap_ok),
        "E_half": e_half,
        "half_linearity_ok": float(half_linearity_ok),
        "pass": float(monotone_ok and quarter_cap_ok and half_linearity_ok),
    }
    return metrics


def _horizon_metrics(
    config: HankGeConfig, primary: GeRun, long: GeRun
) -> dict[str, float]:
    window = config.gates.horizon_window_T
    k_max = int(round(window / config.dt))
    p = primary.result.final
    l = long.result.final
    metrics: dict[str, float] = {}
    ok = True
    for name, pa, la in (
        ("pi", p.aggregates.pi, l.aggregates.pi),
        ("r", p.aggregates.r, l.aggregates.r),
        ("w", p.aggregates.w, l.aggregates.w),
        ("N", p.aggregates.N, l.aggregates.N),
        ("A_hh", p.A_hh, l.A_hh),
        ("C", p.C, l.C),
    ):
        diff = float(np.max(np.abs(pa[: k_max + 1] - la[: k_max + 1])))
        metrics[f"{name}_diff"] = diff
        ok = ok and diff <= config.gates.horizon_tolerance
    metrics["pass"] = float(
        ok and primary.hjb_gates_pass and primary.kfe_gates_pass
        and long.hjb_gates_pass and long.kfe_gates_pass
        and long.result.root_converged
    )
    return metrics


@dataclass(frozen=True)
class GeValidationResult:
    config_sha256: str
    baseline: BaselineInfo
    runs: tuple[GeRun, ...]
    zero_invariance: dict[str, float]
    full_gates: dict[str, float]
    amplitude: dict[str, float]
    horizon_robustness: dict[str, float]
    hjb_global: dict[str, float]
    kfe_global: dict[str, float]
    all_gates_pass: bool


def run_ge_validation(config: HankGeConfig) -> GeValidationResult:
    """Run the complete DLH-3D validation set and evaluate all gates."""
    config.validate()
    baseline = load_baseline_3d(config)
    zero = run_ge(config, baseline, amplitude=0.0, horizon=config.T)
    full = run_ge(config, baseline, amplitude=1.0, horizon=config.T)
    half = run_ge(config, baseline, amplitude=0.5, horizon=config.T)
    quarter = run_ge(config, baseline, amplitude=0.25, horizon=config.T)
    long_full = run_ge(config, baseline, amplitude=1.0, horizon=config.T_long)
    runs = (zero, full, half, quarter, long_full)

    zero_invariance = _zero_invariance_metrics(config, zero, baseline)
    full_gates = _full_gates(config, full, baseline)
    amplitude = _amplitude_metrics(config, full, half, quarter, zero)
    horizon_robustness = _horizon_metrics(config, full, long_full)

    hjb_global: dict[str, float] = {
        "hjb_residual_max": 0.0,
        "labor_kkt_max": 0.0,
        "consumption_foc_max": 0.0,
        "nan_inf_max": 0.0,
    }
    kfe_global: dict[str, float] = {
        "mass_error_max": 0.0,
        "minimum_mass_min": 0.0,
        "negative_mass_count_max": 0.0,
        "nan_inf_count_max": 0.0,
    }
    for run in runs:
        hjb_global["hjb_residual_max"] = max(
            hjb_global["hjb_residual_max"], run.result.final.hjb.hjb_residual_max
        )
        hjb_global["labor_kkt_max"] = max(
            hjb_global["labor_kkt_max"], run.result.final.hjb.labor_kkt_max
        )
        hjb_global["consumption_foc_max"] = max(
            hjb_global["consumption_foc_max"], run.result.final.hjb.consumption_foc_max
        )
        hjb_global["nan_inf_max"] = max(
            hjb_global["nan_inf_max"],
            float(max(s.nan_inf_count for s in run.result.final.hjb.steps)),
        )
        kfe_global["mass_error_max"] = max(
            kfe_global["mass_error_max"], run.result.final.kfe.mass_error_max
        )
        kfe_global["minimum_mass_min"] = min(
            kfe_global["minimum_mass_min"], run.result.final.kfe.minimum_mass_min
        )
        kfe_global["negative_mass_count_max"] = max(
            kfe_global["negative_mass_count_max"],
            float(run.result.final.kfe.negative_mass_count_max),
        )
        kfe_global["nan_inf_count_max"] = max(
            kfe_global["nan_inf_count_max"], float(run.result.final.kfe.nan_inf_count_max)
        )

    all_gates_pass = bool(
        zero_invariance["pass"] == 1.0
        and full_gates["pass"] == 1.0
        and amplitude["pass"] == 1.0
        and horizon_robustness["pass"] == 1.0
        and all(run.hjb_gates_pass and run.kfe_gates_pass for run in runs)
    )
    return GeValidationResult(
        config_sha256=config.sha256(),
        baseline=baseline,
        runs=runs,
        zero_invariance=zero_invariance,
        full_gates=full_gates,
        amplitude=amplitude,
        horizon_robustness=horizon_robustness,
        hjb_global=hjb_global,
        kfe_global=kfe_global,
        all_gates_pass=all_gates_pass,
    )


_CACHE: dict[str, GeValidationResult] = {}


def run_ge_validation_cached(config: HankGeConfig) -> GeValidationResult:
    """Test-level cached entry point.  The reproducibility test bypasses the
    cache and re-runs the complete validation set, so non-determinism can
    never hide."""
    key = config.sha256()
    if key not in _CACHE:
        _CACHE[key] = run_ge_validation(config)
    return _CACHE[key]


def reproducibility_differences(config: HankGeConfig) -> dict[str, float]:
    """Run the complete validation set twice and report max repeat differences."""
    first = run_ge_validation(config)
    second = run_ge_validation(config)
    diffs: dict[str, float] = {}
    for a, b in zip(first.runs, second.runs):
        label = f"amp{a.amplitude}_T{a.horizon}"
        fa, fb = a.result.final, b.result.final
        diffs[f"{label}_root_x"] = float(np.max(np.abs(a.result.root_x - b.result.root_x)))
        diffs[f"{label}_w"] = float(np.max(np.abs(fa.aggregates.w - fb.aggregates.w)))
        diffs[f"{label}_N"] = float(np.max(np.abs(fa.aggregates.N - fb.aggregates.N)))
        diffs[f"{label}_pi"] = float(np.max(np.abs(fa.aggregates.pi - fb.aggregates.pi)))
        diffs[f"{label}_r"] = float(np.max(np.abs(fa.aggregates.r - fb.aggregates.r)))
        diffs[f"{label}_value"] = float(np.max(np.abs(fa.hjb.value_path - fb.hjb.value_path)))
        diffs[f"{label}_consumption"] = float(
            np.max(np.abs(fa.hjb.consumption_path - fb.hjb.consumption_path))
        )
        diffs[f"{label}_labor"] = float(np.max(np.abs(fa.hjb.labor_path - fb.hjb.labor_path)))
        diffs[f"{label}_drift"] = float(np.max(np.abs(fa.hjb.drift_path - fb.hjb.drift_path)))
        diffs[f"{label}_mass"] = float(np.max(np.abs(fa.kfe.mass_path - fb.kfe.mass_path)))
        diffs[f"{label}_A_hh"] = float(np.max(np.abs(fa.A_hh - fb.A_hh)))
        diffs[f"{label}_N_hh"] = float(np.max(np.abs(fa.N_hh - fb.N_hh)))
        diffs[f"{label}_C"] = float(np.max(np.abs(fa.C - fb.C)))
        diffs[f"{label}_residual_vector"] = float(
            np.max(np.abs(fa.residual_vector() - fb.residual_vector()))
        )
    for key in first.zero_invariance:
        if key != "pass":
            diffs[f"zero_invariance_{key}"] = abs(
                first.zero_invariance[key] - second.zero_invariance[key]
            )
    for key in ("M_full", "M_half", "M_quarter", "E_half"):
        diffs[f"amplitude_{key}"] = abs(first.amplitude[key] - second.amplitude[key])
    return diffs
