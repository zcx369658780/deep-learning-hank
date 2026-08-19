"""DLH-3C horizon/terminal robustness and deterministic reproducibility tests.

- Horizon robustness: full-amplitude Path W / Path R on the long horizon
  ``T_long`` vs the primary horizon ``T`` agree on the common early window
  ``[0, 8]`` within the frozen aggregate tolerance.
- Reproducibility: the complete primary validation set (zero path, W and R
  full/half/quarter, both long-horizon full-amplitude runs) is executed twice
  and every repeat difference must be <= 1e-12.
"""

from pathlib import Path

import numpy as np

from deep_learning_hank.diagnostics.hank_transition import (
    reproducibility_differences,
    run_transition_validation_cached,
)
from deep_learning_hank.hank_transition_config import HankTransitionConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3c_hank_transition_validation.toml"


def _config():
    return HankTransitionConfig.from_toml(FIXTURE_PATH)


def test_horizon_terminal_robustness() -> None:
    config = _config()
    result = run_transition_validation_cached(config)
    metrics = result.horizon_robustness
    assert metrics["pass"] == 1.0
    for family in ("W", "R"):
        for name in ("A_hh", "N_hh", "C"):
            assert metrics[f"{family}_{name}_diff"] <= config.gates.horizon_aggregate_tolerance
    # Long-horizon runs must satisfy the HJB/KFE gates.
    for family in ("W", "R"):
        long_run = next(
            r for r in result.runs if r.family == family and r.horizon == config.T_long
        )
        assert long_run.hjb_gates_pass
        assert long_run.kfe_gates_pass


def test_reproducibility_within_threshold() -> None:
    config = _config()
    diffs = reproducibility_differences(config)
    threshold = config.gates.reproducibility_tolerance
    max_diff = max(diffs.values())
    assert max_diff <= threshold, (
        "BLOCKED_DLH_3C_REPRODUCIBILITY_THRESHOLD: "
        f"observed max repeat difference {max_diff} > {threshold}"
    )
