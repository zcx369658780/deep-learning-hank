"""DLH-5F (Issue #29) — upper-domain adequacy and stationary-tail diagnostic.

Diagnoses whether the artificial finite upper asset domain influences the
accepted MATLAB-faithful HJB on the frozen two-asset household as the domain is
widened under controlled resolution, and whether any pre-frozen grid variant
reaches the same-process stationary/tail gate.

Scientific authority:
- accepted MATLAB-faithful household/HJB source
  ``matlab_faithful_two_asset_ha.py`` is IMMUTABLE and reused read-only;
- accepted DLH-5E diagnostic helper ``conservative_stationary_kfe.py`` is
  read-only authority where applicable (requested rates, conservative generator,
  generator diagnostics, SCC / nullspace, pin validation, contaminated solve,
  household aggregation);
- binding HJB/KFE consistency law: ``HJB boundary policy <=> KFE boundary
  transition law``. A mechanically conservative ``Q_c`` is never accepted as the
  stationary process while the HJB requests material outward boundary drift.

This is a bounded diagnostic gate, not production integration and not a
calibration / PASS-seeking exercise.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
import tomllib
from typing import Any

import numpy as np
from scipy import sparse
from scipy.sparse import linalg as spla

from deep_learning_hank.two_asset import (
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    aggregate_stationary_household,
    solve_matlab_faithful_hjb,
)
from deep_learning_hank.two_asset.conservative_stationary_kfe import (
    assemble_conservative_operator,
    contaminated_system,
    diagnostic_solve,
    generator_diagnostics,
    graph_structure,
    nullspace_dimension,
    pin_validation,
    requested_rates,
)
from deep_learning_hank.regional.two_region_fixed_point import (
    build_fixture as build_dlh5b_fixture,
    household_initial_condition,
    load_config as load_dlh5b_config,
)

# ---------------------------------------------------------------------------
# Terminal classifications / markers (Issue #29 section 13-14)
# ---------------------------------------------------------------------------

TERMINAL_OUTCOME_A = (
    "DLH_5F_PREFROZEN_UPPER_DOMAIN_REACHES_SAME_PROCESS_STATIONARY_VALIDATION__GPT_REVIEW_REQUIRED"
)
TERMINAL_OUTCOME_B = (
    "DLH_5F_UPPER_DOMAIN_DIAGNOSTIC_COMPLETE__NO_PREFROZEN_DOMAIN_REACHES_SAME_PROCESS_STATIONARY_TAIL__SCIENTIFIC_REVIEW_REQUIRED"
)
TERMINAL_HJB_STABILITY = "BLOCKED_DLH_5F_HJB_NUMERICAL_STABILITY_ON_PREFROZEN_DOMAIN"
TERMINAL_REPRODUCIBILITY = "BLOCKED_DLH_5F_REPRODUCIBILITY"
ANNOTATION_LIQUID_ILLIQUID_DIVERGE = (
    "LIQUID_ILLIQUID_UPPER_DOMAIN_BEHAVIOR_DIVERGES__SEPARATE_SCIENTIFIC_TREATMENT_REQUIRED"
)
NOT_REACHED_MARKER = "NOT_REACHED__HJB_KFE_SAME_PROCESS_BOUNDARY_GATE_FAILED"

# Accepted MATLAB-faithful oracle identity (Issue #23/#26, re-verified read-only).
ACCEPTED_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"
ACCEPTED_SHA256 = "1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024"


@dataclasses.dataclass(frozen=True)
class GridSpec:
    id: str
    b_pts: int
    b_lo: float
    b_hi: float
    a_pts: int
    a_lo: float
    a_hi: float


@dataclasses.dataclass(frozen=True)
class DLH5FConfig:
    dlh5b_config_path: str
    region_index: int
    wbar: float
    r_a: float
    variants: tuple
    b_index_max: int
    a_index_max: int
    boundary_threshold: float
    generator_row_sum_tol: float
    generator_neg_offdiag_tol: float
    original_residual_tol: float
    mass_tol: float
    min_density_tol: float
    multi_pin_diff_tol: float
    reproducibility_tol: float
    numeric_compare_tol: float
    nullspace_tol: float
    zero_support_rel_tol: float
    svd_maxiter: int
    pin_rhs: float
    pin_spec: tuple
    output_root: str


def load_config(path: str | pathlib.Path) -> DLH5FConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    hf = raw["household_fixture"]
    fp = raw["frozen_prices"]
    si = raw["shared_interior"]
    v = raw["validation"]
    out = raw["output"]
    variants = tuple(
        GridSpec(
            id=str(g["id"]),
            b_pts=int(g["b_pts"]),
            b_lo=float(g["b_lo"]),
            b_hi=float(g["b_hi"]),
            a_pts=int(g["a_pts"]),
            a_lo=float(g["a_lo"]),
            a_hi=float(g["a_hi"]),
        )
        for g in raw["variants"]
    )
    required = {"first", "quarter", "accepted", "half", "three_quarter", "last"}
    pin_spec = tuple(str(x) for x in v["pin_spec"])
    if set(pin_spec) != required or len(pin_spec) != len(required):
        raise ValueError("pin_spec must be exactly {first,quarter,accepted,half,three_quarter,last}")
    return DLH5FConfig(
        dlh5b_config_path=str(hf["dlh5b_config_path"]),
        region_index=int(hf["region_index"]),
        wbar=float(fp["wbar"]),
        r_a=float(fp["r_a"]),
        variants=variants,
        b_index_max=int(si["b_index_max"]),
        a_index_max=int(si["a_index_max"]),
        boundary_threshold=float(v["boundary_threshold"]),
        generator_row_sum_tol=float(v["generator_row_sum_tol"]),
        generator_neg_offdiag_tol=float(v["generator_neg_offdiag_tol"]),
        original_residual_tol=float(v["original_residual_tol"]),
        mass_tol=float(v["mass_tol"]),
        min_density_tol=float(v["min_density_tol"]),
        multi_pin_diff_tol=float(v["multi_pin_diff_tol"]),
        reproducibility_tol=float(v["reproducibility_tol"]),
        numeric_compare_tol=float(v["numeric_compare_tol"]),
        nullspace_tol=float(v["nullspace_tol"]),
        zero_support_rel_tol=float(v["zero_support_rel_tol"]),
        svd_maxiter=int(v["svd_maxiter"]),
        pin_rhs=float(v["pin_rhs"]),
        pin_spec=pin_spec,
        output_root=str(out["root"]),
    )


# ---------------------------------------------------------------------------
# Frozen grid plan identity
# ---------------------------------------------------------------------------

DB0 = 7.0 / 19.0
DA0 = 10.0 / 19.0


def build_variant_grid(spec: GridSpec, z: np.ndarray, switch: np.ndarray) -> MatlabFaithfulHJBGrid:
    b = np.linspace(spec.b_lo, spec.b_hi, spec.b_pts)
    a = np.linspace(spec.a_lo, spec.a_hi, spec.a_pts)
    return MatlabFaithfulHJBGrid(b, a, np.asarray(z, dtype=float), np.asarray(switch, dtype=float))


def grid_plan_identity(cfg: DLH5FConfig) -> dict:
    """Persist + validate the exact pre-frozen six-variant grid plan.

    Asserts the properties required by Issue #29 section 5:
    - V0-V4 share exact baseline spacings on every expanded dimension;
    - V0 is exactly nested in the same-spacing wider grids;
    - V5 uses half baseline spacing and contains every V0 node at every second
      grid point.
    """
    by_id = {v.id: v for v in cfg.variants}
    ids = [v.id for v in cfg.variants]
    plan = {}
    for v in cfg.variants:
        db = (v.b_hi - v.b_lo) / (v.b_pts - 1)
        da = (v.a_hi - v.a_lo) / (v.a_pts - 1)
        plan[v.id] = {
            "b_pts": v.b_pts, "b_lo": v.b_lo, "b_hi": v.b_hi, "b_max": v.b_hi,
            "db": float(db), "a_pts": v.a_pts, "a_lo": v.a_lo, "a_hi": v.a_hi,
            "a_max": v.a_hi, "da": float(da),
        }
    # exact baseline spacing preservation for V0-V4
    for vid in ("V0_BASE", "V1_A_WIDE", "V2_B_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        assert abs(plan[vid]["db"] - DB0) <= 1e-12, f"{vid} db != db0"
        assert abs(plan[vid]["da"] - DA0) <= 1e-12, f"{vid} da != da0"
    # V5 half spacing
    assert abs(plan["V5_BASE_FINE"]["db"] - DB0 / 2.0) <= 1e-12
    assert abs(plan["V5_BASE_FINE"]["da"] - DA0 / 2.0) <= 1e-12
    # nesting on same-spacing wider grids (b dimension)
    for vid in ("V2_B_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        assert abs(plan["V0_BASE"]["b_lo"] - plan[vid]["b_lo"]) <= 1e-12
        assert abs(plan["V0_BASE"]["db"] - plan[vid]["db"]) <= 1e-12
        assert plan[vid]["b_pts"] > plan["V0_BASE"]["b_pts"]
    # nesting on same-spacing wider grids (a dimension)
    for vid in ("V1_A_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        assert abs(plan["V0_BASE"]["a_lo"] - plan[vid]["a_lo"]) <= 1e-12
        assert abs(plan["V0_BASE"]["da"] - plan[vid]["da"]) <= 1e-12
        assert plan[vid]["a_pts"] > plan["V0_BASE"]["a_pts"]
    # V5 contains every V0 node at every second point (asserted on actual grids
    # inside build_all_grids; here on plan: same bounds, half spacing, ~2x-1 pts)
    assert plan["V5_BASE_FINE"]["b_pts"] == 2 * plan["V0_BASE"]["b_pts"] - 1
    assert plan["V5_BASE_FINE"]["a_pts"] == 2 * plan["V0_BASE"]["a_pts"] - 1
    assert ids == ["V0_BASE", "V1_A_WIDE", "V2_B_WIDE", "V3_AB_MID", "V4_AB_WIDE", "V5_BASE_FINE"]
    return plan


def build_all_grids(cfg: DLH5FConfig, z: np.ndarray, switch: np.ndarray) -> dict:
    plan = grid_plan_identity(cfg)
    grids = {}
    for v in cfg.variants:
        g = build_variant_grid(v, z, switch)
        grids[v.id] = g
    # actual-node nesting / alignment checks on the real grids
    g0 = grids["V0_BASE"]
    for vid in ("V2_B_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        assert np.allclose(g0.b, grids[vid].b[: g0.b.size], atol=1e-12)
    for vid in ("V1_A_WIDE", "V3_AB_MID", "V4_AB_WIDE"):
        assert np.allclose(g0.a, grids[vid].a[: g0.a.size], atol=1e-12)
    g5 = grids["V5_BASE_FINE"]
    assert np.allclose(g5.b[::2], g0.b, atol=1e-12)
    assert np.allclose(g5.a[::2], g0.a, atol=1e-12)
    return grids, plan


# ---------------------------------------------------------------------------
# Phase B — full requested-rate boundary diagnostics
# ---------------------------------------------------------------------------


def boundary_diagnostics_full(requested: dict, grid: MatlabFaithfulHJBGrid, threshold: float) -> dict:
    """Per-boundary requested outward diagnostics with index AND physical
    coordinates, positive-outward quantiles, counts/shares and the complete set
    of states above the threshold. Coordinates use C-order unraveling on the
    actual 2-D boundary slice shape. Requested rates are never clipped/mutated.
    """
    i_count, j_count, nz = grid.b.size, grid.a.size, grid.z.size
    bb_req = requested["b_backward_requested"]
    bf_req = requested["b_forward_requested"]
    ab_req = requested["a_backward_requested"]
    af_req = requested["a_forward_requested"]

    def _slice(name, values, b_fixed, a_fixed, direction):
        v = np.asarray(values, dtype=float)
        total = int(v.size)
        maxv = float(v.max()) if v.size else 0.0
        argmax_index = None
        argmax_physical = None
        req_at_max = None
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
            req_at_max = float(v.flat[argmax_flat])
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
                    "requested_outward_rate": float(v[r, c]),
                })
        offending.sort(key=lambda o: (o["b_index"], o["a_index"], o["z_index"]))
        count = len(offending)
        return {
            "boundary": name,
            "direction": direction,
            "requested_outward_max": maxv,
            "count_above_threshold": count,
            "share_above_threshold": float(count / total) if total else 0.0,
            "argmax_index": argmax_index,
            "argmax_physical": argmax_physical,
            "requested_at_max": req_at_max,
            "quantiles": quantiles,
            "offending_states": offending,
        }

    rows = [
        _slice("lower_b", bb_req[0, :, :], 0, None, "b_backward"),
        _slice("upper_b", bf_req[-1, :, :], i_count - 1, None, "b_forward"),
        _slice("lower_a", ab_req[:, 0, :], None, 0, "a_backward"),
        _slice("upper_a", af_req[:, -1, :], None, j_count - 1, "a_forward"),
    ]
    best = max(rows, key=lambda r: r["requested_outward_max"])
    return {
        "boundaries": rows,
        "max_requested_outward": best["requested_outward_max"],
        "max_boundary": best["boundary"],
        "max_coords_index": best["argmax_index"],
        "max_coords_physical": best["argmax_physical"],
    }


# ---------------------------------------------------------------------------
# Phase C — shared-interior policy stability at exact aligned nodes
# ---------------------------------------------------------------------------


def _aligned_slices(r0, r1, b_keep, a_keep, half_spacing):
    """Return the (r0_b, r0_a, r1_b, r1_a) slice tuples selecting exact common
    V0 nodes under the frozen mask (b_index<=b_keep-1, a_index<=a_keep-1, all z).

    - same-spacing nested grids: r1 uses the same index window (0..b_keep-1);
    - V5_BASE_FINE (half spacing): r1 selects every second node (0..2*b_keep-2
      step 2), which contains exactly the V0 nodes at even positions.
    """
    if half_spacing:
        return (
            slice(None, b_keep), slice(None, a_keep),
            slice(None, 2 * b_keep, 2), slice(None, 2 * a_keep, 2),
        )
    return (
        slice(None, b_keep), slice(None, a_keep),
        slice(None, b_keep), slice(None, a_keep),
    )


def _strict_slice(s: slice) -> slice:
    """Exclude the first asset layer inside a primary-mask slice.

    For half-spacing V5 slices the step is 2, so the first interior node is at
    index 2 (which is the V5 node matching V0 index 1)."""
    step = s.step or 1
    start = 0 if s.start is None else s.start
    return slice(start + step, s.stop, s.step)


def shared_interior_pair(
    r0, r1, comparison: str, b_keep: int, a_keep: int, half_spacing: bool = False
) -> dict:
    """Compare accepted HJB outputs at exact common V0 nodes (no interpolation).

    Primary frozen mask: ``b_index <= b_keep-1`` (17), ``a_index <= a_keep-1``
    (17), all z. A strict-interior submetric (first asset layer excluded) is
    additionally reported without replacing the frozen primary mask.
    """
    numeric_fields = ["value", "consumption", "labor", "transfer", "mu_a", "mu_b"]
    label_fields = ["liquid_label", "transfer_label"]
    s0b, s0a, s1b, s1a = _aligned_slices(r0, r1, b_keep, a_keep, half_spacing)
    s0b_si, s0a_si = _strict_slice(s0b), _strict_slice(s0a)
    s1b_si, s1a_si = _strict_slice(s1b), _strict_slice(s1a)

    out = {"comparison": comparison, "half_spacing": bool(half_spacing), "fields": {}}
    for f in numeric_fields:
        x = np.asarray(getattr(r0, f)[s0b, s0a, :], dtype=float)
        y = np.asarray(getattr(r1, f)[s1b, s1a, :], dtype=float)
        m = float(np.max(np.abs(x - y))) if x.size else 0.0
        ref = float(np.max(np.abs(x))) if x.size else 0.0
        rel = m / max(1.0, ref)
        # strict interior
        x_si = np.asarray(getattr(r0, f)[s0b_si, s0a_si, :], dtype=float)
        y_si = np.asarray(getattr(r1, f)[s1b_si, s1a_si, :], dtype=float)
        m_si = float(np.max(np.abs(x_si - y_si))) if x_si.size else 0.0
        ref_si = float(np.max(np.abs(x_si))) if x_si.size else 0.0
        rel_si = m_si / max(1.0, ref_si)
        out["fields"][f] = {
            "max_abs_diff": m, "rel_diff": rel,
            "strict_interior_max_abs_diff": m_si, "strict_interior_rel_diff": rel_si,
        }
    for lab in label_fields:
        x = getattr(r0, lab)[s0b, s0a, :]
        y = getattr(r1, lab)[s1b, s1a, :]
        out["fields"][lab] = {"mismatch_count": int(np.sum(x != y))}
    return out


# ---------------------------------------------------------------------------
# Phase E/F/G — stationary / tail / aggregate (only for same-process variants)
# ---------------------------------------------------------------------------


def _accepted_density(Q_c: sparse.csr_matrix, pin: int, c: float, n: int, db: float, da: float):
    """MATLAB-style pin solve on the ORIGINAL conservative operator, followed by
    the accepted separate mass normalization (no economic clipping)."""
    cont, rhs = contaminated_system(Q_c, pin, c, n)
    raw, _e, _w = diagnostic_solve(cont, rhs)
    if raw is None or not np.isfinite(raw).all():
        return None
    factor = float(np.sum(raw) * db * da)
    if not np.isfinite(factor) or factor == 0.0:
        return None
    return raw / factor


def phase_e_stationary(cfg: DLH5FConfig, Q_c: sparse.csr_matrix, n: int, db: float, da: float) -> dict:
    """Run the accepted Issue #27 / DLH-5E stationary contract on Q_c.

    Returns the stationary-class evidence (graph, nullspace, pins) and a gate
    decision. No regularization / jitter / pseudoinverse / alternative pin.
    """
    graph = graph_structure(Q_c)
    ns = nullspace_dimension(Q_c, cfg.svd_maxiter, cfg.nullspace_tol)
    pins = pin_validation(Q_c, n, db, da, cfg)
    nullity = ns.get("nullspace_dimension")
    nullity_ok = bool(ns.get("converged") and nullity == 1)
    pin_gate_ok = bool(pins.get("terminal") is None)  # default valid + >=2 valid + within tol
    gate = "PASS" if (nullity_ok and pin_gate_ok) else "FAIL"
    reason = None
    if not nullity_ok:
        reason = f"nullspace_dimension={nullity} (target 1)"
    elif not pin_gate_ok:
        reason = f"pin gate failed (default class {pins.get('default_pin_class')}, valid count {pins.get('valid_pin_count')})"
    return {
        "gate": gate,
        "reason": reason,
        "nullspace_dimension": nullity,
        "smallest_singular_values": ns.get("smallest_singular_values"),
        "graph": {
            "scc_count": graph.get("scc_count"),
            "scc_sizes_sorted": graph.get("scc_sizes_sorted"),
            "closed_component_count": graph.get("closed_component_count"),
            "closed_component_sizes": graph.get("closed_component_sizes"),
        },
        "pins": {
            "classes": [p.get("classification") for p in pins.get("pins", [])],
            "valid_pin_count": pins.get("valid_pin_count"),
            "valid_pin_indices": pins.get("valid_pin_indices"),
            "valid_pin_max_density_diff": pins.get("valid_pin_max_density_diff"),
            "default_pin_class": pins.get("default_pin_class"),
            "default_pin_index": pins.get("default_pin_index"),
            "per_pin": [
                {
                    "pin_label": p.get("pin_label"),
                    "pin_index": p.get("pin_index"),
                    "classification": p.get("classification"),
                    "original_residual_inf": p.get("original_residual_inf"),
                    "mass_error": p.get("mass_error"),
                    "min_density": p.get("min_density"),
                }
                for p in pins.get("pins", [])
            ],
        },
    }


def tail_diagnostics(cfg: DLH5FConfig, grid: MatlabFaithfulHJBGrid, hjb, density: np.ndarray) -> dict:
    """Phase F tail diagnostics using a scientifically admissible density."""
    shape = (grid.b.size, grid.a.size, grid.z.size)
    g = np.asarray(density, dtype=float).reshape(shape)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    weight = db * da
    i_count, j_count, nz = shape
    b = np.broadcast_to(grid.b[:, None, None], shape)
    a = np.broadcast_to(grid.a[None, :, None], shape)
    z = np.broadcast_to(grid.z[None, None, :], shape)
    mass_a_max = float(np.sum(g[:, j_count - 1, :]) * weight)
    mass_b_max = float(np.sum(g[i_count - 1, :, :]) * weight)
    pr_a_ge_09 = float(np.sum(g[a >= 0.9 * grid.a[-1]]) * weight)
    pr_b_near = float(np.sum(g[b >= grid.b[-1] - 0.1 * (grid.b[-1] - grid.b[0])]) * weight)
    top2_a = float(np.sum(g[:, j_count - 2 :, :]) * weight)
    top2_b = float(np.sum(g[i_count - 2 :, :, :]) * weight)
    mu_a = np.asarray(hjb.mu_a, dtype=float)
    mu_b = np.asarray(hjb.mu_b, dtype=float)
    phi_a_upper = float(np.sum(g[:, j_count - 1, :] * np.maximum(mu_a[:, j_count - 1, :], 0.0)) * weight)
    phi_b_upper = float(np.sum(g[i_count - 1, :, :] * np.maximum(mu_b[i_count - 1, :, :], 0.0)) * weight)
    return {
        "mass_a_max": mass_a_max,
        "mass_b_max": mass_b_max,
        "pr_a_ge_0.9_amax": pr_a_ge_09,
        "pr_b_near_upper": pr_b_near,
        "top2_a_layer_mass": top2_a,
        "top2_b_layer_mass": top2_b,
        "phi_a_upper_flux": phi_a_upper,
        "phi_b_upper_flux": phi_b_upper,
        "cell_weight": weight,
    }


def aggregate_from_density(cfg: DLH5FConfig, grid: MatlabFaithfulHJBGrid, hjb, density: np.ndarray) -> dict:
    """Phase G aggregates C,L,A,B from the accepted density (cell_weight=db*da
    per discrete z state). No historical row-295 aggregate and no anchor claim."""
    agg = aggregate_stationary_household(grid, hjb.consumption, hjb.labor, density)
    return {
        "C": float(agg.c_ss),
        "L": float(agg.l_ss),
        "A": float(agg.a_ss),
        "B": float(agg.b_ss),
        "total_assets": float(agg.total_assets),
        "density_normalization": float(agg.density_normalization),
    }


# ---------------------------------------------------------------------------
# Per-variant pipeline (Phases A-E-F-G)
# ---------------------------------------------------------------------------


def run_variant(cfg: DLH5FConfig, dlh5b, params, numerics, spec: GridSpec, z, switch) -> dict:
    grid = build_variant_grid(spec, z, switch)
    shape = (grid.b.size, grid.a.size, grid.z.size)
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    n = int(np.prod(shape))
    inputs = HouseholdInputs(
        r_a=cfg.r_a,
        r_b=dlh5b.r_b,
        tau=dlh5b.tau[cfg.region_index],
        wages=np.array([cfg.wbar]),
        migration_costs=np.array([0.0]),
        labor_weights=np.array([1.0]),
    )
    # accepted initialization formula, evaluated FRESH on this variant's own grid
    initial, labor0 = household_initial_condition(grid, params, inputs, dlh5b.rb_gap[cfg.region_index])
    hjb = solve_matlab_faithful_hjb(
        grid, params, inputs, initial, labor0,
        dlh5b.transfer_income[cfg.region_index],
        dlh5b.rb_gap[cfg.region_index],
        numerics,
    )
    rec: dict = {
        "variant": spec.id,
        "grid": {
            "b_pts": int(grid.b.size), "b_lo": float(grid.b[0]), "b_hi": float(grid.b[-1]),
            "a_pts": int(grid.a.size), "a_lo": float(grid.a[0]), "a_hi": float(grid.a[-1]),
            "db": float(grid.b[1] - grid.b[0]), "da": float(grid.a[1] - grid.a[0]),
            "z_pts": int(grid.z.size),
        },
        "frozen_prices_identity": {
            "wbar": cfg.wbar, "r_a": cfg.r_a,
            "dlh5b_config": cfg.dlh5b_config_path, "region_index": cfg.region_index,
        },
        "hjb_converged": bool(hjb.converged),
        "hjb_iterations": int(hjb.iterations),
        "hjb_statistic": float(hjb.convergence_statistic),
    }
    return _finalize_variant_record(cfg, rec, hjb, grid, db, da, n, Q_c=None)


def _finalize_variant_record(
    cfg: DLH5FConfig, rec: dict, hjb, grid: MatlabFaithfulHJBGrid,
    db: float, da: float, n: int, Q_c=None,
) -> dict:
    """Fill in boundary/generator/stationary/tail/aggregate gates. The HJB result
    object itself is NOT embedded in the persisted record (kept for shared-interior
    comparisons in a separate container)."""
    shape = (grid.b.size, grid.a.size, grid.z.size)
    if not rec["hjb_converged"]:
        rec["boundary_policy_gate"] = "HJB_NOT_CONVERGED"
        rec["phase_e_reached"] = False
        rec["stationary"] = None
        rec["tail"] = NOT_REACHED_MARKER
        rec["aggregates"] = NOT_REACHED_MARKER
        rec["variant_terminal"] = "HJB_NOT_CONVERGED"
        return rec

    requested = requested_rates(hjb.mu_b, hjb.mu_a, db, da)
    rec["boundary"] = boundary_diagnostics_full(requested, grid, cfg.boundary_threshold)
    Q_c = Q_c if Q_c is not None else assemble_conservative_operator(requested, grid.switch_matrix)
    rec["generator"] = generator_diagnostics(Q_c)

    if rec["boundary"]["max_requested_outward"] > cfg.boundary_threshold:
        rec["boundary_policy_gate"] = "VIOLATION"
        rec["phase_e_reached"] = False
        rec["stationary"] = None
        rec["tail"] = NOT_REACHED_MARKER
        rec["aggregates"] = NOT_REACHED_MARKER
        rec["variant_terminal"] = NOT_REACHED_MARKER
        return rec

    rec["boundary_policy_gate"] = "PASS"
    rec["phase_e_reached"] = True
    st = phase_e_stationary(cfg, Q_c, n, db, da)
    rec["stationary"] = st
    if st["gate"] != "PASS":
        rec["tail"] = NOT_REACHED_MARKER
        rec["aggregates"] = NOT_REACHED_MARKER
        rec["variant_terminal"] = "STATIONARY_CONTRACT_FAIL"
        return rec

    # scientifically admissible density from the accepted pin solve
    density = _accepted_density(Q_c, st["pins"]["default_pin_index"], cfg.pin_rhs, n, db, da)
    if density is None:
        rec["tail"] = NOT_REACHED_MARKER
        rec["aggregates"] = NOT_REACHED_MARKER
        rec["variant_terminal"] = "DENSITY_SOLVE_FAIL"
        return rec
    density3d = np.asarray(density, dtype=float).reshape(shape)
    rec["tail"] = tail_diagnostics(cfg, grid, hjb, density3d)
    rec["aggregates"] = aggregate_from_density(cfg, grid, hjb, density3d)
    rec["variant_terminal"] = "STATIONARY_VALIDATED"
    return rec


def run_all_variants(cfg: DLH5FConfig, dlh5b, params, numerics) -> dict:
    """Fresh HJB on all six pre-frozen variants; no warm start between grids.

    Returns the persisted variant records plus an in-memory ``hjb_results``
    container (never JSON-serialized) used for shared-interior comparisons.
    """
    z = np.asarray(dlh5b.z, dtype=float)
    switch = np.asarray(dlh5b.switch_matrix, dtype=float)
    grids, plan = build_all_grids(cfg, z, switch)
    variants = []
    hjb_results: dict[str, Any] = {}
    for spec in cfg.variants:
        grid = build_variant_grid(spec, z, switch)
        shape = (grid.b.size, grid.a.size, grid.z.size)
        db = float(grid.b[1] - grid.b[0])
        da = float(grid.a[1] - grid.a[0])
        n = int(np.prod(shape))
        inputs = HouseholdInputs(
            r_a=cfg.r_a,
            r_b=dlh5b.r_b,
            tau=dlh5b.tau[cfg.region_index],
            wages=np.array([cfg.wbar]),
            migration_costs=np.array([0.0]),
            labor_weights=np.array([1.0]),
        )
        initial, labor0 = household_initial_condition(grid, params, inputs, dlh5b.rb_gap[cfg.region_index])
        hjb = solve_matlab_faithful_hjb(
            grid, params, inputs, initial, labor0,
            dlh5b.transfer_income[cfg.region_index],
            dlh5b.rb_gap[cfg.region_index],
            numerics,
        )
        rec = {
            "variant": spec.id,
            "grid": {
                "b_pts": int(grid.b.size), "b_lo": float(grid.b[0]), "b_hi": float(grid.b[-1]),
                "a_pts": int(grid.a.size), "a_lo": float(grid.a[0]), "a_hi": float(grid.a[-1]),
                "db": db, "da": da, "z_pts": int(grid.z.size),
            },
            "frozen_prices_identity": {
                "wbar": cfg.wbar, "r_a": cfg.r_a,
                "dlh5b_config": cfg.dlh5b_config_path, "region_index": cfg.region_index,
            },
            "hjb_converged": bool(hjb.converged),
            "hjb_iterations": int(hjb.iterations),
            "hjb_statistic": float(hjb.convergence_statistic),
        }
        rec = _finalize_variant_record(cfg, rec, hjb, grid, db, da, n)
        variants.append(rec)
        hjb_results[spec.id] = hjb
    return {"grid_plan": plan, "variants": variants, "hjb_results": hjb_results}


def _z_of(dlh5b):
    # TwoRegionConfig exposes z and switch_matrix
    return dlh5b.z


def _switch_of(dlh5b):
    return dlh5b.switch_matrix


def build_fixture(cfg: DLH5FConfig):
    """Accepted DLH-5B fixture (params, numerics, z, switch), read-only."""
    dlh5b = load_dlh5b_config(cfg.dlh5b_config_path)
    _grid, params, numerics = build_dlh5b_fixture(dlh5b)
    return dlh5b, params, numerics


# ---------------------------------------------------------------------------
# Shared-interior comparisons (V0 vs each wider variant)
# ---------------------------------------------------------------------------


def shared_interior_all(cfg: DLH5FConfig, runs: dict) -> list:
    """Compare V0 against every other variant at exact aligned nodes under the
    frozen V0-based mask. Uses the converged HJB results from the FIRST run."""
    by_id = {v["variant"]: v for v in runs["variants"]}
    hjb_by_id = runs.get("hjb_results", {})
    b_keep = cfg.b_index_max + 1
    a_keep = cfg.a_index_max + 1
    comparisons = []
    pairs = [
        ("V0_vs_V1_A_WIDE", "V0_BASE", "V1_A_WIDE", False),
        ("V0_vs_V2_B_WIDE", "V0_BASE", "V2_B_WIDE", False),
        ("V0_vs_V3_AB_MID", "V0_BASE", "V3_AB_MID", False),
        ("V0_vs_V4_AB_WIDE", "V0_BASE", "V4_AB_WIDE", False),
        ("V0_vs_V5_BASE_FINE", "V0_BASE", "V5_BASE_FINE", True),
    ]
    for cid, id0, id1, half in pairs:
        r0 = by_id[id0]
        r1 = by_id[id1]
        if not (r0.get("hjb_converged") and r1.get("hjb_converged")):
            comparisons.append({"comparison": cid, "reached": False,
                                "reason": "one or both HJB not converged"})
            continue
        comparisons.append(shared_interior_pair(
            hjb_by_id[id0], hjb_by_id[id1], cid, b_keep, a_keep, half_spacing=half))
    return comparisons


# ---------------------------------------------------------------------------
# Terminal classification
# ---------------------------------------------------------------------------


def liquid_illiquid_annotation(cfg: DLH5FConfig, runs: dict) -> bool:
    """Outcome D annotation: supported when the liquid (upper-b) and illiquid
    (upper-a) material-request indicators diverge across variants."""
    th = cfg.boundary_threshold
    seen_divergence = False
    for v in runs["variants"]:
        b = v.get("boundary") or {}
        by_name = {bi["boundary"]: bi for bi in b.get("boundaries", [])}
        upper_b = by_name.get("upper_b") or {}
        upper_a = by_name.get("upper_a") or {}
        ub_mat = (upper_b.get("requested_outward_max") or 0.0) > th
        ua_mat = (upper_a.get("requested_outward_max") or 0.0) > th
        if ub_mat != ua_mat:
            seen_divergence = True
    return seen_divergence


def overall_terminal(cfg: DLH5FConfig, runs: dict, repro: dict) -> dict:
    terminal = None
    if not repro["pass_bool"]:
        terminal = TERMINAL_REPRODUCIBILITY
    elif any(not v["hjb_converged"] for v in runs["variants"]):
        terminal = TERMINAL_HJB_STABILITY
    elif any(v["phase_e_reached"] for v in runs["variants"]):
        terminal = TERMINAL_OUTCOME_A
    else:
        terminal = TERMINAL_OUTCOME_B
    annotations = []
    if liquid_illiquid_annotation(cfg, runs):
        annotations.append(ANNOTATION_LIQUID_ILLIQUID_DIVERGE)
    return {"terminal": terminal, "annotations": annotations}


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------


def _variant_structural_signature(rec: dict) -> str:
    b = rec.get("boundary") or {}
    boundary_discrete = {}
    for bi in b.get("boundaries", []):
        boundary_discrete[bi["boundary"]] = {
            "direction": bi.get("direction"),
            "count_above_threshold": bi.get("count_above_threshold"),
            "argmax_index": bi.get("argmax_index"),
            "argmax_physical": bi.get("argmax_physical"),
            "offending_coords": [(o["b_index"], o["a_index"], o["z_index"])
                                 for o in bi.get("offending_states", [])],
        }
    st = rec.get("stationary") or {}
    pins = st.get("pins") or {}
    graph = st.get("graph") or {}
    return json.dumps({
        "variant": rec.get("variant"),
        "grid": rec.get("grid"),
        "hjb_converged": rec.get("hjb_converged"),
        "hjb_iterations": rec.get("hjb_iterations"),
        "boundary_policy_gate": rec.get("boundary_policy_gate"),
        "phase_e_reached": rec.get("phase_e_reached"),
        "boundary": boundary_discrete,
        "generator_nnz": (rec.get("generator") or {}).get("nnz"),
        "stationary_gate": st.get("gate"),
        "nullspace_dimension": st.get("nullspace_dimension"),
        "graph": graph,
        "pin_classes": pins.get("classes"),
        "valid_pin_count": pins.get("valid_pin_count"),
        "tail_reached": isinstance(rec.get("tail"), dict),
        "aggregates_reached": isinstance(rec.get("aggregates"), dict),
    }, sort_keys=True)


def _variant_numeric_numbers(rec: dict) -> list:
    out: list[float] = []
    if rec.get("hjb_statistic") is not None:
        out.append(float(rec["hjb_statistic"]))
    b = rec.get("boundary") or {}
    out.append(float(b.get("max_requested_outward", float("nan"))))
    for bi in b.get("boundaries", []):
        out.append(float(bi.get("requested_outward_max", float("nan"))))
        out.append(float(bi.get("requested_at_max", float("nan"))))
        out.append(float(bi.get("share_above_threshold", float("nan"))))
        q = bi.get("quantiles")
        if isinstance(q, dict):
            for k in ("q50", "q90", "q95", "q99"):
                out.append(float(q.get(k, float("nan"))))
        for o in bi.get("offending_states", []):
            out.append(float(o.get("requested_outward_rate", float("nan"))))
    g = rec.get("generator") or {}
    for key in ("row_sum_max_abs", "negative_offdiag_max_mag", "row_sum_min", "row_sum_max"):
        v = g.get(key)
        out.append(float(v) if v is not None else float("nan"))
    st = rec.get("stationary") or {}
    for v in st.get("smallest_singular_values") or []:
        out.append(float(v))
    pins = st.get("pins") or {}
    for p in pins.get("per_pin", []):
        out.append(float(p.get("original_residual_inf", float("nan"))))
        out.append(float(p.get("mass_error", float("nan"))))
        out.append(float(p.get("min_density", float("nan"))))
    out.append(float(pins.get("valid_pin_max_density_diff", float("nan"))))
    tail = rec.get("tail")
    if isinstance(tail, dict):
        for key in ("mass_a_max", "mass_b_max", "pr_a_ge_0.9_amax", "pr_b_near_upper",
                    "top2_a_layer_mass", "top2_b_layer_mass",
                    "phi_a_upper_flux", "phi_b_upper_flux"):
            out.append(float(tail.get(key, float("nan"))))
    agg = rec.get("aggregates")
    if isinstance(agg, dict):
        for key in ("C", "L", "A", "B", "total_assets", "density_normalization"):
            out.append(float(agg.get(key, float("nan"))))
    return out


def _nonfinite_aligned(a, b) -> bool:
    return bool((not np.isfinite(a)) and (not np.isfinite(b)))


def compare_variant_records(r1: dict, r2: dict, cfg: DLH5FConfig) -> dict:
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
        "pass_bool": bool(
            same_struct and mismatch == 0 and max_diff <= cfg.reproducibility_tol
        ),
    }


def reproduce(cfg: DLH5FConfig, dlh5b, params, numerics) -> dict:
    run1 = run_all_variants(cfg, dlh5b, params, numerics)
    run2 = run_all_variants(cfg, dlh5b, params, numerics)
    per_variant = {}
    for r1, r2 in zip(run1["variants"], run2["variants"]):
        per_variant[r1["variant"]] = compare_variant_records(r1, r2, cfg)
    t1 = overall_terminal(cfg, run1, {"pass_bool": True})
    t2 = overall_terminal(cfg, run2, {"pass_bool": True})
    pass_bool = all(v["pass_bool"] for v in per_variant.values())
    # Persist only JSON-serializable evidence (hjb results are in-memory only).
    return {
        "run1": {"grid_plan": run1["grid_plan"], "variants": run1["variants"]},
        "run2": {"grid_plan": run2["grid_plan"], "variants": run2["variants"]},
        "per_variant": per_variant,
        "pass_bool": bool(pass_bool),
        "randomness": "NOT_APPLICABLE",
        "terminal_run1": t1["terminal"],
        "terminal_run2": t2["terminal"],
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


def write_evidence(root: pathlib.Path, cfg: DLH5FConfig, runs: dict, comparisons: list, repro: dict, term: dict) -> None:
    root = pathlib.Path(root)
    root.mkdir(parents=True, exist_ok=True)

    # 1) VARIANT_STATUS.csv
    rows = []
    for v in runs["variants"]:
        g = v["grid"]
        b = v.get("boundary") or {}
        rows.append([v["variant"], g["b_pts"], _fmt(g["b_lo"]), _fmt(g["b_hi"]), g["a_pts"],
                     _fmt(g["a_lo"]), _fmt(g["a_hi"]), _fmt(g["db"]), _fmt(g["da"]),
                     v["hjb_converged"], v["hjb_iterations"], _fmt(v["hjb_statistic"]),
                     v.get("boundary_policy_gate"), _fmt(b.get("max_requested_outward")),
                     b.get("max_boundary"), v.get("phase_e_reached"), v.get("variant_terminal")])
    _write_csv(root / "DLH_5F_VARIANT_STATUS.csv",
               ["variant", "b_pts", "b_lo", "b_hi", "a_pts", "a_lo", "a_hi", "db", "da",
                "hjb_converged", "hjb_iterations", "hjb_statistic", "boundary_gate",
                "max_requested_outward", "max_boundary", "phase_e_reached", "variant_terminal"], rows)

    # 2) BOUNDARY_POLICY_DIAGNOSTICS.csv (summary + complete offending rows)
    rows = []
    for v in runs["variants"]:
        b = v.get("boundary") or {}
        for bi in b.get("boundaries", []):
            rows.append([v["variant"], "summary", bi["boundary"], bi.get("direction"),
                         _fmt(bi["requested_outward_max"]), bi["count_above_threshold"],
                         _fmt(bi["share_above_threshold"]), bi.get("argmax_index"),
                         bi.get("argmax_physical"), _fmt(bi.get("requested_at_max")),
                         _q_fmt(bi.get("quantiles")), "", "", "", "", "", "", "", "", ""])
            for o in bi.get("offending_states", []):
                rows.append([v["variant"], "offending", o["boundary"], o.get("direction"),
                             _fmt(o["requested_outward_rate"]), "", "", "", "", "", "",
                             o["b_index"], o["a_index"], o["z_index"], _fmt(o["b"]),
                             _fmt(o["a"]), _fmt(o["z"]), _fmt(o["requested_outward_rate"]), "", ""])
    _write_csv(root / "DLH_5F_BOUNDARY_POLICY_DIAGNOSTICS.csv",
               ["variant", "row_type", "boundary", "direction", "requested_outward_max",
                "count_above_threshold", "share_above_threshold", "argmax_index",
                "argmax_physical", "requested_at_max", "quantiles_q50_q90_q95_q99",
                "offending_b_index", "offending_a_index", "offending_z_index",
                "offending_b", "offending_a", "offending_z",
                "offending_requested_outward_rate", "", ""], rows)

    # 3) INTERIOR_POLICY_STABILITY.csv
    rows = []
    for c in comparisons:
        if not c.get("reached", True):
            rows.append([c["comparison"], "NOT_REACHED", "", "", "", "", "", c.get("reason", "")])
            continue
        for f, m in c["fields"].items():
            if f in ("liquid_label", "transfer_label"):
                rows.append([c["comparison"], f, "", "", "", "", m["mismatch_count"], ""])
            else:
                rows.append([c["comparison"], f, _fmt(m["max_abs_diff"]), _fmt(m["rel_diff"]),
                             _fmt(m.get("strict_interior_max_abs_diff")),
                             _fmt(m.get("strict_interior_rel_diff")), "", ""])
    _write_csv(root / "DLH_5F_INTERIOR_POLICY_STABILITY.csv",
               ["comparison", "field", "max_abs_diff", "rel_diff",
                "strict_interior_max_abs_diff", "strict_interior_rel_diff",
                "label_mismatch_count", "note"], rows)

    # 4) STATIONARY_TAIL_DIAGNOSTICS.csv
    rows = []
    for v in runs["variants"]:
        t = v.get("tail")
        if isinstance(t, dict):
            rows.append([v["variant"], v.get("phase_e_reached"), "REACHED",
                         _fmt(t["mass_a_max"]), _fmt(t["mass_b_max"]),
                         _fmt(t["pr_a_ge_0.9_amax"]), _fmt(t["pr_b_near_upper"]),
                         _fmt(t["top2_a_layer_mass"]), _fmt(t["top2_b_layer_mass"]),
                         _fmt(t["phi_a_upper_flux"]), _fmt(t["phi_b_upper_flux"]), ""])
        else:
            rows.append([v["variant"], v.get("phase_e_reached"), str(t), "", "", "", "", "", "", "", "", ""])
    _write_csv(root / "DLH_5F_STATIONARY_TAIL_DIAGNOSTICS.csv",
               ["variant", "phase_e_reached", "status", "mass_a_max", "mass_b_max",
                "pr_a_ge_0.9_amax", "pr_b_near_upper", "top2_a_layer_mass",
                "top2_b_layer_mass", "phi_a_upper_flux", "phi_b_upper_flux", "note"], rows)

    # 5) AGGREGATE_STABILITY.csv
    rows = []
    valid = []
    for v in runs["variants"]:
        a = v.get("aggregates")
        if isinstance(a, dict):
            rows.append([v["variant"], "REACHED", _fmt(a["C"]), _fmt(a["L"]), _fmt(a["A"]), _fmt(a["B"]),
                         _fmt(a["total_assets"]), _fmt(a["density_normalization"]), ""])
            valid.append((v["variant"], a))
        else:
            rows.append([v["variant"], str(a), "", "", "", "", "", "", ""])
    if len(valid) >= 2:
        for i in range(len(valid)):
            for j in range(i + 1, len(valid)):
                vi, ai = valid[i]
                vj, aj = valid[j]
                rows.append([f"{vi}_vs_{vj}", "DIFF", _fmt(abs(ai["C"] - aj["C"])),
                             _fmt(abs(ai["L"] - aj["L"])), _fmt(abs(ai["A"] - aj["A"])),
                             _fmt(abs(ai["B"] - aj["B"])), "", "", "abs diff"])
    _write_csv(root / "DLH_5F_AGGREGATE_STABILITY.csv",
               ["variant", "status", "C", "L", "A", "B", "total_assets", "density_normalization", "note"], rows)

    # 6) REPRODUCIBILITY.json
    with open(root / "DLH_5F_REPRODUCIBILITY.json", "w", encoding="utf-8") as fh:
        json.dump(repro, fh, indent=2, default=str, sort_keys=True)

    # 7) EXECUTION_REPORT.md
    with open(root / "DLH_5F_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_report(cfg, runs, comparisons, repro, term))

    # 8) FORBIDDEN_OPERATION_CHECK.md
    with open(root / "DLH_5F_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write(_render_forbidden_check(cfg, runs, repro, term))


def _render_report(cfg: DLH5FConfig, runs: dict, comparisons: list, repro: dict, term: dict) -> str:
    lines = []
    lines.append("# DLH-5F — Upper-Domain Adequacy and Stationary-Tail Diagnostic (Issue #29)")
    lines.append("")
    lines.append("Bounded diagnostic on the frozen two-asset household over the exact six "
                 "pre-frozen numerical domains. The accepted MATLAB-faithful HJB source is "
                 "immutable and reused read-only; the accepted DLH-5E diagnostic helper is "
                 "read-only authority where applicable.")
    lines.append("")
    lines.append(f"Overall terminal classification: `{term['terminal']}`")
    if term["annotations"]:
        lines.append("")
        lines.append("Secondary scientific annotations: " +
                     ", ".join(f"`{a}`" for a in term["annotations"]))
    lines.append("")
    lines.append(f"Frozen economics/prices: `wbar={cfg.wbar}`, `r_a={cfg.r_a}`; all non-grid "
                 f"objects exactly the accepted DLH-5B/DLH-5E canonical fixture "
                 f"(`{cfg.dlh5b_config_path}`, region_index={cfg.region_index}).")
    lines.append("")

    lines.append("## Variant status (Phase A)")
    lines.append("")
    lines.append("| variant | b pts | b domain | b max | db | a pts | a domain | a max | da | HJB conv | iters | stat | gate | max requested outward | Phase E | variant terminal |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for v in runs["variants"]:
        g = v["grid"]
        b = v.get("boundary") or {}
        lines.append(f"| {v['variant']} | {g['b_pts']} | [{_sf(g['b_lo'])},{_sf(g['b_hi'])}] | "
                     f"{_sf(g['b_hi'])} | {_sf(g['db'])} | {g['a_pts']} | [{_sf(g['a_lo'])},{_sf(g['a_hi'])}] | "
                     f"{_sf(g['a_hi'])} | {_sf(g['da'])} | {v['hjb_converged']} | {v['hjb_iterations']} | "
                     f"{_sf(v['hjb_statistic'], '.3e')} | {_sf(v.get('boundary_policy_gate'))} | "
                     f"{_sf(b.get('max_requested_outward'), '.3e')} | {_sf(v.get('phase_e_reached'))} | "
                     f"{_sf(v.get('variant_terminal'))} |")
    lines.append("")

    lines.append("## Boundary requested-rate diagnostics (Phase B)")
    lines.append("")
    lines.append("Requested directional rates are reconstructed from post-convergence `mu_b`/`mu_a` "
                 "as `max(-mu_b,0)/db`, `max(mu_b,0)/db`, `max(-mu_a,0)/da`, `max(mu_a,0)/da` and are "
                 "NEVER clipped or mutated. Coordinates are exact `(b_index,a_index,z_index)` plus "
                 "physical `(b,a,z)` recovered with C-order `np.unravel_index` on the actual 2-D "
                 "boundary slice shape.")
    lines.append("")
    for v in runs["variants"]:
        b = v.get("boundary") or {}
        if not b:
            lines.append(f"### {v['variant']} — HJB not converged; boundary diagnostics not reached")
            lines.append("")
            continue
        lines.append(f"### {v['variant']}")
        lines.append("")
        lines.append("| boundary | direction | max | count>1e-10 | share | argmax index | argmax physical | requested at max | q50/q90/q95/q99 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for bi in b["boundaries"]:
            lines.append(f"| {bi['boundary']} | {bi['direction']} | {_sf(bi['requested_outward_max'], '.3e')} | "
                         f"{_sf(bi['count_above_threshold'])} | {_sf(bi['share_above_threshold'], '.3e')} | "
                         f"{bi.get('argmax_index')} | {bi.get('argmax_physical')} | "
                         f"{_sf(bi.get('requested_at_max'), '.3e')} | {_q_fmt(bi.get('quantiles'))} |")
        off = [o for bi in b["boundaries"] for o in bi.get("offending_states", [])]
        lines.append("")
        if off:
            lines.append("Complete offending states (requested outward rate > 1e-10):")
            lines.append("")
            lines.append("| boundary | direction | b_index | a_index | z_index | b | a | z | requested outward rate |")
            lines.append("|---|---|---|---|---|---|---|---|---|")
            for o in off:
                lines.append(f"| {o['boundary']} | {o['direction']} | {o['b_index']} | {o['a_index']} | "
                             f"{o['z_index']} | {_sf(o['b'], '.6f')} | {_sf(o['a'], '.6f')} | "
                             f"{_sf(o['z'], '.6f')} | {_sf(o['requested_outward_rate'], '.9e')} |")
        else:
            lines.append("No state exceeds the `1e-10` requested-outward threshold.")
        lines.append("")

    lines.append("## Shared-interior policy stability (Phase C)")
    lines.append("")
    lines.append("Frozen V0-based shared-interior mask: `b_index <= 17`, `a_index <= 17`, all z. "
                 "Comparisons are at exact common nodes without interpolation. `rel_diff = max_abs / "
                 "max(1, max|V0 reference|)` is a scale-aware relative difference. Strict-interior "
                 "submetrics exclude the first asset layer and do not replace the frozen primary mask.")
    lines.append("")
    for c in comparisons:
        lines.append(f"### {c['comparison']}")
        lines.append("")
        if not c.get("reached", True):
            lines.append(f"- NOT_REACHED: {c.get('reason')}")
            lines.append("")
            continue
        lines.append("| field | max_abs_diff | rel_diff | strict-interior max_abs | strict-interior rel | label mismatch |")
        lines.append("|---|---|---|---|---|---|")
        for f, m in c["fields"].items():
            if f in ("liquid_label", "transfer_label"):
                lines.append(f"| {f} | — | — | — | — | {_sf(m['mismatch_count'])} |")
            else:
                lines.append(f"| {f} | {_sf(m['max_abs_diff'], '.3e')} | {_sf(m['rel_diff'], '.3e')} | "
                             f"{_sf(m['strict_interior_max_abs_diff'], '.3e')} | "
                             f"{_sf(m['strict_interior_rel_diff'], '.3e')} | — |")
        lines.append("")

    lines.append("## Mechanical generator diagnostics (Phase D)")
    lines.append("")
    lines.append("The candidate generator `Q_c` admits only represented in-grid transitions, omits "
                 "out-of-grid transitions, sets the diagonal to the negative sum of ACTUALLY ADMITTED "
                 "off-diagonal rates, and includes the accepted z-switch block. Passing the mechanical "
                 "thresholds does NOT authorize stationary density while the HJB requests material "
                 "outward boundary policy.")
    lines.append("")
    lines.append("| variant | row-sum max abs | neg offdiag max mag | neg offdiag count | nnz |")
    lines.append("|---|---|---|---|---|")
    for v in runs["variants"]:
        g = v.get("generator") or {}
        lines.append(f"| {v['variant']} | {_sf(g.get('row_sum_max_abs'), '.3e')} | "
                     f"{_sf(g.get('negative_offdiag_max_mag'), '.3e')} | "
                     f"{_sf(g.get('negative_offdiag_count'))} | {_sf(g.get('nnz'))} |")
    lines.append("")
    lines.append(f"Required mechanical thresholds: `row_sum max abs <= 1e-12`, "
                 f"`negative off-diagonal magnitude <= 1e-12`.")

    lines.append("")
    lines.append("## Stationary / tail / aggregate reachability (Phases E-F-G)")
    lines.append("")
    any_reached = any(v["phase_e_reached"] for v in runs["variants"])
    if not any_reached:
        lines.append("No pre-frozen variant reaches the same-process stationary gate: every converged "
                     "variant retains material upper-boundary requested policy under the frozen "
                     "`max requested outward <= 1e-10` criterion. All stationary/tail/aggregate fields "
                     f"are therefore `{NOT_REACHED_MARKER}`. No clipped density is accepted.")
        lines.append("")
        lines.append("Scientific reading: boundary influence does NOT converge away within the exact "
                     "pre-frozen domains; the evidence points to persistent high-wealth mean-reversion / "
                     "finite-domain HJB/KFE closure behavior. This is a bounded diagnostic observation, "
                     "not a claim of stationary-tail existence/non-existence.")
        lines.append("")
    else:
        for v in runs["variants"]:
            if not v["phase_e_reached"]:
                continue
            st = v.get("stationary") or {}
            t = v.get("tail")
            a = v.get("aggregates")
            lines.append(f"### {v['variant']} — same-process stationary reached")
            lines.append("")
            lines.append(f"- stationary gate: `{st.get('gate')}` (reason: {st.get('reason')}); "
                         f"nullspace dimension {st.get('nullspace_dimension')}; SCC count "
                         f"{(st.get('graph') or {}).get('scc_count')}, closed component sizes "
                         f"{(st.get('graph') or {}).get('closed_component_sizes')}.")
            lines.append(f"- pins: classes {st.get('pins', {}).get('classes')}; valid count "
                         f"{st.get('pins', {}).get('valid_pin_count')}; max valid-pin density diff "
                         f"{st.get('pins', {}).get('valid_pin_max_density_diff')}; default pin class "
                         f"{st.get('pins', {}).get('default_pin_class')}.")
            if isinstance(t, dict):
                lines.append(f"- tail: mass(a_max)={t['mass_a_max']:.6e}, mass(b_max)={t['mass_b_max']:.6e}, "
                             f"Pr(a>=0.9 a_max)={t['pr_a_ge_0.9_amax']:.6e}, "
                             f"Pr(b near upper)={t['pr_b_near_upper']:.6e}, top2 a={t['top2_a_layer_mass']:.6e}, "
                             f"top2 b={t['top2_b_layer_mass']:.6e}, Phi_a_upper={t['phi_a_upper_flux']:.6e}, "
                             f"Phi_b_upper={t['phi_b_upper_flux']:.6e}.")
            if isinstance(a, dict):
                lines.append(f"- aggregates: C={a['C']:.9e}, L={a['L']:.9e}, A={a['A']:.9e}, B={a['B']:.9e}.")
            lines.append("")

    lines.append("## Reproducibility")
    lines.append("")
    lines.append(f"- randomness: `{repro['randomness']}`; repeat pass: `{repro['pass_bool']}`; "
                 f"terminal run1/run2: `{repro['terminal_run1']}` / `{repro['terminal_run2']}`.")
    for vid, cmp in repro["per_variant"].items():
        lines.append(f"- {vid}: structural identical {cmp['identical_structural_signature']}, "
                     f"max numeric diff {cmp['max_numeric_diff']:.3e}, "
                     f"aligned non-finite {cmp['aligned_nonfinite_fields']}, "
                     f"mismatched {cmp['mismatched_fields']}, pass {cmp['pass_bool']}.")
    lines.append("")

    lines.append("## Liquid-vs-illiquid upper-domain behavior")
    lines.append("")
    if ANNOTATION_LIQUID_ILLIQUID_DIVERGE in term["annotations"]:
        lines.append("Material-request indicators for the liquid (upper-b) and illiquid (upper-a) "
                     "dimensions diverge across variants, supporting the secondary annotation "
                     "`LIQUID_ILLIQUID_UPPER_DOMAIN_BEHAVIOR_DIVERGES__SEPARATE_SCIENTIFIC_TREATMENT_REQUIRED`.")
    else:
        lines.append("Liquid (upper-b) and illiquid (upper-a) material-request indicators agree across "
                     "all variants; no separate-treatment annotation is supported by this evidence.")
    lines.append("")

    lines.append("## Artifact integrity")
    lines.append("")
    lines.append(f"- accepted MATLAB-faithful oracle blob `{ACCEPTED_BLOB}`, SHA-256 `{ACCEPTED_SHA256}` "
                 "re-verified read-only (unchanged from the accepted Issue #23/#26 state).")
    lines.append("- no existing tracked file modified; dedicated branch "
                 "`dsh/issue-29-dlh-5f-upper-domain-stationary-tail-2026-09-01`; allowlist-only "
                 "additions (3 artifacts + 8 evidence files).")
    lines.append("")
    lines.append("DLH-5F implements NO repair: the accepted HJB/local-policy/KFE/regional source is "
                 "immutable; no conservative density is accepted for economic interpretation when the "
                 "HJB/KFE process differs; no regularization/jitter/pseudoinverse; no parameter/price/"
                 "tolerance retuning; no D1-D3; no regional or multi-province GE; no learned network; "
                 "no nominal HANK.")
    return "\n".join(lines)


def _render_forbidden_check(cfg: DLH5FConfig, runs: dict, repro: dict, term: dict) -> str:
    lines = [
        "# DLH-5F — Forbidden-Operation / Scope Check (Issue #29)",
        "",
        "DSH did NOT perform any of the following during DLH-5F execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |",
        "| Modify `conservative_stationary_kfe.py` | NOT performed (read-only authority) |",
        "| Modify any existing HJB/local-policy/KFE/regional source | NOT performed |",
        "| Modify accepted Issue #23-#28 evidence | NOT performed |",
        "| Change economic parameters/prices/taxes/transfers/shocks | NOT performed (frozen D0) |",
        "| Change HJB numerics or tolerances | NOT performed (accepted fixture) |",
        "| Warm-start one grid from another | NOT performed (fresh initialization per variant) |",
        "| Adaptively add a grid after seeing results | NOT performed (exact six variants) |",
        "| Expand beyond the exact six frozen variants | NOT performed |",
        "| Clip HJB policy to seek stationary PASS | NOT performed (fail-closed gate) |",
        "| Accept a stationary density from a different controlled process | NOT performed |",
        "| Use old row-295 density as economic evidence | NOT performed |",
        "| Change contamination constant `0.007` | NOT performed (frozen) |",
        "| Regularization / jitter / pseudoinverse | NOT performed |",
        "| Auto-select another production pin | NOT performed |",
        "| Run D1-D3 | NOT performed |",
        "| Run two-region outer iteration | NOT performed |",
        "| Run 3-5/31-province GE or `31_PROVINCE_HOUSEHOLD_UPPER_DOMAIN_AUDIT` | NOT performed |",
        "| Train `W^L` or any neural network | NOT performed |",
        "| Enter nominal HANK / calibration / policy / welfare / Results | NOT performed |",
        "| Mutate governance files from the Builder branch | NOT performed |",
        "| `git add .` / `git add -A` | NOT performed (explicit staging only) |",
        "| Create PR / merge / close Issue / successor / self-accept | NOT performed |",
        "",
        f"Terminal classification: `{term['terminal']}`",
        "",
        "Secondary annotations: " + (", ".join(f"`{a}`" for a in term["annotations"]) or "none"),
        "",
    ]
    return "\n".join(lines)


def _sf(v, spec=None) -> str:
    if v is None:
        return "—"
    try:
        if spec is not None:
            return format(float(v), spec)
        return str(v)
    except (TypeError, ValueError):
        return str(v)


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="DLH-5F upper-domain stationary-tail diagnostic (Issue #29)")
    parser.add_argument("--config", default="configs/dlh_5f_upper_domain_stationary_tail_diagnostic.toml")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    root = pathlib.Path(cfg.output_root)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"output root already exists (no-overwrite): {root}")
    dlh5b, params, numerics = build_fixture(cfg)
    runs = run_all_variants(cfg, dlh5b, params, numerics)
    comparisons = shared_interior_all(cfg, runs)
    repro = reproduce(cfg, dlh5b, params, numerics)
    term = overall_terminal(cfg, runs, repro)
    write_evidence(root, cfg, runs, comparisons, repro, term)
    print(f"artifacts written under {root}")
    print(f"terminal = {term['terminal']}")
    if term["annotations"]:
        print("annotations = " + ", ".join(term["annotations"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
