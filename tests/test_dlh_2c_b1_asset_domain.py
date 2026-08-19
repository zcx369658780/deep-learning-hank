"""DLH-2C-B1 asset-domain adequacy / upper-tail convergence tests (active gates).

The wide-domain grid-refinement test asserts the Issue #8 gate
``d_grid_200 <= d_grid_100 + 1e-12`` and ``d_grid_200 <= 0.005``.  If the
accepted benchmark does not satisfy it, that test FAILS on purpose — the
documented fail-closed evidence ``BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE``
— and the execution report records the exact values.  No economics, grid
standard, domain criterion, or threshold is modified to force a PASS.
"""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_asset_domain import (
    COARSE_CONFIGS,
    FINE_CONFIGS,
    coarse_bound_convergence_metrics,
    load_variants,
    reproducibility_metrics,
    tail_diagnostics,
    wide_domain_grid_refinement_metrics,
)

COARSE_NAMES = ("C50", "C100", "C150", "C200")
FINE_NAMES = ("F100", "F200")


@pytest.fixture(scope="module")
def variants():
    return load_variants()


def test_variant_configs_not_calibration_labels() -> None:
    for name, path in {**COARSE_CONFIGS, **FINE_CONFIGS}.items():
        if name in ("C50", "C100"):
            continue  # accepted Issue #7 configs already labeled
        text = path.read_text(encoding="utf-8")
        assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text, name
        assert "calibration" in text.lower(), name


def test_coarse_spacing_matches() -> None:
    spacings = {}
    for name in ("C50", "C100", "C150", "C200"):
        cfg = SteadyStateConfig.from_toml(COARSE_CONFIGS[name])
        spacings[name] = (cfg.a_max - cfg.a_min) / (cfg.asset_grid_count - 1)
        assert spacings[name] == pytest.approx(50.0 / 79.0, abs=1e-15), name
    for name in ("F100", "F200"):
        cfg = SteadyStateConfig.from_toml(FINE_CONFIGS[name])
        spacings[name] = (cfg.a_max - cfg.a_min) / (cfg.asset_grid_count - 1)
        assert spacings[name] == pytest.approx(25.0 / 79.0, abs=1e-15), name


def test_per_variant_numerical_gates(variants) -> None:
    for name in ("C150", "C200", "F100", "F200"):
        diagnostics = variants[name][1]
        assert diagnostics.all_gates_pass, name
        final = diagnostics.result.final
        assert diagnostics.root_trace_finite_ok, name
        assert diagnostics.result.root_converged, name
        assert abs(final.capital_residual) <= 1e-7, name
        assert final.hjb_true_residual <= 1e-7, name
        assert final.hjb_min_consumption > 0.0, name
        assert final.hjb_lower_boundary_min_drift >= -1e-12, name
        assert final.hjb_upper_boundary_max_drift <= 1e-12, name
        assert final.hjb_generator_row_sum_max_abs <= 1e-12, name
        assert final.hjb_generator_min_off_diagonal >= -1e-14, name
        assert final.hjb_nan_inf_count == 0, name
        assert final.kfe_mass_error <= 1e-10, name
        assert final.kfe_stationarity_residual <= 1e-8, name
        assert final.kfe_minimum_mass >= -1e-12, name
        assert final.kfe_negative_mass_count == 0, name
        assert final.kfe_nan_inf_count == 0, name
        assert abs(diagnostics.effective_labor_error) <= 1e-8, name
        assert abs(final.goods_residual) <= 1e-7, name
        assert abs(final.household_budget_residual) <= 1e-7, name
        assert abs(final.mean_drift) <= 1e-7, name
        assert final.output > 0.0 and final.wage > 0.0 and final.mean_consumption > 0.0
        assert final.capital > 0.0 and np.isfinite(final.net_capital_return)


def test_coarse_bound_convergence_gates(variants) -> None:
    metrics = coarse_bound_convergence_metrics(variants)
    # Accepted Issue #7 blocker provenance preserved (d50_100 reproduced).
    assert metrics["gate_provenance"], (
        f"d50_100 = {metrics['d50_100']:.17f} does not reproduce accepted "
        f"{metrics['accepted_d50_100']}"
    )
    assert metrics["gate_no_worsen_1"], (
        f"d100_150 = {metrics['d100_150']:.12f} > d50_100 + 1e-12"
    )
    assert metrics["gate_no_worsen_2"], (
        f"d150_200 = {metrics['d150_200']:.12f} > d100_150 + 1e-12"
    )
    assert metrics["gate_final"], (
        "BLOCKED_DLH_2C_B1_ASSET_DOMAIN_NOT_CONVERGED: "
        f"d150_200 = {metrics['d150_200']:.12f} > 0.005"
    )
    assert metrics["gate"]


def test_wide_domain_grid_refinement_gates(variants) -> None:
    metrics = wide_domain_grid_refinement_metrics(variants)
    assert metrics["gate_100"], (
        "BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE: "
        f"d_grid_100 = {metrics['d_grid_100']:.12f} > 0.005"
    )
    assert metrics["gate_200_no_worsen"], (
        "BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE: "
        f"d_grid_200 = {metrics['d_grid_200']:.12f} > d_grid_100 + 1e-12 "
        f"(d_grid_100 = {metrics['d_grid_100']:.12f}); "
        "actual diagnostics preserved; not modified to force a PASS"
    )
    assert metrics["gate_200_final"], (
        "BLOCKED_DLH_2C_B1_WIDE_DOMAIN_GRID_CONVERGENCE: "
        f"d_grid_200 = {metrics['d_grid_200']:.12f} > 0.005"
    )
    assert metrics["gate"]


def test_tail_diagnostics_observations(variants) -> None:
    metrics = tail_diagnostics(variants)
    rows = metrics["rows"]
    for name in ("C50", "C100", "C150", "C200"):
        row = rows[name]
        assert row["capital"] > 0.0 and row["output"] > 0.0 and row["wage"] > 0.0
        assert 0.0 <= row["upper_boundary_mass"] <= 1.0
        assert 0.0 <= row["top5_mass"] <= 1.0
        assert row["mean_assets_over_amax"] >= 0.0
    # d_fine_bound_100_200 is an observation; if > 0.5% it must be flagged.
    d_fine = metrics["d_fine_bound_100_200"]
    assert metrics["d_fine_bound_flag_gt_half_percent"] == (d_fine > 0.005)


def test_reproducibility_variants(variants) -> None:
    metrics = reproducibility_metrics(variants)
    assert metrics["gate"], (
        "BLOCKED_DLH_2C_B1_REPRODUCIBILITY_THRESHOLD: "
        f"per-variant diffs = {metrics['per_variant_max_abs_diffs']}"
    )
