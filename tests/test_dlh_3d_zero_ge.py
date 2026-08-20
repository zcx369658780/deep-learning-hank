"""DLH-3D zero-innovation tests: accepted baseline identities, zero-innovation
invariance of the closed NK GE, and fixture labels."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_ge_transition import run_ge_validation_cached
from deep_learning_hank.hank_ge_config import HankGeConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3d_hank_monetary_ge_validation.toml"


@pytest.fixture(scope="module")
def config():
    return HankGeConfig.from_toml(FIXTURE_PATH)


@pytest.fixture(scope="module")
def result(config):
    return run_ge_validation_cached(config)


def test_baseline_identities_are_frozen(config) -> None:
    observed_3b, observed_3c = config.verify_baseline_identities()
    assert observed_3b == "82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1"
    assert observed_3c == "C7AA76DF3758F46FCBA827872FC0FD0078EDD5309CCFAD04E32C42F5CB4D39A2"


def test_fixture_labels() -> None:
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text
    assert "D2_MACHINE_DIAGNOSTIC__MINIMAL_SINGLE_REGION_HANK_DYNAMIC_VALIDATION_FIXTURE" in text


def test_zero_innovation_root(config, result) -> None:
    zero = next(r for r in result.runs if r.amplitude == 0.0 and r.horizon == config.T)
    assert zero.result.root_converged
    assert np.max(np.abs(zero.result.root_x)) <= 1e-4


def test_zero_innovation_invariance(config, result) -> None:
    metrics = result.zero_invariance
    g = config.gates
    assert metrics["w_max"] <= g.zero_w_tolerance
    assert metrics["N_max"] <= g.zero_N_tolerance
    assert metrics["pi_max"] <= g.zero_pi_tolerance
    assert metrics["r_max"] <= g.zero_r_tolerance
    assert metrics["A_hh_max"] <= g.zero_A_hh_tolerance
    assert metrics["N_hh_max"] <= g.zero_N_hh_tolerance
    assert metrics["C_max"] <= g.zero_C_tolerance
    assert metrics["pass"] == 1.0


def test_zero_innovation_hjb_kfe_gates(result) -> None:
    zero = next(r for r in result.runs if r.amplitude == 0.0)
    assert zero.hjb_gates_pass
    assert zero.kfe_gates_pass
