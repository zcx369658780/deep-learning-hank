"""DLH-2B accounting tests: fiscal, goods/resource, household aggregate
budget, mean-drift diagnostics (computed independently, not zeroed)."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_steady_state import run_tier0_steady_state

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_2b_tier0_steady_state_validation.toml"


@pytest.fixture(scope="module")
def diagnostics():
    config = SteadyStateConfig.from_toml(FIXTURE_PATH)
    return run_tier0_steady_state(config)


def test_fiscal_balanced_identity(diagnostics) -> None:
    config = SteadyStateConfig.from_toml(FIXTURE_PATH)
    final = diagnostics.result.final
    expected_transfer = config.tau_l * final.wage * diagnostics.l_bar - config.public_outlay
    assert abs(final.transfer - expected_transfer) <= 1e-12
    assert diagnostics.fiscal_ok


def test_goods_resource_residual(diagnostics) -> None:
    final = diagnostics.result.final
    # R_goods = Y - C - delta*K - G, computed from independently aggregated objects.
    assert abs(final.goods_residual) <= 1e-7
    assert diagnostics.goods_ok


def test_household_aggregate_budget_residual(diagnostics) -> None:
    final = diagnostics.result.final
    # R_hh_budget = C - [(1-tau_l)*w*L_g + r*A_hh + transfer]
    assert abs(final.household_budget_residual) <= 1e-7
    assert diagnostics.budget_ok


def test_mean_drift_diagnostic(diagnostics) -> None:
    final = diagnostics.result.final
    assert abs(final.mean_drift) <= 1e-7
    assert diagnostics.mean_drift_ok


def test_positivity_and_finite_return(diagnostics) -> None:
    final = diagnostics.result.final
    assert final.output > 0.0
    assert final.wage > 0.0
    assert final.mean_consumption > 0.0
    assert final.capital > 0.0
    assert np.isfinite(final.net_capital_return)
    assert diagnostics.positivity_ok


def test_all_accounting_gates_pass(diagnostics) -> None:
    assert diagnostics.all_gates_pass
