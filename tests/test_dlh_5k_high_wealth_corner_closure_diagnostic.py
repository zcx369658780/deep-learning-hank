"""DLH-5K (Issue #37) focused tests.

Covers the Issue #37 minimum tests:

1. exact J0-J5 rerun identity and no new grid;
2. accepted source identity unchanged;
3. accepted J HJB/boundary reproduction;
4. exact drift-decomposition reconstruction;
5. offender completeness;
6. required n-1/n-2/n-3/n-5 localization layers;
7. no invented derivative outside the grid;
8. joint-corner inequality algebra checked numerically against direct drifts;
9. exact cross-a aligned high-wealth comparison;
10. terminal classification matrix;
11. deterministic repeat;
12. no stationary/KFE/aggregate path;
13. no source mutation and no grid continuation.
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

import deep_learning_hank.two_asset.high_wealth_corner_closure_diagnostic as mod

CONFIG_PATH = "configs/dlh_5k_high_wealth_corner_closure_diagnostic.toml"
ORACLE_PATH = pathlib.Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")

_A_PTS = {"a77": 77, "a153": 153}
_B_PTS = {"b120": 120, "b140": 140, "b160": 160}
_B_HI = {"b120": 795.0 / 19.0, "b140": 935.0 / 19.0, "b160": 1075.0 / 19.0}


def _cfg():
    return mod.load_config(CONFIG_PATH)


def _tiny_grid(nb=12, na=6):
    b = np.linspace(-2.0, 41.84210526315789, nb)
    a = np.linspace(0.0, 10.0, na)
    z = np.array([0.8, 1.3])
    switch = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    return MatlabFaithfulHJBGrid(b, a, z, switch)


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
# 2. Accepted source identity unchanged
# ---------------------------------------------------------------------------


def test_accepted_source_identity_unchanged():
    data = ORACLE_PATH.read_bytes()
    assert mod.ACCEPTED_SHA256 == hashlib.sha256(data).hexdigest().upper()
    assert mod.ACCEPTED_BLOB == "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"


# ---------------------------------------------------------------------------
# 3. Accepted J HJB/boundary reproduction (fail closed -> Outcome D)
# ---------------------------------------------------------------------------


def test_accepted_j_reproduction_anchors_match_dlh5j_evidence():
    # anchors copied at full precision from the accepted DLH-5J evidence
    # DLH_5J_REPRODUCIBILITY.json (run1) on origin/main
    assert mod.ACCEPTED_J_HJB_STAT["J0_A77_B120"] == 6.566175159150589e-08
    assert mod.ACCEPTED_J_HJB_STAT["J5_A153_B160"] == 2.059856285541173e-08
    assert mod.ACCEPTED_J_UPPER_B["J3_A153_B120"]["count"] == 6
    assert mod.ACCEPTED_J_UPPER_B["J2_A77_B160"]["count"] == 0
    assert mod.ACCEPTED_J_UPPER_B["J5_A153_B160"]["requested_max"] == 0.040486981858915395
    assert mod.ACCEPTED_J_UPPER_B["J0_A77_B120"]["raw_max"] == 0.04291614197305571
    assert mod.ACCEPTED_J_OFFENDERS["J0_A77_B120"] == [(119, 74, 1), (119, 75, 1), (119, 76, 1)]
    assert mod.ACCEPTED_J_OFFENDERS["J5_A153_B160"] == [(159, 151, 1), (159, 152, 1)]


def _fake_variant_record(vid, a_res, b_ext, stat, raw_ub, req_ub, count):
    a_pts = _A_PTS[a_res]
    b_pts = _B_PTS[b_ext]
    return {
        "variant": vid, "a_res": a_res, "b_ext": b_ext,
        "grid": {"a_pts": a_pts, "a_lo": 0.0, "a_hi": 10.0,
                 "b_pts": b_pts, "b_lo": -2.0, "b_hi": _B_HI[b_ext], "db": mod.DB0},
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


def _full_fake_runs(mu_b_pattern=None, transfer=None, mu_a_state=None):
    """Build a complete fake ``runs`` dict (all six accepted grids) with the given
    top-layer ``mu_b`` pattern (dict variant -> list of (b,a,z) coordinates), a
    constant transfer, and an optional per-state mu_a override."""
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


def test_reproduction_check_passes_on_accepted_anchors():
    cfg = _cfg()
    runs = {"variants": _fake_runs_variants()}
    rep = mod.check_accepted_j_reproduction(cfg, runs)
    assert rep["pass_bool"] is True
    for vid, r in rep["per_variant"].items():
        assert r["pass"] is True


def test_reproduction_check_fails_closed_on_stat_mismatch():
    cfg = _cfg()
    runs = {"variants": _fake_runs_variants()}
    runs["variants"][0]["hjb_statistic"] = 9.999e-08
    rep = mod.check_accepted_j_reproduction(cfg, runs)
    assert rep["pass_bool"] is False
    assert rep["per_variant"]["J0_A77_B120"]["pass"] is False
    assert mod.TERMINAL_OUTCOME_D == "BLOCKED_DLH_5K_ACCEPTED_HJB_REPRODUCTION"


# ---------------------------------------------------------------------------
# 4. Exact drift-decomposition reconstruction
# ---------------------------------------------------------------------------


def test_drift_decomposition_reconstruction():
    cfg = _cfg()
    grid = _tiny_grid()
    shape = (grid.b.size, grid.a.size, grid.z.size)
    i, j, nz = grid.b.size - 1, grid.a.size - 1, 1
    transfer = -2.5
    cost = 0.4
    consumption = 3.2
    labor = 0.6
    # build an hjb whose mu_b matches the accepted identity at (i,j,nz)
    mu_b = np.zeros(shape)
    hjb = _fake_hjb(shape, mu_b=mu_b, transfer=np.full(shape, transfer))
    hjb.consumption = np.ones(shape)
    hjb.consumption[i, j, nz] = consumption
    hjb.labor = np.ones(shape)
    hjb.labor[i, j, nz] = labor
    hjb.adjustment_cost = np.zeros(shape)
    hjb.adjustment_cost[i, j, nz] = cost
    inputs = SimpleNamespace(r_a=0.03, r_b=0.015, tau=0.15,
                             wages=np.array([1.0]), migration_costs=np.array([0.0]),
                             labor_weights=np.array([1.0]))
    labor0 = np.ones(shape)
    der = mod.reconstruct_derivatives(grid, hjb, _params(), inputs, labor0, 0.0, 0.01)
    d = mod._decompose_state("J0_A77_B120", i, j, nz, grid, hjb, _params(), inputs,
                             labor0, 0.0, 0.01, der, cfg)
    b = float(grid.b[i]); a = float(grid.a[j]); z = float(grid.z[nz])
    r_b_eff = inputs.r_b  # b>0
    labor_income = (1 - inputs.tau) * inputs.wages[0] * z * labor
    expected_bls = r_b_eff * b + labor_income - (consumption - 0.0)
    assert abs(d["base_liquid_surplus"] - expected_bls) <= 1e-12
    assert abs(d["transfer_injection"] - (-transfer - cost)) <= 1e-12
    assert abs(d["reconstruction_residual"] - (d["mu_b"] - (d["base_liquid_surplus"] + d["transfer_injection"]))) <= 1e-15


def _params():
    from deep_learning_hank.two_asset import EconomicParams
    return EconomicParams(0.02, 2.0, 5.0, 0.1, 2.0, 1e-6, 0.0, 0.0)


# ---------------------------------------------------------------------------
# 5. Offender completeness
# ---------------------------------------------------------------------------


def test_offender_coordinates_match_accepted_sets():
    cfg = _cfg()
    # build fake runs whose top-layer mu_b reproduces exactly the accepted
    # offender counts (material = requested > 1e-10)
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    hjb_results = {}
    variants = []
    for vid, g in grids.items():
        shape = (g.b.size, g.a.size, g.z.size)
        a_res, b_ext = vid.split("_")[1].lower(), vid.split("_")[2].lower()
        db = float(g.b[1] - g.b[0])
        mu_b = np.zeros(shape)
        for (bi, aj, nz) in mod.ACCEPTED_J_OFFENDERS[vid]:
            mu_b[bi, aj, nz] = 1e-8  # raw > 1e-10*db => requested > 1e-10
        hjb_results[vid] = _fake_hjb(shape, mu_b=mu_b)
        variants.append(_fake_variant_record(
            vid, a_res, b_ext, 1e-8, 1e-8, 1e-8 / db, len(mod.ACCEPTED_J_OFFENDERS[vid])))
    runs = {"variants": variants, "hjb_results": hjb_results, "grids": grids}
    coords = mod.offender_coordinates(runs)
    for vid in mod.VARIANT_IDS:
        if vid == "J2_A77_B160":
            assert coords[vid] == []
            continue
        assert set(coords[vid]) == set(mod.ACCEPTED_J_OFFENDERS[vid])
    # completeness via offender_decomposition (no solve needed; uses fake hjb)
    runs["params"] = _params()
    runs["labor0"] = {vid: np.ones((grids[vid].b.size, grids[vid].a.size, grids[vid].z.size))
                      for vid in grids}
    runs["inputs"] = {vid: SimpleNamespace(r_a=0.03, r_b=0.015, tau=0.15,
                                            wages=np.array([1.0]), migration_costs=np.array([0.0]),
                                            labor_weights=np.array([1.0])) for vid in grids}
    runs["transfer_income"] = 0.0
    runs["rb_gap"] = 0.01
    decomps = mod.offender_decomposition(cfg, runs)
    for vid in mod.VARIANT_IDS:
        if vid == "J2_A77_B160":
            continue
        assert decomps["completeness"][vid]["match"] is True


# ---------------------------------------------------------------------------
# 6. Required n-1/n-2/n-3/n-5 localization layers
# ---------------------------------------------------------------------------


def test_localization_layers_required_set():
    layers = mod.localization_layers(120)
    assert layers == [("n-1", 119), ("n-2", 118), ("n-3", 117), ("n-5", 115)]
    layers160 = mod.localization_layers(160)
    assert layers160 == [("n-1", 159), ("n-2", 158), ("n-3", 157), ("n-5", 155)]


def test_boundary_interior_classification_logic():
    cfg = _cfg()
    # boundary-only: top (119) material positive, all interior layers non-positive
    runs = _full_fake_runs({"J0_A77_B120": [(119, 5, 1)]})
    local = mod.boundary_interior_localization(cfg, runs)
    assert len(local["classifications"]) == 1
    c = local["classifications"][0]
    assert c["classification"] == mod.CLASS_BOUNDARY_ONLY
    assert set(r["layer"] for r in local["rows"]) == {"n-1", "n-2", "n-3", "n-5"}
    # interior persists: top AND one interior layer material positive
    runs2 = _full_fake_runs({"J0_A77_B120": [(119, 5, 1), (117, 5, 1)]})
    local2 = mod.boundary_interior_localization(cfg, runs2)
    assert local2["classifications"][0]["classification"] == mod.CLASS_INTERIOR_PERSISTS


# ---------------------------------------------------------------------------
# 7. No invented derivative outside the grid
# ---------------------------------------------------------------------------


def test_reconstruct_derivatives_uses_accepted_finite_grid_formulas():
    grid = _tiny_grid(nb=12, na=6)
    shape = (grid.b.size, grid.a.size, grid.z.size)
    value = np.arange(np.prod(shape), dtype=float).reshape(shape) * 0.001
    hjb = _fake_hjb(shape, value=value)
    inputs = SimpleNamespace(r_a=0.03, r_b=0.015, tau=0.15, wages=np.array([1.0]),
                             migration_costs=np.array([0.0]), labor_weights=np.array([1.0]))
    labor0 = np.ones(shape)
    params = _params()
    der = mod.reconstruct_derivatives(grid, hjb, params, inputs, labor0, 0.0, 0.01)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    # interior forward/backward equal the accepted finite differences
    assert np.allclose(der["vb_f"][:-1], (value[1:] - value[:-1]) / db, atol=1e-12)
    assert np.allclose(der["vb_b"][1:], der["vb_f"][:-1], atol=1e-12)
    assert np.allclose(der["va_f"][:, :-1], (value[:, 1:] - value[:, :-1]) / da, atol=1e-12)
    assert np.allclose(der["va_b"][:, 1:], der["va_f"][:, :-1], atol=1e-12)
    # top-boundary closure equals the accepted resource marginal utility
    i_top = grid.b.size - 1
    rb = inputs.r_b
    resources = (1 - inputs.tau) * inputs.wages[0] * grid.z * 1.0 + 0.0 + rb * grid.b[i_top]
    expected = resources ** (-params.gamma_c)
    assert np.allclose(der["vb_f"][i_top], expected, atol=1e-12)
    # no derivatives outside the grid: forward a at top a and forward b at top b
    # are closure-filled; backward a at lower a and backward b at lower b are zero
    assert np.all(der["va_f"][:, -1] == 0.0)
    assert np.all(der["va_b"][:, 0] == 0.0)
    assert np.all(der["vb_b"][0] == 0.0)


# ---------------------------------------------------------------------------
# 8. Joint-corner inequality algebra checked numerically against direct drifts
# ---------------------------------------------------------------------------


def test_joint_corner_feasibility_algebra_matches_direct_drifts():
    cfg = _cfg()
    params = _params()
    # J3 offender at (119,152,1) with transfer=-3 (d=-x, x=3), mu_a/mu_b from the
    # joint-corner algebra with a chosen base_liquid_surplus=0.5
    j3 = mod.build_all_grids(cfg, np.asarray([0.8, 1.3]), np.asarray([[-1 / 3, 1 / 3], [1 / 3, -1 / 3]]))[0]["J3_A153_B120"]
    a = float(j3.a[152])
    r_a_eff = float(matlab_faithful_illiquid_return(a, cfg.a_max, 0.03))
    x = 3.0
    a_den = max(a, params.a_bar)
    bls = 0.5
    mu_b_val = bls + x * (1 - params.chi_0) - 0.5 * params.chi_1 * x * x / a_den
    mu_a_val = r_a_eff * a - x
    runs = _full_fake_runs({"J3_A153_B120": [(119, 152, 1)]}, transfer=-3.0,
                           mu_a_state={(119, 152, 1): mu_a_val})
    # mu_b at the offender set to the algebra value
    runs["hjb_results"]["J3_A153_B120"].mu_b[119, 152, 1] = mu_b_val
    # decompose the offender state and align base_liquid_surplus
    der = mod.reconstruct_derivatives(
        j3, runs["hjb_results"]["J3_A153_B120"], params, runs["inputs"]["J3_A153_B120"],
        runs["labor0"]["J3_A153_B120"], 0.0, 0.01)
    decomp = mod._decompose_state(
        "J3_A153_B120", 119, 152, 1, j3, runs["hjb_results"]["J3_A153_B120"], params,
        runs["inputs"]["J3_A153_B120"], runs["labor0"]["J3_A153_B120"], 0.0, 0.01, der, cfg)
    decomp["base_liquid_surplus"] = bls
    decomps = {"rows": [decomp]}
    feasible = mod.joint_corner_feasibility(cfg, runs, decomps)
    row = next(r for r in feasible["rows"] if (r["variant"], r["b_index"], r["a_index"], r["z_index"]) == ("J3_A153_B120", 119, 152, 1))
    assert abs(row["mu_a_residual"]) <= 1e-9
    assert abs(row["mu_b_residual"]) <= 1e-9
    assert abs(row["mu_a_algebra"] - mu_a_val) <= 1e-12
    assert abs(row["mu_b_algebra_general"] - mu_b_val) <= 1e-12
    assert row["x_min_a"] == pytest.approx(r_a_eff * a, abs=1e-12)


# ---------------------------------------------------------------------------
# 9. Exact cross-a aligned high-wealth comparison
# ---------------------------------------------------------------------------


def test_cross_a_aligned_comparison_and_channel():
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
        hjb_results[vid] = _fake_hjb(shape, mu_b=np.full(shape, 1e-6))
        variants.append(_fake_variant_record(vid, a_res, b_ext, 1e-8, 1e-6, 1e-6, 0))
    runs = {
        "variants": variants,
        "hjb_results": hjb_results,
        "grids": grids,
        "params": _params(),
        "labor0": {vid: np.ones((grids[vid].b.size, grids[vid].a.size, grids[vid].z.size))
                   for vid in grids},
        "inputs": {vid: SimpleNamespace(r_a=0.03, r_b=0.015, tau=0.15, wages=np.array([1.0]),
                                        migration_costs=np.array([0.0]), labor_weights=np.array([1.0]))
                   for vid in grids},
        "transfer_income": 0.0,
        "rb_gap": 0.01,
    }
    ca = mod.cross_a_mechanism(cfg, runs)
    assert len(ca["rows"]) > 0
    for r in ca["rows"]:
        assert r["a153_index"] == 2 * r["a77_index"]
        assert abs(r["residual"] - (r["delta_mu_b"] - (r["delta_base_liquid_surplus"] + r["delta_transfer_injection"]))) <= 1e-15
        assert r["channel"] in ("TRANSFER_DERIVATIVE", "BASE_LIQUID_SURPLUS", "BOTH_EQUAL")
    for ext in mod.B_EXT_ORDER:
        assert ext in ca["totals"]
    assert isinstance(ca["b160_primarily_transfer_channel"], bool)


# ---------------------------------------------------------------------------
# 10. Terminal classification matrix
# ---------------------------------------------------------------------------


def test_terminal_classification_matrix():
    cfg = _cfg()
    empty_classifs = []
    empty_decomps = {"rows": []}
    cross_a = {"b160_primarily_transfer_channel": False}

    # Outcome D: accepted reproduction fails
    term_d = mod.overall_terminal(cfg, {"pass_bool": False}, {"pass_bool": True},
                                  empty_classifs, empty_decomps, cross_a)
    assert term_d["terminal"] == mod.TERMINAL_OUTCOME_D

    # Outcome E: deterministic repeat fails
    term_e = mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": False},
                                  empty_classifs, empty_decomps, cross_a)
    assert term_e["terminal"] == mod.TERMINAL_OUTCOME_E

    # Outcome A: all boundary-only + decomposition holds + transfer dominant
    classifs_a = [
        {"variant": "J0_A77_B120", "a_index": 76, "z_index": 1, "classification": mod.CLASS_BOUNDARY_ONLY},
        {"variant": "J3_A153_B120", "a_index": 152, "z_index": 1, "classification": mod.CLASS_BOUNDARY_ONLY},
    ]
    decomps_a = {"rows": [
        {"variant": "J0_A77_B120", "mu_b": 0.05, "transfer_injection": 0.06, "base_liquid_surplus": -0.01, "reconstruction_residual": 0.0},
        {"variant": "J3_A153_B120", "mu_b": 0.05, "transfer_injection": 0.06, "base_liquid_surplus": -0.01, "reconstruction_residual": 0.0},
    ]}
    term_a = mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                  classifs_a, decomps_a, cross_a)
    assert term_a["terminal"] == mod.TERMINAL_OUTCOME_A

    # Outcome B: all interior persists
    classifs_b = [
        {"variant": "J0_A77_B120", "a_index": 76, "z_index": 1, "classification": mod.CLASS_INTERIOR_PERSISTS},
        {"variant": "J3_A153_B120", "a_index": 152, "z_index": 1, "classification": mod.CLASS_INTERIOR_PERSISTS},
    ]
    term_b = mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                  classifs_b, decomps_a, cross_a)
    assert term_b["terminal"] == mod.TERMINAL_OUTCOME_B

    # Outcome C: mixed (some boundary-only, some interior persists)
    classifs_c = [
        {"variant": "J0_A77_B120", "a_index": 76, "z_index": 1, "classification": mod.CLASS_BOUNDARY_ONLY},
        {"variant": "J3_A153_B120", "a_index": 152, "z_index": 1, "classification": mod.CLASS_INTERIOR_PERSISTS},
    ]
    term_c = mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                  classifs_c, decomps_a, cross_a)
    assert term_c["terminal"] == mod.TERMINAL_OUTCOME_C

    # annotation fires when b160 divergence is primarily transfer channel
    term_annot = mod.overall_terminal(cfg, {"pass_bool": True}, {"pass_bool": True},
                                      classifs_c, decomps_a,
                                      {"b160_primarily_transfer_channel": True})
    assert mod.ANNOTATION_CROSS_A_TRANSFER_CHANNEL in term_annot["annotations"]


# ---------------------------------------------------------------------------
# 11. Deterministic repeat
# ---------------------------------------------------------------------------


def test_compare_scalar_records_nonfinite_aware():
    cfg = _cfg()
    r1 = _fake_variant_record("J0_A77_B120", "a77", "b120", 6.566175159e-08, 4.291614197e-02, 1.164866711e-01, 3)
    r2 = _fake_variant_record("J0_A77_B120", "a77", "b120", 6.566175159e-08, 4.291614197e-02, 1.164866711e-01, 3)
    cmp = mod.compare_scalar_records(r1, r2, cfg.reproducibility_tol)
    assert cmp["pass_bool"] is True
    assert cmp["max_numeric_diff"] == 0.0
    r3 = _fake_variant_record("J0_A77_B120", "a77", "b120", 6.566175159e-08, 4.3e-02, 1.164866711e-01, 3)
    cmp3 = mod.compare_scalar_records(r1, r3, cfg.reproducibility_tol)
    assert cmp3["pass_bool"] is False
    # non-finite aligned
    r4 = _fake_variant_record("J0_A77_B120", "a77", "b120", float("nan"), 4.291614197e-02, 1.164866711e-01, 3)
    r5 = _fake_variant_record("J0_A77_B120", "a77", "b120", float("nan"), 4.291614197e-02, 1.164866711e-01, 3)
    cmp5 = mod.compare_scalar_records(r4, r5, cfg.reproducibility_tol)
    assert cmp5["pass_bool"] is True
    assert cmp5["aligned_nonfinite"] >= 1


# ---------------------------------------------------------------------------
# 12. No stationary/KFE/aggregate path
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
        "C,L,A,B",
    ):
        assert forbidden not in src, f"forbidden stationary symbol present: {forbidden}"
    assert mod.NOT_AUTHORIZED_MARKER == "NOT_AUTHORIZED__DLH_5K_POLICY_ONLY_HIGH_WEALTH_CORNER_CLOSURE_DIAGNOSTIC"


# ---------------------------------------------------------------------------
# 13. No source mutation / no grid continuation
# ---------------------------------------------------------------------------


def test_no_source_mutation_and_no_grid_continuation():
    cfg = _cfg()
    # the accepted oracle is byte-identical on disk (read-only reference)
    blob_check = hashlib.sha256(ORACLE_PATH.read_bytes()).hexdigest().upper()
    assert blob_check == mod.ACCEPTED_SHA256
    plan = mod.grid_plan_identity(cfg)  # raises unless the exact J0-J5 plan
    assert plan["liquid"]["hard_ceiling_b_hi"] == 1075.0 / 19.0
    assert set(plan["b_extents"].keys()) == {"b120", "b140", "b160"}
    assert max(e["b_hi"] for e in plan["b_extents"].values()) == 1075.0 / 19.0
    assert cfg.output_root == "reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01"


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
    decomps = mod.offender_decomposition(cfg, runs)
    local = mod.boundary_interior_localization(cfg, runs)
    feasible = mod.joint_corner_feasibility(cfg, runs, decomps)
    cross_a = mod.cross_a_mechanism(cfg, runs)
    return cfg, runs, repro_accepted, decomps, local, feasible, cross_a


def test_canonical_reproduction_passes(canonical):
    _cfg, _runs, repro_accepted, _d, _l, _f, _c = canonical
    assert repro_accepted["pass_bool"] is True
    for vid, r in repro_accepted["per_variant"].items():
        assert r["pass"] is True


def test_canonical_offender_completeness_and_localization(canonical):
    cfg, _runs, _ra, decomps, local, _f, _c = canonical
    for vid in mod.VARIANT_IDS:
        if vid == "J2_A77_B160":
            continue
        assert decomps["completeness"][vid]["match"] is True
    assert len(local["classifications"]) > 0
    for c in local["classifications"]:
        assert c["classification"] in (mod.CLASS_BOUNDARY_ONLY, mod.CLASS_INTERIOR_PERSISTS, mod.CLASS_MIXED)
    # every localized row has the 4 required layers
    for r in local["rows"]:
        assert r["layer"] in ("n-1", "n-2", "n-3", "n-5")


def test_canonical_decomposition_and_feasibility_consistency(canonical):
    cfg, _runs, _ra, decomps, _l, feasible, _c = canonical
    offender_rows = [r for r in decomps["rows"] if r["variant"] != "J2_A77_B160"]
    assert len(offender_rows) > 0
    for r in offender_rows:
        assert abs(r["reconstruction_residual"]) <= cfg.decomposition_residual_tol
    for r in feasible["rows"]:
        assert abs(r["mu_a_residual"]) <= 1e-9
        assert abs(r["mu_b_residual"]) <= 1e-9


def test_canonical_terminal_not_blocked(canonical):
    cfg, runs, repro_accepted, decomps, local, _f, cross_a = canonical
    dlh5b, params, numerics = mod.build_fixture(cfg)
    repro = mod.reproduce(cfg, dlh5b, params, numerics)
    term = mod.overall_terminal(cfg, repro_accepted, repro, local["classifications"], decomps, cross_a)
    assert term["terminal"] in (mod.TERMINAL_OUTCOME_A, mod.TERMINAL_OUTCOME_B, mod.TERMINAL_OUTCOME_C)
    assert term["terminal"] not in (mod.TERMINAL_OUTCOME_D, mod.TERMINAL_OUTCOME_E)
