"""Pure economics / algebra tests for DLH-2A (Tier-0A)."""

import numpy as np
import pytest

from deep_learning_hank.economics.firm import production_block
from deep_learning_hank.economics.fiscal import balanced_fiscal
from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
    stationary_state_probabilities,
)
from deep_learning_hank.economics.preferences import (
    inverse_marginal_utility,
    marginal_utility,
    utility,
)


def test_crra_utility_marginal_inverse_identity() -> None:
    consumption = np.array([0.5, 1.0, 2.0])
    marginal = marginal_utility(consumption, gamma=2.0)
    np.testing.assert_allclose(inverse_marginal_utility(marginal, gamma=2.0), consumption)
    np.testing.assert_allclose(utility(consumption, gamma=2.0), [-2.0, -1.0, -0.5])


def test_crra_log_case_and_errors() -> None:
    np.testing.assert_allclose(utility(np.array([1.0, np.e]), gamma=1.0), [0.0, 1.0])
    with pytest.raises(ValueError):
        utility(np.array([0.0]), gamma=2.0)
    with pytest.raises(ValueError):
        marginal_utility(np.array([1.0]), gamma=0.0)


def test_asset_grid_matches_fixture_bounds_and_dimension() -> None:
    grid = build_asset_grid(0.0, 50.0, 40)
    assert grid.shape == (40,)
    assert grid[0] == 0.0
    assert grid[-1] == 50.0
    assert np.all(np.diff(grid) > 0.0)


def test_two_state_ctmc_generator_contract() -> None:
    generator = build_idiosyncratic_generator(0.25, 0.25)
    np.testing.assert_allclose(generator.sum(axis=1), 0.0, atol=1e-15)
    assert np.all(generator.sum(axis=1) == 0.0)
    # off-diagonal rates >= 0; diagonal = negative total outflow
    assert generator[0, 1] >= 0.0 and generator[1, 0] >= 0.0
    assert generator[0, 0] == -generator[0, 1]
    assert generator[1, 1] == -generator[1, 0]


def test_analytic_stationary_probabilities_symmetric() -> None:
    generator = build_idiosyncratic_generator(0.25, 0.25)
    probabilities = stationary_state_probabilities(generator)
    np.testing.assert_allclose(probabilities, [0.5, 0.5], atol=1e-14)
    np.testing.assert_allclose(probabilities @ generator, 0.0, atol=1e-14)


def test_two_factor_cobb_douglas_factor_price_identities() -> None:
    result = production_block(capital=4.0, labor=1.0, productivity=1.0, alpha_k=0.30, delta=0.02)
    assert result.output == pytest.approx(4.0**0.30)
    assert result.mpk == pytest.approx(0.30 * result.output / 4.0)
    assert result.net_capital_return == pytest.approx(result.mpk - 0.02)
    assert result.wage == pytest.approx(0.70 * result.output)


def test_balanced_fiscal_identity() -> None:
    fiscal = balanced_fiscal(wage=1.57, labor=1.0, tau_l=0.15, public_outlay=0.0)
    assert fiscal.labor_tax_revenue == pytest.approx(0.15 * 1.57)
    assert fiscal.transfer == pytest.approx(fiscal.labor_tax_revenue)
    assert fiscal.residual == 0.0
