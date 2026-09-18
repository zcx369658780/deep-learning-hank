"""DLH-WL-P1A — focused deterministic tests for the offline conditional
labor-destination accounting interface (Issue #74).

Authority: Issue #74 ``DLH-WL-P1A``; final Reviewer activation comment
``5730955781``; authority marker
``DLH_WL_P1A_OFFLINE_ACCOUNTING_AND_HOUSEHOLD_REGISTRY_AUTHORIZED``.
Operative baseline ``e046feccf9f98adad0d7db713eca427e0e7f1e36``.

This file also carries the bounded remediation of Reviewer HOLD ``5731223867``:
``conditional_choice_identified`` is TRUE only when at least one row has
``m_i > 0``, ``ell_i > 0``, a valid conditional-share row and at least two
structurally available foreign destinations (see the section-1b tests).

Scope ceiling (binding): offline algebra only.  No household solver, no HJB, no
KFE, no GE/outer fixed point, no MATLAB, no training, no data download, no
repository-wide suite.  Expensive scientific/model calls = 0.

All fixtures are deterministic and deliberately **asymmetric** so that a
transposed ``[destination, origin]`` orientation cannot pass accidentally.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from deep_learning_hank.regional import labor_destination as m

MODULE_PATH = Path(m.__file__)
MODULE_SOURCE = MODULE_PATH.read_text(encoding="utf-8")
TREE = ast.parse(MODULE_SOURCE)

REPO_ROOT = MODULE_PATH.parents[3]
SRC_ROOT = REPO_ROOT / "src"

# --- repository paths that this Issue must NOT touch or execute ---
ORACLE_RELPATH = "src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py"
SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"
KFE_RELPATH = "src/deep_learning_hank/two_asset/conservative_stationary_kfe.py"

FORBIDDEN_IMPORT_ROOTS = (
    "scipy",
    "torch",
    "tensorflow",
    "jax",
    "sklearn",
    "matlab",
    "deep_learning_hank.two_asset",
    "subprocess",
    "importlib",
    "os",
    "shutil",
)

ALLOWED_IMPORT_NAMES = {"__future__", "dataclasses", "typing", "numpy"}

# --- deterministic asymmetric 3-region fixture ---
#   m and ell are pairwise unequal; W is asymmetric and NOT doubly stochastic;
#   row 0 sends more labor to destination 1, row 1 splits evenly.
FIXTURE_M = (0.25, 0.4, 0.0)
FIXTURE_ELL = (100.0, 60.0, 40.0)
FIXTURE_W = (
    (0.0, 0.75, 0.25),
    (0.5, 0.0, 0.5),
    (0.5, 0.5, 0.0),
)
FIXTURE_WAGES = (2.0, 3.0, 5.0)


def _fixture(**overrides):
    kwargs = dict(
        m=np.array(FIXTURE_M, dtype=float),
        ell=np.array(FIXTURE_ELL, dtype=float),
        W=np.array(FIXTURE_W, dtype=float),
    )
    kwargs.update(overrides)
    return kwargs


def _imported_names(source: str) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"__import__", "eval", "exec", "compile", "open"}:
                names.add(f"CALL:{node.func.id}")
    return names


# --------------------------------------------------------------------------
# 1. asymmetric 3-region baseline with unequal m and ell
# --------------------------------------------------------------------------
def test_asymmetric_three_region_accounting_matches_closed_form():
    result = m.build_labor_destination_accounting(**_fixture())

    assert result.region_count == 3
    assert result.m.tolist() == list(FIXTURE_M)
    assert result.ell.tolist() == list(FIXTURE_ELL)

    m_arr = np.array(FIXTURE_M)
    ell_arr = np.array(FIXTURE_ELL)
    W = np.array(FIXTURE_W)
    expected_P = np.eye(3) * (1.0 - m_arr)[:, None] + m_arr[:, None] * W
    expected_F = ell_arr[:, None] * expected_P

    np.testing.assert_allclose(result.P, expected_P, rtol=0.0, atol=0.0)
    np.testing.assert_allclose(result.F, expected_F, rtol=0.0, atol=0.0)
    np.testing.assert_allclose(
        result.destination_labor, expected_F.sum(axis=0), rtol=0.0, atol=0.0
    )
    # hand-computed closed form for the fixture
    np.testing.assert_allclose(
        result.P,
        [[0.75, 0.1875, 0.0625], [0.2, 0.6, 0.2], [0.0, 0.0, 1.0]],
        rtol=0.0,
        atol=1e-15,
    )
    np.testing.assert_allclose(
        result.F,
        [[75.0, 18.75, 6.25], [12.0, 36.0, 12.0], [0.0, 0.0, 40.0]],
        rtol=0.0,
        atol=1e-12,
    )


def test_rectangular_case_is_rejected_and_orientation_is_asymmetric():
    """Orientation guard: the accounting is square ``[origin, destination]`` only,
    a transposed ``[destination, origin]`` reading is not accepted, and the
    fixture is genuinely asymmetric."""
    m_vec = np.array([0.25, 0.4, 0.0])
    ell_vec = np.array([100.0, 60.0, 40.0])
    rectangular = np.array([[0.0, 1.0], [0.6, 0.0], [0.3, 0.7]])

    assert rectangular.shape != rectangular.T.shape
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(m=m_vec, ell=ell_vec, W=rectangular)
    assert excinfo.value.reason == "DIMENSION_MISMATCH"
    # the transposed reading has the wrong shape as well
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo2:
        m.build_labor_destination_accounting(m=m_vec, ell=ell_vec, W=rectangular.T)
    assert excinfo2.value.reason == "DIMENSION_MISMATCH"

    W = np.array(FIXTURE_W)
    assert not np.allclose(W, W.T)
    assert not np.allclose(W.sum(axis=0), W.sum(axis=1))

    # a row-normalized transposed reading is accepted as *input* but denotes a
    # different economic object and must not reproduce the same flows
    W_transposed = np.array(
        [[0.0, 0.5, 0.5], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]
    )
    np.testing.assert_allclose(W_transposed.sum(axis=1), 1.0, rtol=0.0, atol=1e-15)
    square = m.build_labor_destination_accounting(**_fixture())
    transposed = m.build_labor_destination_accounting(
        m=np.array(FIXTURE_M), ell=np.array(FIXTURE_ELL), W=W_transposed
    )
    assert not np.allclose(square.F, transposed.F)
    assert not np.allclose(square.destination_labor, transposed.destination_labor)
    assert not np.allclose(square.P, transposed.P)


def test_orientation_and_scope_metadata_are_recorded():
    result = m.build_labor_destination_accounting(**_fixture())
    assert result.diagnostics["orientation"] == "origin_x_destination"
    assert result.diagnostics["region_count"] == 3
    assert result.diagnostics["two_region_accounting_only"] is False
    assert result.diagnostics["single_region_limit"] is False
    assert result.conditional_choice_identified is True
    assert result.units is None
    # the 3-region fixture has >= 2 available foreign options in its active rows,
    # so the corrected identification flag stays TRUE
    assert result.rows_with_conditional_choice.tolist() == [True, True, False]
    assert result.diagnostics["rows_with_conditional_choice"] == [0, 1]
    assert result.diagnostics["rows_with_conditional_choice_count"] == 2


# --------------------------------------------------------------------------
# 1b. conditional_choice_identified semantics (Reviewer HOLD 5731223867)
# --------------------------------------------------------------------------
def test_conditional_choice_not_identified_when_only_active_row_has_zero_labor():
    """>=3 regions, active row with ell_i = 0 and otherwise valid W -> False."""
    result = m.build_labor_destination_accounting(
        m=np.array([0.25, 0.0, 0.0]),
        ell=np.array([0.0, 50.0, 40.0]),
        W=np.array([[0.0, 0.6, 0.4], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]),
    )
    assert result.region_count == 3
    # the only m_i > 0 row carries no labor, so it supplies no identifiable target
    assert result.active_row_mask.tolist() == [True, False, False]
    assert result.rows_without_identifiable_target.tolist() == [True, True, True]
    assert np.all(result.F[0] == 0.0)
    assert result.conditional_choice_identified is False
    assert result.rows_with_conditional_choice.tolist() == [False, False, False]
    assert result.diagnostics["rows_with_conditional_choice"] == []
    assert result.diagnostics["rows_with_conditional_choice_count"] == 0
    # W/P/F accounting and conservation are untouched by the flag change
    np.testing.assert_allclose(result.P[0], [0.75, 0.15, 0.1], rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(result.F.sum(axis=1), result.ell, rtol=0.0, atol=1e-15)


def test_conditional_choice_not_identified_with_one_available_foreign_destination():
    """>=3 regions, every active positive-labor row has exactly one available foreign
    destination under support_mask -> False (degenerate choice)."""
    result = m.build_labor_destination_accounting(
        m=np.array([0.3, 0.0, 0.4]),
        ell=np.array([100.0, 20.0, 30.0]),
        W=np.array([[0.0, 1.0, 0.0], [0.5, 0.0, 0.5], [0.0, 1.0, 0.0]]),
        support_mask=np.array(
            [[False, True, False], [True, False, True], [False, True, False]]
        ),
    )
    assert result.region_count == 3
    # both active rows are supported by exactly ONE foreign destination
    assert result.active_row_mask.tolist() == [True, False, True]
    assert result.support_mask.sum(axis=1).tolist() == [1, 2, 1]
    assert result.F[0].tolist() == [70.0, 30.0, 0.0]
    assert result.F[2].tolist() == [0.0, 12.0, 18.0]
    assert result.conditional_choice_identified is False
    assert result.rows_with_conditional_choice.tolist() == [False, False, False]
    assert result.diagnostics["rows_with_conditional_choice_count"] == 0
    assert result.diagnostics["n_regions_available_per_origin_min"] == 1
    # a row with only one option is not reported as having no identifiable target:
    # it does carry labor abroad, it simply has no choice to identify
    assert not bool(result.rows_without_identifiable_target[0])


def test_conditional_choice_not_identified_in_large_economy_with_one_option():
    """The old >= 3 regions shortcut must not matter: 4 regions can still be False."""
    result = m.build_labor_destination_accounting(
        m=np.array([0.3, 0.0, 0.0, 0.0]),
        ell=np.array([100.0, 20.0, 30.0, 10.0]),
        W=np.array(
            [
                [0.0, 1.0, 0.0, 0.0],
                [0.25, 0.0, 0.25, 0.5],
                [0.25, 0.25, 0.0, 0.5],
                [0.25, 0.25, 0.5, 0.0],
            ]
        ),
        support_mask=np.array(
            [
                [False, True, False, False],
                [True, False, True, True],
                [True, True, False, True],
                [True, True, True, False],
            ]
        ),
    )
    assert result.region_count == 4
    assert result.conditional_choice_identified is False
    assert result.diagnostics["rows_with_conditional_choice_count"] == 0


def test_conditional_choice_identified_with_two_available_foreign_destinations():
    """>=3 regions, active positive-labor row with >= 2 available options -> True."""
    result = m.build_labor_destination_accounting(
        m=np.array([0.4, 0.0, 0.3]),
        ell=np.array([100.0, 20.0, 30.0]),
        W=np.array([[0.0, 0.6, 0.4], [0.4, 0.0, 0.6], [0.5, 0.5, 0.0]]),
        support_mask=np.array(
            [[False, True, True], [True, False, True], [True, True, False]]
        ),
    )
    assert result.diagnostics["n_regions_available_per_origin_min"] >= 2
    assert result.rows_with_conditional_choice.tolist() == [True, False, True]
    assert result.conditional_choice_identified is True


# --------------------------------------------------------------------------
# 2. exact origin conservation and national conservation
# --------------------------------------------------------------------------
def test_origin_and_national_conservation_are_exact():
    result = m.build_labor_destination_accounting(**_fixture())

    np.testing.assert_allclose(result.F.sum(axis=1), result.ell, rtol=0.0, atol=1e-15)
    assert float(result.F.sum()) == pytest.approx(result.total_labor, abs=1e-15)
    assert result.diagnostics["origin_conservation_max_abs_deviation"] == 0.0
    assert result.diagnostics["national_conservation_max_abs_deviation"] == 0.0


def test_home_and_foreign_mass_decompose_per_origin():
    result = m.build_labor_destination_accounting(**_fixture())
    home = np.diag(result.F)
    foreign = result.F.sum(axis=1) - home

    np.testing.assert_allclose(home, (1.0 - result.m) * result.ell, rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(foreign, result.m * result.ell, rtol=0.0, atol=1e-15)
    assert result.diagnostics["own_region_diagonal_max_abs_deviation"] == 0.0


# --------------------------------------------------------------------------
# 3. destination aggregation
# --------------------------------------------------------------------------
def test_destination_aggregation_equals_column_sums():
    result = m.build_labor_destination_accounting(**_fixture())

    manual = np.array(
        [
            result.F[0, 0] + result.F[1, 0] + result.F[2, 0],
            result.F[0, 1] + result.F[1, 1] + result.F[2, 1],
            result.F[0, 2] + result.F[1, 2] + result.F[2, 2],
        ]
    )
    np.testing.assert_allclose(result.destination_labor, manual, rtol=0.0, atol=0.0)
    assert result.diagnostics["destination_aggregation_max_abs_deviation"] == 0.0

    # explicit hand-computed destination labor
    np.testing.assert_allclose(
        result.destination_labor, [87.0, 54.75, 58.25], rtol=0.0, atol=1e-12
    )
    assert float(result.destination_labor.sum()) == pytest.approx(
        result.total_labor, abs=1e-12
    )


# --------------------------------------------------------------------------
# 4. zero diagonal / non-negativity / required-row normalization
# --------------------------------------------------------------------------
def test_zero_diagonal_non_negativity_and_required_row_normalization():
    result = m.build_labor_destination_accounting(**_fixture())

    np.testing.assert_array_equal(np.diag(result.W), np.zeros(3))
    assert np.all(result.W >= 0.0)
    assert np.all(result.F >= 0.0)
    np.testing.assert_allclose(
        result.W.sum(axis=1)[result.valid_row_mask], 1.0, rtol=0.0, atol=1e-15
    )
    assert result.active_row_mask.tolist() == [True, True, False]
    assert result.valid_row_mask.tolist() == [True, True, False]
    assert result.diagnostics["active_row_count"] == 2
    assert result.diagnostics["valid_row_count"] == 2


# --------------------------------------------------------------------------
# 5. wage-bill identity with unequal wages
# --------------------------------------------------------------------------
def test_wage_bill_identity_closes_with_unequal_wages():
    wages = np.array(FIXTURE_WAGES)
    result = m.build_labor_destination_accounting(**_fixture(destination_wages=wages))

    expected_wbar = result.P @ wages
    np.testing.assert_allclose(result.wbar, expected_wbar, rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(
        result.wbar, [2.375, 3.2, 5.0], rtol=0.0, atol=1e-15
    )

    left = float((result.ell * result.wbar).sum())
    right = float((result.destination_labor * wages).sum())
    assert right == pytest.approx(left, rel=0.0, abs=1e-12)
    assert result.diagnostics["wage_bill_identity_closed"] is True
    assert result.diagnostics["wage_bill_abs_deviation"] == pytest.approx(0.0, abs=1e-12)
    assert result.diagnostics["wage_bill_left"] == pytest.approx(629.5, abs=1e-9)
    assert result.diagnostics["wage_bill_right"] == pytest.approx(629.5, abs=1e-9)

    # the identity is only non-trivial because wages differ across destinations
    assert not np.allclose(wages, wages[0])


def test_wage_outputs_absent_when_no_wages_supplied():
    result = m.build_labor_destination_accounting(**_fixture())
    assert result.destination_wages is None
    assert result.wbar is None
    assert result.destination_wage_bill is None
    assert "wage_bill_identity_closed" not in result.diagnostics


# --------------------------------------------------------------------------
# 6. region-permutation equivariance
# --------------------------------------------------------------------------
def test_region_permutation_equivariance():
    perm = np.array([2, 0, 1])
    base = m.build_labor_destination_accounting(**_fixture())
    permuted = m.build_labor_destination_accounting(
        m=np.array(FIXTURE_M)[perm],
        ell=np.array(FIXTURE_ELL)[perm],
        W=np.array(FIXTURE_W)[np.ix_(perm, perm)],
    )

    np.testing.assert_allclose(
        permuted.F, base.F[np.ix_(perm, perm)], rtol=0.0, atol=1e-12
    )
    np.testing.assert_allclose(
        permuted.destination_labor, base.destination_labor[perm], rtol=0.0, atol=1e-12
    )
    np.testing.assert_allclose(
        permuted.P, base.P[np.ix_(perm, perm)], rtol=0.0, atol=1e-12
    )
    assert permuted.total_labor == pytest.approx(base.total_labor, abs=1e-12)
    assert permuted.valid_row_mask.tolist() == base.valid_row_mask[perm].tolist()


# --------------------------------------------------------------------------
# 7. two-region accounting degeneration
# --------------------------------------------------------------------------
def test_two_region_case_is_accounting_only():
    result = m.build_labor_destination_accounting(
        m=np.array([0.3, 0.2]),
        ell=np.array([100.0, 50.0]),
        W=np.array([[0.0, 1.0], [1.0, 0.0]]),
    )

    np.testing.assert_allclose(result.P, [[0.7, 0.3], [0.2, 0.8]], rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(
        result.F, [[70.0, 30.0], [10.0, 40.0]], rtol=0.0, atol=1e-12
    )
    np.testing.assert_allclose(
        result.destination_labor, [80.0, 70.0], rtol=0.0, atol=1e-12
    )
    assert result.diagnostics["two_region_accounting_only"] is True
    # the foreign destination is unique in two regions -> no conditional choice
    assert result.conditional_choice_identified is False


# --------------------------------------------------------------------------
# 8. single-region m = 0 limit and fail-closed m > 0
# --------------------------------------------------------------------------
def test_single_region_m_zero_is_the_accounting_limit():
    result = m.build_labor_destination_accounting(
        m=np.array([0.0]), ell=np.array([123.0]), W=np.array([[0.0]])
    )
    np.testing.assert_allclose(result.P, [[1.0]], rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(result.F, [[123.0]], rtol=0.0, atol=1e-12)
    np.testing.assert_allclose(result.destination_labor, [123.0], rtol=0.0, atol=1e-12)
    assert result.diagnostics["single_region_limit"] is True
    assert result.conditional_choice_identified is False
    assert result.rows_without_identifiable_target.tolist() == [True]


def test_single_region_outflow_fails_closed():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([0.5]), ell=np.array([123.0]), W=np.array([[0.0]])
        )
    assert excinfo.value.reason == "SINGLE_REGION_OUTFLOW"
    assert isinstance(excinfo.value, ValueError)


# --------------------------------------------------------------------------
# 9. m = 0 row: no fabricated supervision target
# --------------------------------------------------------------------------
def test_m_zero_row_has_no_fabricated_supervision_target():
    result = m.build_labor_destination_accounting(**_fixture())

    zero_row = 2
    assert result.m[zero_row] == 0.0
    assert not bool(result.active_row_mask[zero_row])
    # full accounting stays well defined ...
    np.testing.assert_allclose(result.P[zero_row], [0.0, 0.0, 1.0], rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(result.F[zero_row], [0.0, 0.0, 40.0], rtol=0.0, atol=1e-12)
    # ... while the row is explicitly reported as carrying no identifiable label
    assert bool(result.rows_without_identifiable_target[zero_row])
    assert result.diagnostics["rows_without_identifiable_target"] == [2]
    # the given W row is echoed unchanged (never rewritten into a uniform target)
    np.testing.assert_allclose(result.W[zero_row], FIXTURE_W[zero_row], rtol=0.0, atol=0.0)
    assert not np.allclose(result.W[zero_row], np.array([0.0, 0.5, 0.5]))


def test_row_without_foreign_option_is_distinct_from_row_without_labor():
    support = np.array(
        [
            [False, False, False],
            [True, False, True],
            [True, True, False],
        ]
    )
    result = m.build_labor_destination_accounting(
        m=np.array([0.0, 0.0, 0.4]),
        ell=np.array([10.0, 20.0, 30.0]),
        W=np.array([[0.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]),
        support_mask=support,
    )
    # origin 0 has no structurally available foreign destination at all
    assert result.diagnostics["rows_without_foreign_option"] == [0]
    assert result.rows_without_foreign_option.tolist() == [True, False, False]
    assert result.F[0].tolist() == [10.0, 0.0, 0.0]
    # origin 1 has a foreign option but m = 0, so it carries no identifiable label
    assert result.m[1] == 0.0
    assert bool(result.rows_without_identifiable_target[1])
    assert result.F[1].tolist() == [0.0, 20.0, 0.0]
    # origin 2 is the only row with both a foreign option and allocated foreign labor
    assert not bool(result.rows_without_identifiable_target[2])
    assert result.diagnostics["rows_without_identifiable_target"] == [0, 1]
    assert result.diagnostics["foreign_option_row_count"] == 2


def test_two_region_row_without_foreign_option():
    """Isolated no-foreign-option case: the W row is a structural zero row."""
    result = m.build_labor_destination_accounting(
        m=np.array([0.0, 0.4]),
        ell=np.array([10.0, 20.0]),
        W=np.array([[0.0, 0.0], [1.0, 0.0]]),
        support_mask=np.array([[False, False], [True, False]]),
    )
    assert result.diagnostics["rows_without_foreign_option"] == [0]
    assert result.rows_without_foreign_option.tolist() == [True, False]
    assert result.rows_without_identifiable_target.tolist() == [True, False]
    assert result.F[0].tolist() == [10.0, 0.0]
    assert result.F[1].tolist() == [8.0, 12.0]


# --------------------------------------------------------------------------
# 10. m = 1 case
# --------------------------------------------------------------------------
def test_m_one_sends_all_labor_abroad():
    result = m.build_labor_destination_accounting(
        m=np.array([1.0, 0.0]),
        ell=np.array([10.0, 10.0]),
        W=np.array([[0.0, 1.0], [1.0, 0.0]]),
    )
    # origin 0 exports everything; origin 1 has m = 0 so its foreign cell is 0
    np.testing.assert_allclose(result.P, [[0.0, 1.0], [0.0, 1.0]], rtol=0.0, atol=1e-15)
    assert result.F[0, 0] == 0.0
    assert result.F[0, 1] == pytest.approx(10.0, abs=1e-15)
    assert result.F[1, 0] == 0.0
    np.testing.assert_allclose(
        result.destination_labor, [0.0, 20.0], rtol=0.0, atol=1e-12
    )
    assert result.diagnostics["own_region_diagonal_max_abs_deviation"] == 0.0
    assert float(result.F.sum()) == pytest.approx(20.0, abs=1e-15)


def test_m_one_without_any_foreign_option_fails_closed():
    """m = 1 with no foreign destination at all is refused outright."""
    # (a) an all-zero conditional row is malformed once m_i > 0
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([1.0, 0.0, 0.0]),
            ell=np.array([10.0, 20.0, 30.0]),
            W=np.array([[0.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]),
            support_mask=np.array(
                [[False, False, False], [True, False, True], [True, True, False]]
            ),
        )
    assert excinfo.value.reason == "ROW_SUM"

    # (b) conditional mass that cannot be routed anywhere is an impossible support
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([1.0, 0.0, 0.0]),
            ell=np.array([10.0, 20.0, 30.0]),
            W=np.array([[0.0, 0.5, 0.6], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]),
            support_mask=np.array(
                [[False, False, False], [True, False, True], [True, True, False]]
            ),
        )
    assert excinfo.value.reason == "IMPOSSIBLE_SUPPORT"


def test_m_zero_row_without_foreign_option_is_reported_not_refused():
    """m = 0 is the no-outflow limit: it is reported, never fabricated or refused."""
    result = m.build_labor_destination_accounting(
        m=np.array([0.0, 0.0, 0.4]),
        ell=np.array([10.0, 20.0, 30.0]),
        W=np.array([[0.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.5, 0.5, 0.0]]),
        support_mask=np.array(
            [[False, False, False], [True, False, True], [True, True, False]]
        ),
    )
    assert result.rows_without_foreign_option.tolist() == [True, False, False]
    assert result.rows_without_identifiable_target.tolist() == [True, True, False]
    assert result.F[0].tolist() == [10.0, 0.0, 0.0]
    assert result.diagnostics["single_region_limit"] is False


# --------------------------------------------------------------------------
# 11. zero ell case
# --------------------------------------------------------------------------
def test_zero_ell_row_produces_zero_flows_and_no_label():
    result = m.build_labor_destination_accounting(
        m=np.array([0.5, 0.3]),
        ell=np.array([0.0, 50.0]),
        W=np.array([[0.0, 1.0], [1.0, 0.0]]),
    )
    np.testing.assert_allclose(result.F[0], [0.0, 0.0], rtol=0.0, atol=0.0)
    assert result.F.sum() == pytest.approx(50.0, abs=1e-15)
    # the origin still declares a foreign share, but carries no labor mass, so it
    # has no identifiable realized target
    np.testing.assert_allclose(result.W[0], [0.0, 1.0], rtol=0.0, atol=0.0)
    assert result.rows_without_identifiable_target.tolist() == [True, False]
    assert result.total_labor == 50.0
    assert result.diagnostics["n_regions_with_positive_labor"] == 1


# --------------------------------------------------------------------------
# 12. structural support mask
# --------------------------------------------------------------------------
def test_structural_support_mask_blocks_unavailable_destination():
    support = np.array(
        [
            [False, True, False],
            [True, False, True],
            [True, True, False],
        ]
    )
    result = m.build_labor_destination_accounting(
        m=np.array(FIXTURE_M),
        ell=np.array(FIXTURE_ELL),
        W=np.array(
            [
                [0.0, 1.0, 0.0],
                [0.5, 0.0, 0.5],
                [0.5, 0.5, 0.0],
            ]
        ),
        support_mask=support,
    )

    np.testing.assert_array_equal(result.support_mask, support)
    assert np.all(result.W[~support] == 0.0)
    assert result.F[0, 2] == 0.0
    np.testing.assert_allclose(result.F[0, 1], 25.0, rtol=0.0, atol=1e-12)
    assert result.diagnostics["support_respected"] is True
    assert result.diagnostics["n_regions_available_per_origin_min"] == 1
    assert result.diagnostics["n_regions_available_per_origin_max"] == 2


def test_support_mask_rejects_mass_on_unavailable_destination():
    support = np.array(
        [[False, True, False], [True, False, True], [True, True, False]]
    )
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M),
            ell=np.array(FIXTURE_ELL),
            W=np.array(FIXTURE_W),
            support_mask=support,
        )
    assert excinfo.value.reason == "IMPOSSIBLE_SUPPORT"


def test_support_mask_diagonal_must_be_unavailable():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            **_fixture(support_mask=np.ones((3, 3), dtype=bool))
        )
    assert excinfo.value.reason == "IMPOSSIBLE_SUPPORT"


# --------------------------------------------------------------------------
# 13. invalid / non-finite / negative / dimension-mismatch failures
# --------------------------------------------------------------------------
def test_dimension_mismatch_fails_closed():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([0.1, 0.2]), ell=np.array([1.0]), W=np.zeros((2, 2))
        )
    assert excinfo.value.reason == "DIMENSION_MISMATCH"


def test_matrix_shape_mismatch_fails_closed():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([0.1, 0.2, 0.3]),
            ell=np.array([1.0, 1.0, 1.0]),
            W=np.zeros((2, 2)),
        )
    assert excinfo.value.reason == "DIMENSION_MISMATCH"


def test_non_1d_input_fails_closed():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([[0.1, 0.2], [0.3, 0.4]]),
            ell=np.array([1.0, 1.0]),
            W=np.zeros((2, 2)),
        )
    assert excinfo.value.reason == "DIMENSION_MISMATCH"


def test_m_out_of_range_fails_closed():
    for bad in (np.array([0.1, -0.01, 0.2]), np.array([0.1, 1.5, 0.2])):
        with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
            m.build_labor_destination_accounting(
                m=bad, ell=np.array([1.0, 1.0, 1.0]), W=np.array(FIXTURE_W)
            )
        assert excinfo.value.reason == "RANGE"


def test_negative_ell_fails_closed():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M),
            ell=np.array([100.0, -1.0, 40.0]),
            W=np.array(FIXTURE_W),
        )
    assert excinfo.value.reason == "NEGATIVE_MASS"


def test_negative_share_fails_closed():
    W = np.array(FIXTURE_W)
    W[0, 1] = -0.25
    W[0, 2] = 1.25
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M), ell=np.array(FIXTURE_ELL), W=W
        )
    assert excinfo.value.reason == "NEGATIVE_MASS"


def test_non_finite_input_fails_closed():
    W = np.array(FIXTURE_W)
    W[0, 1] = np.nan
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M), ell=np.array(FIXTURE_ELL), W=W
        )
    assert excinfo.value.reason == "NON_FINITE"

    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([np.inf, 0.4, 0.0]),
            ell=np.array(FIXTURE_ELL),
            W=np.array(FIXTURE_W),
        )
    assert excinfo.value.reason == "NON_FINITE"


def test_illegal_diagonal_fails_closed():
    W = np.array(FIXTURE_W)
    W[1, 1] = 0.2
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M), ell=np.array(FIXTURE_ELL), W=W
        )
    assert excinfo.value.reason == "ILLEGAL_DIAGONAL"


def test_invalid_row_sum_fails_closed():
    W = np.array(FIXTURE_W)
    W[0, 1] = 0.25  # row 0 now sums to 0.5
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M), ell=np.array(FIXTURE_ELL), W=W
        )
    assert excinfo.value.reason == "ROW_SUM"


def test_zero_conditional_mass_on_required_row_fails_closed():
    support = np.array(
        [[False, True, False], [True, False, True], [True, True, False]]
    )
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M),
            ell=np.array(FIXTURE_ELL),
            W=np.zeros((3, 3)),
            support_mask=support,
        )
    assert excinfo.value.reason == "ROW_SUM"


def test_unsupported_destination_without_mass_fails_closed():
    support = np.array(
        [[False, True, False], [True, False, True], [True, True, False]]
    )
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array(FIXTURE_M),
            ell=np.array(FIXTURE_ELL),
            W=np.array(FIXTURE_W),
            support_mask=support,
        )
    assert excinfo.value.reason == "IMPOSSIBLE_SUPPORT"
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            **_fixture(support_mask=np.ones((2, 2), dtype=bool))
        )
    assert excinfo.value.reason == "DIMENSION_MISMATCH"

    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            **_fixture(support_mask=np.array([[0, 2, 0], [1, 0, 1], [1, 1, 0]]))
        )
    assert excinfo.value.reason == "INCONSISTENT_INPUT"


def test_wage_vector_dimension_mismatch_fails_closed():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            **_fixture(destination_wages=np.array([1.0, 2.0]))
        )
    assert excinfo.value.reason == "DIMENSION_MISMATCH"


def test_wage_vector_non_finite_fails_closed():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            **_fixture(destination_wages=np.array([1.0, np.nan, 2.0]))
        )
    assert excinfo.value.reason == "NON_FINITE"


def test_error_messages_carry_reason_prefix():
    with pytest.raises(m.LaborDestinationAccountingError) as excinfo:
        m.build_labor_destination_accounting(
            m=np.array([0.1, 0.2]), ell=np.array([1.0]), W=np.zeros((2, 2))
        )
    assert str(excinfo.value).startswith("[DIMENSION_MISMATCH]")


# --------------------------------------------------------------------------
# 14. import / static guard: no household / HJB / KFE / GE execution
# --------------------------------------------------------------------------
def test_module_imports_only_offline_safe_names():
    imported = _imported_names(MODULE_SOURCE)
    assert imported, "expected at least the numpy import"
    for name in imported:
        assert name in ALLOWED_IMPORT_NAMES, name
        for forbidden in FORBIDDEN_IMPORT_ROOTS:
            assert not name.startswith(forbidden), f"{name} imports forbidden {forbidden}"


def test_module_has_no_dynamic_import_or_file_access_calls():
    called = {
        node.func.id
        for node in ast.walk(TREE)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert called.isdisjoint({"__import__", "eval", "exec", "compile", "open"})


def test_test_file_does_not_import_forbidden_scientific_modules():
    imported = _imported_names(Path(__file__).read_text(encoding="utf-8"))
    for name in imported:
        assert not name.startswith("deep_learning_hank.two_asset"), name
        assert not name.startswith("matlab"), name


def test_module_never_references_household_or_solver_entrypoints():
    forbidden_symbols = (
        "solve_household_steady_state",
        "solve_matlab_faithful_hjb",
        "solve_matlab_faithful_stationary_kfe",
        "select_matlab_faithful_local_policy",
        "aggregate_stationary_household",
        "assemble_source_operator",
    )
    for symbol in forbidden_symbols:
        assert symbol not in MODULE_SOURCE, symbol


def test_subprocess_import_loads_no_household_hjb_kfe_or_ge_modules():
    """Independent-process proof that importing this module is inert."""
    code = (
        "import sys;"
        "import deep_learning_hank.regional.labor_destination;"
        "bad=[n for n in sys.modules if n.startswith('deep_learning_hank.two_asset')]"
        "+[n for n in ('scipy','torch','tensorflow','matlab','matlabengine')"
        " if n in sys.modules];"
        "print('FORBIDDEN=' + ','.join(sorted(bad)))"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    completed = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
        check=True,
    )
    assert "FORBIDDEN=" in completed.stdout
    assert completed.stdout.strip().endswith("FORBIDDEN="), completed.stdout


def test_allowlist_paths_and_untouched_scientific_modules():
    """The allowlist artefacts exist; the referenced scientific modules are intact."""
    assert MODULE_PATH.as_posix().endswith(
        "src/deep_learning_hank/regional/labor_destination.py"
    )
    assert (REPO_ROOT / "tests" / "test_dlh_wl_p1a_labor_destination.py").is_file()
    for relpath in (ORACLE_RELPATH, SELECTED_Q_RELPATH, KFE_RELPATH):
        assert (REPO_ROOT / relpath).is_file(), relpath
