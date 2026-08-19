"""DLH-2C state-label permutation invariance tests (B40_50 vs P40_50)."""

import numpy as np

from deep_learning_hank.diagnostics.tier0_robustness import (
    load_variants,
    permutation_invariance_metrics,
)


def test_state_permutation_invariance() -> None:
    variants = load_variants()
    metrics = permutation_invariance_metrics(variants)
    max_diffs = metrics["max_abs_diffs"]
    assert metrics["gate"], (
        "BLOCKED_DLH_2C_STATE_PERMUTATION_INVARIANCE: "
        f"max abs differences = {max_diffs} (must be <= 1e-10)"
    )
    for name, diff in max_diffs.items():
        assert diff <= 1e-10, f"{name} diff {diff} > 1e-10"
