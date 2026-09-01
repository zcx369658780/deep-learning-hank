"""DLH-5G (Issue #31) focused tests.

Covers the Issue #31 minimum tests:

1. exact six-variant plan identity
2. frozen illiquid a-grid/taper identity across all variants
3. G0-G3 exact same-spacing nesting
4. G4 every-second alignment with G0
5. G5 every-second alignment with G1
6. fresh initialization per variant (no warm-start plumbing)
7. raw upper/lower b boundary reconstruction with index+physical coordinates
8. requested-rate reconstruction and the raw threshold 1e-10*db
9. complete offending-state evidence
10. extent attenuation-ratio calculation
11. aligned b-resolution comparison on both pairs (G0/G4, G1/G5)
12. no stationary/KFE/density/tail/aggregate execution path
13. deterministic repeat (structural + numeric + non-finite-aware)
14. accepted MATLAB-faithful HJB source identity unchanged
15. canonical six-variant execution; G0/G1 reproduce accepted DLH-5F b-only facts
"""

import hashlib
import pathlib
from types import SimpleNamespace

import numpy as np
import pytest

from deep_learning_hank.two_asset import MatlabFaithfulHJBGrid

import deep_learning_hank.two_asset.liquid_upper_domain_asymptotic_diagnostic as mod

CONFIG_PATH = "configs/dlh_5g_liquid_upper_domain_asymptotic_diagnostic.toml"
ORACLE_PATH = pathlib.Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")


def _cfg():
    return mod.load_config(CONFIG_PATH)


def _tiny_grid(nb=5, na=5):
    b = np.linspace(-2.0, 5.0, nb)
    a = np.linspace(0.0, 10.0, na)
    z = np.array([0.8, 1.3])
    switch = np.array([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    return MatlabFaithfulHJBGrid(b, a, z, switch)


def _fake_hjb(shape, mu_b=None, mu_a=None, value=None, db=1.0, da=1.0):
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
                         count=0, share=0.0, offending=()):
    """Minimal JSON-safe variant record shaped like run_all_variants output."""
    return {
        "variant": variant,
        "grid": {"b_pts": 20, "db": float(mod.DB0), "a_pts": 20, "da": float(mod.DA0)},
        "frozen_prices_identity": {"wbar": 1.0, "r_a": 0.03},
        "hjb_converged": True,
        "hjb_iterations": 11,
        "hjb_statistic": hjb_statistic,
        "liquid": {
            "max_raw_upper_b": raw_max,
            "max_raw_lower_b": 0.0,
            "boundaries": [
                {
                    "boundary": "upper_b",
                    "direction": "b_forward",
                    "raw": {
                        "max": raw_max, "count_above_threshold": count,
                        "share_above_threshold": share,
                        "argmax_index": (1, 1, 1), "argmax_physical": (5.0, 10.0, 1.3),
                        "value_at_argmax": raw_max,
                        "quantiles": {"q50": 1.0, "q90": 2.0, "q95": 3.0, "q99": 4.0},
                        "offending_states": [
                            {"b_index": o[0], "a_index": o[1], "z_index": o[2],
                             "b": 5.0, "a": 10.0, "z": 1.3, "rate": float(o[3])}
                            for o in offending
                        ],
                    },
                    "requested": {
                        "max": req_max, "count_above_threshold": count,
                        "share_above_threshold": share,
                        "argmax_index": (1, 1, 1), "argmax_physical": (5.0, 10.0, 1.3),
                        "value_at_argmax": req_max,
                        "quantiles": {"q50": 1.0, "q90": 2.0, "q95": 3.0, "q99": 4.0},
                        "offending_states": [
                            {"b_index": o[0], "a_index": o[1], "z_index": o[2],
                             "b": 5.0, "a": 10.0, "z": 1.3, "rate": float(o[3])}
                            for o in offending
                        ],
                    },
                },
                {
                    "boundary": "lower_b",
                    "direction": "b_backward",
                    "raw": {"max": 0.0, "count_above_threshold": 0, "share_above_threshold": 0.0,
                            "argmax_index": (0, 0, 0), "argmax_physical": (-2.0, 0.0, 0.8),
                            "value_at_argmax": 0.0, "quantiles": "NOT_APPLICABLE",
                            "offending_states": []},
                    "requested": {"max": 0.0, "count_above_threshold": 0, "share_above_threshold": 0.0,
                                  "argmax_index": (0, 0, 0), "argmax_physical": (-2.0, 0.0, 0.8),
                                  "value_at_argmax": 0.0, "quantiles": "NOT_APPLICABLE",
                                  "offending_states": []},
                },
            ],
        },
        "illiquid": {"boundaries": []},
        "variant_terminal": "HJB_CONVERGED",
    }


# ---------------------------------------------------------------------------
# 1. Exact six-variant plan identity
# ---------------------------------------------------------------------------


def test_exact_six_variant_plan_identity():
    cfg = _cfg()
    plan = mod.grid_plan_identity(cfg)
    ids = list(plan["variants"].keys())
    assert ids == ["G0_BASE", "G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3",
                   "G4_BASE_B_FINE", "G5_WIDE1_B_FINE"]
    for vid in ("G0_BASE", "G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3"):
        assert abs(plan["variants"][vid]["db"] - mod.DB0) <= 1e-12
        assert abs(plan["variants"][vid]["b_lo"] + 2.0) <= 1e-12
    assert abs(plan["variants"]["G4_BASE_B_FINE"]["db"] - mod.DB0 / 2) <= 1e-12
    assert abs(plan["variants"]["G5_WIDE1_B_FINE"]["db"] - mod.DB0 / 2) <= 1e-12
    assert plan["variants"]["G4_BASE_B_FINE"]["b_pts"] == 2 * 20 - 1
    assert plan["variants"]["G5_WIDE1_B_FINE"]["b_pts"] == 2 * 40 - 1


# ---------------------------------------------------------------------------
# 2. Frozen illiquid identity
# ---------------------------------------------------------------------------


def test_frozen_illiquid_identity():
    cfg = _cfg()
    ill = mod.grid_plan_identity(cfg)["illiquid"]
    assert ill["a_pts"] == 20
    assert ill["a_lo"] == 0.0
    assert ill["a_hi"] == 10.0
    assert ill["a_max"] == 10.0
    assert abs(ill["da"] - mod.DA0) <= 1e-12
    assert ill["taper_identity"] == "r_a*(1-0.1*(a/a_max)^9)_MATLAB_FAITHFUL_UNCHANGED"


def test_all_variants_share_identical_illiquid_grid():
    cfg = _cfg()
    dlh5b, _params, _numerics = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    a0 = grids["G0_BASE"].a
    for g in grids.values():
        assert np.allclose(g.a, a0, atol=1e-12)
        assert g.a.size == 20
        assert abs(g.a[-1] - 10.0) <= 1e-12


# ---------------------------------------------------------------------------
# 3/4/5. Nesting and alignment
# ---------------------------------------------------------------------------


def test_g0_g3_same_spacing_nesting():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    g0 = grids["G0_BASE"]
    for vid in ("G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3"):
        gw = grids[vid]
        assert gw.b[0] == g0.b[0] == -2.0
        assert np.allclose(gw.b[: g0.b.size], g0.b, atol=1e-12)


def test_g4_every_second_alignment_g0():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    assert np.allclose(grids["G4_BASE_B_FINE"].b[::2], grids["G0_BASE"].b, atol=1e-12)


def test_g5_every_second_alignment_g1():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    assert np.allclose(grids["G5_WIDE1_B_FINE"].b[::2], grids["G1_B_WIDE_1"].b, atol=1e-12)


# ---------------------------------------------------------------------------
# 6. Fresh initialization / no warm-start
# ---------------------------------------------------------------------------


def test_fresh_initialization_per_variant(monkeypatch):
    cfg = _cfg()
    dlh5b, params, numerics = mod.build_fixture(cfg)
    calls = []
    orig = mod.household_initial_condition

    def fake_initial_condition(grid, *a, **k):
        calls.append(grid.b.size)
        return orig(grid, *a, **k)

    monkeypatch.setattr(mod, "household_initial_condition", fake_initial_condition)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    assert calls == [20, 40, 60, 80, 39, 79]
    assert all(v["hjb_converged"] for v in runs["variants"])


# ---------------------------------------------------------------------------
# 7/8/9. Boundary diagnostics (raw + requested, coordinates, offending)
# ---------------------------------------------------------------------------


def _boundary_fixture():
    grid = _tiny_grid(nb=5, na=6)
    db = float(grid.b[1] - grid.b[0])
    # upper-b slice shape (a=6, z=2). Raw values chosen as fractions of db.
    ub = np.zeros((6, 2))
    ub[1, 0] = 0.1 * db
    ub[3, 1] = 0.2 * db
    ub[4, 1] = 0.6 * db
    mu_b = np.zeros((5, 6, 2))
    mu_b[4, :, :] = ub
    return grid, db, mu_b


def test_raw_boundary_reconstruction_index_physical():
    grid, db, mu_b = _boundary_fixture()
    hjb = _fake_hjb((5, 6, 2), mu_b=mu_b)
    liq = mod.liquid_boundary_diagnostics(hjb, grid, db, 1e-10)
    ub = next(b for b in liq["boundaries"] if b["boundary"] == "upper_b")
    raw = ub["raw"]
    # argmax at (b=4, a=4, z=1): physical (5.0, grid.a[4], 1.3)
    assert raw["argmax_index"] == (4, 4, 1)
    assert raw["argmax_physical"] == (5.0, float(grid.a[4]), 1.3)
    assert abs(raw["value_at_argmax"] - 0.6 * db) <= 1e-12
    # raw threshold = 1e-10*db
    assert abs(raw["max"] - 0.6 * db) <= 1e-12
    lb = next(b for b in liq["boundaries"] if b["boundary"] == "lower_b")
    assert lb["raw"]["max"] == 0.0
    assert lb["raw"]["argmax_physical"] == (-2.0, 0.0, 0.8)


def test_requested_rate_and_raw_threshold():
    grid, db, mu_b = _boundary_fixture()
    hjb = _fake_hjb((5, 6, 2), mu_b=mu_b)
    liq = mod.liquid_boundary_diagnostics(hjb, grid, db, 1e-10)
    ub = next(b for b in liq["boundaries"] if b["boundary"] == "upper_b")
    raw, req = ub["raw"], ub["requested"]
    # requested = raw/db; values 0.1, 0.2, 0.6 all > 1e-10
    assert abs(req["max"] - 0.6) <= 1e-12
    assert req["count_above_threshold"] == 3
    assert abs(req["share_above_threshold"] - 3.0 / 12.0) <= 1e-12
    assert abs(raw["max"] - req["max"] * db) <= 1e-12
    q = req["quantiles"]
    assert q["q50"] == 0.2
    # np.quantile linear interpolation over the three positive values
    expected = np.quantile([0.1, 0.2, 0.6], [0.9, 0.95, 0.99])
    assert q["q90"] == pytest.approx(expected[0], abs=1e-12)
    assert q["q95"] == pytest.approx(expected[1], abs=1e-12)
    assert q["q99"] == pytest.approx(expected[2], abs=1e-12)
    # raw threshold counts the same states at 1e-10*db
    assert raw["count_above_threshold"] == 3


def test_complete_offending_states():
    grid, db, mu_b = _boundary_fixture()
    hjb = _fake_hjb((5, 6, 2), mu_b=mu_b)
    liq = mod.liquid_boundary_diagnostics(hjb, grid, db, 1e-10)
    ub = next(b for b in liq["boundaries"] if b["boundary"] == "upper_b")
    req = ub["requested"]
    states = {(o["b_index"], o["a_index"], o["z_index"]) for o in req["offending_states"]}
    assert states == {(4, 1, 0), (4, 3, 1), (4, 4, 1)}
    rates = {o["rate"] for o in req["offending_states"]}
    assert rates == {0.1, 0.2, 0.6}
    # sorted by (b, a, z)
    idxs = [(o["b_index"], o["a_index"], o["z_index"]) for o in req["offending_states"]]
    assert idxs == sorted(idxs)
    # illiquid regression diagnostics never trigger on zero mu_a
    ill = mod.illiquid_regression_diagnostics(hjb, grid, db, 0.5263157894736842, 1e-10)
    assert all(b["requested"]["max"] == 0.0 for b in ill["boundaries"])


# ---------------------------------------------------------------------------
# 10. Extent attenuation ratios
# ---------------------------------------------------------------------------


def test_extent_attenuation_ratios():
    cfg = _cfg()
    # raw maxima strictly decreasing: 1.0, 0.5, 0.25, 0.125
    recs = []
    raw = [1.0, 0.5, 0.25, 0.125]
    req = [0.6, 0.4, 0.2, 0.1]
    for i, vid in enumerate(("G0_BASE", "G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3")):
        rec = _fake_variant_record(vid, raw_max=raw[i], req_max=req[i],
                                   count=1, share=0.01, offending=((1, 1, 1, 0.1),))
        recs.append(rec)
    runs = {"variants": recs}
    trend = mod.extent_trend(cfg, runs)
    seq = [s for s in trend["sequence"] if s.get("reached")]
    assert [s["raw_max"] for s in seq] == [1.0, 0.5, 0.25, 0.125]
    assert trend["ratios"]["adjacent_raw"] == [2.0, 2.0, 2.0]
    assert trend["ratios"]["vs_G0_raw"] == [0.5, 0.25, 0.125]
    assert trend["ratios"]["adjacent_requested"] == [1.5, 2.0, 2.0]
    assert trend["ratios"]["vs_G0_requested"] == [
        pytest.approx(0.4 / 0.6, abs=1e-6), pytest.approx(0.2 / 0.6, abs=1e-6),
        pytest.approx(0.1 / 0.6, abs=1e-6),
    ]
    assert trend["strictly_decreasing_raw"] is True
    assert trend["strictly_decreasing_requested"] is True


# ---------------------------------------------------------------------------
# 11. Aligned b-resolution comparison (both pairs)
# ---------------------------------------------------------------------------


def test_aligned_resolution_comparison_both_pairs():
    cfg = _cfg()
    dlh5b, _p, _n = mod.build_fixture(cfg)
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, _plan = mod.build_all_grids(cfg, z, switch)
    g0, g1 = grids["G0_BASE"], grids["G1_B_WIDE_1"]
    g4, g5 = grids["G4_BASE_B_FINE"], grids["G5_WIDE1_B_FINE"]

    # value = 0.5 on coarse grids, 0.0 on fine grids -> max_abs_diff 0.5 on every pair
    hc0 = _fake_hjb((20, 20, 2), value=np.full((20, 20, 2), 0.5))
    hf4 = _fake_hjb((39, 20, 2), value=np.zeros((39, 20, 2)))
    hc1 = _fake_hjb((40, 20, 2), value=np.full((40, 20, 2), 0.5))
    hf5 = _fake_hjb((79, 20, 2), value=np.zeros((79, 20, 2)))
    runs = {
        "hjb_results": {"G0_BASE": hc0, "G4_BASE_B_FINE": hf4,
                        "G1_B_WIDE_1": hc1, "G5_WIDE1_B_FINE": hf5},
        "variants": [
            _fake_variant_record("G0_BASE", raw_max=0.1, req_max=0.1),
            _fake_variant_record("G1_B_WIDE_1", raw_max=0.05, req_max=0.05),
            _fake_variant_record("G4_BASE_B_FINE", raw_max=0.05, req_max=0.05),
            _fake_variant_record("G5_WIDE1_B_FINE", raw_max=0.02, req_max=0.02),
        ],
    }
    res = mod.resolution_stability(cfg, runs)
    assert [c["comparison"] for c in res] == ["G0_vs_G4", "G1_vs_G5"]
    for c in res:
        assert c["reached"] is True
        assert c["fields"]["value"]["max_abs_diff"] == pytest.approx(0.5, abs=1e-12)
        assert c["fields"]["value"]["rel_diff"] == pytest.approx(0.5 / 1.0, abs=1e-12)
        assert "raw_mu_b_upper_shared_nodes" in c["fields"]


# ---------------------------------------------------------------------------
# 12. No stationary / KFE / aggregate path
# ---------------------------------------------------------------------------


def test_no_stationary_execution_path():
    src = pathlib.Path(mod.__file__).read_text(encoding="utf-8")
    # policy-only marker is the ONLY stationary reference permitted
    for forbidden in (
        "solve_matlab_faithful_stationary_kfe",
        "assemble_conservative_operator",
        "conservative_stationary_kfe",
        "nullspace_dimension",
        "pin_validation",
        "tail_diagnostics",
        "aggregate_stationary_household",
    ):
        assert forbidden not in src, f"forbidden stationary symbol present: {forbidden}"
    assert mod.NOT_AUTHORIZED_MARKER == "NOT_AUTHORIZED__DLH_5G_POLICY_ONLY_LIQUID_DOMAIN_DIAGNOSTIC"


# ---------------------------------------------------------------------------
# 13. Deterministic repeat (structural + numeric + non-finite-aware)
# ---------------------------------------------------------------------------


def test_deterministic_nonfinite_aware_repeat_comparison():
    cfg = _cfg()
    r1 = _fake_variant_record("G0_BASE", hjb_statistic=1.5e-8, raw_max=0.3, req_max=0.3,
                              count=2, share=0.05, offending=((1, 1, 1, 0.3), (2, 2, 1, 0.2)))
    r2 = _fake_variant_record("G0_BASE", hjb_statistic=1.5e-8, raw_max=0.3, req_max=0.3,
                              count=2, share=0.05, offending=((1, 1, 1, 0.3), (2, 2, 1, 0.2)))
    cmp = mod.compare_variant_records(r1, r2, cfg)
    assert cmp["identical_structural_signature"] is True
    assert cmp["max_numeric_diff"] == 0.0
    assert cmp["mismatched_fields"] == 0
    assert cmp["pass_bool"] is True

    # identical structure, only the convergence statistic differs -> numeric diff
    r3 = _fake_variant_record("G0_BASE", hjb_statistic=2.5e-8, raw_max=0.3, req_max=0.3,
                              count=2, share=0.05, offending=((1, 1, 1, 0.3), (2, 2, 1, 0.2)))
    cmp3 = mod.compare_variant_records(r1, r3, cfg)
    assert cmp3["identical_structural_signature"] is True
    assert cmp3["max_numeric_diff"] == pytest.approx(1.0e-8, abs=1e-12)
    assert cmp3["mismatched_fields"] == 0
    assert cmp3["pass_bool"] is False

    # aligned non-finite handling: identical NaN quantile-free records pass
    r4 = _fake_variant_record("G0_BASE")
    r4["liquid"]["boundaries"][0]["raw"]["quantiles"] = "NOT_APPLICABLE"
    r5 = _fake_variant_record("G0_BASE")
    r5["liquid"]["boundaries"][0]["raw"]["quantiles"] = "NOT_APPLICABLE"
    cmp5 = mod.compare_variant_records(r4, r5, cfg)
    assert cmp5["pass_bool"] is True
    assert cmp5["aligned_nonfinite_fields"] == 0  # string fields are structural

    # true NaN-vs-finite mismatch must be flagged
    r6 = _fake_variant_record("G0_BASE")
    r6["liquid"]["boundaries"][0]["raw"]["max"] = float("nan")
    r7 = _fake_variant_record("G0_BASE")
    cmp6 = mod.compare_variant_records(r6, r7, cfg)
    assert cmp6["mismatched_fields"] >= 1
    assert cmp6["pass_bool"] is False


def test_randomness_not_applicable_and_repro_structure(monkeypatch):
    cfg = _cfg()
    dlh5b, params, numerics = mod.build_fixture(cfg)
    # Determinism of the reproduce wrapper itself: replace the heavy real solve
    # path with two deterministic stub runs. The real two-pass repeat is produced
    # by evidence generation (DLH_5G_REPRODUCIBILITY.json, run1 vs run2).
    calls = {"n": 0}

    def fake_runs(*a, **k):
        calls["n"] += 1
        return {"grid_plan": {}, "variants": [], "hjb_results": {}}

    monkeypatch.setattr(mod, "run_all_variants", fake_runs)
    monkeypatch.setattr(mod, "resolution_stability", lambda cfg, runs: [])
    repro = mod.reproduce(cfg, dlh5b, params, numerics)
    assert calls["n"] == 2
    assert repro["randomness"] == "NOT_APPLICABLE"
    assert repro["pass_bool"] is True
    assert repro["terminal_run1"] == repro["terminal_run2"]


# ---------------------------------------------------------------------------
# 14. Accepted source identity
# ---------------------------------------------------------------------------


def test_accepted_source_identity_unchanged():
    data = ORACLE_PATH.read_bytes()
    assert mod.ACCEPTED_SHA256 == hashlib.sha256(data).hexdigest().upper()
    assert mod.ACCEPTED_BLOB == "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"


# ---------------------------------------------------------------------------
# 15. Canonical six-variant execution + accepted DLH-5F reproduction
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def canonical():
    cfg = mod.load_config(CONFIG_PATH)
    dlh5b, params, numerics = mod.build_fixture(cfg)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    trend = mod.extent_trend(cfg, runs)
    res = mod.resolution_stability(cfg, runs)
    return cfg, runs, trend, res


def test_canonical_all_six_converge_and_terminal_class(canonical):
    cfg, runs, trend, _res = canonical
    assert len(runs["variants"]) == 6
    assert all(v["hjb_converged"] for v in runs["variants"])
    repro = {"pass_bool": True}
    term = mod.overall_terminal(cfg, runs, repro, _res)
    assert term["terminal"] in (mod.TERMINAL_OUTCOME_A, mod.TERMINAL_OUTCOME_B, mod.TERMINAL_OUTCOME_C)
    assert term["terminal"] not in (mod.TERMINAL_OUTCOME_D, mod.TERMINAL_OUTCOME_E)
    # extent sequence fully reached
    seq = [s for s in trend["sequence"] if s.get("reached")]
    assert [s["variant"] for s in seq] == ["G0_BASE", "G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3"]


def test_g0_g1_reproduce_accepted_dlh5f_b_facts(canonical):
    _cfg_, runs, _trend, _res = canonical
    by_id = {v["variant"]: v for v in runs["variants"]}

    def ub(v):
        return next(b for b in v["liquid"]["boundaries"] if b["boundary"] == "upper_b")["requested"]

    # G0_BASE == DLH-5F V0_BASE: upper-b requested 3.537477040e-01 @ (19,19,1)
    g0 = ub(by_id["G0_BASE"])
    assert abs(g0["max"] - 3.537477040e-01) <= 2e-9
    assert g0["argmax_index"] == (19, 19, 1)
    assert g0["argmax_physical"] == (5.0, 10.0, 1.3)
    assert g0["count_above_threshold"] == 3

    # G1_B_WIDE_1 == DLH-5F V2_B_WIDE: upper-b requested 1.020335606e-02 @ (39,19,1)
    g1 = ub(by_id["G1_B_WIDE_1"])
    assert abs(g1["max"] - 1.020335606e-02) <= 2e-9
    assert g1["argmax_index"] == (39, 19, 1)
    assert g1["argmax_physical"] == (12.368421052631579, 10.0, 1.3)
    assert g1["count_above_threshold"] == 1
