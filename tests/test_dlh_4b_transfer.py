"""DLH-4B transfer tests: local-policy, sparse operator, KFE, aggregates,
end-to-end steady state, and deterministic repeat.

Issue #18 Phase D tests 3-7 (with the accepted source-repository fixtures):

3. local-policy and boundary behavior smoke tests;
4. sparse operator construction smoke test;
5. stationary KFE transfer test;
6. household aggregate transfer test;
7. deterministic repeat test.

Plus an end-to-end steady-state smoke that verifies the imported oracle
converges on the canonical validation fixture with a unique stationary
distribution and separate asset aggregates.  The fixture mirrors the accepted
MATLAB reference grid/parameters (``VALIDATION_FIXTURE_NOT_CALIBRATION``);
expected values come from the accepted source-repository contracts, not from a
new calibration.
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.optimize import brentq

from deep_learning_hank.two_asset import (
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    aggregate_stationary_household,
    assemble_source_axis,
    flow_utility,
    matlab_contaminated_row_index,
    matlab_faithful_illiquid_return,
    select_matlab_faithful_local_policy,
    solve_household_steady_state,
    solve_matlab_faithful_stationary_kfe,
)


# ---------------------------------------------------------------------------
# Canonical validation fixture (mirrors the accepted MATLAB reference grid and
# the source-repository EconomicParams conventions; VALIDATION_FIXTURE_NOT_CALIBRATION).
# ---------------------------------------------------------------------------
def build_fixture():
    params = EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)
    inputs = HouseholdInputs(
        r_a=0.03, r_b=0.015, tau=0.15, wages=np.array([1.0]),
        migration_costs=np.array([0.0]), labor_weights=np.array([1.0]),
    )
    b = np.linspace(-2.0, 5.0, 20)
    a = np.linspace(0.0, 10.0, 20)
    z = np.asarray([0.8, 1.3])
    switch = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    grid = MatlabFaithfulHJBGrid(b, a, z, switch)
    shape = (20, 20, 2)
    labor0 = np.empty(shape)
    initial = np.empty(shape)
    gap = 0.01
    for nz in range(2):
        for j in range(20):
            for i in range(20):
                rb = inputs.r_b + (gap if b[i] < 0 else 0.0)
                base = rb * b[i]
                net = (1.0 - inputs.tau) * inputs.wages[0] * z[nz]

                def f(l):
                    return l ** params.phi - net * (net * l + base) ** (-params.gamma_c)

                labor0[i, j, nz] = brentq(f, 1e-8, 5.0)
                ra = float(matlab_faithful_illiquid_return(a[j], a[-1], inputs.r_a))
                c_full = net * labor0[i, j, nz] + base + ra * a[j]
                initial[i, j, nz] = flow_utility(c_full, np.array([labor0[i, j, nz]]), inputs, params) / params.rho
    numerics = MatlabFaithfulHJBNumerics(
        delta=1000.0, convergence_tolerance=1e-7, max_iterations=1000, drift_tolerance=1e-12
    )
    return grid, params, inputs, numerics, initial, labor0, 0.0, gap


# ---------------------------------------------------------------------------
# 3. local-policy and boundary behavior smoke tests
# ---------------------------------------------------------------------------
def test_local_policy_liquid_branch_and_boundaries():
    grid, params, inputs, _, _, _, transfer_income, gap = build_fixture()
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    a_mid = float(grid.a[10])
    b_mid = float(grid.b[10])
    p = select_matlab_faithful_local_policy(
        a=a_mid, b=b_mid, z=0.8,
        v_a_forward=1.2, v_a_backward=1.1, v_b_forward=1.0, v_b_backward=1.0,
        baseline_labor=1.0, transfer_income=transfer_income, borrowing_rate_gap=gap,
        a_max=float(grid.a[-1]), da=da, db=db,
        at_lower_a=False, at_upper_a=False, at_lower_b=False, at_upper_b=False,
        inputs=inputs, params=params,
    )
    assert p.consumption > 0.0
    assert p.liquid_label in ("B", "F", "0")
    assert p.transfer_label in ("B", "F", "0")
    assert p.effective_illiquid_return == float(matlab_faithful_illiquid_return(a_mid, grid.a[-1], inputs.r_a))
    assert p.mu_a == p.transfer + p.effective_illiquid_return * a_mid
    assert p.a_forward_rate >= 0.0 and p.b_forward_rate >= 0.0
    assert p.a_backward_rate >= 0.0 and p.b_backward_rate >= 0.0


def test_local_policy_boundary_flags():
    grid, params, inputs, _, _, _, transfer_income, gap = build_fixture()
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    # lower-a boundary: at_lower_a must be flagged; buying (positive d) is forced only upward.
    p_lower = select_matlab_faithful_local_policy(
        a=float(grid.a[0]), b=float(grid.b[10]), z=1.3,
        v_a_forward=1.4, v_a_backward=0.9, v_b_forward=1.0, v_b_backward=1.0,
        baseline_labor=1.0, transfer_income=transfer_income, borrowing_rate_gap=gap,
        a_max=float(grid.a[-1]), da=da, db=db,
        at_lower_a=True, at_upper_a=False, at_lower_b=False, at_upper_b=False,
        inputs=inputs, params=params,
    )
    assert p_lower.transfer >= 0.0  # at a=0, no negative transfer survives the boundary rule
    # upper-b boundary: forward transfer forced off, backward forced on.
    p_topb = select_matlab_faithful_local_policy(
        a=float(grid.a[10]), b=float(grid.b[-1]), z=0.8,
        v_a_forward=1.2, v_a_backward=1.1, v_b_forward=1.0, v_b_backward=1.0,
        baseline_labor=1.0, transfer_income=transfer_income, borrowing_rate_gap=gap,
        a_max=float(grid.a[-1]), da=da, db=db,
        at_lower_a=False, at_upper_a=False, at_lower_b=False, at_upper_b=True,
        inputs=inputs, params=params,
    )
    assert p_topb.liquid_direction in ("0", "B")


# ---------------------------------------------------------------------------
# 4. sparse operator construction smoke test
# ---------------------------------------------------------------------------
def test_source_axis_boundary_truncation():
    backward = np.zeros((2, 2, 1))
    forward = np.zeros_like(backward)
    backward[0, 0, 0] = 2.0
    forward[1, 0, 0] = 3.0
    matrix = assemble_source_axis(backward, forward, 0).toarray()
    # outward components are truncated but their diagonal is retained.
    assert matrix[0, 0] == -2.0 and np.count_nonzero(matrix[0]) == 1
    assert matrix[1, 1] == -3.0 and np.count_nonzero(matrix[1]) == 1


def test_contaminated_row_index_reference():
    assert matlab_contaminated_row_index(800) == 295
    assert matlab_contaminated_row_index(50) == 17


# ---------------------------------------------------------------------------
# 5. stationary KFE transfer test
# ---------------------------------------------------------------------------
def test_stationary_kfe_density_normalization():
    operator = sparse.csr_matrix(np.array([[-1.0, 1.0, 0.0], [1.0, -2.0, 1.0], [0.0, 1.0, -1.0]]))
    kfe = solve_matlab_faithful_stationary_kfe(operator, shape=(3, 1, 1), db=0.5, da=0.25)
    # density integrates to one against the grid cell measure (accepted contract).
    assert np.sum(kfe.density_vector) * kfe.cell_weight == 1.0
    assert kfe.contaminated_row_index == matlab_contaminated_row_index(3)


# ---------------------------------------------------------------------------
# 6. household aggregate transfer test
# ---------------------------------------------------------------------------
def test_household_aggregate_weighting():
    grid = MatlabFaithfulHJBGrid(np.array([-1.0, 1.0]), np.array([0.0, 2.0]), np.array([1.0, 3.0]), np.zeros((2, 2)))
    shape = (2, 2, 2)
    g = np.ones(shape)
    consumption = np.arange(8.0, dtype=float).reshape(shape, order="F")
    labor = np.ones(shape)
    q = aggregate_stationary_household(grid, consumption, labor, g)
    weight = 4.0
    assert q.c_ss == np.sum(consumption) * weight
    assert q.l_ss == np.sum(np.broadcast_to(grid.z[None, None, :], shape)) * weight
    assert q.a_ss == np.sum(np.broadcast_to(grid.a[None, :, None], shape)) * weight
    assert q.b_ss == np.sum(np.broadcast_to(grid.b[:, None, None], shape)) * weight
    assert q.total_assets == q.a_ss + q.b_ss


# ---------------------------------------------------------------------------
# 7. deterministic repeat test + end-to-end steady-state smoke
# ---------------------------------------------------------------------------
def test_end_to_end_steady_state_smoke():
    grid, params, inputs, numerics, initial, labor0, transfer_income, gap = build_fixture()
    result = solve_household_steady_state(grid, params, inputs, initial, labor0, transfer_income, gap, numerics)
    assert result.hjb.converged
    assert result.hjb.convergence_statistic <= 1e-7
    assert np.isfinite(result.aggregates.c_ss)
    assert result.aggregates.density_normalization == 1.0
    # separate asset aggregates: both assets held and distinct in this fixture.
    assert result.aggregates.a_ss > 0.0
    assert result.aggregates.b_ss != result.aggregates.a_ss
    assert np.isfinite(result.aggregates.l_ss)


def test_deterministic_repeat():
    grid, params, inputs, numerics, initial, labor0, transfer_income, gap = build_fixture()
    first = solve_household_steady_state(grid, params, inputs, initial, labor0, transfer_income, gap, numerics)
    second = solve_household_steady_state(grid, params, inputs, initial, labor0, transfer_income, gap, numerics)
    assert float(np.max(np.abs(first.hjb.value - second.hjb.value))) == 0.0
    assert float(np.max(np.abs(first.kfe.density - second.kfe.density))) == 0.0
    assert first.aggregates.c_ss == second.aggregates.c_ss
    assert first.aggregates.a_ss == second.aggregates.a_ss
    assert first.aggregates.b_ss == second.aggregates.b_ss
    assert first.hjb.iterations == second.hjb.iterations
