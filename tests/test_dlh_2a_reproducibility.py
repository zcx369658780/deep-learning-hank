"""DLH-2A deterministic reproducibility test.

Runs the fixed-price HJB+KFE pipeline at least twice in the same environment
and reports the max absolute repeat differences for value, consumption,
drift, distribution mass, and scalar diagnostics.

Target: max absolute repeat difference <= 1e-12.  If the platform linear
algebra prevents this, the observed differences must be reported (BLOCKED)
rather than silently relaxing the threshold.
"""

from pathlib import Path

import numpy as np

from deep_learning_hank.config import FixedPriceConfig
from deep_learning_hank.diagnostics.tier0_fixed_price import run_fixed_price_validation

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_2a_fixed_price_validation.toml"


def _repeat_differences() -> dict[str, float]:
    config = FixedPriceConfig.from_toml(FIXTURE_PATH)
    first = run_fixed_price_validation(config)
    second = run_fixed_price_validation(config)
    diffs = {
        "value": float(np.max(np.abs(first.household.value - second.household.value))),
        "consumption": float(
            np.max(np.abs(first.household.consumption - second.household.consumption))
        ),
        "drift": float(np.max(np.abs(first.household.drift - second.household.drift))),
        "distribution_mass": float(
            np.max(np.abs(first.distribution.mass - second.distribution.mass))
        ),
        "scalars": float(np.max(np.abs(first.scalar_vector() - second.scalar_vector()))),
    }
    return diffs


def test_fixed_price_pipeline_is_deterministic_within_threshold() -> None:
    diffs = _repeat_differences()
    threshold = 1e-12
    max_diff = max(diffs.values())
    # The reproducibility threshold is an acceptance gate: do not relax it
    # here. If it fails, report BLOCKED_DLH_2A_REPRODUCIBILITY_THRESHOLD with
    # the exact observed differences for reviewer decision.
    assert max_diff <= threshold, (
        "BLOCKED_DLH_2A_REPRODUCIBILITY_THRESHOLD: "
        f"observed max repeat difference {max_diff} > {threshold}; diffs={diffs}"
    )
