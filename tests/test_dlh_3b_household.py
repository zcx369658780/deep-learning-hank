"""DLH-3B household tests: zero-drift policy, labor FOC/KKT, household HJB
numerical gates, stationary KFE gates at a fixed candidate, fail-closed
feasibility, and scope boundaries."""

from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.economics.grids import (
    build_asset_grid,
    build_idiosyncratic_generator,
    stationary_state_probabilities,
)
from deep_learning_hank.economics.hank_firm import hank_production
from deep_learning_hank.economics.hank_fiscal import hank_fiscal
from deep_learning_hank.hank_config import HankSteadyStateConfig
from deep_learning_hank.solvers.distribution_kfe import solve_stationary_distribution
from deep_learning_hank.solvers.hank_household_steady_state import (
    HankHouseholdFeasibilityError,
    labor_disutility,
    labor_policy,
    marginal_labor_disutility,
    solve_hank_household,
    zero_drift_policy,
)

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "configs" / "dlh_3b_hank_steady_state_validation.toml"

# Fixed synthetic candidate (test plumbing, not a frozen economic value):
# r = 0.005, N = 1.0 with w = Z/mu, tr and Pi from the frozen fiscal/firm blocks.
R_CANDIDATE = 0.005
N_CANDIDATE = 1.0


@pytest.fixture(scope="module")
def config():
    return HankSteadyStateConfig.from_toml(FIXTURE_PATH)


@pytest.fixture(scope="module")
def candidate_household(config):
    production = hank_production(
        productivity=config.productivity, labor=N_CANDIDATE, epsilon=config.epsilon
    )
    fiscal = hank_fiscal(
        wage=production.wage,
        labor=N_CANDIDATE,
        real_return=R_CANDIDATE,
        bond_supply=config.bond_supply,
        tau_l=config.tau_l,
        public_outlay=config.public_outlay,
    )
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    household = solve_hank_household(
        asset_grid=asset_grid,
        efficiency_states=efficiency_states,
        state_generator=state_generator,
        wage=production.wage,
        real_return=R_CANDIDATE,
        transfer=fiscal.transfer,
        profits=production.profits,
        tau_l=config.tau_l,
        rho_hh=config.rho_hh,
        gamma=config.gamma,
        frisch=config.frisch,
        chi=config.chi,
        n_max=config.n_max,
        tolerance=config.numerical.hjb_tolerance,
        max_iterations=config.numerical.hjb_max_iterations,
        pseudo_time_step=config.numerical.hjb_pseudo_time_step,
        consumption_floor=config.numerical.consumption_floor,
    )
    return household


def test_zero_drift_policy_foc(config) -> None:
    q = (1.0 - config.tau_l) * (config.productivity / (config.epsilon / (config.epsilon - 1.0)))
    b = np.array([0.1, 0.5, 1.0, 2.0], dtype=np.float64)
    qq = q * np.array([0.5, 1.5, 1.0, 1.0])
    c0, n0, feasible = zero_drift_policy(
        qq,
        b,
        gamma=config.gamma,
        frisch=config.frisch,
        chi=config.chi,
        n_max=config.n_max,
        consumption_floor=config.numerical.consumption_floor,
    )
    assert np.all(feasible)
    assert np.all(c0 > config.numerical.consumption_floor)
    assert np.all(n0 <= config.n_max + 1e-12)
    # Interior nodes satisfy the scalar FOC chi*n0^(1/frisch) = q*c0^(-gamma).
    interior = (n0 < config.n_max - 1e-9) & (n0 > 1e-9)
    lhs = config.chi * n0[interior] ** (1.0 / config.frisch)
    rhs = qq[interior] * c0[interior] ** (-config.gamma)
    assert np.max(np.abs(lhs - rhs)) <= 1e-6


def test_labor_policy_interior_and_kkt(config) -> None:
    q = 0.5
    marginal = 2.0
    n = labor_policy(
        np.array([q]), np.array([marginal]), chi=config.chi, frisch=config.frisch, n_max=config.n_max
    )[0]
    # Interior FOC: v'(n) = q*V_a.
    assert n < config.n_max - 1e-9
    assert abs(marginal_labor_disutility(np.array([n]), chi=config.chi, frisch=config.frisch)[0] - q * marginal) <= 1e-12
    # Upper-cap KKT: with q*V_a above v'(n_max), the policy is capped at n_max
    # and the KKT violation max(-gap, 0) is exactly 0.
    q_high, marginal_high = 1.0, 10.0
    n_capped = labor_policy(
        np.array([q_high]), np.array([marginal_high]), chi=config.chi, frisch=config.frisch, n_max=config.n_max
    )[0]
    assert n_capped == config.n_max
    gap = q_high * marginal_high - marginal_labor_disutility(
        np.array([config.n_max]), chi=config.chi, frisch=config.frisch
    )[0]
    assert gap > 0.0
    assert max(-gap, 0.0) == 0.0


def test_household_solver_numerical_gates(config, candidate_household) -> None:
    household = candidate_household
    assert household.converged
    assert household.true_residual <= 1e-7
    assert household.min_consumption > 0.0
    assert household.lower_boundary_min_drift >= -1e-12
    assert household.upper_boundary_max_drift <= 1e-12
    assert household.generator_row_sum_max_abs <= 1e-12
    assert household.generator_min_off_diagonal >= -1e-14
    assert household.nan_inf_count == 0
    assert household.labor_kkt_max <= 1e-7
    assert household.consumption_foc_max <= 1e-7
    assert np.all(np.isfinite(household.value))
    assert np.all(np.isfinite(household.labor))


def test_kfe_gates_at_candidate(config, candidate_household) -> None:
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    distribution = solve_stationary_distribution(
        generator=candidate_household.generator,
        asset_grid=asset_grid,
        consumption=candidate_household.consumption,
        stationarity_tolerance=config.numerical.kfe_stationarity_tolerance,
        mass_tolerance=config.numerical.kfe_mass_tolerance,
        negative_mass_threshold=config.numerical.negative_mass_threshold,
    )
    assert distribution.mass_error <= 1e-10
    assert distribution.stationarity_residual <= 1e-8
    assert distribution.minimum_mass >= -1e-12
    assert distribution.negative_mass_count == 0
    assert distribution.nan_inf_count == 0
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    ctmc_law = stationary_state_probabilities(state_generator)
    assert np.max(np.abs(distribution.state_marginals - ctmc_law)) <= 1e-8


def test_household_feasibility_fail_closed(config) -> None:
    asset_grid = build_asset_grid(config.a_min, config.a_max, config.asset_grid_count)
    efficiency_states = np.asarray(config.idiosyncratic_states, dtype=np.float64)
    state_generator = build_idiosyncratic_generator(config.q_low_to_high, config.q_high_to_low)
    with pytest.raises(HankHouseholdFeasibilityError):
        solve_hank_household(
            asset_grid=asset_grid,
            efficiency_states=efficiency_states,
            state_generator=state_generator,
            wage=config.productivity / (config.epsilon / (config.epsilon - 1.0)),
            real_return=-50.0,
            transfer=0.0,
            profits=0.0,
            tau_l=config.tau_l,
            rho_hh=config.rho_hh,
            gamma=config.gamma,
            frisch=config.frisch,
            chi=config.chi,
            n_max=config.n_max,
            tolerance=config.numerical.hjb_tolerance,
            max_iterations=config.numerical.hjb_max_iterations,
            pseudo_time_step=config.numerical.hjb_pseudo_time_step,
            consumption_floor=config.numerical.consumption_floor,
        )


def test_no_time_dependent_or_forbidden_machinery() -> None:
    import deep_learning_hank.solvers.hank_household_steady_state as hh

    source = Path(hh.__file__).read_text(encoding="utf-8")
    import_lines = [
        line.strip()
        for line in source.splitlines()
        if line.strip().startswith(("from ", "import "))
    ]
    forbidden_imports = (
        "transition",
        "shocks",
        "aggregate_block",
        "regional_structure",
        "spatial_links",
        "neural",
        "rl",
    )
    for line in import_lines:
        assert not any(token in line for token in forbidden_imports), (
            f"forbidden import in DLH-3B household module: {line}"
        )
    for token in ("W^L", "W^K", "W^G", "Taylor", "NKPC", "neural", "rl", "IRF"):
        assert token not in source, f"forbidden token in DLH-3B household module: {token}"
