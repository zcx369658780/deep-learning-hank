"""DLH-5V-J Gate 3: exactly ONE predeclared deterministic HJB smoke.

FROZEN SMOKE CONFIGURATION (predeclared before the first run, NOT modified by
any engineering retry or Micro-Rev):
  m = 1, W_max = 10.0   (VALIDATION INSTANCE ONLY, not a production W_max)
  r_b = 0.02, r_a = 0.08  (DIAGNOSTIC / VALIDATION ONLY)
  borrowing_rate_gap = 0.0
  delta = 1000.0
  tolerance_iter = 1e-7 (max |V_new - V_old|)
  tolerance_Bellman = 1e-3 (inf norm), max_iterations = 1000
  bracket init: transfer-FOC anchor +/- D (D = max(1, |d*|)), expansion x4,
  max 3 expansions, deterministic c/l/d grids (n_c = n_d = 9)
  structural tolerances: drift 1e-12, row sum 1e-9, first moment 1e-9

SMOKE RESULT (Terminal B, Micro-Rev classification repair per Reviewer
comment 5645920346): iteration 1 is unchanged (conservative, deterministic:
186 boundary rows + 596 F0 rows, 0 expansions, 0 artificial bindings,
max|Q row sum| = 7.1e-15, V1 finite and bounded). Iteration 2 fails
deterministically with DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE at the SAME F3
state (j, i) = (13, 13), z = 0: the accepted boundary effective-domain guard
(frozen Issue #57 Rev-2 rule) surfaces BEFORE any raw candidate/bracket
search because the effective liquid marginal evidence p_b = (V(s)-V(down))/db
is non-positive on the iteration-2 value iterate (recorded p_b = -0.3652 < 0).
The iterate has left the accepted positive-liquid-marginal effective domain;
the previously documented unbounded R_DEPLETE Bellman score is the CONSEQUENCE
of this invalid effective-domain state (q_down * [V(down)-V(s)] -> +inf as
|d|, c grow). This is an effective-domain / unbounded-control
production-iteration failure WITHIN the frozen Issue #56 Outcome-B
convergence-application block; the run never reaches the iterate-convergence
or final Bellman residual stage. The tests below pin the corrected
deterministic failure signature (family, cell, z, iteration, offending p_b)
and the deterministic repeat.
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
    # corrected classification: effective-domain failure, NOT optimizer search
    assert exc.failure_name == "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE"
    assert exc.failure_name != "OPTIMIZER_SEARCH_FAILURE"
    # same failing state as reported for candidate d0e5267
    assert "F3" in exc.message and "(13,13)" in exc.message and "z=0" in exc.message
    # the guard fires BEFORE candidate/bracket search (no expansion disguise)
    assert "before candidate/bracket search" in exc.message
    # detail records family/state/z/iteration and the offending derivative
    assert exc.detail.get("iteration") == 2
    assert exc.detail.get("family") == "F3"
    assert (exc.detail.get("j"), exc.detail.get("i")) == (13, 13)
    assert exc.detail.get("z") == 0
    assert exc.detail.get("p_b") <= 0.0
    # recorded p_b is the declared backward derivative (V(s)-V(down))/db,
    # approximately -0.3652 (db = 7/19, V(s)-V(down) = -0.1346)
    assert abs(exc.detail["p_b"] - (-0.1346 / (7.0 / 19.0))) < 1e-3


def test_gate3_smoke_deterministic_repeat():
    e1 = run_smoke()
    e2 = run_smoke()
    assert e1.failure_name == e2.failure_name
    assert e1.failure_name == "DERIVATIVE_EFFECTIVE_DOMAIN_FAILURE"
    assert e1.message == e2.message
    assert e1.detail == e2.detail
    assert e1.detail.get("p_b") <= 0.0 and e2.detail.get("p_b") <= 0.0
    # iteration-1 stage determinism (same V1 for both runs)
    solver = BoundaryHJBSolver(frozen_config())
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    v1a = solver._iteration_one_value(labor0, 0.0, 0.0)
    v1b = solver._iteration_one_value(labor0, 0.0, 0.0)
    assert np.max(np.abs(v1a - v1b)) == 0.0
    # the iterate is finite and bounded (the failure is an effective-domain
    # selection failure, not a divergence of the value iterate)
    assert np.isfinite(v1a).all()
    assert -100.0 < v1a.min() and v1a.max() < -1.0
