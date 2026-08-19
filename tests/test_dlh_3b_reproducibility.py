"""DLH-3B deterministic reproducibility test.

Runs the complete DLH-3B steady-state pipeline at least twice in the same
environment and reports max absolute repeat differences for r*, i*, N, Y, w,
tr, Pi, C, A_hh, household value/consumption/labor/drift, distribution mass,
and the full scalar diagnostic vector.

Target for every repeat difference: <= 1e-12.  Do not relax this threshold.
"""

from pathlib import Path

import numpy as np

from deep_learning_hank.diagnostics.hank_steady_state import run_hank_steady_state
from deep_learning_hank.hank_config import HankSteadyStateConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3b_hank_steady_state_validation.toml"


def _repeat_differences() -> dict[str, float]:
    config = HankSteadyStateConfig.from_toml(FIXTURE_PATH)
    first = run_hank_steady_state(config)
    second = run_hank_steady_state(config)
    a, b = first.result.final, second.result.final
    ha, hb = a.household, b.household
    da, db = a.distribution, b.distribution
    diffs = {
        "r_star": abs(first.result.root_r - second.result.root_r),
        "i_star": abs(first.interest_rate - second.interest_rate),
        "N_star": abs(first.result.root_N - second.result.root_N),
        "Y": abs(a.output - b.output),
        "w": abs(a.wage - b.wage),
        "tr": abs(a.transfer - b.transfer),
        "Pi": abs(a.profits - b.profits),
        "C": abs(a.C - b.C),
        "A_hh": abs(a.A_hh - b.A_hh),
        "value": float(np.max(np.abs(ha.value - hb.value))),
        "consumption": float(np.max(np.abs(ha.consumption - hb.consumption))),
        "labor": float(np.max(np.abs(ha.labor - hb.labor))),
        "drift": float(np.max(np.abs(ha.drift - hb.drift))),
        "distribution_mass": float(np.max(np.abs(da.mass - db.mass))),
        "scalars": float(np.max(np.abs(first.scalar_vector() - second.scalar_vector()))),
    }
    return diffs


def test_hank_steady_state_is_deterministic_within_threshold() -> None:
    diffs = _repeat_differences()
    threshold = 1e-12
    max_diff = max(diffs.values())
    assert max_diff <= threshold, (
        "BLOCKED_DLH_3B_REPRODUCIBILITY_THRESHOLD: "
        f"observed max repeat difference {max_diff} > {threshold}; diffs={diffs}"
    )
