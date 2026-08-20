"""DLH-3B-R2 kernel KFE / accounting tests.

Issue #15 §7: KFE mass conservation, non-negativity, and the explicit
accounting residuals (asset, labor, goods, fiscal, profits, wealth flow).
"""

from __future__ import annotations

from pathlib import Path

from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.ha_kernel.equilibrium import solve_kernel_equilibrium

CONFIG_PATH = Path("configs/dlh_3b_hank_steady_state_validation.toml")


def test_kernel_kfe_mass_and_nonnegativity():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = solve_kernel_equilibrium(config)
    dist = result.final.distribution
    assert dist.mass_error <= config.numerical.kfe_mass_tolerance
    assert dist.minimum_mass >= config.numerical.negative_mass_threshold
    assert dist.negative_mass_count == 0
    assert dist.nan_inf_count == 0
    assert abs(dist.state_marginals.sum() - 1.0) <= 1e-10


def test_kernel_accounting_residuals():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = solve_kernel_equilibrium(config)
    final = result.final
    assert abs(final.R_goods) <= config.numerical.goods_tolerance
    assert abs(final.R_fiscal) <= config.numerical.fiscal_tolerance
    assert abs(final.R_profits) <= config.numerical.profits_tolerance
    assert abs(final.R_wealth) <= config.numerical.wealth_tolerance


def test_kernel_asset_labor_clearing():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = solve_kernel_equilibrium(config)
    final = result.final
    assert abs(final.A_hh - config.bond_supply) <= 1e-6
    assert abs(final.N_hh - result.root_N) <= 1e-6
