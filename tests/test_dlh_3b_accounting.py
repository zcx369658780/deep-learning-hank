"""DLH-3B accounting tests: goods, fiscal, profits and aggregate wealth-flow
residuals at the final equilibrium, computed independently (never zeroed by
labeling), plus the wealth-flow consistency chain."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_steady_state import run_hank_steady_state_cached
from deep_learning_hank.hank_config import HankSteadyStateConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3b_hank_steady_state_validation.toml"


@pytest.fixture(scope="module")
def diagnostics():
    config = HankSteadyStateConfig.from_toml(FIXTURE_PATH)
    return run_hank_steady_state_cached(config)


def test_goods_residual(diagnostics) -> None:
    # R_goods = Y - C because pi = 0 and G = 0.
    assert abs(diagnostics.R_goods) <= 1e-7
    assert diagnostics.accounting_ok


def test_fiscal_residual(diagnostics) -> None:
    # R_fiscal = tau_l*w*N - r*B - tr (constant-B budget identity).
    assert abs(diagnostics.R_fiscal) <= 1e-12


def test_profits_residual(diagnostics) -> None:
    # R_profits = Pi - (Y - w*N) at zero inflation.
    assert abs(diagnostics.R_profits) <= 1e-12


def test_wealth_flow_residual(diagnostics) -> None:
    # Steady-state aggregate wealth-flow identity (dot A_hh = 0):
    # (1-tau_l)*w*N + r*A_hh + tr + Pi - C = 0.
    assert abs(diagnostics.R_wealth) <= 1e-7


def test_wealth_flow_consistency_chain(diagnostics) -> None:
    final = diagnostics.result.final
    result = diagnostics.result
    # Chain: constant-B clearing + fiscal identity => C = w*N + Pi; profits
    # identity + goods clearing => C = Y.
    assert abs(final.C - (final.wage * result.root_N + final.profits)) <= 1e-7
    assert abs(final.C - final.output) <= 1e-7
    assert abs(final.A_hh - 10.0) <= 1e-7


def test_all_gates_pass(diagnostics) -> None:
    assert diagnostics.all_gates_pass
