"""DLH-2C Tier-0 numerical robustness / grid-boundary / invariance validation.

Freezes the accepted DLH-2A/DLH-2B economics and solver family; varies only
grid resolution, asset upper bound, and productivity-state label ordering.

Variants:
  * B40_50   = accepted DLH-2B baseline (40 points on [0,50]);
  * G80_50   = 80 points on [0,50];
  * G160_50  = 160 points on [0,50];
  * W159_100 = 159 points on [0,100] (spacing 100/158 = 50/79, matched to
               G80_50 to isolate the upper-bound effect);
  * P40_50   = B40_50 with productivity-state ordering reversed (1.5,0.5) and
               CTMC state labels reversed consistently (pure permutation).

All configs are ``VALIDATION_FIXTURE_NOT_CALIBRATION``.

Gates (Issue #7):
  * per-variant numerical gates (accepted thresholds);
  * grid-refinement convergence (d40_80, d80_160);
  * asset upper-bound sensitivity (d_bound_K);
  * state-label permutation invariance (<=1e-10 after axis reversal);
  * bounded residual-shape / root-uniqueness scan (21 points on [0.5,45.0]);
  * deterministic reproducibility (<=1e-12 per variant).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_steady_state import (
    SteadyStateDiagnostics,
    run_tier0_steady_state,
)
from deep_learning_hank.economics.grids import build_asset_grid
from deep_learning_hank.solvers.steady_state import evaluate_capital

__all__ = [
    "REPO_ROOT",
    "BASELINE_CONFIG",
    "VARIANT_CONFIGS",
    "relative_diff",
    "load_variants",
    "grid_convergence_metrics",
    "upper_bound_sensitivity_metrics",
    "permutation_invariance_metrics",
    "residual_scan",
    "reproducibility_metrics",
]

REPO_ROOT = Path(__file__).resolve().parents[3]
BASELINE_CONFIG = REPO_ROOT / "configs" / "dlh_2b_tier0_steady_state_validation.toml"
VARIANT_CONFIGS: dict[str, Path] = {
    "B40_50": BASELINE_CONFIG,
    "G80_50": REPO_ROOT / "configs" / "dlh_2c_grid80_bound50_validation.toml",
    "G160_50": REPO_ROOT / "configs" / "dlh_2c_grid160_bound50_validation.toml",
    "W159_100": REPO_ROOT / "configs" / "dlh_2c_grid159_bound100_validation.toml",
    "P40_50": REPO_ROOT / "configs" / "dlh_2c_state_permutation_validation.toml",
}

FloatArray = npt.NDArray[np.float64]


def relative_diff(reference: float, value: float) -> float:
    """Relative difference ``abs(value - reference)/max(1, abs(value))``."""
    return float(abs(value - reference) / max(1.0, abs(value)))


def load_variants() -> dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]]:
    """Run the accepted steady-state pipeline for every variant."""
    loaded: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]] = {}
    for name, path in VARIANT_CONFIGS.items():
        config = SteadyStateConfig.from_toml(path)
        diagnostics = run_tier0_steady_state(config)
        loaded[name] = (config, diagnostics)
    return loaded


def grid_convergence_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """B40_50 vs G80_50 vs G160_50: successive-refinement capital gates."""
    k40 = variants["B40_50"][1].result.final.capital
    k80 = variants["G80_50"][1].result.final.capital
    k160 = variants["G160_50"][1].result.final.capital
    d40_80 = float(abs(k80 - k40) / max(1.0, abs(k80)))
    d80_160 = float(abs(k160 - k80) / max(1.0, abs(k160)))
    gate_no_worsen = bool(d80_160 <= d40_80 + 1e-12)
    gate_final = bool(d80_160 <= 0.005)
    fields = {
        "output": ("output",),
        "wage": ("wage",),
        "net_capital_return": ("net_capital_return",),
        "transfer": ("transfer",),
        "mean_consumption": ("mean_consumption",),
        "mean_assets": ("mean_assets",),
    }
    rel_diffs: dict[str, float] = {}
    flags: dict[str, bool] = {}
    f80 = variants["G80_50"][1].result.final
    f160 = variants["G160_50"][1].result.final
    for key, (attr,) in fields.items():
        value80 = getattr(f80, attr)
        value160 = getattr(f160, attr)
        rel_diffs[key] = relative_diff(value160, value80)
        flags[key] = bool(rel_diffs[key] > 0.005)
    return {
        "k40": float(k40),
        "k80": float(k80),
        "k160": float(k160),
        "d40_80": d40_80,
        "d80_160": d80_160,
        "gate_no_worsen": gate_no_worsen,
        "gate_final": gate_final,
        "gate": bool(gate_no_worsen and gate_final),
        "relative_diffs_80_160": rel_diffs,
        "flags_gt_half_percent": flags,
    }


def upper_bound_sensitivity_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """G80_50 vs W159_100 (matched spacing): asset upper-bound sensitivity."""
    config80, diag80 = variants["G80_50"]
    config100, diag100 = variants["W159_100"]
    f80 = diag80.result.final
    f100 = diag100.result.final
    k50 = f80.capital
    k100 = f100.capital
    d_bound_k = float(abs(k100 - k50) / max(1.0, abs(k100)))
    gate = bool(d_bound_k <= 0.005)
    grid80 = build_asset_grid(config80.a_min, config80.a_max, config80.asset_grid_count)
    grid100 = build_asset_grid(config100.a_min, config100.a_max, config100.asset_grid_count)
    upper_boundary_mass_50 = f80.distribution.upper_boundary_mass
    upper_boundary_mass_100 = f100.distribution.upper_boundary_mass
    top5_mask_50 = grid80 >= 0.95 * config80.a_max
    top5_mask_100 = grid100 >= 0.95 * config100.a_max
    top5_mass_50 = float(np.sum(f80.distribution.mass[:, top5_mask_50]))
    top5_mass_100 = float(np.sum(f100.distribution.mass[:, top5_mask_100]))
    rel_diffs = {
        "output": relative_diff(f100.output, f80.output),
        "wage": relative_diff(f100.wage, f80.wage),
        "net_capital_return": relative_diff(f100.net_capital_return, f80.net_capital_return),
        "transfer": relative_diff(f100.transfer, f80.transfer),
        "mean_consumption": relative_diff(f100.mean_consumption, f80.mean_consumption),
    }
    return {
        "k50": float(k50),
        "k100": float(k100),
        "d_bound_K": d_bound_k,
        "gate": gate,
        "upper_boundary_mass_50": float(upper_boundary_mass_50),
        "upper_boundary_mass_100": float(upper_boundary_mass_100),
        "top5_mass_50": top5_mass_50,
        "top5_mass_100": top5_mass_100,
        "mean_assets_over_amax_50": float(f80.mean_assets / config80.a_max),
        "mean_assets_over_amax_100": float(f100.mean_assets / config100.a_max),
        "relative_diffs_50_100": rel_diffs,
    }


def permutation_invariance_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """B40_50 vs P40_50 after reversing the permuted state axis."""
    b40 = variants["B40_50"][1].result.final
    p40 = variants["P40_50"][1].result.final
    scalars = {
        "capital": abs(p40.capital - b40.capital),
        "output": abs(p40.output - b40.output),
        "wage": abs(p40.wage - b40.wage),
        "net_capital_return": abs(p40.net_capital_return - b40.net_capital_return),
        "transfer": abs(p40.transfer - b40.transfer),
    }
    arrays = {
        "value": float(np.max(np.abs(p40.household.value[::-1, :] - b40.household.value))),
        "consumption": float(
            np.max(np.abs(p40.household.consumption[::-1, :] - b40.household.consumption))
        ),
        "drift": float(np.max(np.abs(p40.household.drift[::-1, :] - b40.household.drift))),
        "distribution_mass": float(
            np.max(np.abs(p40.distribution.mass[::-1, :] - b40.distribution.mass))
        ),
        "scalars": float(np.max(np.abs(p40.scalar_vector() - b40.scalar_vector()))),
    }
    all_diffs = {**scalars, **arrays}
    gate = bool(all(value <= 1e-10 for value in all_diffs.values()))
    return {"max_abs_diffs": all_diffs, "gate": gate}


def residual_scan(
    config: SteadyStateConfig, *, points: int = 21
) -> dict[str, object]:
    """Bounded residual-shape scan of R_K(K) on [0.5, 45.0].

    Exactly ``points`` equally spaced capital values; counts distinct adjacent
    sign-changing intervals (an exact-zero sample counts as one root interval,
    not two).  Bounded numerical uniqueness diagnostic, not a global proof.
    """
    lower, upper = config.capital_bracket
    capital_points = np.linspace(lower, upper, points)
    residuals: list[float] = []
    for capital in capital_points:
        residuals.append(evaluate_capital(config, float(capital)).capital_residual)
    residuals_arr = np.asarray(residuals, dtype=np.float64)
    all_finite = bool(np.all(np.isfinite(capital_points)) and np.all(np.isfinite(residuals_arr)))
    crossings = 0
    for i in range(len(residuals_arr) - 1):
        if residuals_arr[i] * residuals_arr[i + 1] < 0.0:
            crossings += 1
    zero_count = int(np.count_nonzero(residuals_arr == 0.0))
    intervals = crossings + zero_count
    gate = bool(all_finite and intervals == 1)
    return {
        "points": [float(x) for x in capital_points],
        "residuals": residuals,
        "all_finite": all_finite,
        "sign_changing_intervals": intervals,
        "crossings": crossings,
        "exact_zero_samples": zero_count,
        "gate": gate,
    }


def reproducibility_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Two identical runs per variant (G80_50, G160_50, W159_100, P40_50)."""
    results: dict[str, dict[str, float]] = {}
    for name in ("G80_50", "G160_50", "W159_100", "P40_50"):
        config = variants[name][0]
        first = run_tier0_steady_state(config)
        second = run_tier0_steady_state(config)
        a, b = first.result.final, second.result.final
        diffs = {
            "capital_star": abs(a.capital - b.capital),
            "wage": abs(a.wage - b.wage),
            "net_capital_return": abs(a.net_capital_return - b.net_capital_return),
            "output": abs(a.output - b.output),
            "transfer": abs(a.transfer - b.transfer),
            "value": float(np.max(np.abs(a.household.value - b.household.value))),
            "consumption": float(
                np.max(np.abs(a.household.consumption - b.household.consumption))
            ),
            "drift": float(np.max(np.abs(a.household.drift - b.household.drift))),
            "distribution_mass": float(
                np.max(np.abs(a.distribution.mass - b.distribution.mass))
            ),
            "scalars": float(np.max(np.abs(a.scalar_vector() - b.scalar_vector()))),
        }
        results[name] = diffs
    gate = bool(
        all(diff <= 1e-12 for per_variant in results.values() for diff in per_variant.values())
    )
    return {"per_variant_max_abs_diffs": results, "gate": gate}
