"""DLH-5V-K fixed-household price-envelope diagnostic tests.

Verifies the frozen diagnostic contract:

- legacy rectangle domain: b_max EXACTLY 5, b_min -2, a in [0, 10], 20 points;
- fixed household parameters (VALIDATION_FIXTURE_NOT_CALIBRATION) and
  fixed numerics/initialization conventions;
- exact predeclared 9-case list (r_a line, r_b sentinels, wage sentinels);
- no accidental b_max / W_max / m / resolution variation (run signatures);
- diagnostic output schema (stable CSV header);
- deterministic rerun for a representative central legacy case and a
  representative selected-Q sentinel;
- selected-Q sentinel list exactly {0.07, 0.10, 0.13};
- NO KFE / stationary KFE / steady-state invocation anywhere in the module.

HJB ONLY. No KFE is called; ``solve_household_steady_state`` is never used.
"""

from __future__ import annotations

import inspect

import numpy as np

from deep_learning_hank.two_asset.fixed_household_price_envelope_diagnostic import (
    CSV_HEADER,
    FROZEN_PARAMS,
    LEGACY_A,
    LEGACY_B,
    LEGACY_GRID,
    LEGACY_NUMERICS,
    PREDECLARED_LEGACY_CASES,
    SELECTED_Q_M,
    SELECTED_Q_R_A_SENTINELS,
    SELECTED_Q_W_MAX,
    SWITCH,
    Z,
    all_case_rows,
    csv_lines,
    run_legacy_case,
    run_selected_q_case,
)


# ---------------------------------------------------------------------------
# Frozen domain / household / numerics
# ---------------------------------------------------------------------------
def test_frozen_legacy_grid_bmax_exactly_5_and_a_0_10():
    assert LEGACY_B.size == 20
    assert float(LEGACY_B[0]) == -2.0
    assert float(LEGACY_B[-1]) == 5.0          # b_max = 5 IS FROZEN
    assert float(LEGACY_A[0]) == 0.0
    assert float(LEGACY_A[-1]) == 10.0
    assert LEGACY_A.size == 20
    assert np.all(np.diff(LEGACY_B) > 0) and np.all(np.diff(LEGACY_A) > 0)


def test_frozen_household_parameters_and_z_switch():
    assert FROZEN_PARAMS.rho == 0.02
    assert FROZEN_PARAMS.gamma_c == 2.0
    assert FROZEN_PARAMS.phi == 5.0
    assert FROZEN_PARAMS.chi_0 == 0.1
    assert FROZEN_PARAMS.chi_1 == 2.0
    assert FROZEN_PARAMS.a_bar == 1e-6
    assert np.allclose(Z, [0.8, 1.3])
    assert np.allclose(SWITCH, [[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    assert LEGACY_NUMERICS.delta == 1000.0
    assert LEGACY_NUMERICS.convergence_tolerance == 1e-7
    assert LEGACY_NUMERICS.max_iterations == 1000


def test_exact_predeclared_case_list():
    assert PREDECLARED_LEGACY_CASES == [
        (0.05, 0.02, 1.00),
        (0.07, 0.02, 1.00),   # central anchor / safe-region reference
        (0.09, 0.02, 1.00),
        (0.11, 0.02, 1.00),
        (0.13, 0.02, 1.00),   # high-rate reference
        (0.07, 0.015, 1.00),
        (0.07, 0.025, 1.00),
        (0.07, 0.02, 0.80),
        (0.07, 0.02, 1.20),
    ]
    assert len(PREDECLARED_LEGACY_CASES) == 9
    assert (0.07, 0.02, 1.00) in PREDECLARED_LEGACY_CASES


def test_no_bmax_or_wmax_variation():
    # run entry points accept ONLY (r_a, r_b, w) plus the frozen gap default;
    # no b_max / W_max / m / resolution parameters exist
    legacy_params = inspect.signature(run_legacy_case).parameters
    sq_params = inspect.signature(run_selected_q_case).parameters
    for name in ("b_max", "W_max", "m", "resolution", "grid"):
        assert name not in legacy_params
        assert name not in sq_params
    assert SELECTED_Q_M == 1
    assert SELECTED_Q_W_MAX == 10.0


def test_selected_q_sentinels_exactly_three():
    assert SELECTED_Q_R_A_SENTINELS == [0.07, 0.10, 0.13]


# ---------------------------------------------------------------------------
# Schema / determinism / no-KFE
# ---------------------------------------------------------------------------
def test_diagnostic_output_schema_selected_q():
    rec = run_selected_q_case(0.07)
    for key in CSV_HEADER:
        assert key in rec, key
    assert rec["solver"] == "selected_q"
    assert rec["domain"] == "triangle W_max=10"
    assert rec["iter1_max_abs_q1"] is not None
    assert rec["iter1_min_boundary_p_b"] is not None


def test_diagnostic_output_schema_legacy():
    rec = run_legacy_case(0.07, 0.02, 1.00)
    for key in CSV_HEADER:
        assert key in rec, key
    assert rec["solver"] == "legacy_oracle"
    assert rec["domain"] == "rectangle b_max=5"
    assert rec["converged"] is True          # central anchor converges on frozen rectangle
    assert rec["iterations"] < 1000
    assert rec["convergence_statistic"] < 1e-7
    assert rec["v_finite"] is True
    assert rec["vb_min_evidence"] is not None
    assert rec["vb_nonpositive_share"] is not None


def test_deterministic_rerun_selected_q():
    a = run_selected_q_case(0.10)
    b = run_selected_q_case(0.10)
    assert a == b


def test_deterministic_rerun_central_legacy():
    a = run_legacy_case(0.07, 0.02, 1.00)
    b = run_legacy_case(0.07, 0.02, 1.00)
    assert a == b


def test_csv_lines_schema_consistency():
    rows = [run_selected_q_case(0.07)]
    lines = csv_lines(rows)
    assert lines[0].split(",") == CSV_HEADER
    assert len(lines) == 2
    assert len(lines[1].split(",")) == len(CSV_HEADER)


def test_no_kfe_or_steady_state_invocation():
    import ast
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[1] / "src"
    module_text = (src / "deep_learning_hank" / "two_asset"
                   / "fixed_household_price_envelope_diagnostic.py").read_text(encoding="utf-8")
    tree = ast.parse(module_text)
    used: set[str] = set()
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.ImportFrom):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
    # no API reference / call site for KFE, stationary KFE, or steady state
    for banned in ("solve_matlab_faithful_stationary_kfe", "solve_household_steady_state",
                   "aggregate_stationary_household", "MatlabFaithfulKFEResult",
                   "StationaryHouseholdAggregates", "solve_matlab_faithful_hjb_kfe"):
        assert banned not in used and banned not in imported, banned
    # the only oracle imports are the HJB-only public entry points
    for required in ("solve_matlab_faithful_hjb", "BoundaryHJBSolver",
                     "MatlabFaithfulHJBGrid", "MatlabFaithfulHJBNumerics"):
        assert required in imported, required
    # no distribution / stationary aggregate computation
    assert "density" not in used
    assert "stationary" not in used
