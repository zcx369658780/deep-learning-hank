"""DLH-2C-B1 Tier-0 asset-domain adequacy / upper-tail convergence validation.

Freezes the accepted economics and solver family (DLH-2A/2B/2C); varies only
the asset upper bound and grid spacing.  All configs are
``VALIDATION_FIXTURE_NOT_CALIBRATION``.

Variants (spacing h = 50/79 coarse, h/2 = 25/79 fine):
  * C50  = accepted G80_50  (80  pts  [0,  50])   -- read-only
  * C100 = accepted W159_100 (159 pts  [0, 100])   -- read-only
  * C150 = new               (238 pts  [0, 150])
  * C200 = new               (317 pts  [0, 200])
  * F100 = new fine          (317 pts  [0, 100])
  * F200 = new fine          (633 pts  [0, 200])

Gates (Issue #8):
  * coarse-spacing asset-bound convergence:
      d50_100 reproduces accepted 0.03411577346665587 (<=1e-12);
      d100_150 <= d50_100 + 1e-12; d150_200 <= d100_150 + 1e-12;
      d150_200 <= 0.005;
  * wide-domain grid refinement:
      d_grid_100 <= 0.005; d_grid_200 <= d_grid_100 + 1e-12; d_grid_200 <= 0.005;
  * per-variant numerical gates (accepted thresholds);
  * deterministic reproducibility (<=1e-12).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_steady_state import (
    SteadyStateDiagnostics,
    run_tier0_steady_state,
)
from deep_learning_hank.economics.grids import build_asset_grid

__all__ = [
    "REPO_ROOT",
    "COARSE_CONFIGS",
    "FINE_CONFIGS",
    "load_variants",
    "relative_diff",
    "coarse_bound_convergence_metrics",
    "wide_domain_grid_refinement_metrics",
    "tail_diagnostics",
    "reproducibility_metrics",
]

REPO_ROOT = Path(__file__).resolve().parents[3]

COARSE_CONFIGS: dict[str, Path] = {
    "C50": REPO_ROOT / "configs" / "dlh_2c_grid80_bound50_validation.toml",
    "C100": REPO_ROOT / "configs" / "dlh_2c_grid159_bound100_validation.toml",
    "C150": REPO_ROOT / "configs" / "dlh_2c_b1_bound150_coarse_validation.toml",
    "C200": REPO_ROOT / "configs" / "dlh_2c_b1_bound200_coarse_validation.toml",
}
FINE_CONFIGS: dict[str, Path] = {
    "F100": REPO_ROOT / "configs" / "dlh_2c_b1_bound100_fine_validation.toml",
    "F200": REPO_ROOT / "configs" / "dlh_2c_b1_bound200_fine_validation.toml",
}

ACCEPTED_D50_100 = 0.03411577346665587


def relative_diff(reference: float, value: float) -> float:
    """Relative difference ``abs(value - reference)/max(1, abs(value))``."""
    return float(abs(value - reference) / max(1.0, abs(value)))


def load_variants() -> dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]]:
    """Run the accepted steady-state pipeline for every coarse and fine variant."""
    loaded: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]] = {}
    for name, path in {**COARSE_CONFIGS, **FINE_CONFIGS}.items():
        config = SteadyStateConfig.from_toml(path)
        diagnostics = run_tier0_steady_state(config)
        loaded[name] = (config, diagnostics)
    return loaded


def coarse_bound_convergence_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Sequential matched-spacing bound increments C50->C100->C150->C200."""
    k50 = variants["C50"][1].result.final.capital
    k100 = variants["C100"][1].result.final.capital
    k150 = variants["C150"][1].result.final.capital
    k200 = variants["C200"][1].result.final.capital
    d50_100 = float(abs(k100 - k50) / max(1.0, abs(k100)))
    d100_150 = float(abs(k150 - k100) / max(1.0, abs(k150)))
    d150_200 = float(abs(k200 - k150) / max(1.0, abs(k200)))
    gate_provenance = bool(abs(d50_100 - ACCEPTED_D50_100) <= 1e-12)
    gate_no_worsen_1 = bool(d100_150 <= d50_100 + 1e-12)
    gate_no_worsen_2 = bool(d150_200 <= d100_150 + 1e-12)
    gate_final = bool(d150_200 <= 0.005)
    return {
        "k50": float(k50),
        "k100": float(k100),
        "k150": float(k150),
        "k200": float(k200),
        "d50_100": d50_100,
        "d100_150": d100_150,
        "d150_200": d150_200,
        "accepted_d50_100": ACCEPTED_D50_100,
        "gate_provenance": gate_provenance,
        "gate_no_worsen_1": gate_no_worsen_1,
        "gate_no_worsen_2": gate_no_worsen_2,
        "gate_final": gate_final,
        "gate": bool(
            gate_provenance and gate_no_worsen_1 and gate_no_worsen_2 and gate_final
        ),
    }


def wide_domain_grid_refinement_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Fixed-bound grid-spacing halving at a_max=100 and a_max=200."""
    k_c100 = variants["C100"][1].result.final.capital
    k_f100 = variants["F100"][1].result.final.capital
    k_c200 = variants["C200"][1].result.final.capital
    k_f200 = variants["F200"][1].result.final.capital
    d_grid_100 = float(abs(k_f100 - k_c100) / max(1.0, abs(k_f100)))
    d_grid_200 = float(abs(k_f200 - k_c200) / max(1.0, abs(k_f200)))
    gate_100 = bool(d_grid_100 <= 0.005)
    gate_200_no_worsen = bool(d_grid_200 <= d_grid_100 + 1e-12)
    gate_200_final = bool(d_grid_200 <= 0.005)

    def rel_fields(cfg_name: str, fine_name: str) -> dict[str, float]:
        c = variants[cfg_name][1].result.final
        f = variants[fine_name][1].result.final
        return {
            "output": relative_diff(f.output, c.output),
            "wage": relative_diff(f.wage, c.wage),
            "net_capital_return": relative_diff(f.net_capital_return, c.net_capital_return),
            "transfer": relative_diff(f.transfer, c.transfer),
            "mean_consumption": relative_diff(f.mean_consumption, c.mean_consumption),
            "mean_assets": relative_diff(f.mean_assets, c.mean_assets),
        }

    rel_100 = rel_fields("C100", "F100")
    rel_200 = rel_fields("C200", "F200")
    return {
        "k_c100": float(k_c100),
        "k_f100": float(k_f100),
        "k_c200": float(k_c200),
        "k_f200": float(k_f200),
        "d_grid_100": d_grid_100,
        "d_grid_200": d_grid_200,
        "gate_100": gate_100,
        "gate_200_no_worsen": gate_200_no_worsen,
        "gate_200_final": gate_200_final,
        "gate": bool(gate_100 and gate_200_no_worsen and gate_200_final),
        "relative_diffs_c100_f100": rel_100,
        "relative_diffs_c200_f200": rel_200,
        "flags_gt_half_percent_100": {k: bool(v > 0.005) for k, v in rel_100.items()},
        "flags_gt_half_percent_200": {k: bool(v > 0.005) for k, v in rel_200.items()},
    }


def tail_diagnostics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Tail evidence for C50/C100/C150/C200 plus fine-bound observation."""
    rows: dict[str, dict[str, float]] = {}
    for name in ("C50", "C100", "C150", "C200"):
        config, diag = variants[name]
        final = diag.result.final
        grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
        top5_mask = grid >= 0.95 * config.a_max
        rows[name] = {
            "capital": final.capital,
            "output": final.output,
            "wage": final.wage,
            "net_capital_return": final.net_capital_return,
            "transfer": final.transfer,
            "mean_consumption": final.mean_consumption,
            "upper_boundary_mass": final.distribution.upper_boundary_mass,
            "top5_mass": float(np.sum(final.distribution.mass[:, top5_mask])),
            "mean_assets_over_amax": final.mean_assets / config.a_max,
        }
    successive: dict[str, float] = {}
    for prev, cur in (("C50", "C100"), ("C100", "C150"), ("C150", "C200")):
        successive[f"{prev}_to_{cur}"] = relative_diff(
            rows[prev]["capital"], rows[cur]["capital"]
        )
    k_f100 = variants["F100"][1].result.final.capital
    k_f200 = variants["F200"][1].result.final.capital
    d_fine_bound = float(abs(k_f200 - k_f100) / max(1.0, abs(k_f200)))
    return {
        "rows": rows,
        "successive_relative_changes": successive,
        "k_f100": float(k_f100),
        "k_f200": float(k_f200),
        "d_fine_bound_100_200": d_fine_bound,
        "d_fine_bound_flag_gt_half_percent": bool(d_fine_bound > 0.005),
    }


def reproducibility_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Two identical runs per new variant (C150, C200, F100, F200)."""
    results: dict[str, dict[str, float]] = {}
    for name in ("C150", "C200", "F100", "F200"):
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
