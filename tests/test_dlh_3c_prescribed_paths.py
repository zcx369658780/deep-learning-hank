"""DLH-3C prescribed-path tests: Path W / Path R non-structural input
construction, nontrivial response, amplitude full/half/quarter monotonicity,
quarter-amplitude cap, and half-amplitude local-scaling diagnostics."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_transition import (
    build_inputs_path,
    bump_function,
    run_transition_validation_cached,
)
from deep_learning_hank.hank_transition_config import HankTransitionConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3c_hank_transition_validation.toml"


@pytest.fixture(scope="module")
def config():
    return HankTransitionConfig.from_toml(FIXTURE_PATH)


@pytest.fixture(scope="module")
def result(config):
    return run_transition_validation_cached(config)


def test_bump_function_support_and_smoothness(config) -> None:
    t = np.linspace(-1.0, config.T + 1.0, 1001)
    h = bump_function(t, config.bump_length_L)
    assert h[0] == pytest.approx(0.0, abs=1e-15)
    # Exactly zero outside the support, including the terminal region.
    assert np.all(h[t >= config.bump_length_L] == 0.0)
    assert np.all(h[t <= 0.0] == 0.0)
    assert np.max(h) == pytest.approx(1.0, abs=1e-12)


def test_path_W_inputs_are_wage_only(config, result) -> None:
    baseline = result.baseline
    w_full = next(r for r in result.runs if r.family == "W" and r.amplitude == 1.0)
    grid = w_full.time_grid
    h = bump_function(grid, config.bump_length_L)
    for k, inputs in enumerate(w_full.inputs):
        assert inputs.wage == pytest.approx(
            baseline.wage_star * (1.0 + config.eta_w * h[k]), abs=1e-15
        )
        assert inputs.real_return == pytest.approx(baseline.r_star, abs=1e-15)
        assert inputs.transfer == pytest.approx(baseline.transfer_star, abs=1e-15)
        assert inputs.profits == pytest.approx(baseline.profits_star, abs=1e-15)


def test_path_R_inputs_are_return_only(config, result) -> None:
    baseline = result.baseline
    r_full = next(r for r in result.runs if r.family == "R" and r.amplitude == 1.0)
    grid = r_full.time_grid
    h = bump_function(grid, config.bump_length_L)
    for k, inputs in enumerate(r_full.inputs):
        assert inputs.real_return == pytest.approx(
            baseline.r_star + config.eta_r * h[k], abs=1e-15
        )
        assert inputs.wage == pytest.approx(baseline.wage_star, abs=1e-15)
        assert inputs.transfer == pytest.approx(baseline.transfer_star, abs=1e-15)
        assert inputs.profits == pytest.approx(baseline.profits_star, abs=1e-15)


def test_nontrivial_response(config, result) -> None:
    for metrics in result.amplitude:
        assert metrics.M_full > config.gates.nontrivial_response_threshold
        assert metrics.nontrivial_ok


def test_amplitude_monotone_and_quarter_cap(config, result) -> None:
    for metrics in result.amplitude:
        assert metrics.M_full > metrics.M_half > metrics.M_quarter > 0.0
        assert metrics.M_quarter <= config.gates.quarter_amplitude_ratio_cap * metrics.M_full
        assert metrics.monotone_ok
        assert metrics.quarter_cap_ok


def test_half_amplitude_local_scaling(config, result) -> None:
    for metrics in result.amplitude:
        assert metrics.E_half <= config.gates.half_linearity_metric_cap
        assert metrics.half_linearity_ok


def test_amplitude_gates_pass(result) -> None:
    assert result.amplitude[0].pass_
    assert result.amplitude[1].pass_


def test_amplitude_sequence_is_exactly_frozen(config, result) -> None:
    for family in ("W", "R"):
        amps = sorted(r.amplitude for r in result.runs if r.family == family and r.horizon == config.T)
        assert amps == [0.25, 0.5, 1.0]
