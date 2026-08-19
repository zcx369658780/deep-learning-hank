"""DLH-2B deterministic reproducibility test.

Runs the full single-region Tier-0 steady-state pipeline at least twice in the
same environment and reports max absolute repeat differences for K*, wage, net
capital return, output, transfer, household value, consumption policy, drift,
distribution mass, and the scalar diagnostic vector.

Target for every repeat difference: <= 1e-12.  Do not relax this threshold.
"""

from pathlib import Path

import numpy as np

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_steady_state import run_tier0_steady_state

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_2b_tier0_steady_state_validation.toml"


def _repeat_differences() -> dict[str, float]:
    config = SteadyStateConfig.from_toml(FIXTURE_PATH)
    first = run_tier0_steady_state(config)
    second = run_tier0_steady_state(config)
    a, b = first.result.final, second.result.final
    diffs = {
        "capital_star": abs(a.capital - b.capital),
        "wage": abs(a.wage - b.wage),
        "net_capital_return": abs(a.net_capital_return - b.net_capital_return),
        "output": abs(a.output - b.output),
        "transfer": abs(a.transfer - b.transfer),
        "value": float(np.max(np.abs(a.household.value - b.household.value))),
        "consumption": float(
            np.max(np.abs(a.household.consumption - b.household.consumption))
        ),
        "drift": float(np.max(np.abs(a.household.drift - b.household.drift))),
        "distribution_mass": float(
            np.max(np.abs(a.distribution.mass - b.distribution.mass))
        ),
        "scalars": float(np.max(np.abs(a.scalar_vector() - b.scalar_vector()))),
    }
    return diffs


def test_steady_state_pipeline_is_deterministic_within_threshold() -> None:
    diffs = _repeat_differences()
    threshold = 1e-12
    max_diff = max(diffs.values())
    assert max_diff <= threshold, (
        "BLOCKED_DLH_2B_REPRODUCIBILITY_THRESHOLD: "
        f"observed max repeat difference {max_diff} > {threshold}; diffs={diffs}"
    )
