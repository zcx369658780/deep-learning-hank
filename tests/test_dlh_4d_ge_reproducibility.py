"""DLH-4D GE reproducibility tests (Issue #20).

Verifies that the GE residual evaluation and the cold initialization are
exactly deterministic at a fixed candidate point (repeat difference 0.0 in the
same environment).  The full-solve deterministic repeat (Issue #20 gate 10) is
executed and evidenced in the DLH-4D execution run (multi-hour; report + CSV).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from deep_learning_hank.ge import GeConfig, evaluate_ge

CONFIG_PATH = Path("configs/dlh_4d_two_asset_single_region_ge_validation.toml")


def _config():
    return GeConfig.from_toml(CONFIG_PATH)


def test_ge_evaluation_deterministic_at_fixed_candidate():
    cfg = _config()
    first = evaluate_ge(cfg, 0.02, 0.015, 1.0)
    second = evaluate_ge(cfg, 0.02, 0.015, 1.0)
    assert first.finite and second.finite
    assert first.R1 == second.R1
    assert first.R2 == second.R2
    assert first.R3 == second.R3
    assert first.A_hh == second.A_hh
    assert first.B_hh == second.B_hh
    assert first.L_hh == second.L_hh
    assert first.C_hh == second.C_hh
    assert first.AC == second.AC
    assert first.W_taper == second.W_taper
    assert first.hjb_iterations == second.hjb_iterations
    assert first.hjb_statistic == second.hjb_statistic
