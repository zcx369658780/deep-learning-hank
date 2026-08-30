"""DLH-4D GE solver machinery tests (Issue #20).

Tests the frozen bracketing protocol (full interval first, one uniform 9-point
scan, exactly one sign-changing interval or exact grid root, zero/multiple
brackets fail closed) and the deterministic cold initialization adapter, on
lightweight synthetic inputs.  The full nested GE solve is executed and
evidenced in the DLH-4D execution run (multi-hour; report + CSV), not in this
unit test.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.ge import GeConfig, RootBracketError, build_cold_initialization
from deep_learning_hank.ge.two_asset_single_region import (
    MultipleSteadyStateBracketsError,
    _find_bracket,
)
from deep_learning_hank.two_asset import (
    EconomicParams,
    MatlabFaithfulHJBGrid,
)

CONFIG_PATH = Path("configs/dlh_4d_two_asset_single_region_ge_validation.toml")


def _config():
    return GeConfig.from_toml(CONFIG_PATH)


def test_bracket_full_interval_first():
    cfg = _config()
    residual = lambda x: 2.0 * (x - 0.5)  # noqa: E731
    bracket, from_scan, _ = _find_bracket(residual, 0.0, 1.0, cfg.bracket_scan_points, "t")
    assert not from_scan
    assert bracket == (0.0, 1.0)


def test_bracket_via_scan_with_nan_neighborhood():
    """A single sign-changing interval found only in the scan (non-finite
    neighbors, as can occur when a household solve fails at some candidates)."""
    cfg = _config()
    residual = lambda x: np.nan if x < 0.3 else (x - 0.55)  # noqa: E731
    bracket, from_scan, _ = _find_bracket(residual, 0.0, 1.0, cfg.bracket_scan_points, "t")
    assert from_scan
    lo, hi = bracket
    assert lo <= 0.55 <= hi


def test_bracket_zero_fails_closed():
    cfg = _config()
    residual = lambda x: 1.0 + x * x  # noqa: E731  (no real root)
    try:
        _find_bracket(residual, 0.0, 1.0, cfg.bracket_scan_points, "t")
        raise AssertionError("expected RootBracketError")
    except RootBracketError:
        pass


def test_bracket_multiple_fails_closed():
    cfg = _config()
    # Two roots inside (0,1) with same-sign endpoints: the full interval does
    # not bracket, and the scan finds two sign-changing intervals -> fail closed.
    residual = lambda x: (x - 0.3) * (x - 0.7)  # noqa: E731
    try:
        _find_bracket(residual, 0.0, 1.0, cfg.bracket_scan_points, "t")
        raise AssertionError("expected MultipleSteadyStateBracketsError")
    except MultipleSteadyStateBracketsError:
        pass


def test_cold_initialization_deterministic_and_positive():
    cfg = _config()
    grid = MatlabFaithfulHJBGrid(
        np.linspace(cfg.b_min, cfg.b_max, cfg.b_points),
        np.linspace(cfg.a_min, cfg.a_max, cfg.a_points),
        np.asarray(cfg.z_states, dtype=np.float64),
        np.asarray(cfg.switch_matrix, dtype=np.float64),
    )
    params = EconomicParams(
        rho=cfg.rho, gamma_c=cfg.gamma_c, phi=cfg.phi, chi_0=cfg.chi_0,
        chi_1=cfg.chi_1, a_bar=cfg.a_bar, mu_z=cfg.mu_z, sigma_z=cfg.sigma_z,
    )
    a = build_cold_initialization(
        grid, params, r_a=0.03, r_b=0.015, w=1.0, transfer_income=0.1,
        rb_gap=cfg.rb_gap, tau=cfg.tau,
    )
    b = build_cold_initialization(
        grid, params, r_a=0.03, r_b=0.015, w=1.0, transfer_income=0.1,
        rb_gap=cfg.rb_gap, tau=cfg.tau,
    )
    initial, labor0 = a
    assert float(np.max(np.abs(a[0] - b[0]))) == 0.0
    assert float(np.max(np.abs(a[1] - b[1]))) == 0.0
    assert np.all(np.isfinite(initial)) and np.all(np.isfinite(labor0))
    assert np.all(labor0 > 0.0)
    # initial value = flow utility / rho (u(c) < 0 for gamma_c=2 -> value < 0)
    assert np.all(initial < 0.0)
