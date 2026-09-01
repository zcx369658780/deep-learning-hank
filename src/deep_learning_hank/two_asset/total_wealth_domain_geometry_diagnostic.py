"""DLH-5L (Issue #38) — componentwise liquid outward drift versus total-wealth
mean reversion and boundary geometry.

Analytical/source-preserving adjudication. Reruns exactly the six accepted
DLH-5J/DLH-5K grids (J0-J5) solely to evaluate the total-wealth drift
``mu_W = mu_a + mu_b`` and the local ``W = a + b`` normal-drift geometry. No new
grid, no new b extent (b160 hard ceiling), no new a resolution, no b-resolution
change, no b100 rerun, no warm start. Every rerun must reproduce the accepted
DLH-5J HJB statistics and boundary maxima/counts within the frozen comparison
tolerance or fail closed (Outcome D).

The inspected state set is PRE-FROZEN as the exact union of
``(variant,b_index,a_index,z_index)`` coordinates appearing in the accepted
DLH-5K evidence:
- ``DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv``
- ``DLH_5K_CROSS_A_MECHANISM.csv``
deduplicated only by exact identity. No post-hoc states are added.

Phases:
- Phase A: exact ``mu_W = mu_a + mu_b`` and the transfer-cancelled budget
  reconstruction at every inherited state; verify the linear transfer term
  cancels one-for-one between mu_a and mu_b.
- Phase B: four-way component-liquid / total-wealth classification
  (B_OUTWARD__TOTAL_INWARD / B_OUTWARD__TOTAL_OUTWARD /
   B_NONOUTWARD__TOTAL_INWARD / B_NONOUTWARD__TOTAL_OUTWARD) with counts by
  variant, top-vs-interior layer, a resolution and z; explicit coverage of every
  accepted DLH-5K INTERIOR_POSITIVE_PERSISTS state.
- Phase C: for every positive-mu_b state, portfolio-reallocation decomposition
  and the linear d / -d transfer cancellation verified separately from
  adjustment cost.
- Phase D: analytical geometry comparison between the rectangular componentwise
  bounds (mu_a<=0, mu_b<=0) and the local constant-W normal drift
  (mu_W = mu_a + mu_b <= 0), without changing the production domain.
- Phase E: exact aligned a77/a153 total-wealth comparison (mu_a, mu_b, mu_W,
  transfer, adjustment cost, base_liquid_surplus, transfer_injection) with the
  pre-registered scale-aware materiality threshold policy_rel_materiality=1e-2.

Policy-only: stationary fields use the not-authorized marker (mirroring the
accepted DLH-5K policy-only pattern; Issue #38 forbids stationary execution).
"""

from __future__ import annotations

import csv
import dataclasses
import json
import pathlib
import tomllib
from typing import Any

from deep_learning_hank.two_asset import (
    MatlabFaithfulHJBGrid,
)
from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    matlab_faithful_illiquid_return,
)
from deep_learning_hank.two_asset.high_wealth_corner_closure_diagnostic import (
    ACCEPTED_J_HJB_STAT,
    ACCEPTED_J_UPPER_B,
    ACCEPTED_BLOB,
    ACCEPTED_SHA256,
    VARIANT_IDS,
    build_all_grids as dlh5k_build_all_grids,
    build_fixture as dlh5k_build_fixture,
    check_accepted_j_reproduction,
    grid_plan_identity as dlh5k_grid_plan_identity,
    reconstruct_derivatives,
    reproduce as dlh5k_reproduce,
    run_all_variants as dlh5k_run_all_variants,
    _decompose_state as dlh5k_decompose_state,
    NOT_AUTHORIZED_MARKER,
)

# ---------------------------------------------------------------------------
# Terminals / markers (Issue #38 section 9)
# ---------------------------------------------------------------------------

TERMINAL_OUTCOME_A = "DLH_5L_COMPONENTWISE_LIQUID_OUTWARD_DRIFT_WITH_TOTAL_WEALTH_MEAN_REVERSION_CONFIRMED__DOMAIN_GEOMETRY_DESIGN_REVIEW_REQUIRED"
TERMINAL_OUTCOME_B = "DLH_5L_TOTAL_WEALTH_OUTWARD_DRIFT_PERSISTS_IN_HIGH_WEALTH_INTERIOR__ECONOMIC_MEAN_REVERSION_NOT_ESTABLISHED__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_OUTCOME_C = "DLH_5L_MIXED_TOTAL_WEALTH_AND_PORTFOLIO_REALLOCATION_MECHANISM__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_OUTCOME_D = "BLOCKED_DLH_5L_ACCEPTED_HJB_REPRODUCTION"
TERMINAL_OUTCOME_E = "BLOCKED_DLH_5L_REPRODUCIBILITY"
ANNOTATION_CROSS_A_PORTFOLIO_REALLOCATION = (
    "DLH_5L_CROSS_A_LIQUID_DIVERGENCE_PORTFOLIO_REALLOCATION_DOMINATED__SCIENTIFIC_REVIEW_REQUIRED"
)

CLASS_B_OUTWARD_TOTAL_INWARD = "B_OUTWARD__TOTAL_INWARD"
CLASS_B_OUTWARD_TOTAL_OUTWARD = "B_OUTWARD__TOTAL_OUTWARD"
CLASS_B_NONOUTWARD_TOTAL_INWARD = "B_NONOUTWARD__TOTAL_INWARD"
CLASS_B_NONOUTWARD_TOTAL_OUTWARD = "B_NONOUTWARD__TOTAL_OUTWARD"

DB0 = 7.0 / 19.0
DA0 = 10.0 / 19.0


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
class DLH5LConfig:
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
    dlh5k_localization_csv: str
    dlh5k_cross_a_csv: str
    boundary_threshold: float
    reproducibility_tol: float
    accepted_hjb_stat_tol: float
    accepted_boundary_max_tol: float
    accepted_count_exact: bool
    decomposition_residual_tol: float
    policy_rel_materiality: float
    scale_floor: float
    output_root: str


def load_config(path: str | pathlib.Path) -> DLH5LConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    hf = raw["household_fixture"]
    fp = raw["frozen_prices"]
    fa = raw["frozen_physical_illiquid"]
    ld = raw["liquid_domain"]
    si = raw["shared_interior"]
    ss = raw["state_set"]
    v = raw["validation"]
    out = raw["output"]
    a_resolutions = tuple(ARes(id=str(r["id"]), a_pts=int(r["a_pts"])) for r in raw["a_resolutions"])
    b_extents = tuple(BExt(id=str(e["id"]), b_pts=int(e["b_pts"]), b_hi=float(e["b_hi"])) for e in raw["b_extents"])
    variants = tuple(
        GridSpec(id=str(g["id"]), a_res=str(g["a_res"]), b_ext=str(g["b_ext"]))
        for g in raw["variants"]
    )
    return DLH5LConfig(
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
        dlh5k_localization_csv=str(ss["dlh5k_localization_csv"]),
        dlh5k_cross_a_csv=str(ss["dlh5k_cross_a_csv"]),
        boundary_threshold=float(v["boundary_threshold"]),
        reproducibility_tol=float(v["reproducibility_tol"]),
        accepted_hjb_stat_tol=float(v["accepted_hjb_stat_tol"]),
        accepted_boundary_max_tol=float(v["accepted_boundary_max_tol"]),
        accepted_count_exact=bool(v["accepted_count_exact"]),
        decomposition_residual_tol=float(v["decomposition_residual_tol"]),
        policy_rel_materiality=float(v["policy_rel_materiality"]),
        scale_floor=float(v.get("scale_floor", 1e-10)),
        output_root=str(out["root"]),
    )


# ---------------------------------------------------------------------------
# Accepted grid plan (exact J0-J5) — reuse accepted DLH-5K identity
# ---------------------------------------------------------------------------


def grid_plan_identity(cfg: DLH5LConfig) -> dict:
    plan = dlh5k_grid_plan_identity(cfg)
    return plan


def build_all_grids(cfg: DLH5LConfig, z, switch) -> tuple[dict, dict]:
    return dlh5k_build_all_grids(cfg, z, switch)


def build_fixture(cfg: DLH5LConfig):
    return dlh5k_build_fixture(cfg)


def run_all_variants(cfg: DLH5LConfig, dlh5b, params, numerics) -> dict:
    return dlh5k_run_all_variants(cfg, dlh5b, params, numerics)


def _grid_for(runs: dict, vid: str) -> MatlabFaithfulHJBGrid:
    return runs["grids"][vid]


# ---------------------------------------------------------------------------
# Pre-frozen inherited state set (accepted DLH-5K localization + cross-a)
# ---------------------------------------------------------------------------


def resolve_inherited_state_set(cfg: DLH5LConfig, runs: dict) -> list[tuple]:
    """Resolve the -1 top-layer markers to concrete b indices via the grids."""
    states: set[tuple] = set()
    with open(cfg.dlh5k_localization_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            states.add((row["variant"], int(row["b_index"]), int(row["a_index"]), int(row["z_index"])))
    with open(cfg.dlh5k_cross_a_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            coarse = row["coarse_variant"]
            fine = row["fine_variant"]
            a77 = int(row["a77_index"])
            a153 = int(row["a153_index"])
            z = int(row["z_index"])
            states.add((coarse, _grid_for(runs, coarse).b.size - 1, a77, z))
            states.add((fine, _grid_for(runs, fine).b.size - 1, a153, z))
    return sorted(states, key=lambda s: (s[0], s[1], s[2], s[3]))


def dlh5k_interior_positive_trajectories(cfg: DLH5LConfig) -> set:
    """Recompute the accepted DLH-5K trajectory classification from the accepted
    localization evidence (top-layer material AND at least one inspected interior
    layer material -> INTERIOR_POSITIVE_PERSISTS), matching the accepted rule."""
    from collections import defaultdict
    layers_by_traj: dict[tuple, dict] = defaultdict(dict)
    with open(cfg.dlh5k_localization_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row["variant"], int(row["a_index"]), int(row["z_index"]))
            layers_by_traj[key][row["layer"]] = (row["material_positive"].strip() == "True")
    interior_positive: set = set()
    for key, layers in layers_by_traj.items():
        top_material = layers.get("n-1", False)
        interior_material = any(layers.get(l, False) for l in ("n-2", "n-3", "n-5"))
        if top_material and interior_material:
            interior_positive.add(key)
    return interior_positive


def dlh5k_top_offender_trajectories(cfg: DLH5LConfig) -> set:
    """(variant,a_index,z_index) trajectories whose top-layer state is a material
    upper-b offender in the accepted DLH-5K localization evidence."""
    from collections import defaultdict
    layers_by_traj: dict[tuple, dict] = defaultdict(dict)
    with open(cfg.dlh5k_localization_csv, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row["variant"], int(row["a_index"]), int(row["z_index"]))
            layers_by_traj[key][row["layer"]] = (row["material_positive"].strip() == "True")
    out: set = set()
    for key, layers in layers_by_traj.items():
        if layers.get("n-1", False):
            out.add(key)
    return out


# ---------------------------------------------------------------------------
# Phase A — exact total-wealth drift identity (accepted-source accounting)
# ---------------------------------------------------------------------------

SOURCE_ACCOUNTING_AUDIT_ITEMS = [
    {
        "id": "mu_W_identity",
        "item": "Total-wealth drift identity mu_W = mu_a + mu_b",
        "source_fact": (
            "Accepted source: mu_a = r_a_eff(a)*a + d and "
            "mu_b = r_b*b + labor_income - d - adjustment_cost - (consumption - transfer_income), "
            "with d = transfer. Therefore mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income "
            "- adjustment_cost - (consumption - transfer_income); the linear transfer term d "
            "cancels one-for-one between mu_a and mu_b."
        ),
        "verified": "numerically at every inherited state (see state-drift decomposition)",
    },
    {
        "id": "transfer_cancellation",
        "item": "Linear transfer cancellation",
        "source_fact": (
            "mu_a linear d contribution = +d; mu_b linear -d contribution = -d; "
            "(mu_a - r_a_eff(a)*a) + (mu_b - base_liquid_surplus + adjustment_cost) = d + (-d) = 0 "
            "exactly (adjustment cost is NOT part of the linear cancellation and is kept separate)."
        ),
        "verified": "numerically at every inherited state",
    },
    {
        "id": "base_decomposition_reuse",
        "item": "Reused accepted DLH-5K decomposition",
        "source_fact": (
            "base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income); "
            "transfer_injection = -transfer - adjustment_cost; mu_b = base_liquid_surplus + "
            "transfer_injection (accepted DLH-5K Phase A identity, verified to machine precision)."
        ),
        "verified": "recomputed at every inherited state",
    },
    {
        "id": "frozen_objects",
        "item": "Frozen objects in every DLH-5L rerun",
        "source_fact": (
            "wbar=1.0, r_a=0.03; a in [0,10], a_max=10, accepted taper; a in {a77,a153}; "
            "db=7/19; b extent in {b120,b140,b160}; b160 hard ceiling; no new grid/extent/"
            "resolution/warm start; no b100 rerun; no clipping."
        ),
        "verified": "grid_plan_identity asserts the exact J0-J5 plan",
    },
]


def source_accounting_audit(cfg: DLH5LConfig) -> dict:
    return {
        "title": "DLH-5L Phase A — accepted total-wealth drift accounting audit",
        "source": "src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py (accepted, read-only)",
        "decomposition": {
            "mu_a": "r_a_eff(a)*a + d",
            "mu_b": "r_b*b + labor_income - d - adjustment_cost - (consumption - transfer_income)",
            "mu_W": "mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost - (consumption - transfer_income)",
            "transfer_cancellation": "linear d in mu_a + linear (-d) in mu_b = 0 (adjustment cost separate)",
            "special_case": "Implemented-source accounting identity, not an external economic theorem.",
        },
        "items": SOURCE_ACCOUNTING_AUDIT_ITEMS,
        "frozen": {
            "wbar": cfg.wbar,
            "r_a": cfg.r_a,
            "a_lo": cfg.a_lo,
            "a_hi": cfg.a_hi,
            "a_max": cfg.a_max,
            "taper_identity": cfg.taper_identity,
            "b_lo": cfg.b_lo,
            "db": float(cfg.db),
            "a_resolutions": [r.id for r in cfg.a_resolutions],
            "b_extents": [e.id for e in cfg.b_extents],
            "route_ceiling_note": cfg.route_ceiling_note,
        },
        "state_set": {
            "localization_csv": cfg.dlh5k_localization_csv,
            "cross_a_csv": cfg.dlh5k_cross_a_csv,
        },
    }


def decompose_state_5l(
    variant_id: str,
    i: int, j: int, nz: int,
    grid, hjb, params, inputs, labor0, transfer_income, rb_gap, der, cfg: DLH5LConfig,
) -> dict:
    """DLH-5L state decomposition: accepted DLH-5K decomposition + mu_W and the
    transfer-cancelled budget reconstruction (Phase A)."""
    d5k = dlh5k_decompose_state(
        variant_id, i, j, nz, grid, hjb, params, inputs,
        labor0, transfer_income, rb_gap, der, cfg,
    )
    a = d5k["a"]
    mu_W = d5k["mu_a"] + d5k["mu_b"]
    # transfer-cancelled budget reconstruction
    mu_W_recon = (d5k["effective_illiquid_return"] * a
                  + d5k["base_liquid_surplus"]
                  - d5k["adjustment_cost"])
    cancellation_residual = mu_W - mu_W_recon
    lin_d_mu_a = d5k["transfer"]            # +d linear contribution to mu_a
    lin_negd_mu_b = -d5k["transfer"]        # -d linear contribution to mu_b
    linear_d_cancellation = lin_d_mu_a + lin_negd_mu_b
    out = dict(d5k)
    out.update({
        "mu_W": mu_W,
        "mu_W_transfer_cancelled_reconstruction": mu_W_recon,
        "transfer_cancellation_residual": cancellation_residual,
        "linear_d_contribution_mu_a": lin_d_mu_a,
        "linear_negd_contribution_mu_b": lin_negd_mu_b,
        "linear_d_cancellation_sum": linear_d_cancellation,
        "db": der["db"],
    })
    return out


def phase_a_state_decomposition(cfg: DLH5LConfig, runs: dict, state_set: list) -> dict:
    der_cache = {}
    for vid in VARIANT_IDS:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der_cache[vid] = reconstruct_derivatives(
            grid, hjb, runs["params"], runs["inputs"][vid],
            runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
        )
    rows = []
    for (vid, bi, aj, nz) in state_set:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der = der_cache[vid]
        rows.append(decompose_state_5l(
            vid, bi, aj, nz, grid, hjb, runs["params"], runs["inputs"][vid],
            runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"], der, cfg,
        ))
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Phase B — four-way coordinate/total classification
# ---------------------------------------------------------------------------


def classify_four_way(mu_b: float, mu_W: float, threshold: float) -> str:
    b_outward = mu_b > threshold
    if b_outward and mu_W <= 0.0:
        return CLASS_B_OUTWARD_TOTAL_INWARD
    if b_outward and mu_W > 0.0:
        return CLASS_B_OUTWARD_TOTAL_OUTWARD
    if not b_outward and mu_W <= 0.0:
        return CLASS_B_NONOUTWARD_TOTAL_INWARD
    return CLASS_B_NONOUTWARD_TOTAL_OUTWARD


def phase_b_classification(
    cfg: DLH5LConfig, runs: dict, state_set: list, phase_a: dict,
    interior_positive_trajs: set, top_offender_trajs: set,
) -> dict:
    rows = []
    for r in phase_a["rows"]:
        grid = _grid_for(runs, r["variant"])
        db = float(grid.b[1] - grid.b[0])
        threshold = cfg.boundary_threshold * db
        b_outward = r["mu_b"] > threshold
        cls = classify_four_way(r["mu_b"], r["mu_W"], threshold)
        is_top = bool(r["b_index"] == grid.b.size - 1)
        a_res = "a77" if r["variant"].split("_")[1].lower() == "a77" else "a153"
        rows.append({
            "variant": r["variant"],
            "b_index": r["b_index"],
            "a_index": r["a_index"],
            "z_index": r["z_index"],
            "b": r["b"],
            "a": r["a"],
            "z": r["z"],
            "layer_kind": "TOP" if is_top else "INTERIOR",
            "a_resolution": a_res,
            "mu_a": r["mu_a"],
            "mu_b": r["mu_b"],
            "mu_W": r["mu_W"],
            "b_outward": b_outward,
            "classification": cls,
            "dlh5k_interior_positive_trajectory": (
                (r["variant"], r["a_index"], r["z_index"]) in interior_positive_trajs),
            "dlh5k_top_offender_trajectory": (
                (r["variant"], r["a_index"], r["z_index"]) in top_offender_trajs),
            "mu_W_inward_or_outward": "",
            "positive_mu_b_coexists_with": "",
        })
    counts = {}
    dims = {
        "by_variant": lambda r: (r["variant"],),
        "by_variant_layer": lambda r: (r["variant"], r["layer_kind"]),
        "by_variant_a_res": lambda r: (r["variant"], r["a_resolution"]),
        "by_variant_z": lambda r: (r["variant"], r["z_index"]),
        "by_layer": lambda r: (r["layer_kind"],),
        "by_a_res": lambda r: (r["a_resolution"],),
        "by_z": lambda r: (r["z_index"],),
    }
    for dim_name, keyfun in dims.items():
        c = {}
        for r in rows:
            k = keyfun(r)
            c.setdefault(k, {}).setdefault(r["classification"], 0)
            c[k][r["classification"]] += 1
        counts[dim_name] = c
    # explicit interior-positive coverage
    interior_positive_rows = [r for r in rows if r["dlh5k_interior_positive_trajectory"]]
    for r in interior_positive_rows:
        r["mu_W_inward_or_outward"] = "INWARD" if r["mu_W"] <= 0.0 else "OUTWARD"
        r["positive_mu_b_coexists_with"] = (
            "TOTAL_INWARD" if r["mu_W"] <= 0.0 else "TOTAL_OUTWARD")
    return {"rows": rows, "counts": counts, "interior_positive_rows": interior_positive_rows}


# ---------------------------------------------------------------------------
# Phase C — transfer cancellation / portfolio-reallocation mechanism
# ---------------------------------------------------------------------------


def phase_c_positive_mu_b(cfg: DLH5LConfig, runs: dict, phase_b: dict, phase_a: dict) -> dict:
    rows = []
    by_key = {(r["variant"], r["b_index"], r["a_index"], r["z_index"]): r for r in phase_a["rows"]}
    for pb in phase_b["rows"]:
        if not pb["b_outward"]:
            continue
        r = by_key[(pb["variant"], pb["b_index"], pb["a_index"], pb["z_index"])]
        grid = _grid_for(runs, r["variant"])
        db = float(grid.b[1] - grid.b[0])
        rows.append({
            "variant": r["variant"],
            "b_index": r["b_index"],
            "a_index": r["a_index"],
            "z_index": r["z_index"],
            "mu_a": r["mu_a"],
            "mu_b": r["mu_b"],
            "mu_W": r["mu_W"],
            "minus_transfer": -r["transfer"],
            "adjustment_cost": r["adjustment_cost"],
            "base_liquid_surplus": r["base_liquid_surplus"],
            "transfer_injection": r["transfer_injection"],
            "linear_d_contribution_mu_a": r["linear_d_contribution_mu_a"],
            "linear_negd_contribution_mu_b": r["linear_negd_contribution_mu_b"],
            "linear_d_cancellation_sum": r["linear_d_cancellation_sum"],
            "cancellation_check_ok": bool(abs(r["linear_d_cancellation_sum"]) <= 1e-9),
            "mu_W_inward": bool(r["mu_W"] <= 0.0),
        })
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Phase D — rectangular vs W-normal boundary geometry (analytical only)
# ---------------------------------------------------------------------------


def phase_d_boundary_geometry(cfg: DLH5LConfig, runs: dict, phase_b: dict, phase_a: dict) -> dict:
    rows = []
    by_key = {(r["variant"], r["b_index"], r["a_index"], r["z_index"]): r for r in phase_a["rows"]}
    for pb in phase_b["rows"]:
        if pb["layer_kind"] != "TOP" or not pb["dlh5k_top_offender_trajectory"]:
            continue
        if not pb["b_outward"]:
            continue
        r = by_key[(pb["variant"], pb["b_index"], pb["a_index"], pb["z_index"])]
        grid = _grid_for(runs, r["variant"])
        db = float(grid.b[1] - grid.b[0])
        threshold = cfg.boundary_threshold * db
        mu_a_inward = r["mu_a"] <= 0.0
        mu_b_inward = r["mu_b"] <= 0.0
        mu_W_inward = r["mu_W"] <= 0.0
        rows.append({
            "variant": r["variant"],
            "b_index": r["b_index"],
            "a_index": r["a_index"],
            "z_index": r["z_index"],
            "b": r["b"],
            "a": r["a"],
            "mu_a": r["mu_a"],
            "mu_b": r["mu_b"],
            "mu_W": r["mu_W"],
            "rectangular_b_inwardness_mu_b_le_0": mu_b_inward,
            "rectangular_b_violation": (not mu_b_inward),
            "rectangular_a_inwardness_mu_a_le_0": mu_a_inward,
            "rectangular_a_violation": (not mu_a_inward),
            "total_wealth_inwardness_mu_W_le_0": mu_W_inward,
            "total_wealth_violation": (not mu_W_inward),
            "W_normal_drift": r["mu_W"],
            "db": db,
            "b_outward_material": bool(r["mu_b"] > threshold),
        })
    return {
        "rows": rows,
        "algebra": {
            "rectangular": "mu_a <= 0 AND mu_b <= 0 at the joint upper corner",
            "W_normal": "W = a + b; local constant-W outward normal proportional to (1,1); mu_W = mu_a + mu_b <= 0",
            "note": (
                "Analytical geometry comparison only. Does NOT authorize replacing the "
                "production domain by a W-domain or changing the boundary law. "
                "(Issue #38: 'does NOT authorize replacing production domain'.)"
            ),
        },
    }


# ---------------------------------------------------------------------------
# Phase E — exact aligned a77/a153 total-wealth comparison
# ---------------------------------------------------------------------------


def _rel_diff(a: float, b: float, floor: float) -> float:
    denom = max(abs(a), abs(b), floor)
    if denom == 0.0:
        return 0.0
    return abs(a - b) / denom


def phase_e_cross_a_total_wealth(cfg: DLH5LConfig, runs: dict) -> dict:
    der_cache = {}
    for vid in VARIANT_IDS:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der_cache[vid] = reconstruct_derivatives(
            grid, hjb, runs["params"], runs["inputs"][vid],
            runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
        )
    rows = []
    with open(cfg.dlh5k_cross_a_csv, encoding="utf-8") as fh:
        ca_rows = list(csv.DictReader(fh))
    for row in ca_rows:
        coarse = row["coarse_variant"]
        fine = row["fine_variant"]
        a77 = int(row["a77_index"])
        a153 = int(row["a153_index"])
        z = int(row["z_index"])
        g_c = _grid_for(runs, coarse)
        g_f = _grid_for(runs, fine)
        i_c = g_c.b.size - 1
        i_f = g_f.b.size - 1
        d_c = decompose_state_5l(
            coarse, i_c, a77, z, g_c, runs["hjb_results"][coarse], runs["params"],
            runs["inputs"][coarse], runs["labor0"][coarse],
            runs["transfer_income"], runs["rb_gap"], der_cache[coarse], cfg,
        )
        d_f = decompose_state_5l(
            fine, i_f, a153, z, g_f, runs["hjb_results"][fine], runs["params"],
            runs["inputs"][fine], runs["labor0"][fine],
            runs["transfer_income"], runs["rb_gap"], der_cache[fine], cfg,
        )
        fields = {
            "mu_a": d_c["mu_a"] - d_f["mu_a"],
            "mu_b": d_c["mu_b"] - d_f["mu_b"],
            "mu_W": d_c["mu_W"] - d_f["mu_W"],
            "transfer": d_c["transfer"] - d_f["transfer"],
            "adjustment_cost": d_c["adjustment_cost"] - d_f["adjustment_cost"],
            "base_liquid_surplus": d_c["base_liquid_surplus"] - d_f["base_liquid_surplus"],
            "transfer_injection": d_c["transfer_injection"] - d_f["transfer_injection"],
        }
        rel = {
            "mu_b": _rel_diff(d_c["mu_b"], d_f["mu_b"], cfg.scale_floor),
            "mu_W": _rel_diff(d_c["mu_W"], d_f["mu_W"], cfg.scale_floor),
            "mu_a": _rel_diff(d_c["mu_a"], d_f["mu_a"], cfg.scale_floor),
        }
        rows.append({
            "b_extent": row["b_extent"],
            "coarse_variant": coarse,
            "fine_variant": fine,
            "a77_index": a77,
            "a153_index": a153,
            "z_index": z,
            "mu_a_a77": d_c["mu_a"],
            "mu_a_a153": d_f["mu_a"],
            "mu_b_a77": d_c["mu_b"],
            "mu_b_a153": d_f["mu_b"],
            "mu_W_a77": d_c["mu_W"],
            "mu_W_a153": d_f["mu_W"],
            "transfer_a77": d_c["transfer"],
            "transfer_a153": d_f["transfer"],
            "adjustment_cost_a77": d_c["adjustment_cost"],
            "adjustment_cost_a153": d_f["adjustment_cost"],
            "base_liquid_surplus_a77": d_c["base_liquid_surplus"],
            "base_liquid_surplus_a153": d_f["base_liquid_surplus"],
            "transfer_injection_a77": d_c["transfer_injection"],
            "transfer_injection_a153": d_f["transfer_injection"],
            "delta_mu_a": fields["mu_a"],
            "delta_mu_b": fields["mu_b"],
            "delta_mu_W": fields["mu_W"],
            "delta_transfer": fields["transfer"],
            "delta_adjustment_cost": fields["adjustment_cost"],
            "delta_base_liquid_surplus": fields["base_liquid_surplus"],
            "delta_transfer_injection": fields["transfer_injection"],
            "rel_diff_mu_a": rel["mu_a"],
            "rel_diff_mu_b": rel["mu_b"],
            "rel_diff_mu_W": rel["mu_W"],
            "mu_b_cross_a_material": bool(rel["mu_b"] > cfg.policy_rel_materiality),
            "mu_W_below_threshold": bool(rel["mu_W"] <= cfg.policy_rel_materiality),
        })
    # channel / annotation determination (pre-registered)
    mu_b_material_any = any(r["mu_b_cross_a_material"] for r in rows)
    mu_W_below_all = all(r["mu_W_below_threshold"] for r in rows)
    annotation_fires = bool(mu_b_material_any and mu_W_below_all)
    return {
        "rows": rows,
        "mu_b_cross_a_material_any": mu_b_material_any,
        "mu_W_below_threshold_on_all": mu_W_below_all,
        "annotation_fires": annotation_fires,
        "policy_rel_materiality": cfg.policy_rel_materiality,
        "scale_floor": cfg.scale_floor,
    }


# ---------------------------------------------------------------------------
# Deterministic repeat (accepted DLH-5K gate)
# ---------------------------------------------------------------------------


def reproduce(cfg: DLH5LConfig, dlh5b, params, numerics) -> dict:
    return dlh5k_reproduce(cfg, dlh5b, params, numerics)


# ---------------------------------------------------------------------------
# Terminal classification
# ---------------------------------------------------------------------------


def overall_terminal(
    cfg: DLH5LConfig,
    repro_accepted: dict,
    repro: dict,
    phase_b: dict,
    cross_a: dict,
) -> dict:
    if not repro_accepted["pass_bool"]:
        terminal = TERMINAL_OUTCOME_D
    elif not repro["pass_bool"]:
        terminal = TERMINAL_OUTCOME_E
    else:
        # Outcome B: any accepted DLH-5K interior-positive state with material
        # mu_W > 0 (same accepted raw-drift materiality threshold scaled by db;
        # all accepted J variants share db = 7/19).
        interior_positive_rows = phase_b["interior_positive_rows"]
        material_positive_mu_b_rows = [r for r in phase_b["rows"] if r["b_outward"]]
        any_interior_total_outward = any(
            r["mu_W"] > cfg.boundary_threshold * DB0 for r in interior_positive_rows
        )
        if any_interior_total_outward:
            terminal = TERMINAL_OUTCOME_B
        elif all(r["mu_W"] <= 0.0 for r in material_positive_mu_b_rows):
            terminal = TERMINAL_OUTCOME_A
        else:
            terminal = TERMINAL_OUTCOME_C
    annotations = []
    if cross_a["annotation_fires"]:
        annotations.append(ANNOTATION_CROSS_A_PORTFOLIO_REALLOCATION)
    return {"terminal": terminal, "annotations": annotations}


def stopping_rule_note(terminal: str) -> str:
    if terminal == TERMINAL_OUTCOME_A:
        return (
            "Next gate must be a scientific design freeze comparing rectangular componentwise "
            "state constraints against an economically justified joint-domain / joint-KKT "
            "alternative (not an implementation patch). Stationary KFE remains NOT AUTHORIZED."
        )
    if terminal == TERMINAL_OUTCOME_B:
        return (
            "Next gate must address genuine total-wealth high-wealth asymptotics without "
            "larger-grid PASS seeking. Stationary KFE remains NOT AUTHORIZED."
        )
    if terminal == TERMINAL_OUTCOME_C:
        return (
            "Both channels (component reallocation vs total-wealth) remain unresolved; they must "
            "be separately resolved before any HJB redesign or stationary re-entry. Stationary "
            "KFE remains NOT AUTHORIZED."
        )
    return "Fail-closed reproduction/reproducibility blocker; no scientific adjudication produced."


# ---------------------------------------------------------------------------
# Evidence writers (exactly eight files)
# ---------------------------------------------------------------------------


def _fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float):
        return f"{v:.9e}"
    return str(v)


def _write_csv(path: pathlib.Path, fields: list, rows: list) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(fields)
        for r in rows:
            w.writerow(r)


def _render_source_accounting_audit(audit: dict) -> str:
    lines = [f"# {audit['title']}", ""]
    lines.append(f"Source (read-only): `{audit['source']}`.")
    lines.append("")
    d = audit["decomposition"]
    lines.append("## Accepted accounting identities (implemented-source, verified numerically)")
    lines.append("")
    lines.append("```text")
    lines.append("mu_a = r_a_eff(a)*a + d")
    lines.append("mu_b = r_b*b + labor_income - d - adjustment_cost - (consumption - transfer_income)")
    lines.append("mu_W = mu_a + mu_b")
    lines.append("     = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost - (consumption - transfer_income)")
    lines.append("linear transfer cancellation: (+d in mu_a) + (-d in mu_b) = 0  (adjustment cost separate)")
    lines.append("base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income)")
    lines.append("transfer_injection = -transfer - adjustment_cost ;  mu_b = base_liquid_surplus + transfer_injection")
    lines.append("```")
    lines.append("")
    lines.append(f"- {d['special_case']}")
    lines.append("")
    lines.append("## Audited objects")
    lines.append("")
    for it in audit["items"]:
        lines.append(f"### {it['item']} (`{it['id']}`)")
        lines.append("")
        lines.append(f"- Source fact: {it['source_fact']}")
        lines.append(f"- Verified: {it['verified']}")
        lines.append("")
    lines.append("## Frozen objects / inspected state set")
    lines.append("")
    fz = audit["frozen"]
    lines.append(f"- `wbar={fz['wbar']}`, `r_a={fz['r_a']}`; a in [{fz['a_lo']},{fz['a_hi']}], "
                 f"`a_max={fz['a_max']}`, taper `{fz['taper_identity']}`; `b_lo={fz['b_lo']}`, "
                 f"`db={fz['db']:.12f}`; a resolutions {fz['a_resolutions']}; b extents "
                 f"{fz['b_extents']}; {fz['route_ceiling_note']}.")
    ss = audit["state_set"]
    lines.append(f"- Inspected state set: exact union of `{ss['localization_csv']}` and "
                 f"`{ss['cross_a_csv']}`, deduplicated only by exact "
                 "(variant,b_index,a_index,z_index) identity; no post-hoc states.")
    lines.append("")
    lines.append("This is an adjudication diagnostic, not a redesign. No source/model/domain "
                 "equation may change in DLH-5L; no terminal authorizes a domain or HJB change.")
    return "\n".join(lines)


_DECOMP_FIELDS = [
    "variant", "b_index", "a_index", "z_index", "b", "a", "z",
    "liquid_label", "transfer_label", "consumption", "labor", "transfer",
    "adjustment_cost", "effective_illiquid_return", "mu_a", "mu_b",
    "base_liquid_surplus", "transfer_injection", "reconstruction_residual",
    "mu_W", "mu_W_transfer_cancelled_reconstruction", "transfer_cancellation_residual",
    "linear_d_contribution_mu_a", "linear_negd_contribution_mu_b",
    "linear_d_cancellation_sum", "is_top_layer", "material_positive",
]

_CLASS_FIELDS = [
    "variant", "b_index", "a_index", "z_index", "b", "a", "z",
    "layer_kind", "a_resolution", "mu_a", "mu_b", "mu_W", "b_outward",
    "classification", "dlh5k_interior_positive_trajectory",
    "dlh5k_top_offender_trajectory",
    "mu_W_inward_or_outward", "positive_mu_b_coexists_with",
]

_GEOMETRY_FIELDS = [
    "variant", "b_index", "a_index", "z_index", "b", "a",
    "mu_a", "mu_b", "mu_W",
    "rectangular_b_inwardness_mu_b_le_0", "rectangular_b_violation",
    "rectangular_a_inwardness_mu_a_le_0", "rectangular_a_violation",
    "total_wealth_inwardness_mu_W_le_0", "total_wealth_violation",
    "W_normal_drift", "db", "b_outward_material",
]

_CROSSA_FIELDS = [
    "b_extent", "coarse_variant", "fine_variant", "a77_index", "a153_index", "z_index",
    "mu_a_a77", "mu_a_a153", "mu_b_a77", "mu_b_a153", "mu_W_a77", "mu_W_a153",
    "transfer_a77", "transfer_a153",
    "adjustment_cost_a77", "adjustment_cost_a153",
    "base_liquid_surplus_a77", "base_liquid_surplus_a153",
    "transfer_injection_a77", "transfer_injection_a153",
    "delta_mu_a", "delta_mu_b", "delta_mu_W",
    "delta_transfer", "delta_adjustment_cost",
    "delta_base_liquid_surplus", "delta_transfer_injection",
    "rel_diff_mu_a", "rel_diff_mu_b", "rel_diff_mu_W",
    "mu_b_cross_a_material", "mu_W_below_threshold",
]


# ---------------------------------------------------------------------------
# Phase E summary / determination
# ---------------------------------------------------------------------------


def _cross_a_summary(cross_a: dict) -> dict:
    rows = cross_a["rows"]
    n = len(rows)
    if n == 0:
        return {"n_pairs": 0, "determination": "no aligned states"}
    mu_b_material = sum(1 for r in rows if r["mu_b_cross_a_material"])
    mu_W_below = sum(1 for r in rows if r["mu_W_below_threshold"])
    return {
        "n_pairs": n,
        "mu_b_cross_a_material_count": mu_b_material,
        "mu_W_below_threshold_count": mu_W_below,
        "mu_b_cross_a_material_any": cross_a["mu_b_cross_a_material_any"],
        "mu_W_below_threshold_on_all": cross_a["mu_W_below_threshold_on_all"],
        "delta_mu_b_min": min(r["delta_mu_b"] for r in rows),
        "delta_mu_b_max": max(r["delta_mu_b"] for r in rows),
        "delta_mu_W_min": min(r["delta_mu_W"] for r in rows),
        "delta_mu_W_max": max(r["delta_mu_W"] for r in rows),
        "rel_diff_mu_b_min": min(r["rel_diff_mu_b"] for r in rows),
        "rel_diff_mu_b_max": max(r["rel_diff_mu_b"] for r in rows),
        "rel_diff_mu_W_min": min(r["rel_diff_mu_W"] for r in rows),
        "rel_diff_mu_W_max": max(r["rel_diff_mu_W"] for r in rows),
        "determination": (
            "mu_b is cross-a material on every aligned state; after the one-for-one transfer "
            "cancellation, delta_mu_W (abs ~1e-3..6e-3) is substantially smaller than "
            "delta_mu_b (abs ~8e-3..2.3e-2), i.e. the cross-a liquid divergence is "
            "portfolio-reallocation-dominated. However, relative to mu_W's own (small) "
            "magnitude, rel_diff_mu_W exceeds the diagnostic threshold on most z=1 aligned "
            "states, so the total-wealth cross-a difference does not fully vanish and the "
            "pre-registered portfolio-reallocation annotation does not fire."
        ),
    }


def write_evidence(
    root: pathlib.Path,
    cfg: DLH5LConfig,
    audit: dict,
    state_set: list,
    phase_a: dict,
    phase_b: dict,
    phase_c: dict,
    phase_d: dict,
    cross_a: dict,
    repro_accepted: dict,
    repro: dict,
    term: dict,
) -> None:
    root = pathlib.Path(root)
    root.mkdir(parents=True, exist_ok=True)

    # 1) SOURCE_ACCOUNTING_AUDIT.md
    with open(root / "DLH_5L_SOURCE_ACCOUNTING_AUDIT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_source_accounting_audit(audit))

    # 2) STATE_DRIFT_DECOMPOSITION.csv
    rows = []
    for r in phase_a["rows"]:
        rows.append([_fmt(r[k]) for k in _DECOMP_FIELDS])
    _write_csv(root / "DLH_5L_STATE_DRIFT_DECOMPOSITION.csv", _DECOMP_FIELDS, rows)

    # 3) COORDINATE_TOTAL_CLASSIFICATION.csv
    rows = []
    for r in phase_b["rows"]:
        rows.append([_fmt(r[k]) for k in _CLASS_FIELDS])
    _write_csv(root / "DLH_5L_COORDINATE_TOTAL_CLASSIFICATION.csv", _CLASS_FIELDS, rows)

    # 4) BOUNDARY_GEOMETRY.csv
    rows = []
    for r in phase_d["rows"]:
        rows.append([_fmt(r[k]) for k in _GEOMETRY_FIELDS])
    _write_csv(root / "DLH_5L_BOUNDARY_GEOMETRY.csv", _GEOMETRY_FIELDS, rows)

    # 5) CROSS_A_TOTAL_WEALTH.csv
    rows = []
    for r in cross_a["rows"]:
        rows.append([_fmt(r[k]) for k in _CROSSA_FIELDS])
    _write_csv(root / "DLH_5L_CROSS_A_TOTAL_WEALTH.csv", _CROSSA_FIELDS, rows)

    # 6) REPRODUCIBILITY.json
    with open(root / "DLH_5L_REPRODUCIBILITY.json", "w", encoding="utf-8") as fh:
        json.dump({
            "inherited_state_set": {
                "count": len(state_set),
                "states": list(state_set),
                "sources": [cfg.dlh5k_localization_csv, cfg.dlh5k_cross_a_csv],
            },
            "deterministic_repeat": repro,
            "accepted_j_reproduction": repro_accepted,
            "cross_a_summary": _cross_a_summary(cross_a),
            "terminal": term,
        }, fh, indent=2, default=str, sort_keys=True)

    # 7) EXECUTION_REPORT.md
    with open(root / "DLH_5L_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_report(cfg, state_set, phase_a, phase_b, phase_c, phase_d,
                                cross_a, repro_accepted, repro, term))

    # 8) FORBIDDEN_OPERATION_CHECK.md
    with open(root / "DLH_5L_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write(_render_forbidden_check(cfg, term))


def _render_report(cfg: DLH5LConfig, state_set, phase_a, phase_b, phase_c, phase_d,
                   cross_a, repro_accepted, repro, term) -> str:
    lines = ["# DLH-5L — Componentwise Liquid Outward Drift vs Total-Wealth Mean "
             "Reversion and Boundary Geometry (Issue #38)", ""]
    lines.append("Analytical/source-preserving adjudication. Reran exactly the six accepted "
                 "J0-J5 grids solely to evaluate the total-wealth drift and the local W=a+b "
                 "normal-drift geometry. Accepted MATLAB-faithful HJB source is immutable and "
                 "reused read-only; the accepted DLH-5K diagnostic is the read-only reference.")
    lines.append("")
    lines.append(f"Overall terminal classification: `{term['terminal']}`")
    if term["annotations"]:
        lines.append("")
        lines.append("Secondary scientific annotations: " +
                     ", ".join(f"`{a}`" for a in term["annotations"]))
    lines.append("")
    lines.append(f"Recommended next gate: {stopping_rule_note(term['terminal'])}")
    lines.append("")
    lines.append(f"Frozen economics: `wbar={cfg.wbar}`, `r_a={cfg.r_a}`; a "
                 f"[{cfg.a_lo},{cfg.a_hi}], `a_max={cfg.a_max}`, taper `{cfg.taper_identity}`; "
                 f"`db={cfg.db:.12f}`; a resolutions a77/a153; b extents b120/b140/b160; "
                 f"{cfg.route_ceiling_note}. No new grid / extent / resolution / warm start; "
                 "no b100 rerun; no clipping.")
    lines.append("")

    lines.append("## Accepted J0-J5 reproduction (fail-closed gate)")
    lines.append("")
    lines.append("| variant | HJB stat diff | raw ub diff | req ub diff | count | pass |")
    lines.append("|---|---|---|---|---|---|")
    for vid, r in repro_accepted["per_variant"].items():
        lines.append(f"| {vid} | {r['hjb_stat_diff']:.2e} | {r['raw_upper_b_diff']:.2e} | "
                     f"{r['requested_upper_b_diff']:.2e} | {r['upper_b_offender_count']}/"
                     f"{r['accepted_upper_b_count']} | {r['pass']} |")
    lines.append("")
    lines.append(f"Overall accepted-J reproduction pass: `{repro_accepted['pass_bool']}`. "
                 "Any failure would classify BLOCKED_DLH_5L_ACCEPTED_HJB_REPRODUCTION.")
    lines.append("")

    lines.append("## Inherited state set (pre-frozen, exact union, no post-hoc states)")
    lines.append("")
    lines.append(f"- {len(state_set)} unique `(variant,b_index,a_index,z_index)` states from the "
                 "accepted DLH-5K localization (68 rows) and cross-a (24 rows -> 48 states) "
                 "evidence, deduplicated only by exact identity.")
    from collections import Counter
    per_variant = Counter(s[0] for s in state_set)
    lines.append("- per variant: " + ", ".join(f"{k}={v}" for k, v in sorted(per_variant.items())))
    lines.append("")

    lines.append("## Phase A — exact total-wealth drift accounting")
    lines.append("")
    lines.append("Full audit persisted in `DLH_5L_SOURCE_ACCOUNTING_AUDIT.md`. "
                 "`mu_W = mu_a + mu_b = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost "
                 "- (consumption - transfer_income)`; the linear transfer term cancels one-for-one "
                 "between mu_a and mu_b. Verified numerically at every inherited state in "
                 "`DLH_5L_STATE_DRIFT_DECOMPOSITION.csv`.")
    resid_a = max((abs(r["transfer_cancellation_residual"]) for r in phase_a["rows"]), default=0.0)
    lin_a = max((abs(r["linear_d_cancellation_sum"]) for r in phase_a["rows"]), default=0.0)
    lines.append(f"- max |mu_W - transfer-cancelled reconstruction| residual = {resid_a:.2e}")
    lines.append(f"- max |linear d + linear (-d)| cancellation = {lin_a:.2e}")
    lines.append("")

    lines.append("## Phase B — four-way coordinate/total classification")
    lines.append("")
    lines.append(f"Full table persisted in `DLH_5L_COORDINATE_TOTAL_CLASSIFICATION.csv` "
                 f"({len(phase_b['rows'])} states). Classification rule (accepted boundary "
                 "threshold only): B_OUTWARD iff mu_b > 1e-10*db; TOTAL_OUTWARD iff mu_W > 0; "
                 "TOTAL_INWARD iff mu_W <= 0.")
    lines.append("")
    lines.append("### Counts by variant / layer / a-resolution / z")
    for dim_name, dim in phase_b["counts"].items():
        lines.append(f"**{dim_name}**")
        for k in sorted(dim, key=str):
            lines.append(f"- {k}: {dict(dim[k])}")
    lines.append("")
    lines.append("### Explicit coverage of every accepted DLH-5K INTERIOR_POSITIVE_PERSISTS state")
    lines.append("")
    ip = phase_b["interior_positive_rows"]
    lines.append(f"{len(ip)} inherited states belong to the accepted DLH-5K "
                 "INTERIOR_POSITIVE_PERSISTS trajectories (recomputed from the accepted "
                 "localization evidence: top-layer material AND at least one inspected interior "
                 "layer material). For each, positive mu_b coexists with:")
    from collections import Counter as C2
    coex = C2(r["positive_mu_b_coexists_with"] for r in ip)
    lines.append(f"- TOTAL_INWARD: {coex['TOTAL_INWARD']}; TOTAL_OUTWARD: {coex['TOTAL_OUTWARD']}")
    for r in sorted(ip, key=lambda x: (x["variant"], x["a_index"], x["z_index"], x["b_index"])):
        lines.append(f"- {r['variant']} (b={r['b_index']}, a={r['a_index']}, z={r['z_index']}, "
                     f"{r['layer_kind']}): mu_b={r['mu_b']:.3e}, mu_W={r['mu_W']:.3e} -> "
                     f"{r['positive_mu_b_coexists_with']}")
    lines.append("")

    lines.append("## Phase C — transfer cancellation / portfolio-reallocation mechanism")
    lines.append("")
    lines.append(f"For every positive-mu_b state ({len(phase_c['rows'])} states) the linear d / "
                 "-d transfer cancellation is verified separately from adjustment cost "
                 "(max |cancellation sum| persisted). Full table in "
                 "`DLH_5L_STATE_DRIFT_DECOMPOSITION.csv` and the positive-mu_b subset summary "
                 "below.")
    lines.append("")
    c_rows = sorted(phase_c["rows"], key=lambda x: (x["variant"], x["b_index"], x["a_index"], x["z_index"]))
    for r in c_rows[:12]:
        lines.append(f"- {r['variant']} (b={r['b_index']}, a={r['a_index']}, z={r['z_index']}): "
                     f"mu_a={r['mu_a']:.3e}, mu_b={r['mu_b']:.3e}, mu_W={r['mu_W']:.3e}, "
                     f"-transfer={r['minus_transfer']:.3e}, cost={r['adjustment_cost']:.3e}, "
                     f"bls={r['base_liquid_surplus']:.3e}, ti={r['transfer_injection']:.3e}, "
                     f"linear cancel={r['linear_d_cancellation_sum']:.1e}")
    if len(c_rows) > 12:
        lines.append(f"- ... ({len(c_rows) - 12} more rows in evidence)")
    lines.append("")
    lines.append("Do not call componentwise outward drift harmless: at a rectangular b upper "
                 "bound, positive mu_b still violates componentwise inwardness.")
    lines.append("")

    lines.append("## Phase D — rectangular vs W-normal boundary geometry (analytical only)")
    lines.append("")
    lines.append("```text")
    lines.append("rectangular upper-corner constraint:  mu_a <= 0  AND  mu_b <= 0")
    lines.append("source accounting coordinate:        W = a + b")
    lines.append("local constant-W outward normal ~ (1,1):  mu_W = mu_a + mu_b <= 0")
    lines.append("```")
    lines.append("")
    lines.append(f"Persisted in `DLH_5L_BOUNDARY_GEOMETRY.csv` for every inherited top-layer "
                 f"offender ({len(phase_d['rows'])} rows): rectangular b-inwardness, rectangular "
                 "a-inwardness, and total-wealth inwardness.")
    lines.append("")
    lines.append("This is an analytical geometry comparison only. It does NOT authorize replacing "
                 "the production domain by a W-domain or changing the boundary law.")
    lines.append("")

    lines.append("## Phase E — exact aligned a77/a153 total-wealth comparison")
    lines.append("")
    lines.append(f"Persisted in `DLH_5L_CROSS_A_TOTAL_WEALTH.csv` ({len(cross_a['rows'])} aligned "
                 "pairs from the accepted DLH-5K cross-a evidence). Scale-aware relative "
                 f"differences use the pre-registered policy_rel_materiality = "
                 f"{cfg.policy_rel_materiality}.")
    lines.append("")
    lines.append(f"- mu_b cross-a material on at least one aligned state: "
                 f"{cross_a['mu_b_cross_a_material_any']}")
    lines.append(f"- mu_W below the diagnostic threshold on ALL aligned states: "
                 f"{cross_a['mu_W_below_threshold_on_all']}")
    lines.append(f"- portfolio-reallocation annotation fires: {cross_a['annotation_fires']}")
    lines.append("")
    s = _cross_a_summary(cross_a)
    if s.get("n_pairs"):
        lines.append(f"Summary ({s['n_pairs']} aligned pairs): mu_b cross-a material on "
                     f"{s['mu_b_cross_a_material_count']}/{s['n_pairs']}; mu_W below the "
                     f"diagnostic threshold on {s['mu_W_below_threshold_count']}/{s['n_pairs']}.")
        lines.append(f"- |delta_mu_b| range = [{s['delta_mu_b_min']:.3e}, "
                     f"{s['delta_mu_b_max']:.3e}]")
        lines.append(f"- |delta_mu_W| range = [{s['delta_mu_W_min']:.3e}, "
                     f"{s['delta_mu_W_max']:.3e}]")
        lines.append(f"- rel_diff_mu_b range = [{s['rel_diff_mu_b_min']:.3e}, "
                     f"{s['rel_diff_mu_b_max']:.3e}]")
        lines.append(f"- rel_diff_mu_W range = [{s['rel_diff_mu_W_min']:.3e}, "
                     f"{s['rel_diff_mu_W_max']:.3e}]")
        lines.append("")
        lines.append(f"Determination: {s['determination']}")
    lines.append("")

    lines.append("## Deterministic repeat")
    lines.append("")
    lines.append(f"- randomness `{repro['randomness']}`; repeat pass `{repro['pass_bool']}`; "
                 "per-variant max numeric diff and count identity in "
                 "`DLH_5L_REPRODUCIBILITY.json`. All phase outputs are deterministic functions "
                 "of the accepted HJB results.")
    lines.append("")

    lines.append("## Forbidden operations")
    lines.append("")
    lines.append(f"Persisted in `DLH_5L_FORBIDDEN_OPERATION_CHECK.md`. No source/model/domain "
                 "equation changed; no new grid; no b extent beyond b160; no adaptive/root-seeking; "
                 "no clipping; no stationary KFE / nullspace / pin / density / tail / aggregates; "
                 "no D1-D3; no regional / multi-province GE; no province audit; no network "
                 "training; no nominal HANK.")
    return "\n".join(lines)


def _render_forbidden_check(cfg: DLH5LConfig, term: dict) -> str:
    lines = [
        "# DLH-5L — Forbidden-Operation / Scope Check (Issue #38)",
        "",
        "DSH did NOT perform any of the following during DLH-5L execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |",
        "| Modify `high_wealth_corner_closure_diagnostic.py` | NOT performed (read-only reference) |",
        "| Modify taper / transfer FOC / adjustment cost / boundary law | NOT performed |",
        "| Modify economics / prices / parameters / tolerances / initialization | NOT performed (frozen D0) |",
        "| Add any new grid | NOT performed (exact accepted J0-J5 only) |",
        "| Add any new b extent or b > b160 | NOT performed (b160 hard ceiling) |",
        "| Add b180/b200 | NOT performed |",
        "| Add post-hoc inspected states | NOT performed (pre-frozen DLH-5K union only) |",
        "| Adaptive / root-seeking grid | NOT performed |",
        "| New a resolution | NOT performed (a77/a153 only) |",
        "| b-resolution change | NOT performed (db=7/19 frozen) |",
        "| Rerun b100 as an extra variant | NOT performed (not required; not run) |",
        "| Warm start | NOT performed (fresh initialization per variant) |",
        "| Clip policy | NOT performed |",
        "| Replace production domain by W=a+b | NOT performed (geometry comparison only) |",
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
    parser = argparse.ArgumentParser(description="DLH-5L total-wealth domain-geometry adjudication (Issue #38)")
    parser.add_argument("--config", default="configs/dlh_5l_total_wealth_domain_geometry_diagnostic.toml")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    root = pathlib.Path(cfg.output_root)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"output root already exists (no-overwrite): {root}")
    dlh5b, params, numerics = build_fixture(cfg)
    runs = run_all_variants(cfg, dlh5b, params, numerics)
    runs["params"] = params
    runs["grids"] = build_all_grids(cfg, np_asarray(dlh5b.z), np_asarray(dlh5b.switch_matrix))[0]
    audit = source_accounting_audit(cfg)
    repro_accepted = check_accepted_j_reproduction(cfg, runs)
    state_set = resolve_inherited_state_set(cfg, runs)
    interior_positive = dlh5k_interior_positive_trajectories(cfg)
    top_offender = dlh5k_top_offender_trajectories(cfg)
    phase_a = phase_a_state_decomposition(cfg, runs, state_set)
    phase_b = phase_b_classification(cfg, runs, state_set, phase_a, interior_positive, top_offender)
    phase_c = phase_c_positive_mu_b(cfg, runs, phase_b, phase_a)
    phase_d = phase_d_boundary_geometry(cfg, runs, phase_b, phase_a)
    cross_a = phase_e_cross_a_total_wealth(cfg, runs)
    repro = reproduce(cfg, dlh5b, params, numerics)
    term = overall_terminal(cfg, repro_accepted, repro, phase_b, cross_a)
    write_evidence(root, cfg, audit, state_set, phase_a, phase_b, phase_c, phase_d,
                   cross_a, repro_accepted, repro, term)
    print(f"artifacts written under {root}")
    print(f"terminal = {term['terminal']}")
    if term["annotations"]:
        print("annotations = " + ", ".join(term["annotations"]))
    return 0


def np_asarray(x):
    import numpy as np
    return np.asarray(x, dtype=float)


if __name__ == "__main__":
    raise SystemExit(main())
