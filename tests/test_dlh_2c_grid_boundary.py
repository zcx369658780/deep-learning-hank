"""DLH-2C grid / boundary / residual-shape / reproducibility tests.

Issue #7's ``test_upper_bound_sensitivity_gate`` was independently accepted as
a scientific blocker (``DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED``).  Per
Issue #8, that test is converted here into a **provenance regression
assertion** that preserves the accepted scientific failure
(``d_bound_K = 0.03411577346665587 > 0.005``) so canonical main has no
unexplained red test.  It does NOT relax the Issue #7 gate and does NOT claim
Issue #7 passed.  The active asset-domain adequacy gates live in
``tests/test_dlh_2c_b1_asset_domain.py``.
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


def test_issue7_blocker_provenance_regression(variants) -> None:
    """Accepted Issue #7 blocker provenance (NOT a PASS).

    Issue #7 was independently accepted as
    ``DLH_2C_BOUNDARY_SENSITIVITY_BLOCKED_ACCEPTED``: the ``a_max=50`` domain
    is NOT adequate under the frozen 0.5% upper-bound criterion.  This
    assertion preserves that accepted scientific fact: the frozen Issue #7
    fixture (G80_50 vs W159_100, matched spacing 50/79) must still reproduce
    ``d_bound_K > 0.005`` with the accepted value ``0.03411577346665587``
    within a tight tolerance.  It does NOT relax the Issue #7 gate, and it
    does NOT claim Issue #7 passed.
    """
    metrics = upper_bound_sensitivity_metrics(variants)
    d_bound_k = metrics["d_bound_K"]
    accepted = 0.03411577346665587
    assert d_bound_k > 0.005, (
        "Issue #7 blocker provenance violated: d_bound_K must remain > 0.005 "
        f"(observed {d_bound_k:.12f})"
    )
    assert abs(d_bound_k - accepted) <= 1e-12, (
        f"Issue #7 accepted value drift: d_bound_K = {d_bound_k:.17f} vs "
        f"accepted {accepted}"
    )
    assert metrics["gate"] is False  # the Issue #7 gate is still not passed


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
