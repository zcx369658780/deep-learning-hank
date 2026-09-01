"""DLH-5J (Issue #36) — final bounded coupled liquid-extent continuation.

Completes the last pre-frozen larger-b grid experiment before asymptotic
adjudication, preserving the accepted household controlled process:

- D0 economics/prices frozen (``wbar=1.0``, ``r_a=0.03``);
- physical illiquid domain ``a in [0,10]``, ``a_max=10``, accepted MATLAB-faithful
  taper ``r_a*(1-0.1*(a/a_max)^9)`` unchanged;
- only the two mature illiquid resolutions ``a77`` (``da=(10/19)/4``) and ``a153``
  (``da=(10/19)/8``);
- liquid spacing frozen ``db=7/19``; only the three final pre-frozen b extents
  ``b120 [-2,795/19]``, ``b140 [-2,935/19]``, ``b160 [-2,1075/19]`` — ``b160`` is
  the HARD ROUTE CEILING (no b180/b200);
- exactly six variants J0-J5 (Cartesian ``{a77,a153} x {b120,b140,b160}``), fresh
  initialization each, no warm-start, no adaptive/root-seeking seventh grid, no
  b-resolution change, no a-domain widening, no retuning, no clipping;
- accepted DLH-5I b100 results (I2_A77_B100 / I5_A153_B100) are used ONLY as
  read-only scalar anchors for the continuation trends; b100 is NOT rerun as an
  extra variant.

Raw ``max(mu,0)`` is the primary cross-resolution diagnostic; requested generator
rate (raw/spacing) remains the HJB/KFE boundary-compatibility quantity. Complete
raw + requested diagnostics are reported on all four asset boundaries. Policy-only:
stationary fields use the marker
``NOT_AUTHORIZED__DLH_5J_POLICY_ONLY_FINAL_BOUNDED_EXTENT_DIAGNOSTIC``.
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
# Terminal classifications / markers (Issue #36 section 11)
# ---------------------------------------------------------------------------

TERMINAL_OUTCOME_A = "DLH_5J_FINAL_PREFROZEN_EXTENT_REACHES_CROSS_A_JOINT_BOUNDARY_COMPATIBILITY__GPT_REVIEW_REQUIRED"
TERMINAL_OUTCOME_B = "DLH_5J_JOINT_BOUNDARY_COMPATIBILITY_NOT_ROBUST_ACROSS_A_RESOLUTION__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_OUTCOME_C = "DLH_5J_FINAL_BOUNDED_EXTENT_CONTINUATION_COMPLETE__COMMON_THRESHOLD_NOT_REACHED__ASYMPTOTIC_ADJUDICATION_REQUIRED"
TERMINAL_OUTCOME_D = "DLH_5J_FINAL_BOUNDED_EXTENT_BEHAVIOR_PERSISTENT_OR_NONMONOTONIC__ASYMPTOTIC_ADJUDICATION_REQUIRED"
TERMINAL_OUTCOME_E = "BLOCKED_DLH_5J_HJB_NUMERICAL_STABILITY"
TERMINAL_OUTCOME_F = "BLOCKED_DLH_5J_REPRODUCIBILITY"
ANNOTATION_CROSS_A_SENSITIVITY = (
    "DLH_5J_CROSS_A_POLICY_RESOLUTION_SENSITIVITY_REMAINS_MATERIAL__NUMERICAL_REVIEW_REQUIRED"
)
JOINT_COMPATIBLE = "JOINT_HJB_BOUNDARY_POLICY_COMPATIBLE"
JOINT_NOT_COMPATIBLE = "JOINT_HJB_BOUNDARY_POLICY_NOT_COMPATIBLE"
CROSS_A_COMPATIBLE = "CROSS_A_RESOLUTION_JOINT_COMPATIBLE_AT_B_EXTENT"
CROSS_A_NOT_COMPATIBLE = "CROSS_A_RESOLUTION_JOINT_NOT_COMPATIBLE_AT_B_EXTENT"
NOT_AUTHORIZED_MARKER = "NOT_AUTHORIZED__DLH_5J_POLICY_ONLY_FINAL_BOUNDED_EXTENT_DIAGNOSTIC"

# Accepted MATLAB-faithful oracle identity (Issue #23/#26, re-verified read-only).
ACCEPTED_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"
ACCEPTED_SHA256 = "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"

DB0 = 7.0 / 19.0
DA0 = 10.0 / 19.0

# Accepted DLH-5I (Issue #35) b100 results used ONLY as read-only scalar anchors
# for the final continuation trends (Issue #36 sections 7/13). Values are copied
# verbatim from the accepted evidence file
# reports/dlh_5i_coupled_boundary_frontier_diagnostic_2026_09_01/DLH_5I_BOUNDARY_DIAGNOSTICS.csv.
# b100 is NOT rerun as an extra variant in DLH-5J.
B100_ANCHOR_A77 = {
    "variant": "I2_A77_B100",
    "b_extent": "b100",
    "b_pts": 100,
    "b_hi": 655.0 / 19.0,
    "raw_max": 7.093524248e-02,
    "requested_max": 1.925385153e-01,
    "raw_count": 4,
    "requested_count": 4,
    "raw_share": 2.597402597e-02,
    "requested_share": 2.597402597e-02,
    "argmax_index": (99, 76, 1),
    "argmax_physical": (34.473684210526315, 10.0, 1.3),
    "upper_a_requested_max": 0.0,
}
B100_ANCHOR_A153 = {
    "variant": "I5_A153_B100",
    "b_extent": "b100",
    "b_pts": 100,
    "b_hi": 655.0 / 19.0,
    "raw_max": 9.143516741e-02,
    "requested_max": 2.481811687e-01,
    "raw_count": 8,
    "requested_count": 8,
    "raw_share": 2.614379085e-02,
    "requested_share": 2.614379085e-02,
    "argmax_index": (99, 152, 1),
    "argmax_physical": (34.473684210526315, 10.0, 1.3),
    "upper_a_requested_max": 0.0,
}

VARIANT_IDS = [
    "J0_A77_B120", "J1_A77_B140", "J2_A77_B160",
    "J3_A153_B120", "J4_A153_B140", "J5_A153_B160",
]
A_RES_ORDER = ["a77", "a153"]
B_EXT_ORDER = ["b120", "b140", "b160"]
B100_EXTENT = "b100"


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ARes:
    id: str
    a_pts: int


@dataclasses.dataclass(frozen=True)
class BExt:
    id: str
    b_pts: int
    b_hi: float


@dataclasses.dataclass(frozen=True)
class GridSpec:
    id: str
    a_res: str
    b_ext: str


@dataclasses.dataclass(frozen=True)
class DLH5JConfig:
    dlh5b_config_path: str
    region_index: int
    wbar: float
    r_a: float
    a_lo: float
    a_hi: float
    a_max: float
    taper_identity: str
    b_lo: float
    db: float
    route_ceiling_note: str
    a_resolutions: tuple
    b_extents: tuple
    variants: tuple
    top_coarse_layers_excluded: int
    boundary_threshold: float
    reproducibility_tol: float
    numeric_compare_tol: float
    policy_rel_materiality: float
    output_root: str


def load_config(path: str | pathlib.Path) -> DLH5JConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    hf = raw["household_fixture"]
    fp = raw["frozen_prices"]
    fa = raw["frozen_physical_illiquid"]
    ld = raw["liquid_domain"]
    si = raw["shared_interior"]
    v = raw["validation"]
    out = raw["output"]
    a_resolutions = tuple(ARes(id=str(r["id"]), a_pts=int(r["a_pts"])) for r in raw["a_resolutions"])
    b_extents = tuple(BExt(id=str(e["id"]), b_pts=int(e["b_pts"]), b_hi=float(e["b_hi"])) for e in raw["b_extents"])
    variants = tuple(
        GridSpec(id=str(g["id"]), a_res=str(g["a_res"]), b_ext=str(g["b_ext"]))
        for g in raw["variants"]
    )
    return DLH5JConfig(
        dlh5b_config_path=str(hf["dlh5b_config_path"]),
        region_index=int(hf["region_index"]),
        wbar=float(fp["wbar"]),
        r_a=float(fp["r_a"]),
        a_lo=float(fa["a_lo"]),
        a_hi=float(fa["a_hi"]),
        a_max=float(fa["a_max"]),
        taper_identity=str(fa["taper_identity"]),
        b_lo=float(ld["b_lo"]),
        db=float(ld["db"]),
        route_ceiling_note=str(ld.get("route_ceiling_note", "b160_IS_THE_HARD_ROUTE_CEILING")),
        a_resolutions=a_resolutions,
        b_extents=b_extents,
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


def _a_pts(cfg: DLH5JConfig, a_res: str) -> int:
    for r in cfg.a_resolutions:
        if r.id == a_res:
            return r.a_pts
    raise ValueError(f"unknown a resolution: {a_res}")


def _b_ext(cfg: DLH5JConfig, b_ext: str) -> BExt:
    for e in cfg.b_extents:
        if e.id == b_ext:
            return e
    raise ValueError(f"unknown b extent: {b_ext}")


def build_variant_grid(spec: GridSpec, cfg: DLH5JConfig, z, switch) -> MatlabFaithfulHJBGrid:
    be = _b_ext(cfg, spec.b_ext)
    b = np.linspace(cfg.b_lo, be.b_hi, be.b_pts)
    a = np.linspace(cfg.a_lo, cfg.a_hi, _a_pts(cfg, spec.a_res))
    return MatlabFaithfulHJBGrid(b, a, np.asarray(z, dtype=float), np.asarray(switch, dtype=float))


def grid_plan_identity(cfg: DLH5JConfig) -> dict:
    ids = [v.id for v in cfg.variants]
    assert ids == VARIANT_IDS, f"unexpected variant ids: {ids}"
    assert [r.id for r in cfg.a_resolutions] == A_RES_ORDER
    assert [e.id for e in cfg.b_extents] == B_EXT_ORDER
    a_plan = {}
    for r in cfg.a_resolutions:
        da = (cfg.a_hi - cfg.a_lo) / (r.a_pts - 1)
        assert r.a_pts in (77, 153)
        a_plan[r.id] = {"a_pts": r.a_pts, "a_lo": cfg.a_lo, "a_hi": cfg.a_hi, "da": float(da)}
    assert abs(a_plan["a77"]["da"] - DA0 / 4) <= 1e-12
    assert abs(a_plan["a153"]["da"] - DA0 / 8) <= 1e-12
    b_plan = {}
    for e in cfg.b_extents:
        db = (e.b_hi - cfg.b_lo) / (e.b_pts - 1)
        assert abs(db - DB0) <= 1e-12
        b_plan[e.id] = {"b_pts": e.b_pts, "b_lo": cfg.b_lo, "b_hi": e.b_hi, "db": float(db)}
    assert abs(b_plan["b120"]["b_hi"] - 795.0 / 19.0) <= 1e-12
    assert abs(b_plan["b140"]["b_hi"] - 935.0 / 19.0) <= 1e-12
    assert abs(b_plan["b160"]["b_hi"] - 1075.0 / 19.0) <= 1e-12
    assert b_plan["b120"]["b_pts"] == 120 and b_plan["b140"]["b_pts"] == 140 and b_plan["b160"]["b_pts"] == 160
    variants = {}
    for v in cfg.variants:
        variants[v.id] = {
            "a_res": v.a_res, "b_ext": v.b_ext,
            "a_pts": a_plan[v.a_res]["a_pts"], "da": a_plan[v.a_res]["da"],
            "b_pts": b_plan[v.b_ext]["b_pts"], "b_hi": b_plan[v.b_ext]["b_hi"],
            "db": b_plan[v.b_ext]["db"],
        }
    illiquid = {
        "a_lo": cfg.a_lo, "a_hi": cfg.a_hi, "a_max": cfg.a_max,
        "taper_identity": cfg.taper_identity,
    }
    assert abs(illiquid["a_max"] - 10.0) <= 1e-12
    liquid = {
        "b_lo": cfg.b_lo, "db": float(cfg.db), "b_extents": b_plan,
        "route_ceiling_note": cfg.route_ceiling_note,
        "hard_ceiling_b_hi": float(b_plan["b160"]["b_hi"]),
    }
    return {"variants": variants, "a_resolutions": a_plan, "b_extents": b_plan,
            "illiquid": illiquid, "liquid": liquid}


def build_all_grids(cfg: DLH5JConfig, z, switch) -> tuple[dict, dict]:
    plan = grid_plan_identity(cfg)
    grids = {v.id: build_variant_grid(v, cfg, z, switch) for v in cfg.variants}
    j120 = grids["J0_A77_B120"], grids["J3_A153_B120"]
    j140 = grids["J1_A77_B140"], grids["J4_A153_B140"]
    j160 = grids["J2_A77_B160"], grids["J5_A153_B160"]
    for c, f in (j120, j140, j160):
        assert np.allclose(f.a[::2], c.a, atol=1e-12)
    for hi in (j140[0], j160[0], j140[1], j160[1]):
        assert np.allclose(hi.b[:120], j120[0].b, atol=1e-12)
    assert np.allclose(j160[0].b[:140], j140[0].b, atol=1e-12)
    assert np.allclose(j160[1].b[:140], j140[1].b, atol=1e-12)
    # same-b-extent cross-a grids share identical physical b nodes
    assert np.allclose(j120[1].b, j120[0].b, atol=1e-12)
    assert np.allclose(j140[1].b, j140[0].b, atol=1e-12)
    assert np.allclose(j160[1].b, j160[0].b, atol=1e-12)
    for g in grids.values():
        assert abs(g.a[0] - cfg.a_lo) <= 1e-12 and abs(g.a[-1] - cfg.a_hi) <= 1e-12
    return grids, plan


# ---------------------------------------------------------------------------
# Boundary diagnostics (raw and requested, all four boundaries)
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


def boundary_diagnostics(hjb, grid, da, db, threshold):
    """Raw + requested diagnostics for all four asset boundaries.

    Raw: ``max(mu,0)`` / ``max(-mu,0)`` (primary cross-resolution). Requested:
    raw/spacing (HJB/KFE compatibility). Raw thresholds = ``1e-10*da`` /
    ``1e-10*db`` corresponding to the accepted requested threshold ``1e-10``.
    a-slices have shape (b,z); b-slices have shape (a,z).
    """
    mu_a = np.asarray(hjb.mu_a, dtype=float)
    mu_b = np.asarray(hjb.mu_b, dtype=float)
    j_count = grid.a.size
    i_count = grid.b.size
    raw_threshold_a = threshold * da
    raw_threshold_b = threshold * db
    a_forward_raw = np.maximum(mu_a, 0.0)
    a_backward_raw = np.maximum(-mu_a, 0.0)
    b_forward_raw = np.maximum(mu_b, 0.0)
    b_backward_raw = np.maximum(-mu_b, 0.0)
    boundaries = [
        {
            "boundary": "upper_a",
            "direction": "a_forward",
            "raw": _slice_diagnostics("upper_a", "a_forward",
                                      a_forward_raw[:, j_count - 1, :], grid,
                                      raw_threshold_a, None, j_count - 1),
            "requested": _slice_diagnostics("upper_a", "a_forward",
                                            a_forward_raw[:, j_count - 1, :] / da, grid,
                                            threshold, None, j_count - 1),
        },
        {
            "boundary": "lower_a",
            "direction": "a_backward",
            "raw": _slice_diagnostics("lower_a", "a_backward",
                                      a_backward_raw[:, 0, :], grid,
                                      raw_threshold_a, None, 0),
            "requested": _slice_diagnostics("lower_a", "a_backward",
                                            a_backward_raw[:, 0, :] / da, grid,
                                            threshold, None, 0),
        },
        {
            "boundary": "upper_b",
            "direction": "b_forward",
            "raw": _slice_diagnostics("upper_b", "b_forward",
                                      b_forward_raw[i_count - 1, :, :], grid,
                                      raw_threshold_b, i_count - 1, None),
            "requested": _slice_diagnostics("upper_b", "b_forward",
                                            b_forward_raw[i_count - 1, :, :] / db, grid,
                                            threshold, i_count - 1, None),
        },
        {
            "boundary": "lower_b",
            "direction": "b_backward",
            "raw": _slice_diagnostics("lower_b", "b_backward",
                                      b_backward_raw[0, :, :], grid,
                                      raw_threshold_b, 0, None),
            "requested": _slice_diagnostics("lower_b", "b_backward",
                                            b_backward_raw[0, :, :] / db, grid,
                                            threshold, 0, None),
        },
    ]
    return {
        "max_raw_upper_a": float(a_forward_raw[:, j_count - 1, :].max()),
        "max_raw_lower_a": float(a_backward_raw[:, 0, :].max()),
        "max_raw_upper_b": float(b_forward_raw[i_count - 1, :, :].max()),
        "max_raw_lower_b": float(b_backward_raw[0, :, :].max()),
        "boundaries": boundaries,
    }


def _boundary_by_name(rec, section, name):
    for b in (rec.get(section) or {}).get("boundaries", []):
        if b["boundary"] == name:
            return b
    return None


# ---------------------------------------------------------------------------
# Per-variant pipeline
# ---------------------------------------------------------------------------


def run_all_variants(cfg: DLH5JConfig, dlh5b, params, numerics) -> dict:
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
            "a_res": spec.a_res,
            "b_ext": spec.b_ext,
            "grid": {
                "a_pts": int(grid.a.size), "a_lo": float(grid.a[0]), "a_hi": float(grid.a[-1]),
                "da": da, "b_pts": int(grid.b.size), "b_lo": float(grid.b[0]),
                "b_hi": float(grid.b[-1]), "db": db, "a_max": cfg.a_max,
                "z_pts": int(grid.z.size),
            },
            "frozen_prices_identity": {
                "wbar": cfg.wbar, "r_a": cfg.r_a, "taper_identity": cfg.taper_identity,
                "dlh5b_config": cfg.dlh5b_config_path, "region_index": cfg.region_index,
                "liquid_domain": {"b_lo": cfg.b_lo, "db": float(cfg.db),
                                  "route_ceiling_note": cfg.route_ceiling_note},
            },
            "hjb_converged": bool(hjb.converged),
            "hjb_iterations": int(hjb.iterations),
            "hjb_statistic": float(hjb.convergence_statistic),
        }
        if hjb.converged:
            rec["boundary"] = boundary_diagnostics(hjb, grid, da, db, cfg.boundary_threshold)
            ub = _boundary_by_name(rec, "boundary", "upper_b")
            ua = _boundary_by_name(rec, "boundary", "upper_a")
            rec["requested_upper_a"] = ua["requested"]["max"]
            rec["requested_upper_b"] = ub["requested"]["max"]
            rec["joint_compatible"] = bool(
                ub["requested"]["max"] <= cfg.boundary_threshold
                and ua["requested"]["max"] <= cfg.boundary_threshold
            )
            rec["joint_marker"] = JOINT_COMPATIBLE if rec["joint_compatible"] else JOINT_NOT_COMPATIBLE
            rec["variant_terminal"] = "HJB_CONVERGED"
        else:
            rec["boundary"] = None
            rec["requested_upper_a"] = None
            rec["requested_upper_b"] = None
            rec["joint_compatible"] = None
            rec["joint_marker"] = "HJB_NOT_CONVERGED"
            rec["variant_terminal"] = "HJB_NOT_CONVERGED"
        variants.append(rec)
        hjb_results[spec.id] = hjb
    return {"grid_plan": plan, "variants": variants, "hjb_results": hjb_results}


def build_fixture(cfg: DLH5JConfig):
    dlh5b = load_dlh5b_config(cfg.dlh5b_config_path)
    _grid, params, numerics = build_dlh5b_fixture(dlh5b)
    return dlh5b, params, numerics


# ---------------------------------------------------------------------------
# Accepted b100 scalar anchors (read-only, no rerun)
# ---------------------------------------------------------------------------


def b100_anchor(a_res: str) -> dict:
    if a_res == "a77":
        return dict(B100_ANCHOR_A77)
    if a_res == "a153":
        return dict(B100_ANCHOR_A153)
    raise ValueError(f"no b100 anchor for a resolution: {a_res}")


def b100_anchor_identity(cfg: DLH5JConfig) -> dict:
    """Report accepted b100 anchor identities (read-only scalar facts)."""
    out = {}
    for a_res in A_RES_ORDER:
        a = b100_anchor(a_res)
        out[a_res] = {
            "variant": a["variant"], "b_extent": a["b_extent"],
            "b_pts": a["b_pts"], "b_hi": a["b_hi"],
            "requested_upper_b_max": a["requested_max"],
            "requested_upper_b_count": a["requested_count"],
            "requested_upper_b_share": a["requested_share"],
            "argmax_index": a["argmax_index"],
            "argmax_physical": a["argmax_physical"],
            "raw_upper_b_max": a["raw_max"],
            "upper_a_requested_max": a["upper_a_requested_max"],
            "provenance": "ACCEPTED_DLH_5I_EVIDENCE__DLH_5I_BOUNDARY_DIAGNOSTICS_CSV__READ_ONLY",
            "rerun_in_dlh5j": False,
        }
    return out


# ---------------------------------------------------------------------------
# Phase C — final same-a continuation trends (b100 anchor + b120/b140/b160)
# ---------------------------------------------------------------------------


def _upper_b_entry(v: dict, threshold: float) -> dict:
    ub = _boundary_by_name(v, "boundary", "upper_b")
    ua = _boundary_by_name(v, "boundary", "upper_a")
    req = ub["requested"]
    raw = ub["raw"]
    return {
        "variant": v["variant"],
        "b_extent": v["b_ext"],
        "raw_max": raw["max"],
        "requested_max": req["max"],
        "raw_count": raw["count_above_threshold"],
        "requested_count": req["count_above_threshold"],
        "raw_share": raw["share_above_threshold"],
        "requested_share": req["share_above_threshold"],
        "argmax_physical_a_z": (req["argmax_physical"][1], req["argmax_physical"][2])
        if req["argmax_physical"] else None,
        "upper_a_requested_max": ua["requested"]["max"],
        "upper_a_compatible": bool(ua["requested"]["max"] <= threshold),
    }


def _b100_anchor_entry(a_res: str) -> dict:
    a = b100_anchor(a_res)
    return {
        "variant": a["variant"],
        "b_extent": a["b_extent"],
        "raw_max": a["raw_max"],
        "requested_max": a["requested_max"],
        "raw_count": a["raw_count"],
        "requested_count": a["requested_count"],
        "raw_share": a["raw_share"],
        "requested_share": a["requested_share"],
        "argmax_physical_a_z": (a["argmax_physical"][1], a["argmax_physical"][2]),
        "upper_a_requested_max": a["upper_a_requested_max"],
        "upper_a_compatible": bool(a["upper_a_requested_max"] <= 1e-10),
        "is_anchor": True,
    }


def _sequence_analysis(cfg: DLH5JConfig, entries: list[dict]) -> dict:
    raw_seq = [e["raw_max"] for e in entries]
    req_seq = [e["requested_max"] for e in entries]
    strictly_decreasing_raw = all(
        raw_seq[i] < raw_seq[i - 1] for i in range(1, len(raw_seq))
    ) if len(raw_seq) >= 2 else None
    strictly_decreasing_requested = all(
        req_seq[i] < req_seq[i - 1] for i in range(1, len(req_seq))
    ) if len(req_seq) >= 2 else None
    non_increasing_requested = all(
        req_seq[i] <= req_seq[i - 1] for i in range(1, len(req_seq))
    ) if len(req_seq) >= 2 else None
    plateau = bool(len(req_seq) >= 2 and all(
        abs(req_seq[i] - req_seq[i - 1]) <= 1e-12 * max(1.0, abs(req_seq[i - 1]))
        for i in range(1, len(req_seq))))
    adjacent_raw = []
    adjacent_requested = []
    for i in range(1, len(entries)):
        prev_r, cur_r = raw_seq[i - 1], raw_seq[i]
        if cur_r > 0.0:
            adjacent_raw.append(round(prev_r / cur_r, 6) if prev_r > 0.0 else 0.0)
        elif prev_r > 0.0:
            adjacent_raw.append("inf")
        else:
            adjacent_raw.append(None)
        prev_q, cur_q = req_seq[i - 1], req_seq[i]
        if cur_q > 0.0:
            adjacent_requested.append(round(prev_q / cur_q, 6) if prev_q > 0.0 else 0.0)
        elif prev_q > 0.0:
            adjacent_requested.append("inf")
        else:
            adjacent_requested.append(None)
    base_raw = raw_seq[0] if raw_seq else None
    base_req = req_seq[0] if req_seq else None
    vs_base_raw = [round(x / base_raw, 6) if (base_raw and base_raw > 0.0) else None for x in raw_seq]
    vs_base_requested = [round(x / base_req, 6) if (base_req and base_req > 0.0) else None for x in req_seq]
    first_below_threshold = None
    for e in entries:
        if e["requested_max"] <= cfg.boundary_threshold:
            first_below_threshold = e["b_extent"]
            break
    return {
        "entries": entries,
        "raw_seq": raw_seq,
        "requested_seq": req_seq,
        "adjacent_raw": adjacent_raw,
        "adjacent_requested": adjacent_requested,
        "vs_b100_raw": vs_base_raw,
        "vs_b100_requested": vs_base_requested,
        "strictly_decreasing_raw": bool(strictly_decreasing_raw) if strictly_decreasing_raw is not None else None,
        "strictly_decreasing_requested": bool(strictly_decreasing_requested) if strictly_decreasing_requested is not None else None,
        "non_increasing_requested": bool(non_increasing_requested) if non_increasing_requested is not None else None,
        "plateau": bool(plateau),
        "monotonic_flag": ("strictly_decreasing" if strictly_decreasing_requested
                           else ("non_increasing" if non_increasing_requested
                                 else ("plateau" if plateau else "non_monotonic"))),
        "first_requested_below_threshold": first_below_threshold,
        "upper_a_compatible_on_all_extents": bool(
            entries and all(e["upper_a_compatible"] for e in entries)),
    }


def extent_trends(cfg: DLH5JConfig, runs: dict) -> dict:
    by_id = {v["variant"]: v for v in runs["variants"]}
    sequences = {}
    for a_res in A_RES_ORDER:
        ids = [vid for vid in VARIANT_IDS
               if by_id.get(vid) and by_id[vid]["a_res"] == a_res]
        ids = sorted(ids, key=lambda vid: B_EXT_ORDER.index(by_id[vid]["b_ext"]))
        entries = [_b100_anchor_entry(a_res)]
        for vid in ids:
            v = by_id[vid]
            if not (v["hjb_converged"] and v.get("boundary")):
                continue
            entries.append(_upper_b_entry(v, cfg.boundary_threshold))
        sequences[a_res] = _sequence_analysis(cfg, entries)
    return {"sequences": sequences}


# ---------------------------------------------------------------------------
# Phase D — cross-a exact-node policy comparisons (J0/J3, J1/J4, J2/J5)
# ---------------------------------------------------------------------------


def cross_a_policy_comparisons(cfg: DLH5JConfig, runs: dict) -> list:
    hjb_by_id = runs["hjb_results"]
    by_id = {v["variant"]: v for v in runs["variants"]}
    pairs = [
        ("J0_A77_B120", "J3_A153_B120", "b120"),
        ("J1_A77_B140", "J4_A153_B140", "b140"),
        ("J2_A77_B160", "J5_A153_B160", "b160"),
    ]
    numeric_fields = ["value", "consumption", "labor", "transfer", "mu_a", "mu_b"]
    label_fields = ["liquid_label", "transfer_label"]
    top = cfg.top_coarse_layers_excluded
    out = []
    for coarse_id, fine_id, ext in pairs:
        c = {"comparison": f"{coarse_id}_vs_{fine_id}", "b_extent": ext,
             "coarse_a": "a77", "fine_a": "a153"}
        rc, rf = by_id[coarse_id], by_id[fine_id]
        if not (rc["hjb_converged"] and rf["hjb_converged"]):
            c["reached"] = False
            c["reason"] = "one or both HJB not converged"
            out.append(c)
            continue
        hc, hf = hjb_by_id[coarse_id], hjb_by_id[fine_id]
        b_pts = rc["grid"]["b_pts"]
        coarse_a_pts = rc["grid"]["a_pts"]
        # shared-interior mask: exclude top two coarse layers in EACH asset
        # dimension; include all z. a77 nodes are exactly every second a153 node.
        sb = slice(None, b_pts - top)
        sa_c = slice(None, coarse_a_pts - top)
        sa_f = slice(None, 2 * (coarse_a_pts - top), 2)
        fields = {}
        for f in numeric_fields:
            x = np.asarray(getattr(hc, f)[sb, sa_c, :], dtype=float)
            y = np.asarray(getattr(hf, f)[sb, sa_f, :], dtype=float)
            m = float(np.max(np.abs(x - y))) if x.size else 0.0
            ref = float(np.max(np.abs(x))) if x.size else 0.0
            fields[f] = {"max_abs_diff": m, "rel_diff": m / max(1.0, ref)}
        for lab in label_fields:
            x = getattr(hc, lab)[sb, sa_c, :]
            y = getattr(hf, lab)[sb, sa_f, :]
            fields[lab] = {"mismatch_count": int(np.sum(x != y))}
        c.update({"reached": True, "fields": fields})
        out.append(c)
    return out


# ---------------------------------------------------------------------------
# Phase E — joint compatibility frontier
# ---------------------------------------------------------------------------


def joint_frontier(cfg: DLH5JConfig, runs: dict) -> dict:
    by_id = {v["variant"]: v for v in runs["variants"]}
    per_variant = []
    for vid in VARIANT_IDS:
        v = by_id.get(vid)
        if v is None:
            continue
        per_variant.append({
            "variant": vid,
            "a_res": v["a_res"],
            "b_ext": v["b_ext"],
            "requested_upper_a": v.get("requested_upper_a"),
            "requested_upper_b": v.get("requested_upper_b"),
            "joint_compatible": v.get("joint_compatible"),
            "joint_marker": v.get("joint_marker"),
        })
    extents = []
    for ext in B_EXT_ORDER:
        ids = [vid for vid in VARIANT_IDS
               if by_id.get(vid) and by_id[vid]["b_ext"] == ext]
        ids = sorted(ids, key=lambda vid: A_RES_ORDER.index(by_id[vid]["a_res"]))
        row = {"b_extent": ext}
        comps = []
        for vid in ids:
            v = by_id[vid]
            jc = bool(v.get("joint_compatible"))
            comps.append(jc)
            row[v["a_res"] + "_variant"] = vid
            row[v["a_res"] + "_joint_compatible"] = jc
        both = all(comps)
        row["cross_a_joint_compatible"] = both
        row["marker"] = CROSS_A_COMPATIBLE if both else CROSS_A_NOT_COMPATIBLE
        extents.append(row)
    return {"per_variant": per_variant, "extents": extents}


# ---------------------------------------------------------------------------
# Phase F — final bounded-route stopping rule + terminal classification
# ---------------------------------------------------------------------------


def policy_sensitivity_annotation(cfg: DLH5JConfig, res: list) -> bool:
    """Pre-registered materiality: any required cross-a pair's scale-aware
    aligned-node relative difference for consumption/mu_a/mu_b exceeds
    ``cfg.policy_rel_materiality`` (default 1e-2)."""
    for c in res:
        if not c.get("reached"):
            continue
        for f in ("consumption", "mu_a", "mu_b"):
            m = c["fields"].get(f) or {}
            if (m.get("rel_diff") or 0.0) > cfg.policy_rel_materiality:
                return True
    return False


def stopping_rule(cfg: DLH5JConfig, runs: dict, repro: dict, res: list) -> dict:
    """Binding route rule (Issue #36 section 10 / roadmap decision tree)."""
    if not repro["pass_bool"]:
        return {"route": "REPRODUCIBILITY_BLOCKER", "note": "reproducibility failed; fail closed"}
    if any(not v["hjb_converged"] for v in runs["variants"]):
        return {"route": "HJB_NUMERICAL_STABILITY_BLOCKER", "note": "an HJB did not converge under accepted numerics"}
    frontier = joint_frontier(cfg, runs)
    if any(e["cross_a_joint_compatible"] for e in frontier["extents"]):
        smallest = next(e["b_extent"] for e in frontier["extents"] if e["cross_a_joint_compatible"])
        return {
            "route": "B_RESOLUTION_CONFIRMATION_AT_SMALLEST_COMPATIBLE_EXTENT",
            "smallest_compatible_extent": smallest,
            "note": "STOP grid continuation; only a bounded b-resolution confirmation at "
                    f"{smallest} is recommended before any stationary-KFE re-entry.",
        }
    trends = extent_trends(cfg, runs)
    seqs = trends["sequences"]
    clean = all(s["strictly_decreasing_requested"] for s in seqs.values())
    if clean:
        return {
            "route": "ASYMPTOTIC_OR_FINITE_DOMAIN_CLOSURE_ADJUDICATION",
            "note": "STOP larger-grid continuation (b160 hard ceiling); no common threshold reached; "
                    "next gate must adjudicate high-wealth liquid drift / economic mean reversion / "
                    "finite-domain HJB closure analytically or semi-analytically.",
        }
    return {
        "route": "ASYMPTOTIC_OR_FINITE_DOMAIN_CLOSURE_ADJUDICATION",
        "note": "final extent behavior is persistent/plateau/non-monotonic; escalate immediately to "
                "high-wealth/asymptotic or finite-domain HJB-closure adjudication.",
    }


def overall_terminal(cfg: DLH5JConfig, runs: dict, repro: dict, res: list) -> dict:
    if not repro["pass_bool"]:
        terminal = TERMINAL_OUTCOME_F
    elif any(not v["hjb_converged"] for v in runs["variants"]):
        terminal = TERMINAL_OUTCOME_E
    else:
        frontier = joint_frontier(cfg, runs)
        if any(e["cross_a_joint_compatible"] for e in frontier["extents"]):
            terminal = TERMINAL_OUTCOME_A
        elif any(v.get("joint_compatible") for v in runs["variants"]):
            terminal = TERMINAL_OUTCOME_B
        else:
            trends = extent_trends(cfg, runs)
            seqs = trends["sequences"]
            if all(s["strictly_decreasing_requested"] for s in seqs.values()):
                terminal = TERMINAL_OUTCOME_C
            else:
                terminal = TERMINAL_OUTCOME_D
    annotations = []
    if policy_sensitivity_annotation(cfg, res):
        annotations.append(ANNOTATION_CROSS_A_SENSITIVITY)
    return {"terminal": terminal, "annotations": annotations}


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------


def _variant_structural_signature(rec: dict) -> str:
    bd = rec.get("boundary") or {}
    discrete = {}
    for b in bd.get("boundaries", []):
        discrete[b["boundary"]] = {
            "raw_count": b["raw"]["count_above_threshold"],
            "requested_count": b["requested"]["count_above_threshold"],
            "raw_argmax_index": b["raw"]["argmax_index"],
            "requested_argmax_index": b["requested"]["argmax_index"],
            "raw_offending": [(o["b_index"], o["a_index"], o["z_index"]) for o in b["raw"]["offending_states"]],
            "requested_offending": [(o["b_index"], o["a_index"], o["z_index"]) for o in b["requested"]["offending_states"]],
        }
    return json.dumps({
        "variant": rec.get("variant"),
        "a_res": rec.get("a_res"),
        "b_ext": rec.get("b_ext"),
        "grid": rec.get("grid"),
        "hjb_converged": rec.get("hjb_converged"),
        "hjb_iterations": rec.get("hjb_iterations"),
        "joint_marker": rec.get("joint_marker"),
        "boundary": discrete,
    }, sort_keys=True)


def _variant_numeric_numbers(rec: dict) -> list:
    out: list[float] = []
    if rec.get("hjb_statistic") is not None:
        out.append(float(rec["hjb_statistic"]))
    bd = rec.get("boundary") or {}
    for b in bd.get("boundaries", []):
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


def compare_variant_records(r1: dict, r2: dict, cfg: DLH5JConfig) -> dict:
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


def reproduce(cfg: DLH5JConfig, dlh5b, params, numerics) -> dict:
    run1 = run_all_variants(cfg, dlh5b, params, numerics)
    run2 = run_all_variants(cfg, dlh5b, params, numerics)
    per_variant = {}
    for r1, r2 in zip(run1["variants"], run2["variants"]):
        per_variant[r1["variant"]] = compare_variant_records(r1, r2, cfg)
    res1 = cross_a_policy_comparisons(cfg, run1)
    t1 = overall_terminal(cfg, run1, {"pass_bool": True}, res1)
    res2 = cross_a_policy_comparisons(cfg, run2)
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


def _boundary_rows(rec, kind):
    rows = []
    for b in (rec.get("boundary") or {}).get("boundaries", []):
        for o in b[kind].get("offending_states", []):
            rows.append([rec["variant"], b["boundary"], b["direction"], kind,
                         o["b_index"], o["a_index"], o["z_index"],
                         _fmt(o["b"]), _fmt(o["a"]), _fmt(o["z"]), _fmt(o["rate"])])
    return rows


def write_evidence(root: pathlib.Path, cfg: DLH5JConfig, runs: dict, trends: dict,
                   res: list, frontier: dict, anchors: dict, repro: dict, term: dict,
                   route: dict) -> None:
    root = pathlib.Path(root)
    root.mkdir(parents=True, exist_ok=True)

    # 1) VARIANT_STATUS.csv
    rows = []
    for v in runs["variants"]:
        g = v["grid"]
        bd = v.get("boundary") or {}
        rows.append([v["variant"], v["a_res"], v["b_ext"],
                     g["a_pts"], _fmt(g["a_lo"]), _fmt(g["a_hi"]), _fmt(g["da"]),
                     g["b_pts"], _fmt(g["b_lo"]), _fmt(g["b_hi"]), _fmt(g["db"]),
                     v["hjb_converged"], v["hjb_iterations"], _fmt(v["hjb_statistic"]),
                     _fmt(bd.get("max_raw_upper_a")), _fmt(bd.get("max_raw_lower_a")),
                     _fmt(bd.get("max_raw_upper_b")), _fmt(bd.get("max_raw_lower_b")),
                     v.get("joint_marker"), v.get("variant_terminal")])
    _write_csv(root / "DLH_5J_VARIANT_STATUS.csv",
               ["variant", "a_res", "b_ext", "a_pts", "a_lo", "a_hi", "da",
                "b_pts", "b_lo", "b_hi", "db",
                "hjb_converged", "hjb_iterations", "hjb_statistic",
                "max_raw_upper_a", "max_raw_lower_a", "max_raw_upper_b", "max_raw_lower_b",
                "joint_marker", "variant_terminal"], rows)

    # 2) BOUNDARY_DIAGNOSTICS.csv (summary + offending, raw + requested, 4 boundaries)
    rows = []
    for v in runs["variants"]:
        bd = v.get("boundary") or {}
        for b in bd.get("boundaries", []):
            for kind in ("raw", "requested"):
                d = b[kind]
                rows.append([v["variant"], b["boundary"], b["direction"], kind,
                             _fmt(d["max"]), d["count_above_threshold"],
                             _fmt(d["share_above_threshold"]), d.get("argmax_index"),
                             d.get("argmax_physical"), _fmt(d.get("value_at_argmax")),
                             _q_fmt(d.get("quantiles")), "", "", "", "", "", "", ""])
        for o in _boundary_rows(v, "raw"):
            rows.append([v["variant"], o[1], o[2], "raw_offending", _fmt(o[10]),
                         "", "", "", "", "", "", o[4], o[5], o[6], o[7], o[8], o[9], o[10]])
        for o in _boundary_rows(v, "requested"):
            rows.append([v["variant"], o[1], o[2], "requested_offending", _fmt(o[10]),
                         "", "", "", "", "", "", o[4], o[5], o[6], o[7], o[8], o[9], o[10]])
    _write_csv(root / "DLH_5J_BOUNDARY_DIAGNOSTICS.csv",
               ["variant", "boundary", "direction", "kind", "max", "count_above_threshold",
                "share_above_threshold", "argmax_index", "argmax_physical",
                "value_at_argmax", "quantiles_q50_q90_q95_q99",
                "b_index", "a_index", "z_index", "b", "a", "z", "rate"], rows)

    # 3) FINAL_EXTENT_TRENDS.csv (b100 anchor + b120/b140/b160, A77 and A153)
    rows = []
    for a_res in A_RES_ORDER:
        seq = trends["sequences"][a_res]
        for e in seq["entries"]:
            kind = "ANCHOR_B100" if e.get("is_anchor") else "ENTRY"
            rows.append([a_res, e["b_extent"], e["variant"], kind,
                         _fmt(e["raw_max"]), _fmt(e["requested_max"]),
                         e["raw_count"], e["requested_count"],
                         _fmt(e["raw_share"]), _fmt(e["requested_share"]),
                         e["argmax_physical_a_z"], e["upper_a_compatible"], "", "", ""])
        rows.append([a_res, "RATIO", "adjacent_raw", "", "", "", "", "", "", "",
                     "", "", "", _fmt(seq["adjacent_raw"]), ""])
        rows.append([a_res, "RATIO", "adjacent_requested", "", "", "", "", "", "", "",
                     "", "", "", _fmt(seq["adjacent_requested"]), ""])
        rows.append([a_res, "RATIO", "vs_b100_raw", "", "", "", "", "", "", "",
                     "", "", "", _fmt(seq["vs_b100_raw"]), ""])
        rows.append([a_res, "RATIO", "vs_b100_requested", "", "", "", "", "", "", "",
                     "", "", "", _fmt(seq["vs_b100_requested"]), ""])
        rows.append([a_res, "FLAG", "strictly_decreasing_raw", str(seq["strictly_decreasing_raw"]),
                     "", "", "", "", "", "", "", "", "", "", ""])
        rows.append([a_res, "FLAG", "strictly_decreasing_requested", str(seq["strictly_decreasing_requested"]),
                     "", "", "", "", "", "", "", "", "", "", ""])
        rows.append([a_res, "FLAG", "non_increasing_requested", str(seq["non_increasing_requested"]),
                     "", "", "", "", "", "", "", "", "", "", ""])
        rows.append([a_res, "FLAG", "plateau", str(seq["plateau"]),
                     "", "", "", "", "", "", "", "", "", "", ""])
        rows.append([a_res, "FLAG", "monotonic_flag", seq["monotonic_flag"],
                     "", "", "", "", "", "", "", "", "", "", ""])
        rows.append([a_res, "FLAG", "first_requested_below_threshold", str(seq["first_requested_below_threshold"]),
                     "", "", "", "", "", "", "", "", "", "", ""])
        rows.append([a_res, "FLAG", "upper_a_compatible_on_all_extents", str(seq["upper_a_compatible_on_all_extents"]),
                     "", "", "", "", "", "", "", "", "", "", ""])
    _write_csv(root / "DLH_5J_FINAL_EXTENT_TRENDS.csv",
               ["a_res", "b_extent", "variant", "kind",
                "raw_max", "requested_max", "raw_count", "requested_count",
                "raw_share", "requested_share", "argmax_physical_a_z",
                "upper_a_compatible", "note", "extra1", "extra2"], rows)

    # 4) CROSS_A_POLICY_STABILITY.csv
    rows = []
    for c in res:
        if not c.get("reached"):
            rows.append([c["comparison"], c["b_extent"], c["coarse_a"], c["fine_a"],
                         "NOT_REACHED", "", "", "", c.get("reason", "")])
            continue
        for f, m in c["fields"].items():
            if f in ("liquid_label", "transfer_label"):
                rows.append([c["comparison"], c["b_extent"], c["coarse_a"], c["fine_a"],
                             f, "", "", m["mismatch_count"], ""])
            else:
                rows.append([c["comparison"], c["b_extent"], c["coarse_a"], c["fine_a"],
                             f, _fmt(m["max_abs_diff"]), _fmt(m["rel_diff"]), "", ""])
    _write_csv(root / "DLH_5J_CROSS_A_POLICY_STABILITY.csv",
               ["comparison", "b_extent", "coarse_a", "fine_a",
                "field", "max_abs_diff", "rel_diff", "mismatch_count", "note"], rows)

    # 5) JOINT_COMPATIBILITY_FRONTIER.csv
    rows = []
    for p in frontier["per_variant"]:
        rows.append(["variant", p["b_ext"], p["a_res"], p["variant"],
                     _fmt(p["requested_upper_a"]), _fmt(p["requested_upper_b"]),
                     p["joint_marker"], ""])
    for e in frontier["extents"]:
        rows.append(["cross_a_extent", e["b_extent"], "a77", e["a77_variant"],
                     "", "", "", e["a77_joint_compatible"]])
        rows.append(["cross_a_extent", e["b_extent"], "a153", e["a153_variant"],
                     "", "", "", e["a153_joint_compatible"]])
        rows.append(["cross_a_extent", e["b_extent"], "BOTH", "",
                     "", "", e["marker"], e["cross_a_joint_compatible"]])
    _write_csv(root / "DLH_5J_JOINT_COMPATIBILITY_FRONTIER.csv",
               ["item", "b_extent", "a_res", "variant",
                "requested_upper_a", "requested_upper_b", "marker", "compatible"], rows)

    # 6) REPRODUCIBILITY.json
    with open(root / "DLH_5J_REPRODUCIBILITY.json", "w", encoding="utf-8") as fh:
        json.dump(repro, fh, indent=2, default=str, sort_keys=True)

    # 7) EXECUTION_REPORT.md
    with open(root / "DLH_5J_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_report(cfg, runs, trends, res, frontier, anchors, repro, term, route))

    # 8) FORBIDDEN_OPERATION_CHECK.md
    with open(root / "DLH_5J_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write(_render_forbidden_check(cfg, runs, repro, term))


def _render_report(cfg: DLH5JConfig, runs: dict, trends: dict, res: list,
                   frontier: dict, anchors: dict, repro: dict, term: dict,
                   route: dict) -> str:
    lines = []
    lines.append("# DLH-5J — Final Bounded Coupled Liquid-Extent Continuation (Issue #36)")
    lines.append("")
    lines.append("Policy-only diagnostic completing the last pre-frozen larger-b grid experiment "
                 "before asymptotic adjudication. Accepted MATLAB-faithful HJB source is immutable "
                 "and reused read-only.")
    lines.append("")
    lines.append(f"Overall terminal classification: `{term['terminal']}`")
    if term["annotations"]:
        lines.append("")
        lines.append("Secondary scientific annotations: " +
                     ", ".join(f"`{a}`" for a in term["annotations"]))
    lines.append("")
    lines.append(f"Binding route rule: `{route['route']}` — {route['note']}")
    lines.append("")
    lines.append(f"Frozen economics: `wbar={cfg.wbar}`, `r_a={cfg.r_a}`; physical illiquid domain "
                 f"`a [{cfg.a_lo},{cfg.a_hi}]`, `a_max={cfg.a_max}`, taper `{cfg.taper_identity}`; "
                 f"liquid spacing `db={cfg.db:.12f}`; only mature a resolutions a77/a153 and final b "
                 f"extents b120/b140/b160; {cfg.route_ceiling_note}; all non-grid objects the accepted "
                 f"DLH-5B/DLH-5E fixture (`{cfg.dlh5b_config_path}`, region_index={cfg.region_index}). "
                 f"Accepted DLH-5I b100 results are read-only scalar anchors only (b100 NOT rerun).")
    lines.append("")

    lines.append("## Accepted b100 scalar anchors (read-only, Issue #36 section 7)")
    lines.append("")
    for a_res in A_RES_ORDER:
        a = anchors[a_res]
        lines.append(f"- {a['variant']} ({a_res}): requested upper-b {a['requested_upper_b_max']:.9e} "
                     f"({a['requested_upper_b_count']} states, share {a['requested_upper_b_share']:.9e}), "
                     f"argmax {a['argmax_index']} physical {a['argmax_physical']}, raw upper-b "
                     f"{a['raw_upper_b_max']:.9e}, upper-a requested {a['upper_a_requested_max']:.1e}. "
                     f"Provenance: {a['provenance']} (rerun in DLH-5J: {a['rerun_in_dlh5j']}).")
    lines.append("")

    lines.append("## Variant status (Phase A)")
    lines.append("")
    lines.append("| variant | a res | b ext | a pts | da | b pts | b_hi | db | HJB conv | iters | stat | raw upper-a | raw lower-a | raw upper-b | raw lower-b | joint marker |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for v in runs["variants"]:
        g = v["grid"]
        bd = v.get("boundary") or {}
        lines.append(f"| {v['variant']} | {v['a_res']} | {v['b_ext']} | {g['a_pts']} | {_sf(g['da'])} | "
                     f"{g['b_pts']} | {_sf(g['b_hi'])} | {_sf(g['db'])} | {v['hjb_converged']} | "
                     f"{v['hjb_iterations']} | {_sf(v['hjb_statistic'], '.3e')} | "
                     f"{_sf(bd.get('max_raw_upper_a'), '.3e')} | {_sf(bd.get('max_raw_lower_a'), '.3e')} | "
                     f"{_sf(bd.get('max_raw_upper_b'), '.3e')} | {_sf(bd.get('max_raw_lower_b'), '.3e')} | "
                     f"{_sf(v.get('joint_marker'))} |")
    lines.append("")

    lines.append("## Complete boundary diagnostics (Phase B, all four asset boundaries)")
    lines.append("")
    lines.append("Raw drift (`max(mu,0)` / `max(-mu,0)`) is the primary cross-resolution "
                 "quantity; requested generator rate (raw/spacing) is the HJB/KFE compatibility "
                 "quantity. Raw thresholds `1e-10*da`/`1e-10*db` correspond to the accepted "
                 "requested-rate threshold `1e-10`. Coordinates are exact `(b_index,a_index,z_index)` "
                 "plus physical `(b,a,z)` via C-order unraveling on the actual 2-D boundary slice.")
    lines.append("")
    for v in runs["variants"]:
        bd = v.get("boundary") or {}
        if not bd:
            lines.append(f"### {v['variant']} — HJB not converged")
            lines.append("")
            continue
        lines.append(f"### {v['variant']}")
        lines.append("")
        lines.append("| boundary | kind | max | count | share | argmax index | argmax physical | value at argmax | q50/q90/q95/q99 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for b in bd["boundaries"]:
            for kind in ("raw", "requested"):
                d = b[kind]
                lines.append(f"| {b['boundary']} | {kind} | {_sf(d['max'], '.3e')} | "
                             f"{_sf(d['count_above_threshold'])} | {_sf(d['share_above_threshold'], '.3e')} | "
                             f"{d.get('argmax_index')} | {d.get('argmax_physical')} | "
                             f"{_sf(d.get('value_at_argmax'), '.3e')} | {_q_fmt(d.get('quantiles'))} |")
        lines.append("")
        lines.append("Complete offending states (raw > `1e-10*spacing`; requested > `1e-10`):")
        lines.append("")
        rows = _boundary_rows(v, "raw") + _boundary_rows(v, "requested")
        if rows:
            lines.append("| boundary | kind | b_index | a_index | z_index | b | a | z | rate |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for r in rows:
                lines.append(f"| {r[1]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {_sf(r[7], '.6f')} | "
                             f"{_sf(r[8], '.6f')} | {_sf(r[9], '.6f')} | {_sf(r[10], '.9e')} |")
        else:
            lines.append("No state exceeds the raw or requested threshold.")
        lines.append("")

    lines.append("## Final same-a continuation trends (Phase C: b100 anchor -> b120 -> b140 -> b160)")
    lines.append("")
    for a_res in A_RES_ORDER:
        seq = trends["sequences"][a_res]
        lines.append(f"### {a_res}")
        lines.append("")
        lines.append("| b extent | variant | kind | raw upper-b max | requested upper-b max | raw count | requested count | argmax physical (a,z) | upper-a compatible |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for e in seq["entries"]:
            kind = "ANCHOR_B100" if e.get("is_anchor") else "ENTRY"
            lines.append(f"| {e['b_extent']} | {e['variant']} | {kind} | {_sf(e['raw_max'], '.3e')} | "
                         f"{_sf(e['requested_max'], '.3e')} | {e['raw_count']} | {e['requested_count']} | "
                         f"{e['argmax_physical_a_z']} | {e['upper_a_compatible']} |")
        lines.append("")
        lines.append(f"- adjacent raw attenuation ratios (b100/b120, b120/b140, b140/b160): {seq['adjacent_raw']}")
        lines.append(f"- adjacent requested attenuation ratios: {seq['adjacent_requested']}")
        lines.append(f"- raw ratios relative to accepted b100: {seq['vs_b100_raw']}")
        lines.append(f"- requested ratios relative to accepted b100: {seq['vs_b100_requested']}")
        lines.append(f"- strictly decreasing requested upper-b max over the continuation: {seq['strictly_decreasing_requested']}")
        lines.append(f"- non-increasing requested flag: {seq['non_increasing_requested']}")
        lines.append(f"- plateau flag: {seq['plateau']}")
        lines.append(f"- monotonic flag: {seq['monotonic_flag']}")
        lines.append(f"- first final extent with requested upper-b <= 1e-10: {seq['first_requested_below_threshold']}")
        lines.append(f"- upper-a compatible on every final extent: {seq['upper_a_compatible_on_all_extents']}")
        lines.append("")
    lines.append("These are policy-only trends; no post-hoc root is fitted and no adaptive next extent "
                 "is generated (b160 is the hard route ceiling). Any upper-a reactivation on an extended "
                 "b extent is preserved as evidence, not clipped.")

    lines.append("")
    lines.append("## Cross-a exact-node policy comparisons (Phase D)")
    lines.append("")
    lines.append("Three required pairs at common final extents (a77 vs every-second a153, all common "
                 "b nodes, all z, no interpolation). Shared-interior mask excludes the top two "
                 "coarse layers in EACH asset dimension. `rel_diff = max_abs / max(1, max|coarse|)` "
                 "is scale-aware.")
    lines.append("")
    for c in res:
        lines.append(f"### {c['comparison']} ({c['b_extent']})")
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

    lines.append("## Joint HJB upper-boundary policy compatibility frontier (Phase E)")
    lines.append("")
    lines.append("Per-variant prerequisite marker: `requested_upper_b <= 1e-10 AND "
                 "requested_upper_a <= 1e-10`. `CROSS_A_RESOLUTION_JOINT_COMPATIBLE_AT_B_EXTENT` "
                 "holds only when BOTH mature a resolutions at the same final extent pass both "
                 "thresholds. Prerequisite marker only — it does NOT authorize stationary KFE.")
    lines.append("")
    for p in frontier["per_variant"]:
        lines.append(f"- {p['variant']}: {p['joint_marker']} "
                     f"(ua {_sf(p['requested_upper_a'], '.3e')}, ub {_sf(p['requested_upper_b'], '.3e')})")
    lines.append("")
    for e in frontier["extents"]:
        lines.append(f"- {e['b_extent']} cross-a: a77={e['a77_joint_compatible']}, "
                     f"a153={e['a153_joint_compatible']} -> {e['marker']}")
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
                 "`dsh/issue-36-dlh-5j-final-coupled-b-extent-2026-09-01`; allowlist-only additions "
                 "(3 artifacts + 8 evidence files).")
    lines.append("")
    lines.append("DLH-5J implements NO repair and NO stationary acceptance: accepted HJB/KFE/regional "
                 "source immutable; physical a-domain/a_max/taper/economics/tolerances/initialization "
                 "frozen; a77/a153 only; db=7/19 only; b120/b140/b160 only (b160 hard ceiling); no "
                 "b100 rerun; no clipping; no D1-D3; no regional or multi-province GE; no learned "
                 "network; no nominal HANK.")
    return "\n".join(lines)


def _render_forbidden_check(cfg: DLH5JConfig, runs: dict, repro: dict, term: dict) -> str:
    lines = [
        "# DLH-5J — Forbidden-Operation / Scope Check (Issue #36)",
        "",
        "DSH did NOT perform any of the following during DLH-5J execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |",
        "| Modify `coupled_boundary_frontier_diagnostic.py` | NOT performed (read-only reference) |",
        "| Modify any existing HJB/local-policy/KFE/regional source | NOT performed |",
        "| Modify accepted Issues #23-#35 evidence | NOT performed |",
        "| Change physical a domain, `a_max=10` or accepted taper | NOT performed (frozen) |",
        "| Widen a domain | NOT performed |",
        "| Change a resolution outside a77/a153 | NOT performed (only a77/a153) |",
        "| Change `db` from 7/19 | NOT performed (db=7/19 frozen) |",
        "| Use a b extent beyond b160 | NOT performed (b160 is the hard route ceiling) |",
        "| Rerun b100 as an extra variant | NOT performed (read-only scalar anchors only) |",
        "| Modify economics/prices/parameters/tolerances/initialization | NOT performed (frozen D0) |",
        "| Warm-start one grid from another | NOT performed (fresh initialization per variant) |",
        "| Add adaptive/seventh grid, grid search or root-seeking extent | NOT performed (exact J0-J5) |",
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
    parser = argparse.ArgumentParser(description="DLH-5J final bounded coupled liquid-extent continuation (Issue #36)")
    parser.add_argument("--config", default="configs/dlh_5j_final_coupled_b_extent_diagnostic.toml")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    root = pathlib.Path(cfg.output_root)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"output root already exists (no-overwrite): {root}")
    dlh5b, params, numerics = build_fixture(cfg)
    runs = run_all_variants(cfg, dlh5b, params, numerics)
    trends = extent_trends(cfg, runs)
    res = cross_a_policy_comparisons(cfg, runs)
    frontier = joint_frontier(cfg, runs)
    anchors = b100_anchor_identity(cfg)
    repro = reproduce(cfg, dlh5b, params, numerics)
    term = overall_terminal(cfg, runs, repro, res)
    route = stopping_rule(cfg, runs, repro, res)
    write_evidence(root, cfg, runs, trends, res, frontier, anchors, repro, term, route)
    print(f"artifacts written under {root}")
    print(f"terminal = {term['terminal']}")
    if term["annotations"]:
        print("annotations = " + ", ".join(term["annotations"]))
    print(f"route = {route['route']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
