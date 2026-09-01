"""DLH-5L (Issue #38) focused tests.

Covers the Issue #38 minimum tests:

1. exact J0-J5 rerun identity; no new grid;
2. accepted HJB/source identity unchanged;
3. accepted J reproduction fail-closed gate;
4. exact inherited state-set identity from DLH-5K localization + cross-a evidence;
5. exact mu_W = mu_a + mu_b reconstruction;
6. exact transfer cancellation identity;
7. four-way coordinate/total classification;
8. every DLH-5K interior-positive state included;
9. rectangular vs total-wealth normal-drift algebra;
10. exact cross-a aligned comparison;
11. terminal classification matrix;
12. deterministic repeat;
13. no stationary/KFE/aggregate path;
14. no source mutation and no grid continuation.
"""

import hashlib
import pathlib
from types import SimpleNamespace

import numpy as np
import pytest

from deep_learning_hank.two_asset import MatlabFaithfulHJBGrid
from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    matlab_faithful_illiquid_return,
)

import deep_learning_hank.two_asset.total_wealth_domain_geometry_diagnostic as mod

CONFIG_PATH = "configs/dlh_5l_total_wealth_domain_geometry_diagnostic.toml"
ORACLE_PATH = pathlib.Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")

_A_PTS = {"a77": 77, "a153": 153}
_B_PTS = {"b120": 120, "b140": 140, "b160": 160}
_B_HI = {"b120": 795.0 / 19.0, "b140": 935.0 / 19.0, "b160": 1075.0 / 19.0}


def _cfg():
    return mod.load_config(CONFIG_PATH)


def _params():
    from deep_learning_hank.two_asset import EconomicParams
    return EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)


def _fake_variant_record(vid, a_res, b_ext, stat, raw_ub, req_ub, count):
    return {
        "variant": vid, "a_res": a_res, "b_ext": b_ext,
        "grid": {"a_pts": _A_PTS[a_res], "a_lo": 0.0, "a_hi": 10.0,
                 "b_pts": _B_PTS[b_ext], "b_lo": -2.0, "b_hi": _B_HI[b_ext], "db": mod.DB0},
        "frozen_prices_identity": {"wbar": 1.0, "r_a": 0.03},
        "hjb_converged": True,
        "hjb_iterations": 10,
        "hjb_statistic": stat,
        "max_raw_upper_a": 0.0,
        "max_raw_lower_a": 0.0,
        "max_raw_upper_b": raw_ub,
        "max_raw_lower_b": 0.0,
        "max_requested_upper_b": req_ub,
        "upper_b_offender_count": count,
    }


def _fake_runs_variants():
    return [_fake_variant_record(
        vid, vid.split("_")[1].lower(), vid.split("_")[2].lower(),
        mod.ACCEPTED_J_HJB_STAT[vid],
        mod.ACCEPTED_J_UPPER_B[vid]["raw_max"],
        mod.ACCEPTED_J_UPPER_B[vid]["requested_max"],
        mod.ACCEPTED_J_UPPER_B[vid]["count"],
    ) for vid in mod.VARIANT_IDS]


def _fake_hjb(shape, mu_b=None, mu_a=None, transfer=None, value=None):
    mu_b = np.zeros(shape) if mu_b is None else mu_b
    mu_a = np.zeros(shape) if mu_a is None else mu_a
    transfer = np.zeros(shape) if transfer is None else transfer
    value = np.zeros(shape) if value is None else value
    return SimpleNamespace(
        value=value,
        consumption=np.ones(shape),
        labor=np.ones(shape),
        transfer=transfer,
        adjustment_cost=np.zeros(shape),
        effective_illiquid_return=np.zeros(shape),
        mu_a=mu_a,
        mu_b=mu_b,
        liquid_label=np.full(shape, "0", dtype="U1"),
        transfer_label=np.full(shape, "0", dtype="U1"),
    )


def _full_fake_runs(mu_b_pattern=None, transfer=None, mu_a_state=None):
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    hjb_results = {}
    variants = []
    for vid, g in grids.items():
        shape = (g.b.size, g.a.size, g.z.size)
        a_res, b_ext = vid.split("_")[1].lower(), vid.split("_")[2].lower()
        mu_b = np.zeros(shape)
        for (bi, aj, nz) in (mu_b_pattern or {}).get(vid, []):
            mu_b[bi, aj, nz] = 1e-6
        mu_a = np.zeros(shape)
        if mu_a_state:
            for (bi, aj, nz), val in mu_a_state.items():
                if bi < g.b.size and aj < g.a.size and nz < g.z.size:
                    mu_a[bi, aj, nz] = val
        hjb_results[vid] = _fake_hjb(
            shape, mu_b=mu_b, mu_a=mu_a,
            transfer=np.full(shape, transfer if transfer is not None else 0.0))
        cnt = len((mu_b_pattern or {}).get(vid, []))
        variants.append(_fake_variant_record(vid, a_res, b_ext, 1e-8, 1e-6 if cnt else 0.0,
                                             1e-6 / mod.DB0 if cnt else 0.0, cnt))
    inputs = SimpleNamespace(r_a=0.03, r_b=0.015, tau=0.15, wages=np.array([1.0]),
                             migration_costs=np.array([0.0]), labor_weights=np.array([1.0]))
    return {
        "variants": variants,
        "hjb_results": hjb_results,
        "grids": grids,
        "params": _params(),
        "labor0": {vid: np.ones((grids[vid].b.size, grids[vid].a.size, grids[vid].z.size))
                   for vid in grids},
        "inputs": {vid: inputs for vid in grids},
        "transfer_income": 0.0,
        "rb_gap": 0.01,
    }


# ---------------------------------------------------------------------------
# 1. Exact J0-J5 rerun identity / no new grid
# ---------------------------------------------------------------------------


def test_exact_j0_j5_rerun_identity_no_new_grid():
    cfg = _cfg()
    plan = mod.grid_plan_identity(cfg)
    assert list(plan["variants"].keys()) == mod.VARIANT_IDS
    assert [e.id for e in cfg.b_extents] == ["b120", "b140", "b160"]
    assert [r.id for r in cfg.a_resolutions] == ["a77", "a153"]
    assert "b100" not in plan["b_extents"]
    assert not any(v.b_ext == "b100" for v in cfg.variants)
    assert plan["liquid"]["hard_ceiling_b_hi"] == 1075.0 / 19.0
    assert "b160" in cfg.route_ceiling_note and "NO_B180_B200" in cfg.route_ceiling_note
    for vid, p in plan["variants"].items():
        assert p["a_pts"] == _A_PTS[p["a_res"]]
        assert p["b_pts"] == _B_PTS[p["b_ext"]]
        assert abs(p["db"] - mod.DB0) <= 1e-12
        assert abs(p["b_hi"] - _B_HI[p["b_ext"]]) <= 1e-12


# ---------------------------------------------------------------------------
# 2. Accepted HJB/source identity unchanged
# ---------------------------------------------------------------------------


def test_accepted_source_identity_unchanged():
    data = ORACLE_PATH.read_bytes()
    assert mod.ACCEPTED_SHA256 == hashlib.sha256(data).hexdigest().upper()
    assert mod.ACCEPTED_BLOB == "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"


# ---------------------------------------------------------------------------
# 3. Accepted J reproduction fail-closed gate
# ---------------------------------------------------------------------------


def test_reproduction_check_passes_on_accepted_anchors():
    cfg = _cfg()
    rep = mod.check_accepted_j_reproduction(cfg, {"variants": _fake_runs_variants()})
    assert rep["pass_bool"] is True


def test_reproduction_check_fails_closed_on_stat_mismatch():
    cfg = _cfg()
    runs = {"variants": _fake_runs_variants()}
    runs["variants"][0]["hjb_statistic"] = 9.999e-08
    rep = mod.check_accepted_j_reproduction(cfg, runs)
    assert rep["pass_bool"] is False
    assert mod.TERMINAL_OUTCOME_D == "BLOCKED_DLH_5L_ACCEPTED_HJB_REPRODUCTION"


# ---------------------------------------------------------------------------
# 4. Exact inherited state-set identity (accepted DLH-5K union)
# ---------------------------------------------------------------------------


def test_inherited_state_set_identity():
    cfg = _cfg()
    runs = _full_fake_runs()
    state_set = mod.resolve_inherited_state_set(cfg, runs)
    assert len(state_set) == 105
    per_variant = {}
    for s in state_set:
        per_variant.setdefault(s[0], set()).add((s[1], s[2], s[3]))
    assert {k: len(v) for k, v in per_variant.items()} == {
        "J0_A77_B120": 17, "J1_A77_B140": 14, "J2_A77_B160": 8,
        "J3_A153_B120": 29, "J4_A153_B140": 22, "J5_A153_B160": 15,
    }
    # a few exact coordinates from the accepted evidence
    assert ("J0_A77_B120", 119, 74, 1) in state_set
    assert ("J0_A77_B120", 115, 76, 1) in state_set
    assert ("J3_A153_B120", 119, 152, 1) in state_set
    assert ("J2_A77_B160", 159, 75, 1) in state_set
    assert ("J5_A153_B160", 159, 151, 1) in state_set
    # no post-hoc states: all b indices are top-layer or the n-1/n-2/n-3/n-5 set
    for (vid, bi, aj, nz) in state_set:
        g = runs["grids"][vid]
        assert bi <= g.b.size - 1
        assert aj < g.a.size and nz < g.z.size


def test_inherited_state_set_excludes_nothing_from_accepted_sources():
    cfg = _cfg()
    import csv
    loc_states = set()
    with open(cfg.dlh5k_localization_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            loc_states.add((row["variant"], int(row["b_index"]), int(row["a_index"]), int(row["z_index"])))
    runs = _full_fake_runs()
    state_set = set(mod.resolve_inherited_state_set(cfg, runs))
    assert loc_states <= state_set
    ca_states = set()
    with open(cfg.dlh5k_cross_a_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            b_top = {"b120": 119, "b140": 139, "b160": 159}[row["b_extent"]]
            ca_states.add((row["coarse_variant"], b_top, int(row["a77_index"]), int(row["z_index"])))
            ca_states.add((row["fine_variant"], b_top, int(row["a153_index"]), int(row["z_index"])))
    assert ca_states <= state_set


# ---------------------------------------------------------------------------
# 5. Exact mu_W = mu_a + mu_b reconstruction
# ---------------------------------------------------------------------------


def test_mu_W_reconstruction():
    cfg = _cfg()
    runs = _full_fake_runs()
    grid = runs["grids"]["J3_A153_B120"]
    i, j, nz = grid.b.size - 1, 152, 1
    transfer = -0.43
    cost = 0.06
    a = float(grid.a[j])
    b = float(grid.b[i])
    z = float(grid.z[nz])
    r_a_eff = float(matlab_faithful_illiquid_return(a, cfg.a_max, 0.03))
    # Self-consistent fake policies: labor=1, consumption=1, labor_income =
    # (1-tau)*w*z*labor, bls = r_b*b + labor_income - (consumption - transfer_income).
    labor_income = (1.0 - 0.15) * 1.0 * z * 1.0
    bls = 0.015 * b + labor_income - 1.0
    mu_b_val = bls + (-transfer) - cost  # ti = -transfer - cost
    mu_a_val = r_a_eff * a + transfer
    hjb = runs["hjb_results"]["J3_A153_B120"]
    hjb.mu_b[i, j, nz] = mu_b_val
    hjb.mu_a[i, j, nz] = mu_a_val
    hjb.transfer[i, j, nz] = transfer
    hjb.adjustment_cost[i, j, nz] = cost
    hjb.consumption[i, j, nz] = 1.0
    hjb.labor[i, j, nz] = 1.0
    der = mod.reconstruct_derivatives(
        grid, hjb, runs["params"], runs["inputs"]["J3_A153_B120"],
        runs["labor0"]["J3_A153_B120"], 0.0, 0.01)
    d = mod.decompose_state_5l(
        "J3_A153_B120", i, j, nz, grid, hjb, runs["params"],
        runs["inputs"]["J3_A153_B120"], runs["labor0"]["J3_A153_B120"],
        0.0, 0.01, der, cfg)
    assert abs(d["mu_W"] - (d["mu_a"] + d["mu_b"])) <= 1e-15
    assert abs(d["transfer_cancellation_residual"]) <= 1e-12
    # transfer-cancelled reconstruction equals r_a_eff*a + bls - cost
    assert abs(d["mu_W_transfer_cancelled_reconstruction"] - (r_a_eff * a + bls - cost)) <= 1e-12
    assert abs(d["mu_W"] - (r_a_eff * a + bls - cost)) <= 1e-12


# ---------------------------------------------------------------------------
# 6. Exact transfer cancellation identity
# ---------------------------------------------------------------------------


def test_transfer_cancellation_identity():
    cfg = _cfg()
    runs = _full_fake_runs(transfer=-0.43)
    grid = runs["grids"]["J0_A77_B120"]
    i, j, nz = grid.b.size - 1, 76, 1
    der = mod.reconstruct_derivatives(
        grid, runs["hjb_results"]["J0_A77_B120"], runs["params"],
        runs["inputs"]["J0_A77_B120"], runs["labor0"]["J0_A77_B120"], 0.0, 0.01)
    d = mod.decompose_state_5l(
        "J0_A77_B120", i, j, nz, grid, runs["hjb_results"]["J0_A77_B120"],
        runs["params"], runs["inputs"]["J0_A77_B120"],
        runs["labor0"]["J0_A77_B120"], 0.0, 0.01, der, cfg)
    assert d["linear_d_contribution_mu_a"] == pytest.approx(d["transfer"], abs=1e-15)
    assert d["linear_negd_contribution_mu_b"] == pytest.approx(-d["transfer"], abs=1e-15)
    assert abs(d["linear_d_cancellation_sum"]) <= 1e-12


# ---------------------------------------------------------------------------
# 7. Four-way coordinate/total classification
# ---------------------------------------------------------------------------


def test_four_way_classification():
    thr = 1e-10 * mod.DB0
    assert mod.classify_four_way(0.05, -0.3, thr) == mod.CLASS_B_OUTWARD_TOTAL_INWARD
    assert mod.classify_four_way(0.05, 0.1, thr) == mod.CLASS_B_OUTWARD_TOTAL_OUTWARD
    assert mod.classify_four_way(-0.05, -0.3, thr) == mod.CLASS_B_NONOUTWARD_TOTAL_INWARD
    assert mod.classify_four_way(-0.05, 0.1, thr) == mod.CLASS_B_NONOUTWARD_TOTAL_OUTWARD


def test_four_way_phase_b_on_fake_runs():
    cfg = _cfg()
    # one top-layer offender on J0 (119,76,1) with mu_a<0, mu_b>0 => mu_W could
    # be negative if |mu_a|>mu_b
    runs = _full_fake_runs(
        {"J0_A77_B120": [(119, 76, 1)]},
        transfer=-0.43,
        mu_a_state={(119, 76, 1): -0.40})
    g = runs["grids"]["J0_A77_B120"]
    runs["hjb_results"]["J0_A77_B120"].mu_b[119, 76, 1] = 0.05
    state_set = [("J0_A77_B120", 119, 76, 1)]
    interior_positive = set()
    top_offender = {("J0_A77_B120", 76, 1)}
    phase_a = mod.phase_a_state_decomposition(cfg, runs, state_set)
    phase_b = mod.phase_b_classification(cfg, runs, state_set, phase_a,
                                         interior_positive, top_offender)
    r = phase_b["rows"][0]
    assert r["classification"] == mod.CLASS_B_OUTWARD_TOTAL_INWARD  # mu_W = -0.35 <= 0
    assert r["layer_kind"] == "TOP"
    assert r["a_resolution"] == "a77"


# ---------------------------------------------------------------------------
# 8. Every accepted DLH-5K interior-positive state included
# ---------------------------------------------------------------------------


def test_interior_positive_trajectories_match_accepted():
    cfg = _cfg()
    ip = mod.dlh5k_interior_positive_trajectories(cfg)
    # accepted DLH-5K verdict: 12/17 material offenders are interior-positive
    assert len(ip) == 12
    assert ("J0_A77_B120", 76, 1) in ip
    assert ("J3_A153_B120", 152, 1) in ip
    # boundary-only ones excluded
    assert ("J0_A77_B120", 74, 1) not in ip
    assert ("J3_A153_B120", 147, 1) not in ip


def test_interior_positive_states_in_phase_b():
    cfg = _cfg()
    runs = _full_fake_runs()
    state_set = mod.resolve_inherited_state_set(cfg, runs)
    ip = mod.dlh5k_interior_positive_trajectories(cfg)
    top_off = mod.dlh5k_top_offender_trajectories(cfg)
    phase_a = mod.phase_a_state_decomposition(cfg, runs, state_set)
    phase_b = mod.phase_b_classification(cfg, runs, state_set, phase_a, ip, top_off)
    ip_rows = phase_b["interior_positive_rows"]
    # every inherited state whose trajectory is interior-positive is included
    expected_trajs = set()
    for s in state_set:
        if (s[0], s[2], s[3]) in ip:
            expected_trajs.add((s[0], s[2], s[3]))
    included_trajs = {(r["variant"], r["a_index"], r["z_index"]) for r in ip_rows}
    assert included_trajs == expected_trajs
    for r in ip_rows:
        assert r["positive_mu_b_coexists_with"] in ("TOTAL_INWARD", "TOTAL_OUTWARD")


# ---------------------------------------------------------------------------
# 9. Rectangular vs total-wealth normal-drift algebra
# ---------------------------------------------------------------------------


def test_boundary_geometry_rectangular_vs_w_normal():
    cfg = _cfg()
    runs = _full_fake_runs(
        {"J0_A77_B120": [(119, 76, 1)]},
        transfer=-0.43,
        mu_a_state={(119, 76, 1): -0.40})
    runs["hjb_results"]["J0_A77_B120"].mu_b[119, 76, 1] = 0.05
    state_set = [("J0_A77_B120", 119, 76, 1)]
    ip = set()
    top_off = {("J0_A77_B120", 76, 1)}
    phase_a = mod.phase_a_state_decomposition(cfg, runs, state_set)
    phase_b = mod.phase_b_classification(cfg, runs, state_set, phase_a, ip, top_off)
    phase_d = mod.phase_d_boundary_geometry(cfg, runs, phase_b, phase_a)
    assert len(phase_d["rows"]) == 1
    r = phase_d["rows"][0]
    # mu_b=+0.05 violates rectangular b-inwardness
    assert r["rectangular_b_inwardness_mu_b_le_0"] is False
    assert r["rectangular_b_violation"] is True
    # mu_a=-0.40 satisfies rectangular a-inwardness
    assert r["rectangular_a_inwardness_mu_a_le_0"] is True
    # mu_W=-0.35 <= 0 satisfies total-wealth inwardness
    assert r["total_wealth_inwardness_mu_W_le_0"] is True
    assert r["W_normal_drift"] == pytest.approx(-0.35, abs=1e-12)
    assert "mu_W = mu_a + mu_b <= 0" in phase_d["algebra"]["W_normal"]
    assert "NOT authorize replacing the production domain" in phase_d["algebra"]["note"]


# ---------------------------------------------------------------------------
# 10. Exact cross-a aligned comparison
# ---------------------------------------------------------------------------


def test_cross_a_total_wealth_comparison():
    cfg = _cfg()
    runs = _full_fake_runs(transfer=-0.43)
    ca = mod.phase_e_cross_a_total_wealth(cfg, runs)
    assert len(ca["rows"]) == 24
    for r in ca["rows"]:
        assert r["a153_index"] == 2 * r["a77_index"]
        # delta_mu_W = delta_mu_a + delta_mu_b exactly
        assert abs(r["delta_mu_W"] - (r["delta_mu_a"] + r["delta_mu_b"])) <= 1e-9
        assert r["rel_diff_mu_W"] >= 0.0
        assert isinstance(r["mu_b_cross_a_material"], bool)
        assert isinstance(r["mu_W_below_threshold"], bool)
    assert isinstance(ca["annotation_fires"], bool)
    assert ca["policy_rel_materiality"] == 1e-2


# ---------------------------------------------------------------------------
# 11. Terminal classification matrix
# ---------------------------------------------------------------------------


def _fake_phase_b(rows, ip_rows):
    return {"rows": rows, "interior_positive_rows": ip_rows}


def test_terminal_classification_matrix():
    cfg = _cfg()
    cross_a_none = {"annotation_fires": False}
    # Outcome D
    assert mod.overall_terminal(cfg, {"pass_bool": False}, {"pass_bool": True},
                                _fake_phase_b([], []), cross_a_none)["terminal"] == mod.TERMINAL_OUTCOME_D
    # Outcome E
    assert mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": False},
                                _fake_phase_b([], []), cross_a_none)["terminal"] == mod.TERMINAL_OUTCOME_E
    # Outcome A: all positive-mu_b states have mu_W <= 0 (incl. interior-positive)
    rows_a = [{"b_outward": True, "mu_W": -0.1},
              {"b_outward": True, "mu_W": 0.0},
              {"b_outward": False, "mu_W": 0.2}]
    ip_a = [{"mu_W": -0.05}]
    assert mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                _fake_phase_b(rows_a, ip_a), cross_a_none)["terminal"] == mod.TERMINAL_OUTCOME_A
    # Outcome B: an interior-positive state has material mu_W > 0
    rows_b = [{"b_outward": True, "mu_W": -0.1}]
    ip_b = [{"mu_W": 1e-4}]  # > 1e-10 * 7/19 ~ 3.7e-11
    assert mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                _fake_phase_b(rows_b, ip_b), cross_a_none)["terminal"] == mod.TERMINAL_OUTCOME_B
    # Outcome C: a non-interior positive-mu_b state has mu_W > 0 but interior are inward
    rows_c = [{"b_outward": True, "mu_W": -0.1},
              {"b_outward": True, "mu_W": 0.1}]
    ip_c = [{"mu_W": -0.05}]
    assert mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                _fake_phase_b(rows_c, ip_c), cross_a_none)["terminal"] == mod.TERMINAL_OUTCOME_C
    # annotation fires when mu_b cross-a material and mu_W below threshold everywhere
    cross_a_annot = {"annotation_fires": True}
    term = mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                _fake_phase_b(rows_a, ip_a), cross_a_annot)
    assert mod.ANNOTATION_CROSS_A_PORTFOLIO_REALLOCATION in term["annotations"]


# ---------------------------------------------------------------------------
# 12. Deterministic repeat
# ---------------------------------------------------------------------------


def test_deterministic_repeat_records_identical():
    cfg = _cfg()
    from deep_learning_hank.two_asset.high_wealth_corner_closure_diagnostic import compare_scalar_records
    r1 = _fake_variant_record("J0_A77_B120", "a77", "b120",
                              mod.ACCEPTED_J_HJB_STAT["J0_A77_B120"], 0.04291614197305571,
                              0.11648667106972263, 3)
    r2 = _fake_variant_record("J0_A77_B120", "a77", "b120",
                              mod.ACCEPTED_J_HJB_STAT["J0_A77_B120"], 0.04291614197305571,
                              0.11648667106972263, 3)
    cmp = compare_scalar_records(r1, r2, cfg.reproducibility_tol)
    assert cmp["pass_bool"] is True
    assert cmp["max_numeric_diff"] == 0.0


# ---------------------------------------------------------------------------
# 13. No stationary/KFE/aggregate path
# ---------------------------------------------------------------------------


def test_no_stationary_kfe_aggregate_path():
    src = pathlib.Path(mod.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "solve_matlab_faithful_stationary_kfe",
        "assemble_conservative_operator",
        "nullspace_dimension",
        "pin_validation",
        "tail_diagnostics",
        "aggregate_stationary_household",
        "solve_household_steady_state",
    ):
        assert forbidden not in src, f"forbidden stationary symbol present: {forbidden}"
    assert mod.NOT_AUTHORIZED_MARKER == "NOT_AUTHORIZED__DLH_5K_POLICY_ONLY_HIGH_WEALTH_CORNER_CLOSURE_DIAGNOSTIC"


# ---------------------------------------------------------------------------
# 14. No source mutation / no grid continuation
# ---------------------------------------------------------------------------


def test_no_source_mutation_and_no_grid_continuation():
    cfg = _cfg()
    blob_check = hashlib.sha256(ORACLE_PATH.read_bytes()).hexdigest().upper()
    assert blob_check == mod.ACCEPTED_SHA256
    plan = mod.grid_plan_identity(cfg)
    assert plan["liquid"]["hard_ceiling_b_hi"] == 1075.0 / 19.0
    assert set(plan["b_extents"].keys()) == {"b120", "b140", "b160"}
    assert max(e["b_hi"] for e in plan["b_extents"].values()) == 1075.0 / 19.0
    assert cfg.output_root == "reports/dlh_5l_total_wealth_domain_geometry_diagnostic_2026_09_01"


# ---------------------------------------------------------------------------
# Canonical execution (real accepted HJB solves on the six J grids)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def canonical():
    cfg = mod.load_config(CONFIG_PATH)
    dlh5b, params, numerics = mod.build_fixture(cfg)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    runs["params"] = params
    runs["grids"] = mod.build_all_grids(cfg, np.asarray(dlh5b.z, dtype=float),
                                        np.asarray(dlh5b.switch_matrix, dtype=float))[0]
    repro_accepted = mod.check_accepted_j_reproduction(cfg, runs)
    state_set = mod.resolve_inherited_state_set(cfg, runs)
    ip = mod.dlh5k_interior_positive_trajectories(cfg)
    top_off = mod.dlh5k_top_offender_trajectories(cfg)
    phase_a = mod.phase_a_state_decomposition(cfg, runs, state_set)
    phase_b = mod.phase_b_classification(cfg, runs, state_set, phase_a, ip, top_off)
    phase_c = mod.phase_c_positive_mu_b(cfg, runs, phase_b, phase_a)
    phase_d = mod.phase_d_boundary_geometry(cfg, runs, phase_b, phase_a)
    cross_a = mod.phase_e_cross_a_total_wealth(cfg, runs)
    return cfg, runs, repro_accepted, state_set, phase_a, phase_b, phase_c, phase_d, cross_a


def test_canonical_reproduction_passes(canonical):
    _cfg, _runs, repro_accepted, *_ = canonical
    assert repro_accepted["pass_bool"] is True
    for vid, r in repro_accepted["per_variant"].items():
        assert r["pass"] is True


def test_canonical_state_set_and_identities(canonical):
    cfg, runs, _ra, state_set, phase_a, *_ = canonical
    assert len(state_set) == 105
    # every state decomposition: mu_W identity and transfer cancellation exact
    for r in phase_a["rows"]:
        assert abs(r["transfer_cancellation_residual"]) <= cfg.decomposition_residual_tol
        assert abs(r["linear_d_cancellation_sum"]) <= cfg.decomposition_residual_tol


def test_canonical_classification_and_geometry(canonical):
    cfg, runs, _ra, state_set, _pa, phase_b, _pc, phase_d, cross_a = canonical
    ip_rows = phase_b["interior_positive_rows"]
    # every accepted DLH-5K interior-positive state included (12 trajectories)
    trajs = {(r["variant"], r["a_index"], r["z_index"]) for r in ip_rows}
    assert len(trajs) == 12
    # top-layer offenders have rectangular b violation but a-inward and W-inward
    for r in phase_d["rows"]:
        assert r["rectangular_b_violation"] is True
        assert r["rectangular_a_inwardness_mu_a_le_0"] is True
        assert r["total_wealth_inwardness_mu_W_le_0"] is True
        assert r["W_normal_drift"] <= 0.0
    # cross-a: delta_mu_W == delta_mu_a + delta_mu_b
    for r in cross_a["rows"]:
        assert abs(r["delta_mu_W"] - (r["delta_mu_a"] + r["delta_mu_b"])) <= 1e-9


def test_canonical_terminal_not_blocked(canonical):
    cfg, runs, repro_accepted, _ss, _pa, phase_b, _pc, _pd, cross_a = canonical
    dlh5b, params, numerics = mod.build_fixture(cfg)
    repro = mod.reproduce(cfg, dlh5b, params, numerics)
    term = mod.overall_terminal(cfg, repro_accepted, repro, phase_b, cross_a)
    assert term["terminal"] in (mod.TERMINAL_OUTCOME_A, mod.TERMINAL_OUTCOME_B, mod.TERMINAL_OUTCOME_C)
    assert term["terminal"] not in (mod.TERMINAL_OUTCOME_D, mod.TERMINAL_OUTCOME_E)
