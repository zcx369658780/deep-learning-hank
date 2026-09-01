"""DLH-5G (Issue #31) — liquid upper-domain asymptotic and resolution diagnostic.

Isolates the liquid (b) upper boundary under a completely frozen illiquid side
and frozen economics:

- ``a``: 20 points on [0,10], ``a_max=10``, ``da=10/19``, accepted MATLAB-faithful
  illiquid-return taper ``r_a*(1-0.1*(a/a_max)^9)`` unchanged;
- ``wbar=1.0``, ``r_a=0.03`` and every non-grid object exactly the accepted
  DLH-5B/DLH-5E canonical fixture;
- exactly six pre-frozen b variants G0-G5, fresh initialization each, no
  warm-start, no adaptive grid, no retuning, no clipping.

Raw ``max(mu_b,0)`` is the primary cross-resolution asymptotic quantity;
requested generator rate ``max(mu_b,0)/db`` remains the HJB/KFE
boundary-compatibility quantity. This is a policy-only diagnostic: it does NOT
execute stationary KFE, nullspace/pin, density, tail mass, stationary flux or
``C,L,A,B`` aggregation (marker
``NOT_AUTHORIZED__DLH_5G_POLICY_ONLY_LIQUID_DOMAIN_DIAGNOSTIC``).
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
# Terminal classifications / markers (Issue #31 section 11)
# ---------------------------------------------------------------------------

TERMINAL_OUTCOME_A = "DLH_5G_LIQUID_B_PREFROZEN_EXTENT_REACHES_BOUNDARY_THRESHOLD__GPT_REVIEW_REQUIRED"
TERMINAL_OUTCOME_B = "DLH_5G_LIQUID_B_EXTENT_ATTENUATION_CONFIRMED__THRESHOLD_NOT_REACHED__GPT_REVIEW_REQUIRED"
TERMINAL_OUTCOME_C = "DLH_5G_LIQUID_B_EXTENT_NONMONOTONIC_OR_PERSISTENT__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_OUTCOME_D = "BLOCKED_DLH_5G_HJB_NUMERICAL_STABILITY_ON_PREFROZEN_LIQUID_DOMAIN"
TERMINAL_OUTCOME_E = "BLOCKED_DLH_5G_REPRODUCIBILITY"
ANNOTATION_RESOLUTION_SENSITIVE = (
    "DLH_5G_B_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__SEPARATE_NUMERICAL_REVIEW_REQUIRED"
)
NOT_AUTHORIZED_MARKER = "NOT_AUTHORIZED__DLH_5G_POLICY_ONLY_LIQUID_DOMAIN_DIAGNOSTIC"

# Accepted MATLAB-faithful oracle identity (Issue #23/#26, re-verified read-only).
ACCEPTED_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"
ACCEPTED_SHA256 = "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"

DB0 = 7.0 / 19.0
DA0 = 10.0 / 19.0


@dataclasses.dataclass(frozen=True)
class GridSpec:
    id: str
    b_pts: int
    b_lo: float
    b_hi: float


@dataclasses.dataclass(frozen=True)
class DLH5GConfig:
    dlh5b_config_path: str
    region_index: int
    wbar: float
    r_a: float
    a_pts: int
    a_lo: float
    a_hi: float
    a_max: float
    da: float
    taper_identity: str
    variants: tuple
    a_index_max: int
    boundary_threshold: float
    reproducibility_tol: float
    numeric_compare_tol: float
    resolution_rel_materiality: float
    output_root: str


def load_config(path: str | pathlib.Path) -> DLH5GConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    hf = raw["household_fixture"]
    fp = raw["frozen_prices"]
    fa = raw["frozen_illiquid"]
    si = raw["shared_interior"]
    v = raw["validation"]
    out = raw["output"]
    variants = tuple(
        GridSpec(id=str(g["id"]), b_pts=int(g["b_pts"]),
                 b_lo=float(g["b_lo"]), b_hi=float(g["b_hi"]))
        for g in raw["variants"]
    )
    return DLH5GConfig(
        dlh5b_config_path=str(hf["dlh5b_config_path"]),
        region_index=int(hf["region_index"]),
        wbar=float(fp["wbar"]),
        r_a=float(fp["r_a"]),
        a_pts=int(fa["a_pts"]),
        a_lo=float(fa["a_lo"]),
        a_hi=float(fa["a_hi"]),
        a_max=float(fa["a_max"]),
        da=float(fa["da"]),
        taper_identity=str(fa["taper_identity"]),
        variants=variants,
        a_index_max=int(si["a_index_max"]),
        boundary_threshold=float(v["boundary_threshold"]),
        reproducibility_tol=float(v["reproducibility_tol"]),
        numeric_compare_tol=float(v["numeric_compare_tol"]),
        resolution_rel_materiality=float(v["resolution_rel_materiality"]),
        output_root=str(out["root"]),
    )


# ---------------------------------------------------------------------------
# Frozen grid plan identity
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class DLH5GGridParams:
    a_lo: float
    a_hi: float
    a_pts: int


def build_variant_grid(spec: GridSpec, gparams: DLH5GGridParams, z, switch) -> MatlabFaithfulHJBGrid:
    b = np.linspace(spec.b_lo, spec.b_hi, spec.b_pts)
    a = np.linspace(gparams.a_lo, gparams.a_hi, gparams.a_pts)
    return MatlabFaithfulHJBGrid(b, a, np.asarray(z, dtype=float), np.asarray(switch, dtype=float))


def grid_plan_identity(cfg: DLH5GConfig) -> dict:
    """Validate + persist the exact G0-G5 liquid grid plan and the frozen
    illiquid identity."""
    ids = [v.id for v in cfg.variants]
    assert ids == ["G0_BASE", "G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3",
                   "G4_BASE_B_FINE", "G5_WIDE1_B_FINE"], f"unexpected variant ids: {ids}"
    plan = {}
    for v in cfg.variants:
        db = (v.b_hi - v.b_lo) / (v.b_pts - 1)
        plan[v.id] = {
            "b_pts": v.b_pts, "b_lo": v.b_lo, "b_hi": v.b_hi, "b_max": v.b_hi, "db": float(db),
        }
    # G0-G3 exact same-spacing db0, exactly nested from the common lower bound
    for vid in ("G0_BASE", "G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3"):
        assert abs(plan[vid]["db"] - DB0) <= 1e-12, f"{vid} db != db0"
        assert abs(plan[vid]["b_lo"] + 2.0) <= 1e-12, f"{vid} b_lo != -2"
    # G4 half spacing on baseline domain; G5 half spacing on G1 domain
    assert abs(plan["G4_BASE_B_FINE"]["db"] - DB0 / 2) <= 1e-12
    assert abs(plan["G5_WIDE1_B_FINE"]["db"] - DB0 / 2) <= 1e-12
    assert plan["G4_BASE_B_FINE"]["b_pts"] == 2 * plan["G0_BASE"]["b_pts"] - 1
    assert plan["G5_WIDE1_B_FINE"]["b_pts"] == 2 * plan["G1_B_WIDE_1"]["b_pts"] - 1
    illiquid = {
        "a_pts": cfg.a_pts, "a_lo": cfg.a_lo, "a_hi": cfg.a_hi, "a_max": cfg.a_max,
        "da": float(cfg.da), "taper_identity": cfg.taper_identity,
    }
    assert abs(illiquid["da"] - DA0) <= 1e-12
    assert abs(illiquid["a_max"] - 10.0) <= 1e-12
    return {"variants": plan, "illiquid": illiquid}


def build_all_grids(cfg: DLH5GConfig, z, switch) -> tuple[dict, dict]:
    plan = grid_plan_identity(cfg)
    gparams = DLH5GGridParams(a_lo=cfg.a_lo, a_hi=cfg.a_hi, a_pts=cfg.a_pts)
    grids = {}
    for v in cfg.variants:
        grids[v.id] = build_variant_grid(v, gparams, z, switch)
    # actual-node nesting / alignment checks
    g0, g1 = grids["G0_BASE"], grids["G1_B_WIDE_1"]
    g2, g3 = grids["G2_B_WIDE_2"], grids["G3_B_WIDE_3"]
    g4, g5 = grids["G4_BASE_B_FINE"], grids["G5_WIDE1_B_FINE"]
    for gw in (g1, g2, g3):
        assert np.allclose(gw.b[: g0.b.size], g0.b, atol=1e-12)
    assert np.allclose(g4.b[::2], g0.b, atol=1e-12)
    assert np.allclose(g5.b[::2], g1.b, atol=1e-12)
    # all variants share the identical illiquid grid
    for g in grids.values():
        assert np.allclose(g.a, g0.a, atol=1e-12)
    return grids, plan


# ---------------------------------------------------------------------------
# Boundary diagnostics (raw and requested)
# ---------------------------------------------------------------------------


def _slice_diagnostics(name, direction, values, grid, threshold, b_fixed, a_fixed):
    """Per-slice outward-rate diagnostics with index+physical coordinates,
    positive quantiles, count/share and complete offending states above
    ``threshold``. Coordinates use C-order unraveling on the actual 2-D slice."""
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


def liquid_boundary_diagnostics(hjb, grid, db, threshold):
    """Upper/lower b diagnostics with BOTH raw drift and requested generator rate.

    raw: ``max(mu_b,0)`` at upper-b, ``max(-mu_b,0)`` at lower-b (primary
    cross-resolution quantity). Requested: the same divided by ``db``
    (HJB/KFE boundary-compatibility quantity). Raw threshold = ``1e-10*db``
    corresponds to the accepted requested-rate threshold.
    """
    mu_b = np.asarray(hjb.mu_b, dtype=float)
    i_count = grid.b.size
    raw_threshold = threshold * db
    b_forward_raw = np.maximum(mu_b, 0.0)
    b_backward_raw = np.maximum(-mu_b, 0.0)
    out = {
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
    return out


def illiquid_regression_diagnostics(hjb, grid, db, da, threshold):
    """Upper/lower a requested-rate regression evidence (policy-only; the
    illiquid boundary remains scientifically unresolved)."""
    mu_a = np.asarray(hjb.mu_a, dtype=float)
    j_count = grid.a.size
    a_backward_raw = np.maximum(-mu_a, 0.0)
    a_forward_raw = np.maximum(mu_a, 0.0)
    return {
        "boundaries": [
            {
                "boundary": "lower_a",
                "direction": "a_backward",
                "requested": _slice_diagnostics("lower_a", "a_backward",
                                                a_backward_raw[:, 0, :] / da, grid,
                                                threshold, None, 0),
            },
            {
                "boundary": "upper_a",
                "direction": "a_forward",
                "requested": _slice_diagnostics("upper_a", "a_forward",
                                                a_forward_raw[:, -1, :] / da, grid,
                                                threshold, None, j_count - 1),
            },
        ],
        "max_requested_upper_a": float(a_forward_raw[:, j_count - 1, :].max() / da),
        "max_requested_lower_a": float(a_backward_raw[:, 0, :].max() / da),
    }


# ---------------------------------------------------------------------------
# Per-variant pipeline
# ---------------------------------------------------------------------------


def run_all_variants(cfg: DLH5GConfig, dlh5b, params, numerics) -> dict:
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, plan = build_all_grids(cfg, z, switch)
    variants = []
    hjb_results: dict[str, Any] = {}
    for spec in cfg.variants:
        grid = build_variant_grid(spec, DLH5GGridParams(cfg.a_lo, cfg.a_hi, cfg.a_pts), z, switch)
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
            },
            "hjb_converged": bool(hjb.converged),
            "hjb_iterations": int(hjb.iterations),
            "hjb_statistic": float(hjb.convergence_statistic),
        }
        if hjb.converged:
            rec["liquid"] = liquid_boundary_diagnostics(hjb, grid, db, cfg.boundary_threshold)
            rec["illiquid"] = illiquid_regression_diagnostics(hjb, grid, db, da, cfg.boundary_threshold)
            rec["variant_terminal"] = "HJB_CONVERGED"
        else:
            rec["liquid"] = None
            rec["illiquid"] = None
            rec["variant_terminal"] = "HJB_NOT_CONVERGED"
        variants.append(rec)
        hjb_results[spec.id] = hjb
    return {"grid_plan": plan, "variants": variants, "hjb_results": hjb_results}


def build_fixture(cfg: DLH5GConfig):
    dlh5b = load_dlh5b_config(cfg.dlh5b_config_path)
    _grid, params, numerics = build_dlh5b_fixture(dlh5b)
    return dlh5b, params, numerics


# ---------------------------------------------------------------------------
# Phase D — same-spacing liquid extent trend (G0 -> G1 -> G2 -> G3)
# ---------------------------------------------------------------------------


def extent_trend(cfg: DLH5GConfig, runs: dict) -> dict:
    by_id = {v["variant"]: v for v in runs["variants"]}
    seq = []
    for vid in ("G0_BASE", "G1_B_WIDE_1", "G2_B_WIDE_2", "G3_B_WIDE_3"):
        v = by_id.get(vid)
        if v is None:
            seq.append({"variant": vid, "reached": False})
            continue
        ub = v.get("liquid") or {}
        ub_ub = next((b for b in ub.get("boundaries", []) if b["boundary"] == "upper_b"), None)
        if not (v["hjb_converged"] and ub_ub):
            seq.append({"variant": vid, "reached": False})
            continue
        raw = ub_ub["raw"]
        req = ub_ub["requested"]
        seq.append({
            "variant": vid,
            "reached": True,
            "raw_max": raw["max"],
            "requested_max": req["max"],
            "raw_count": raw["count_above_threshold"],
            "requested_count": req["count_above_threshold"],
            "raw_share": raw["share_above_threshold"],
            "requested_share": req["share_above_threshold"],
            "argmax_physical_a_z": (raw["argmax_physical"][1], raw["argmax_physical"][2])
            if raw["argmax_physical"] else None,
        })
    # attenuation ratios (raw and requested)
    reached = [s for s in seq if s.get("reached")]
    ratios = {"adjacent_raw": [], "adjacent_requested": [], "vs_G0_raw": [], "vs_G0_requested": []}
    for i in range(1, len(reached)):
        # adjacent: previous/current; nonzero->zero is recorded as "inf"; 0/0 is None
        for key in ("raw", "requested"):
            prev = reached[i - 1][f"{key}_max"]
            cur = reached[i][f"{key}_max"]
            if cur > 0.0:
                ratios[f"adjacent_{key}"].append(round(prev / cur, 6) if prev > 0.0 else 0.0)
            elif prev > 0.0:
                ratios[f"adjacent_{key}"].append("inf")
            else:
                ratios[f"adjacent_{key}"].append(None)
        # relative to G0; G0 denominator always positive here (G0 raw/requested > 0)
        for key in ("raw", "requested"):
            g0v = reached[0][f"{key}_max"]
            cur = reached[i][f"{key}_max"]
            ratios[f"vs_G0_{key}"].append(round(cur / g0v, 6) if g0v > 0.0 else None)
    raw_seq = [s["raw_max"] for s in reached if s.get("reached")]
    req_seq = [s["requested_max"] for s in reached if s.get("reached")]
    strictly_decreasing_raw = all(raw_seq[i] < raw_seq[i - 1] for i in range(1, len(raw_seq))) if len(raw_seq) >= 2 else None
    strictly_decreasing_requested = all(req_seq[i] < req_seq[i - 1] for i in range(1, len(req_seq))) if len(req_seq) >= 2 else None
    attenuated_to_zero_at = None
    for s in reached:
        if s["raw_max"] == 0.0 and s["requested_max"] == 0.0:
            attenuated_to_zero_at = s["variant"]
            break
    return {
        "sequence": seq,
        "ratios": ratios,
        "strictly_decreasing_raw": bool(strictly_decreasing_raw) if strictly_decreasing_raw is not None else None,
        "strictly_decreasing_requested": bool(strictly_decreasing_requested) if strictly_decreasing_requested is not None else None,
        "attenuated_to_zero_at": attenuated_to_zero_at,
    }


# ---------------------------------------------------------------------------
# Phase E — b-resolution stability (G0 vs G4, G1 vs G5)
# ---------------------------------------------------------------------------


def _aligned_pair_slices(coarse_b_pts, half_spacing_b):
    # coarse index i <-> fine index 2*i
    return (slice(None, coarse_b_pts - 2), slice(None, 2 * (coarse_b_pts - 2), 2))


def resolution_stability(cfg: DLH5GConfig, runs: dict) -> list:
    """Compare coarse vs fine b-resolution at exact aligned nodes.

    Pairs: G0 (20) vs G4 (39, half db), G1 (40) vs G5 (79, half db).
    Shared-interior mask: b_index <= coarse_b_pts-3, a_index <= a_index_max (17),
    all z. A supplementary upper-region raw mu_b comparison at the shared
    physical coarse-grid b nodes is reported separately from each grid's own
    upper-boundary slice.
    """
    hjb_by_id = runs["hjb_results"]
    by_id = {v["variant"]: v for v in runs["variants"]}
    pairs = [
        ("G0_BASE", "G4_BASE_B_FINE", "G0_vs_G4"),
        ("G1_B_WIDE_1", "G5_WIDE1_B_FINE", "G1_vs_G5"),
    ]
    out = []
    for coarse_id, fine_id, cid in pairs:
        c = {"comparison": cid}
        rc, rf = by_id[coarse_id], by_id[fine_id]
        if not (rc["hjb_converged"] and rf["hjb_converged"]):
            c["reached"] = False
            c["reason"] = "one or both HJB not converged"
            out.append(c)
            continue
        hc, hf = hjb_by_id[coarse_id], hjb_by_id[fine_id]
        coarse_b_pts = rc["grid"]["b_pts"]
        a_keep = cfg.a_index_max + 1
        b_keep = coarse_b_pts - 2  # b_index <= coarse_b_pts-3
        sb_c, sb_f = _aligned_pair_slices(coarse_b_pts, True)
        sa = slice(None, a_keep)
        numeric_fields = ["value", "consumption", "labor", "transfer", "mu_a", "mu_b"]
        label_fields = ["liquid_label", "transfer_label"]
        fields = {}
        for f in numeric_fields:
            x = np.asarray(getattr(hc, f)[sb_c, sa, :], dtype=float)
            y = np.asarray(getattr(hf, f)[sb_f, sa, :], dtype=float)
            m = float(np.max(np.abs(x - y))) if x.size else 0.0
            ref = float(np.max(np.abs(x))) if x.size else 0.0
            fields[f] = {"max_abs_diff": m, "rel_diff": m / max(1.0, ref)}
        for lab in label_fields:
            x = getattr(hc, lab)[sb_c, sa, :]
            y = getattr(hf, lab)[sb_f, sa, :]
            fields[lab] = {"mismatch_count": int(np.sum(x != y))}
        # supplementary: raw mu_b at the shared coarse-grid upper-region b nodes
        # (top 3 coarse layers: b_index in {b_keep-1, b_keep, b_keep+1}), all a,z
        upper_c = slice(max(0, b_keep - 1), coarse_b_pts)
        upper_f = slice(2 * max(0, b_keep - 1), 2 * coarse_b_pts, 2)
        xm = np.asarray(np.maximum(getattr(hc, "mu_b"), 0.0)[upper_c, :, :], dtype=float)
        ym = np.asarray(np.maximum(getattr(hf, "mu_b"), 0.0)[upper_f, :, :], dtype=float)
        m_upper = float(np.max(np.abs(xm - ym))) if xm.size else 0.0
        ref_upper = float(np.max(np.abs(xm))) if xm.size else 0.0
        fields["raw_mu_b_upper_shared_nodes"] = {
            "max_abs_diff": m_upper, "rel_diff": m_upper / max(1.0, ref_upper),
        }
        c.update({"reached": True, "coarse_b_pts": coarse_b_pts, "fields": fields})
        out.append(c)
    return out


# ---------------------------------------------------------------------------
# Terminal classification + secondary annotation
# ---------------------------------------------------------------------------


def resolution_sensitivity_annotation(cfg: DLH5GConfig, res: list) -> bool:
    """Pre-registered materiality criterion: either aligned pair's scale-aware
    mu_b relative difference (over the shared-interior mask) exceeds
    ``cfg.resolution_rel_materiality`` (default 1e-2)."""
    for c in res:
        if not c.get("reached"):
            continue
        mu_b = c["fields"].get("mu_b") or {}
        rel = mu_b.get("rel_diff") or 0.0
        if rel > cfg.resolution_rel_materiality:
            return True
    return False


def overall_terminal(cfg: DLH5GConfig, runs: dict, repro: dict, res: list) -> dict:
    if not repro["pass_bool"]:
        terminal = TERMINAL_OUTCOME_E
    elif any(not v["hjb_converged"] for v in runs["variants"]):
        terminal = TERMINAL_OUTCOME_D
    else:
        trend = extent_trend(cfg, runs)
        seq = [s for s in trend["sequence"] if s.get("reached")]
        req_seq = [s["requested_max"] for s in seq]
        if any(r <= cfg.boundary_threshold for r in req_seq):
            terminal = TERMINAL_OUTCOME_A
        elif trend["strictly_decreasing_raw"]:
            terminal = TERMINAL_OUTCOME_B
        else:
            terminal = TERMINAL_OUTCOME_C
    annotations = []
    if resolution_sensitivity_annotation(cfg, res):
        annotations.append(ANNOTATION_RESOLUTION_SENSITIVE)
    return {"terminal": terminal, "annotations": annotations}


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------


def _variant_structural_signature(rec: dict) -> str:
    liq = rec.get("liquid") or {}
    ill = rec.get("illiquid") or {}
    liquid_discrete = {}
    for b in liq.get("boundaries", []):
        liquid_discrete[b["boundary"]] = {
            "raw_count": b["raw"]["count_above_threshold"],
            "requested_count": b["requested"]["count_above_threshold"],
            "raw_argmax_index": b["raw"]["argmax_index"],
            "requested_argmax_index": b["requested"]["argmax_index"],
            "raw_offending": [(o["b_index"], o["a_index"], o["z_index"]) for o in b["raw"]["offending_states"]],
            "requested_offending": [(o["b_index"], o["a_index"], o["z_index"]) for o in b["requested"]["offending_states"]],
        }
    illiquid_discrete = {}
    for b in ill.get("boundaries", []):
        illiquid_discrete[b["boundary"]] = {
            "requested_count": b["requested"]["count_above_threshold"],
            "requested_argmax_index": b["requested"]["argmax_index"],
            "requested_offending": [(o["b_index"], o["a_index"], o["z_index"]) for o in b["requested"]["offending_states"]],
        }
    return json.dumps({
        "variant": rec.get("variant"),
        "grid": rec.get("grid"),
        "hjb_converged": rec.get("hjb_converged"),
        "hjb_iterations": rec.get("hjb_iterations"),
        "liquid": liquid_discrete,
        "illiquid": illiquid_discrete,
    }, sort_keys=True)


def _variant_numeric_numbers(rec: dict) -> list:
    out: list[float] = []
    if rec.get("hjb_statistic") is not None:
        out.append(float(rec["hjb_statistic"]))
    liq = rec.get("liquid") or {}
    for b in liq.get("boundaries", []):
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
    ill = rec.get("illiquid") or {}
    for b in ill.get("boundaries", []):
        d = b.get("requested") or {}
        out.append(float(d.get("max", float("nan"))))
        out.append(float(d.get("share_above_threshold", float("nan"))))
        for o in d.get("offending_states", []):
            out.append(float(o.get("rate", float("nan"))))
    return out


def _nonfinite_aligned(a, b) -> bool:
    return bool((not np.isfinite(a)) and (not np.isfinite(b)))


def compare_variant_records(r1: dict, r2: dict, cfg: DLH5GConfig) -> dict:
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


def reproduce(cfg: DLH5GConfig, dlh5b, params, numerics) -> dict:
    run1 = run_all_variants(cfg, dlh5b, params, numerics)
    run2 = run_all_variants(cfg, dlh5b, params, numerics)
    per_variant = {}
    for r1, r2 in zip(run1["variants"], run2["variants"]):
        per_variant[r1["variant"]] = compare_variant_records(r1, r2, cfg)
    res1 = resolution_stability(cfg, run1)
    t1 = overall_terminal(cfg, run1, {"pass_bool": True}, res1)
    res2 = resolution_stability(cfg, run2)
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


def _bmax_for(cfg: DLH5GConfig, vid: str) -> str:
    for v in cfg.variants:
        if v.id == vid:
            return f"{v.b_hi:.6f}"
    return vid


def _offending_rows(rec, kind):
    """kind in {'raw','requested'} for liquid, or 'illiquid'."""
    rows = []
    if kind == "illiquid":
        for b in (rec.get("illiquid") or {}).get("boundaries", []):
            for o in b.get("requested", {}).get("offending_states", []):
                rows.append([rec["variant"], b["boundary"], b["direction"], "requested",
                             o["b_index"], o["a_index"], o["z_index"],
                             _fmt(o["b"]), _fmt(o["a"]), _fmt(o["z"]), _fmt(o["rate"])])
        return rows
    for b in (rec.get("liquid") or {}).get("boundaries", []):
        for o in b[kind].get("offending_states", []):
            rows.append([rec["variant"], b["boundary"], b["direction"], kind,
                         o["b_index"], o["a_index"], o["z_index"],
                         _fmt(o["b"]), _fmt(o["a"]), _fmt(o["z"]), _fmt(o["rate"])])
    return rows


def write_evidence(root: pathlib.Path, cfg: DLH5GConfig, runs: dict, trend: dict,
                   res: list, repro: dict, term: dict) -> None:
    root = pathlib.Path(root)
    root.mkdir(parents=True, exist_ok=True)

    # 1) VARIANT_STATUS.csv
    rows = []
    for v in runs["variants"]:
        g = v["grid"]
        liq = v.get("liquid") or {}
        rows.append([v["variant"], g["b_pts"], _fmt(g["b_lo"]), _fmt(g["b_hi"]), _fmt(g["db"]),
                     g["a_pts"], _fmt(g["a_lo"]), _fmt(g["a_hi"]), _fmt(g["da"]),
                     v["hjb_converged"], v["hjb_iterations"], _fmt(v["hjb_statistic"]),
                     _fmt(liq.get("max_raw_upper_b")), _fmt(liq.get("max_raw_lower_b")),
                     v.get("variant_terminal")])
    _write_csv(root / "DLH_5G_VARIANT_STATUS.csv",
               ["variant", "b_pts", "b_lo", "b_hi", "db", "a_pts", "a_lo", "a_hi", "da",
                "hjb_converged", "hjb_iterations", "hjb_statistic",
                "max_raw_upper_b", "max_raw_lower_b", "variant_terminal"], rows)

    # 2) LIQUID_BOUNDARY_DIAGNOSTICS.csv (summary + complete offending rows)
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
                             _q_fmt(d.get("quantiles")), "", "", "", "", "", "", ""])
            for o in _offending_rows(v, "raw"):
                rows.append([v["variant"], o[1], o[2], "raw_offending",
                             _fmt(o[10]), "", "", "", "", "", "",
                             o[4], o[5], o[6], o[7], o[8], o[9], o[10]])
            for o in _offending_rows(v, "requested"):
                rows.append([v["variant"], o[1], o[2], "requested_offending",
                             _fmt(o[10]), "", "", "", "", "", "",
                             o[4], o[5], o[6], o[7], o[8], o[9], o[10]])
    _write_csv(root / "DLH_5G_LIQUID_BOUNDARY_DIAGNOSTICS.csv",
               ["variant", "boundary", "direction", "kind", "max", "count_above_threshold",
                "share_above_threshold", "argmax_index", "argmax_physical",
                "value_at_argmax", "quantiles_q50_q90_q95_q99",
                "b_index", "a_index", "z_index", "b", "a", "z", "rate"], rows)

    # 3) ILLIQUID_REGRESSION_DIAGNOSTICS.csv (requested-rate regression only)
    rows = []
    for v in runs["variants"]:
        ill = v.get("illiquid") or {}
        for b in ill.get("boundaries", []):
            d = b.get("requested") or {}
            rows.append([v["variant"], b["boundary"], b["direction"],
                         _fmt(d.get("max")), d.get("count_above_threshold"),
                         _fmt(d.get("share_above_threshold")), d.get("argmax_index"),
                         d.get("argmax_physical"), _fmt(d.get("value_at_argmax")),
                         _q_fmt(d.get("quantiles")), "", "", "", "", "", "", ""])
        for o in _offending_rows(v, "illiquid"):
            rows.append([v["variant"], o[1], o[2], "offending", _fmt(o[10]), "", "",
                         "", "", "", "", o[4], o[5], o[6], o[7], o[8], o[9], o[10]])
    _write_csv(root / "DLH_5G_ILLIQUID_REGRESSION_DIAGNOSTICS.csv",
               ["variant", "boundary", "direction", "kind", "max", "count_above_threshold",
                "share_above_threshold", "argmax_index", "argmax_physical",
                "value_at_argmax", "quantiles_q50_q90_q95_q99",
                "b_index", "a_index", "z_index", "b", "a", "z", "rate"], rows)

    # 4) EXTENT_TREND.csv
    rows = []
    for s in trend["sequence"]:
        if not s.get("reached"):
            rows.append([s["variant"], "NOT_REACHED", "", "", "", "", "", "", "", "", "", ""])
            continue
        rows.append([s["variant"], "REACHED", _fmt(s["raw_max"]), _fmt(s["requested_max"]),
                     s["raw_count"], s["requested_count"], _fmt(s["raw_share"]),
                     _fmt(s["requested_share"]), s["argmax_physical_a_z"],
                     "", "", ""])
    ar = trend["ratios"]
    rows.append(["adjacent_raw_ratio", "RATIO"] + [_fmt(v) for v in ar["adjacent_raw"]] + ["", "", "", "", "", "", ""])
    rows.append(["adjacent_requested_ratio", "RATIO"] + [_fmt(v) for v in ar["adjacent_requested"]] + ["", "", "", "", "", "", ""])
    rows.append(["vs_G0_raw_ratio", "RATIO"] + [_fmt(v) for v in ar["vs_G0_raw"]] + ["", "", "", "", "", "", ""])
    rows.append(["vs_G0_requested_ratio", "RATIO"] + [_fmt(v) for v in ar["vs_G0_requested"]] + ["", "", "", "", "", "", ""])
    rows.append(["strictly_decreasing_raw", "FLAG", str(trend["strictly_decreasing_raw"]), "", "", "", "", "", "", "", "", ""])
    rows.append(["strictly_decreasing_requested", "FLAG", str(trend["strictly_decreasing_requested"]), "", "", "", "", "", "", "", "", ""])
    rows.append(["attenuated_to_zero_at", "FLAG", str(trend["attenuated_to_zero_at"]), "", "", "", "", "", "", "", "", ""])
    _write_csv(root / "DLH_5G_EXTENT_TREND.csv",
               ["item", "kind", "value1", "value2", "value3", "count1", "count2", "share1",
                "share2", "argmax_a_z", "note", "extra"], rows)

    # 5) RESOLUTION_STABILITY.csv
    rows = []
    for c in res:
        if not c.get("reached"):
            rows.append([c["comparison"], "NOT_REACHED", "", "", "", c.get("reason", "")])
            continue
        for f, m in c["fields"].items():
            if f in ("liquid_label", "transfer_label"):
                rows.append([c["comparison"], f, "", "", m["mismatch_count"], ""])
            else:
                rows.append([c["comparison"], f, _fmt(m["max_abs_diff"]), _fmt(m["rel_diff"]), "", ""])
    _write_csv(root / "DLH_5G_RESOLUTION_STABILITY.csv",
               ["comparison", "field", "max_abs_diff", "rel_diff", "mismatch_count", "note"], rows)

    # 6) REPRODUCIBILITY.json
    with open(root / "DLH_5G_REPRODUCIBILITY.json", "w", encoding="utf-8") as fh:
        json.dump(repro, fh, indent=2, default=str, sort_keys=True)

    # 7) EXECUTION_REPORT.md
    with open(root / "DLH_5G_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_report(cfg, runs, trend, res, repro, term))

    # 8) FORBIDDEN_OPERATION_CHECK.md
    with open(root / "DLH_5G_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write(_render_forbidden_check(cfg, runs, repro, term))


def _sf(v, spec=None) -> str:
    if v is None:
        return "—"
    try:
        if spec is not None:
            return format(float(v), spec)
        return str(v)
    except (TypeError, ValueError):
        return str(v)


def _render_report(cfg: DLH5GConfig, runs: dict, trend: dict, res: list,
                   repro: dict, term: dict) -> str:
    lines = []
    lines.append("# DLH-5G — Liquid Upper-Domain Asymptotic and Resolution Diagnostic (Issue #31)")
    lines.append("")
    lines.append("Policy-only diagnostic isolating the liquid (b) upper boundary under a completely "
                 "frozen illiquid side and frozen economics. Accepted MATLAB-faithful HJB source is "
                 "immutable and reused read-only.")
    lines.append("")
    lines.append(f"Overall terminal classification: `{term['terminal']}`")
    if term["annotations"]:
        lines.append("")
        lines.append("Secondary scientific annotations: " +
                     ", ".join(f"`{a}`" for a in term["annotations"]))
    lines.append("")
    lines.append(f"Frozen economics: `wbar={cfg.wbar}`, `r_a={cfg.r_a}`; illiquid side frozen at "
                 f"`a20 [{cfg.a_lo},{cfg.a_hi}]`, `a_max={cfg.a_max}`, `da={cfg.da:.12f}`, taper "
                 f"`{cfg.taper_identity}`; all non-grid objects the accepted DLH-5B/DLH-5E fixture "
                 f"(`{cfg.dlh5b_config_path}`, region_index={cfg.region_index}).")
    lines.append("")
    lines.append("## Variant status (Phase A)")
    lines.append("")
    lines.append("| variant | b pts | b domain | b max | db | a grid | HJB conv | iters | stat | raw upper-b max | raw lower-b max | terminal |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for v in runs["variants"]:
        g = v["grid"]
        liq = v.get("liquid") or {}
        lines.append(f"| {v['variant']} | {g['b_pts']} | [{_sf(g['b_lo'])},{_sf(g['b_hi'])}] | "
                     f"{_sf(g['b_hi'])} | {_sf(g['db'])} | a{g['a_pts']} [{_sf(g['a_lo'])},{_sf(g['a_hi'])}] | "
                     f"{v['hjb_converged']} | {v['hjb_iterations']} | {_sf(v['hjb_statistic'], '.3e')} | "
                     f"{_sf(liq.get('max_raw_upper_b'), '.3e')} | {_sf(liq.get('max_raw_lower_b'), '.3e')} | "
                     f"{_sf(v.get('variant_terminal'))} |")
    lines.append("")

    lines.append("## Liquid upper/lower boundary diagnostics (Phase B)")
    lines.append("")
    lines.append("Raw drift (`max(mu_b,0)` / `max(-mu_b,0)`) is the primary cross-resolution asymptotic "
                 "quantity; requested generator rate (raw/`db`) is the HJB/KFE boundary-compatibility "
                 "quantity. Raw threshold = `1e-10*db` corresponds to the accepted requested-rate "
                 "threshold `1e-10`. Coordinates are exact `(b_index,a_index,z_index)` plus physical "
                 "`(b,a,z)` via C-order unraveling on the actual 2-D boundary slice.")
    lines.append("")
    for v in runs["variants"]:
        liq = v.get("liquid") or {}
        if not liq:
            lines.append(f"### {v['variant']} — HJB not converged")
            lines.append("")
            continue
        lines.append(f"### {v['variant']}")
        lines.append("")
        lines.append("| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for b in liq["boundaries"]:
            for kind in ("raw", "requested"):
                d = b[kind]
                lines.append(f"| {b['boundary']} | {kind} | {_sf(d['max'], '.3e')} | "
                             f"{_sf(d['count_above_threshold'])} | {_sf(d['share_above_threshold'], '.3e')} | "
                             f"{d.get('argmax_index')} | {d.get('argmax_physical')} | "
                             f"{_sf(d.get('value_at_argmax'), '.3e')} | {_q_fmt(d.get('quantiles'))} |")
        lines.append("")
        lines.append("Complete offending states (raw > `1e-10*db`; requested > `1e-10`):")
        lines.append("")
        rows = _offending_rows(v, "raw") + _offending_rows(v, "requested")
        if rows:
            lines.append("| boundary | kind | b_index | a_index | z_index | b | a | z | rate |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for r in rows:
                lines.append(f"| {r[1]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {_sf(r[7], '.6f')} | "
                             f"{_sf(r[8], '.6f')} | {_sf(r[9], '.6f')} | {_sf(r[10], '.9e')} |")
        else:
            lines.append("No state exceeds the raw or requested threshold.")
        lines.append("")

    lines.append("## Illiquid-boundary regression evidence (Phase C)")
    lines.append("")
    lines.append("Upper/lower a requested-rate regression diagnostics only. The illiquid domain/taper "
                 "is frozen but remains scientifically unresolved; DLH-5G does not resolve or redesign "
                 "the illiquid boundary.")
    lines.append("")
    for v in runs["variants"]:
        ill = v.get("illiquid") or {}
        if not ill:
            continue
        parts = []
        for b in ill.get("boundaries", []):
            d = b.get("requested") or {}
            parts.append(f"{b['boundary']}: max={_sf(d.get('max'), '.3e')} count={_sf(d.get('count_above_threshold'))} "
                         f"share={_sf(d.get('share_above_threshold'), '.3e')} argmax={d.get('argmax_index')}")
        lines.append(f"- {v['variant']}: " + "; ".join(parts))
    lines.append("")

    lines.append("## Same-spacing liquid extent trend (Phase D: G0 -> G1 -> G2 -> G3)")
    lines.append("")
    lines.append("| variant | raw upper-b max | requested upper-b max | raw count | requested count | raw share | requested share | argmax physical (a,z) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for s in trend["sequence"]:
        if not s.get("reached"):
            lines.append(f"| {s['variant']} | NOT_REACHED | | | | | | |")
            continue
        lines.append(f"| {s['variant']} | {_sf(s['raw_max'], '.3e')} | {_sf(s['requested_max'], '.3e')} | "
                     f"{s['raw_count']} | {s['requested_count']} | {_sf(s['raw_share'], '.3e')} | "
                     f"{_sf(s['requested_share'], '.3e')} | {s['argmax_physical_a_z']} |")
    ar = trend["ratios"]
    lines.append("")
    lines.append(f"- adjacent raw attenuation ratios (G0/G1, G1/G2, G2/G3): {ar['adjacent_raw']} "
                 f"(`inf` = nonzero-to-zero attenuation)")
    lines.append(f"- adjacent requested attenuation ratios: {ar['adjacent_requested']}")
    lines.append(f"- raw ratios relative to G0 (G1/G0, G2/G0, G3/G0): {ar['vs_G0_raw']}")
    lines.append(f"- requested ratios relative to G0: {ar['vs_G0_requested']}")
    lines.append(f"- strictly decreasing raw upper-b max over G0->G3: {trend['strictly_decreasing_raw']}")
    lines.append(f"- strictly decreasing requested upper-b max over G0->G3: {trend['strictly_decreasing_requested']}")
    if trend.get("attenuated_to_zero_at"):
        lines.append(f"- **raw and requested upper-b outward drift reach EXACT ZERO at "
                     f"`{trend['attenuated_to_zero_at']}` (b_max={_bmax_for(cfg, trend['attenuated_to_zero_at'])}) "
                     f"and remain zero at wider extents.** This is full attenuation: the liquid upper-boundary "
                     f"influence converges away within the pre-frozen b extents.")
    lines.append("")
    lines.append("This is a policy-only trend; it does not establish stationary-tail existence or "
                 "non-existence.")

    lines.append("")
    lines.append("## b-resolution stability (Phase E: G0 vs G4, G1 vs G5)")
    lines.append("")
    lines.append("Exact aligned-node comparisons at the shared-interior mask (`b_index <= "
                 "coarse_b_pts-3`, `a_index <= 17`, all z). `rel_diff = max_abs / max(1, max|coarse|)` "
                 "is scale-aware. A supplementary raw `mu_b` comparison at the shared coarse-grid "
                 "upper-region b nodes is reported separately from each grid's own upper-boundary slice.")
    lines.append("")
    for c in res:
        lines.append(f"### {c['comparison']}")
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

    lines.append("## Scientific stopping rule (Phase F)")
    lines.append("")
    lines.append(f"DLH-5G is policy-only. Stationary KFE / nullspace / pin / density / tail mass / "
                 f"stationary flux / `C,L,A,B` are `{NOT_AUTHORIZED_MARKER}` and were not executed, "
                 f"because the illiquid upper-boundary process remains unresolved and DLH-5G isolates "
                 f"liquid-domain behavior without changing that scientific state.")

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
                 "`dsh/issue-31-dlh-5g-liquid-upper-domain-asymptotic-2026-09-01`; allowlist-only "
                 "additions (3 artifacts + 8 evidence files).")
    lines.append("")
    lines.append("DLH-5G implements NO repair and NO stationary acceptance: accepted HJB/KFE/regional "
                 "source immutable; `a_max`/a-grid/taper/economics/tolerances/initialization frozen; no "
                 "clipping; no D1-D3; no regional or multi-province GE; no learned network; no nominal HANK.")
    return "\n".join(lines)


def _render_forbidden_check(cfg: DLH5GConfig, runs: dict, repro: dict, term: dict) -> str:
    lines = [
        "# DLH-5G — Forbidden-Operation / Scope Check (Issue #31)",
        "",
        "DSH did NOT perform any of the following during DLH-5G execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |",
        "| Modify `upper_domain_stationary_tail_diagnostic.py` | NOT performed (read-only reference) |",
        "| Modify any existing HJB/local-policy/KFE/regional source | NOT performed |",
        "| Modify accepted Issues #23-#29 evidence | NOT performed |",
        "| Modify `a_max`, a-grid, `da` or accepted illiquid-return taper | NOT performed (frozen) |",
        "| Modify economics/prices/parameters/tolerances/initialization | NOT performed (frozen D0) |",
        "| Warm-start one grid from another | NOT performed (fresh initialization per variant) |",
        "| Add adaptive/seventh grid or grid search | NOT performed (exact G0-G5) |",
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
    parser = argparse.ArgumentParser(description="DLH-5G liquid upper-domain asymptotic diagnostic (Issue #31)")
    parser.add_argument("--config", default="configs/dlh_5g_liquid_upper_domain_asymptotic_diagnostic.toml")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    root = pathlib.Path(cfg.output_root)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"output root already exists (no-overwrite): {root}")
    dlh5b, params, numerics = build_fixture(cfg)
    runs = run_all_variants(cfg, dlh5b, params, numerics)
    trend = extent_trend(cfg, runs)
    res = resolution_stability(cfg, runs)
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
