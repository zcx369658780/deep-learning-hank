"""DLH-3B equilibrium tests: frozen fixture labels/values, nested roots and
bracket evidence, clearing, nominal consistency, positivity, gross upper-bound
truncation sanity, and scope boundaries."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.diagnostics.hank_steady_state import run_hank_steady_state_cached
from deep_learning_hank.hank_config import HankSteadyStateConfig

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3b_hank_steady_state_validation.toml"


@pytest.fixture(scope="module")
def diagnostics():
    config = HankSteadyStateConfig.from_toml(FIXTURE_PATH)
    return run_hank_steady_state_cached(config)


def test_fixture_is_not_calibration_label() -> None:
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text
    assert "HANK_STEADY_STATE_STRUCTURAL_ONLY" in text
    assert "STARTING_DLH3B_DEVELOPMENT_DOMAIN_NOT_HANK_DOMAIN_ADEQUACY" in text


def test_frozen_fixture_values() -> None:
    config = HankSteadyStateConfig.from_toml(FIXTURE_PATH)
    assert config.frequency == "annual"
    assert config.asset_grid_count == 401
    assert config.a_min == 0.0
    assert config.a_max == 100.0
    assert config.idiosyncratic_states == (0.5, 1.5)
    assert config.q_low_to_high == 0.25 and config.q_high_to_low == 0.25
    assert config.rho_hh == 0.01 and config.gamma == 2.0 and config.tau_l == 0.15
    assert config.frisch == 1.0 and config.chi == 0.70 and config.n_max == 5.0
    assert config.productivity == 1.0 and config.epsilon == 6.0 and config.phi_p == 100.0
    assert config.phi_pi == 1.5 and config.pi_bar == 0.0 and config.epsilon_i == 0.0
    assert config.bond_supply == 10.0 and config.public_outlay == 0.0
    assert config.labor_bracket == (0.20, 2.00)
    assert config.labor_scan_bounds == (0.05, 4.00) and config.labor_scan_points == 80
    assert config.asset_bracket == (-0.0200, 0.0095)
    assert config.asset_scan_bounds == (-0.0300, 0.0099) and config.asset_scan_points == 80


def test_root_converged_within_bracket(diagnostics) -> None:
    result = diagnostics.result
    assert result.root_converged
    bracket_lo, bracket_hi = result.outer_bracket_used
    assert bracket_lo <= result.root_r <= bracket_hi
    assert result.outer_evaluations > 0
    assert result.inner_evaluations > 0
    assert len(result.root_trace) == result.outer_evaluations + result.inner_evaluations + 1
    # All trace rows must be recorded (finite or not) and every finite row finite.
    for row in result.root_trace:
        assert row.stage in {
            "outer_primary_lower", "outer_primary_upper", "outer_scan", "outer_brentq",
            "inner_primary_lower", "inner_primary_upper", "inner_scan", "inner_brentq", "final",
        }
        if row.finite:
            assert np.isfinite(row.R_asset) and np.isfinite(row.R_labor)
    assert diagnostics.root_ok


def test_clearing_residuals(diagnostics) -> None:
    final = diagnostics.result.final
    assert abs(final.R_asset) <= 1e-7
    assert abs(final.R_labor) <= 1e-7
    assert diagnostics.clearing_ok


def test_nominal_consistency(diagnostics) -> None:
    final = diagnostics.result.final
    result = diagnostics.result
    config = HankSteadyStateConfig.from_toml(FIXTURE_PATH)
    assert abs(diagnostics.R_nkpc) <= 1e-12
    assert abs(diagnostics.R_fisher) <= 1e-12
    assert abs(diagnostics.R_taylor) <= 1e-12
    assert final.marginal_cost == pytest.approx(1.0 / final.markup, abs=1e-12)
    assert final.markup == pytest.approx(1.2, abs=1e-12)
    # Fisher: i = r + pi with pi = pi_bar = 0; Taylor: r_bar = r.
    assert diagnostics.interest_rate == pytest.approx(result.root_r + config.pi_bar, abs=1e-12)
    assert diagnostics.nominal_ok


def test_positivity_and_finiteness(diagnostics) -> None:
    final = diagnostics.result.final
    result = diagnostics.result
    assert final.output > 0.0
    assert result.root_N > 0.0
    assert final.C > 0.0
    assert final.wage > 0.0
    assert final.A_hh > 0.0
    assert np.isfinite(result.root_r)
    assert np.isfinite(final.transfer)
    assert np.isfinite(final.profits)
    assert np.isfinite(diagnostics.interest_rate)
    assert diagnostics.positivity_ok


def test_gross_upper_bound_truncation_sanity(diagnostics) -> None:
    # Not a HANK domain-adequacy proof; gross safety gate only.
    assert diagnostics.upper_boundary_mass <= 1e-3
    assert np.isfinite(diagnostics.top5_mass)
    assert np.isfinite(diagnostics.lower_boundary_mass)
    assert 0.0 <= diagnostics.A_hh_over_a_max <= 1.0
    assert diagnostics.truncation_ok


def test_kfe_state_marginals_at_equilibrium(diagnostics) -> None:
    assert diagnostics.state_marginal_error <= 1e-8


def test_all_gates_pass(diagnostics) -> None:
    assert diagnostics.all_gates_pass


def test_no_forbidden_scope_machinery() -> None:
    import deep_learning_hank.solvers.hank_steady_state as ss

    source = Path(ss.__file__).read_text(encoding="utf-8")
    for token in ("W^L", "W^K", "W^G", "transition", "shock", "neural", "rl", "IRF"):
        assert token not in source, f"forbidden token in DLH-3B steady-state solver: {token}"
