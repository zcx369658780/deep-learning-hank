"""DLH-5J (Issue #36) focused tests.

Covers the Issue #36 minimum tests:

1. exact six-variant identity
2. fixed physical a domain and a_max=10 across all variants
3. exact unchanged taper identity/value on every common physical a node
4. exact a77/a153 nesting (a77 nodes = every second a153 node)
5. exact b120/b140/b160 same-spacing nesting
6. exact same-b-extent cross-a physical-grid identity and db=7/19 unchanged
7. fresh initialization / no warm-start plumbing
8. raw + requested diagnostics for all four asset boundaries
9. raw-threshold relations
10. complete offending-state evidence
11. final A77 and A153 continuation trend calculations using accepted DLH-5I
    b100 scalar anchors WITHOUT rerunning b100
12. exact aligned cross-a policy comparison on all three required pairs
13. per-variant joint compatibility marker
14. per-final-extent cross-a joint compatibility marker
15. final route stopping-rule classification (Outcomes A-F)
16. no stationary/KFE/density/tail/aggregate execution path
17. deterministic repeat with non-finite-aware comparison
18. accepted HJB source identity unchanged
19. accepted DLH-5I b100 scalar-anchor identity reproduced from read-only evidence
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

import deep_learning_hank.two_asset.final_coupled_b_extent_diagnostic as mod

CONFIG_PATH = "configs/dlh_5j_final_coupled_b_extent_diagnostic.toml"
ORACLE_PATH = pathlib.Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")

_A_PTS = {"a77": 77, "a153": 153}
_B_PTS = {"b120": 120, "b140": 140, "b160": 160}
_B_HI = {"b120": 795.0 / 19.0, "b140": 935.0 / 19.0, "b160": 1075.0 / 19.0}


def _cfg():
    return mod.load_config(CONFIG_PATH)


def _tiny_grid(nb=8, na=6):
    b = np.linspace(-2.0, 41.84210526315789, nb)
    a = np.linspace(0.0, 10.0, na)
    z = np.array([0.8, 1.3])
    switch = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    return MatlabFaithfulHJBGrid(b, a, z, switch)


def _fake_hjb(shape, mu_a=None, mu_b=None, value=None):
    return SimpleNamespace(
        value=np.full(shape, 0.0) if value is None else value,
        consumption=np.ones(shape),
        labor=np.ones(shape),
        transfer=np.ones(shape),
        mu_a=np.zeros(shape) if mu_a is None else mu_a,
        mu_b=np.zeros(shape) if mu_b is None else mu_b,
        liquid_label=np.zeros(shape, dtype=int),
        transfer_label=np.zeros(shape, dtype=int),
    )


def _bd(name, direction, maxv, cnt, shr, off, req_max=None):
    rmax = req_max if req_max is not None else maxv
    return {
        "boundary": name,
        "direction": direction,
        "raw": {
            "max": maxv, "count_above_threshold": cnt, "share_above_threshold": shr,
            "argmax_index": (1, 1, 1), "argmax_physical": (1.0, 10.0, 0.8),
            "value_at_argmax": maxv,
            "quantiles": {"q50": 1.0, "q90": 2.0, "q95": 3.0, "q99": 4.0},
            "offending_states": [
                {"b_index": o[0], "a_index": o[1], "z_index": o[2],
                 "b": 1.0, "a": 10.0, "z": 0.8, "rate": float(o[3])} for o in off
            ],
        },
        "requested": {
            "max": rmax, "count_above_threshold": cnt, "share_above_threshold": shr,
            "argmax_index": (1, 1, 1), "argmax_physical": (1.0, 10.0, 0.8),
            "value_at_argmax": rmax,
            "quantiles": {"q50": 1.0, "q90": 2.0, "q95": 3.0, "q99": 4.0},
            "offending_states": [
                {"b_index": o[0], "a_index": o[1], "z_index": o[2],
                 "b": 1.0, "a": 10.0, "z": 0.8, "rate": float(o[3])} for o in off
            ],
        },
    }


def _fake_variant_record(variant, a_res, b_ext, ua_raw=0.0, ua_req=0.0,
                         ub_raw=0.0, ub_req=0.0, hjb_statistic=1.0,
                         ua_cnt=0, ub_cnt=0, offending=()):
    a_pts = _A_PTS[a_res]
    b_pts = _B_PTS[b_ext]
    ub_hi = _B_HI[b_ext]
    da = 10.0 / (a_pts - 1)
    db = float(mod.DB0)
    thr = 1e-10
    joint = bool(ub_req <= thr and ua_req <= thr)
    return {
        "variant": variant,
        "a_res": a_res,
        "b_ext": b_ext,
        "grid": {
            "a_pts": a_pts, "a_lo": 0.0, "a_hi": 10.0, "da": da, "a_max": 10.0,
            "b_pts": b_pts, "b_lo": -2.0, "b_hi": ub_hi, "db": db, "z_pts": 2,
        },
        "frozen_prices_identity": {"wbar": 1.0, "r_a": 0.03},
        "hjb_converged": True,
        "hjb_iterations": 10,
        "hjb_statistic": hjb_statistic,
        "boundary": {
            "max_raw_upper_a": ua_raw,
            "max_raw_lower_a": 0.0,
            "max_raw_upper_b": ub_raw,
            "max_raw_lower_b": 0.0,
            "boundaries": [
                _bd("upper_a", "a_forward", ua_raw, ua_cnt, 0.0, (), req_max=ua_req),
                _bd("lower_a", "a_backward", 0.0, 0, 0.0, ()),
                _bd("upper_b", "b_forward", ub_raw, ub_cnt, 0.0, offending, req_max=ub_req),
                _bd("lower_b", "b_backward", 0.0, 0, 0.0, ()),
            ],
        },
        "requested_upper_a": ua_req,
        "requested_upper_b": ub_req,
        "joint_compatible": joint,
        "joint_marker": mod.JOINT_COMPATIBLE if joint else mod.JOINT_NOT_COMPATIBLE,
        "variant_terminal": "HJB_CONVERGED",
    }


def _six_fake_records(seq=None):
    """Default: all upper-a/b zero (all jointly compatible). seq overrides per
    variant (J0..J5) upper-b requested maxima and upper-a requested maxima."""
    seq = seq or {}
    return [
        _fake_variant_record(
            vid, vid.split("_")[1].lower(), vid.split("_")[2].lower(),
            ua_req=seq.get((vid, "ua"), 0.0),
            ub_req=seq.get((vid, "ub"), 0.0),
            ub_raw=seq.get((vid, "ub_raw"), seq.get((vid, "ub"), 0.0)),
            ub_cnt=seq.get((vid, "ub_cnt"), 0),
        )
        for vid in mod.VARIANT_IDS
    ]


# ---------------------------------------------------------------------------
# 1. Exact six-variant plan identity
# ---------------------------------------------------------------------------


def test_exact_six_variant_plan_identity():
    cfg = _cfg()
    plan = mod.grid_plan_identity(cfg)
    ids = list(plan["variants"].keys())
    assert ids == mod.VARIANT_IDS
    for vid in mod.VARIANT_IDS:
        p = plan["variants"][vid]
        assert p["a_pts"] == _A_PTS[p["a_res"]]
        assert p["b_pts"] == _B_PTS[p["b_ext"]]
        assert abs(p["db"] - mod.DB0) <= 1e-12
    assert abs(plan["a_resolutions"]["a77"]["da"] - mod.DA0 / 4) <= 1e-12
    assert abs(plan["a_resolutions"]["a153"]["da"] - mod.DA0 / 8) <= 1e-12
    assert abs(plan["b_extents"]["b120"]["b_hi"] - 795.0 / 19.0) <= 1e-12
    assert abs(plan["b_extents"]["b140"]["b_hi"] - 935.0 / 19.0) <= 1e-12
    assert abs(plan["b_extents"]["b160"]["b_hi"] - 1075.0 / 19.0) <= 1e-12
    # b160 is the hard route ceiling (no extent beyond b160 in the plan)
    assert plan["liquid"]["hard_ceiling_b_hi"] == 1075.0 / 19.0
    assert cfg.route_ceiling_note == "b160_IS_THE_HARD_ROUTE_CEILING__NO_B180_B200"


# ---------------------------------------------------------------------------
# 2/3. Frozen physical a domain / a_max / taper identity
# ---------------------------------------------------------------------------


def test_fixed_physical_a_domain_and_amax():
    cfg = _cfg()
    ill = mod.grid_plan_identity(cfg)["illiquid"]
    assert ill["a_lo"] == 0.0
    assert ill["a_hi"] == 10.0
    assert ill["a_max"] == 10.0
    assert ill["taper_identity"] == "r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED"
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    for g in grids.values():
        assert abs(g.a[0] - 0.0) <= 1e-12
        assert abs(g.a[-1] - 10.0) <= 1e-12


def test_taper_identity_value_on_common_nodes():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    r_a = cfg.r_a
    a_max = cfg.a_max
    a77 = grids["J0_A77_B120"]
    a153 = grids["J3_A153_B120"]
    assert np.allclose(matlab_faithful_illiquid_return(a77.a, a_max, r_a),
                       matlab_faithful_illiquid_return(a153.a[::2], a_max, r_a), atol=1e-15)
    for vid, g in grids.items():
        if vid.startswith(("J0", "J1", "J2")):
            assert np.allclose(g.a, a77.a, atol=1e-12)
        else:
            assert np.allclose(g.a, a153.a, atol=1e-12)
    assert np.allclose(matlab_faithful_illiquid_return(grids["J4_A153_B140"].a[::2], a_max, r_a),
                       matlab_faithful_illiquid_return(a77.a, a_max, r_a), atol=1e-15)
    assert np.allclose(matlab_faithful_illiquid_return(grids["J5_A153_B160"].a[::2], a_max, r_a),
                       matlab_faithful_illiquid_return(a77.a, a_max, r_a), atol=1e-15)


# ---------------------------------------------------------------------------
# 4/5/6. Nesting and alignment
# ---------------------------------------------------------------------------


def test_a77_a153_nesting_and_b_extent_nesting():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    for cid, fid in (("J0_A77_B120", "J3_A153_B120"),
                     ("J1_A77_B140", "J4_A153_B140"),
                     ("J2_A77_B160", "J5_A153_B160")):
        assert np.allclose(grids[fid].a[::2], grids[cid].a, atol=1e-12)
    # b120 nested in b140/b160, b140 nested in b160 (common nodes, same spacing)
    assert np.allclose(grids["J1_A77_B140"].b[:120], grids["J0_A77_B120"].b, atol=1e-12)
    assert np.allclose(grids["J2_A77_B160"].b[:120], grids["J0_A77_B120"].b, atol=1e-12)
    assert np.allclose(grids["J2_A77_B160"].b[:140], grids["J1_A77_B140"].b, atol=1e-12)
    for vid in mod.VARIANT_IDS:
        assert abs(grids[vid].b[1] - grids[vid].b[0] - mod.DB0) <= 1e-12
    # db=7/19 unchanged across all extents
    for vid in mod.VARIANT_IDS:
        assert abs(grids[vid].b[1] - grids[vid].b[0]) - mod.DB0 <= 1e-12


def test_same_b_extent_cross_a_grid_identity():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    for cid, fid in (("J0_A77_B120", "J3_A153_B120"),
                     ("J1_A77_B140", "J4_A153_B140"),
                     ("J2_A77_B160", "J5_A153_B160")):
        assert np.allclose(grids[cid].b, grids[fid].b, atol=1e-12)
        assert np.allclose(grids[cid].z, grids[fid].z, atol=1e-12)


# ---------------------------------------------------------------------------
# 7. Fresh initialization / no warm-start
# ---------------------------------------------------------------------------


def test_fresh_initialization_per_variant(monkeypatch):
    cfg = _cfg()
    dlh5b, params, numerics = mod.build_fixture(cfg)
    calls = []

    def fake_initial_condition(grid, *a, **k):
        calls.append((grid.b.size, grid.a.size))
        shape = (grid.b.size, grid.a.size, grid.z.size)
        return np.zeros(shape), np.ones(shape)

    def fake_solve(grid, params, inputs, initial, labor0, *a, **k):
        shape = (grid.b.size, grid.a.size, grid.z.size)
        return SimpleNamespace(
            value=np.zeros(shape), consumption=np.ones(shape), labor=np.ones(shape),
            transfer=np.zeros(shape), mu_a=np.zeros(shape), mu_b=np.zeros(shape),
            liquid_label=np.zeros(shape, dtype=int), transfer_label=np.zeros(shape, dtype=int),
            converged=True, iterations=10, convergence_statistic=1e-9,
        )

    monkeypatch.setattr(mod, "household_initial_condition", fake_initial_condition)
    monkeypatch.setattr(mod, "solve_matlab_faithful_hjb", fake_solve)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    assert calls == [(120, 77), (140, 77), (160, 77), (120, 153), (140, 153), (160, 153)]
    assert all(v["hjb_converged"] for v in runs["variants"])


# ---------------------------------------------------------------------------
# 8/9/10. Boundary diagnostics (all four boundaries, raw + requested)
# ---------------------------------------------------------------------------


def _boundary_fixture():
    grid = _tiny_grid(nb=8, na=6)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    ua = np.zeros((8, 2))
    ua[1, 0] = 0.1 * da
    ua[3, 1] = 0.2 * da
    ua[5, 1] = 0.6 * da
    mu_a = np.zeros((8, 6, 2))
    mu_a[:, 5, :] = ua
    mu_b = np.zeros((8, 6, 2))
    mu_b[7, 4, 1] = 0.3 * db
    return grid, db, da, mu_a, mu_b


def test_raw_and_requested_all_four_boundaries():
    grid, db, da, mu_a, mu_b = _boundary_fixture()
    hjb = _fake_hjb((8, 6, 2), mu_a=mu_a, mu_b=mu_b)
    bd = mod.boundary_diagnostics(hjb, grid, da, db, 1e-10)
    ua = next(b for b in bd["boundaries"] if b["boundary"] == "upper_a")
    assert ua["raw"]["argmax_index"] == (5, 5, 1)
    assert abs(ua["raw"]["max"] - 0.6 * da) <= 1e-12
    assert abs(ua["requested"]["max"] - 0.6) <= 1e-12
    assert ua["requested"]["count_above_threshold"] == 3
    la = next(b for b in bd["boundaries"] if b["boundary"] == "lower_a")
    assert la["raw"]["max"] == 0.0
    ub = next(b for b in bd["boundaries"] if b["boundary"] == "upper_b")
    assert ub["raw"]["max"] == 0.3 * db
    assert abs(ub["requested"]["max"] - 0.3) <= 1e-12
    assert ub["requested"]["count_above_threshold"] == 1
    lb = next(b for b in bd["boundaries"] if b["boundary"] == "lower_b")
    assert lb["raw"]["max"] == 0.0


def test_threshold_relations_raw_1e10_spacing():
    grid, db, da, mu_a, mu_b = _boundary_fixture()
    hjb = _fake_hjb((8, 6, 2), mu_a=mu_a, mu_b=mu_b)
    bd = mod.boundary_diagnostics(hjb, grid, da, db, 1e-10)
    ua = next(b for b in bd["boundaries"] if b["boundary"] == "upper_a")
    ub = next(b for b in bd["boundaries"] if b["boundary"] == "upper_b")
    assert ua["raw"]["count_above_threshold"] == 3
    assert ua["requested"]["count_above_threshold"] == 3
    assert abs(ua["raw"]["max"] - ua["requested"]["max"] * da) <= 1e-12
    assert ub["raw"]["count_above_threshold"] == 1
    assert ub["requested"]["count_above_threshold"] == 1
    assert abs(ub["raw"]["max"] - ub["requested"]["max"] * db) <= 1e-12


def test_complete_offending_states():
    grid, db, da, mu_a, mu_b = _boundary_fixture()
    hjb = _fake_hjb((8, 6, 2), mu_a=mu_a, mu_b=mu_b)
    bd = mod.boundary_diagnostics(hjb, grid, da, db, 1e-10)
    ua = next(b for b in bd["boundaries"] if b["boundary"] == "upper_a")
    req = ua["requested"]
    states = {(o["b_index"], o["a_index"], o["z_index"]) for o in req["offending_states"]}
    assert states == {(5, 5, 1), (3, 5, 1), (1, 5, 0)}
    rates = {o["rate"] for o in req["offending_states"]}
    assert rates == {0.1, 0.2, 0.6}
    idxs = [(o["b_index"], o["a_index"], o["z_index"]) for o in req["offending_states"]]
    assert idxs == sorted(idxs)


# ---------------------------------------------------------------------------
# 11. Final continuation trends with accepted b100 anchors (no b100 rerun)
# ---------------------------------------------------------------------------


def test_extent_trends_uses_b100_anchor_and_continuation():
    cfg = _cfg()
    recs = _six_fake_records({
        ("J0_A77_B120", "ub"): 0.15, ("J0_A77_B120", "ub_raw"): 0.06, ("J0_A77_B120", "ub_cnt"): 4,
        ("J1_A77_B140", "ub"): 0.10, ("J1_A77_B140", "ub_raw"): 0.04, ("J1_A77_B140", "ub_cnt"): 3,
        ("J2_A77_B160", "ub"): 0.06, ("J2_A77_B160", "ub_raw"): 0.023, ("J2_A77_B160", "ub_cnt"): 2,
        ("J3_A153_B120", "ub"): 0.18, ("J3_A153_B120", "ub_raw"): 0.07, ("J3_A153_B120", "ub_cnt"): 6,
        ("J4_A153_B140", "ub"): 0.12, ("J4_A153_B140", "ub_raw"): 0.046, ("J4_A153_B140", "ub_cnt"): 4,
        ("J5_A153_B160", "ub"): 0.08, ("J5_A153_B160", "ub_raw"): 0.03, ("J5_A153_B160", "ub_cnt"): 3,
    })
    trends = mod.extent_trends(cfg, {"variants": recs})
    s77 = trends["sequences"]["a77"]
    assert [e["b_extent"] for e in s77["entries"]] == ["b100", "b120", "b140", "b160"]
    assert s77["entries"][0]["variant"] == "I2_A77_B100"
    assert s77["entries"][0]["is_anchor"] is True
    assert s77["entries"][0]["requested_max"] == mod.B100_ANCHOR_A77["requested_max"]
    assert s77["entries"][0]["raw_max"] == mod.B100_ANCHOR_A77["raw_max"]
    assert s77["requested_seq"] == [mod.B100_ANCHOR_A77["requested_max"], 0.15, 0.10, 0.06]
    assert s77["strictly_decreasing_requested"] is True
    assert s77["vs_b100_requested"] == [1.0, round(0.15 / mod.B100_ANCHOR_A77["requested_max"], 6),
                                        round(0.10 / mod.B100_ANCHOR_A77["requested_max"], 6),
                                        round(0.06 / mod.B100_ANCHOR_A77["requested_max"], 6)]
    assert s77["first_requested_below_threshold"] is None
    s153 = trends["sequences"]["a153"]
    assert [e["b_extent"] for e in s153["entries"]] == ["b100", "b120", "b140", "b160"]
    assert s153["entries"][0]["variant"] == "I5_A153_B100"
    assert s153["entries"][0]["is_anchor"] is True
    assert s153["strictly_decreasing_requested"] is True


def test_b100_is_not_rerun_by_extent_trends():
    """Phase C must consume the accepted b100 scalar anchors and must not run a
    b100 variant (no b100 grid/variant exists in the plan or the runs)."""
    cfg = _cfg()
    plan = mod.grid_plan_identity(cfg)
    assert "b100" not in plan["b_extents"]
    assert not any(v.b_ext == "b100" for v in cfg.variants)
    recs = _six_fake_records()
    trends = mod.extent_trends(cfg, {"variants": recs})
    for a_res in mod.A_RES_ORDER:
        entries = trends["sequences"][a_res]["entries"]
        assert entries[0]["is_anchor"] is True
        assert entries[0]["variant"].endswith("B100")
        # continuation entries are only the six J variants
        assert [e["variant"] for e in entries[1:]] == [
            vid for vid in mod.VARIANT_IDS if vid.split("_")[1].lower() == a_res]


# ---------------------------------------------------------------------------
# 12. Exact aligned cross-a policy comparison on all three required pairs
# ---------------------------------------------------------------------------


def test_cross_a_policy_comparison_all_three_pairs():
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
        hjb_results[vid] = _fake_hjb(shape, value=np.full(shape, 0.5))
        variants.append(_fake_variant_record(vid, a_res, b_ext, ua_raw=0.1, ua_req=0.1, ub_raw=0.1, ub_req=0.1))
    res = mod.cross_a_policy_comparisons(cfg, {"hjb_results": hjb_results, "variants": variants})
    assert [c["comparison"] for c in res] == [
        "J0_A77_B120_vs_J3_A153_B120",
        "J1_A77_B140_vs_J4_A153_B140",
        "J2_A77_B160_vs_J5_A153_B160",
    ]
    assert [c["b_extent"] for c in res] == ["b120", "b140", "b160"]
    for c in res:
        assert c["reached"] is True
        assert c["fields"]["value"]["max_abs_diff"] == 0.0
        assert c["fields"]["value"]["rel_diff"] == 0.0
        assert c["fields"]["liquid_label"]["mismatch_count"] == 0
        assert c["fields"]["transfer_label"]["mismatch_count"] == 0


# ---------------------------------------------------------------------------
# 13/14. Joint compatibility marker + per-final-extent cross-a frontier
# ---------------------------------------------------------------------------


def test_joint_compatibility_marker():
    cfg = _cfg()
    r1 = _fake_variant_record("J0_A77_B120", "a77", "b120", ua_req=0.3, ub_req=0.0)
    assert r1["joint_marker"] == mod.JOINT_NOT_COMPATIBLE
    r2 = _fake_variant_record("J1_A77_B140", "a77", "b140", ua_req=0.0, ub_req=0.0)
    assert r2["joint_marker"] == mod.JOINT_COMPATIBLE


def test_cross_a_joint_frontier_marker():
    cfg = _cfg()
    # b120: only a77 compatible -> NOT; b140: both compatible -> CROSS_A_COMPATIBLE
    recs = _six_fake_records({
        ("J0_A77_B120", "ub"): 0.0,
        ("J3_A153_B120", "ub"): 0.2,
        ("J1_A77_B140", "ub"): 0.0,
        ("J4_A153_B140", "ub"): 0.0,
        ("J2_A77_B160", "ub"): 0.0,
        ("J5_A153_B160", "ub"): 0.2,
    })
    frontier = mod.joint_frontier(cfg, {"variants": recs})
    assert [p["variant"] for p in frontier["per_variant"]] == mod.VARIANT_IDS
    by_ext = {e["b_extent"]: e for e in frontier["extents"]}
    assert by_ext["b120"]["a77_joint_compatible"] is True
    assert by_ext["b120"]["a153_joint_compatible"] is False
    assert by_ext["b120"]["cross_a_joint_compatible"] is False
    assert by_ext["b120"]["marker"] == mod.CROSS_A_NOT_COMPATIBLE
    assert by_ext["b140"]["cross_a_joint_compatible"] is True
    assert by_ext["b140"]["marker"] == mod.CROSS_A_COMPATIBLE
    assert by_ext["b160"]["cross_a_joint_compatible"] is False


# ---------------------------------------------------------------------------
# 15. Final route stopping-rule classification
# ---------------------------------------------------------------------------


def test_terminal_and_stopping_rule_matrix():
    cfg = _cfg()
    # Outcome A: common final extent jointly compatible at both a77 and a153
    runs_a = {"variants": _six_fake_records({("J0_A77_B120", "ub"): 0.0, ("J3_A153_B120", "ub"): 0.0})}
    term_a = mod.overall_terminal(cfg, runs_a, {"pass_bool": True}, [])
    assert term_a["terminal"] == mod.TERMINAL_OUTCOME_A
    route_a = mod.stopping_rule(cfg, runs_a, {"pass_bool": True}, [])
    assert route_a["route"] == "B_RESOLUTION_CONFIRMATION_AT_SMALLEST_COMPATIBLE_EXTENT"
    assert route_a["smallest_compatible_extent"] == "b120"

    # Outcome B: joint compatibility at only one mature a resolution
    runs_b = {"variants": _six_fake_records({
        ("J0_A77_B120", "ub"): 0.0, ("J1_A77_B140", "ub"): 0.0, ("J2_A77_B160", "ub"): 0.0,
        ("J3_A153_B120", "ub"): 0.2, ("J4_A153_B140", "ub"): 0.15, ("J5_A153_B160", "ub"): 0.1,
    })}
    term_b = mod.overall_terminal(cfg, runs_b, {"pass_bool": True}, [])
    assert term_b["terminal"] == mod.TERMINAL_OUTCOME_B

    # Outcome C: clean attenuation persists through b160 but no common threshold
    runs_c = {"variants": _six_fake_records({
        ("J0_A77_B120", "ub"): 0.15, ("J1_A77_B140", "ub"): 0.10, ("J2_A77_B160", "ub"): 0.06,
        ("J3_A153_B120", "ub"): 0.18, ("J4_A153_B140", "ub"): 0.12, ("J5_A153_B160", "ub"): 0.08,
    })}
    term_c = mod.overall_terminal(cfg, runs_c, {"pass_bool": True}, [])
    assert term_c["terminal"] == mod.TERMINAL_OUTCOME_C
    route_c = mod.stopping_rule(cfg, runs_c, {"pass_bool": True}, [])
    assert route_c["route"] == "ASYMPTOTIC_OR_FINITE_DOMAIN_CLOSURE_ADJUDICATION"
    assert "b160" in route_c["note"] and "larger-grid" in route_c["note"]

    # Outcome D: non-monotonic behavior in the final continuation
    runs_d = {"variants": _six_fake_records({
        ("J0_A77_B120", "ub"): 0.15, ("J1_A77_B140", "ub"): 0.03, ("J2_A77_B160", "ub"): 0.15,
        ("J3_A153_B120", "ub"): 0.18, ("J4_A153_B140", "ub"): 0.12, ("J5_A153_B160", "ub"): 0.08,
    })}
    term_d = mod.overall_terminal(cfg, runs_d, {"pass_bool": True}, [])
    assert term_d["terminal"] == mod.TERMINAL_OUTCOME_D
    route_d = mod.stopping_rule(cfg, runs_d, {"pass_bool": True}, [])
    assert route_d["route"] == "ASYMPTOTIC_OR_FINITE_DOMAIN_CLOSURE_ADJUDICATION"

    # Outcome E: HJB numerical stability blocker
    runs_e = {"variants": _six_fake_records()}
    runs_e["variants"][0]["hjb_converged"] = False
    term_e = mod.overall_terminal(cfg, runs_e, {"pass_bool": True}, [])
    assert term_e["terminal"] == mod.TERMINAL_OUTCOME_E

    # Outcome F: reproducibility blocker
    runs_f = {"variants": _six_fake_records()}
    term_f = mod.overall_terminal(cfg, runs_f, {"pass_bool": False}, [])
    assert term_f["terminal"] == mod.TERMINAL_OUTCOME_F


# ---------------------------------------------------------------------------
# 16. No stationary execution path
# ---------------------------------------------------------------------------


def test_no_stationary_execution_path():
    src = pathlib.Path(mod.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "solve_matlab_faithful_stationary_kfe",
        "assemble_conservative_operator",
        "conservative_stationary_kfe",
        "nullspace_dimension",
        "pin_validation",
        "tail_diagnostics",
        "aggregate_stationary_household",
        "requested_rates",
    ):
        assert forbidden not in src, f"forbidden stationary symbol present: {forbidden}"
    assert mod.NOT_AUTHORIZED_MARKER == "NOT_AUTHORIZED__DLH_5J_POLICY_ONLY_FINAL_BOUNDED_EXTENT_DIAGNOSTIC"


# ---------------------------------------------------------------------------
# 17. Deterministic repeat (structural + numeric + non-finite-aware)
# ---------------------------------------------------------------------------


def test_deterministic_nonfinite_aware_repeat_comparison():
    cfg = _cfg()
    r1 = _fake_variant_record("J0_A77_B120", "a77", "b120", hjb_statistic=1.5e-8,
                              ua_raw=0.3, ua_req=0.3, ub_raw=0.0, ub_req=0.0,
                              ua_cnt=2, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    r2 = _fake_variant_record("J0_A77_B120", "a77", "b120", hjb_statistic=1.5e-8,
                              ua_raw=0.3, ua_req=0.3, ub_raw=0.0, ub_req=0.0,
                              ua_cnt=2, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    cmp = mod.compare_variant_records(r1, r2, cfg)
    assert cmp["identical_structural_signature"] is True
    assert cmp["max_numeric_diff"] == 0.0
    assert cmp["pass_bool"] is True

    r3 = _fake_variant_record("J0_A77_B120", "a77", "b120", hjb_statistic=2.5e-8,
                              ua_raw=0.3, ua_req=0.3, ub_raw=0.0, ub_req=0.0,
                              ua_cnt=2, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    cmp3 = mod.compare_variant_records(r1, r3, cfg)
    assert cmp3["identical_structural_signature"] is True
    assert cmp3["max_numeric_diff"] == pytest.approx(1.0e-8, abs=1e-12)
    assert cmp3["pass_bool"] is False

    r4 = _fake_variant_record("J0_A77_B120", "a77", "b120")
    r4["boundary"]["boundaries"][0]["raw"]["max"] = float("nan")
    r5 = _fake_variant_record("J0_A77_B120", "a77", "b120")
    r5["boundary"]["boundaries"][0]["raw"]["max"] = float("nan")
    cmp5 = mod.compare_variant_records(r4, r5, cfg)
    assert cmp5["pass_bool"] is True
    assert cmp5["aligned_nonfinite_fields"] >= 1

    r6 = _fake_variant_record("J0_A77_B120", "a77", "b120")
    r6["boundary"]["boundaries"][0]["raw"]["max"] = float("nan")
    r7 = _fake_variant_record("J0_A77_B120", "a77", "b120")
    cmp6 = mod.compare_variant_records(r6, r7, cfg)
    assert cmp6["mismatched_fields"] >= 1
    assert cmp6["pass_bool"] is False


def test_randomness_not_applicable_and_repro_structure(monkeypatch):
    cfg = _cfg()
    dlh5b, params, numerics = mod.build_fixture(cfg)
    calls = {"n": 0}

    def fake_runs(*a, **k):
        calls["n"] += 1
        return {"grid_plan": {}, "variants": [], "hjb_results": {}}

    monkeypatch.setattr(mod, "run_all_variants", fake_runs)
    monkeypatch.setattr(mod, "cross_a_policy_comparisons", lambda cfg, runs: [])
    repro = mod.reproduce(cfg, dlh5b, params, numerics)
    assert calls["n"] == 2
    assert repro["randomness"] == "NOT_APPLICABLE"
    assert repro["pass_bool"] is True
    assert repro["terminal_run1"] == repro["terminal_run2"]


# ---------------------------------------------------------------------------
# 18. Accepted source identity
# ---------------------------------------------------------------------------


def test_accepted_source_identity_unchanged():
    data = ORACLE_PATH.read_bytes()
    assert mod.ACCEPTED_SHA256 == hashlib.sha256(data).hexdigest().upper()
    assert mod.ACCEPTED_BLOB == "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"


# ---------------------------------------------------------------------------
# 19. Accepted DLH-5I b100 scalar-anchor identity from read-only evidence
# ---------------------------------------------------------------------------


def test_b100_anchor_identity_matches_accepted_dlh5i_evidence():
    """Values copied verbatim from the accepted DLH-5I evidence
    DLH_5I_BOUNDARY_DIAGNOSTICS.csv (read-only)."""
    a77 = mod.b100_anchor("a77")
    assert a77["variant"] == "I2_A77_B100"
    assert a77["requested_max"] == 1.925385153e-01
    assert a77["requested_count"] == 4
    assert a77["requested_share"] == 2.597402597e-02
    assert a77["raw_max"] == 7.093524248e-02
    assert a77["argmax_index"] == (99, 76, 1)
    assert a77["argmax_physical"] == (34.473684210526315, 10.0, 1.3)
    assert a77["upper_a_requested_max"] == 0.0
    assert a77["b_hi"] == 655.0 / 19.0
    assert a77["b_pts"] == 100

    a153 = mod.b100_anchor("a153")
    assert a153["variant"] == "I5_A153_B100"
    assert a153["requested_max"] == 2.481811687e-01
    assert a153["requested_count"] == 8
    assert a153["requested_share"] == 2.614379085e-02
    assert a153["raw_max"] == 9.143516741e-02
    assert a153["argmax_index"] == (99, 152, 1)
    assert a153["argmax_physical"] == (34.473684210526315, 10.0, 1.3)
    assert a153["upper_a_requested_max"] == 0.0

    ident = mod.b100_anchor_identity(_cfg())
    assert ident["a77"]["rerun_in_dlh5j"] is False
    assert ident["a153"]["rerun_in_dlh5j"] is False
    assert "READ_ONLY" in ident["a77"]["provenance"]


# ---------------------------------------------------------------------------
# Canonical six-variant execution (real accepted HJB solves)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def canonical():
    cfg = mod.load_config(CONFIG_PATH)
    dlh5b, params, numerics = mod.build_fixture(cfg)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    trends = mod.extent_trends(cfg, runs)
    res = mod.cross_a_policy_comparisons(cfg, runs)
    return cfg, runs, trends, res


def test_canonical_all_six_converge_and_terminal_class(canonical):
    cfg, runs, _trends, res = canonical
    assert len(runs["variants"]) == 6
    assert all(v["hjb_converged"] for v in runs["variants"])
    assert all(v["grid"]["a_pts"] in (77, 153) for v in runs["variants"])
    assert all(abs(v["grid"]["db"] - mod.DB0) <= 1e-12 for v in runs["variants"])
    assert all(v["grid"]["b_pts"] in (120, 140, 160) for v in runs["variants"])
    repro = {"pass_bool": True}
    term = mod.overall_terminal(cfg, runs, repro, res)
    assert term["terminal"] in (mod.TERMINAL_OUTCOME_A, mod.TERMINAL_OUTCOME_B,
                                mod.TERMINAL_OUTCOME_C, mod.TERMINAL_OUTCOME_D)
    assert term["terminal"] not in (mod.TERMINAL_OUTCOME_E, mod.TERMINAL_OUTCOME_F)


def test_canonical_upper_a_zero_and_joint_marker_consistency(canonical):
    cfg, runs, _trends, _res = canonical
    for v in runs["variants"]:
        ua = next(b for b in v["boundary"]["boundaries"] if b["boundary"] == "upper_a")
        assert ua["requested"]["max"] == 0.0
        ub = next(b for b in v["boundary"]["boundaries"] if b["boundary"] == "upper_b")
        lb = next(b for b in v["boundary"]["boundaries"] if b["boundary"] == "lower_b")
        la = next(b for b in v["boundary"]["boundaries"] if b["boundary"] == "lower_a")
        assert la["requested"]["max"] == 0.0
        assert lb["requested"]["max"] == 0.0
        # joint marker consistent with requested rates
        expect_joint = bool(ua["requested"]["max"] <= cfg.boundary_threshold
                            and ub["requested"]["max"] <= cfg.boundary_threshold)
        assert v["joint_compatible"] == expect_joint
        assert v["joint_marker"] == (mod.JOINT_COMPATIBLE if expect_joint else mod.JOINT_NOT_COMPATIBLE)


def test_canonical_trends_include_accepted_b100_anchors(canonical):
    cfg, runs, trends, _res = canonical
    for a_res in mod.A_RES_ORDER:
        seq = trends["sequences"][a_res]
        assert seq["entries"][0]["is_anchor"] is True
        assert seq["entries"][0]["variant"] == (
            "I2_A77_B100" if a_res == "a77" else "I5_A153_B100")
        # continuation variants are exactly the three J variants for this a_res
        cont = [e["variant"] for e in seq["entries"][1:]]
        assert cont == [vid for vid in mod.VARIANT_IDS if vid.split("_")[1].lower() == a_res]
        assert all(e["upper_a_compatible"] for e in seq["entries"])
