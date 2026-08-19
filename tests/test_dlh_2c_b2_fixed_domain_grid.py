"""DLH-2C-B2 fixed-domain third-level grid convergence tests (active gates).

Fixed asset domain ``a in [0,200]``; three-level sequence C200 -> F200 -> Q200
(spacing h -> h/2 -> h/4 = 50/79 -> 25/79 -> 12.5/79).  All economics and
thresholds are the accepted DLH-2B fixture (``VALIDATION_FIXTURE_NOT_CALIBRATION``).
"""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_fixed_domain_grid import (
    GRID_CONFIGS,
    fixed_domain_grid_convergence_metrics,
    load_variants,
    macro_object_convergence_metrics,
    reproducibility_metrics,
    tail_diagnostics,
)


@pytest.fixture(scope="module")
def variants():
    return load_variants()


def test_q200_config_not_calibration_label() -> None:
    text = GRID_CONFIGS["Q200"].read_text(encoding="utf-8")
    assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text
    assert "calibration" in text.lower()


def test_grid_spacing_sequence() -> None:
    spacings = {}
    for name in ("C200", "F200", "Q200"):
        cfg = SteadyStateConfig.from_toml(GRID_CONFIGS[name])
        assert cfg.a_max == 200.0, name  # fixed domain
        spacings[name] = (cfg.a_max - cfg.a_min) / (cfg.asset_grid_count - 1)
    assert spacings["C200"] == pytest.approx(50.0 / 79.0, abs=1e-15)
    assert spacings["F200"] == pytest.approx(25.0 / 79.0, abs=1e-15)
    assert spacings["Q200"] == pytest.approx(12.5 / 79.0, abs=1e-15)
    assert spacings["Q200"] == pytest.approx(spacings["F200"] / 2.0, abs=1e-15)


def test_q200_per_variant_numerical_gates(variants) -> None:
    diagnostics = variants["Q200"][1]
    assert diagnostics.all_gates_pass
    final = diagnostics.result.final
    assert diagnostics.root_trace_finite_ok
    assert diagnostics.result.root_converged
    assert abs(final.capital_residual) <= 1e-7
    assert final.hjb_true_residual <= 1e-7
    assert final.hjb_min_consumption > 0.0
    assert final.hjb_lower_boundary_min_drift >= -1e-12
    assert final.hjb_upper_boundary_max_drift <= 1e-12
    assert final.hjb_generator_row_sum_max_abs <= 1e-12
    assert final.hjb_generator_min_off_diagonal >= -1e-14
    assert final.hjb_nan_inf_count == 0
    assert final.kfe_mass_error <= 1e-10
    assert final.kfe_stationarity_residual <= 1e-8
    assert final.kfe_minimum_mass >= -1e-12
    assert final.kfe_negative_mass_count == 0
    assert final.kfe_nan_inf_count == 0
    assert abs(diagnostics.effective_labor_error) <= 1e-8
    assert abs(final.goods_residual) <= 1e-7
    assert abs(final.household_budget_residual) <= 1e-7
    assert abs(final.mean_drift) <= 1e-7
    assert final.output > 0.0 and final.wage > 0.0 and final.mean_consumption > 0.0
    assert final.capital > 0.0 and np.isfinite(final.net_capital_return)


def test_fixed_domain_grid_convergence_gates(variants) -> None:
    metrics = fixed_domain_grid_convergence_metrics(variants)
    # Issue #8 provenance preserved (d_C_F reproduced within 1e-12).
    assert metrics["gate_provenance"], (
        f"d_C_F = {metrics['d_C_F']:.17f} does not reproduce accepted "
        f"{metrics['accepted_d_C_F']}"
    )
    assert metrics["gate_no_worsen"], (
        "BLOCKED_DLH_2C_B2_FIXED_DOMAIN_GRID_NOT_CONVERGED: "
        f"d_F_Q = {metrics['d_F_Q']:.12f} > d_C_F + 1e-12 "
        f"(d_C_F = {metrics['d_C_F']:.12f})"
    )
    assert metrics["gate_final"], (
        "BLOCKED_DLH_2C_B2_FIXED_DOMAIN_GRID_NOT_CONVERGED: "
        f"d_F_Q = {metrics['d_F_Q']:.12f} > 0.005"
    )
    assert metrics["gate"]
    # Refinement ratio is an observation (STRONG_REFINEMENT_OBSERVATION if <= 0.5);
    # it is not a mandatory gate and is not imposed ex-post.
    ratio = metrics["ratio_d_F_Q_over_d_C_F"]
    assert ratio is not None and ratio > 0.0
    assert metrics["strong_refinement_observation"] == (ratio <= 0.5)


def test_macro_object_fixed_domain_convergence(variants) -> None:
    metrics = macro_object_convergence_metrics(variants)
    assert metrics["gate"], (
        "BLOCKED_DLH_2C_B2_MACRO_GRID_CONVERGENCE: "
        f"F200->Q200 relative diffs = {metrics['relative_diffs_F200_Q200']}"
    )
    for name, diff in metrics["relative_diffs_F200_Q200"].items():
        assert diff <= 0.005, f"{name} rel diff {diff} > 0.005"


def test_tail_diagnostics_observations(variants) -> None:
    metrics = tail_diagnostics(variants)
    for name, row in metrics["rows"].items():
        assert 0.0 <= row["upper_boundary_mass"] <= 1.0, name
        assert 0.0 <= row["top5_mass"] <= 1.0, name
        assert row["mean_assets_over_amax"] >= 0.0, name


def test_q200_reproducibility(variants) -> None:
    metrics = reproducibility_metrics(variants)
    assert metrics["gate"], (
        "BLOCKED_DLH_2C_B2_REPRODUCIBILITY_THRESHOLD: "
        f"max abs diffs = {metrics['max_abs_diffs']}"
    )
