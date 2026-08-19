"""DLH-3C mass / boundary tests: forward-KFE mass conservation and
non-negativity along every prescribed path, backward-HJB boundary/KKT gates,
and idiosyncratic state-marginal stationarity."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_transition import run_transition_validation_cached
from deep_learning_hank.economics.grids import stationary_state_probabilities
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.hank_transition_config import HankTransitionConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3c_hank_transition_validation.toml"


@pytest.fixture(scope="module")
def config():
    return HankTransitionConfig.from_toml(FIXTURE_PATH)


@pytest.fixture(scope="module")
def result(config):
    return run_transition_validation_cached(config)


def test_forward_kfe_mass_conservation_every_run(config, result) -> None:
    n = config.numerical
    for run in result.runs:
        assert run.kfe.mass_error_max <= n.kfe_mass_tolerance, f"{run.family}/{run.amplitude}"
        assert run.kfe.minimum_mass_min >= n.minimum_mass_threshold, f"{run.family}/{run.amplitude}"
        assert run.kfe.negative_mass_count_max == 0, f"{run.family}/{run.amplitude}"
        assert run.kfe.nan_inf_count_max == 0, f"{run.family}/{run.amplitude}"
        assert run.kfe_gates_pass


def test_backward_hjb_gates_every_run(config, result) -> None:
    n = config.numerical
    for run in result.runs:
        hjb = run.hjb
        assert hjb.converged_all, f"{run.family}/{run.amplitude}"
        assert hjb.hjb_residual_max <= n.hjb_residual_tolerance, f"{run.family}/{run.amplitude}"
        assert np.min(hjb.consumption_path) > 0.0, f"{run.family}/{run.amplitude}"
        assert np.min(hjb.drift_path[:, :, 0]) >= -1e-12, f"{run.family}/{run.amplitude}"
        assert np.max(hjb.drift_path[:, :, -1]) <= 1e-12, f"{run.family}/{run.amplitude}"
        assert hjb.labor_kkt_max <= n.kkt_tolerance, f"{run.family}/{run.amplitude}"
        assert hjb.consumption_foc_max <= n.consumption_foc_tolerance, f"{run.family}/{run.amplitude}"
        assert all(s.nan_inf_count == 0 for s in hjb.steps), f"{run.family}/{run.amplitude}"
        assert run.hjb_gates_pass


def test_state_marginals_stationary_every_run(config, result) -> None:
    hb_config = HankSteadyStateConfig.from_toml(config.baseline_config_path)
    state_generator = np.array(
        [[-hb_config.q_low_to_high, hb_config.q_low_to_high],
         [hb_config.q_high_to_low, -hb_config.q_high_to_low]],
        dtype=np.float64,
    )
    ctmc_law = stationary_state_probabilities(state_generator)
    for run in result.runs:
        assert np.max(np.abs(run.kfe.state_marginals_path - ctmc_law)) <= 1e-8, (
            f"{run.family}/{run.amplitude}"
        )


def test_mass_initial_is_steady_state(result) -> None:
    zero = next(r for r in result.runs if r.family == "zero")
    assert np.max(np.abs(zero.kfe.mass_path[0] - result.baseline.g_ss)) <= 1e-15


def test_aggregate_paths_finite(result) -> None:
    for run in result.runs:
        assert np.all(np.isfinite(run.kfe.A_hh_path))
        assert np.all(np.isfinite(run.kfe.N_hh_path))
        assert np.all(np.isfinite(run.kfe.C_path))
