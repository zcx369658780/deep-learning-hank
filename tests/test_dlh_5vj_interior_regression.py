"""DLH-5V-J Gate 1A: common-input local regression of the interior (F0) rows.

For every interior node whose row does not differ from the accepted rectangle
machinery by triangle truncation (i <= 18), the module's F0 row must be
BIT-IDENTICAL to the accepted oracle's local policy + row assembly given the
SAME state and derivative inputs (common-input regression):
- classifier identity (family == F0, transfer_label);
- policy controls (c, l, d) and drifts (mu_a, mu_b) and utility;
- iteration rates (iteration_b_backward/forward, a_backward/forward);
- row assembly: destinations per the accepted placement (b_backward -> (j,i-1),
  b_forward -> (j,i+1), a_backward -> (j-1,i), a_forward -> (j+1,i)), diagonal
  == -(rb + rf + ab + af) with the source truncation convention (no outward
  destination is dropped from the diagonal for this shared-node set).
"""

import numpy as np

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    EconomicParams,
    HouseholdInputs,
    select_matlab_faithful_local_policy,
)
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBConfig,
    BoundaryHJBSolver,
)

PARAMS = EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)
INPUTS = HouseholdInputs(r_a=0.08, r_b=0.02, tau=0.15, wages=[1.0],
                         migration_costs=[0.0], labor_weights=[1.0])
Z = np.array([0.8, 1.3])
SWITCH = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])


def make_solver() -> BoundaryHJBSolver:
    cfg = BoundaryHJBConfig(
        m=1, w_max=10.0, b_min=-2.0, a_max=10.0, params=PARAMS, inputs=INPUTS,
        z=Z, switch_matrix=SWITCH, delta=1000.0, tolerance_iter=1e-7,
        tolerance_bellman=1e-3, max_iterations=1000,
    )
    return BoundaryHJBSolver(cfg)


def test_f0_rows_bit_identical_to_oracle_policy_and_row_assembly():
    solver = make_solver()
    g = solver.grid
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    vb_f, vb_b, va_f, va_b = solver.compute_derivatives(V0, labor0, 0.0, 0.0)
    da = g.da
    db = g.db

    checked = 0
    for node in range(g.n_nodes):
        j, i = int(g.j_arr[node]), int(g.i_arr[node])
        if g.families[node] != "F0" or i > 18:
            continue
        for nz in range(2):
            pol, entries, diag = solver.local_interior_row(
                node, nz, V0, vb_f, vb_b, va_f, va_b, labor0, 0.0, 0.0)
            ref = select_matlab_faithful_local_policy(
                a=float(g.a_arr[node]), b=float(g.b_arr[node]), z=float(Z[nz]),
                v_a_forward=float(va_f[node, nz]), v_a_backward=float(va_b[node, nz]),
                v_b_forward=float(vb_f[node, nz]), v_b_backward=float(vb_b[node, nz]),
                baseline_labor=float(labor0[node, nz]), transfer_income=0.0,
                borrowing_rate_gap=0.0, a_max=10.0, da=da, db=db,
                at_lower_a=(j == 0), at_upper_a=(j == 19),
                at_lower_b=(i == 0), at_upper_b=False,
                inputs=INPUTS, params=PARAMS, tolerance=1e-12)
            # common-input policy identity (bit-exact)
            assert pol.consumption == ref.consumption
            assert pol.labor == ref.labor
            assert pol.transfer == ref.transfer
            assert pol.mu_a == ref.mu_a and pol.mu_b == ref.mu_b
            assert pol.utility == ref.utility
            assert pol.transfer_label == ref.transfer_label
            assert pol.iteration_b_backward_rate == ref.iteration_b_backward_rate
            assert pol.iteration_b_forward_rate == ref.iteration_b_forward_rate
            assert pol.a_backward_rate == ref.a_backward_rate
            assert pol.a_forward_rate == ref.a_forward_rate
            # row assembly identity (accepted placement + truncation convention);
            # zero rates are dropped from the sparse row (identical operator)
            expected = {
                g.node_of[(j, i - 1)]: ref.iteration_b_backward_rate,
                g.node_of[(j, i + 1)]: ref.iteration_b_forward_rate,
                g.node_of[(j - 1, i)]: ref.a_backward_rate,
                g.node_of[(j + 1, i)]: ref.a_forward_rate,
            }
            expected = {d: v for d, v in expected.items() if v != 0.0}
            assert dict(entries) == expected, ((j, i), nz, entries, expected)
            assert diag == -(
                ref.iteration_b_backward_rate + ref.iteration_b_forward_rate
                + ref.a_backward_rate + ref.a_forward_rate)
            checked += 1
    assert checked == 504  # 252 shared F0 nodes x 2 z (validation instance)
