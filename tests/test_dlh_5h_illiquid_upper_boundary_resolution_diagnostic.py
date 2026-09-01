"""DLH-5H (Issue #34) focused tests.

Covers the Issue #34 minimum tests:

1. exact six-variant identity
2. fixed physical a domain and a_max=10 across all variants
3. exact unchanged taper identity/value on every common physical a node
4. H0/H1/H2/H3 exact nested a alignment
5. H1/H4 and H2/H5 exact every-second b alignment
6. fresh initialization / no warm-start plumbing
7. raw + requested upper/lower a reconstruction
8. threshold relation raw_threshold = 1e-10*da
9. complete offending-state evidence
10. upper/lower b regression reconstruction
11. a-resolution attenuation-ratio calculation
12. exact aligned policy comparison on all five required pairs
13. joint HJB boundary compatibility marker
14. no stationary/KFE/density/tail/aggregate execution path
15. deterministic repeat with non-finite-aware comparison
16. accepted HJB source identity unchanged
17. canonical six-variant execution; H0 reproduces accepted DLH-5G G2 facts
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

import deep_learning_hank.two_asset.illiquid_upper_boundary_resolution_diagnostic as mod

CONFIG_PATH = "configs/dlh_5h_illiquid_upper_boundary_resolution_diagnostic.toml"
ORACLE_PATH = pathlib.Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")


def _cfg():
    return mod.load_config(CONFIG_PATH)


def _tiny_grid(nb=8, na=6):
    b = np.linspace(-2.0, 19.736842105263158, nb)
    a = np.linspace(0.0, 10.0, na)
    z = np.array([0.8, 1.3])
    switch = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    return MatlabFaithfulHJBGrid(b, a, z, switch)


def _fake_hjb(shape, mu_a=None, mu_b=None, value=None, db=1.0, da=1.0):
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


def _fake_variant_record(variant, hjb_statistic=1.0, raw_max=1.0, req_max=1.0,
                         count=0, share=0.0, ub_max=0.0, offending=()):
    """Minimal JSON-safe variant record shaped like run_all_variants output."""
    def _bd(name, direction, maxv, cnt, shr, off):
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
                "max": req_max if name == "upper_a" else maxv,
                "count_above_threshold": cnt, "share_above_threshold": shr,
                "argmax_index": (1, 1, 1), "argmax_physical": (1.0, 10.0, 0.8),
                "value_at_argmax": req_max if name == "upper_a" else maxv,
                "quantiles": {"q50": 1.0, "q90": 2.0, "q95": 3.0, "q99": 4.0},
                "offending_states": [
                    {"b_index": o[0], "a_index": o[1], "z_index": o[2],
                     "b": 1.0, "a": 10.0, "z": 0.8, "rate": float(o[3])} for o in off
                ],
            },
        }
    return {
        "variant": variant,
        "grid": {"b_pts": 60, "db": float(mod.DB0), "a_pts": 20, "da": float(mod.DA0)},
        "frozen_prices_identity": {"wbar": 1.0, "r_a": 0.03},
        "hjb_converged": True,
        "hjb_iterations": 11,
        "hjb_statistic": hjb_statistic,
        "illiquid": {
            "max_raw_upper_a": raw_max,
            "max_raw_lower_a": 0.0,
            "boundaries": [
                _bd("upper_a", "a_forward", raw_max, count, share, offending),
                _bd("lower_a", "a_backward", 0.0, 0, 0.0, ()),
            ],
        },
        "liquid": {
            "max_raw_upper_b": ub_max,
            "max_raw_lower_b": 0.0,
            "boundaries": [
                _bd("upper_b", "b_forward", ub_max, 1 if ub_max > 0 else 0,
                    1.0 / 120.0 if ub_max > 0 else 0.0, ()),
                _bd("lower_b", "b_backward", 0.0, 0, 0.0, ()),
            ],
        },
        "joint_compatible": bool(ub_max <= 1e-10 and (req_max if variant.startswith("H") else raw_max) <= 1e-10),
        "joint_marker": "JOINT_HJB_BOUNDARY_POLICY_COMPATIBLE" if (
            ub_max <= 1e-10 and (req_max if variant.startswith("H") else raw_max) <= 1e-10
        ) else "JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE",
        "variant_terminal": "HJB_CONVERGED",
    }


# ---------------------------------------------------------------------------
# 1. Exact six-variant plan identity
# ---------------------------------------------------------------------------


def test_exact_six_variant_plan_identity():
    cfg = _cfg()
    plan = mod.grid_plan_identity(cfg)
    ids = list(plan["variants"].keys())
    assert ids == ["H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST",
                   "H4_B119_A39", "H5_B119_A77"]
    for hid in ("H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST"):
        assert plan["variants"][hid]["b_pts"] == 60
        assert abs(plan["variants"][hid]["db"] - mod.DB0) <= 1e-12
    assert [plan["variants"][h]["a_pts"] for h in
            ("H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST")] == [20, 39, 77, 153]
    assert abs(plan["variants"]["H1_A39_FINE"]["da"] - mod.DA0 / 2) <= 1e-12
    assert abs(plan["variants"]["H2_A77_FINER"]["da"] - mod.DA0 / 4) <= 1e-12
    assert abs(plan["variants"]["H3_A153_FINEST"]["da"] - mod.DA0 / 8) <= 1e-12
    for hid in ("H4_B119_A39", "H5_B119_A77"):
        assert plan["variants"][hid]["b_pts"] == 119
        assert abs(plan["variants"][hid]["db"] - mod.DB0 / 2) <= 1e-12


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
    h0 = grids["H0_A20_BASE"]
    # every common physical a node has the identical accepted taper value:
    # H0 nodes appear as every 2nd/4th/8th node of H1/H2/H3
    assert np.allclose(matlab_faithful_illiquid_return(h0.a, a_max, r_a),
                       matlab_faithful_illiquid_return(grids["H1_A39_FINE"].a[::2], a_max, r_a), atol=1e-15)
    assert np.allclose(matlab_faithful_illiquid_return(h0.a, a_max, r_a),
                       matlab_faithful_illiquid_return(grids["H2_A77_FINER"].a[::4], a_max, r_a), atol=1e-15)
    assert np.allclose(matlab_faithful_illiquid_return(h0.a, a_max, r_a),
                       matlab_faithful_illiquid_return(grids["H3_A153_FINEST"].a[::8], a_max, r_a), atol=1e-15)
    # H4/H5 share physical a nodes with H1/H2 respectively
    assert np.allclose(matlab_faithful_illiquid_return(grids["H1_A39_FINE"].a, a_max, r_a),
                       matlab_faithful_illiquid_return(grids["H4_B119_A39"].a, a_max, r_a), atol=1e-15)
    assert np.allclose(matlab_faithful_illiquid_return(grids["H2_A77_FINER"].a, a_max, r_a),
                       matlab_faithful_illiquid_return(grids["H5_B119_A77"].a, a_max, r_a), atol=1e-15)


# ---------------------------------------------------------------------------
# 4/5. Nesting and alignment
# ---------------------------------------------------------------------------


def test_h0_h3_nested_a_alignment():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    assert np.allclose(grids["H1_A39_FINE"].a[::2], grids["H0_A20_BASE"].a, atol=1e-12)
    assert np.allclose(grids["H2_A77_FINER"].a[::2], grids["H1_A39_FINE"].a, atol=1e-12)
    assert np.allclose(grids["H3_A153_FINEST"].a[::2], grids["H2_A77_FINER"].a, atol=1e-12)
    # identical core b60 grid on H0-H3
    for hid in ("H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST"):
        assert np.allclose(grids[hid].b, grids["H0_A20_BASE"].b, atol=1e-12)


def test_h1_h4_and_h2_h5_every_second_b_alignment():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    assert np.allclose(grids["H4_B119_A39"].b[::2], grids["H1_A39_FINE"].b, atol=1e-12)
    assert np.allclose(grids["H5_B119_A77"].b[::2], grids["H2_A77_FINER"].b, atol=1e-12)
    # same physical b domain
    assert grids["H4_B119_A39"].b[0] == grids["H1_A39_FINE"].b[0] == -2.0
    assert grids["H4_B119_A39"].b[-1] == grids["H1_A39_FINE"].b[-1]


# ---------------------------------------------------------------------------
# 6. Fresh initialization / no warm-start
# ---------------------------------------------------------------------------


def test_fresh_initialization_per_variant(monkeypatch):
    cfg = _cfg()
    dlh5b, params, numerics = mod.build_fixture(cfg)
    calls = []
    orig = mod.household_initial_condition

    def fake_initial_condition(grid, *a, **k):
        calls.append((grid.b.size, grid.a.size))
        return orig(grid, *a, **k)

    monkeypatch.setattr(mod, "household_initial_condition", fake_initial_condition)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    assert calls == [(60, 20), (60, 39), (60, 77), (60, 153), (119, 39), (119, 77)]
    assert all(v["hjb_converged"] for v in runs["variants"])


# ---------------------------------------------------------------------------
# 7/8/9. Boundary diagnostics (raw + requested, coords, offending)
# ---------------------------------------------------------------------------


def _boundary_fixture():
    grid = _tiny_grid(nb=8, na=6)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    # upper-a slice shape (b=8, z=2). Raw values as fractions of da.
    ua = np.zeros((8, 2))
    ua[1, 0] = 0.1 * da
    ua[3, 1] = 0.2 * da
    ua[5, 1] = 0.6 * da
    mu_a = np.zeros((8, 6, 2))
    mu_a[:, 5, :] = ua
    return grid, db, da, mu_a


def test_raw_and_requested_upper_lower_a_reconstruction():
    grid, db, da, mu_a = _boundary_fixture()
    hjb = _fake_hjb((8, 6, 2), mu_a=mu_a)
    ill = mod.illiquid_boundary_diagnostics(hjb, grid, da, 1e-10)
    ua = next(b for b in ill["boundaries"] if b["boundary"] == "upper_a")
    raw, req = ua["raw"], ua["requested"]
    assert raw["argmax_index"] == (5, 5, 1)
    assert raw["argmax_physical"] == (float(grid.b[5]), 10.0, 1.3)
    assert abs(raw["max"] - 0.6 * da) <= 1e-12
    assert abs(req["max"] - 0.6) <= 1e-12
    assert req["count_above_threshold"] == 3
    assert abs(req["share_above_threshold"] - 3.0 / 16.0) <= 1e-12
    la = next(b for b in ill["boundaries"] if b["boundary"] == "lower_a")
    assert la["raw"]["max"] == 0.0
    assert la["raw"]["argmax_physical"] == (-2.0, 0.0, 0.8)


def test_threshold_relation_raw_1e10_da():
    grid, db, da, mu_a = _boundary_fixture()
    hjb = _fake_hjb((8, 6, 2), mu_a=mu_a)
    ill = mod.illiquid_boundary_diagnostics(hjb, grid, da, 1e-10)
    ua = next(b for b in ill["boundaries"] if b["boundary"] == "upper_a")
    # raw threshold = 1e-10*da; the three positive values all exceed it
    assert ua["raw"]["count_above_threshold"] == 3
    assert ua["requested"]["count_above_threshold"] == 3
    assert abs(ua["raw"]["max"] - ua["requested"]["max"] * da) <= 1e-12


def test_complete_offending_states():
    grid, db, da, mu_a = _boundary_fixture()
    hjb = _fake_hjb((8, 6, 2), mu_a=mu_a)
    ill = mod.illiquid_boundary_diagnostics(hjb, grid, da, 1e-10)
    ua = next(b for b in ill["boundaries"] if b["boundary"] == "upper_a")
    req = ua["requested"]
    states = {(o["b_index"], o["a_index"], o["z_index"]) for o in req["offending_states"]}
    assert states == {(5, 5, 1), (3, 5, 1), (1, 5, 0)}
    rates = {o["rate"] for o in req["offending_states"]}
    assert rates == {0.1, 0.2, 0.6}
    idxs = [(o["b_index"], o["a_index"], o["z_index"]) for o in req["offending_states"]]
    assert idxs == sorted(idxs)


# ---------------------------------------------------------------------------
# 10. Liquid regression reconstruction
# ---------------------------------------------------------------------------


def test_liquid_regression_reconstruction():
    grid, db, da, mu_a = _boundary_fixture()
    nb = grid.b.size
    mu_b = np.zeros((nb, 6, 2))
    mu_b[nb - 1, 4, 1] = 0.3 * db
    hjb = _fake_hjb((nb, 6, 2), mu_a=mu_a, mu_b=mu_b)
    liq = mod.liquid_regression_diagnostics(hjb, grid, db, 1e-10)
    ub = next(b for b in liq["boundaries"] if b["boundary"] == "upper_b")
    assert ub["raw"]["max"] == 0.3 * db
    assert abs(ub["requested"]["max"] - 0.3) <= 1e-12
    assert ub["requested"]["count_above_threshold"] == 1
    assert ub["requested"]["argmax_index"] == (nb - 1, 4, 1)
    lb = next(b for b in liq["boundaries"] if b["boundary"] == "lower_b")
    assert lb["raw"]["max"] == 0.0


# ---------------------------------------------------------------------------
# 11. A-resolution attenuation ratios
# ---------------------------------------------------------------------------


def test_a_resolution_attenuation_ratios():
    cfg = _cfg()
    raw = [1.0, 0.5, 0.25, 0.0]
    req = [0.6, 0.4, 0.2, 0.0]
    recs = []
    for i, vid in enumerate(("H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST")):
        rec = _fake_variant_record(vid, raw_max=raw[i], req_max=req[i], count=1, share=0.01)
        recs.append(rec)
    trend = mod.resolution_trend(cfg, {"variants": recs})
    seq = [s for s in trend["sequence"] if s.get("reached")]
    assert [s["raw_max"] for s in seq] == [1.0, 0.5, 0.25, 0.0]
    assert trend["ratios"]["adjacent_raw"] == [2.0, 2.0, "inf"]
    assert trend["ratios"]["vs_H0_raw"] == [0.5, 0.25, 0.0]
    assert trend["ratios"]["vs_H0_requested"] == [
        pytest.approx(0.4 / 0.6, abs=1e-6), pytest.approx(0.2 / 0.6, abs=1e-6), 0.0,
    ]
    assert trend["first_requested_below_threshold"] == "H3_A153_FINEST"
    assert trend["strictly_decreasing_raw"] is True
    assert trend["plateau"] is False


# ---------------------------------------------------------------------------
# 12. Aligned policy comparison on all five pairs
# ---------------------------------------------------------------------------


def test_exact_aligned_policy_comparison_all_five_pairs():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    hjb_results = {}
    variants = []
    for vid, g in grids.items():
        shape = (g.b.size, g.a.size, g.z.size)
        hjb_results[vid] = _fake_hjb(shape, value=np.full(shape, 0.5))
        variants.append(_fake_variant_record(vid, raw_max=0.1, req_max=0.1))
    res = mod.policy_stability(cfg, {"hjb_results": hjb_results, "variants": variants})
    assert [c["comparison"] for c in res] == [
        "H0_vs_H1", "H1_vs_H2", "H2_vs_H3", "H1_vs_H4", "H2_vs_H5"]
    assert [c["kind"] for c in res] == ["a", "a", "a", "b", "b"]
    for c in res:
        assert c["reached"] is True
        # coarse value=0.5, fine value=0.5 -> max_abs_diff 0
        assert c["fields"]["value"]["max_abs_diff"] == 0.0
        assert c["fields"]["value"]["rel_diff"] == 0.0
        for f in ("consumption", "labor", "transfer", "mu_a", "mu_b"):
            assert c["fields"][f]["max_abs_diff"] == 0.0
        assert c["fields"]["liquid_label"]["mismatch_count"] == 0
        assert c["fields"]["transfer_label"]["mismatch_count"] == 0


# ---------------------------------------------------------------------------
# 13. Joint compatibility marker + terminal classification
# ---------------------------------------------------------------------------


def test_joint_compatibility_marker():
    cfg = _cfg()
    # not compatible: ub=0, ua material
    r1 = _fake_variant_record("H0_A20_BASE", raw_max=0.3, req_max=0.3, ub_max=0.0)
    assert r1["joint_marker"] == mod.JOINT_NOT_COMPATIBLE
    assert r1["joint_compatible"] is False
    # compatible: ub=0, ua <= 1e-10
    r2 = _fake_variant_record("H1_A39_FINE", raw_max=0.0, req_max=0.0, ub_max=0.0)
    assert r2["joint_marker"] == mod.JOINT_COMPATIBLE
    assert r2["joint_compatible"] is True


def test_terminal_classification_matrix():
    cfg = _cfg()
    # Outcome A: any joint-compatible variant
    runs = {
        "variants": [
            _fake_variant_record("H0_A20_BASE", raw_max=0.3, req_max=0.3, ub_max=0.0),
            _fake_variant_record("H1_A39_FINE", raw_max=0.0, req_max=0.0, ub_max=0.0),
            _fake_variant_record("H2_A77_FINER", raw_max=0.0, req_max=0.0, ub_max=0.0),
            _fake_variant_record("H3_A153_FINEST", raw_max=0.0, req_max=0.0, ub_max=0.0),
            _fake_variant_record("H4_B119_A39", raw_max=0.0, req_max=0.0, ub_max=0.0),
            _fake_variant_record("H5_B119_A77", raw_max=0.0, req_max=0.0, ub_max=0.0),
        ]
    }
    term = mod.overall_terminal(cfg, runs, {"pass_bool": True}, [])
    assert term["terminal"] == mod.TERMINAL_OUTCOME_A

    # Outcome D: liquid reactivation (ub material) with NO joint compatibility
    runs_d = {
        "variants": [
            _fake_variant_record("H0_A20_BASE", raw_max=0.3, req_max=0.3, ub_max=0.05),
            _fake_variant_record("H1_A39_FINE", raw_max=0.2, req_max=0.2, ub_max=0.0),
            _fake_variant_record("H2_A77_FINER", raw_max=0.1, req_max=0.1, ub_max=0.0),
            _fake_variant_record("H3_A153_FINEST", raw_max=0.05, req_max=0.05, ub_max=0.0),
            _fake_variant_record("H4_B119_A39", raw_max=0.05, req_max=0.05, ub_max=0.0),
            _fake_variant_record("H5_B119_A77", raw_max=0.05, req_max=0.05, ub_max=0.0),
        ]
    }
    term_d = mod.overall_terminal(cfg, runs_d, {"pass_bool": True}, [])
    assert term_d["terminal"] == mod.TERMINAL_OUTCOME_D

    # Outcome B: no joint compat, no liquid reactivation, clean attenuation
    runs_b = {
        "variants": [
            _fake_variant_record("H0_A20_BASE", raw_max=0.3, req_max=0.3, ub_max=0.0),
            _fake_variant_record("H1_A39_FINE", raw_max=0.1, req_max=0.1, ub_max=0.0),
            _fake_variant_record("H2_A77_FINER", raw_max=0.02, req_max=0.02, ub_max=0.0),
            _fake_variant_record("H3_A153_FINEST", raw_max=0.005, req_max=0.005, ub_max=0.0),
            _fake_variant_record("H4_B119_A39", raw_max=0.004, req_max=0.004, ub_max=0.0),
            _fake_variant_record("H5_B119_A77", raw_max=0.004, req_max=0.004, ub_max=0.0),
        ]
    }
    term_b = mod.overall_terminal(cfg, runs_b, {"pass_bool": True}, [])
    assert term_b["terminal"] == mod.TERMINAL_OUTCOME_B

    # Outcome F: repro fail
    term_f = mod.overall_terminal(cfg, runs_b, {"pass_bool": False}, [])
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
    assert mod.NOT_AUTHORIZED_MARKER == "NOT_AUTHORIZED__DLH_5H_POLICY_ONLY_ILLIQUID_RESOLUTION_DIAGNOSTIC"


# ---------------------------------------------------------------------------
# 15. Deterministic repeat (structural + numeric + non-finite-aware)
# ---------------------------------------------------------------------------


def test_deterministic_nonfinite_aware_repeat_comparison():
    cfg = _cfg()
    r1 = _fake_variant_record("H0_A20_BASE", hjb_statistic=1.5e-8, raw_max=0.3, req_max=0.3,
                              count=2, share=0.05, ub_max=0.0, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    r2 = _fake_variant_record("H0_A20_BASE", hjb_statistic=1.5e-8, raw_max=0.3, req_max=0.3,
                              count=2, share=0.05, ub_max=0.0, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    cmp = mod.compare_variant_records(r1, r2, cfg)
    assert cmp["identical_structural_signature"] is True
    assert cmp["max_numeric_diff"] == 0.0
    assert cmp["mismatched_fields"] == 0
    assert cmp["pass_bool"] is True

    r3 = _fake_variant_record("H0_A20_BASE", hjb_statistic=2.5e-8, raw_max=0.3, req_max=0.3,
                              count=2, share=0.05, ub_max=0.0, offending=((1, 1, 1, 0.3), (2, 1, 1, 0.2)))
    cmp3 = mod.compare_variant_records(r1, r3, cfg)
    assert cmp3["identical_structural_signature"] is True
    assert cmp3["max_numeric_diff"] == pytest.approx(1.0e-8, abs=1e-12)
    assert cmp3["mismatched_fields"] == 0
    assert cmp3["pass_bool"] is False

    # aligned non-finite: identical NaN max on both -> pass
    r4 = _fake_variant_record("H0_A20_BASE")
    r4["illiquid"]["boundaries"][0]["raw"]["max"] = float("nan")
    r5 = _fake_variant_record("H0_A20_BASE")
    r5["illiquid"]["boundaries"][0]["raw"]["max"] = float("nan")
    cmp5 = mod.compare_variant_records(r4, r5, cfg)
    assert cmp5["pass_bool"] is True
    assert cmp5["aligned_nonfinite_fields"] >= 1

    # NaN vs finite -> mismatch, fail
    r6 = _fake_variant_record("H0_A20_BASE")
    r6["illiquid"]["boundaries"][0]["raw"]["max"] = float("nan")
    r7 = _fake_variant_record("H0_A20_BASE")
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
    monkeypatch.setattr(mod, "policy_stability", lambda cfg, runs: [])
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
# 17. Canonical six-variant execution + H0 reproduction of DLH-5G G2 facts
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def canonical():
    cfg = mod.load_config(CONFIG_PATH)
    dlh5b, params, numerics = mod.build_fixture(cfg)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    trend = mod.resolution_trend(cfg, runs)
    res = mod.policy_stability(cfg, runs)
    return cfg, runs, trend, res


def test_canonical_all_six_converge_and_terminal_class(canonical):
    cfg, runs, _trend, _res = canonical
    assert len(runs["variants"]) == 6
    assert all(v["hjb_converged"] for v in runs["variants"])
    repro = {"pass_bool": True}
    term = mod.overall_terminal(cfg, runs, repro, _res)
    assert term["terminal"] in (mod.TERMINAL_OUTCOME_A, mod.TERMINAL_OUTCOME_B,
                                mod.TERMINAL_OUTCOME_C, mod.TERMINAL_OUTCOME_D)
    assert term["terminal"] not in (mod.TERMINAL_OUTCOME_E, mod.TERMINAL_OUTCOME_F)
    seq = [s for s in _trend["sequence"] if s.get("reached")]
    assert [s["variant"] for s in seq] == ["H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST"]


def test_h0_reproduces_accepted_dlh5g_g2_facts(canonical):
    _cfg_, runs, _trend, _res = canonical
    h0 = next(v for v in runs["variants"] if v["variant"] == "H0_A20_BASE")
    ua = next(b for b in h0["illiquid"]["boundaries"] if b["boundary"] == "upper_a")
    req = ua["requested"]
    # accepted DLH-5G G2 = H0: upper-a requested 0.30947308540162455, 108 states,
    # argmax (22,19,0) physical (6.105263157894736, 10.0, 0.8)
    assert abs(req["max"] - 0.30947308540162455) <= 2e-9
    assert req["count_above_threshold"] == 108
    assert req["argmax_index"] == (22, 19, 0)
    assert req["argmax_physical"] == (6.105263157894736, 10.0, 0.8)
    # liquid-safe domain non-binding: H0 upper-b requested is zero
    ub = next(b for b in h0["liquid"]["boundaries"] if b["boundary"] == "upper_b")
    assert ub["requested"]["max"] == 0.0
    assert h0["joint_marker"] == mod.JOINT_NOT_COMPATIBLE
