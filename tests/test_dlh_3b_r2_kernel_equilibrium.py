"""DLH-3B-R2 kernel equilibrium tests.

Issue #15 §5/§7: the canonical kernel equilibrium must clear both markets and
reproduce the accepted DLH-3B steady state (the kernel implements the same
economic problem; scientific meaning unchanged).
"""

from __future__ import annotations

from pathlib import Path

from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.ha_kernel.equilibrium import solve_kernel_equilibrium

CONFIG_PATH = Path("configs/dlh_3b_hank_steady_state_validation.toml")

# Frozen accepted DLH-3B steady state (Task Index / Startup Snapshot / 3B report).
ACCEPTED_R_STAR = 0.007370613883670197
ACCEPTED_N_STAR = 1.0656334480169984
ACCEPTED_A_HH_STAR = 10.000000002223675
ACCEPTED_W_STAR = 5.0 / 6.0
ACCEPTED_C_STAR = 1.065633448423122
B = 10.0


def test_kernel_equilibrium_root_converges():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = solve_kernel_equilibrium(config)
    assert result.root_converged
    assert result.final.finite


def test_kernel_equilibrium_clearing():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = solve_kernel_equilibrium(config)
    assert abs(result.final.R_asset) <= config.numerical.clearing_tolerance
    assert abs(result.final.R_labor) <= config.numerical.clearing_tolerance


def test_kernel_equilibrium_reproduces_accepted_3b():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    result = solve_kernel_equilibrium(config)
    final = result.final
    assert abs(result.root_r - ACCEPTED_R_STAR) <= 1e-6
    assert abs(result.root_N - ACCEPTED_N_STAR) <= 1e-6
    assert abs(final.A_hh - ACCEPTED_A_HH_STAR) <= 1e-6
    assert abs(final.wage - ACCEPTED_W_STAR) <= 1e-6
    assert abs(final.C - ACCEPTED_C_STAR) <= 1e-6
    assert abs(final.A_hh - B) <= 1e-6
