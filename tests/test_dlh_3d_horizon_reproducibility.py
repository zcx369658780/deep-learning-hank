"""DLH-3D horizon/terminal robustness and deterministic reproducibility tests.

- Horizon robustness: full-amplitude innovation on the long horizon
  ``T_long`` vs the primary horizon ``T`` agree on the common early window
  ``[0, 8]`` within the frozen tolerance for pi, r, w, N, A_hh, C.
- Reproducibility: the complete validation set (zero; full/half/quarter
  primary; full long-horizon) is executed twice and every repeat difference
  must be <= 1e-12.
"""

from pathlib import Path

from deep_learning_hank.diagnostics.hank_ge_transition import (
    reproducibility_differences,
    run_ge_validation_cached,
)
from deep_learning_hank.hank_ge_config import HankGeConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3d_hank_monetary_ge_validation.toml"


def _config() -> HankGeConfig:
    return HankGeConfig.from_toml(FIXTURE_PATH)


def test_horizon_terminal_robustness() -> None:
    config = _config()
    result = run_ge_validation_cached(config)
    metrics = result.horizon_robustness
    assert metrics["pass"] == 1.0
    for name in ("pi", "r", "w", "N", "A_hh", "C"):
        assert metrics[f"{name}_diff"] <= config.gates.horizon_tolerance
    long_run = next(r for r in result.runs if r.horizon == config.T_long)
    assert long_run.hjb_gates_pass
    assert long_run.kfe_gates_pass
    assert long_run.result.root_converged


def test_reproducibility_within_threshold() -> None:
    config = _config()
    diffs = reproducibility_differences(config)
    threshold = config.gates.reproducibility_tolerance
    max_diff = max(diffs.values())
    assert max_diff <= threshold, (
        "BLOCKED_DLH_3D_REPRODUCIBILITY_THRESHOLD: "
        f"observed max repeat difference {max_diff} > {threshold}"
    )
