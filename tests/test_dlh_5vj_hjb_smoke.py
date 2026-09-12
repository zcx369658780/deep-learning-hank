"""DLH-5V-J Gate 3: exactly ONE predeclared deterministic HJB smoke.

FROZEN SMOKE CONFIGURATION (predeclared before the first run, NOT modified by
any engineering retry):
  m = 1, W_max = 10.0   (VALIDATION INSTANCE ONLY, not a production W_max)
  r_b = 0.02, r_a = 0.08  (DIAGNOSTIC / VALIDATION ONLY)
  borrowing_rate_gap = 0.0
  delta = 1000.0
  tolerance_iter = 1e-7 (max |V_new - V_old|)
  tolerance_Bellman = 1e-3 (inf norm), max_iterations = 1000
  bracket init: transfer-FOC anchor +/- D (D = max(1, |d*|)), expansion x4,
  max 3 expansions, deterministic c/l/d grids (n_c = n_d = 9)
  structural tolerances: drift 1e-12, row sum 1e-9, first moment 1e-9

SMOKE RESULT (Terminal B, documented in the implementation report): the full
solve deterministically terminates at iteration 2 with
OPTIMIZER_SEARCH_FAILURE at family F3, cell (j, i) = (13, 13), z = 0: the
Bellman score is unbounded above over the admissible candidate set on the
non-monotone iteration-2 value iterate (V(13,12) - V(13,13) > 0 makes the
R_DEPLETE q_down contribution diverge as |d|, c grow; no finite bracket
localizes the argmax). This is the frozen Issue #56 Outcome-B
unbounded-control convergence-application block, exactly as the accepted
design's failure taxonomy classifies it; the iteration never reaches the
final Bellman residual stage. The tests below pin the deterministic failure
signature (family, cell, z, iteration) and the deterministic repeat.
"""

import numpy as np
import pytest

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    EconomicParams,
    HouseholdInputs,
)
from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBConfig,
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)

PARAMS = EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)
INPUTS = HouseholdInputs(r_a=0.08, r_b=0.02, tau=0.15, wages=[1.0],
                         migration_costs=[0.0], labor_weights=[1.0])
Z = np.array([0.8, 1.3])
SWITCH = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])


def frozen_config() -> BoundaryHJBConfig:
    return BoundaryHJBConfig(
        m=1, w_max=10.0, b_min=-2.0, a_max=10.0, params=PARAMS, inputs=INPUTS,
        z=Z, switch_matrix=SWITCH, delta=1000.0, tolerance_iter=1e-7,
        tolerance_bellman=1e-3, max_iterations=1000,
    )


def run_smoke() -> BoundaryHJBFailure:
    solver = BoundaryHJBSolver(frozen_config())
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    with pytest.raises(BoundaryHJBFailure) as excinfo:
        solver.solve(V0, labor0, 0.0, 0.0)
    return excinfo.value


def test_gate3_smoke_deterministic_failure_signature():
    exc = run_smoke()
    assert exc.failure_name == "OPTIMIZER_SEARCH_FAILURE"
    assert "F3" in exc.message and "(13,13)" in exc.message and "z=0" in exc.message
    assert exc.detail.get("iteration") == 2
    assert "artificial bracket binding after 3 expansions" in exc.message


def test_gate3_smoke_deterministic_repeat():
    e1 = run_smoke()
    e2 = run_smoke()
    assert e1.failure_name == e2.failure_name
    assert e1.message == e2.message
    assert e1.detail == e2.detail
    # iteration-1 stage determinism (same V1 for both runs)
    solver = BoundaryHJBSolver(frozen_config())
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    v1a = solver._iteration_one_value(labor0, 0.0, 0.0)
    v1b = solver._iteration_one_value(labor0, 0.0, 0.0)
    assert np.max(np.abs(v1a - v1b)) == 0.0
    # the iterate is finite and bounded (the failure is a selection failure,
    # not a divergence of the value iterate)
    assert np.isfinite(v1a).all()
    assert -100.0 < v1a.min() and v1a.max() < -1.0
