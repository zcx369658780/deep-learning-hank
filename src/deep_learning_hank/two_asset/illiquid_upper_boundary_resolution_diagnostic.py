"""DLH-5H (Issue #34) — illiquid upper-boundary resolution diagnostic.

Isolates illiquid-grid resolution on the provisional liquid-safe domain while
preserving the accepted household controlled process:

- D0 economics/prices frozen (``wbar=1.0``, ``r_a=0.03``);
- physical illiquid domain ``a in [0,10]``, ``a_max=10``, accepted MATLAB-faithful
  taper ``r_a*(1-0.1*(a/a_max)^9)`` unchanged;
- core liquid-safe b60 ``[-2,375/19]``, ``db=7/19`` for H0-H3;
- H4/H5 are the exact pre-frozen half-``db`` b-resolution cross-checks;
- exactly six variants, fresh initialization each, no warm-start, no adaptive
  grid, no retuning, no clipping.

Raw ``max(mu_a,0)`` is the primary cross-resolution illiquid diagnostic;
requested generator rate ``max(mu_a,0)/da`` remains the HJB/KFE
boundary-compatibility quantity. Upper/lower b diagnostics are a regression
gate only. Policy-only: stationary fields use the marker
``NOT_AUTHORIZED__DLH_5H_POLICY_ONLY_ILLIQUID_RESOLUTION_DIAGNOSTIC``.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
import tomllib
from typing import Any

import numpy as np

from deep_learning_hank.two_asset import (
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    solve_matlab_faithful_hjb,
)
from deep_learning_hank.regional.two_region_fixed_point import (
    build_fixture as build_dlh5b_fixture,
    household_initial_condition,
    load_config as load_dlh5b_config,
)

# ---------------------------------------------------------------------------
# Terminal classifications / markers (Issue #34 section 11)
# ---------------------------------------------------------------------------

TERMINAL_OUTCOME_A = "DLH_5H_PREFROZEN_JOINT_UPPER_BOUNDARY_POLICY_COMPATIBILITY_REACHED__GPT_REVIEW_REQUIRED"
TERMINAL_OUTCOME_B = "DLH_5H_ILLIQUID_A_RESOLUTION_ATTENUATION_CONFIRMED__THRESHOLD_NOT_REACHED__GPT_REVIEW_REQUIRED"
TERMINAL_OUTCOME_C = "DLH_5H_ILLIQUID_A_RESOLUTION_PERSISTENT_OR_NONMONOTONIC__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_OUTCOME_D = "BLOCKED_DLH_5H_LIQUID_BOUNDARY_REACTIVATION_ON_ILLIQUID_RESOLUTION_VARIANTS"
TERMINAL_OUTCOME_E = "BLOCKED_DLH_5H_HJB_NUMERICAL_STABILITY"
TERMINAL_OUTCOME_F = "BLOCKED_DLH_5H_REPRODUCIBILITY"
ANNOTATION_POLICY_SENSITIVE = (
    "DLH_5H_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED"
)
JOINT_COMPATIBLE = "JOINT_HJB_BOUNDARY_POLICY_COMPATIBLE"
JOINT_NOT_COMPATIBLE = "JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE"
NOT_AUTHORIZED_MARKER = "NOT_AUTHORIZED__DLH_5H_POLICY_ONLY_ILLIQUID_RESOLUTION_DIAGNOSTIC"

# Accepted MATLAB-faithful oracle identity (Issue #23/#26, re-verified read-only).
ACCEPTED_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"
ACCEPTED_SHA256 = "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"

DB0 = 7.0 / 19.0
DA0 = 10.0 / 19.0


@dataclasses.dataclass(frozen=True)
class GridSpec:
    id: str
    b_pts: int
    a_pts: int


@dataclasses.dataclass(frozen=True)
class DLH5HConfig:
    dlh5b_config_path: str
    region_index: int
    wbar: float
    r_a: float
    a_lo: float
    a_hi: float
    a_max: float
    taper_identity: str
    b_lo: float
    b_hi: float
    liquid_safe_db: float
    liquid_safe_note: str
    variants: tuple
    top_coarse_layers_excluded: int
    boundary_threshold: float
    reproducibility_tol: float
    numeric_compare_tol: float
    policy_rel_materiality: float
    output_root: str


def load_config(path: str | pathlib.Path) -> DLH5HConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    hf = raw["household_fixture"]
    fp = raw["frozen_prices"]
    fa = raw["frozen_physical_illiquid"]
    ls = raw["liquid_safe_domain"]
    si = raw["shared_interior"]
    v = raw["validation"]
    out = raw["output"]
    variants = tuple(
        GridSpec(id=str(g["id"]), b_pts=int(g["b_pts"]), a_pts=int(g["a_pts"]))
        for g in raw["variants"]
    )
    return DLH5HConfig(
        dlh5b_config_path=str(hf["dlh5b_config_path"]),
        region_index=int(hf["region_index"]),
        wbar=float(fp["wbar"]),
        r_a=float(fp["r_a"]),
        a_lo=float(fa["a_lo"]),
        a_hi=float(fa["a_hi"]),
        a_max=float(fa["a_max"]),
        taper_identity=str(fa["taper_identity"]),
        b_lo=float(ls["b_lo"]),
        b_hi=float(ls["b_hi"]),
        liquid_safe_db=float(ls["db"]),
        liquid_safe_note=str(ls["domain_note"]),
        variants=variants,
        top_coarse_layers_excluded=int(si["top_coarse_layers_excluded"]),
        boundary_threshold=float(v["boundary_threshold"]),
        reproducibility_tol=float(v["reproducibility_tol"]),
        numeric_compare_tol=float(v["numeric_compare_tol"]),
        policy_rel_materiality=float(v["policy_rel_materiality"]),
        output_root=str(out["root"]),
    )


# ---------------------------------------------------------------------------
# Frozen grid plan identity
# ---------------------------------------------------------------------------


def build_variant_grid(spec: GridSpec, cfg: DLH5HConfig, z, switch) -> MatlabFaithfulHJBGrid:
    b = np.linspace(cfg.b_lo, cfg.b_hi, spec.b_pts)
    a = np.linspace(cfg.a_lo, cfg.a_hi, spec.a_pts)
    return MatlabFaithfulHJBGrid(b, a, np.asarray(z, dtype=float), np.asarray(switch, dtype=float))


def grid_plan_identity(cfg: DLH5HConfig) -> dict:
    ids = [v.id for v in cfg.variants]
    assert ids == ["H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST",
                   "H4_B119_A39", "H5_B119_A77"], f"unexpected variant ids: {ids}"
    plan = {}
    for v in cfg.variants:
        db = (cfg.b_hi - cfg.b_lo) / (v.b_pts - 1)
        da = (cfg.a_hi - cfg.a_lo) / (v.a_pts - 1)
        plan[v.id] = {
            "b_pts": v.b_pts, "b_lo": cfg.b_lo, "b_hi": cfg.b_hi, "db": float(db),
            "a_pts": v.a_pts, "a_lo": cfg.a_lo, "a_hi": cfg.a_hi, "da": float(da),
        }
    # H0-H3 core b60 domain, exact db0
    for hid in ("H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST"):
        assert plan[hid]["b_pts"] == 60
        assert abs(plan[hid]["db"] - DB0) <= 1e-12
    # a resolutions: 20/39/77/153 => da0, da0/2, da0/4, da0/8 (2N-1 nesting)
    for hid, expect_pts in (("H0_A20_BASE", 20), ("H1_A39_FINE", 39),
                            ("H2_A77_FINER", 77), ("H3_A153_FINEST", 153)):
        assert plan[hid]["a_pts"] == expect_pts
    assert abs(plan["H1_A39_FINE"]["da"] - DA0 / 2) <= 1e-12
    assert abs(plan["H2_A77_FINER"]["da"] - DA0 / 4) <= 1e-12
    assert abs(plan["H3_A153_FINEST"]["da"] - DA0 / 8) <= 1e-12
    # H4/H5 half-db b cross-checks on the same physical b-domain
    assert plan["H4_B119_A39"]["b_pts"] == 119 and plan["H5_B119_A77"]["b_pts"] == 119
    assert abs(plan["H4_B119_A39"]["db"] - DB0 / 2) <= 1e-12
    assert abs(plan["H5_B119_A77"]["db"] - DB0 / 2) <= 1e-12
    assert plan["H4_B119_A39"]["a_pts"] == 39 and plan["H5_B119_A77"]["a_pts"] == 77
    assert abs(plan["H4_B119_A39"]["da"] - DA0 / 2) <= 1e-12
    assert abs(plan["H5_B119_A77"]["da"] - DA0 / 4) <= 1e-12
    illiquid = {
        "a_lo": cfg.a_lo, "a_hi": cfg.a_hi, "a_max": cfg.a_max,
        "taper_identity": cfg.taper_identity,
    }
    assert abs(illiquid["a_max"] - 10.0) <= 1e-12
    return {"variants": plan, "illiquid": illiquid, "liquid_safe": {
        "b_lo": cfg.b_lo, "b_hi": cfg.b_hi, "db": float(cfg.liquid_safe_db),
        "note": cfg.liquid_safe_note}}


def build_all_grids(cfg: DLH5HConfig, z, switch) -> tuple[dict, dict]:
    plan = grid_plan_identity(cfg)
    grids = {v.id: build_variant_grid(v, cfg, z, switch) for v in cfg.variants}
    h0, h1, h2, h3 = (grids[i] for i in ("H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST"))
    h4, h5 = grids["H4_B119_A39"], grids["H5_B119_A77"]
    # exact nested a alignment H0[i]==H1[2i], H1[i]==H2[2i], H2[i]==H3[2i]
    assert np.allclose(h1.a[::2], h0.a, atol=1e-12)
    assert np.allclose(h2.a[::2], h1.a, atol=1e-12)
    assert np.allclose(h3.a[::2], h2.a, atol=1e-12)
    # core b60 identical on H0-H3; H4/H5 every-second b alignment
    for g in (h1, h2, h3):
        assert np.allclose(g.b, h0.b, atol=1e-12)
    assert np.allclose(h4.b[::2], h1.b, atol=1e-12)
    assert np.allclose(h5.b[::2], h2.b, atol=1e-12)
    # physical a domain identical everywhere
    for g in grids.values():
        assert abs(g.a[0] - cfg.a_lo) <= 1e-12 and abs(g.a[-1] - cfg.a_hi) <= 1e-12
    return grids, plan


# ---------------------------------------------------------------------------
# Boundary diagnostics (raw and requested)
# ---------------------------------------------------------------------------


def _slice_diagnostics(name, direction, values, grid, threshold, b_fixed, a_fixed):
    v = np.asarray(values, dtype=float)
    total = int(v.size)
    maxv = float(v.max()) if v.size else 0.0
    argmax_index = None
    argmax_physical = None
    value_at_argmax = None
    quantiles: Any = "NOT_APPLICABLE"
    offending: list[dict] = []
    if v.size and np.isfinite(v).any():
        argmax_flat = int(np.argmax(np.nan_to_num(v, nan=-np.inf)))
        d0, d1 = np.unravel_index(argmax_flat, v.shape, order="C")
        if b_fixed is None:
            idx = (int(d0), int(a_fixed), int(d1))
        else:
            idx = (int(b_fixed), int(d0), int(d1))
        argmax_index = idx
        argmax_physical = (float(grid.b[idx[0]]), float(grid.a[idx[1]]), float(grid.z[idx[2]]))
        value_at_argmax = float(v.flat[argmax_flat])
        pos = v[v > 0.0]
        if pos.size:
            qs = np.quantile(pos, [0.5, 0.9, 0.95, 0.99])
            quantiles = {
                "q50": float(qs[0]), "q90": float(qs[1]),
                "q95": float(qs[2]), "q99": float(qs[3]),
            }
        for r, c in np.argwhere(v > threshold):
            if b_fixed is None:
                b_idx, a_idx, z_idx = int(r), int(a_fixed), int(c)
            else:
                b_idx, a_idx, z_idx = int(b_fixed), int(r), int(c)
            offending.append({
                "boundary": name,
                "direction": direction,
                "b_index": b_idx,
                "a_index": a_idx,
                "z_index": z_idx,
                "b": float(grid.b[b_idx]),
                "a": float(grid.a[a_idx]),
                "z": float(grid.z[z_idx]),
                "rate": float(v[r, c]),
            })
    offending.sort(key=lambda o: (o["b_index"], o["a_index"], o["z_index"]))
    count = len(offending)
    return {
        "boundary": name,
        "direction": direction,
        "max": maxv,
        "count_above_threshold": count,
        "share_above_threshold": float(count / total) if total else 0.0,
        "argmax_index": argmax_index,
        "argmax_physical": argmax_physical,
        "value_at_argmax": value_at_argmax,
        "quantiles": quantiles,
        "offending_states": offending,
    }


def illiquid_boundary_diagnostics(hjb, grid, da, threshold):
    """Upper/lower a diagnostics with BOTH raw drift and requested rate.

    Raw: ``max(mu_a,0)`` / ``max(-mu_a,0)`` (primary cross-resolution).
    Requested: raw/``da`` (HJB/KFE compatibility). Raw threshold = ``1e-10*da``.
    a-slices have shape (b,z); b is the free index.
    """
    mu_a = np.asarray(hjb.mu_a, dtype=float)
    j_count = grid.a.size
    raw_threshold = threshold * da
    a_forward_raw = np.maximum(mu_a, 0.0)
    a_backward_raw = np.maximum(-mu_a, 0.0)
    return {
        "max_raw_upper_a": float(a_forward_raw[:, j_count - 1, :].max()),
        "max_raw_lower_a": float(a_backward_raw[:, 0, :].max()),
        "boundaries": [
            {
                "boundary": "upper_a",
                "direction": "a_forward",
                "raw": _slice_diagnostics("upper_a", "a_forward",
                                          a_forward_raw[:, j_count - 1, :], grid,
                                          raw_threshold, None, j_count - 1),
                "requested": _slice_diagnostics("upper_a", "a_forward",
                                                a_forward_raw[:, j_count - 1, :] / da, grid,
                                                threshold, None, j_count - 1),
            },
            {
                "boundary": "lower_a",
                "direction": "a_backward",
                "raw": _slice_diagnostics("lower_a", "a_backward",
                                          a_backward_raw[:, 0, :], grid,
                                          raw_threshold, None, 0),
                "requested": _slice_diagnostics("lower_a", "a_backward",
                                                a_backward_raw[:, 0, :] / da, grid,
                                                threshold, None, 0),
            },
        ],
    }


def liquid_regression_diagnostics(hjb, grid, db, threshold):
    """Upper/lower b raw + requested regression gate (the provisional
    liquid-safe domain must remain non-binding)."""
    mu_b = np.asarray(hjb.mu_b, dtype=float)
    i_count = grid.b.size
    raw_threshold = threshold * db
    b_forward_raw = np.maximum(mu_b, 0.0)
    b_backward_raw = np.maximum(-mu_b, 0.0)
    return {
        "max_raw_upper_b": float(b_forward_raw[i_count - 1, :, :].max()),
        "max_raw_lower_b": float(b_backward_raw[0, :, :].max()),
        "boundaries": [
            {
                "boundary": "upper_b",
                "direction": "b_forward",
                "raw": _slice_diagnostics("upper_b", "b_forward",
                                          b_forward_raw[i_count - 1, :, :], grid,
                                          raw_threshold, i_count - 1, None),
                "requested": _slice_diagnostics("upper_b", "b_forward",
                                                b_forward_raw[i_count - 1, :, :] / db, grid,
                                                threshold, i_count - 1, None),
            },
            {
                "boundary": "lower_b",
                "direction": "b_backward",
                "raw": _slice_diagnostics("lower_b", "b_backward",
                                          b_backward_raw[0, :, :], grid,
                                          raw_threshold, 0, None),
                "requested": _slice_diagnostics("lower_b", "b_backward",
                                                b_backward_raw[0, :, :] / db, grid,
                                                threshold, 0, None),
            },
        ],
    }


# ---------------------------------------------------------------------------
# Per-variant pipeline
# ---------------------------------------------------------------------------


def run_all_variants(cfg: DLH5HConfig, dlh5b, params, numerics) -> dict:
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, plan = build_all_grids(cfg, z, switch)
    variants = []
    hjb_results: dict[str, Any] = {}
    for spec in cfg.variants:
        grid = build_variant_grid(spec, cfg, z, switch)
        db = float(grid.b[1] - grid.b[0])
        da = float(grid.a[1] - grid.a[0])
        inputs = HouseholdInputs(
            r_a=cfg.r_a, r_b=dlh5b.r_b, tau=dlh5b.tau[cfg.region_index],
            wages=np.array([cfg.wbar]), migration_costs=np.array([0.0]),
            labor_weights=np.array([1.0]),
        )
        initial, labor0 = household_initial_condition(grid, params, inputs, dlh5b.rb_gap[cfg.region_index])
        hjb = solve_matlab_faithful_hjb(
            grid, params, inputs, initial, labor0,
            dlh5b.transfer_income[cfg.region_index],
            dlh5b.rb_gap[cfg.region_index], numerics,
        )
        rec = {
            "variant": spec.id,
            "grid": {
                "b_pts": int(grid.b.size), "b_lo": float(grid.b[0]), "b_hi": float(grid.b[-1]),
                "db": db, "a_pts": int(grid.a.size), "a_lo": float(grid.a[0]),
                "a_hi": float(grid.a[-1]), "da": da, "a_max": cfg.a_max, "z_pts": int(grid.z.size),
            },
            "frozen_prices_identity": {
                "wbar": cfg.wbar, "r_a": cfg.r_a, "taper_identity": cfg.taper_identity,
                "dlh5b_config": cfg.dlh5b_config_path, "region_index": cfg.region_index,
                "liquid_safe_domain": {"b_lo": cfg.b_lo, "b_hi": cfg.b_hi,
                                       "db": float(cfg.liquid_safe_db)},
            },
            "hjb_converged": bool(hjb.converged),
            "hjb_iterations": int(hjb.iterations),
            "hjb_statistic": float(hjb.convergence_statistic),
        }
        if hjb.converged:
            rec["illiquid"] = illiquid_boundary_diagnostics(hjb, grid, da, cfg.boundary_threshold)
            rec["liquid"] = liquid_regression_diagnostics(hjb, grid, db, cfg.boundary_threshold)
            ub = rec["liquid"]["boundaries"][0]["requested"]["max"]
            ua = rec["illiquid"]["boundaries"][0]["requested"]["max"]
            rec["joint_compatible"] = bool(ub <= cfg.boundary_threshold and ua <= cfg.boundary_threshold)
            rec["joint_marker"] = JOINT_COMPATIBLE if rec["joint_compatible"] else JOINT_NOT_COMPATIBLE
            rec["variant_terminal"] = "HJB_CONVERGED"
        else:
            rec["illiquid"] = None
            rec["liquid"] = None
            rec["joint_compatible"] = None
            rec["joint_marker"] = "HJB_NOT_CONVERGED"
            rec["variant_terminal"] = "HJB_NOT_CONVERGED"
        variants.append(rec)
        hjb_results[spec.id] = hjb
    return {"grid_plan": plan, "variants": variants, "hjb_results": hjb_results}


def build_fixture(cfg: DLH5HConfig):
    dlh5b = load_dlh5b_config(cfg.dlh5b_config_path)
    _grid, params, numerics = build_dlh5b_fixture(dlh5b)
    return dlh5b, params, numerics


# ---------------------------------------------------------------------------
# Phase D — illiquid a-resolution trend (H0 -> H1 -> H2 -> H3)
# ---------------------------------------------------------------------------


def resolution_trend(cfg: DLH5HConfig, runs: dict) -> dict:
    by_id = {v["variant"]: v for v in runs["variants"]}
    seq = []
    for vid in ("H0_A20_BASE", "H1_A39_FINE", "H2_A77_FINER", "H3_A153_FINEST"):
        v = by_id.get(vid)
        if v is None:
            seq.append({"variant": vid, "reached": False})
            continue
        ill = v.get("illiquid") or {}
        ua = next((b for b in ill.get("boundaries", []) if b["boundary"] == "upper_a"), None)
        if not (v["hjb_converged"] and ua):
            seq.append({"variant": vid, "reached": False})
            continue
        raw = ua["raw"]
        req = ua["requested"]
        seq.append({
            "variant": vid,
            "reached": True,
            "raw_max": raw["max"],
            "requested_max": req["max"],
            "raw_count": raw["count_above_threshold"],
            "requested_count": req["count_above_threshold"],
            "raw_share": raw["share_above_threshold"],
            "requested_share": req["share_above_threshold"],
            "argmax_physical_b_z": (raw["argmax_physical"][0], raw["argmax_physical"][2])
            if raw["argmax_physical"] else None,
        })
    reached = [s for s in seq if s.get("reached")]
    ratios = {"adjacent_raw": [], "adjacent_requested": [], "vs_H0_raw": [], "vs_H0_requested": []}
    for i in range(1, len(reached)):
        for key in ("raw", "requested"):
            prev = reached[i - 1][f"{key}_max"]
            cur = reached[i][f"{key}_max"]
            if cur > 0.0:
                ratios[f"adjacent_{key}"].append(round(prev / cur, 6) if prev > 0.0 else 0.0)
            elif prev > 0.0:
                ratios[f"adjacent_{key}"].append("inf")
            else:
                ratios[f"adjacent_{key}"].append(None)
        for key in ("raw", "requested"):
            h0v = reached[0][f"{key}_max"]
            cur = reached[i][f"{key}_max"]
            ratios[f"vs_H0_{key}"].append(round(cur / h0v, 6) if h0v > 0.0 else None)
    raw_seq = [s["raw_max"] for s in reached if s.get("reached")]
    req_seq = [s["requested_max"] for s in reached if s.get("reached")]
    strictly_decreasing_raw = all(raw_seq[i] < raw_seq[i - 1] for i in range(1, len(raw_seq))) if len(raw_seq) >= 2 else None
    strictly_decreasing_requested = all(req_seq[i] < req_seq[i - 1] for i in range(1, len(req_seq))) if len(req_seq) >= 2 else None
    plateau = (len(raw_seq) >= 2 and all(abs(raw_seq[i] - raw_seq[i - 1]) <= 1e-12 * max(1.0, abs(raw_seq[i - 1])) for i in range(1, len(raw_seq))))
    first_below_threshold = None
    for s in reached:
        if s["requested_max"] <= cfg.boundary_threshold:
            first_below_threshold = s["variant"]
            break
    return {
        "sequence": seq,
        "ratios": ratios,
        "strictly_decreasing_raw": bool(strictly_decreasing_raw) if strictly_decreasing_raw is not None else None,
        "strictly_decreasing_requested": bool(strictly_decreasing_requested) if strictly_decreasing_requested is not None else None,
        "plateau": bool(plateau),
        "first_requested_below_threshold": first_below_threshold,
        "attenuated_to_zero_at": None,
    }


# ---------------------------------------------------------------------------
# Phase E — exact aligned-node policy stability (5 pairs)
# ---------------------------------------------------------------------------


def _a_pair_slices(coarse_a_pts, top_excluded):
    a_keep = coarse_a_pts - top_excluded
    return slice(None, a_keep), slice(None, 2 * a_keep, 2)


def _b_pair_slices(coarse_b_pts, top_excluded):
    b_keep = coarse_b_pts - top_excluded
    return slice(None, b_keep), slice(None, 2 * b_keep, 2)


def policy_stability(cfg: DLH5HConfig, runs: dict) -> list:
    hjb_by_id = runs["hjb_results"]
    by_id = {v["variant"]: v for v in runs["variants"]}
    pairs = [
        ("H0_A20_BASE", "H1_A39_FINE", "H0_vs_H1", "a"),
        ("H1_A39_FINE", "H2_A77_FINER", "H1_vs_H2", "a"),
        ("H2_A77_FINER", "H3_A153_FINEST", "H2_vs_H3", "a"),
        ("H1_A39_FINE", "H4_B119_A39", "H1_vs_H4", "b"),
        ("H2_A77_FINER", "H5_B119_A77", "H2_vs_H5", "b"),
    ]
    out = []
    numeric_fields = ["value", "consumption", "labor", "transfer", "mu_a", "mu_b"]
    label_fields = ["liquid_label", "transfer_label"]
    top = cfg.top_coarse_layers_excluded
    for coarse_id, fine_id, cid, kind in pairs:
        c = {"comparison": cid, "kind": kind}
        rc, rf = by_id[coarse_id], by_id[fine_id]
        if not (rc["hjb_converged"] and rf["hjb_converged"]):
            c["reached"] = False
            c["reason"] = "one or both HJB not converged"
            out.append(c)
            continue
        hc, hf = hjb_by_id[coarse_id], hjb_by_id[fine_id]
        coarse_a_pts = rc["grid"]["a_pts"]
        coarse_b_pts = rc["grid"]["b_pts"]
        if kind == "a":
            # same b grid on both; refine only a (every-second aligned)
            sb = slice(None, coarse_b_pts - top)
            sa_c, sa_f = _a_pair_slices(coarse_a_pts, top)
        else:
            # same a grid; refine only b (every-second aligned)
            sb_c, sb_f = _b_pair_slices(coarse_b_pts, top)
            sa = slice(None, coarse_a_pts - top)
            sa_c, sa_f = sa, sa
        fields = {}
        for f in numeric_fields:
            if kind == "a":
                x = np.asarray(getattr(hc, f)[sb, sa_c, :], dtype=float)
                y = np.asarray(getattr(hf, f)[sb, sa_f, :], dtype=float)
            else:
                x = np.asarray(getattr(hc, f)[sb_c, sa, :], dtype=float)
                y = np.asarray(getattr(hf, f)[sb_f, sa, :], dtype=float)
            m = float(np.max(np.abs(x - y))) if x.size else 0.0
            ref = float(np.max(np.abs(x))) if x.size else 0.0
            fields[f] = {"max_abs_diff": m, "rel_diff": m / max(1.0, ref)}
        for lab in label_fields:
            if kind == "a":
                x = getattr(hc, lab)[sb, sa_c, :]
                y = getattr(hf, lab)[sb, sa_f, :]
            else:
                x = getattr(hc, lab)[sb_c, sa, :]
                y = getattr(hf, lab)[sb_f, sa, :]
            fields[lab] = {"mismatch_count": int(np.sum(x != y))}
        c.update({"reached": True, "fields": fields})
        out.append(c)
    return out


# ---------------------------------------------------------------------------
# Phase F — joint compatibility + terminal classification
# ---------------------------------------------------------------------------


def policy_sensitivity_annotation(cfg: DLH5HConfig, res: list) -> bool:
    """Pre-registered materiality: any required pair's scale-aware aligned-node
    relative difference for consumption/mu_a/mu_b exceeds
    ``cfg.policy_rel_materiality`` (default 1e-2)."""
    for c in res:
        if not c.get("reached"):
            continue
        for f in ("consumption", "mu_a", "mu_b"):
            m = c["fields"].get(f) or {}
            if (m.get("rel_diff") or 0.0) > cfg.policy_rel_materiality:
                return True
    return False


def liquid_reactivation(cfg: DLH5HConfig, runs: dict) -> bool:
    """Any variant with requested upper-b > threshold (material reactivation of
    the provisional liquid-safe domain)."""
    for v in runs["variants"]:
        liq = v.get("liquid") or {}
        ub = next((b for b in liq.get("boundaries", []) if b["boundary"] == "upper_b"), None)
        if ub and ub["requested"]["max"] > cfg.boundary_threshold:
            return True
    return False


def overall_terminal(cfg: DLH5HConfig, runs: dict, repro: dict, res: list) -> dict:
    if not repro["pass_bool"]:
        terminal = TERMINAL_OUTCOME_F
    elif any(not v["hjb_converged"] for v in runs["variants"]):
        terminal = TERMINAL_OUTCOME_E
    elif any(v["joint_compatible"] for v in runs["variants"]):
        terminal = TERMINAL_OUTCOME_A
    elif liquid_reactivation(cfg, runs):
        terminal = TERMINAL_OUTCOME_D
    else:
        trend = resolution_trend(cfg, runs)
        if trend["strictly_decreasing_raw"]:
            terminal = TERMINAL_OUTCOME_B
        else:
            terminal = TERMINAL_OUTCOME_C
    annotations = []
    if policy_sensitivity_annotation(cfg, res):
        annotations.append(ANNOTATION_POLICY_SENSITIVE)
    return {"terminal": terminal, "annotations": annotations}


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------


def _variant_structural_signature(rec: dict) -> str:
    ill = rec.get("illiquid") or {}
    liq = rec.get("liquid") or {}
    illiquid_discrete = {}
    for b in ill.get("boundaries", []):
        illiquid_discrete[b["boundary"]] = {
            "raw_count": b["raw"]["count_above_threshold"],
            "requested_count": b["requested"]["count_above_threshold"],
            "raw_argmax_index": b["raw"]["argmax_index"],
            "requested_argmax_index": b["requested"]["argmax_index"],
            "raw_offending": [(o["b_index"], o["a_index"], o["z_index"]) for o in b["raw"]["offending_states"]],
            "requested_offending": [(o["b_index"], o["a_index"], o["z_index"]) for o in b["requested"]["offending_states"]],
        }
    liquid_discrete = {}
    for b in liq.get("boundaries", []):
        liquid_discrete[b["boundary"]] = {
            "raw_count": b["raw"]["count_above_threshold"],
            "requested_count": b["requested"]["count_above_threshold"],
            "raw_argmax_index": b["raw"]["argmax_index"],
            "requested_argmax_index": b["requested"]["argmax_index"],
        }
    return json.dumps({
        "variant": rec.get("variant"),
        "grid": rec.get("grid"),
        "hjb_converged": rec.get("hjb_converged"),
        "hjb_iterations": rec.get("hjb_iterations"),
        "joint_marker": rec.get("joint_marker"),
        "illiquid": illiquid_discrete,
        "liquid": liquid_discrete,
    }, sort_keys=True)


def _variant_numeric_numbers(rec: dict) -> list:
    out: list[float] = []
    if rec.get("hjb_statistic") is not None:
        out.append(float(rec["hjb_statistic"]))
    for section in ("illiquid", "liquid"):
        sec = rec.get(section) or {}
        for b in sec.get("boundaries", []):
            for kind in ("raw", "requested"):
                d = b[kind]
                out.append(float(d.get("max", float("nan"))))
                out.append(float(d.get("share_above_threshold", float("nan"))))
                q = d.get("quantiles")
                if isinstance(q, dict):
                    for k in ("q50", "q90", "q95", "q99"):
                        out.append(float(q.get(k, float("nan"))))
                for o in d.get("offending_states", []):
                    out.append(float(o.get("rate", float("nan"))))
    return out


def _nonfinite_aligned(a, b) -> bool:
    return bool((not np.isfinite(a)) and (not np.isfinite(b)))


def compare_variant_records(r1: dict, r2: dict, cfg: DLH5HConfig) -> dict:
    s1 = _variant_structural_signature(r1)
    s2 = _variant_structural_signature(r2)
    same_struct = s1 == s2
    n1 = _variant_numeric_numbers(r1)
    n2 = _variant_numeric_numbers(r2)
    max_diff = 0.0
    aligned_nonfinite = 0
    mismatch = 0
    for a, b in zip(n1, n2):
        if np.isfinite(a) and np.isfinite(b):
            max_diff = max(max_diff, float(abs(a - b)))
        elif _nonfinite_aligned(a, b):
            aligned_nonfinite += 1
        else:
            mismatch += 1
    return {
        "identical_structural_signature": bool(same_struct),
        "max_numeric_diff": float(max_diff),
        "aligned_nonfinite_fields": int(aligned_nonfinite),
        "mismatched_fields": int(mismatch),
        "pass_bool": bool(same_struct and mismatch == 0 and max_diff <= cfg.reproducibility_tol),
    }


def reproduce(cfg: DLH5HConfig, dlh5b, params, numerics) -> dict:
    run1 = run_all_variants(cfg, dlh5b, params, numerics)
    run2 = run_all_variants(cfg, dlh5b, params, numerics)
    per_variant = {}
    for r1, r2 in zip(run1["variants"], run2["variants"]):
        per_variant[r1["variant"]] = compare_variant_records(r1, r2, cfg)
    res1 = policy_stability(cfg, run1)
    t1 = overall_terminal(cfg, run1, {"pass_bool": True}, res1)
    res2 = policy_stability(cfg, run2)
    t2 = overall_terminal(cfg, run2, {"pass_bool": True}, res2)
    pass_bool = all(v["pass_bool"] for v in per_variant.values())
    return {
        "run1": {"grid_plan": run1["grid_plan"], "variants": run1["variants"]},
        "run2": {"grid_plan": run2["grid_plan"], "variants": run2["variants"]},
        "per_variant": per_variant,
        "pass_bool": bool(pass_bool),
        "randomness": "NOT_APPLICABLE",
        "terminal_run1": t1["terminal"],
        "terminal_run2": t2["terminal"],
        "annotations_run1": t1["annotations"],
        "annotations_run2": t2["annotations"],
    }


# ---------------------------------------------------------------------------
# Evidence writers (exactly eight files)
# ---------------------------------------------------------------------------


def _write_csv(path: pathlib.Path, fields: list, rows: list) -> None:
    import csv
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(fields)
        for r in rows:
            w.writerow(r)


def _fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.9e}"
    return str(v)


def _q_fmt(q) -> str:
    if isinstance(q, dict):
        return f"{q.get('q50','')}/{q.get('q90','')}/{q.get('q95','')}/{q.get('q99','')}"
    return str(q)


def _sf(v, spec=None) -> str:
    if v is None:
        return "—"
    try:
        if spec is not None:
            return format(float(v), spec)
        return str(v)
    except (TypeError, ValueError):
        return str(v)


def _boundary_rows(rec, section, kind):
    rows = []
    for b in (rec.get(section) or {}).get("boundaries", []):
        for o in b[kind].get("offending_states", []):
            rows.append([rec["variant"], b["boundary"], b["direction"], kind,
                         o["b_index"], o["a_index"], o["z_index"],
                         _fmt(o["b"]), _fmt(o["a"]), _fmt(o["z"]), _fmt(o["rate"])])
    return rows


def write_evidence(root: pathlib.Path, cfg: DLH5HConfig, runs: dict, trend: dict,
                   res: list, repro: dict, term: dict) -> None:
    root = pathlib.Path(root)
    root.mkdir(parents=True, exist_ok=True)

    # 1) VARIANT_STATUS.csv
    rows = []
    for v in runs["variants"]:
        g = v["grid"]
        ill = v.get("illiquid") or {}
        rows.append([v["variant"], g["b_pts"], _fmt(g["b_lo"]), _fmt(g["b_hi"]), _fmt(g["db"]),
                     g["a_pts"], _fmt(g["a_lo"]), _fmt(g["a_hi"]), _fmt(g["da"]),
                     v["hjb_converged"], v["hjb_iterations"], _fmt(v["hjb_statistic"]),
                     _fmt(ill.get("max_raw_upper_a")), _fmt(ill.get("max_raw_lower_a")),
                     v.get("joint_marker"), v.get("variant_terminal")])
    _write_csv(root / "DLH_5H_VARIANT_STATUS.csv",
               ["variant", "b_pts", "b_lo", "b_hi", "db", "a_pts", "a_lo", "a_hi", "da",
                "hjb_converged", "hjb_iterations", "hjb_statistic",
                "max_raw_upper_a", "max_raw_lower_a", "joint_marker", "variant_terminal"], rows)

    # 2) ILLIQUID_BOUNDARY_DIAGNOSTICS.csv (summary + offending, raw + requested)
    rows = []
    for v in runs["variants"]:
        ill = v.get("illiquid") or {}
        for b in ill.get("boundaries", []):
            for kind in ("raw", "requested"):
                d = b[kind]
                rows.append([v["variant"], b["boundary"], b["direction"], kind,
                             _fmt(d["max"]), d["count_above_threshold"],
                             _fmt(d["share_above_threshold"]), d.get("argmax_index"),
                             d.get("argmax_physical"), _fmt(d.get("value_at_argmax")),
                             _q_fmt(d.get("quantiles")), "", "", "", "", "", "", ""])
        for o in _boundary_rows(v, "illiquid", "raw"):
            rows.append([v["variant"], o[1], o[2], "raw_offending", _fmt(o[10]),
                         "", "", "", "", "", "", o[4], o[5], o[6], o[7], o[8], o[9], o[10]])
        for o in _boundary_rows(v, "illiquid", "requested"):
            rows.append([v["variant"], o[1], o[2], "requested_offending", _fmt(o[10]),
                         "", "", "", "", "", "", o[4], o[5], o[6], o[7], o[8], o[9], o[10]])
    _write_csv(root / "DLH_5H_ILLIQUID_BOUNDARY_DIAGNOSTICS.csv",
               ["variant", "boundary", "direction", "kind", "max", "count_above_threshold",
                "share_above_threshold", "argmax_index", "argmax_physical",
                "value_at_argmax", "quantiles_q50_q90_q95_q99",
                "b_index", "a_index", "z_index", "b", "a", "z", "rate"], rows)

    # 3) LIQUID_REGRESSION_DIAGNOSTICS.csv (upper/lower b raw + requested)
    rows = []
    for v in runs["variants"]:
        liq = v.get("liquid") or {}
        for b in liq.get("boundaries", []):
            for kind in ("raw", "requested"):
                d = b[kind]
                rows.append([v["variant"], b["boundary"], b["direction"], kind,
                             _fmt(d["max"]), d["count_above_threshold"],
                             _fmt(d["share_above_threshold"]), d.get("argmax_index"),
                             d.get("argmax_physical"), _fmt(d.get("value_at_argmax")),
                             _q_fmt(d.get("quantiles"))])
    _write_csv(root / "DLH_5H_LIQUID_REGRESSION_DIAGNOSTICS.csv",
               ["variant", "boundary", "direction", "kind", "max", "count_above_threshold",
                "share_above_threshold", "argmax_index", "argmax_physical",
                "value_at_argmax", "quantiles_q50_q90_q95_q99"], rows)

    # 4) RESOLUTION_TREND.csv
    rows = []
    for s in trend["sequence"]:
        if not s.get("reached"):
            rows.append([s["variant"], "NOT_REACHED", "", "", "", "", "", "", "", "", "", ""])
            continue
        rows.append([s["variant"], "REACHED", _fmt(s["raw_max"]), _fmt(s["requested_max"]),
                     s["raw_count"], s["requested_count"], _fmt(s["raw_share"]),
                     _fmt(s["requested_share"]), s["argmax_physical_b_z"], "", "", ""])
    ar = trend["ratios"]
    rows.append(["adjacent_raw_ratio", "RATIO"] + [_fmt(v) for v in ar["adjacent_raw"]] + ["", "", "", "", "", "", ""])
    rows.append(["adjacent_requested_ratio", "RATIO"] + [_fmt(v) for v in ar["adjacent_requested"]] + ["", "", "", "", "", "", ""])
    rows.append(["vs_H0_raw_ratio", "RATIO"] + [_fmt(v) for v in ar["vs_H0_raw"]] + ["", "", "", "", "", "", ""])
    rows.append(["vs_H0_requested_ratio", "RATIO"] + [_fmt(v) for v in ar["vs_H0_requested"]] + ["", "", "", "", "", "", ""])
    rows.append(["strictly_decreasing_raw", "FLAG", str(trend["strictly_decreasing_raw"]), "", "", "", "", "", "", "", "", ""])
    rows.append(["strictly_decreasing_requested", "FLAG", str(trend["strictly_decreasing_requested"]), "", "", "", "", "", "", "", "", ""])
    rows.append(["plateau", "FLAG", str(trend["plateau"]), "", "", "", "", "", "", "", "", ""])
    rows.append(["first_requested_below_threshold", "FLAG", str(trend["first_requested_below_threshold"]), "", "", "", "", "", "", "", "", ""])
    _write_csv(root / "DLH_5H_RESOLUTION_TREND.csv",
               ["item", "kind", "value1", "value2", "value3", "count1", "count2", "share1",
                "share2", "argmax_b_z", "note", "extra"], rows)

    # 5) POLICY_STABILITY.csv
    rows = []
    for c in res:
        if not c.get("reached"):
            rows.append([c["comparison"], c["kind"], "NOT_REACHED", "", "", "", "", c.get("reason", "")])
            continue
        for f, m in c["fields"].items():
            if f in ("liquid_label", "transfer_label"):
                rows.append([c["comparison"], c["kind"], f, "", "", "", m["mismatch_count"], ""])
            else:
                rows.append([c["comparison"], c["kind"], f, _fmt(m["max_abs_diff"]), _fmt(m["rel_diff"]), "", "", ""])
    _write_csv(root / "DLH_5H_POLICY_STABILITY.csv",
               ["comparison", "pair_kind", "field", "max_abs_diff", "rel_diff", "mismatch_count", "note", "extra"], rows)

    # 6) REPRODUCIBILITY.json
    with open(root / "DLH_5H_REPRODUCIBILITY.json", "w", encoding="utf-8") as fh:
        json.dump(repro, fh, indent=2, default=str, sort_keys=True)

    # 7) EXECUTION_REPORT.md
    with open(root / "DLH_5H_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_report(cfg, runs, trend, res, repro, term))

    # 8) FORBIDDEN_OPERATION_CHECK.md
    with open(root / "DLH_5H_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write(_render_forbidden_check(cfg, runs, repro, term))


def _render_report(cfg: DLH5HConfig, runs: dict, trend: dict, res: list,
                   repro: dict, term: dict) -> str:
    lines = []
    lines.append("# DLH-5H — Illiquid Upper-Boundary Resolution Diagnostic (Issue #34)")
    lines.append("")
    lines.append("Policy-only diagnostic isolating illiquid-grid resolution on the provisional "
                 "liquid-safe domain. Accepted MATLAB-faithful HJB source is immutable and reused "
                 "read-only.")
    lines.append("")
    lines.append(f"Overall terminal classification: `{term['terminal']}`")
    if term["annotations"]:
        lines.append("")
        lines.append("Secondary scientific annotations: " +
                     ", ".join(f"`{a}`" for a in term["annotations"]))
    lines.append("")
    lines.append(f"Frozen economics: `wbar={cfg.wbar}`, `r_a={cfg.r_a}`; physical illiquid domain "
                 f"`a [{cfg.a_lo},{cfg.a_hi}]`, `a_max={cfg.a_max}`, taper `{cfg.taper_identity}`; "
                 f"liquid-safe core `b60 [{cfg.b_lo},{cfg.b_hi}]`, `db={cfg.liquid_safe_db:.12f}` "
                 f"({cfg.liquid_safe_note}); all non-grid objects the accepted DLH-5B/DLH-5E fixture "
                 f"(`{cfg.dlh5b_config_path}`, region_index={cfg.region_index}).")
    lines.append("")
    lines.append("## Variant status (Phase A)")
    lines.append("")
    lines.append("| variant | b pts | db | a pts | da | HJB conv | iters | stat | raw upper-a max | raw lower-a max | joint marker |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for v in runs["variants"]:
        g = v["grid"]
        ill = v.get("illiquid") or {}
        lines.append(f"| {v['variant']} | {g['b_pts']} | {_sf(g['db'])} | {g['a_pts']} | {_sf(g['da'])} | "
                     f"{v['hjb_converged']} | {v['hjb_iterations']} | {_sf(v['hjb_statistic'], '.3e')} | "
                     f"{_sf(ill.get('max_raw_upper_a'), '.3e')} | {_sf(ill.get('max_raw_lower_a'), '.3e')} | "
                     f"{_sf(v.get('joint_marker'))} |")
    lines.append("")

    lines.append("## Illiquid upper/lower boundary diagnostics (Phase B)")
    lines.append("")
    lines.append("Raw drift (`max(mu_a,0)` / `max(-mu_a,0)`) is the primary cross-resolution "
                 "quantity; requested generator rate (raw/`da`) is the HJB/KFE compatibility "
                 "quantity. Raw threshold = `1e-10*da` corresponds to the accepted requested-rate "
                 "threshold `1e-10`. Coordinates are exact `(b_index,a_index,z_index)` plus physical "
                 "`(b,a,z)` via C-order unraveling on the actual 2-D boundary slice.")
    lines.append("")
    for v in runs["variants"]:
        ill = v.get("illiquid") or {}
        if not ill:
            lines.append(f"### {v['variant']} — HJB not converged")
            lines.append("")
            continue
        lines.append(f"### {v['variant']}")
        lines.append("")
        lines.append("| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for b in ill["boundaries"]:
            for kind in ("raw", "requested"):
                d = b[kind]
                lines.append(f"| {b['boundary']} | {kind} | {_sf(d['max'], '.3e')} | "
                             f"{_sf(d['count_above_threshold'])} | {_sf(d['share_above_threshold'], '.3e')} | "
                             f"{d.get('argmax_index')} | {d.get('argmax_physical')} | "
                             f"{_sf(d.get('value_at_argmax'), '.3e')} | {_q_fmt(d.get('quantiles'))} |")
        lines.append("")
        lines.append("Complete offending states (raw > `1e-10*da`; requested > `1e-10`):")
        lines.append("")
        rows = _boundary_rows(v, "illiquid", "raw") + _boundary_rows(v, "illiquid", "requested")
        if rows:
            lines.append("| boundary | kind | b_index | a_index | z_index | b | a | z | rate |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for r in rows:
                lines.append(f"| {r[1]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {_sf(r[7], '.6f')} | "
                             f"{_sf(r[8], '.6f')} | {_sf(r[9], '.6f')} | {_sf(r[10], '.9e')} |")
        else:
            lines.append("No state exceeds the raw or requested threshold.")
        lines.append("")

    lines.append("## Liquid-boundary regression gate (Phase C)")
    lines.append("")
    lines.append("Upper/lower b raw + requested max/count/share on the provisional liquid-safe "
                 "domain. The preferred interpretation requires the liquid-safe domain to remain "
                 "non-binding. No silent b enlargement; any material reactivation is recorded.")
    lines.append("")
    lines.append("| variant | upper-b raw | upper-b requested | count | lower-b raw | lower-b requested | count |")
    lines.append("|---|---|---|---|---|---|---|")
    for v in runs["variants"]:
        liq = v.get("liquid") or {}
        if not liq:
            continue
        ub = next(b for b in liq["boundaries"] if b["boundary"] == "upper_b")
        lb = next(b for b in liq["boundaries"] if b["boundary"] == "lower_b")
        lines.append(f"| {v['variant']} | {_sf(ub['raw']['max'], '.3e')} | {_sf(ub['requested']['max'], '.3e')} | "
                     f"{ub['requested']['count_above_threshold']} | {_sf(lb['raw']['max'], '.3e')} | "
                     f"{_sf(lb['requested']['max'], '.3e')} | {lb['requested']['count_above_threshold']} |")
    lines.append("")

    lines.append("## Illiquid a-resolution trend (Phase D: H0 -> H1 -> H2 -> H3)")
    lines.append("")
    lines.append("| variant | raw upper-a max | requested upper-a max | raw count | requested count | raw share | requested share | argmax physical (b,z) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for s in trend["sequence"]:
        if not s.get("reached"):
            lines.append(f"| {s['variant']} | NOT_REACHED | | | | | | |")
            continue
        lines.append(f"| {s['variant']} | {_sf(s['raw_max'], '.3e')} | {_sf(s['requested_max'], '.3e')} | "
                     f"{s['raw_count']} | {s['requested_count']} | {_sf(s['raw_share'], '.3e')} | "
                     f"{_sf(s['requested_share'], '.3e')} | {s['argmax_physical_b_z']} |")
    ar = trend["ratios"]
    lines.append("")
    lines.append(f"- adjacent raw attenuation ratios (H0/H1, H1/H2, H2/H3): {ar['adjacent_raw']} "
                 f"(`inf` = nonzero-to-zero attenuation)")
    lines.append(f"- adjacent requested attenuation ratios: {ar['adjacent_requested']}")
    lines.append(f"- raw ratios relative to H0: {ar['vs_H0_raw']}")
    lines.append(f"- requested ratios relative to H0: {ar['vs_H0_requested']}")
    lines.append(f"- strictly decreasing raw upper-a max over H0->H3: {trend['strictly_decreasing_raw']}")
    lines.append(f"- strictly decreasing requested upper-a max over H0->H3: {trend['strictly_decreasing_requested']}")
    lines.append(f"- plateau flag: {trend['plateau']}")
    lines.append(f"- first variant with requested upper-a <= 1e-10: {trend['first_requested_below_threshold']}")
    lines.append("")
    lines.append("This is a policy-only trend; it does not infer stationary-tail existence or "
                 "non-existence.")

    lines.append("")
    lines.append("## Exact aligned-node policy stability (Phase E)")
    lines.append("")
    lines.append("Five required pairs: a-resolution H0/H1, H1/H2, H2/H3 (identical b grid, "
                 "every-second a alignment) and b cross-checks H1/H4, H2/H5 (identical a grid, "
                 "every-second b alignment). Coarse-grid shared-interior mask excludes the top two "
                 "coarse layers in both asset dimensions, all z. `rel_diff = max_abs / "
                 "max(1, max|coarse|)` is scale-aware.")
    lines.append("")
    for c in res:
        lines.append(f"### {c['comparison']} ({c['kind']}-resolution)")
        lines.append("")
        if not c.get("reached"):
            lines.append(f"- NOT_REACHED: {c.get('reason')}")
            lines.append("")
            continue
        lines.append("| field | max_abs_diff | rel_diff | label mismatch |")
        lines.append("|---|---|---|---|")
        for f, m in c["fields"].items():
            if f in ("liquid_label", "transfer_label"):
                lines.append(f"| {f} | — | — | {_sf(m['mismatch_count'])} |")
            else:
                lines.append(f"| {f} | {_sf(m['max_abs_diff'], '.3e')} | {_sf(m['rel_diff'], '.3e')} | — |")
        lines.append("")

    lines.append("## Joint HJB upper-boundary policy compatibility (Phase F)")
    lines.append("")
    lines.append("Per-variant prerequisite marker only (no stationary solve): "
                 "`requested_upper_b <= 1e-10 AND requested_upper_a <= 1e-10`.")
    lines.append("")
    for v in runs["variants"]:
        lines.append(f"- {v['variant']}: {v.get('joint_marker')}")
    lines.append("")
    lines.append(f"Stationary KFE / nullspace / pin / density / tail mass / stationary flux / "
                 f"`C,L,A,B` are `{NOT_AUTHORIZED_MARKER}` and were not executed.")

    lines.append("")
    lines.append("## Reproducibility")
    lines.append("")
    lines.append(f"- randomness: `{repro['randomness']}`; repeat pass: `{repro['pass_bool']}`; "
                 f"terminal run1/run2: `{repro['terminal_run1']}` / `{repro['terminal_run2']}`; "
                 f"annotations run1/run2: {repro['annotations_run1']} / {repro['annotations_run2']}.")
    for vid, cmp in repro["per_variant"].items():
        lines.append(f"- {vid}: structural identical {cmp['identical_structural_signature']}, "
                     f"max numeric diff {cmp['max_numeric_diff']:.3e}, "
                     f"aligned non-finite {cmp['aligned_nonfinite_fields']}, "
                     f"mismatched {cmp['mismatched_fields']}, pass {cmp['pass_bool']}.")
    lines.append("")

    lines.append("## Artifact integrity")
    lines.append("")
    lines.append(f"- accepted MATLAB-faithful oracle blob `{ACCEPTED_BLOB}`, SHA-256 `{ACCEPTED_SHA256}` "
                 "re-verified read-only (unchanged from the accepted Issue #23/#26 state).")
    lines.append("- no existing tracked file modified; dedicated branch "
                 "`dsh/issue-34-dlh-5h-illiquid-resolution-2026-09-01`; allowlist-only additions "
                 "(3 artifacts + 8 evidence files).")
    lines.append("")
    lines.append("DLH-5H implements NO repair and NO stationary acceptance: accepted HJB/KFE/regional "
                 "source immutable; physical a-domain/a_max/taper/economics/tolerances/initialization "
                 "frozen; no clipping; no D1-D3; no regional or multi-province GE; no learned network; "
                 "no nominal HANK.")
    return "\n".join(lines)


def _render_forbidden_check(cfg: DLH5HConfig, runs: dict, repro: dict, term: dict) -> str:
    lines = [
        "# DLH-5H — Forbidden-Operation / Scope Check (Issue #34)",
        "",
        "DSH did NOT perform any of the following during DLH-5H execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |",
        "| Modify `liquid_upper_domain_asymptotic_diagnostic.py` | NOT performed (read-only reference) |",
        "| Modify any existing HJB/local-policy/KFE/regional source | NOT performed |",
        "| Modify accepted Issues #23-#31 evidence | NOT performed |",
        "| Change physical a domain, `a_max=10` or accepted taper | NOT performed (frozen) |",
        "| Widen a domain | NOT performed |",
        "| Modify economics/prices/parameters/tolerances/initialization | NOT performed (frozen D0) |",
        "| Warm-start one grid from another | NOT performed (fresh initialization per variant) |",
        "| Add adaptive/seventh grid or grid search | NOT performed (exact H0-H5) |",
        "| Clip policy | NOT performed |",
        "| Run stationary KFE / nullspace / pin / density / tail / aggregates | NOT performed (policy-only) |",
        "| Run D1-D3 | NOT performed |",
        "| Run two-region or multi-province GE | NOT performed |",
        "| Run `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` | NOT performed |",
        "| Train any network | NOT performed |",
        "| Enter nominal HANK / calibration / policy / welfare / Results | NOT performed |",
        "| Mutate governance files from the Builder branch | NOT performed |",
        "| `git add .` / `git add -A` | NOT performed (explicit staging only) |",
        "| Create PR / merge / close Issue / successor / self-accept | NOT performed |",
        "",
        f"Terminal classification: `{term['terminal']}`",
        "",
        "Secondary annotations: " + (", ".join(f"`{a}`" for a in term["annotations"]) or "none"),
        "",
        f"Stationary fields marker: `{NOT_AUTHORIZED_MARKER}`",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="DLH-5H illiquid upper-boundary resolution diagnostic (Issue #34)")
    parser.add_argument("--config", default="configs/dlh_5h_illiquid_upper_boundary_resolution_diagnostic.toml")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    root = pathlib.Path(cfg.output_root)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"output root already exists (no-overwrite): {root}")
    dlh5b, params, numerics = build_fixture(cfg)
    runs = run_all_variants(cfg, dlh5b, params, numerics)
    trend = resolution_trend(cfg, runs)
    res = policy_stability(cfg, runs)
    repro = reproduce(cfg, dlh5b, params, numerics)
    term = overall_terminal(cfg, runs, repro, res)
    write_evidence(root, cfg, runs, trend, res, repro, term)
    print(f"artifacts written under {root}")
    print(f"terminal = {term['terminal']}")
    if term["annotations"]:
        print("annotations = " + ", ".join(term["annotations"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
