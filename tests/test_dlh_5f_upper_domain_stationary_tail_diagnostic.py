"""DLH-5F (Issue #29) — focused upper-domain / stationary-tail diagnostic tests.

Covers the 13 minimum required tests from Issue #29 section 15:
1. exact six-variant plan identity;
2. exact baseline spacing preservation for V1-V4;
3. exact V0 nesting in same-spacing wider variants;
4. exact every-second V0 alignment inside V5_BASE_FINE;
5. fresh initialization per variant / no warm-start plumbing;
6. boundary physical-coordinate and index-coordinate reconstruction on
   nontrivial synthetic shapes;
7. positive outward quantiles / counts / shares;
8. shared-interior extraction for same-spacing and half-spacing nested grids;
9. Phase E fail-closed: no stationary density/tail/aggregates when boundary
   policy exceeds 1e-10;
10. synthetic valid conservative generator where stationary/tail metrics are
    reached and computed correctly;
11. probability-weighted flux includes cell_weight exactly once;
12. deterministic non-finite-aware repeat comparison;
13. accepted MATLAB-faithful source identity remains unchanged.

Plus a module-scope canonical run verifying all six frozen variants converge and
none reaches the same-process stationary gate (the expected evidence-driven
outcome of the pre-frozen upper-domain experiment).
"""

from __future__ import annotations

import hashlib
import pathlib
import types

import numpy as np
import pytest

from deep_learning_hank.two_asset import MatlabFaithfulHJBGrid
from deep_learning_hank.two_asset.conservative_stationary_kfe import (
    assemble_conservative_operator,
    requested_rates,
)
from deep_learning_hank.two_asset.upper_domain_stationary_tail_diagnostic import (
    ACCEPTED_SHA256,
    DB0,
    DA0,
    DLH5FConfig,
    NOT_REACHED_MARKER,
    TERMINAL_OUTCOME_B,
    TERMINAL_REPRODUCIBILITY,
    boundary_diagnostics_full,
    build_fixture,
    build_variant_grid,
    compare_variant_records,
    grid_plan_identity,
    load_config,
    overall_terminal,
    run_all_variants,
    shared_interior_pair,
    tail_diagnostics,
    _finalize_variant_record,
)

CONFIG_PATH = "configs/dlh_5f_upper_domain_stationary_tail_diagnostic.toml"


def _cfg(tmp_path) -> DLH5FConfig:
    return DLH5FConfig(
        dlh5b_config_path="configs/dlh_5b_two_region_symmetric_anchor.toml",
        region_index=0,
        wbar=1.0,
        r_a=0.03,
        variants=load_config(CONFIG_PATH).variants,
        b_index_max=17,
        a_index_max=17,
        boundary_threshold=1e-10,
        generator_row_sum_tol=1e-12,
        generator_neg_offdiag_tol=1e-12,
        original_residual_tol=1e-10,
        mass_tol=1e-12,
        min_density_tol=-1e-12,
        multi_pin_diff_tol=1e-10,
        reproducibility_tol=1e-12,
        numeric_compare_tol=1e-12,
        nullspace_tol=1e-8,
        zero_support_rel_tol=1e-6,
        svd_maxiter=5000,
        pin_rhs=0.007,
        pin_spec=("first", "quarter", "accepted", "half", "three_quarter", "last"),
        output_root=str(tmp_path / "dlh_5f_out"),
    )


def _tiny_grid() -> MatlabFaithfulHJBGrid:
    return MatlabFaithfulHJBGrid(
        np.linspace(-2.0, 5.0, 3),
        np.linspace(0.0, 10.0, 3),
        np.asarray([0.8, 1.3]),
        np.asarray([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]]),
    )


def _synthetic_irreducible_requested(shape):
    """Requested rates forming an irreducible birth-death chain in each asset
    dimension plus the accepted z-switch, with ZERO outward boundary rates."""
    i_count, j_count, nz = shape
    bb = np.ones(shape)
    bb[0, :, :] = 0.0
    bf = np.ones(shape)
    bf[-1, :, :] = 0.0
    ab = np.ones(shape)
    ab[:, 0, :] = 0.0
    af = np.ones(shape)
    af[:, -1, :] = 0.0
    return {"b_backward_requested": bb, "b_forward_requested": bf,
            "a_backward_requested": ab, "a_forward_requested": af}


# ---------------------------------------------------------------------------
# 1-4. Grid plan identity / spacing / nesting / half-spacing alignment
# ---------------------------------------------------------------------------


def test_exact_six_variant_plan_identity(tmp_path):
    cfg = _cfg(tmp_path)
    plan = grid_plan_identity(cfg)
    ids = list(plan.keys())
    assert ids == ["V0_BASE", "V1_A_WIDE", "V2_B_WIDE", "V3_AB_MID", "V4_AB_WIDE", "V5_BASE_FINE"]
    v0 = plan["V0_BASE"]
    assert v0["b_pts"] == 20 and v0["a_pts"] == 20
    assert v0["b_lo"] == pytest.approx(-2.0) and v0["b_hi"] == pytest.approx(5.0)
    assert v0["a_lo"] == pytest.approx(0.0) and v0["a_hi"] == pytest.approx(10.0)
    v1 = plan["V1_A_WIDE"]
    assert v1["b_pts"] == 20 and v1["a_pts"] == 40
    assert v1["a_hi"] == pytest.approx(390 / 19)
    v2 = plan["V2_B_WIDE"]
    assert v2["b_pts"] == 40 and v2["a_pts"] == 20
    assert v2["b_hi"] == pytest.approx(235 / 19)
    v3 = plan["V3_AB_MID"]
    assert v3["b_pts"] == 30 and v3["a_pts"] == 30
    assert v3["b_hi"] == pytest.approx(165 / 19) and v3["a_hi"] == pytest.approx(290 / 19)
    v4 = plan["V4_AB_WIDE"]
    assert v4["b_pts"] == 40 and v4["a_pts"] == 40
    assert v4["b_hi"] == pytest.approx(235 / 19) and v4["a_hi"] == pytest.approx(390 / 19)
    v5 = plan["V5_BASE_FINE"]
    assert v5["b_pts"] == 39 and v5["a_pts"] == 39
    assert v5["b_hi"] == pytest.approx(5.0) and v5["a_hi"] == pytest.approx(10.0)


def test_baseline_spacing_preservation_v1_v4(tmp_path):
    cfg = _cfg(tmp_path)
    plan = grid_plan_identity(cfg)
    for vid in ("V0_BASE", "V1_A_WIDE", "V2_B_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        assert plan[vid]["db"] == pytest.approx(DB0, abs=1e-12)
        assert plan[vid]["da"] == pytest.approx(DA0, abs=1e-12)
    assert plan["V5_BASE_FINE"]["db"] == pytest.approx(DB0 / 2, abs=1e-12)
    assert plan["V5_BASE_FINE"]["da"] == pytest.approx(DA0 / 2, abs=1e-12)


def test_v0_nesting_in_same_spacing_wider(tmp_path):
    cfg = _cfg(tmp_path)
    z = np.asarray([0.8, 1.3])
    switch = np.asarray([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    g0 = build_variant_grid(cfg.variants[0], z, switch)
    for vid in ("V2_B_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        spec = next(v for v in cfg.variants if v.id == vid)
        gw = build_variant_grid(spec, z, switch)
        assert np.allclose(gw.b[: g0.b.size], g0.b, atol=1e-12)
    for vid in ("V1_A_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        spec = next(v for v in cfg.variants if v.id == vid)
        gw = build_variant_grid(spec, z, switch)
        assert np.allclose(gw.a[: g0.a.size], g0.a, atol=1e-12)


def test_v5_every_second_v0_alignment(tmp_path):
    cfg = _cfg(tmp_path)
    z = np.asarray([0.8, 1.3])
    switch = np.asarray([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]])
    g0 = build_variant_grid(cfg.variants[0], z, switch)
    g5 = build_variant_grid(cfg.variants[5], z, switch)
    assert np.allclose(g5.b[::2], g0.b, atol=1e-12)
    assert np.allclose(g5.a[::2], g0.a, atol=1e-12)


# ---------------------------------------------------------------------------
# 5. Fresh initialization per variant / no warm-start plumbing
# ---------------------------------------------------------------------------


def test_fresh_initialization_per_variant(tmp_path, monkeypatch):
    from deep_learning_hank.two_asset import upper_domain_stationary_tail_diagnostic as mod

    cfg = _cfg(tmp_path)
    dlh5b, params, numerics = build_fixture(cfg)
    calls: list[tuple[int, int]] = []
    real_init = mod.household_initial_condition

    def _wrapped(grid, params_, inputs_, rb_gap):
        calls.append((int(grid.b.size), int(grid.a.size)))
        return real_init(grid, params_, inputs_, rb_gap)

    monkeypatch.setattr(mod, "household_initial_condition", _wrapped)
    runs = mod.run_all_variants(cfg, dlh5b, params, numerics)
    assert len(calls) == 6
    expected = [(20, 20), (20, 40), (40, 20), (30, 30), (40, 40), (39, 39)]
    assert calls == expected  # each variant initialized fresh on its own grid


# ---------------------------------------------------------------------------
# 6-7. Boundary coordinate reconstruction + quantiles/counts/shares
# ---------------------------------------------------------------------------


def test_boundary_physical_and_index_coordinates_nontrivial(tmp_path):
    cfg = _cfg(tmp_path)
    grid = MatlabFaithfulHJBGrid(
        np.linspace(-1.0, 3.0, 4),
        np.linspace(0.0, 8.0, 5),
        np.asarray([0.8, 1.3]),
        np.asarray([[-1.0 / 3.0, 1.0 / 3.0], [1.0 / 3.0, -1.0 / 3.0]]),
    )
    shape = (4, 5, 2)
    db = grid.b[1] - grid.b[0]
    da = grid.a[1] - grid.a[0]
    mu_b = np.zeros(shape)
    mu_a = np.zeros(shape)
    # peaks deliberately NOT at the last slice element
    mu_b[0, 2, 1] = -2.0 * db          # lower-b peak at (a=2,z=1)
    mu_b[-1, 1, 0] = 1.0 * db          # upper-b peak at (a=1,z=0)
    mu_a[3, 0, 1] = -0.5 * da          # lower-a peak at (b=3,z=1)
    mu_a[2, -1, 0] = 2.0 * da          # upper-a peak at (b=2,z=0)
    requested = requested_rates(mu_b, mu_a, db, da)
    bd = boundary_diagnostics_full(requested, grid, cfg.boundary_threshold)
    by = {b["boundary"]: b for b in bd["boundaries"]}
    assert by["lower_b"]["argmax_index"] == (0, 2, 1)
    assert by["lower_b"]["argmax_physical"] == (float(grid.b[0]), float(grid.a[2]), float(grid.z[1]))
    assert by["upper_b"]["argmax_index"] == (3, 1, 0)
    assert by["upper_b"]["argmax_physical"] == (float(grid.b[3]), float(grid.a[1]), float(grid.z[0]))
    assert by["lower_a"]["argmax_index"] == (3, 0, 1)
    assert by["upper_a"]["argmax_index"] == (2, 4, 0)
    assert by["upper_a"]["argmax_physical"] == (float(grid.b[2]), float(grid.a[4]), float(grid.z[0]))
    for bname, count in (("lower_b", 1), ("upper_b", 1), ("lower_a", 1), ("upper_a", 1)):
        assert by[bname]["count_above_threshold"] == count
        assert len(by[bname]["offending_states"]) == count
    # complete offending sets carry index AND physical coordinates
    o = by["upper_a"]["offending_states"][0]
    assert (o["b_index"], o["a_index"], o["z_index"]) == (2, 4, 0)
    assert o["b"] == pytest.approx(float(grid.b[2])) and o["a"] == pytest.approx(float(grid.a[4]))


def test_positive_outward_quantiles_counts_shares(tmp_path):
    cfg = _cfg(tmp_path)
    grid = _tiny_grid()
    shape = (3, 3, 2)
    db = grid.b[1] - grid.b[0]
    da = grid.a[1] - grid.a[0]
    mu_b = np.zeros(shape)
    mu_a = np.zeros(shape)
    # three distinct positive outward rates on upper-b (a,z) slice
    mu_b[-1, 0, 0] = 0.1 * db
    mu_b[-1, 1, 0] = 0.2 * db
    mu_b[-1, 2, 1] = 0.6 * db
    requested = requested_rates(mu_b, mu_a, db, da)
    bd = boundary_diagnostics_full(requested, grid, cfg.boundary_threshold)
    ub = next(b for b in bd["boundaries"] if b["boundary"] == "upper_b")
    assert ub["count_above_threshold"] == 3
    assert ub["share_above_threshold"] == pytest.approx(3 / 6)  # (a x z) = 6 states
    pos = np.array([0.1, 0.2, 0.6])
    q = ub["quantiles"]
    assert q["q50"] == pytest.approx(float(np.quantile(pos, 0.5)))
    assert q["q90"] == pytest.approx(float(np.quantile(pos, 0.9)))
    assert q["q95"] == pytest.approx(float(np.quantile(pos, 0.95)))
    assert q["q99"] == pytest.approx(float(np.quantile(pos, 0.99)))
    la = next(b for b in bd["boundaries"] if b["boundary"] == "lower_a")
    assert la["quantiles"] == "NOT_APPLICABLE"  # no positive outward rate
    assert la["count_above_threshold"] == 0
    assert la["share_above_threshold"] == 0.0


# ---------------------------------------------------------------------------
# 8. Shared-interior extraction (same-spacing and half-spacing)
# ---------------------------------------------------------------------------


def _fake_hjb(shape, db=None, da=None, value_offset=0.0):
    value = np.full(shape, value_offset, dtype=float)
    return types.SimpleNamespace(
        value=value,
        consumption=np.ones(shape),
        labor=np.ones(shape),
        transfer=np.zeros(shape),
        mu_a=np.zeros(shape),
        mu_b=np.zeros(shape),
        liquid_label=np.full(shape, "0", dtype="U1"),
        transfer_label=np.full(shape, "0", dtype="U1"),
        iterations=1,
        converged=True,
        convergence_statistic=0.0,
    )


def test_shared_interior_extraction_same_and_half_spacing(tmp_path):
    cfg = _cfg(tmp_path)
    # same-spacing wider grid: V0(20x20x2) vs V1(20x40x2); aligned window 18x18
    r0 = _fake_hjb((20, 20, 2))
    r1 = _fake_hjb((20, 40, 2), value_offset=0.5)
    c_same = shared_interior_pair(r0, r1, "test_same", 18, 18, half_spacing=False)
    assert c_same["fields"]["value"]["max_abs_diff"] == pytest.approx(0.5, abs=1e-12)
    assert c_same["fields"]["value"]["strict_interior_max_abs_diff"] == pytest.approx(0.5, abs=1e-12)
    assert c_same["fields"]["liquid_label"]["mismatch_count"] == 0
    assert c_same["fields"]["value"]["max_abs_diff"] > 0.0
    # half-spacing: V5(39x39x2); V0 index i matches V5 index 2i
    r0h = _fake_hjb((20, 20, 2))
    r5 = _fake_hjb((39, 39, 2), value_offset=0.25)
    c_half = shared_interior_pair(r0h, r5, "test_half", 18, 18, half_spacing=True)
    assert c_half["half_spacing"] is True
    assert c_half["fields"]["value"]["max_abs_diff"] == pytest.approx(0.25, abs=1e-12)
    assert c_half["fields"]["value"]["strict_interior_max_abs_diff"] == pytest.approx(0.25, abs=1e-12)
    # extraction windows hold 18x18x2 for both r0 and r1; consumption identical
    assert c_same["fields"]["consumption"]["max_abs_diff"] == 0.0
    assert c_half["fields"]["consumption"]["max_abs_diff"] == 0.0


# ---------------------------------------------------------------------------
# 9. Phase E fail-closed when boundary policy exceeds threshold
# ---------------------------------------------------------------------------


def test_phase_e_fail_closed_on_boundary_violation(tmp_path):
    cfg = _cfg(tmp_path)
    grid = _tiny_grid()
    shape = (3, 3, 2)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    n = int(np.prod(shape))
    mu_b = np.zeros(shape)
    mu_a = np.zeros(shape)
    mu_b[-1, :, :] = 1.0  # material outward requested drift at upper-b
    hjb = _fake_hjb(shape, db, da)
    hjb.mu_b = mu_b
    hjb.mu_a = mu_a
    rec = {"variant": "SYN", "grid": {}, "hjb_converged": True,
           "hjb_iterations": 1, "hjb_statistic": 0.0}
    rec = _finalize_variant_record(cfg, rec, hjb, grid, db, da, n)
    assert rec["boundary_policy_gate"] == "VIOLATION"
    assert rec["phase_e_reached"] is False
    assert rec["stationary"] is None
    assert rec["tail"] == NOT_REACHED_MARKER
    assert rec["aggregates"] == NOT_REACHED_MARKER


# ---------------------------------------------------------------------------
# 10. Synthetic valid conservative generator reaches stationary/tail/aggregates
# ---------------------------------------------------------------------------


def test_synthetic_valid_generator_reaches_stationary_tail_aggregates(tmp_path):
    cfg = _cfg(tmp_path)
    grid = _tiny_grid()
    shape = (3, 3, 2)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    n = int(np.prod(shape))
    requested = _synthetic_irreducible_requested(shape)
    # boundary gate must pass: all boundary outward slices are zero
    bd = boundary_diagnostics_full(requested, grid, cfg.boundary_threshold)
    assert bd["max_requested_outward"] <= cfg.boundary_threshold
    Q_c = assemble_conservative_operator(requested, grid.switch_matrix)
    hjb = _fake_hjb(shape, db, da)
    hjb.mu_a = np.zeros(shape)
    hjb.mu_b = np.zeros(shape)
    rec = {"variant": "SYN_VALID", "grid": {}, "hjb_converged": True,
           "hjb_iterations": 1, "hjb_statistic": 0.0}
    rec = _finalize_variant_record(cfg, rec, hjb, grid, db, da, n, Q_c=Q_c)
    assert rec["boundary_policy_gate"] == "PASS"
    assert rec["phase_e_reached"] is True
    assert rec["stationary"]["gate"] == "PASS"
    assert rec["stationary"]["nullspace_dimension"] == 1
    assert rec["stationary"]["pins"]["valid_pin_count"] >= 2
    assert rec["stationary"]["pins"]["default_pin_class"] == "PIN_VALID_STATIONARY_NORMALIZATION"
    tail = rec["tail"]
    assert isinstance(tail, dict)
    agg = rec["aggregates"]
    assert isinstance(agg, dict)
    # irreducible symmetric chain -> uniform stationary: density = 1/(N*weight)
    # expected aggregates and tail masses (exact closed forms)
    assert agg["C"] == pytest.approx(1.0, abs=1e-9)
    assert agg["L"] == pytest.approx(1.05, abs=1e-9)  # mean(z)
    assert agg["A"] == pytest.approx(5.0, abs=1e-9)   # mean(a)
    assert agg["B"] == pytest.approx(1.5, abs=1e-9)   # mean(b)
    assert tail["mass_a_max"] == pytest.approx(6 / 18, abs=1e-9)
    assert tail["mass_b_max"] == pytest.approx(6 / 18, abs=1e-9)
    assert tail["phi_a_upper_flux"] == pytest.approx(0.0, abs=1e-12)
    assert tail["phi_b_upper_flux"] == pytest.approx(0.0, abs=1e-12)


# ---------------------------------------------------------------------------
# 11. Probability-weighted flux includes cell_weight exactly once
# ---------------------------------------------------------------------------


def test_probability_weighted_flux_cell_weight_once(tmp_path):
    cfg = _cfg(tmp_path)
    grid = _tiny_grid()
    shape = (3, 3, 2)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    weight = db * da
    density = np.ones(shape)  # deliberately NON-normalized to expose weight misuse
    mu_a = np.zeros(shape)
    mu_b = np.zeros(shape)
    mu_a[:, -1, :] = 2.0   # positive upper-a drift
    mu_b[-1, :, :] = 3.0   # positive upper-b drift
    hjb = _fake_hjb(shape, db, da)
    hjb.mu_a = mu_a
    hjb.mu_b = mu_b
    tail = tail_diagnostics(cfg, grid, hjb, density)
    # Phi = sum over boundary states of g*max(mu,0)*weight  (weight applied ONCE)
    upper_a_states = grid.b.size * grid.z.size
    upper_b_states = grid.a.size * grid.z.size
    assert tail["phi_a_upper_flux"] == pytest.approx(upper_a_states * 2.0 * weight, rel=1e-12)
    assert tail["phi_b_upper_flux"] == pytest.approx(upper_b_states * 3.0 * weight, rel=1e-12)
    # cell_weight reported exactly db*da
    assert tail["cell_weight"] == pytest.approx(weight)


# ---------------------------------------------------------------------------
# 12. Deterministic non-finite-aware repeat comparison
# ---------------------------------------------------------------------------


def _boundary_violation_record(variant="V0_BASE"):
    return {
        "variant": variant,
        "grid": {"b_pts": 20, "a_pts": 20, "db": DB0, "da": DA0},
        "hjb_converged": True,
        "hjb_iterations": 11,
        "hjb_statistic": 1.0e-8,
        "boundary_policy_gate": "VIOLATION",
        "phase_e_reached": False,
        "boundary": {
            "max_requested_outward": 0.35,
            "boundaries": [
                {"boundary": "upper_b", "direction": "b_forward",
                 "requested_outward_max": 0.35, "count_above_threshold": 1,
                 "share_above_threshold": 1.0 / 40.0, "argmax_index": (19, 19, 1),
                 "argmax_physical": (5.0, 10.0, 1.3), "requested_at_max": 0.35,
                 "quantiles": "NOT_APPLICABLE",
                 "offending_states": [{"boundary": "upper_b", "direction": "b_forward",
                                       "b_index": 19, "a_index": 19, "z_index": 1,
                                       "b": 5.0, "a": 10.0, "z": 1.3,
                                       "requested_outward_rate": 0.35}]},
            ],
        },
        "generator": {"row_sum_max_abs": 1e-16, "negative_offdiag_max_mag": 0.0,
                      "row_sum_min": -1e-16, "row_sum_max": 1e-16, "nnz": 40},
        "stationary": None,
        "tail": NOT_REACHED_MARKER,
        "aggregates": NOT_REACHED_MARKER,
    }


def test_deterministic_nonfinite_aware_repeat_comparison(tmp_path):
    cfg = _cfg(tmp_path)
    base = _boundary_violation_record()
    r1 = dict(base)
    r2 = dict(base)
    cmp = compare_variant_records(r1, r2, cfg)
    assert cmp["identical_structural_signature"] is True
    assert cmp["max_numeric_diff"] <= cfg.reproducibility_tol
    assert cmp["pass_bool"] is True
    # rate perturbation above tolerance fails the numeric compare
    r3 = dict(base)
    b3 = dict(base["boundary"])
    b3["max_requested_outward"] = 0.35 + 1e-6
    r3["boundary"] = b3
    cmp_bad = compare_variant_records(r1, r3, cfg)
    assert cmp_bad["pass_bool"] is False
    # aligned non-finite is explicit and allowed
    r4 = dict(base)
    b4 = dict(base["boundary"])
    b4["max_requested_outward"] = float("nan")
    r4["boundary"] = b4
    r5 = dict(r4)
    cmp_nf = compare_variant_records(r4, r5, cfg)
    assert cmp_nf["pass_bool"] is True
    assert cmp_nf["aligned_nonfinite_fields"] >= 1


# ---------------------------------------------------------------------------
# 13. Accepted MATLAB-faithful source identity unchanged
# ---------------------------------------------------------------------------


def test_accepted_source_identity_unchanged():
    path = pathlib.Path("src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py")
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest().upper()
    assert sha == ACCEPTED_SHA256
    assert sha == "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"


# ---------------------------------------------------------------------------
# Module-scope canonical run (all six frozen variants)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def canonical():
    cfg = load_config(CONFIG_PATH)
    dlh5b, params, numerics = build_fixture(cfg)
    runs = run_all_variants(cfg, dlh5b, params, numerics)
    return cfg, runs


def test_all_six_variants_converge_and_none_reaches_phase_e(canonical):
    cfg, runs = canonical
    assert len(runs["variants"]) == 6
    for v in runs["variants"]:
        assert v["hjb_converged"] is True
        assert v["boundary_policy_gate"] == "VIOLATION"
        assert v["phase_e_reached"] is False
        assert v["tail"] == NOT_REACHED_MARKER
        assert v["aggregates"] == NOT_REACHED_MARKER
    # expected overall outcome for the pre-frozen domains
    term = overall_terminal(cfg, runs, {"pass_bool": True})
    assert term["terminal"] == TERMINAL_OUTCOME_B


def test_v0_matches_accepted_dlh5e_d0_boundary_facts(canonical):
    cfg, runs = canonical
    v0 = next(v for v in runs["variants"] if v["variant"] == "V0_BASE")
    b = {bi["boundary"]: bi for bi in v0["boundary"]["boundaries"]}
    assert v0["hjb_iterations"] == 11
    assert b["upper_b"]["requested_outward_max"] == pytest.approx(0.353747704, rel=1e-5)
    assert b["upper_b"]["count_above_threshold"] == 3
    assert b["upper_b"]["argmax_index"] == (19, 19, 1)
    assert b["upper_a"]["count_above_threshold"] == 28
    assert b["upper_a"]["argmax_index"] == (14, 19, 1)
    assert b["lower_b"]["requested_outward_max"] == 0.0
    assert b["lower_a"]["requested_outward_max"] == 0.0


def test_reproducibility_failure_classification(tmp_path):
    cfg = _cfg(tmp_path)
    runs = {"variants": [_boundary_violation_record(), _boundary_violation_record("V1_A_WIDE")]}
    repro_bad = {"pass_bool": False}
    term = overall_terminal(cfg, runs, repro_bad)
    assert term["terminal"] == TERMINAL_REPRODUCIBILITY
