"""DLH-2C grid / boundary / residual-shape / reproducibility tests.

Note on the upper-bound sensitivity test: it asserts the Issue #7 gate
``d_bound_K <= 0.005``.  If the accepted benchmark does not satisfy it, the
test FAILS on purpose — that is the documented fail-closed evidence
``BLOCKED_DLH_2C_BOUNDARY_SENSITIVITY`` — and the execution report records the
exact value.  No economics, grid standard, or threshold is modified to force a
PASS.
"""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_robustness import (
    BASELINE_CONFIG,
    VARIANT_CONFIGS,
    grid_convergence_metrics,
    load_variants,
    relative_diff,
    reproducibility_metrics,
    residual_scan,
    upper_bound_sensitivity_metrics,
)

VARIANT_NAMES = ("B40_50", "G80_50", "G160_50", "W159_100", "P40_50")


@pytest.fixture(scope="module")
def variants():
    return load_variants()


def test_variant_configs_not_calibration_labels() -> None:
    for name, path in VARIANT_CONFIGS.items():
        if name == "B40_50":
            continue  # accepted DLH-2B config already labeled
        text = path.read_text(encoding="utf-8")
        assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text, name
        assert "calibration" in text.lower(), name


def test_spacing_match_g80_w159() -> None:
    cfg80 = SteadyStateConfig.from_toml(VARIANT_CONFIGS["G80_50"])
    cfg100 = SteadyStateConfig.from_toml(VARIANT_CONFIGS["W159_100"])
    spacing80 = (cfg80.a_max - cfg80.a_min) / (cfg80.asset_grid_count - 1)
    spacing100 = (cfg100.a_max - cfg100.a_min) / (cfg100.asset_grid_count - 1)
    assert spacing80 == pytest.approx(spacing100, abs=1e-15)


def test_per_variant_numerical_gates(variants) -> None:
    for name in VARIANT_NAMES:
        diagnostics = variants[name][1]
        assert diagnostics.all_gates_pass, name
        final = diagnostics.result.final
        assert diagnostics.root_trace_finite_ok, name
        assert diagnostics.result.root_converged, name
        assert abs(final.capital_residual) <= 1e-7, name
        assert final.hjb_true_residual <= 1e-7, name
        assert final.hjb_min_consumption > 0.0, name
        assert final.kfe_mass_error <= 1e-10, name
        assert final.kfe_stationarity_residual <= 1e-8, name
        assert abs(diagnostics.effective_labor_error) <= 1e-8, name


def test_grid_convergence_gates(variants) -> None:
    metrics = grid_convergence_metrics(variants)
    assert metrics["gate_no_worsen"]
    assert metrics["d80_160"] <= metrics["d40_80"] + 1e-12
    assert metrics["gate_final"]
    assert metrics["d80_160"] <= 0.005
    # Observation flags: any 80->160 relative difference > 0.5% is flagged.
    flags = metrics["flags_gt_half_percent"]
    for field, flagged in flags.items():
        assert not flagged, (
            f"observation relative diff 80->160 for {field} exceeds 0.5%: "
            f"{metrics['relative_diffs_80_160'][field]:.6f} (flagged for reviewer)"
        )


def test_upper_bound_sensitivity_gate(variants) -> None:
    metrics = upper_bound_sensitivity_metrics(variants)
    assert metrics["d_bound_K"] <= 0.005, (
        "BLOCKED_DLH_2C_BOUNDARY_SENSITIVITY: "
        f"d_bound_K = {metrics['d_bound_K']:.8f} > 0.005 "
        f"(K50={metrics['k50']:.10f}, K100={metrics['k100']:.10f}); "
        "not modified to force a PASS — actual diagnostics in report"
    )
    assert metrics["gate"]


def test_residual_scan_single_root_interval(variants) -> None:
    config = variants["B40_50"][0]
    scan = residual_scan(config, points=21)
    assert scan["all_finite"]
    assert scan["sign_changing_intervals"] == 1, (
        "BLOCKED_DLH_2C_MULTIPLE_BOUNDED_ROOT_INTERVALS: "
        f"{scan['sign_changing_intervals']} intervals detected"
    )
    assert scan["gate"]


def test_reproducibility_variants(variants) -> None:
    metrics = reproducibility_metrics(variants)
    assert metrics["gate"], (
        "BLOCKED_DLH_2C_REPRODUCIBILITY_THRESHOLD: "
        f"per-variant diffs = {metrics['per_variant_max_abs_diffs']}"
    )
