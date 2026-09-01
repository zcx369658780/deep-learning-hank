"""DLH-5I (Issue #35) focused tests.

Covers the Issue #35 minimum tests:

1. exact six-variant identity
2. fixed physical a domain and a_max=10 across all variants
3. exact unchanged taper identity/value on every common physical a node
4. exact a77/a153 nesting (a77 nodes = every second a153 node)
5. exact b60/b80/b100 same-spacing nesting
6. exact same-b-extent cross-a physical-grid identity
7. fresh initialization / no warm-start plumbing
8. raw + requested diagnostics for all four asset boundaries
9. threshold relations raw_threshold = 1e-10*spacing
10. complete offending-state evidence
11. separate A77 and A153 b-extent trend calculations
12. exact aligned cross-a policy comparison on all three required pairs
13. per-variant joint compatibility marker + per-b-extent cross-a frontier marker
14. no stationary/KFE/density/tail/aggregate execution path
15. deterministic repeat with non-finite-aware comparison
16. accepted HJB source identity unchanged
17. canonical six-variant execution; I0 reproduces accepted DLH-5H H2 facts and
    I3 reproduces accepted DLH-5H H3 facts within frozen tolerance
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

import deep_learning_hank.two_asset.coupled_boundary_frontier_diagnostic as mod

CONFIG_PATH = "configs/dlh_5i_coupled_boundary_frontier_diagnostic.toml"
ORACLE_PATH = pathlib.Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")

_A_PTS = {"a77": 77, "a153": 153}
_B_PTS = {"b60": 60, "b80": 80, "b100": 100}
_B_HI = {"b60": 375.0 / 19.0, "b80": 515.0 / 19.0, "b100": 655.0 / 19.0}


def _cfg():
    return mod.load_config(CONFIG_PATH)


def _tiny_grid(nb=8, na=6):
    b = np.linspace(-2.0, 19.736842105263158, nb)
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
    variant (I0..I5) upper-b requested maxima and upper-a requested maxima."""
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
    assert abs(plan["b_extents"]["b60"]["b_hi"] - 375.0 / 19.0) <= 1e-12
    assert abs(plan["b_extents"]["b80"]["b_hi"] - 515.0 / 19.0) <= 1e-12
    assert abs(plan["b_extents"]["b100"]["b_hi"] - 655.0 / 19.0) <= 1e-12


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
    a77 = grids["I0_A77_B60"]
    a153 = grids["I3_A153_B60"]
    # every common physical a node has the identical accepted taper value:
    # a77 nodes appear as every 2nd a153 node at every b extent
    assert np.allclose(matlab_faithful_illiquid_return(a77.a, a_max, r_a),
                       matlab_faithful_illiquid_return(a153.a[::2], a_max, r_a), atol=1e-15)
    # all a77 variants share identical physical a nodes; all a153 variants too
    for vid, g in grids.items():
        if vid.startswith(("I0", "I1", "I2")):
            assert np.allclose(g.a, a77.a, atol=1e-12)
        else:
            assert np.allclose(g.a, a153.a, atol=1e-12)
    assert np.allclose(matlab_faithful_illiquid_return(grids["I4_A153_B80"].a[::2], a_max, r_a),
                       matlab_faithful_illiquid_return(a77.a, a_max, r_a), atol=1e-15)
    assert np.allclose(matlab_faithful_illiquid_return(grids["I5_A153_B100"].a[::2], a_max, r_a),
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
    # a77 nodes = every second a153 node at every b extent
    for cid, fid in (("I0_A77_B60", "I3_A153_B60"),
                     ("I1_A77_B80", "I4_A153_B80"),
                     ("I2_A77_B100", "I5_A153_B100")):
        assert np.allclose(grids[fid].a[::2], grids[cid].a, atol=1e-12)
    # b60 nested in b80/b100, b80 nested in b100 (common nodes, same spacing)
    assert np.allclose(grids["I1_A77_B80"].b[:60], grids["I0_A77_B60"].b, atol=1e-12)
    assert np.allclose(grids["I2_A77_B100"].b[:60], grids["I0_A77_B60"].b, atol=1e-12)
    assert np.allclose(grids["I2_A77_B100"].b[:80], grids["I1_A77_B80"].b, atol=1e-12)
    # db identical at all extents
    for vid in mod.VARIANT_IDS:
        assert abs(grids[vid].b[1] - grids[vid].b[0] - mod.DB0) <= 1e-12


def test_same_b_extent_cross_a_grid_identity():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    for cid, fid in (("I0_A77_B60", "I3_A153_B60"),
                     ("I1_A77_B80", "I4_A153_B80"),
                     ("I2_A77_B100", "I5_A153_B100")):
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
    assert calls == [(60, 77), (80, 77), (100, 77), (60, 153), (80, 153), (100, 153)]
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
    assert ua["raw"]["argmax_physical"] == (float(grid.b[5]), 10.0, 1.3)
    assert abs(ua["raw"]["max"] - 0.6 * da) <= 1e-12
    assert abs(ua["requested"]["max"] - 0.6) <= 1e-12
    assert ua["requested"]["count_above_threshold"] == 3
    assert abs(ua["requested"]["share_above_threshold"] - 3.0 / 16.0) <= 1e-12
    la = next(b for b in bd["boundaries"] if b["boundary"] == "lower_a")
    assert la["raw"]["max"] == 0.0
    ub = next(b for b in bd["boundaries"] if b["boundary"] == "upper_b")
    assert ub["raw"]["max"] == 0.3 * db
    assert abs(ub["requested"]["max"] - 0.3) <= 1e-12
    assert ub["requested"]["count_above_threshold"] == 1
    assert ub["requested"]["argmax_index"] == (7, 4, 1)
    lb = next(b for b in bd["boundaries"] if b["boundary"] == "lower_b")
    assert lb["raw"]["max"] == 0.0
    assert abs(bd["max_raw_upper_a"] - 0.6 * da) <= 1e-12
    assert abs(bd["max_raw_upper_b"] - 0.3 * db) <= 1e-12
    assert bd["max_raw_lower_a"] == 0.0
    assert bd["max_raw_lower_b"] == 0.0


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
# 11. Separate A77 and A153 b-extent trend calculations
# ---------------------------------------------------------------------------


def test_extent_trends_separate_sequences():
    cfg = _cfg()
    recs = _six_fake_records({
        ("I0_A77_B60", "ub"): 0.4, ("I0_A77_B60", "ub_raw"): 0.15, ("I0_A77_B60", "ub_cnt"): 7,
        ("I1_A77_B80", "ub"): 0.2, ("I1_A77_B80", "ub_raw"): 0.08, ("I1_A77_B80", "ub_cnt"): 3,
        ("I2_A77_B100", "ub"): 0.05, ("I2_A77_B100", "ub_raw"): 0.02, ("I2_A77_B100", "ub_cnt"): 1,
        ("I3_A153_B60", "ub"): 0.5, ("I3_A153_B60", "ub_raw"): 0.18, ("I3_A153_B60", "ub_cnt"): 13,
        ("I4_A153_B80", "ub"): 0.25, ("I4_A153_B80", "ub_raw"): 0.09, ("I4_A153_B80", "ub_cnt"): 5,
        ("I5_A153_B100", "ub"): 0.1, ("I5_A153_B100", "ub_raw"): 0.035, ("I5_A153_B100", "ub_cnt"): 2,
    })
    trends = mod.extent_trends(cfg, {"variants": recs})
    s77 = trends["sequences"]["a77"]
    assert [e["variant"] for e in s77["entries"]] == ["I0_A77_B60", "I1_A77_B80", "I2_A77_B100"]
    assert [e["b_extent"] for e in s77["entries"]] == ["b60", "b80", "b100"]
    assert s77["requested_seq"] == [0.4, 0.2, 0.05]
    assert s77["strictly_decreasing_requested"] is True
    assert s77["adjacent_requested"] == [2.0, 4.0]
    assert s77["vs_b60_requested"] == [1.0, 0.5, 0.125]
    assert s77["upper_a_compatible_on_all_extents"] is True
    s153 = trends["sequences"]["a153"]
    assert [e["variant"] for e in s153["entries"]] == ["I3_A153_B60", "I4_A153_B80", "I5_A153_B100"]
    assert s153["requested_seq"] == [0.5, 0.25, 0.1]
    assert s153["strictly_decreasing_requested"] is True


def test_extent_trends_non_monotonic_detected():
    cfg = _cfg()
    recs = _six_fake_records({
        ("I0_A77_B60", "ub"): 0.4, ("I1_A77_B80", "ub"): 0.05, ("I2_A77_B100", "ub"): 0.4,
    })
    trends = mod.extent_trends(cfg, {"variants": recs})
    s77 = trends["sequences"]["a77"]
    assert s77["strictly_decreasing_requested"] is False
    assert s77["monotonic_flag"] == "non_monotonic"
    assert s77["upper_a_compatible_on_all_extents"] is True


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
        "I0_A77_B60_vs_I3_A153_B60",
        "I1_A77_B80_vs_I4_A153_B80",
        "I2_A77_B100_vs_I5_A153_B100",
    ]
    assert [c["b_extent"] for c in res] == ["b60", "b80", "b100"]
    for c in res:
        assert c["reached"] is True
        assert c["fields"]["value"]["max_abs_diff"] == 0.0
        assert c["fields"]["value"]["rel_diff"] == 0.0
        for f in ("consumption", "labor", "transfer", "mu_a", "mu_b"):
            assert c["fields"][f]["max_abs_diff"] == 0.0
        assert c["fields"]["liquid_label"]["mismatch_count"] == 0
        assert c["fields"]["transfer_label"]["mismatch_count"] == 0


# ---------------------------------------------------------------------------
# 13. Joint compatibility marker + per-extent cross-a frontier
# ---------------------------------------------------------------------------


def test_joint_compatibility_marker():
    cfg = _cfg()
    r1 = _fake_variant_record("I0_A77_B60", "a77", "b60", ua_req=0.3, ub_req=0.0)
    assert r1["joint_marker"] == mod.JOINT_NOT_COMPATIBLE
    r2 = _fake_variant_record("I1_A77_B80", "a77", "b80", ua_req=0.0, ub_req=0.0)
    assert r2["joint_marker"] == mod.JOINT_COMPATIBLE


def test_cross_a_joint_frontier_marker():
    cfg = _cfg()
    # b60: only a77 compatible -> NOT; b80: both compatible -> CROSS_A_COMPATIBLE
    recs = _six_fake_records({
        ("I0_A77_B60", "ub"): 0.0,
        ("I3_A153_B60", "ub"): 0.4,
        ("I1_A77_B80", "ub"): 0.0,
        ("I4_A153_B80", "ub"): 0.0,
        ("I2_A77_B100", "ub"): 0.0,
        ("I5_A153_B100", "ub"): 0.4,
    })
    frontier = mod.joint_frontier(cfg, {"variants": recs})
    assert [p["variant"] for p in frontier["per_variant"]] == mod.VARIANT_IDS
    by_ext = {e["b_extent"]: e for e in frontier["extents"]}
    assert by_ext["b60"]["a77_joint_compatible"] is True
    assert by_ext["b60"]["a153_joint_compatible"] is False
    assert by_ext["b60"]["cross_a_joint_compatible"] is False
    assert by_ext["b60"]["marker"] == mod.CROSS_A_NOT_COMPATIBLE
    assert by_ext["b80"]["cross_a_joint_compatible"] is True
    assert by_ext["b80"]["marker"] == mod.CROSS_A_COMPATIBLE
    assert by_ext["b100"]["cross_a_joint_compatible"] is False


def test_terminal_classification_matrix():
    cfg = _cfg()
    # Outcome A: common b extent jointly compatible at both a77 and a153
    runs_a = {"variants": _six_fake_records({("I0_A77_B60", "ub"): 0.0, ("I3_A153_B60", "ub"): 0.0})}
    term = mod.overall_terminal(cfg, runs_a, {"pass_bool": True}, [])
    assert term["terminal"] == mod.TERMINAL_OUTCOME_A

    # Outcome B: joint compatibility at only one mature a resolution
    runs_b = {"variants": _six_fake_records({
        ("I0_A77_B60", "ub"): 0.0,
        ("I1_A77_B80", "ub"): 0.0,
        ("I2_A77_B100", "ub"): 0.0,
        ("I3_A153_B60", "ub"): 0.4,
        ("I4_A153_B80", "ub"): 0.3,
        ("I5_A153_B100", "ub"): 0.2,
    })}
    term_b = mod.overall_terminal(cfg, runs_b, {"pass_bool": True}, [])
    assert term_b["terminal"] == mod.TERMINAL_OUTCOME_B

    # Outcome C: both sequences attenuate but no common extent reaches threshold
    runs_c = {"variants": _six_fake_records({
        ("I0_A77_B60", "ub"): 0.4, ("I1_A77_B80", "ub"): 0.2, ("I2_A77_B100", "ub"): 0.1,
        ("I3_A153_B60", "ub"): 0.5, ("I4_A153_B80", "ub"): 0.25, ("I5_A153_B100", "ub"): 0.12,
    })}
    term_c = mod.overall_terminal(cfg, runs_c, {"pass_bool": True}, [])
    assert term_c["terminal"] == mod.TERMINAL_OUTCOME_C

    # Outcome D: non-monotonic coupled behavior
    runs_d = {"variants": _six_fake_records({
        ("I0_A77_B60", "ub"): 0.4, ("I1_A77_B80", "ub"): 0.05, ("I2_A77_B100", "ub"): 0.4,
        ("I3_A153_B60", "ub"): 0.5, ("I4_A153_B80", "ub"): 0.25, ("I5_A153_B100", "ub"): 0.1,
    })}
    term_d = mod.overall_terminal(cfg, runs_d, {"pass_bool": True}, [])
    assert term_d["terminal"] == mod.TERMINAL_OUTCOME_D

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
# 14. No stationary execution path
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
    assert mod.NOT_AUTHORIZED_MARKER == "NOT_AUTHORIZED__DLH_5I_POLICY_ONLY_COUPLED_FRONTIER_DIAGNOSTIC"


# ---------------------------------------------------------------------------
# 15. Deterministic repeat (structural + numeric + non-finite-aware)
# ---------------------------------------------------------------------------


def test_deterministic_nonfinite_aware_repeat_comparison():
    cfg = _cfg()
    r1 = _fake_variant_record("I0_A77_B60", "a77", "b60", hjb_statistic=1.5e-8,
                              ua_raw=0.3, ua_req=0.3, ub_raw=0.0, ub_req=0.0,
                              ua_cnt=2, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    r2 = _fake_variant_record("I0_A77_B60", "a77", "b60", hjb_statistic=1.5e-8,
                              ua_raw=0.3, ua_req=0.3, ub_raw=0.0, ub_req=0.0,
                              ua_cnt=2, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    cmp = mod.compare_variant_records(r1, r2, cfg)
    assert cmp["identical_structural_signature"] is True
    assert cmp["max_numeric_diff"] == 0.0
    assert cmp["mismatched_fields"] == 0
    assert cmp["pass_bool"] is True

    r3 = _fake_variant_record("I0_A77_B60", "a77", "b60", hjb_statistic=2.5e-8,
                              ua_raw=0.3, ua_req=0.3, ub_raw=0.0, ub_req=0.0,
                              ua_cnt=2, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    cmp3 = mod.compare_variant_records(r1, r3, cfg)
    assert cmp3["identical_structural_signature"] is True
    assert cmp3["max_numeric_diff"] == pytest.approx(1.0e-8, abs=1e-12)
    assert cmp3["pass_bool"] is False

    r4 = _fake_variant_record("I0_A77_B60", "a77", "b60")
    r4["boundary"]["boundaries"][0]["raw"]["max"] = float("nan")
    r5 = _fake_variant_record("I0_A77_B60", "a77", "b60")
    r5["boundary"]["boundaries"][0]["raw"]["max"] = float("nan")
    cmp5 = mod.compare_variant_records(r4, r5, cfg)
    assert cmp5["pass_bool"] is True
    assert cmp5["aligned_nonfinite_fields"] >= 1

    r6 = _fake_variant_record("I0_A77_B60", "a77", "b60")
    r6["boundary"]["boundaries"][0]["raw"]["max"] = float("nan")
    r7 = _fake_variant_record("I0_A77_B60", "a77", "b60")
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
# 16. Accepted source identity
# ---------------------------------------------------------------------------


def test_accepted_source_identity_unchanged():
    data = ORACLE_PATH.read_bytes()
    assert mod.ACCEPTED_SHA256 == hashlib.sha256(data).hexdigest().upper()
    assert mod.ACCEPTED_BLOB == "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"


# ---------------------------------------------------------------------------
# 17. Canonical six-variant execution + I0/I3 reproduction of DLH-5H H2/H3
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
    repro = {"pass_bool": True}
    term = mod.overall_terminal(cfg, runs, repro, res)
    assert term["terminal"] in (mod.TERMINAL_OUTCOME_A, mod.TERMINAL_OUTCOME_B,
                                mod.TERMINAL_OUTCOME_C, mod.TERMINAL_OUTCOME_D)
    assert term["terminal"] not in (mod.TERMINAL_OUTCOME_E, mod.TERMINAL_OUTCOME_F)


def _upper_b(v):
    return next(b for b in v["boundary"]["boundaries"] if b["boundary"] == "upper_b")


def _upper_a(v):
    return next(b for b in v["boundary"]["boundaries"] if b["boundary"] == "upper_a")


def test_i0_reproduces_accepted_dlh5h_h2_facts(canonical):
    cfg, runs, _trends, _res = canonical
    i0 = next(v for v in runs["variants"] if v["variant"] == "I0_A77_B60")
    # grid identity: a77 (da=DA0/4) x b60 (db=DB0, b_hi=375/19)
    assert i0["grid"]["a_pts"] == 77
    assert abs(i0["grid"]["da"] - mod.DA0 / 4) <= 1e-12
    assert i0["grid"]["b_pts"] == 60
    assert abs(i0["grid"]["db"] - mod.DB0) <= 1e-12
    assert abs(i0["grid"]["b_hi"] - 375.0 / 19.0) <= 1e-12
    ub = _upper_b(i0)
    req = ub["requested"]
    # accepted DLH-5H H2: requested upper-b 3.915648627e-01, 7 states,
    # argmax (59,76,1) physical (19.736842105263158, 10.0, 1.3)
    assert abs(req["max"] - mod.ACCEPTED_H2_UPPER_B_REQUESTED_MAX) <= cfg.h2_h3_repro_tol
    assert req["count_above_threshold"] == mod.ACCEPTED_H2_UPPER_B_REQUESTED_COUNT
    assert req["argmax_index"] == mod.ACCEPTED_H2_UPPER_B_REQUESTED_ARGM_INDEX
    # upper-a requested is exact zero on a77 (accepted DLH-5H H2 fact)
    ua = _upper_a(i0)
    assert ua["requested"]["max"] == 0.0
    assert i0["joint_marker"] == mod.JOINT_NOT_COMPATIBLE


def test_i3_reproduces_accepted_dlh5h_h3_facts(canonical):
    cfg, runs, _trends, _res = canonical
    i3 = next(v for v in runs["variants"] if v["variant"] == "I3_A153_B60")
    assert i3["grid"]["a_pts"] == 153
    assert abs(i3["grid"]["da"] - mod.DA0 / 8) <= 1e-12
    assert i3["grid"]["b_pts"] == 60
    assert abs(i3["grid"]["db"] - mod.DB0) <= 1e-12
    ub = _upper_b(i3)
    req = ub["requested"]
    # accepted DLH-5H H3: requested upper-b 4.449370735e-01, 13 states,
    # argmax (59,152,1) physical (19.736842105263158, 10.0, 1.3)
    assert abs(req["max"] - mod.ACCEPTED_H3_UPPER_B_REQUESTED_MAX) <= cfg.h2_h3_repro_tol
    assert req["count_above_threshold"] == mod.ACCEPTED_H3_UPPER_B_REQUESTED_COUNT
    assert req["argmax_index"] == mod.ACCEPTED_H3_UPPER_B_REQUESTED_ARGM_INDEX
    ua = _upper_a(i3)
    assert ua["requested"]["max"] == 0.0
    assert i3["joint_marker"] == mod.JOINT_NOT_COMPATIBLE
