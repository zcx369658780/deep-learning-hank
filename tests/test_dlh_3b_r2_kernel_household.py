"""DLH-3B-R2 kernel household HJB tests.

Issue #15 §5/§7: canonical one-asset household HJB must converge with a true
HJB residual within the frozen tolerance and satisfy the KKT / consumption-FOC
/ boundary / generator gates at the accepted steady-state inputs.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.economics.grids import build_asset_grid, build_idiosyncratic_generator
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.ha_kernel.household import solve_kernel_household

CONFIG_PATH = Path("configs/dlh_3b_hank_steady_state_validation.toml")
# Accepted DLH-3B steady-state inputs (frozen accepted provenance).
R_STAR = 0.007370613883670197
N_STAR = 1.0656334480169984
W_STAR = 5.0 / 6.0
TR_STAR = 0.05949804216542284
PI_STAR = 0.17760557466949967


def _household_at_steady_state():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    return solve_kernel_household(
        asset_grid=asset_grid,
        efficiency_states=efficiency_states,
        state_generator=state_generator,
        wage=W_STAR,
        real_return=R_STAR,
        transfer=TR_STAR,
        profits=PI_STAR,
        tau_l=config.tau_l,
        rho_hh=config.rho_hh,
        gamma=config.gamma,
        frisch=config.frisch,
        chi=config.chi,
        n_max=config.n_max,
        tolerance=config.numerical.hjb_tolerance,
        max_iterations=config.numerical.hjb_max_iterations,
        pseudo_time_step=config.numerical.hjb_pseudo_time_step,
        consumption_floor=config.numerical.consumption_floor,
    )


def test_kernel_household_converges_with_true_residual():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = _household_at_steady_state()
    assert result.converged
    assert result.true_residual <= config.numerical.hjb_tolerance


def test_kernel_household_kkt_and_consumption_foc():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = _household_at_steady_state()
    assert result.labor_kkt_max <= config.numerical.kkt_tolerance
    assert result.consumption_foc_max <= config.numerical.consumption_foc_tolerance


def test_kernel_household_boundaries_and_generator():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = _household_at_steady_state()
    assert result.min_consumption > 0.0
    assert result.lower_boundary_min_drift >= -1e-12
    assert result.upper_boundary_max_drift <= 1e-12
    assert result.generator_row_sum_max_abs <= config.numerical.generator_row_sum_tolerance
    assert result.generator_min_off_diagonal >= config.numerical.generator_min_off_diagonal_tolerance
    assert result.nan_inf_count == 0


def test_kernel_household_deterministic_repeat():
    first = _household_at_steady_state()
    second = _household_at_steady_state()
    assert float(np.max(np.abs(first.value - second.value))) == 0.0
    assert float(np.max(np.abs(first.consumption - second.consumption))) == 0.0
