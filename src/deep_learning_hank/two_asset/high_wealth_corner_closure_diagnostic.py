"""DLH-5K (Issue #37) — high-wealth liquid drift vs joint upper-corner HJB closure.

Analytical/source-preserving adjudication. Reruns exactly the six accepted DLH-5J
grids (J0-J5) solely to extract local high-wealth diagnostics; no new grid, no
new b extent (b160 hard ceiling), no new a resolution, no b-resolution change,
no b100 rerun, no warm start. Every rerun must reproduce the accepted DLH-5J HJB
statistics and boundary maxima/counts within the frozen comparison tolerance or
fail closed (Outcome D).

Phases:
- Phase A: exact accepted source-law audit (upper-b derivative closure; liquid
  resource/consumption branch; transfer candidate construction; upper-a
  transfer-direction restriction; upper-b transfer-direction override;
  adjustment cost; final mu_a/mu_b; requested-rate conversion) and the drift
  decomposition ``mu_b = base_liquid_surplus + transfer_injection`` with
  ``base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income)``
  and ``transfer_injection = -transfer - adjustment_cost``. When the liquid
  zero-drift ("0") branch holds, ``base_liquid_surplus = 0`` so
  ``mu_b = -transfer - adjustment_cost`` (an implemented-source identity, not an
  economic theorem).
- Phase B: complete upper-b offender mechanism decomposition (indices/physical
  state, labels, controls, transfer, adjustment cost, effective illiquid
  return, mu_a/mu_b, base_liquid_surplus, transfer_injection, reconstruction
  residual, V_b boundary/backward derivatives, available V_a derivatives,
  V_a/V_b - 1, selected transfer candidate) using only derivatives recoverable
  from the accepted finite grid and converged value function.
- Phase C: boundary-vs-interior localization at n-1/n-2/n-3/n-5 b layers with
  factual classification BOUNDARY_ONLY_POSITIVE / INTERIOR_POSITIVE_PERSISTS /
  MIXED_OR_LABEL_TRANSITION (accepted boundary threshold only).
- Phase D: joint upper-corner feasibility algebra for d=-x<0 under
  chi(d,a)=chi_0*|d|+0.5*chi_1*d^2/max(a,a_bar) with upper-a inward mu_a<=0 and
  upper-b inward mu_b<=0, general base_liquid_surplus first, simplified only
  under the empirically verified base_liquid_surplus≈0 branch; numerically
  verified against direct drifts at the actual offender states.
- Phase E: cross-a mechanism comparison at b120/b140/b160 (exact aligned a77 vs
  every-second a153 high-wealth nodes); channel attribution
  (transfer/derivative vs base-liquid-surplus vs both).

Policy-only: stationary fields use
``NOT_AUTHORIZED__DLH_5K_POLICY_ONLY_HIGH_WEALTH_CORNER_CLOSURE_DIAGNOSTIC``.
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
from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (
    adjustment_cost,
    matlab_faithful_illiquid_return,
    transfer_candidate,
)
from deep_learning_hank.regional.two_region_fixed_point import (
    build_fixture as build_dlh5b_fixture,
    household_initial_condition,
    load_config as load_dlh5b_config,
)

# ---------------------------------------------------------------------------
# Terminal classifications / markers (Issue #37 section 10)
# ---------------------------------------------------------------------------

TERMINAL_OUTCOME_A = "DLH_5K_UPPER_B_OUTWARD_DRIFT_BOUNDARY_CORNER_TRANSFER_CLOSURE_DOMINATED__SCIENTIFIC_REDESIGN_REVIEW_REQUIRED"
TERMINAL_OUTCOME_B = "DLH_5K_HIGH_WEALTH_INTERIOR_OUTWARD_DRIFT_PERSISTS__ECONOMIC_MEAN_REVERSION_NOT_ESTABLISHED__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_OUTCOME_C = "DLH_5K_MIXED_HIGH_WEALTH_AND_BOUNDARY_CLOSURE_MECHANISM__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_OUTCOME_D = "BLOCKED_DLH_5K_ACCEPTED_HJB_REPRODUCTION"
TERMINAL_OUTCOME_E = "BLOCKED_DLH_5K_REPRODUCIBILITY"
ANNOTATION_CROSS_A_TRANSFER_CHANNEL = (
    "DLH_5K_CROSS_A_DIVERGENCE_PRIMARILY_TRANSFER_DERIVATIVE_CHANNEL__SCIENTIFIC_REVIEW_REQUIRED"
)
NOT_AUTHORIZED_MARKER = "NOT_AUTHORIZED__DLH_5K_POLICY_ONLY_HIGH_WEALTH_CORNER_CLOSURE_DIAGNOSTIC"

CLASS_BOUNDARY_ONLY = "BOUNDARY_ONLY_POSITIVE"
CLASS_INTERIOR_PERSISTS = "INTERIOR_POSITIVE_PERSISTS"
CLASS_MIXED = "MIXED_OR_LABEL_TRANSITION"

# Accepted MATLAB-faithful oracle identity (read-only).
ACCEPTED_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"
ACCEPTED_SHA256 = "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"

DB0 = 7.0 / 19.0
DA0 = 10.0 / 19.0

# Accepted DLH-5J (Issue #36) HJB statistics and upper-b boundary maxima/counts
# (reproduction anchors) at FULL precision, copied verbatim from the accepted
# evidence file reports/dlh_5j_final_coupled_b_extent_diagnostic_2026_09_01/
# DLH_5J_REPRODUCIBILITY.json (run1 per-variant records) on origin/main. The
# CSVs store ~10 significant digits; the JSON preserves full float precision and
# is therefore the authoritative anchor source for the DLH-5K fail-closed
# accepted-J reproduction gate.
ACCEPTED_J_HJB_STAT = {
    "J0_A77_B120": 6.566175159150589e-08,
    "J1_A77_B140": 6.566185817291625e-08,
    "J2_A77_B160": 6.56618013294974e-08,
    "J3_A153_B120": 2.057089432128123e-08,
    "J4_A153_B140": 2.0598477590283437e-08,
    "J5_A153_B160": 2.059856285541173e-08,
}
ACCEPTED_J_UPPER_B = {
    "J0_A77_B120": {"raw_max": 0.04291614197305571, "requested_max": 0.11648667106972263, "count": 3},
    "J1_A77_B140": {"raw_max": 0.01758505362781082, "requested_max": 0.04773085984691508, "count": 2},
    "J2_A77_B160": {"raw_max": 0.0, "requested_max": 0.0, "count": 0},
    "J3_A153_B120": {"raw_max": 0.063625946244114, "requested_max": 0.1726989969483094, "count": 6},
    "J4_A153_B140": {"raw_max": 0.03844034000754548, "requested_max": 0.1043380657347663, "count": 4},
    "J5_A153_B160": {"raw_max": 0.014916256474337253, "requested_max": 0.040486981858915395, "count": 2},
}
# Accepted upper-b offender coordinate sets (b_index, a_index, z_index) from
# the accepted DLH-5J evidence, used to guarantee offender completeness and to
# anchor the exact offender coordinates before/independent of the rerun.
ACCEPTED_J_OFFENDERS = {
    "J0_A77_B120": [(119, 74, 1), (119, 75, 1), (119, 76, 1)],
    "J1_A77_B140": [(139, 75, 1), (139, 76, 1)],
    "J2_A77_B160": [],
    "J3_A153_B120": [(119, 147, 1), (119, 148, 1), (119, 149, 1), (119, 150, 1), (119, 151, 1), (119, 152, 1)],
    "J4_A153_B140": [(139, 149, 1), (139, 150, 1), (139, 151, 1), (139, 152, 1)],
    "J5_A153_B160": [(159, 151, 1), (159, 152, 1)],
}

VARIANT_IDS = [
    "J0_A77_B120", "J1_A77_B140", "J2_A77_B160",
    "J3_A153_B120", "J4_A153_B140", "J5_A153_B160",
]
A_RES_ORDER = ["a77", "a153"]
B_EXT_ORDER = ["b120", "b140", "b160"]
LOCALIZATION_LAYERS = ("n-1", "n-2", "n-3", "n-5")


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
class DLH5KConfig:
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
    accepted_hjb_stat_tol: float
    accepted_boundary_max_tol: float
    accepted_count_exact: bool
    decomposition_residual_tol: float
    policy_rel_materiality: float
    output_root: str


def load_config(path: str | pathlib.Path) -> DLH5KConfig:
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
    return DLH5KConfig(
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
        accepted_hjb_stat_tol=float(v["accepted_hjb_stat_tol"]),
        accepted_boundary_max_tol=float(v["accepted_boundary_max_tol"]),
        accepted_count_exact=bool(v["accepted_count_exact"]),
        decomposition_residual_tol=float(v["decomposition_residual_tol"]),
        policy_rel_materiality=float(v["policy_rel_materiality"]),
        output_root=str(out["root"]),
    )


# ---------------------------------------------------------------------------
# Frozen grid plan (exact accepted J0-J5)
# ---------------------------------------------------------------------------


def _a_pts(cfg: DLH5KConfig, a_res: str) -> int:
    for r in cfg.a_resolutions:
        if r.id == a_res:
            return r.a_pts
    raise ValueError(f"unknown a resolution: {a_res}")


def _b_ext(cfg: DLH5KConfig, b_ext: str) -> BExt:
    for e in cfg.b_extents:
        if e.id == b_ext:
            return e
    raise ValueError(f"unknown b extent: {b_ext}")


def build_variant_grid(spec: GridSpec, cfg: DLH5KConfig, z, switch) -> MatlabFaithfulHJBGrid:
    be = _b_ext(cfg, spec.b_ext)
    b = np.linspace(cfg.b_lo, be.b_hi, be.b_pts)
    a = np.linspace(cfg.a_lo, cfg.a_hi, _a_pts(cfg, spec.a_res))
    return MatlabFaithfulHJBGrid(b, a, np.asarray(z, dtype=float), np.asarray(switch, dtype=float))


def grid_plan_identity(cfg: DLH5KConfig) -> dict:
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
    liquid = {"b_lo": cfg.b_lo, "db": float(cfg.db), "b_extents": b_plan,
              "route_ceiling_note": cfg.route_ceiling_note,
              "hard_ceiling_b_hi": float(b_plan["b160"]["b_hi"])}
    return {"variants": variants, "a_resolutions": a_plan, "b_extents": b_plan,
            "illiquid": illiquid, "liquid": liquid}


def build_all_grids(cfg: DLH5KConfig, z, switch) -> tuple[dict, dict]:
    plan = grid_plan_identity(cfg)
    grids = {v.id: build_variant_grid(v, cfg, z, switch) for v in cfg.variants}
    for cid, fid in (("J0_A77_B120", "J3_A153_B120"),
                     ("J1_A77_B140", "J4_A153_B140"),
                     ("J2_A77_B160", "J5_A153_B160")):
        assert np.allclose(grids[fid].a[::2], grids[cid].a, atol=1e-12)
    assert np.allclose(grids["J1_A77_B140"].b[:120], grids["J0_A77_B120"].b, atol=1e-12)
    assert np.allclose(grids["J2_A77_B160"].b[:120], grids["J0_A77_B120"].b, atol=1e-12)
    assert np.allclose(grids["J2_A77_B160"].b[:140], grids["J1_A77_B140"].b, atol=1e-12)
    for vid, g in grids.items():
        assert abs(g.a[0] - cfg.a_lo) <= 1e-12 and abs(g.a[-1] - cfg.a_hi) <= 1e-12
    return grids, plan


# ---------------------------------------------------------------------------
# Phase A — exact accepted source-law audit (facts + algebra)
# ---------------------------------------------------------------------------

# Exact accepted source facts (verified by direct inspection of the accepted
# immutable oracle; the audit is persisted by the writer). Line references are
# to src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py on the
# accepted blob.
SOURCE_LAW_AUDIT_ITEMS = [
    {
        "id": "upper_b_derivative_closure",
        "item": "Upper-b derivative closure",
        "source_fact": (
            "At the top liquid node i=n-1, the forward liquid derivative V_b^+ is "
            "closed from a resource-based marginal utility, not from the value "
            "function: vb_f[n-1,j,z] = resources^(-gamma_c) with resources = "
            "(1-tau)*w*z*labor0 + transfer_income + r_b_eff*b_top (solve loop, "
            "lines 536-541). The interior forward/backward derivatives are "
            "vb_f[:-1]=(V[1:]-V[:-1])/db and vb_b[1:]=vb_f[:-1] (line 533)."
        ),
        "implied_identity": (
            "At the top node, V_b^+(closure) is the marginal utility of the notional "
            "resource branch at baseline labor0; this is what consumption/labor FOCs "
            "see through the 1e-6 derivative floor."
        ),
    },
    {
        "id": "liquid_resource_branch",
        "item": "Liquid resource / consumption branch construction",
        "source_fact": (
            "vb_b=max(v_b_backward,1e-6), vb_f=max(v_b_forward,1e-6) for controls "
            "(lines 270-271). consumption_b=vb_b^(-1/gamma_c), consumption_f=vb_f^(-1/gamma_c); "
            "liquid_resources = net_wage*labor + transfer_income + effective_r_b*b; "
            "sc_b=liquid_resources_b-consumption_b, sc_f=liquid_resources_f-consumption_f. "
            "If sc_b<-tol -> liquid_label 'B'; elif sc_f>tol -> 'F'; else liquid_label "
            "'0' with labor=baseline_labor and consumption=net_wage*baseline_labor + "
            "transfer_income + effective_r_b*b (lines 281-298)."
        ),
        "implied_identity": (
            "In the '0' branch, consumption equals total liquid resources, so "
            "base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income) = 0 "
            "exactly by construction."
        ),
    },
    {
        "id": "transfer_candidate",
        "item": "Transfer candidate d construction",
        "source_fact": (
            "transfer_candidate(v_a,v_b,a,params) computes q=V_a/V_b-1 and returns "
            "a*threshold/chi_1 with threshold=min(q+chi_0,0)+max(q-chi_0,0) using the "
            "RAW liquid derivative (bare-a FOC, no 1e-6 floor; Issue #23 narrow repair, "
            "lines 85-99). Four candidates d_bb(v_a_b,v_b_b), d_bf(v_a_f,v_b_b), "
            "d_fb(v_a_b,v_b_f), d_ff(v_a_f,v_b_f) are assembled by logical masks "
            "d_b=d_bf*(d_bf>0)+d_bb*(d_bb<0), d_f=d_ff*(d_ff>0)+d_fb*(d_fb<0) (lines 302-312)."
        ),
        "implied_identity": (
            "The transfer FOC uses bare a (not max(a,a_bar)); the direction masks "
            "implement the chi kink: positive d only if q>chi_0, negative d only if q<-chi_0."
        ),
    },
    {
        "id": "upper_a_transfer_restriction",
        "item": "Upper-a transfer-direction restriction",
        "source_fact": (
            "At the upper illiquid boundary a=a_max: d_b=d_bb*(d_bb<-tol) and "
            "d_f=d_fb*(d_fb<-tol), i.e. only NEGATIVE (withdrawal, inward-a) transfer "
            "candidates survive (lines 318-320). At the lower boundary only positive "
            "candidates survive (lines 313-317)."
        ),
        "implied_identity": (
            "At a=a_max, mu_a = r_a_eff*a + d <= 0 is enforced by admitting only d<0 "
            "with |d| large enough; the chosen d is the transfer-FOC candidate d_bb/d_fb."
        ),
    },
    {
        "id": "upper_b_transfer_override",
        "item": "Upper-b transfer-direction override",
        "source_fact": (
            "sdh_b=-d_b-adjustment_cost(d_b), sdh_f=-d_f-adjustment_cost(d_f); "
            "use_transfer_f=sdh_f>tol, use_transfer_b=sdh_b<-tol and not use_transfer_f. "
            "At the upper liquid boundary: use_transfer_f=False and use_transfer_b=True "
            "(forced backward-transfer branch); at the lower liquid boundary "
            "use_transfer_b=False (lines 322-355)."
        ),
        "implied_identity": (
            "At b=b_max the forward transfer selection is disabled and the backward "
            "transfer branch (d_b) is forced, so transfer = d_b."
        ),
    },
    {
        "id": "adjustment_cost",
        "item": "Adjustment cost",
        "source_fact": (
            "adjustment_cost(d,a,params)=chi_0*|d|+0.5*chi_1*d^2/max(a,a_bar) "
            "(lines 80-83). The denominator uses max(a,a_bar) (a_bar=1e-6 floor), unlike "
            "the transfer FOC which uses bare a."
        ),
        "implied_identity": (
            "cost is convex in d with the a_bar floor; at d=-x<0, cost=chi_0*x+0.5*chi_1*x^2/max(a,a_bar)."
        ),
    },
    {
        "id": "final_mu_a_mu_b",
        "item": "Final mu_a / mu_b evaluation",
        "source_fact": (
            "asset_drifts_matlab_faithful computes cost=adjustment_cost(transfer,a,params), "
            "labor_income=sum(wages*(1-tau-migration_costs)*z*labor), "
            "mu_b=r_b*b+labor_income-transfer-cost-consumption_net where the wrapper "
            "passes consumption_net = consumption - transfer_income (lines 379-389, 138-157). "
            "mu_a=r_a_eff(a)*a+transfer with the MATLAB taper r_a*(1-0.1*(a/a_max)^9) "
            "(lines 155-156)."
        ),
        "implied_identity": (
            "mu_b = [r_b*b + labor_income - (consumption - transfer_income)] + [-transfer - adjustment_cost] "
            "= base_liquid_surplus + transfer_injection, exactly by construction."
        ),
    },
    {
        "id": "requested_rate_conversion",
        "item": "Requested generator-rate conversion",
        "source_fact": (
            "b_forward_rate=max(mu_b,0)/db, b_backward_rate=max(-mu_b,0)/db; "
            "a_forward_rate=mh_f/da, a_backward_rate=-mh_b/da with mh_b=min(shadow_transfer_b,0) "
            "and mh_f=max(shadow_transfer_f,0)+effective_return*a (lines 404-415); the "
            "post-convergence operator uses max(mu_b,0)/db, max(-mu_b,0)/db, max(mu_a,0)/da, "
            "max(-mu_a,0)/da (line 562)."
        ),
        "implied_identity": (
            "The requested generator rate is raw outward drift divided by spacing "
            "(max(mu,0)/spacing), the HJB/KFE boundary-compatibility quantity."
        ),
    },
]


def source_law_audit(cfg: DLH5KConfig) -> dict:
    return {
        "title": "DLH-5K Phase A — accepted MATLAB-faithful source-law audit",
        "source": "src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py (accepted blob, read-only)",
        "blob": ACCEPTED_BLOB,
        "sha256": ACCEPTED_SHA256,
        "decomposition": {
            "mu_b": "base_liquid_surplus + transfer_injection",
            "base_liquid_surplus": "r_b*b + labor_income - (consumption - transfer_income)",
            "transfer_injection": "-transfer - adjustment_cost",
            "special_case": (
                "When the liquid zero-drift ('0') branch holds, consumption equals total "
                "liquid resources so base_liquid_surplus = 0 and mu_b = -transfer - "
                "adjustment_cost. This is an implemented-source identity under the stated "
                "branch conditions, NOT an economic theorem."
            ),
        },
        "items": SOURCE_LAW_AUDIT_ITEMS,
        "frozen": {
            "wbar": cfg.wbar,
            "r_a": cfg.r_a,
            "a_lo": cfg.a_lo,
            "a_hi": cfg.a_hi,
            "a_max": cfg.a_max,
            "taper_identity": cfg.taper_identity,
            "b_lo": cfg.b_lo,
            "db": float(cfg.db),
            "b_extents": [e.id for e in cfg.b_extents],
            "a_resolutions": [r.id for r in cfg.a_resolutions],
            "route_ceiling_note": cfg.route_ceiling_note,
        },
    }


# ---------------------------------------------------------------------------
# Fresh accepted HJB reruns (exact J0-J5)
# ---------------------------------------------------------------------------


def run_all_variants(cfg: DLH5KConfig, dlh5b, params, numerics) -> dict:
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, plan = build_all_grids(cfg, z, switch)
    variants = []
    hjb_results: dict[str, Any] = {}
    labor0_by_variant: dict[str, np.ndarray] = {}
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
            "max_raw_upper_a": float(np.max(np.maximum(hjb.mu_a[:, -1, :], 0.0))),
            "max_raw_lower_a": float(np.max(np.maximum(-hjb.mu_a[:, 0, :], 0.0))),
            "max_raw_upper_b": float(np.max(np.maximum(hjb.mu_b[-1, :, :], 0.0))),
            "max_raw_lower_b": float(np.max(np.maximum(-hjb.mu_b[0, :, :], 0.0))),
        }
        ub = np.maximum(hjb.mu_b[-1, :, :], 0.0) / db
        rec["max_requested_upper_b"] = float(np.max(ub)) if ub.size else 0.0
        rec["upper_b_offender_count"] = int(np.sum(ub > cfg.boundary_threshold))
        variants.append(rec)
        hjb_results[spec.id] = hjb
        labor0_by_variant[spec.id] = np.asarray(labor0, dtype=float)
    return {
        "grid_plan": plan,
        "variants": variants,
        "hjb_results": hjb_results,
        "labor0": labor0_by_variant,
        "inputs": {v.id: HouseholdInputs(
            r_a=cfg.r_a, r_b=dlh5b.r_b, tau=dlh5b.tau[cfg.region_index],
            wages=np.array([cfg.wbar]), migration_costs=np.array([0.0]),
            labor_weights=np.array([1.0]),
        ) for v in cfg.variants},
        "transfer_income": dlh5b.transfer_income[cfg.region_index],
        "rb_gap": dlh5b.rb_gap[cfg.region_index],
    }


def build_fixture(cfg: DLH5KConfig):
    dlh5b = load_dlh5b_config(cfg.dlh5b_config_path)
    _grid, params, numerics = build_dlh5b_fixture(dlh5b)
    return dlh5b, params, numerics


# ---------------------------------------------------------------------------
# Accepted-DLH-5J reproduction check (fail closed -> Outcome D)
# ---------------------------------------------------------------------------


def check_accepted_j_reproduction(cfg: DLH5KConfig, runs: dict) -> dict:
    per_variant = {}
    pass_bool = True
    for v in runs["variants"]:
        vid = v["variant"]
        acc_stat = ACCEPTED_J_HJB_STAT[vid]
        acc_ub = ACCEPTED_J_UPPER_B[vid]
        stat_diff = abs(v["hjb_statistic"] - acc_stat)
        raw_diff = abs(v["max_raw_upper_b"] - acc_ub["raw_max"])
        req_diff = abs(v["max_requested_upper_b"] - acc_ub["requested_max"])
        count_ok = (v["upper_b_offender_count"] == acc_ub["count"])
        stat_ok = stat_diff <= cfg.accepted_hjb_stat_tol
        max_ok = raw_diff <= cfg.accepted_boundary_max_tol and req_diff <= cfg.accepted_boundary_max_tol
        upper_a_ok = v["max_raw_upper_a"] <= cfg.accepted_boundary_max_tol
        lower_a_ok = v["max_raw_lower_a"] <= cfg.accepted_boundary_max_tol
        lower_b_ok = v["max_raw_lower_b"] <= cfg.accepted_boundary_max_tol
        conv_ok = bool(v["hjb_converged"])
        ok = bool(conv_ok and stat_ok and max_ok and count_ok and upper_a_ok and lower_a_ok and lower_b_ok)
        pass_bool = pass_bool and ok
        per_variant[vid] = {
            "hjb_converged": v["hjb_converged"],
            "hjb_iterations": v["hjb_iterations"],
            "hjb_statistic": v["hjb_statistic"],
            "accepted_hjb_statistic": acc_stat,
            "hjb_stat_diff": stat_diff,
            "hjb_stat_ok": stat_ok,
            "max_raw_upper_b": v["max_raw_upper_b"],
            "max_requested_upper_b": v["max_requested_upper_b"],
            "accepted_raw_upper_b": acc_ub["raw_max"],
            "accepted_requested_upper_b": acc_ub["requested_max"],
            "raw_upper_b_diff": raw_diff,
            "requested_upper_b_diff": req_diff,
            "boundary_max_ok": max_ok,
            "upper_b_offender_count": v["upper_b_offender_count"],
            "accepted_upper_b_count": acc_ub["count"],
            "count_ok": count_ok,
            "upper_a_raw_ok": upper_a_ok,
            "lower_a_raw_ok": lower_a_ok,
            "lower_b_raw_ok": lower_b_ok,
            "pass": ok,
        }
    return {"per_variant": per_variant, "pass_bool": bool(pass_bool)}


# ---------------------------------------------------------------------------
# Finite-grid derivative reconstruction (accepted formulas only)
# ---------------------------------------------------------------------------


def reconstruct_derivatives(grid, hjb, params, inputs, labor0, transfer_income, rb_gap) -> dict:
    shape = (grid.b.size, grid.a.size, grid.z.size)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    value = np.asarray(hjb.value, dtype=float)
    vb_f = np.zeros(shape)
    vb_b = np.zeros(shape)
    va_f = np.zeros(shape)
    va_b = np.zeros(shape)
    vb_f[:-1] = (value[1:] - value[:-1]) / db
    vb_b[1:] = vb_f[:-1]
    va_f[:, :-1] = (value[:, 1:] - value[:, :-1]) / da
    va_b[:, 1:] = va_f[:, :-1]
    # exact accepted upper-b derivative closure (lines 536-541)
    i_top = grid.b.size - 1
    for j in range(grid.a.size):
        for nz in range(grid.z.size):
            rb_t = inputs.r_b + (rb_gap if grid.b[i_top] < 0.0 else 0.0)
            resources = (1.0 - inputs.tau) * inputs.wages[0] * grid.z[nz] * labor0[i_top, j, nz] \
                + transfer_income + rb_t * grid.b[i_top]
            vb_f[i_top, j, nz] = resources ** (-params.gamma_c)
    return {
        "vb_f": vb_f, "vb_b": vb_b, "va_f": va_f, "va_b": va_b,
        "db": db, "da": da,
    }


# ---------------------------------------------------------------------------
# Phase B — complete upper-b offender mechanism decomposition
# ---------------------------------------------------------------------------


def _decompose_state(
    variant_id: str,
    i: int, j: int, nz: int,
    grid, hjb, params, inputs, labor0, transfer_income, rb_gap, der, cfg: DLH5KConfig,
) -> dict:
    b = float(grid.b[i])
    a = float(grid.a[j])
    z = float(grid.z[nz])
    r_b_eff = inputs.r_b + (rb_gap if b < 0.0 else 0.0)
    labor = float(hjb.labor[i, j, nz])
    consumption = float(hjb.consumption[i, j, nz])
    transfer = float(hjb.transfer[i, j, nz])
    cost = float(hjb.adjustment_cost[i, j, nz])
    labor_income = float(np.sum(
        inputs.wages * (1.0 - inputs.tau - inputs.migration_costs) * z * np.array([labor])
    ))
    base_liquid_surplus = r_b_eff * b + labor_income - (consumption - transfer_income)
    transfer_injection = -transfer - cost
    mu_b = float(hjb.mu_b[i, j, nz])
    mu_a = float(hjb.mu_a[i, j, nz])
    residual = mu_b - (base_liquid_surplus + transfer_injection)
    r_a_eff = float(matlab_faithful_illiquid_return(a, cfg.a_max, inputs.r_a))
    vb_f = float(der["vb_f"][i, j, nz])
    vb_b = float(der["vb_b"][i, j, nz])
    va_f = float(der["va_f"][i, j, nz])
    va_b = float(der["va_b"][i, j, nz])
    q_used = None
    candidate = None
    candidate_source = None
    tlabel = str(hjb.transfer_label[i, j, nz])
    if tlabel == "B":
        if transfer < 0.0:
            v_a_used, v_b_used, candidate_source = va_b, vb_b, "d_bb(va_b,vb_b)"
        elif transfer > 0.0:
            v_a_used, v_b_used, candidate_source = va_f, vb_b, "d_bf(va_f,vb_b)"
        else:
            v_a_used = v_b_used = None
        if v_a_used is not None and np.isfinite(v_a_used) and np.isfinite(v_b_used):
            q_used = float(v_a_used / v_b_used - 1.0)
            candidate = float(transfer_candidate(v_a_used, v_b_used, a, params))
    elif tlabel == "F":
        if transfer > 0.0:
            v_a_used, v_b_used, candidate_source = va_f, vb_f, "d_ff(va_f,vb_f)"
        elif transfer < 0.0:
            v_a_used, v_b_used, candidate_source = va_b, vb_f, "d_fb(va_b,vb_f)"
        else:
            v_a_used = v_b_used = None
        if v_a_used is not None and np.isfinite(v_a_used) and np.isfinite(v_b_used):
            q_used = float(v_a_used / v_b_used - 1.0)
            candidate = float(transfer_candidate(v_a_used, v_b_used, a, params))
    return {
        "variant": variant_id,
        "b_index": i, "a_index": j, "z_index": nz,
        "b": b, "a": a, "z": z,
        "liquid_label": str(hjb.liquid_label[i, j, nz]),
        "transfer_label": tlabel,
        "consumption": consumption,
        "labor": labor,
        "transfer": transfer,
        "adjustment_cost": cost,
        "effective_illiquid_return": r_a_eff,
        "mu_a": mu_a,
        "mu_b": mu_b,
        "base_liquid_surplus": base_liquid_surplus,
        "transfer_injection": transfer_injection,
        "reconstruction_residual": residual,
        "vb_boundary_closure": vb_f,
        "vb_backward": vb_b,
        "va_forward": va_f,
        "va_backward": va_b,
        "va_over_vb_minus_1": q_used,
        "selected_transfer_candidate": candidate,
        "candidate_source": candidate_source,
        "is_top_layer": bool(i == grid.b.size - 1),
        "material_positive": bool(mu_b > cfg.boundary_threshold * der["db"]),
    }


def offender_coordinates(runs: dict) -> dict:
    """Recompute material upper-b offender coordinates (requested > threshold)."""
    cfg_threshold = 1e-10
    out = {}
    for v in runs["variants"]:
        vid = v["variant"]
        hjb = runs["hjb_results"][vid]
        grid = _grid_for(runs, vid)
        db = float(grid.b[1] - grid.b[0])
        ub = np.maximum(hjb.mu_b[-1, :, :], 0.0) / db
        coords = [(int(grid.b.size - 1), int(j), int(nz))
                  for j, nz in np.argwhere(ub > cfg_threshold)]
        out[vid] = coords
    return out


def _grid_for(runs: dict, vid: str) -> MatlabFaithfulHJBGrid:
    return runs["grids"][vid]


def offender_decomposition(cfg: DLH5KConfig, runs: dict) -> dict:
    """Phase B: decompose every material upper-b offender on J0/J1/J3/J4/J5 plus
    the corresponding aligned states on J2 (even when non-offending)."""
    der_cache = {}
    for vid in VARIANT_IDS:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der_cache[vid] = reconstruct_derivatives(
            grid, hjb, runs["params"], runs["inputs"][vid],
            runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
        )
    coords = offender_coordinates(runs)
    rows = []
    for vid in VARIANT_IDS:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der = der_cache[vid]
        if vid == "J2_A77_B160":
            # aligned states on J2: for each offender (a,z) from the other a77
            # variants map directly; from a153 variants map a153//2 -> a77.
            seen = set()
            for other in ("J0_A77_B120", "J1_A77_B140", "J3_A153_B120", "J4_A153_B140", "J5_A153_B160"):
                for (_i, j, nz) in coords[other]:
                    if other.startswith("J3") or other.startswith("J4") or other.startswith("J5"):
                        j_map = j // 2
                    else:
                        j_map = j
                    key = (j_map, nz)
                    if key in seen:
                        continue
                    seen.add(key)
                    rows.append(_decompose_state(
                        vid, int(grid.b.size - 1), j_map, nz,
                        grid, hjb, runs["params"], runs["inputs"][vid],
                        runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
                        der, cfg,
                    ))
            continue
        for (i, j, nz) in coords[vid]:
            rows.append(_decompose_state(
                vid, i, j, nz,
                grid, hjb, runs["params"], runs["inputs"][vid],
                runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
                der, cfg,
            ))
    # complete-offender cross-check against accepted coordinate sets
    accepted_set = {vid: set(tuple(c) for c in ACCEPTED_J_OFFENDERS[vid]) for vid in VARIANT_IDS}
    completeness = {}
    for vid in VARIANT_IDS:
        if vid == "J2_A77_B160":
            completeness[vid] = {"accepted": 0, "recomputed": 0, "match": True}
            continue
        recomputed = set(tuple(c) for c in coords[vid])
        completeness[vid] = {
            "accepted_count": len(accepted_set[vid]),
            "recomputed_count": len(recomputed),
            "missing": sorted(accepted_set[vid] - recomputed),
            "extra": sorted(recomputed - accepted_set[vid]),
            "match": bool(accepted_set[vid] == recomputed),
        }
    return {"rows": rows, "coordinates": coords, "completeness": completeness}


# ---------------------------------------------------------------------------
# Phase C — boundary vs interior high-wealth localization
# ---------------------------------------------------------------------------


def localization_layers(b_pts: int) -> list[tuple[str, int]]:
    top = b_pts - 1
    return [("n-1", top), ("n-2", top - 1), ("n-3", top - 2), ("n-5", top - 4)]


def boundary_interior_localization(cfg: DLH5KConfig, runs: dict) -> dict:
    """Phase C: for each material offender (a,z), inspect n-1/n-2/n-3/n-5 b
    layers with the same decomposition and labels; classify each trajectory."""
    coords = offender_coordinates(runs)
    der_cache = {}
    for vid in VARIANT_IDS:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der_cache[vid] = reconstruct_derivatives(
            grid, hjb, runs["params"], runs["inputs"][vid],
            runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
        )
    rows = []
    classifications = []
    for vid in VARIANT_IDS:
        if vid == "J2_A77_B160":
            continue
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der = der_cache[vid]
        b_pts = grid.b.size
        for (i_top, j, nz) in coords[vid]:
            layers = []
            for label, idx in localization_layers(b_pts):
                if idx < 0:
                    continue
                d = _decompose_state(
                    vid, idx, j, nz,
                    grid, hjb, runs["params"], runs["inputs"][vid],
                    runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
                    der, cfg,
                )
                d["layer"] = label
                layers.append(d)
            top = layers[0]
            interior = layers[1:]
            top_material = bool(top["material_positive"])
            interior_material = bool(any(l["material_positive"] for l in interior))
            if top_material and not interior_material:
                cls = CLASS_BOUNDARY_ONLY
            elif top_material and interior_material:
                cls = CLASS_INTERIOR_PERSISTS
            else:
                cls = CLASS_MIXED
            classifications.append({
                "variant": vid, "a_index": j, "z_index": nz,
                "classification": cls,
                "top_material": top_material,
                "interior_material": interior_material,
            })
            for l in layers:
                rows.append(l)
    return {"rows": rows, "classifications": classifications}


# ---------------------------------------------------------------------------
# Phase D — joint upper-corner feasibility algebra + numerical evaluation
# ---------------------------------------------------------------------------


def joint_corner_feasibility(cfg: DLH5KConfig, runs: dict, decomps: dict) -> dict:
    """Phase D: for negative transfer d=-x<0 at each offender state, derive and
    numerically verify the joint-corner inequalities mu_a<=0 and mu_b<=0."""
    der_cache = {}
    for vid in VARIANT_IDS:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der_cache[vid] = reconstruct_derivatives(
            grid, hjb, runs["params"], runs["inputs"][vid],
            runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
        )
    coords = offender_coordinates(runs)
    params = runs["params"]
    rows = []
    for vid in VARIANT_IDS:
        if vid == "J2_A77_B160":
            continue
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der = der_cache[vid]
        for (i, j, nz) in coords[vid]:
            a = float(grid.a[j])
            b = float(grid.b[i])
            z = float(grid.z[nz])
            transfer = float(hjb.transfer[i, j, nz])
            cost = float(hjb.adjustment_cost[i, j, nz])
            mu_a_direct = float(hjb.mu_a[i, j, nz])
            mu_b_direct = float(hjb.mu_b[i, j, nz])
            base = float(decomps_by_index(decomps, vid, i, j, nz)["base_liquid_surplus"])
            r_a_eff = float(matlab_faithful_illiquid_return(a, cfg.a_max, runs["inputs"][vid].r_a))
            # algebraic mu_a from d=-x
            x = -transfer
            chi_0 = params.chi_0
            chi_1 = params.chi_1
            a_den = max(a, params.a_bar)
            # general base_liquid_surplus kept first
            mu_a_algebra = r_a_eff * a - x
            mu_b_algebra_general = base + x * (1.0 - chi_0) - 0.5 * chi_1 * x * x / a_den
            x_min_a = r_a_eff * a  # from mu_a<=0 -> x >= r_a_eff*a
            # general inward mu_b condition: base + x(1-chi_0) - 0.5*chi_1*x^2/a_den <= 0
            # positive root of the quadratic = threshold x_b
            # 0.5*chi_1/a_den * x^2 - (1-chi_0)*x - base = 0  ->  x^2 - 2(1-chi_0)*a_den/chi_1*x - 2*base*a_den/chi_1 = 0
            qq = 2.0 * (1.0 - chi_0) * a_den / chi_1
            rr = 2.0 * base * a_den / chi_1
            disc = qq * qq + 4.0 * rr
            x_b_general = (qq + np.sqrt(disc)) / 2.0 if disc >= 0.0 else None
            x_b_simplified = qq  # base_liquid_surplus = 0 branch
            base_is_zero = bool(abs(base) <= cfg.decomposition_residual_tol)
            mu_a_inward_holds = bool(mu_a_algebra <= 1e-12)
            mu_b_inward_holds = bool(mu_b_algebra_general <= 1e-12)
            joint_feasible = bool(mu_a_inward_holds and mu_b_inward_holds)
            residual_mu_a = mu_a_direct - mu_a_algebra
            residual_mu_b = mu_b_direct - mu_b_algebra_general
            rows.append({
                "variant": vid,
                "b_index": i, "a_index": j, "z_index": nz,
                "b": b, "a": a, "z": z,
                "x_minus_transfer": x,
                "chi_0": chi_0, "chi_1": chi_1, "a_bar": params.a_bar,
                "a_denominator": a_den,
                "r_a_effective": r_a_eff,
                "mu_a_direct": mu_a_direct,
                "mu_a_algebra": mu_a_algebra,
                "mu_a_residual": residual_mu_a,
                "mu_a_inward_holds": mu_a_inward_holds,
                "x_min_a": x_min_a,
                "base_liquid_surplus": base,
                "transfer_injection": -transfer - cost,
                "mu_b_direct": mu_b_direct,
                "mu_b_algebra_general": mu_b_algebra_general,
                "mu_b_residual": residual_mu_b,
                "mu_b_inward_holds_general": mu_b_inward_holds,
                "x_b_general_positive_root": x_b_general,
                "x_b_simplified_base_zero": x_b_simplified,
                "base_is_zero_branch": base_is_zero,
                "joint_corner_feasible": joint_feasible,
                "simplified_inequality": (
                    f"x >= {x_b_simplified:.6e}" if base_is_zero
                    else f"x satisfies 0.5*chi_1*x^2/a_den >= base + x*(1-chi_0); root {x_b_general:.6e}" if x_b_general is not None
                    else "base + x(1-chi_0) - 0.5*chi_1*x^2/a_den <= 0"
                ),
            })
    return {"rows": rows, "algebra": {
        "chi": "chi(d,a)=chi_0*|d|+0.5*chi_1*d^2/max(a,a_bar)",
        "d": "d=-x, x>0",
        "upper_a_inward": "mu_a = r_a_eff(a)*a + d = r_a_eff(a)*a - x <= 0  <=>  x >= r_a_eff(a)*a",
        "upper_b_inward_general": (
            "mu_b = base_liquid_surplus + (-d - chi(d,a)) "
            "= base_liquid_surplus + x(1-chi_0) - 0.5*chi_1*x^2/max(a,a_bar) <= 0"
        ),
        "upper_b_inward_simplified": (
            "when base_liquid_surplus = 0: x >= 2*(1-chi_0)*max(a,a_bar)/chi_1 "
            "(under the empirically verified zero-drift branch only)"
        ),
    }}


def decomps_by_index(decomps: dict, vid: str, i: int, j: int, nz: int) -> dict:
    for r in decomps["rows"]:
        if (r["variant"], r["b_index"], r["a_index"], r["z_index"]) == (vid, i, j, nz):
            return r
    raise KeyError((vid, i, j, nz))


# ---------------------------------------------------------------------------
# Phase E — cross-a resolution mechanism at common final b extents
# ---------------------------------------------------------------------------


def cross_a_mechanism(cfg: DLH5KConfig, runs: dict) -> dict:
    """Phase E: exact aligned a77 vs every-second a153 high-wealth nodes at
    b120/b140/b160; channel attribution."""
    der_cache = {}
    for vid in VARIANT_IDS:
        grid = _grid_for(runs, vid)
        hjb = runs["hjb_results"][vid]
        der_cache[vid] = reconstruct_derivatives(
            grid, hjb, runs["params"], runs["inputs"][vid],
            runs["labor0"][vid], runs["transfer_income"], runs["rb_gap"],
        )
    coords = offender_coordinates(runs)
    rows = []
    totals = {"b120": {"abs_delta_ti": 0.0, "abs_delta_bls": 0.0},
              "b140": {"abs_delta_ti": 0.0, "abs_delta_bls": 0.0},
              "b160": {"abs_delta_ti": 0.0, "abs_delta_bls": 0.0}}
    for ext in B_EXT_ORDER:
        coarse_id = {"b120": "J0_A77_B120", "b140": "J1_A77_B140", "b160": "J2_A77_B160"}[ext]
        fine_id = {"b120": "J3_A153_B120", "b140": "J4_A153_B140", "b160": "J5_A153_B160"}[ext]
        grid_c = _grid_for(runs, coarse_id)
        grid_f = _grid_for(runs, fine_id)
        hjb_c = runs["hjb_results"][coarse_id]
        hjb_f = runs["hjb_results"][fine_id]
        der_c = der_cache[coarse_id]
        der_f = der_cache[fine_id]
        # high-wealth a-coordinate band: union of offender a indices mapped to
        # coarse/fine; also the aligned top-corner band (top a layers used above)
        a_band = set()
        for vid in (coarse_id, fine_id):
            for (_i, j, nz) in coords[vid]:
                if nz == 1:
                    if vid in (fine_id,):
                        a_band.add(j // 2)
                    else:
                        a_band.add(j)
        # ensure the top-corner band is always included (top 4 coarse a layers)
        for jc in range(grid_c.a.size - 1, max(grid_c.a.size - 5, -1), -1):
            a_band.add(jc)
        a_band = sorted(a_band)
        i_top_c = grid_c.b.size - 1
        i_top_f = grid_f.b.size - 1
        for jc in a_band:
            jf = 2 * jc
            if jf >= grid_f.a.size:
                continue
            for nz in range(grid_c.z.size):
                d_c = _decompose_state(
                    coarse_id, i_top_c, jc, nz,
                    grid_c, hjb_c, runs["params"], runs["inputs"][coarse_id],
                    runs["labor0"][coarse_id], runs["transfer_income"], runs["rb_gap"],
                    der_c, cfg,
                )
                d_f = _decompose_state(
                    fine_id, i_top_f, jf, nz,
                    grid_f, hjb_f, runs["params"], runs["inputs"][fine_id],
                    runs["labor0"][fine_id], runs["transfer_income"], runs["rb_gap"],
                    der_f, cfg,
                )
                delta_mu_b = d_c["mu_b"] - d_f["mu_b"]
                delta_bls = d_c["base_liquid_surplus"] - d_f["base_liquid_surplus"]
                delta_ti = d_c["transfer_injection"] - d_f["transfer_injection"]
                residual = delta_mu_b - (delta_bls + delta_ti)
                if abs(delta_ti) > abs(delta_bls):
                    channel = "TRANSFER_DERIVATIVE"
                elif abs(delta_bls) > abs(delta_ti):
                    channel = "BASE_LIQUID_SURPLUS"
                else:
                    channel = "BOTH_EQUAL"
                totals[ext]["abs_delta_ti"] += abs(delta_ti)
                totals[ext]["abs_delta_bls"] += abs(delta_bls)
                q_c = d_c["va_over_vb_minus_1"]
                q_f = d_f["va_over_vb_minus_1"]
                rows.append({
                    "b_extent": ext,
                    "coarse_variant": coarse_id, "fine_variant": fine_id,
                    "a77_index": jc, "a153_index": jf, "z_index": nz,
                    "a77_physical_a": d_c["a"], "a153_physical_a": d_f["a"],
                    "b_top": d_c["b"],
                    "va_over_vb_minus_1_a77": q_c,
                    "va_over_vb_minus_1_a153": q_f,
                    "selected_transfer_candidate_a77": d_c["selected_transfer_candidate"],
                    "selected_transfer_candidate_a153": d_f["selected_transfer_candidate"],
                    "transfer_label_a77": d_c["transfer_label"],
                    "transfer_label_a153": d_f["transfer_label"],
                    "liquid_label_a77": d_c["liquid_label"],
                    "liquid_label_a153": d_f["liquid_label"],
                    "transfer_a77": d_c["transfer"],
                    "transfer_a153": d_f["transfer"],
                    "adjustment_cost_a77": d_c["adjustment_cost"],
                    "adjustment_cost_a153": d_f["adjustment_cost"],
                    "base_liquid_surplus_a77": d_c["base_liquid_surplus"],
                    "base_liquid_surplus_a153": d_f["base_liquid_surplus"],
                    "transfer_injection_a77": d_c["transfer_injection"],
                    "transfer_injection_a153": d_f["transfer_injection"],
                    "mu_b_a77": d_c["mu_b"],
                    "mu_b_a153": d_f["mu_b"],
                    "delta_mu_b": delta_mu_b,
                    "delta_base_liquid_surplus": delta_bls,
                    "delta_transfer_injection": delta_ti,
                    "residual": residual,
                    "channel": channel,
                })
    b160_primarily_transfer = bool(
        totals["b160"]["abs_delta_ti"] > totals["b160"]["abs_delta_bls"]
    )
    return {"rows": rows, "totals": totals,
            "b160_primarily_transfer_channel": b160_primarily_transfer}


# ---------------------------------------------------------------------------
# Deterministic repeat
# ---------------------------------------------------------------------------


def _nonfinite_aligned(a, b) -> bool:
    return bool((not np.isfinite(a)) and (not np.isfinite(b)))


def compare_scalar_records(r1: dict, r2: dict, tol: float) -> dict:
    keys = ["hjb_statistic", "max_raw_upper_a", "max_raw_lower_a",
            "max_raw_upper_b", "max_raw_lower_b", "max_requested_upper_b"]
    max_diff = 0.0
    mismatched = 0
    aligned_nonfinite = 0
    for k in keys:
        a = float(r1[k]); b = float(r2[k])
        if np.isfinite(a) and np.isfinite(b):
            max_diff = max(max_diff, abs(a - b))
        elif _nonfinite_aligned(a, b):
            aligned_nonfinite += 1
        else:
            mismatched += 1
    counts_ok = all(r1["upper_b_offender_count"] == r2["upper_b_offender_count"] for _ in [0])
    return {
        "max_numeric_diff": float(max_diff),
        "aligned_nonfinite": aligned_nonfinite,
        "mismatched": mismatched,
        "counts_identical": bool(counts_ok and r1["upper_b_offender_count"] == r2["upper_b_offender_count"]),
        "pass_bool": bool(max_diff <= tol and mismatched == 0 and counts_ok),
    }


def reproduce(cfg: DLH5KConfig, dlh5b, params, numerics) -> dict:
    run1 = run_all_variants(cfg, dlh5b, params, numerics)
    run2 = run_all_variants(cfg, dlh5b, params, numerics)
    per_variant = {}
    for r1, r2 in zip(run1["variants"], run2["variants"]):
        per_variant[r1["variant"]] = compare_scalar_records(r1, r2, cfg.reproducibility_tol)
    pass_bool = all(v["pass_bool"] for v in per_variant.values())
    return {
        "run1": {"variants": run1["variants"]},
        "run2": {"variants": run2["variants"]},
        "per_variant": per_variant,
        "pass_bool": bool(pass_bool),
        "randomness": "NOT_APPLICABLE",
    }


# ---------------------------------------------------------------------------
# Terminal classification
# ---------------------------------------------------------------------------


def dominant_transfer_component(decomps: dict, cfg: DLH5KConfig) -> bool:
    offender_rows = [r for r in decomps["rows"] if r["variant"] != "J2_A77_B160"]
    if not offender_rows:
        return False
    for r in offender_rows:
        ti = r["transfer_injection"]
        bls = r["base_liquid_surplus"]
        # dominant positive component is the transfer-injection term: |ti| > |bls|
        if not (abs(ti) > abs(bls)):
            return False
        if not (r["mu_b"] > 0.0):
            return False
    return True


def decomposition_holds(decomps: dict, cfg: DLH5KConfig) -> bool:
    offender_rows = [r for r in decomps["rows"] if r["variant"] != "J2_A77_B160"]
    if not offender_rows:
        return False
    return all(abs(r["reconstruction_residual"]) <= cfg.decomposition_residual_tol
               for r in offender_rows)


def overall_terminal(cfg: DLH5KConfig, repro_accepted: dict, repro: dict,
                     classifs: list, decomps: dict, cross_a: dict) -> dict:
    if not repro_accepted["pass_bool"]:
        terminal = TERMINAL_OUTCOME_D
    elif not repro["pass_bool"]:
        terminal = TERMINAL_OUTCOME_E
    else:
        codes = [c["classification"] for c in classifs]
        any_interior = any(c == CLASS_INTERIOR_PERSISTS for c in codes)
        all_boundary_only = bool(codes) and all(c == CLASS_BOUNDARY_ONLY for c in codes)
        dominant = dominant_transfer_component(decomps, cfg)
        decomp_ok = decomposition_holds(decomps, cfg)
        if any_interior:
            if all(c == CLASS_INTERIOR_PERSISTS for c in codes):
                terminal = TERMINAL_OUTCOME_B
            else:
                terminal = TERMINAL_OUTCOME_C
        elif all_boundary_only and dominant and decomp_ok:
            terminal = TERMINAL_OUTCOME_A
        else:
            terminal = TERMINAL_OUTCOME_C
    annotations = []
    if cross_a["b160_primarily_transfer_channel"]:
        annotations.append(ANNOTATION_CROSS_A_TRANSFER_CHANNEL)
    return {"terminal": terminal, "annotations": annotations}


def stopping_rule_note(terminal: str) -> str:
    if terminal == TERMINAL_OUTCOME_A:
        return (
            "Next gate must be a scientific design freeze for a joint upper-corner "
            "HJB/KKT boundary law (not an implementation patch). Stationary KFE remains "
            "NOT AUTHORIZED until that design gate passes under Issue #27."
        )
    if terminal == TERMINAL_OUTCOME_B:
        return (
            "Next gate must address high-wealth economic asymptotics / mean reversion "
            "without larger-grid PASS seeking. Stationary KFE remains NOT AUTHORIZED."
        )
    if terminal == TERMINAL_OUTCOME_C:
        return (
            "Both mechanisms must be separately resolved before any HJB redesign or "
            "stationary re-entry. Stationary KFE remains NOT AUTHORIZED."
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


def _fmt_bool(v) -> str:
    return "True" if v else "False"


def _write_csv(path: pathlib.Path, fields: list, rows: list) -> None:
    import csv
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(fields)
        for r in rows:
            w.writerow(r)


def _render_source_law_audit(audit: dict) -> str:
    lines = [f"# {audit['title']}", ""]
    lines.append(f"Source (read-only): `{audit['source']}`; blob `{audit['blob']}`; "
                 f"SHA-256 `{audit['sha256']}`.")
    lines.append("")
    lines.append("## Accepted drift decomposition (derived from the implemented equations only)")
    lines.append("")
    d = audit["decomposition"]
    lines.append("```text")
    lines.append("mu_b = base_liquid_surplus + transfer_injection")
    lines.append("base_liquid_surplus = r_b*b + labor_income - (consumption - transfer_income)")
    lines.append("transfer_injection = -transfer - adjustment_cost")
    lines.append("```")
    lines.append("")
    lines.append(f"- Special case ({d['special_case']})")
    lines.append("")
    lines.append("## Exact accepted implementation ordering (8 audited objects)")
    lines.append("")
    for it in audit["items"]:
        lines.append(f"### {it['item']} (`{it['id']}`)")
        lines.append("")
        lines.append(f"- Source fact: {it['source_fact']}")
        lines.append(f"- Implied identity: {it['implied_identity']}")
        lines.append("")
    lines.append("## Frozen objects in every DLH-5K rerun")
    lines.append("")
    fz = audit["frozen"]
    lines.append(f"- `wbar={fz['wbar']}`, `r_a={fz['r_a']}`; a in "
                 f"[{fz['a_lo']},{fz['a_hi']}], `a_max={fz['a_max']}`, taper `{fz['taper_identity']}`; "
                 f"`b_lo={fz['b_lo']}`, `db={fz['db']:.12f}`; a resolutions "
                 f"{fz['a_resolutions']}; b extents {fz['b_extents']}; "
                 f"{fz['route_ceiling_note']}.")
    lines.append("")
    lines.append("This is an adjudication diagnostic, not a redesign. No source/model "
                 "equation may change in DLH-5K; no terminal authorizes a source change.")
    return "\n".join(lines)


_DECOMP_FIELDS = [
    "variant", "b_index", "a_index", "z_index", "b", "a", "z",
    "liquid_label", "transfer_label", "consumption", "labor", "transfer",
    "adjustment_cost", "effective_illiquid_return", "mu_a", "mu_b",
    "base_liquid_surplus", "transfer_injection", "reconstruction_residual",
    "vb_boundary_closure", "vb_backward", "va_forward", "va_backward",
    "va_over_vb_minus_1", "selected_transfer_candidate", "candidate_source",
    "is_top_layer", "material_positive",
]


def write_evidence(root: pathlib.Path, cfg: DLH5KConfig, audit: dict, runs: dict,
                   repro_accepted: dict, decomps: dict, local: dict, feasible: dict,
                   cross_a: dict, repro: dict, term: dict) -> None:
    root = pathlib.Path(root)
    root.mkdir(parents=True, exist_ok=True)

    # 1) SOURCE_LAW_AUDIT.md
    with open(root / "DLH_5K_SOURCE_LAW_AUDIT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_source_law_audit(audit))

    # 2) OFFENDER_DECOMPOSITION.csv
    rows = []
    for r in decomps["rows"]:
        rows.append([_fmt(r[k]) for k in _DECOMP_FIELDS])
    _write_csv(root / "DLH_5K_OFFENDER_DECOMPOSITION.csv", _DECOMP_FIELDS, rows)

    # 3) BOUNDARY_INTERIOR_LOCALIZATION.csv
    loc_fields = ["layer"] + _DECOMP_FIELDS
    rows = []
    for r in local["rows"]:
        rows.append([r.get("layer", "")] + [_fmt(r[k]) for k in _DECOMP_FIELDS])
    _write_csv(root / "DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv", loc_fields, rows)

    # 4) JOINT_CORNER_FEASIBILITY.csv
    feas_fields = [
        "variant", "b_index", "a_index", "z_index", "b", "a", "z",
        "x_minus_transfer", "chi_0", "chi_1", "a_bar", "a_denominator",
        "r_a_effective", "mu_a_direct", "mu_a_algebra", "mu_a_residual",
        "mu_a_inward_holds", "x_min_a", "base_liquid_surplus", "transfer_injection",
        "mu_b_direct", "mu_b_algebra_general", "mu_b_residual",
        "mu_b_inward_holds_general", "x_b_general_positive_root",
        "x_b_simplified_base_zero", "base_is_zero_branch",
        "joint_corner_feasible", "simplified_inequality",
    ]
    rows = []
    for r in feasible["rows"]:
        rows.append([_fmt(r[k]) for k in feas_fields])
    _write_csv(root / "DLH_5K_JOINT_CORNER_FEASIBILITY.csv", feas_fields, rows)

    # 5) CROSS_A_MECHANISM.csv
    ca_fields = [
        "b_extent", "coarse_variant", "fine_variant", "a77_index", "a153_index",
        "z_index", "a77_physical_a", "a153_physical_a", "b_top",
        "va_over_vb_minus_1_a77", "va_over_vb_minus_1_a153",
        "selected_transfer_candidate_a77", "selected_transfer_candidate_a153",
        "transfer_label_a77", "transfer_label_a153",
        "liquid_label_a77", "liquid_label_a153",
        "transfer_a77", "transfer_a153",
        "adjustment_cost_a77", "adjustment_cost_a153",
        "base_liquid_surplus_a77", "base_liquid_surplus_a153",
        "transfer_injection_a77", "transfer_injection_a153",
        "mu_b_a77", "mu_b_a153",
        "delta_mu_b", "delta_base_liquid_surplus", "delta_transfer_injection",
        "residual", "channel",
    ]
    rows = []
    for r in cross_a["rows"]:
        rows.append([_fmt(r[k]) for k in ca_fields])
    _write_csv(root / "DLH_5K_CROSS_A_MECHANISM.csv", ca_fields, rows)

    # 6) REPRODUCIBILITY.json
    with open(root / "DLH_5K_REPRODUCIBILITY.json", "w", encoding="utf-8") as fh:
        json.dump({"deterministic_repeat": repro, "accepted_j_reproduction": repro_accepted,
                   "terminal": term}, fh, indent=2, default=str, sort_keys=True)

    # 7) EXECUTION_REPORT.md
    with open(root / "DLH_5K_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_report(cfg, runs, repro_accepted, decomps, local, feasible,
                                cross_a, repro, term))

    # 8) FORBIDDEN_OPERATION_CHECK.md
    with open(root / "DLH_5K_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write(_render_forbidden_check(cfg, term))


def _render_report(cfg: DLH5KConfig, runs: dict, repro_accepted: dict, decomps: dict,
                   local: dict, feasible: dict, cross_a: dict, repro: dict, term: dict) -> str:
    lines = ["# DLH-5K — High-Wealth Liquid Drift vs Joint Upper-Corner HJB Closure "
             "(Issue #37)", ""]
    lines.append("Analytical/source-preserving adjudication. Reran exactly the six accepted "
                 "DLH-5J grids J0-J5 solely to extract local high-wealth diagnostics. "
                 "Accepted MATLAB-faithful HJB source is immutable and reused read-only.")
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
                 f"no b100 rerun; no clipping.")
    lines.append("")

    lines.append("## Accepted J0-J5 reproduction (fail-closed gate)")
    lines.append("")
    lines.append("| variant | HJB stat | accepted stat | |stat diff| | raw ub | req ub | count | pass |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for vid, r in repro_accepted["per_variant"].items():
        lines.append(f"| {vid} | {r['hjb_statistic']:.3e} | {r['accepted_hjb_statistic']:.3e} | "
                     f"{r['hjb_stat_diff']:.3e} | {r['max_raw_upper_b']:.3e} | "
                     f"{r['max_requested_upper_b']:.3e} | {r['upper_b_offender_count']} | "
                     f"{r['pass']} |")
    lines.append("")
    lines.append(f"Overall accepted-J reproduction pass: `{repro_accepted['pass_bool']}`. "
                 "Any failure would classify BLOCKED_DLH_5K_ACCEPTED_HJB_REPRODUCTION.")
    lines.append("")

    lines.append("## Phase A — source-law audit")
    lines.append("")
    lines.append(f"Full audit persisted in `DLH_5K_SOURCE_LAW_AUDIT.md` (8 audited objects: "
                 "upper-b derivative closure; liquid resource/consumption branch; transfer "
                 "candidate; upper-a transfer-direction restriction; upper-b transfer-direction "
                 "override; adjustment cost; final mu_a/mu_b; requested-rate conversion). "
                 "Decomposition verified numerically in Phase B for every offender: "
                 "`mu_b = base_liquid_surplus + transfer_injection`.")
    lines.append("")
    lines.append("### Implemented-source special-case identity")
    lines.append("")
    lines.append("When the liquid zero-drift (`0`) branch holds, `consumption` equals total "
                 "liquid resources, so `base_liquid_surplus = 0` and the implemented identity is "
                 "`mu_b = -transfer - adjustment_cost`. This is an implemented-source identity "
                 "under the stated branch conditions, **not** an economic theorem.")
    lines.append("")

    lines.append("## Phase B — complete upper-b offender mechanism decomposition")
    lines.append("")
    lines.append(f"Full table persisted in `DLH_5K_OFFENDER_DECOMPOSITION.csv` "
                 f"({len(decomps['rows'])} rows: every material upper-b offender on "
                 "J0/J1/J3/J4/J5 plus the corresponding aligned states on J2). Completeness vs "
                 "the accepted DLH-5J offender sets:")
    lines.append("")
    for vid, c in decomps["completeness"].items():
        if vid == "J2_A77_B160":
            continue
        lines.append(f"- {vid}: accepted {c['accepted_count']}, recomputed {c['recomputed_count']}, "
                     f"match {c['match']} (missing {c['missing']}, extra {c['extra']})")
    lines.append("")
    lines.append("Per-state persisted: indices + physical (b,a,z); liquid_label; transfer_label; "
                 "consumption; labor; transfer; adjustment cost; effective illiquid return; mu_a; "
                 "mu_b; base_liquid_surplus; transfer_injection; reconstruction residual; "
                 "V_b boundary-closure derivative; backward V_b derivative; available forward/"
                 "backward V_a derivatives; V_a/V_b-1; selected transfer candidate where finite. "
                 "Only derivatives recoverable from the accepted finite grid and converged value "
                 "function are used (no invented derivatives).")
    lines.append("")

    lines.append("## Phase C — boundary-vs-interior high-wealth localization")
    lines.append("")
    lines.append(f"Full table persisted in `DLH_5K_BOUNDARY_INTERIOR_LOCALIZATION.csv`. Each "
                 "material offender (a,z) is inspected at n-1/n-2/n-3/n-5 b layers with the same "
                 "decomposition and labels; no tolerance beyond the accepted boundary threshold "
                 "is used.")
    lines.append("")
    for c in local["classifications"]:
        lines.append(f"- {c['variant']} (a={c['a_index']}, z={c['z_index']}): "
                     f"{c['classification']} (top material {c['top_material']}, "
                     f"interior material {c['interior_material']})")
    lines.append("")

    lines.append("## Phase D — joint upper-corner feasibility algebra + numerical evaluation")
    lines.append("")
    lines.append("```text")
    lines.append("chi(d,a) = chi_0*|d| + 0.5*chi_1*d^2/max(a,a_bar)")
    lines.append("d = -x, x > 0")
    lines.append("upper-a inward: mu_a = r_a_eff(a)*a - x <= 0   <=>  x >= r_a_eff(a)*a")
    lines.append("upper-b inward (general): mu_b = base_liquid_surplus")
    lines.append("                        + x*(1-chi_0) - 0.5*chi_1*x^2/max(a,a_bar) <= 0")
    lines.append("upper-b inward (base_liquid_surplus=0 branch only):")
    lines.append("                        x >= 2*(1-chi_0)*max(a,a_bar)/chi_1")
    lines.append("```")
    lines.append("")
    lines.append(f"Numerical evaluation persisted in `DLH_5K_JOINT_CORNER_FEASIBILITY.csv` "
                 f"({len(feasible['rows'])} rows) at the actual offender states with the frozen "
                 "D0 parameters, verifying the algebra against the direct drifts "
                 "(mu_a/mu_b residuals reported).")
    lines.append("")

    lines.append("## Phase E — cross-a resolution mechanism (b120/b140/b160)")
    lines.append("")
    lines.append(f"Full table persisted in `DLH_5K_CROSS_A_MECHANISM.csv` "
                 f"({len(cross_a['rows'])} aligned a77 vs every-second a153 pairs).")
    lines.append("")
    for ext in B_EXT_ORDER:
        t = cross_a["totals"][ext]
        lines.append(f"- {ext}: sum|delta transfer_injection| = {t['abs_delta_ti']:.6e}, "
                     f"sum|delta base_liquid_surplus| = {t['abs_delta_bls']:.6e}")
    lines.append("")
    lines.append(f"b160 divergence primarily transfer/derivative channel: "
                 f"{cross_a['b160_primarily_transfer_channel']}.")
    lines.append("")

    lines.append("## Deterministic repeat")
    lines.append("")
    lines.append(f"- randomness `{repro['randomness']}`; repeat pass `{repro['pass_bool']}`; "
                 "per-variant max numeric diff and count identity in "
                 "`DLH_5K_REPRODUCIBILITY.json`.")
    lines.append("")

    lines.append("## Forbidden operations")
    lines.append("")
    lines.append(f"Persisted in `DLH_5K_FORBIDDEN_OPERATION_CHECK.md`. Stationary marker: "
                 f"`{NOT_AUTHORIZED_MARKER}`. No source/model equation changed; no new grid; "
                 "no b extent beyond b160; no adaptive/root-seeking; no clipping; no stationary "
                 "KFE / nullspace / pin / density / tail / C-L-A-B; no D1-D3; no regional / "
                 "multi-province GE; no province audit; no network training; no nominal HANK.")
    return "\n".join(lines)


def _render_forbidden_check(cfg: DLH5KConfig, term: dict) -> str:
    lines = [
        "# DLH-5K — Forbidden-Operation / Scope Check (Issue #37)",
        "",
        "DSH did NOT perform any of the following during DLH-5K execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |",
        "| Modify `final_coupled_b_extent_diagnostic.py` | NOT performed (read-only reference) |",
        "| Modify taper / transfer FOC / adjustment cost / boundary law | NOT performed |",
        "| Modify economics / prices / parameters / tolerances / initialization | NOT performed (frozen D0) |",
        "| Add any new grid | NOT performed (exact accepted J0-J5 only) |",
        "| Add any new b extent or b > b160 | NOT performed (b160 hard ceiling) |",
        "| Add b180/b200 | NOT performed |",
        "| Adaptive / root-seeking grid | NOT performed |",
        "| New a resolution | NOT performed (a77/a153 only) |",
        "| b-resolution change | NOT performed (db=7/19 frozen) |",
        "| Rerun b100 as an extra variant | NOT performed (not required; not run) |",
        "| Warm start | NOT performed (fresh initialization per variant) |",
        "| Clip policy | NOT performed |",
        "| Run stationary KFE / nullspace / pin / density / tail / C-L-A-B | NOT performed (policy-only) |",
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
    parser = argparse.ArgumentParser(description="DLH-5K high-wealth corner-closure adjudication (Issue #37)")
    parser.add_argument("--config", default="configs/dlh_5k_high_wealth_corner_closure_diagnostic.toml")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    root = pathlib.Path(cfg.output_root)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"output root already exists (no-overwrite): {root}")
    dlh5b, params, numerics = build_fixture(cfg)
    runs = run_all_variants(cfg, dlh5b, params, numerics)
    runs["params"] = params
    runs["grids"] = build_all_grids(cfg, np.asarray(dlh5b.z, dtype=float),
                                    np.asarray(dlh5b.switch_matrix, dtype=float))[0]
    audit = source_law_audit(cfg)
    repro_accepted = check_accepted_j_reproduction(cfg, runs)
    decomps = offender_decomposition(cfg, runs)
    local = boundary_interior_localization(cfg, runs)
    feasible = joint_corner_feasibility(cfg, runs, decomps)
    cross_a = cross_a_mechanism(cfg, runs)
    repro = reproduce(cfg, dlh5b, params, numerics)
    term = overall_terminal(cfg, repro_accepted, repro, local["classifications"], decomps, cross_a)
    write_evidence(root, cfg, audit, runs, repro_accepted, decomps, local, feasible,
                   cross_a, repro, term)
    print(f"artifacts written under {root}")
    print(f"terminal = {term['terminal']}")
    if term["annotations"]:
        print("annotations = " + ", ".join(term["annotations"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
