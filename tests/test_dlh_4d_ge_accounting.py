"""DLH-4D GE accounting / faithful resource tests (Issue #20).

Verifies on a real candidate evaluation: the faithful resource objects
(``AC``, ``W_taper``, ``R_resource_structural``, ``R_resource_faithful``), the
fiscal residual, the aggregate wealth-flow diagnostics, separate ``A_hh`` /
``B_hh`` reporting, and the KFE density properties.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.ge import GeConfig, evaluate_ge

CONFIG_PATH = Path("configs/dlh_4d_two_asset_single_region_ge_validation.toml")


def _candidate():
    cfg = GeConfig.from_toml(CONFIG_PATH)
    return cfg, evaluate_ge(cfg, 0.02, 0.015, 1.0)


def test_ac_taper_wedge_faithful_decomposition():
    cfg, e = _candidate()
    assert e.finite
    # Faithful residual is the structural gap minus the taper wedge by definition.
    assert abs(e.R_resource_faithful - (e.R_resource_structural - e.W_taper)) < 1e-12
    # AC and W_taper are reported separately and finite.
    assert np.isfinite(e.AC) and np.isfinite(e.W_taper)
    # AC aggregates the adjustment cost read-only (nonnegative for chi0, chi1 > 0).
    assert e.AC >= -1e-12


def test_fiscal_residual():
    cfg, e = _candidate()
    assert e.finite
    # T is defined as the balanced transfer rule -> residual is exactly 0.
    assert abs(e.R_fiscal) <= cfg.fiscal_tolerance


def test_separate_asset_aggregates():
    _, e = _candidate()
    assert e.finite
    assert np.isfinite(e.A_hh) and np.isfinite(e.B_hh)
    # Reported separately; inequality is NOT a gate (Issue #20 gate 4).
    assert e.A_hh != e.B_hh or abs(e.A_hh - e.B_hh) > 0.0


def test_kfe_density_properties():
    cfg, e = _candidate()
    assert e.finite
    assert e.kfe_mass_error <= cfg.kfe_mass_tolerance
    assert e.kfe_min_mass >= cfg.kfe_min_mass_threshold


def test_hjb_convergence_at_candidate():
    cfg, e = _candidate()
    assert e.finite
    assert e.hjb_converged
    assert e.hjb_statistic <= cfg.convergence_tolerance


def test_wealth_flow_direct_stationarity():
    """The oracle-array aggregate drift is the exact stationary wealth flow."""
    _, e = _candidate()
    assert e.finite
    # At r_a = rho (no illiquid holdings) the direct flow is machine-zero.
    assert abs(e.R_wealth_direct) < 1e-9


def test_no_nan_in_final_objects():
    _, e = _candidate()
    assert e.finite
    assert e.nan_inf_count == 0
