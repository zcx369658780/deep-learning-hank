"""DLH-3C zero-path invariance tests: baseline identity, prescribed-path
zero-amplitude invariance of the backward HJB + forward KFE engine, and the
zero-run HJB/KFE gates."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_transition import (
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


def test_baseline_identity_is_frozen(config) -> None:
    # Issue #12 §4: fresh DLH-3B baseline config hash must equal the frozen value.
    observed = config.verify_baseline_identity()
    assert observed == "82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1"
    assert result is not None  # no-op to keep fixture reference


def test_zero_path_is_running(config, result) -> None:
    zero = next(r for r in result.runs if r.family == "zero")
    assert zero.amplitude == 0.0
    assert zero.horizon == config.T
    assert zero.hjb.converged_all
    assert zero.hjb_gates_pass
    assert zero.kfe_gates_pass


def test_zero_path_invariance_value(config, result) -> None:
    metrics = result.zero_invariance
    assert metrics["V_max"] <= config.gates.zero_path_V_tolerance
    assert metrics["c_max"] <= config.gates.zero_path_policy_tolerance
    assert metrics["n_max"] <= config.gates.zero_path_policy_tolerance
    assert metrics["drift_max"] <= config.gates.zero_path_policy_tolerance
    assert metrics["g_max"] <= config.gates.zero_path_mass_tolerance
    assert metrics["A_hh_max"] <= config.gates.zero_path_aggregate_tolerance
    assert metrics["N_hh_max"] <= config.gates.zero_path_aggregate_tolerance
    assert metrics["C_max"] <= config.gates.zero_path_aggregate_tolerance
    assert metrics["pass"] == 1.0


def test_zero_path_prescribed_inputs_are_baseline(config, result) -> None:
    zero = next(r for r in result.runs if r.family == "zero")
    baseline = result.baseline
    for inputs in zero.inputs:
        assert inputs.wage == pytest.approx(baseline.wage_star, abs=1e-15)
        assert inputs.real_return == pytest.approx(baseline.r_star, abs=1e-15)
        assert inputs.transfer == pytest.approx(baseline.transfer_star, abs=1e-15)
        assert inputs.profits == pytest.approx(baseline.profits_star, abs=1e-15)


def test_fixture_labels() -> None:
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text
    assert "EXOGENOUS_NUMERICAL_RESPONSE_PATH_NOT_STRUCTURAL_SHOCK" in text
    assert "D2_MACHINE_DIAGNOSTIC__HANK_TIME_DEPENDENT_HOUSEHOLD_KFE_ONLY" in text
