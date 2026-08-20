"""DLH-4A two-asset generator tests (Issue #17).

Verifies the machinery properties of the reconstructed two-asset generator:
``G = G_b + G_a + G_z`` structure, exact rows-sum-zero (mass conservation),
non-negative off-diagonals (valid infinitesimal-generator rates), and the pure
z-switch block.  The honest outcome of the Issue #17 validation gates (HJB
monotonicity / KFE uniqueness on the reference fixture) is reported by
``run_two_asset_diagnostics`` and the execution report, not asserted here.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.two_asset.config import TwoAssetConfig
from deep_learning_hank.two_asset.household_hjb import (
    build_generator,
    solve_two_asset_household,
)

CONFIG_PATH = Path("configs/dlh_4a_two_asset_household_validation.toml")


def _solve():
    config = TwoAssetConfig.from_toml(CONFIG_PATH)
    b_grid = np.linspace(config.b_min, config.b_max, config.b_points)
    a_grid = np.linspace(config.a_min, config.a_max, config.a_points)
    z_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = np.array(
        [[-config.q_low_to_high, config.q_low_to_high], [config.q_high_to_low, -config.q_high_to_low]]
    )
    return solve_two_asset_household(
        b_grid=b_grid,
        a_grid=a_grid,
        z_states=z_states,
        state_generator=state_generator,
        w=config.w,
        rb=config.rb,
        rb_gap=config.rb_gap,
        ra=config.ra,
        Tt=config.Tt,
        tau_l=config.tau_l,
        rho=config.rho,
        gamma=config.gamma,
        alphac=config.alphac,
        alphal=config.alphal,
        frisch_l=config.frisch_l,
        n_max=config.n_max,
        chi0=config.chi0,
        chi1=config.chi1,
        a_bar=config.a_bar,
        consumption_floor=config.consumption_floor,
        pseudo_time_step=config.pseudo_time_step,
        value_change_tolerance=config.value_change_tolerance,
        max_value_iterations=config.max_value_iterations,
    )


def test_generator_row_sums_zero():
    config = TwoAssetConfig.from_toml(CONFIG_PATH)
    result = _solve()
    assert result.generator_row_sum_max_abs <= config.generator_row_sum_tolerance


def test_generator_off_diagonals_nonnegative():
    config = TwoAssetConfig.from_toml(CONFIG_PATH)
    result = _solve()
    assert result.generator_min_off_diagonal >= config.generator_min_off_diagonal_tolerance


def test_generator_finite():
    result = _solve()
    assert result.nan_inf_count == 0
    assert np.all(np.isfinite(result.generator.data))


def test_generator_dimensions():
    config = TwoAssetConfig.from_toml(CONFIG_PATH)
    result = _solve()
    size = config.b_points * config.a_points * 2
    assert result.generator.shape == (size, size)


def test_generator_z_switch_block():
    """With zero drifts the generator reduces to the pure idiosyncratic switch."""
    config = TwoAssetConfig.from_toml(CONFIG_PATH)
    i_count, j_count, nz_count = config.b_points, config.a_points, 2
    zero_b = np.zeros((i_count, j_count, nz_count))
    zero_a = np.zeros_like(zero_b)
    state_generator = np.array(
        [[-config.q_low_to_high, config.q_low_to_high], [config.q_high_to_low, -config.q_high_to_low]]
    )
    g = build_generator(zero_b, zero_a, state_generator).toarray()
    size = i_count * j_count * nz_count
    block = i_count * j_count
    # z transitions on matching asset nodes at rate q; diagonal -q.
    assert abs(g[0, block] - config.q_low_to_high) < 1e-12
    assert abs(g[block, 0] - config.q_high_to_low) < 1e-12
    assert abs(g[0, 0] + config.q_low_to_high) < 1e-12
    assert abs(g[0, size - 1]) < 1e-12  # no cross-block-to-wrong-node coupling
