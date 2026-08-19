"""DLH-2B equilibrium tests: effective labor, bracket/root, capital clearing,
root-trace finiteness, evaluation counts, HJB/KFE-at-equilibrium gates, scope
boundaries, fixture labeling."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.config import SteadyStateConfig
from deep_learning_hank.diagnostics.tier0_steady_state import run_tier0_steady_state
from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
)
from deep_learning_hank.solvers.steady_state import (
    effective_labor_from_ctmc,
    evaluate_capital,
)

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_2b_tier0_steady_state_validation.toml"


@pytest.fixture(scope="module")
def diagnostics():
    config = SteadyStateConfig.from_toml(FIXTURE_PATH)
    return run_tier0_steady_state(config)


def test_fixture_is_not_calibration_label() -> None:
    text = FIXTURE_PATH.read_text(encoding="utf-8")
    assert "VALIDATION_FIXTURE_NOT_CALIBRATION" in text
    assert "calibration" in text.lower()


def test_effective_labor_from_ctmc_stationary_law() -> None:
    config = SteadyStateConfig.from_toml(FIXTURE_PATH)
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    l_bar = effective_labor_from_ctmc(state_generator, efficiency_states)
    # stationary law pi = (0.5, 0.5); L_bar = dot(pi, z) = 1.0 (computed, not hard-coded)
    assert np.isfinite(l_bar) and l_bar > 0.0
    assert l_bar == pytest.approx(1.0, abs=1e-12)


def test_primary_bracket_sign_contract(diagnostics) -> None:
    config = SteadyStateConfig.from_toml(FIXTURE_PATH)
    lower, upper = config.capital_bracket
    low = evaluate_capital(config, lower)
    high = evaluate_capital(config, upper)
    assert np.isfinite(low.capital_residual)
    assert np.isfinite(high.capital_residual)
    # Primary bracket must sign-change (or an endpoint is exactly zero).
    assert low.capital_residual * high.capital_residual <= 0.0


def test_capital_clearing_root(diagnostics) -> None:
    assert diagnostics.result.root_converged
    final = diagnostics.result.final
    assert final.capital > 0.0
    bracket_lo, bracket_hi = diagnostics.result.bracket_used
    assert bracket_lo <= final.capital <= bracket_hi
    assert abs(final.capital_residual) <= 1e-7
    assert np.isfinite(final.capital_residual)
    assert diagnostics.capital_clearing_ok


def test_root_trace_finiteness_machine_gate(diagnostics) -> None:
    # Issue #6: "all root evaluations finite" — every trace entry must be finite.
    assert diagnostics.root_trace_finite_ok
    for capital, residual in diagnostics.result.root_trace:
        assert np.isfinite(capital)
        assert np.isfinite(residual)
    assert diagnostics.root_gate_ok


def test_root_evaluation_count_semantics(diagnostics) -> None:
    # Precise R1 semantics: root_trace entries + one post-root verification.
    result = diagnostics.result
    assert result.root_trace_evaluations == len(result.root_trace)
    assert result.post_root_validation_evaluations == 1
    assert result.total_capital_evaluations == result.root_trace_evaluations + 1
    # Accepted fixture: trace = 2 endpoint pre-checks + 9 brentq callbacks = 11;
    # total capital evaluations = 12.
    assert result.root_trace_evaluations == 11
    assert result.total_capital_evaluations == 12


def test_equilibrium_hjb_gates(diagnostics) -> None:
    final = diagnostics.result.final
    assert final.hjb_converged
    assert final.hjb_true_residual <= 1e-7
    assert final.hjb_min_consumption > 0.0
    assert final.hjb_lower_boundary_min_drift >= -1e-12
    assert final.hjb_upper_boundary_max_drift <= 1e-12
    assert final.hjb_generator_row_sum_max_abs <= 1e-12
    assert final.hjb_generator_min_off_diagonal >= -1e-14
    assert final.hjb_nan_inf_count == 0
    assert diagnostics.hjb_ok


def test_equilibrium_kfe_gates(diagnostics) -> None:
    final = diagnostics.result.final
    assert final.kfe_mass_error <= 1e-10
    assert final.kfe_stationarity_residual <= 1e-8
    assert final.kfe_minimum_mass >= -1e-12
    assert final.kfe_negative_mass_count == 0
    assert final.kfe_nan_inf_count == 0
    assert diagnostics.kfe_ok


def test_effective_labor_consistency_at_equilibrium(diagnostics) -> None:
    assert abs(diagnostics.effective_labor_error) <= 1e-8
    assert diagnostics.effective_labor_ok


def test_no_regional_w_soe_nominal_objects() -> None:
    import deep_learning_hank.solvers.steady_state as ss

    source = Path(ss.__file__).read_text(encoding="utf-8")
    import_lines = [
        line.strip()
        for line in source.splitlines()
        if line.strip().startswith(("from ", "import "))
    ]
    # No forbidden machinery may be imported by the Tier-0 steady-state solver.
    forbidden_imports = (
        "spatial_links",
        "regional_structure",
        "aggregate_block",
        "shocks",
        "transition",
        "chapter5_model",
        "neural",
        "rl",
        "nominal",
    )
    for line in import_lines:
        assert not any(token in line for token in forbidden_imports), (
            f"forbidden import in Tier-0 steady-state solver: {line}"
        )
    # No forbidden mechanism identifiers as code tokens.
    for token in ("W^L", "W^K", "alpha_g", "state_owned", "RegionalAccounts", "NKPC", "Taylor"):
        assert token not in source, f"forbidden token in Tier-0 steady-state solver: {token}"
