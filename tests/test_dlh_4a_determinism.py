"""DLH-4A two-asset kernel determinism tests (Issue #17).

The reconstruction is deterministic (no random numbers); two identical
household solves must produce identical results.  (The honest outcome of the
validation gates on the reference fixture is reported by the diagnostics layer
and the execution report, not asserted here.)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.two_asset.config import TwoAssetConfig
from deep_learning_hank.two_asset.household_hjb import solve_two_asset_household

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


def test_two_asset_solve_deterministic():
    first = _solve()
    second = _solve()
    assert float(np.max(np.abs(first.value - second.value))) == 0.0
    assert float(np.max(np.abs(first.consumption - second.consumption))) == 0.0
    assert float(np.max(np.abs(first.transfer - second.transfer))) == 0.0
    assert float(np.max(np.abs(first.generator.data - second.generator.data))) == 0.0
    assert first.iterations == second.iterations
