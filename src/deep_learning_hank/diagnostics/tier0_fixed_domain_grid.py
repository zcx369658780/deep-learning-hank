"""DLH-2C-B2 fixed-domain third-level grid convergence / canonical Tier-0
numerical standard.

Frozen asset domain ``a in [0, 200]``.  Freezes the accepted economics and
solver family (DLH-2A/2B/2C/2C-B1); varies only grid resolution.

Grids on the fixed domain (all ``VALIDATION_FIXTURE_NOT_CALIBRATION``):
  * C200 = accepted 317 pts  [0,200], spacing h    = 50/79  (read-only)
  * F200 = accepted 633 pts  [0,200], spacing h/2  = 25/79  (read-only)
  * Q200 = new      1265 pts [0,200], spacing h/4  = 12.5/79

Gates (Issue #9):
  * Q200 per-variant numerical gates (accepted thresholds);
  * fixed-domain successive grid convergence: d_C_F reproduces accepted
    0.004952190294576287 (<=1e-12); d_F_Q <= d_C_F + 1e-12; d_F_Q <= 0.005;
    refinement ratio reported (STRONG_REFINEMENT_OBSERVATION if <= 0.5;
    observation only, not a gate);
  * macro-object fixed-domain convergence F200->Q200 (each rel diff <= 0.005);
  * upper-tail diagnostics on Q200 (observations);
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
    "GRID_CONFIGS",
    "ACCEPTED_D_C_F",
    "load_variants",
    "relative_diff",
    "fixed_domain_grid_convergence_metrics",
    "macro_object_convergence_metrics",
    "tail_diagnostics",
    "reproducibility_metrics",
]

REPO_ROOT = Path(__file__).resolve().parents[3]

GRID_CONFIGS: dict[str, Path] = {
    "C200": REPO_ROOT / "configs" / "dlh_2c_b1_bound200_coarse_validation.toml",
    "F200": REPO_ROOT / "configs" / "dlh_2c_b1_bound200_fine_validation.toml",
    "Q200": REPO_ROOT / "configs" / "dlh_2c_b2_bound200_quarter_spacing_validation.toml",
}

ACCEPTED_D_C_F = 0.004952190294576287


def relative_diff(reference: float, value: float) -> float:
    """Relative difference ``abs(value - reference)/max(1, abs(value))``."""
    return float(abs(value - reference) / max(1.0, abs(value)))


def load_variants() -> dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]]:
    """Run the accepted steady-state pipeline for C200, F200, Q200."""
    loaded: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]] = {}
    for name, path in GRID_CONFIGS.items():
        config = SteadyStateConfig.from_toml(path)
        diagnostics = run_tier0_steady_state(config)
        loaded[name] = (config, diagnostics)
    return loaded


def fixed_domain_grid_convergence_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Successive fixed-domain refinement C200 -> F200 -> Q200 (h -> h/2 -> h/4)."""
    k_c = variants["C200"][1].result.final.capital
    k_f = variants["F200"][1].result.final.capital
    k_q = variants["Q200"][1].result.final.capital
    d_c_f = float(abs(k_f - k_c) / max(1.0, abs(k_f)))
    d_f_q = float(abs(k_q - k_f) / max(1.0, abs(k_q)))
    gate_provenance = bool(abs(d_c_f - ACCEPTED_D_C_F) <= 1e-12)
    gate_no_worsen = bool(d_f_q <= d_c_f + 1e-12)
    gate_final = bool(d_f_q <= 0.005)
    ratio = float(d_f_q / d_c_f) if d_c_f > 0.0 else None
    return {
        "k_c": float(k_c),
        "k_f": float(k_f),
        "k_q": float(k_q),
        "d_C_F": d_c_f,
        "d_F_Q": d_f_q,
        "accepted_d_C_F": ACCEPTED_D_C_F,
        "gate_provenance": gate_provenance,
        "gate_no_worsen": gate_no_worsen,
        "gate_final": gate_final,
        "gate": bool(gate_provenance and gate_no_worsen and gate_final),
        "ratio_d_F_Q_over_d_C_F": ratio,
        "strong_refinement_observation": bool(ratio is not None and ratio <= 0.5),
    }


def macro_object_convergence_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """F200 -> Q200 fixed-domain macro-object relative differences."""
    f_final = variants["F200"][1].result.final
    q_final = variants["Q200"][1].result.final
    fields = {
        "output": "output",
        "wage": "wage",
        "net_capital_return": "net_capital_return",
        "transfer": "transfer",
        "mean_consumption": "mean_consumption",
        "mean_assets": "mean_assets",
    }
    rel_diffs: dict[str, float] = {}
    for key, attr in fields.items():
        rel_diffs[key] = relative_diff(getattr(q_final, attr), getattr(f_final, attr))
    gate = bool(all(value <= 0.005 for value in rel_diffs.values()))
    return {"relative_diffs_F200_Q200": rel_diffs, "gate": gate}


def tail_diagnostics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Upper-tail observations on the fixed domain (C200/F200/Q200)."""
    rows: dict[str, dict[str, float]] = {}
    for name in ("C200", "F200", "Q200"):
        config, diag = variants[name]
        final = diag.result.final
        grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
        top5_mask = grid >= 0.95 * config.a_max
        rows[name] = {
            "upper_boundary_mass": final.distribution.upper_boundary_mass,
            "top5_mass": float(np.sum(final.distribution.mass[:, top5_mask])),
            "mean_assets_over_amax": final.mean_assets / config.a_max,
        }
    return {"rows": rows}


def reproducibility_metrics(
    variants: dict[str, tuple[SteadyStateConfig, SteadyStateDiagnostics]],
) -> dict[str, object]:
    """Two identical runs of Q200."""
    config = variants["Q200"][0]
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
    gate = bool(all(diff <= 1e-12 for diff in diffs.values()))
    return {"max_abs_diffs": diffs, "gate": gate}
