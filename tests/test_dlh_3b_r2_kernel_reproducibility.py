"""DLH-3B-R2 kernel deterministic reproducibility tests.

Issue #15 §5/§7: the kernel is deterministic (no random numbers); two
identical equilibrium solves must produce identical results (max repeat
difference 0.0, consistent with the accepted 3B/3C precedents).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.ha_kernel.equilibrium import solve_kernel_equilibrium

CONFIG_PATH = Path("configs/dlh_3b_hank_steady_state_validation.toml")


def test_kernel_reproducibility_identical_solves():
    config = HankSteadyStateConfig.from_toml(CONFIG_PATH)
    first = solve_kernel_equilibrium(config)
    second = solve_kernel_equilibrium(config)
    assert abs(first.root_r - second.root_r) <= 1e-12
    assert abs(first.root_N - second.root_N) <= 1e-12
    f1, f2 = first.final, second.final
    assert abs(f1.A_hh - f2.A_hh) <= 1e-12
    assert abs(f1.N_hh - f2.N_hh) <= 1e-12
    assert abs(f1.C - f2.C) <= 1e-12
    assert float(np.max(np.abs(f1.household.value - f2.household.value))) <= 1e-12
    assert float(np.max(np.abs(f1.distribution.mass - f2.distribution.mass))) <= 1e-12
    assert abs(f1.R_asset - f2.R_asset) <= 1e-12
