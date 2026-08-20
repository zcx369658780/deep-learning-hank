"""DLH-3D monetary-innovation tests: innovation path construction, full GE
root/market-clearing gates, aggregate-equation residuals, nontrivial response,
amplitude-to-zero / local scaling, and terminal-boundary reporting."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_ge_transition import run_ge_validation_cached
from deep_learning_hank.hank_ge_config import HankGeConfig
from deep_learning_hank.solvers.hank_ge_transition import build_innovation_path

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3d_hank_monetary_ge_validation.toml"


@pytest.fixture(scope="module")
def config():
    return HankGeConfig.from_toml(FIXTURE_PATH)


@pytest.fixture(scope="module")
def result(config):
    return run_ge_validation_cached(config)


def test_innovation_path_construction(config) -> None:
    grid = config.dt * np.arange(int(round(config.T / config.dt)) + 1)
    h = np.where(
        (grid >= 0.0) & (grid <= config.L_i), np.sin(np.pi * grid / config.L_i) ** 2, 0.0
    )
    eps = build_innovation_path(config, 1.0, config.T)
    assert eps == pytest.approx(config.eta_i * h, abs=1e-15)
    assert eps[0] == pytest.approx(0.0, abs=1e-15)
    assert np.all(eps[grid >= config.L_i] == 0.0)
    assert np.max(eps) == pytest.approx(config.eta_i, abs=1e-12)


def test_full_innovation_root_and_clearing(config, result) -> None:
    full = next(r for r in result.runs if r.amplitude == 1.0 and r.horizon == config.T)
    g = config.gates
    assert full.result.root_converged
    assert full.result.root_residual_inf_norm <= config.root_tolerance_inf_norm
    k = full.result.K
    assert np.max(np.abs(full.result.final.R_asset[:k])) <= g.clearing_asset_tolerance
    assert np.max(np.abs(full.result.final.R_labor[:k])) <= g.clearing_labor_tolerance
    assert full.result.root_nfev > 0
    assert full.hjb_gates_pass
    assert full.kfe_gates_pass
    assert result.full_gates["pass"] == 1.0


def test_terminal_boundary_is_reported_not_rooted(config, result) -> None:
    full = next(r for r in result.runs if r.amplitude == 1.0 and r.horizon == config.T)
    k = full.result.K
    # Root unknown vector covers k = 0..K-1 only (2K unknowns).
    assert full.result.root_x.size == 2 * k
    assert full.result.final.aggregates.w[k] == pytest.approx(result.baseline.wage_star, abs=1e-12)
    assert full.result.final.aggregates.N[k] == pytest.approx(result.baseline.N_star, abs=1e-12)
    assert full.result.final.aggregates.pi[k] == pytest.approx(0.0, abs=1e-12)
    # Terminal approximations MUST be reported (finite values, not omitted).
    assert np.isfinite(full.terminal_A_hh_minus_B)
    assert np.isfinite(full.terminal_N_hh_minus_N_star)
    assert np.isfinite(full.terminal_R_goods)


def test_full_amplitude_nontrivial_response(result) -> None:
    assert result.full_gates["nontrivial_max"] > 1e-8
    assert result.full_gates["nontrivial_ok"] == 1.0


def test_amplitude_to_zero(config, result) -> None:
    amp = result.amplitude
    assert amp["M_full"] > amp["M_half"] > amp["M_quarter"] > 0.0
    assert amp["M_quarter"] <= config.gates.quarter_amplitude_ratio_cap * amp["M_full"]
    assert amp["E_half"] <= config.gates.half_linearity_metric_cap
    assert amp["pass"] == 1.0


def test_all_primary_gates_pass(result) -> None:
    assert result.all_gates_pass
