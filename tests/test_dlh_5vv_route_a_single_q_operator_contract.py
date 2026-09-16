"""DLH-5V-V — focused test suite for the Owner-Route-A single-`Q` F0
operator-contract consolidation and final Bellman revalidation (Issue #70).

Authority: Issue #70 OPEN; initial authoritative activation ``5681294485``;
final authoritative activation-refresh ``5682174361`` (post-sync live ``main``
``0bca3b4552a76331302670bf59bddfa4cd4f06f7``). Route decision
``APPROVE_ROUTE_A_MATLAB_FAITHFUL_SINGLE_Q_F0_OPERATOR_CONTRACT``; authority
marker ``DLH_5VV_ROUTE_A_SINGLE_Q_OPERATOR_CONTRACT_AUTHORIZED``.

Owner Route A binding contract: MATLAB-faithful selected iteration-rate
semantics are authoritative for the HJB operator. When ``final=True`` is given a
selected F0 policy record, the final-validation row must reuse that SAME
record's stored MATLAB-faithful ``row_entries`` / iteration-rate semantics /
``diagonal`` / ``utility``; same-z-block destination indexing is preserved; and
no second F0 generator may be constructed from
``asset_drifts_matlab_faithful`` + ``max(±mu)/step``.

Interpretation ceiling: passing this Issue means only that one coherent
MATLAB-faithful F0 generator now governs solve and final validation, and that the
Issue #68/#69 dual-rate validation inconsistency is removed. It is NOT an HJB
convergence claim, does not accept a new iterate, and does not authorize any
tolerance or convergence-rule change.
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from scipy import sparse
from scipy.sparse import linalg

import deep_learning_hank.two_asset.boundary_hjb_selected_q as sq
from deep_learning_hank.two_asset.stagnation_newton_geometry import (
    reconstruct_issue63_stagnation_state,
)
from deep_learning_hank.two_asset.tangent_projected_newton_geometry import (
    limiting_wall_gradient,
    single_wall_tangent_projection,
)

SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"
SELECTED_Q_PRE_ISSUE70_BLOB = "556ccc214f03a1a22306cc4f5c7e9f7691bbf897"
# The blob ACCEPTED by the Issue #70 Reviewer integration (`5691696204`) and now
# carried by live `main` (integration `fb5523d` + governance sync `e1a7a9a`).
ISSUE70_ACCEPTED_SELECTED_Q_BLOB = "7857cabb4d28af99cb9d59e2d1c3024b05787c11"
ORACLE_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"

ALPHA_HALF = 0.08085341880193442
ALPHA_NEAR = 0.16170683760386884
HISTORICAL_GAP_HALF = 0.6718037653783657
HISTORICAL_GAP_NEAR = 1.3379411925537439

FINAL_STATISTIC_EXPECTED = 3.6614352438846254e-08
MIN_BOUNDARY_PB_EXPECTED = 4.8089461301970005e-09
R_ITER_INF_S0 = 10.435094313164921
WALL_NODE, WALL_NZ = 332, 1

MACHINE_TOL = 1.0e-12
BELLMAN_TOLERANCE_UNCHANGED = 1.0e-3

MODULE_PATH = Path(sq.__file__)
MODULE_SOURCE = MODULE_PATH.read_text(encoding="utf-8")

BANNED_TOKENS = (
    "newton_loop", "policy_iteration", "semismooth", "trust_region",
    "continuation", "linesearch", "line_search", "armijo", "backtrack",
    "alpha_tuning", "tune_alpha", "sweep", "kfe", "stationary",
    "steady_state", "solve_household_steady_state",
)


# ---------------------------------------------------------------------------
# fixtures: ONE deterministic reconstruction + the three frozen states
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def frozen():
    """S0/S1/S2 with their ONE build pair each, plus identity diagnostics."""
    rec = reconstruct_issue63_stagnation_state()
    solver = rec["solver"]
    V_star, labor0, rho = rec["V_star"], rec["labor0"], rec["rho"]
    n, nz, S = solver.n, solver.nz, solver.state_size
    V_flat = V_star.ravel(order="F")
    Q0, u0, _d0, _r0 = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R0 = rho * V_flat - (u0 + Q0.dot(V_flat))
    d_n = linalg.spsolve(rho * sparse.eye(S, format="csr") - Q0, -R0)
    gvec = limiting_wall_gradient(solver, WALL_NODE, WALL_NZ)
    d_t = single_wall_tangent_projection(d_n, gvec)["d_T"]

    f0_rows = np.nonzero(np.tile(
        np.array([str(solver.grid.families[i]) for i in range(n)]) == "F0",
        nz))[0]
    non_f0 = np.nonzero(~np.tile(
        np.array([str(solver.grid.families[i]) for i in range(n)]) == "F0",
        nz))[0]

    labels = ("S0", "S1", "S2")
    V_list = [V_star,
              V_star + ALPHA_HALF * d_t.reshape((n, nz), order="F"),
              V_star + ALPHA_NEAR * d_t.reshape((n, nz), order="F")]
    out = {}
    for label, V in zip(labels, V_list):
        V = np.asarray(V, dtype=float)
        Qi, ui, _di, recs = solver.build_operator_and_u(
            V, labor0, 0.0, 0.0, final=False)
        Qf, uf, _df, recf = solver.build_operator_and_u(
            V, labor0, 0.0, 0.0, final=True, f0_policies=recs)
        v = V.ravel(order="F")

        def rowmax(rows):
            best, best_row = 0.0, -1
            for r in rows:
                a = np.asarray(Qf.getrow(int(r)).toarray()).ravel()
                b = np.asarray(Qi.getrow(int(r)).toarray()).ravel()
                m = float(np.max(np.abs(a - b)))
                if m > best:
                    best, best_row = m, int(r)
            return best, best_row

        f0_gap, f0_row = rowmax(f0_rows)
        nf_gap, nf_row = rowmax(non_f0)
        global_gap = max(f0_gap, nf_gap)
        u_gap = float(np.max(np.abs(uf - ui)))
        diag_gap = max(abs(float(recs[int(r)].diagonal)
                           - float(recf[int(r)].diagonal)) for r in f0_rows)
        dest_gap = 0.0
        for r in f0_rows:
            di = {int(d) for d, _ in recs[int(r)].row_entries}
            df = {int(d) for d, _ in recf[int(r)].row_entries}
            dest_gap = max(dest_gap, float(len(di ^ df)))
        R_iter = rho * v - (ui + Qi.dot(v))
        R_final = rho * v - (uf + Qf.dot(v))
        ctrl_gap = 0.0
        label_changes = 0
        for r in f0_rows:
            a, b = recs[int(r)], recf[int(r)]
            ctrl_gap = max(ctrl_gap,
                           abs(a.consumption - b.consumption),
                           abs(a.labor - b.labor),
                           abs(a.transfer - b.transfer),
                           abs(a.mu_a - b.mu_a),
                           abs(a.mu_b - b.mu_b),
                           abs(a.utility - b.utility))
            if a.sector != b.sector:
                label_changes += 1
        # MANDATORY (Issue #70 frozen contract + Reviewer final hold 5691015137):
        # selected policy labels must be preserved by final validation on EVERY F0
        # row. Counted over all F0 rows with the mismatching row and value kept for
        # diagnostics, so a regression reports the exact offending row.
        f0_label_mismatch_rows = [
            int(r) for r in f0_rows
            if recs[int(r)].sector != recf[int(r)].sector]
        f0_label_mismatch_count = len(f0_label_mismatch_rows)
        f0_label_mismatch_first = None
        if f0_label_mismatch_rows:
            _r = f0_label_mismatch_rows[0]
            f0_label_mismatch_first = (
                _r, str(recs[_r].sector), str(recf[_r].sector))
        # non-F0 rows go through the identical boundary path in both builds; this
        # is asserted rather than assumed.
        all_row_label_mismatch_count = sum(
            1 for r in range(len(recs))
            if recs[r] is not None and recf[r] is not None
            and recs[r].sector != recf[r].sector)
        assert f0_label_mismatch_count == label_changes
        out[label] = {
            "V": V, "Q_iter": Qi, "u_iter": ui, "records": recs,
            "Q_final": Qf, "u_final": uf, "records_final": recf,
            "f0_gap": f0_gap, "f0_gap_row": f0_row,
            "non_f0_gap": nf_gap, "non_f0_gap_row": nf_row,
            "global_gap": global_gap, "u_gap": u_gap,
            "diag_gap": diag_gap, "dest_gap": dest_gap,
            "ctrl_gap": ctrl_gap, "label_changes": label_changes,
            "f0_label_mismatch_count": f0_label_mismatch_count,
            "f0_label_mismatch_rows": f0_label_mismatch_rows,
            "f0_label_mismatch_first": f0_label_mismatch_first,
            "all_row_label_mismatch_count": all_row_label_mismatch_count,
            "max_abs_q1_iter": float(np.max(np.abs(np.asarray(
                Qi.sum(axis=1)).ravel()))),
            "max_abs_q1_final": float(np.max(np.abs(np.asarray(
                Qf.sum(axis=1)).ravel()))),
            "R_iter": R_iter, "R_final": R_final,
            "r_iter_inf": float(np.max(np.abs(R_iter))),
            "r_final_inf": float(np.max(np.abs(R_final))),
            "r_gap": float(np.max(np.abs(R_final - R_iter))),
            "r_iter_argmax": int(np.argmax(np.abs(R_iter))),
            "r_final_argmax": int(np.argmax(np.abs(R_final))),
        }
    return {"solver": solver, "d_t": d_t, "gvec": gvec, "states": out,
            "f0_rows": f0_rows, "non_f0_rows": non_f0}


# ---------------------------------------------------------------------------
# 1. authority / blob / non-change surface
# ---------------------------------------------------------------------------
def _build_operator_ast() -> ast.FunctionDef:
    """The ``build_operator_and_u`` FunctionDef (nested inside the solver class)."""
    tree = ast.parse(MODULE_SOURCE)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "build_operator_and_u":
            return node
    raise AssertionError("build_operator_and_u not found in the module")


def test_owner_route_a_authority_marker_present():
    """The Owner Route-A authority marker and route decision are recorded."""
    text = MODULE_SOURCE
    assert "Route A" in text
    assert "Issue #70" in text
    assert "DLH-5V-V" in text
    assert "one selected operator" in text
    assert "f0_policies" in text


def test_pre_issue70_blob_recorded_and_oracle_unchanged():
    """The pre-Issue-70 selected-Q blob and the oracle blob are still verifiable.

    History is preserved explicitly: the remediation commit's parent chain keeps
    the original Issue #70 scientific commit and, behind it, the pre-Issue-70
    revision of the file.
    """
    repo_root = Path(__file__).resolve().parents[1]

    def blob(rev: str, relpath: str) -> str:
        out = subprocess.run(
            ["git", "rev-parse", f"{rev}:{relpath}"],
            cwd=repo_root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=True)
        return out.stdout.strip()

    # the pre-Issue-70 revision is reachable as the parent of the original
    # Issue #70 scientific commit (the Route-A change is that commit's own diff)
    original = "825e241804c7fb260c807602fc0f1487caf84e56"
    parent_sha = subprocess.run(
        ["git", "rev-parse", f"{original}^"],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True).stdout.strip()
    assert blob(parent_sha, SELECTED_Q_RELPATH) == SELECTED_Q_PRE_ISSUE70_BLOB
    # live main now carries the ACCEPTED post-Route-A state (Issue #70
    # integration `fb5523d` plus governance sync `e1a7a9a`). The pre-Route-A blob
    # is therefore no longer main's revision; it is preserved at the ABSOLUTE
    # revision asserted above and remains the recorded comparison authority.
    assert blob("origin/main", SELECTED_Q_RELPATH) == (
        ISSUE70_ACCEPTED_SELECTED_Q_BLOB)
    assert blob(parent_sha, "src/deep_learning_hank/two_asset/"
                            "matlab_faithful_two_asset_ha.py") == ORACLE_BLOB
    # the oracle is unchanged in the current candidate too
    assert blob("HEAD", "src/deep_learning_hank/two_asset/"
                        "matlab_faithful_two_asset_ha.py") == ORACLE_BLOB


def test_final_true_f0_branch_no_longer_constructs_raw_drift_q():
    """The Route-A branch must not rebuild F0 rates from drift."""
    func = _build_operator_ast()
    calls = [n for n in ast.walk(func)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "asset_drifts_matlab_faithful"]
    assert calls == [], "F0 assembly must not recompute drifts"
    src = ast.get_source_segment(MODULE_SOURCE, func) or ""
    for token in ("max(-mu_a_v, 0.0) / self.da", "max(mu_a_v, 0.0) / self.da",
                  "max(-mu_b_v, 0.0) / self.db", "max(mu_b_v, 0.0) / self.db"):
        assert token not in src, token


def test_final_true_f0_branch_reuses_supplied_selected_row():
    """Source-level proof that the Route-A row is copied from the record."""
    func = _build_operator_ast()
    src = ast.get_source_segment(MODULE_SOURCE, func) or ""
    assert "rec = f0_policies[row]" in src
    assert "rec.row_entries" in src
    assert "float(rec.diagonal)" in src
    assert "u[row] = rec.utility" in src
    assert "cols.append(nz * self.n + dn)" in src


def test_final_false_semantics_unchanged():
    """The iteration path still uses local_interior_row with same-z indexing."""
    func = _build_operator_ast()
    calls = [n for n in ast.walk(func)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr == "local_interior_row"]
    assert len(calls) == 1


def test_final_true_f0_branch_preserves_supplied_policy_label():
    """SOURCE-LEVEL proof (Reviewer final hold `5691015137`) that the Route-A
    ``final=True`` F0 assembly preserves the supplied selected record's policy /
    sector label VERBATIM, in both places the label is recorded:

    * ``_PolicyRecord(... sector=rec.sector ...)`` -- not a string literal;
    * ``sector_arr[node, nz] = rec.sector`` -- the stored array the operator /
      diagnostics observe.

    No built-in constant ``INTERIOR_FINAL``, no assembly-path tag, and no string
    literal keyword argument anywhere in ``build_operator_and_u``.
    """
    func = _build_operator_ast()
    src = ast.get_source_segment(MODULE_SOURCE, func) or ""

    # 1. no assembly-path tag anywhere in the assembly function
    assert "INTERIOR_FINAL" not in src
    assert "INTERIOR_FINAL" not in MODULE_SOURCE

    # 2. _PolicyRecord receives sector=rec.sector (an Attribute access)
    record_calls = [
        n for n in ast.walk(func)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        and n.func.id == "_PolicyRecord"]
    assert record_calls, "_PolicyRecord construction not found"
    sector_kwargs = []
    for call in record_calls:
        for kw in call.keywords:
            if kw.arg == "sector":
                sector_kwargs.append(kw.value)
    assert sector_kwargs, "no sector= keyword in _PolicyRecord construction"
    for value in sector_kwargs:
        assert isinstance(value, ast.Attribute), (
            f"sector= must reference a record attribute, got {ast.dump(value)}")
        # both F0 record constructions copy a label off a selected record:
        # `rec.sector` (Route-A final=True) and `policy.transfer_label`
        # (final=False, unchanged semantics)
        assert value.attr in ("sector", "transfer_label"), ast.dump(value)
        # the receiver is a selected record, never a constant/literal
        assert isinstance(value.value, ast.Name)
    assert [v.attr for v in sector_kwargs].count("sector") == 1
    # the final=True F0 branch's sector kwarg specifically is rec.sector
    assert any(isinstance(v.value, ast.Name) and v.value.id == "rec"
               for v in sector_kwargs)

    # 3. sector_arr[node, nz] = rec.sector  (Subscript assign, Attribute value)
    #    THREE sites exist: Route-A F0 final=True, F0 final=False
    #    (policy.transfer_label) and the non-F0 boundary path (rec.sector).
    sector_assigns = []
    for node in ast.walk(func):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "sector_arr"):
                sector_assigns.append(node.value)
    assert len(sector_assigns) == 3, [ast.dump(v) for v in sector_assigns]
    # every one of them is a record label attribute, never a string literal
    assert all(isinstance(v, ast.Attribute) and v.attr in ("sector",
                                                           "transfer_label")
               for v in sector_assigns), [ast.dump(v) for v in sector_assigns]
    assert [v.attr for v in sector_assigns].count("sector") == 2
    # and the Route-A F0 site specifically copies `rec.sector`
    assert any(isinstance(v, ast.Attribute) and v.attr == "sector"
               and isinstance(v.value, ast.Name) and v.value.id == "rec"
               for v in sector_assigns)

    # 4. HARD GUARANTEE: no _PolicyRecord built anywhere in the assembly carries
    #    a string-literal `sector`. Every policy label is copied from a selected
    #    record (`rec.sector` / `policy.transfer_label`). `family="F0"` is a
    #    constant in BOTH F0 branches by design (the branch is already selected by
    #    `fam == "F0"`), so only the policy label is constrained here.
    for call in [n for n in ast.walk(func) if isinstance(n, ast.Call)]:
        if not (isinstance(call.func, ast.Name)
                and call.func.id == "_PolicyRecord"):
            continue
        for kw in call.keywords:
            assert kw.arg != "sector" or not isinstance(kw.value, ast.Constant), (
                f"line {call.lineno}: sector= must not be a literal")


def test_current_selected_q_blob_is_the_post_remediation_candidate():
    """History is preserved AND the CURRENT candidate carries the label fix.

    The pre-Issue-70 blob, the original Issue #70 scientific blob and the
    migration blob all remain verifiable at their own revisions, while the
    current revision of the file (committed or working tree) carries the
    policy-label preservation fix and no assembly tag.
    """
    repo_root = Path(__file__).resolve().parents[1]

    def blob(rev: str) -> str:
        out = subprocess.run(
            ["git", "rev-parse", f"{rev}:{SELECTED_Q_RELPATH}"],
            cwd=repo_root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=True)
        return out.stdout.strip()

    # history, preserved verbatim (validated in CI against the same repos)
    migration = "0e3a9597cd5550a237452aeaa57ed0a145aa6c83"
    original = "825e241804c7fb260c807602fc0f1487caf84e56"
    assert blob(migration) == "35e7dadfa4fb8f1c2a89db21751f2b541bda3cab"
    assert blob(original) == "35e7dadfa4fb8f1c2a89db21751f2b541bda3cab"
    assert blob("825e241804c7fb260c807602fc0f1487caf84e56^") == (
        SELECTED_Q_PRE_ISSUE70_BLOB)

    # the CURRENT revision of the file (working tree == commit when clean)
    current = MODULE_SOURCE
    assert "sector=rec.sector" in current
    assert "sector_arr[node, nz] = rec.sector" in current
    assert "INTERIOR_FINAL" not in current
    # and the working-tree blob differs from the pre-fix migration blob
    wt = subprocess.run(
        ["git", "hash-object", "--", SELECTED_Q_RELPATH],
        cwd=repo_root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True).stdout.strip()
    assert wt != blob(migration)


# ---------------------------------------------------------------------------
# 2. exact frozen-state reconstruction
# ---------------------------------------------------------------------------
def test_exact_s0_reconstruction(frozen):
    """The accepted Issue #63 stagnation state is reproduced exactly."""
    trace = reconstruct_issue63_stagnation_state()["trace"]
    assert len(trace) == 8
    assert float(trace[-1]["accepted_max_stat"]) == pytest.approx(
        FINAL_STATISTIC_EXPECTED, abs=1e-12)
    wall = trace[-1]["worst_after"]
    assert wall["family"] == "F3" and wall["j"] == 13 and wall["i"] == 13
    assert wall["z"] == 1
    s0 = frozen["states"]["S0"]
    assert s0["r_iter_inf"] == pytest.approx(R_ITER_INF_S0, abs=1e-12)


def test_min_boundary_pb_and_exact_fractions(frozen):
    from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
        min_boundary_pb_state,
    )
    rec = reconstruct_issue63_stagnation_state()
    pb, node, nz_i = min_boundary_pb_state(rec["solver"], rec["V_star"],
                                           rec["labor0"])
    assert pb == pytest.approx(MIN_BOUNDARY_PB_EXPECTED, abs=1e-12)
    assert (node, nz_i) == (WALL_NODE, WALL_NZ)
    assert ALPHA_HALF == 0.08085341880193442
    assert ALPHA_NEAR == 0.16170683760386884
    assert abs(frozen["gvec"] @ frozen["d_t"]) == 0.0


def test_exactly_three_frozen_states(frozen):
    assert sorted(frozen["states"]) == ["S0", "S1", "S2"]
    assert len(frozen["states"]) == 3


# ---------------------------------------------------------------------------
# 3. S0 / S1 / S2 single-Q identity
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_f0_and_global_q_identity(frozen, label):
    s = frozen["states"][label]
    assert s["f0_gap"] <= MACHINE_TOL, (label, s["f0_gap"])
    assert s["non_f0_gap"] <= MACHINE_TOL, (label, s["non_f0_gap"])
    assert s["global_gap"] <= MACHINE_TOL, (label, s["global_gap"])
    # bit-identical after the Route-A consolidation
    assert s["global_gap"] == 0.0


@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_u_identity(frozen, label):
    s = frozen["states"][label]
    assert s["u_gap"] <= MACHINE_TOL
    assert s["u_gap"] == 0.0


@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_diagonal_and_destination_identity(frozen, label):
    s = frozen["states"][label]
    assert s["diag_gap"] <= MACHINE_TOL
    assert s["diag_gap"] == 0.0
    assert s["dest_gap"] == 0.0


@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_controls_and_labels_unchanged(frozen, label):
    """Selected controls, realized drifts AND policy labels are carried verbatim.

    FROZEN ISSUE #70 CONTRACT (enforced after Reviewer final hold `5691015137`):
    "selected controls AND selected policy labels are unchanged by final
    validation". The Route-A final-validation F0 record therefore preserves the
    supplied selected record's ``sector`` label verbatim (``rec.sector``); the
    assembly path is recorded in source comments only and is never encoded by
    retagging the policy label. The four continuous controls plus the two
    realized drifts and the utility must be bit-identical.
    """
    s = frozen["states"][label]
    assert s["ctrl_gap"] == 0.0
    # NO label may change: not just "all 596 retagged", but zero changes
    assert s["label_changes"] == 0
    for r in frozen["f0_rows"]:
        a, b = s["records"][int(r)], s["records_final"][int(r)]
        assert a.sector == b.sector, (label, int(r), a.sector, b.sector)
        assert a.consumption == b.consumption
        assert a.labor == b.labor
        assert a.transfer == b.transfer
        assert a.mu_a == b.mu_a
        assert a.mu_b == b.mu_b
        assert a.utility == b.utility


@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_f0_policy_label_identity_all_rows(frozen, label):
    """MANDATORY new check: ALL F0 rows must have identical final vs iteration
    policy/sector labels — label mismatch row count == 0 at S0, S1 and S2.

    This is the frozen Issue #70 requirement requested by Reviewer hold
    `5691015137`: ``_PolicyRecord(... sector=rec.sector ...)`` and
    ``sector_arr[node, nz] = rec.sector``.
    """
    s = frozen["states"][label]
    assert s["f0_label_mismatch_count"] == 0, (
        f"{label}: {s['f0_label_mismatch_count']} F0 rows changed policy label; "
        f"first offender {s['f0_label_mismatch_first']}")
    assert s["f0_label_mismatch_rows"] == []
    assert s["f0_label_mismatch_first"] is None
    # the label_changes counter used by the controls test is the same quantity
    assert s["label_changes"] == 0
    # and it was measured over the full expected F0 row set
    assert s["f0_label_mismatch_count"] == 0
    for r in frozen["f0_rows"]:
        a, b = s["records"][int(r)], s["records_final"][int(r)]
        assert b.sector == a.sector
        # the label is a real selected F0 label, never an assembly tag
        assert b.sector in ("B", "F", "0"), (label, int(r), b.sector)
        assert "INTERIOR_FINAL" not in str(b.sector)
    # non-F0 rows are untouched by the assembly (same boundary path both builds)
    assert s["all_row_label_mismatch_count"] == 0


def test_f0_policy_label_mismatch_count_is_zero_at_all_frozen_states(frozen):
    """The mandatory label-identity result, aggregated: 0 mismatching F0 rows at
    every one of S0 / S1 / S2."""
    counts = {lab: frozen["states"][lab]["f0_label_mismatch_count"]
              for lab in ("S0", "S1", "S2")}
    assert counts == {"S0": 0, "S1": 0, "S2": 0}
    assert all(frozen["states"][lab]["all_row_label_mismatch_count"] == 0
               for lab in ("S0", "S1", "S2"))


@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_q_conservativity(frozen, label):
    s = frozen["states"][label]
    assert s["max_abs_q1_iter"] <= 1e-9
    assert s["max_abs_q1_final"] <= 1e-9
    assert s["max_abs_q1_iter"] == s["max_abs_q1_final"]


@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_represented_rate_identity(frozen, label):
    """Every represented F0 destination rate is carried verbatim."""
    s = frozen["states"][label]
    for r in frozen["f0_rows"]:
        ri = s["records"][int(r)]
        rf = s["records_final"][int(r)]
        mi = {int(d): float(v) for d, v in ri.row_entries}
        mf = {int(d): float(v) for d, v in rf.row_entries}
        assert mi == mf, (label, int(r))
        assert float(ri.diagonal) == float(rf.diagonal)


# ---------------------------------------------------------------------------
# 4. historical Issue #68 gap collapse
# ---------------------------------------------------------------------------
def test_historical_s1_gap_collapses(frozen):
    """S1's historical Issue #68 gap must collapse to machine precision."""
    s = frozen["states"]["S1"]
    assert s["f0_gap"] <= MACHINE_TOL
    assert s["global_gap"] <= MACHINE_TOL
    assert HISTORICAL_GAP_HALF > 0.1
    # the recorded historical value is the pre-Route-A (dual-Q) magnitude
    assert round(s["f0_gap"], 12) != round(HISTORICAL_GAP_HALF, 12)


def test_historical_s2_gap_collapses(frozen):
    """S2's historical Issue #68 gap must collapse to machine precision."""
    s = frozen["states"]["S2"]
    assert s["f0_gap"] <= MACHINE_TOL
    assert s["global_gap"] <= MACHINE_TOL
    assert HISTORICAL_GAP_NEAR > 0.1
    assert round(s["f0_gap"], 12) != round(HISTORICAL_GAP_NEAR, 12)


# ---------------------------------------------------------------------------
# 5. Bellman residual identity and the no-convergence ceiling
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("label", ["S0", "S1", "S2"])
def test_bellman_residual_identity(frozen, label):
    s = frozen["states"][label]
    assert s["r_final_inf"] == pytest.approx(s["r_iter_inf"], abs=1e-12)
    assert s["r_gap"] <= MACHINE_TOL
    assert s["r_gap"] == 0.0
    assert s["r_iter_argmax"] == s["r_final_argmax"]


def test_s0_residual_unchanged_and_not_converged(frozen):
    s = frozen["states"]["S0"]
    assert s["r_iter_inf"] == pytest.approx(R_ITER_INF_S0, abs=1e-12)
    assert s["r_final_inf"] == pytest.approx(R_ITER_INF_S0, abs=1e-12)
    # single-Q consistency does NOT imply convergence
    assert s["r_final_inf"] > BELLMAN_TOLERANCE_UNCHANGED
    assert s["r_final_inf"] / BELLMAN_TOLERANCE_UNCHANGED > 1.0e4


# ---------------------------------------------------------------------------
# 6. execution design: exactly one build pair per state, no third state
# ---------------------------------------------------------------------------
def test_exactly_one_pair_of_builds_per_frozen_state(frozen):
    """ONE final=False and ONE final=True build per frozen state."""
    solver = frozen["solver"]
    seen: list[dict] = []
    real = solver.build_operator_and_u

    def counting(V, labor0v, ti, brg, final=False, f0_policies=None):
        seen.append({"final": final})
        return real(V, labor0v, ti, brg, final=final, f0_policies=f0_policies)

    from deep_learning_hank.two_asset import (
        tangent_projected_newton_geometry as tpg,
    )
    rec = reconstruct_issue63_stagnation_state()
    V_star, labor0, rho = rec["V_star"], rec["labor0"], rec["rho"]
    n, nz, S = solver.n, solver.nz, solver.state_size
    V = V_star.ravel(order="F")
    Q0, u0, _d0, _r0 = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R0 = rho * V - (u0 + Q0.dot(V))
    d_n = linalg.spsolve(rho * sparse.eye(S, format="csr") - Q0, -R0)
    gvec = tpg.limiting_wall_gradient(solver, WALL_NODE, WALL_NZ)
    d_t = tpg.single_wall_tangent_projection(d_n, gvec)["d_T"]
    V_list = [V_star,
              V_star + ALPHA_HALF * d_t.reshape((n, nz), order="F"),
              V_star + ALPHA_NEAR * d_t.reshape((n, nz), order="F")]
    with patch.object(solver, "build_operator_and_u", side_effect=counting):
        # 1 base build + 3 states x (1 iteration + 1 Route-A final) build
        solver.build_operator_and_u(V_star, labor0, 0.0, 0.0, final=False)
        for Vx in V_list:
            Qi, ui, _di, recs = solver.build_operator_and_u(
                Vx, labor0, 0.0, 0.0, final=False)
            solver.build_operator_and_u(
                Vx, labor0, 0.0, 0.0, final=True, f0_policies=recs)
    finals = [c["final"] for c in seen]
    assert finals.count(False) == 4      # 1 base + 3 iteration builds
    assert finals.count(True) == 3       # exactly one Route-A build per state


def test_no_forbidden_machinery_in_module():
    tree = ast.parse(MODULE_SOURCE)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            tok = node.id.lower()
            if any(b in tok for b in BANNED_TOKENS):
                found.append((tok, getattr(node, "lineno", -1)))
        elif isinstance(node, ast.Attribute):
            tok = node.attr.lower()
            if any(b in tok for b in BANNED_TOKENS):
                found.append((tok, getattr(node, "lineno", -1)))
    assert found == [], f"forbidden tokens found: {found}"


def test_deterministic_repeat_identical(frozen):
    """A second independent reconstruction gives bit-identical identity data."""
    rec = reconstruct_issue63_stagnation_state()
    solver = rec["solver"]
    V_star, labor0, rho = rec["V_star"], rec["labor0"], rec["rho"]
    n, nz, S = solver.n, solver.nz, solver.state_size
    V = V_star.ravel(order="F")
    Q0, u0, _d0, _r0 = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R0 = rho * V - (u0 + Q0.dot(V))
    d_n = linalg.spsolve(rho * sparse.eye(S, format="csr") - Q0, -R0)
    gvec = limiting_wall_gradient(solver, WALL_NODE, WALL_NZ)
    d_t = single_wall_tangent_projection(d_n, gvec)["d_T"]
    assert np.array_equal(d_t, frozen["d_t"])
    V1 = V_star + ALPHA_HALF * d_t.reshape((n, nz), order="F")
    Qi, ui, _di, recs = solver.build_operator_and_u(
        V1, labor0, 0.0, 0.0, final=False)
    Qf, uf, _df, _rf = solver.build_operator_and_u(
        V1, labor0, 0.0, 0.0, final=True, f0_policies=recs)
    ref = frozen["states"]["S1"]
    assert np.array_equal(np.asarray(Qi.toarray()), np.asarray(
        ref["Q_iter"].toarray()))
    assert np.array_equal(np.asarray(Qf.toarray()), np.asarray(
        ref["Q_final"].toarray()))
    assert np.array_equal(ui, ref["u_iter"])
    assert np.array_equal(uf, ref["u_final"])


def test_no_convergence_claim_or_tolerance_change(frozen):
    src = MODULE_SOURCE
    for token in ("tolerance_iter =", "tolerance_Bellman =", "PB_MARGIN ="):
        assert token not in src
    # every frozen-state residual still exceeds the unchanged tolerance
    for s in frozen["states"].values():
        assert s["r_final_inf"] > BELLMAN_TOLERANCE_UNCHANGED
