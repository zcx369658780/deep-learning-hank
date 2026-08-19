"""DLH-2A fixed-price HJB + stationary KFE validation gates.

Fixture: ``configs/dlh_2a_fixed_price_validation.toml`` —
``VALIDATION_FIXTURE_NOT_CALIBRATION`` (numerical regression values only).
"""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.config import FixedPriceConfig
from deep_learning_hank.diagnostics.tier0_fixed_price import run_fixed_price_validation

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_2a_fixed_price_validation.toml"


@pytest.fixture(scope="module")
def diagnostics():
    config = FixedPriceConfig.from_toml(FIXTURE_PATH)
    return run_fixed_price_validation(config)


def test_fixture_is_not_calibration_label() -> None:
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text
    assert "calibration" in text.lower()


def test_hjb_gate_converges_and_residual(diagnostics) -> None:
    hh = diagnostics.household
    assert hh.converged
    assert hh.true_residual <= 1e-7
    assert hh.iterations <= 2000


def test_hjb_gate_consumption_and_boundary(diagnostics) -> None:
    hh = diagnostics.household
    assert hh.min_consumption > 0.0
    assert hh.lower_boundary_min_drift >= -1e-12
    assert hh.upper_boundary_max_drift <= 1e-12


def test_hjb_gate_generator_contract(diagnostics) -> None:
    hh = diagnostics.household
    assert hh.generator_row_sum_max_abs <= 1e-12
    # Literal minimum over ALL off-diagonal matrix entries, including implicit
    # sparse zeros: for a generator with all stored rates >= 0 this is 0.0.
    assert hh.generator_min_off_diagonal >= -1e-14
    assert hh.generator_min_off_diagonal == 0.0
    assert hh.nan_inf_count == 0
    # CTMC generator contract: rows sum to 0 (not row-stochastic)
    row_sums = np.asarray(hh.generator.sum(axis=1)).ravel()
    np.testing.assert_allclose(row_sums, 0.0, atol=1e-12)


def test_kfe_gate_mass_and_stationarity(diagnostics) -> None:
    dist = diagnostics.distribution
    assert dist.mass_error <= 1e-10
    assert dist.stationarity_residual <= 1e-8


def test_kfe_gate_nonnegativity_and_marginals(diagnostics) -> None:
    dist = diagnostics.distribution
    assert dist.minimum_mass >= -1e-12
    assert dist.negative_mass_count == 0
    assert dist.nan_inf_count == 0
    np.testing.assert_allclose(dist.state_marginals, [0.5, 0.5], atol=1e-8)
    assert 0.0 <= dist.mean_assets <= 50.0
    assert dist.mean_consumption > 0.0


def test_all_gates_pass(diagnostics) -> None:
    assert diagnostics.all_gates_pass
