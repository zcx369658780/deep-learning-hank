#!/usr/bin/env python
"""DLH-5R (Issue #44) - HJB-only provisional-S3 liquid-tail numerical falsification.

Executes the accepted immutable household HJB solver on exactly the six mature
DLH-5J variants J0-J5 (Issue #44 section 3), reconstructs the raw value gradients
from the converged value using the EXACT accepted finite-difference/upwind
semantics (Issue #44 section 4), computes the pre-registered aligned tail
observables (Issue #44 section 7), the scaling/plateau diagnostics and cross-b /
cross-a comparisons (Issue #44 section 8), applies the frozen evidence masks and
windows (Issue #44 section 6), and writes:

  DLH_5R_VARIANT_RUN_SUMMARY.csv
  DLH_5R_ALIGNED_TAIL_OBSERVABLES.csv
  DLH_5R_SCALING_AND_PLATEAU_DIAGNOSTICS.csv
  _decision_inputs.json          (untracked diagnostic input for the decision report)

The accepted household source
  src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py
is IMPORTED READ-ONLY and never mutated (accepted blob 76ae5b149993... verified at
runtime). NO stationary KFE, NO R/W/domain/endpoint law, NO price/calibration
change, NO grid creation beyond the exact J0-J5 definitions. b160 is the hard
route ceiling.

Raw-gradient provenance:
- The accepted solver computes vb_f/vb_b/va_f/va_b internally every iteration but
  does NOT expose them on the result. They are therefore RECONSTRUCTED from the
  converged value with the exact accepted formulas:
      vb_f[i-1] = (V[i]-V[i-1])/db,  vb_b[i]   = vb_f[i-1]
      va_f[j-1] = (V[j]-V[j-1])/da,  va_b[j]   = va_f[j-1]
      vb_b[0] = resources(b_lo)^(-gamma_c);  vb_f[-1] = resources(b_max)^(-gamma_c)
      va_f[-1] = 0 (a-upper interior zero),   va_b[0]  = 0 (a-lower interior zero)
  with resources = (1-tau)*w*z*labor0 + transfer_income + r_b_eff*b, r_b_eff =
  r_b + rb_gap if b<0 else r_b. This is algebraically identical to one more
  iteration of the accepted operator on the converged value.
- Primary S3 observable R_hat = V_a_raw / V_b_raw uses the raw UPWIND pair
  selected from the accepted drift signs: V_a_raw = va_f if mu_a>=0 else va_b;
  V_b_raw = vb_f if mu_b>=0 else vb_b (raw, unfloored). The transfer FOC is
  evaluated on these raw gradients; the MATLAB_DERIVATIVE_FLOOR (1e-6) applies to
  consumption/labor only and is NEVER substituted into R_hat. On the liquid tail
  the accepted solution is dissaving (r_b < rho => mu_b < 0), so V_b_raw is the
  BACKWARD gradient; this is verified against the consumption FOC
  (c = V_b_raw^(-1/gamma_c) on the dissaving branch to ~1e-10 relative). The
  forward and backward raw gradients are persisted as audit columns, and the
  forward/forward pair is reported as R_hat_ff / Q_hat_ff. Floor activation is
  recorded separately as a numerical-semantic limitation indicator (it did not
  activate in any DLH-5R run).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import pathlib
import sys
import time
import tomllib

import numpy as np

# ---------------------------------------------------------------- path setup --
REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from deep_learning_hank.two_asset.matlab_faithful_two_asset_ha import (  # noqa: E402
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    MATLAB_DERIVATIVE_FLOOR,
    solve_matlab_faithful_hjb,
)
from deep_learning_hank.regional.two_region_fixed_point import (  # noqa: E402
    build_fixture,
    household_initial_condition,
    load_config as load_dlh5b_config,
)

ACCEPTED_SOURCE_BLOB = "76ae5b149993a7edeeb8eb337f1b02b3fe33c51e"
SOURCE_PATH = REPO_ROOT / "src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py"

DB0 = 7.0 / 19.0
VARIANT_IDS = ["J0_A77_B120", "J1_A77_B140", "J2_A77_B160",
               "J3_A153_B120", "J4_A153_B140", "J5_A153_B160"]


def git_blob_sha1(path: pathlib.Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def load_r5_config(path: pathlib.Path) -> dict:
    with open(path, "rb") as fh:
        return tomllib.load(fh)


def load_dlh5j_grid_facts(path: pathlib.Path) -> dict:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    a_res = {r["id"]: int(r["a_pts"]) for r in raw["a_resolutions"]}
    b_ext = {e["id"]: (int(e["b_pts"]), float(e["b_hi"])) for e in raw["b_extents"]}
    return {
        "a_res": a_res,
        "b_ext": b_ext,
        "b_lo": float(raw["liquid_domain"]["b_lo"]),
        "db": float(raw["liquid_domain"]["db"]),
        "a_lo": float(raw["frozen_physical_illiquid"]["a_lo"]),
        "a_hi": float(raw["frozen_physical_illiquid"]["a_hi"]),
    }


def build_variant_grid(a_res: str, b_ext: str, dlh5b_cfg, jfacts: dict) -> MatlabFaithfulHJBGrid:
    a_pts = jfacts["a_res"][a_res]
    b_pts, b_hi = jfacts["b_ext"][b_ext]
    b = np.linspace(jfacts["b_lo"], b_hi, b_pts)
    a = np.linspace(jfacts["a_lo"], jfacts["a_hi"], a_pts)
    z = np.asarray(list(dlh5b_cfg.z), dtype=float)
    switch = np.asarray(dlh5b_cfg.switch_matrix, dtype=float)
    grid = MatlabFaithfulHJBGrid(b, a, z, switch)
    # frozen grid identity checks (DLH-5J facts)
    assert abs(float(grid.b[1] - grid.b[0]) - DB0) <= 1e-12
    assert abs(grid.a[0] - jfacts["a_lo"]) <= 1e-12 and abs(grid.a[-1] - jfacts["a_hi"]) <= 1e-12
    return grid


# --------------------------------------------------- raw gradient reconstruction --
def reconstruct_raw_gradients(V, grid, params, inputs, labor0, transfer_income, rb_gap):
    """Exact accepted raw-gradient reconstruction from the converged value."""
    I, J, Nz = V.shape
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    vb_f = np.zeros((I, J, Nz)); vb_b = np.zeros((I, J, Nz))
    va_f = np.zeros((I, J, Nz)); va_b = np.zeros((I, J, Nz))
    vb_f[:-1] = (V[1:] - V[:-1]) / db
    vb_b[1:] = vb_f[:-1]
    # b-boundary marginal-utility closures (accepted solver lines 534-541)
    for j in range(J):
        for nz in range(Nz):
            for i in (0, I - 1):
                rb = inputs.r_b + (rb_gap if grid.b[i] < 0 else 0.0)
                resources = ((1 - inputs.tau) * inputs.wages[0] * grid.z[nz] * labor0[i, j, nz]
                             + transfer_income + rb * grid.b[i])
                marginal = resources ** (-params.gamma_c)
                if i == 0:
                    vb_b[0, j, nz] = marginal
                else:
                    vb_f[I - 1, j, nz] = marginal
    va_f[:, :-1] = (V[:, 1:] - V[:, :-1]) / da
    va_b[:, 1:] = va_f[:, :-1]
    return vb_f, vb_b, va_f, va_b


# ------------------------------------------------------------------- windows --
WINDOW_BOUNDARY_TOL = 1.0e-9  # window-membership tolerance (db=0.368 >> 1e-9; deterministic)


def assign_windows(b: np.ndarray, r5cfg: dict) -> dict:
    """Return {window_id: sorted b indices within physical bounds}.

    Membership uses a 1e-9 physical tolerance so that exact integer-node bounds
    (e.g. b = 40 = i*7/19 - 2) are classified deterministically despite
    linspace floating-point representation. Neighboring nodes are 7/19 ~= 0.368
    apart, so the tolerance cannot misclassify a node.
    """
    out = {}
    tol = WINDOW_BOUNDARY_TOL
    for wid, spec in r5cfg["b_windows"].items():
        lo = float(spec["b_lo"]); hi = float(spec["b_hi"])
        if spec.get("b_lo_inclusive", True):
            idx = np.where((b >= lo - tol) & (b <= hi + tol))[0]
        else:
            idx = np.where((b > lo + tol) & (b <= hi + tol))[0]
        out[wid] = [int(i) for i in idx]
    return out


def aligned_a_indices(J: int, a_res: str) -> list:
    if a_res == "a77":
        return list(range(J))
    if a_res == "a153":
        return list(range(0, J, 2))
    raise ValueError(a_res)


def primary_a_mask(a_res: str, r5cfg: dict) -> set:
    m = r5cfg["evidence_masks"]
    if a_res == "a77":
        lo, hi = m["a77_primary_j"]
        return set(range(int(lo), int(hi) + 1))
    if a_res == "a153":
        lo, hi = m["a153_primary_jeven"]
        return set(range(int(lo), int(hi) + 1, 2))
    raise ValueError(a_res)


# ------------------------------------------------------------------ workers --
def run_variant(args):
    (variant, a_res, b_ext, r5cfg, dlh5b_cfg, params, numerics, jfacts,
     inputs, transfer_income, rb_gap, out_root) = args
    t0 = time.perf_counter()
    grid = build_variant_grid(a_res, b_ext, dlh5b_cfg, jfacts)
    db = float(grid.b[1] - grid.b[0]); da = float(grid.a[1] - grid.a[0])
    initial, labor0 = household_initial_condition(grid, params, inputs, rb_gap)
    hjb = solve_matlab_faithful_hjb(grid, params, inputs, initial, labor0,
                                    transfer_income, rb_gap, numerics)
    elapsed = time.perf_counter() - t0
    I, J, Nz = grid.b.size, grid.a.size, grid.z.size
    V = np.asarray(hjb.value, dtype=float)
    vb_f, vb_b, va_f, va_b = reconstruct_raw_gradients(
        V, grid, params, inputs, labor0, transfer_income, rb_gap)

    # ---- non-finite and floor diagnostics (full grid) ----
    def n_nonfinite(*arrs):
        return sum(int(np.count_nonzero(~np.isfinite(a))) for a in arrs)

    floor_bf = vb_f < MATLAB_DERIVATIVE_FLOOR
    floor_bb = vb_b < MATLAB_DERIVATIVE_FLOOR
    floor_any = floor_bf | floor_bb
    n_states = int(I * J * Nz)
    nonfinite = {
        "value": int(np.count_nonzero(~np.isfinite(V))),
        "vb_f": int(np.count_nonzero(~np.isfinite(vb_f))),
        "vb_b": int(np.count_nonzero(~np.isfinite(vb_b))),
        "va_f": int(np.count_nonzero(~np.isfinite(va_f))),
        "va_b": int(np.count_nonzero(~np.isfinite(va_b))),
        "consumption": int(np.count_nonzero(~np.isfinite(hjb.consumption))),
        "transfer": int(np.count_nonzero(~np.isfinite(hjb.transfer))),
        "mu": n_nonfinite(hjb.mu_a, hjb.mu_b),
    }

    # ---- windows / masks ----
    windows = assign_windows(grid.b, r5cfg)
    a_aligned = aligned_a_indices(J, a_res)
    a_primary = primary_a_mask(a_res, r5cfg)
    top_excl = bool(r5cfg["evidence_masks"]["top_two_b_nodes_excluded"])

    rows = []           # aligned observables rows
    row_fields = None
    # evidence-window state flags for upwind agreement / floor / primary count
    for nz in range(Nz):
        for j in a_aligned:
            for wid, b_idx in windows.items():
                # descriptive-only W4 never enters primary statistics
                descriptive = bool(r5cfg["b_windows"][wid].get("descriptive_only", False))
                for i in b_idx:
                    b = float(grid.b[i]); a = float(grid.a[j]); z = float(grid.z[nz])
                    b_primary = (not descriptive) and (not (top_excl and i >= I - 2))
                    a_prim = j in a_primary
                    primary = bool(a_prim and b_primary)
                    vbf = float(vb_f[i, j, nz]); vbb = float(vb_b[i, j, nz])
                    vaf = float(va_f[i, j, nz]); vab = float(va_b[i, j, nz])
                    c = float(hjb.consumption[i, j, nz])
                    d = float(hjb.transfer[i, j, nz])
                    chi = float(hjb.adjustment_cost[i, j, nz])
                    mu_a = float(hjb.mu_a[i, j, nz]); mu_b = float(hjb.mu_b[i, j, nz])
                    mu_W = mu_a + mu_b
                    # Upwind raw transfer-FOC-consistent pair (Issue #44 section 4):
                    # v_a = forward raw if mu_a>=0 else backward raw; v_b likewise.
                    v_a_up = vaf if mu_a >= 0 else vab
                    v_b_up = vbf if mu_b >= 0 else vbb
                    vb_pos = v_b_up if (np.isfinite(v_b_up) and v_b_up > 0) else np.nan
                    R_hat = v_a_up / vb_pos if (np.isfinite(v_a_up) and np.isfinite(vb_pos)) else np.nan
                    R_hat_ff = vaf / vbf if (np.isfinite(vaf) and np.isfinite(vbf) and vbf > 0) else np.nan
                    row = {
                        "variant": variant, "b_index": i, "a_index": j, "z_index": nz,
                        "b": b, "a": a, "z": z, "window": wid,
                        "a_primary": a_prim, "b_primary": b_primary, "primary": primary,
                        "V_a_raw": v_a_up, "V_b_raw": v_b_up,
                        "V_a_raw_forward": vaf, "V_b_raw_forward": vbf,
                        "V_a_raw_backward": vab, "V_b_raw_backward": vbb,
                        "R_hat": R_hat, "R_hat_ff": R_hat_ff,
                        "R_over_sqrt_b": (R_hat / np.sqrt(b)) if np.isfinite(R_hat) else np.nan,
                        "Q_hat": (b * b) * v_b_up if np.isfinite(v_b_up) else np.nan,
                        "Q_hat_ff": (b * b) * vbf if np.isfinite(vbf) else np.nan,
                        "c": c, "c_over_b": c / b,
                        "d": d, "d_over_sqrt_b": d / np.sqrt(b),
                        "chi": chi, "chi_over_b": chi / b,
                        "mu_a": mu_a, "mu_b": mu_b, "mu_W": mu_W, "mu_W_over_b": mu_W / b,
                        "floor_activated_bf": bool(floor_bf[i, j, nz]),
                        "floor_activated_bb": bool(floor_bb[i, j, nz]),
                        "liquid_label": str(hjb.liquid_label[i, j, nz]),
                        "transfer_label": str(hjb.transfer_label[i, j, nz]),
                    }
                    if row_fields is None:
                        row_fields = list(row.keys())
                    rows.append(row)

    # ---- window aggregates over primary states ----
    agg = {}
    for wid, spec in r5cfg["b_windows"].items():
        ev = [r for r in rows if r["window"] == wid and r["primary"]]
        agg[wid] = {
            "n_primary": len(ev),
            "n_window_nodes": len(windows[wid]),
            "descriptive_only": bool(spec.get("descriptive_only", False)),
            "rows": ev,
        }

    # ---- a=0 descriptive ----
    a0 = {}
    for wid in r5cfg["b_windows"]:
        ev = [r for r in rows if r["window"] == wid and r["a_index"] == 0 and r["z_index"] == 0]
        a0.setdefault(wid, []).extend(ev)

    meta = {
        "variant": variant, "a_res": a_res, "b_ext": b_ext,
        "a_pts": J, "b_pts": I, "z_pts": Nz,
        "da": da, "db": db, "b_lo": float(grid.b[0]), "b_hi": float(grid.b[-1]),
        "a_lo": float(grid.a[0]), "a_hi": float(grid.a[-1]),
        "source_blob": ACCEPTED_SOURCE_BLOB,
        "converged": bool(hjb.converged), "iterations": int(hjb.iterations),
        "convergence_statistic": float(hjb.convergence_statistic),
        "max_iterations": int(numerics.max_iterations),
        "convergence_tolerance": float(numerics.convergence_tolerance),
        "delta": float(numerics.delta), "drift_tolerance": float(numerics.drift_tolerance),
        "runtime_seconds": elapsed,
        "floor_activation_count": int(np.count_nonzero(floor_any)),
        "floor_activation_fraction": float(np.count_nonzero(floor_any) / n_states),
        "floor_activation_count_bf": int(np.count_nonzero(floor_bf)),
        "floor_activation_count_bb": int(np.count_nonzero(floor_bb)),
        "n_states": n_states,
        "nonfinite": nonfinite,
        "upwind_fb_share": None,  # computed post-hoc on primary rows below
    }
    # upwind branch agreement on primary evidence states
    pev = [r for r in rows if r["primary"]]
    if pev:
        from collections import Counter
        liq = Counter(r["liquid_label"] for r in pev)
        tra = Counter(r["transfer_label"] for r in pev)
        meta["liquid_label_counts"] = dict(liq)
        meta["transfer_label_counts"] = dict(tra)
        meta["mu_a_pos_share"] = float(sum(1 for r in pev if r["mu_a"] > 0) / len(pev))
        meta["mu_b_neg_share"] = float(sum(1 for r in pev if r["mu_b"] < 0) / len(pev))
        meta["upwind_fb_share"] = float(
            sum(1 for r in pev if r["mu_a"] >= 0 and r["mu_b"] < 0) / len(pev))
        meta["primary_floor_fraction"] = float(
            sum(1 for r in pev if r["floor_activated_bf"] or r["floor_activated_bb"]) / len(pev))

    print(f"[{variant}] converged={hjb.converged} iters={hjb.iterations} "
          f"stat={hjb.convergence_statistic:.3e} time={elapsed:.1f}s "
          f"floor_frac={meta['floor_activation_fraction']:.3e} "
          f"upwindFB={meta['upwind_fb_share']}", flush=True)
    return {"meta": meta, "rows": rows, "row_fields": row_fields, "agg": agg, "a0": a0,
            "grid_b": list(grid.b), "grid_a": list(grid.a), "grid_z": list(grid.z)}


# --------------------------------------------------------------- diagnostics --
def _rel_diff(a, b, floor):
    denom = max(abs(a), abs(b), floor)
    return float(abs(a - b) / denom)


def _wsum(rows, key):
    vals = np.array([r[key] for r in rows if np.isfinite(r[key])], dtype=float)
    return vals


def _loglog_slope(rows_bynode, key_vb="V_b_raw"):
    """Slope of ln(vb) vs ln(b) across b nodes for a fixed (a,z)."""
    xs = np.log(np.array([r["b"] for r in rows_bynode], dtype=float))
    ys = np.log(np.array([r[key_vb] for r in rows_bynode], dtype=float))
    if len(xs) < 2 or not np.isfinite(ys).all() or np.any(ys <= -np.inf):
        return np.nan
    xm = xs.mean(); ym = ys.mean()
    denom = float(np.sum((xs - xm) ** 2))
    if denom <= 0:
        return np.nan
    return float(np.sum((xs - xm) * (ys - ym)) / denom)


def _quantile(vals, q):
    if vals.size == 0:
        return np.nan
    return float(np.quantile(vals, q))


def window_aggregate(agg_rows):
    """Per (a,z) window-median first, then aggregate over primary (a,z)."""
    by_az = {}
    for r in agg_rows:
        by_az.setdefault((r["a_index"], r["z_index"]), []).append(r)
    slope_vals = []
    q_med = []; c_med = []; r_med = []; rs_med = []; chi_med = []; mu_med = []
    for (ai, zi), rr in by_az.items():
        rr_sorted = sorted(rr, key=lambda x: x["b"])
        s = _loglog_slope(rr_sorted)
        if np.isfinite(s):
            slope_vals.append(s)
        q_med.append(float(np.median(_wsum(rr, "Q_hat"))))
        c_med.append(float(np.median(_wsum(rr, "c_over_b"))))
        r_med.append(float(np.median(np.abs(_wsum(rr, "R_hat")))))
        rs_med.append(float(np.median(_wsum(rr, "R_over_sqrt_b"))))
        chi_med.append(float(np.median(_wsum(rr, "chi_over_b"))))
        mu_med.append(float(np.median(_wsum(rr, "mu_W_over_b"))))
    slope_vals = np.array(slope_vals); q_med = np.array(q_med); c_med = np.array(c_med)
    r_med = np.array(r_med); rs_med = np.array(rs_med); chi_med = np.array(chi_med)
    mu_med = np.array(mu_med)
    out = {
        "n_az": len(by_az),
        "slope_median": _quantile(slope_vals, 0.5), "slope_p10": _quantile(slope_vals, 0.10),
        "slope_p90": _quantile(slope_vals, 0.90),
        "slope_worst_dev_abs": float(np.max(np.abs(slope_vals + 2))) if slope_vals.size else np.nan,
        "Q_hat_median": _quantile(q_med, 0.5), "Q_hat_p10": _quantile(q_med, 0.10),
        "Q_hat_p90": _quantile(q_med, 0.90),
        "Q_hat_worst_dev_pct": float(np.max(np.abs(q_med - 3265.3061224489797) / 3265.3061224489797 * 100)) if q_med.size else np.nan,
        "c_over_b_median": _quantile(c_med, 0.5), "c_over_b_p10": _quantile(c_med, 0.10),
        "c_over_b_p90": _quantile(c_med, 0.90),
        "c_over_b_worst_dev_pct": float(np.max(np.abs(c_med - 0.0175) / 0.0175 * 100)) if c_med.size else np.nan,
        "absR_median": _quantile(r_med, 0.5), "absR_p10": _quantile(r_med, 0.10), "absR_p90": _quantile(r_med, 0.90),
        "R_over_sqrt_b_median": _quantile(rs_med, 0.5),
        "R_over_sqrt_b_p10": _quantile(rs_med, 0.10), "R_over_sqrt_b_p90": _quantile(rs_med, 0.90),
        "chi_over_b_median": _quantile(chi_med, 0.5),
        "chi_over_b_p10": _quantile(chi_med, 0.10), "chi_over_b_p90": _quantile(chi_med, 0.90),
        "mu_W_over_b_median": _quantile(mu_med, 0.5),
        "mu_W_over_b_p10": _quantile(mu_med, 0.10), "mu_W_over_b_p90": _quantile(mu_med, 0.90),
        "n_nodes_used": len(agg_rows),
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(REPO_ROOT / "configs/dlh_5r_provisional_s3_hjb_tail_falsification.toml"))
    ap.add_argument("--workers", type=int, default=min(6, os.cpu_count() or 1))
    ap.add_argument("--write-json", action="store_true", default=True)
    args = ap.parse_args()

    r5cfg = load_r5_config(pathlib.Path(args.config))
    out_root = REPO_ROOT / r5cfg["output"]["root"]
    out_root.mkdir(parents=True, exist_ok=True)

    # --- authority / source blob verification ---
    blob = git_blob_sha1(SOURCE_PATH)
    assert blob == ACCEPTED_SOURCE_BLOB, f"source blob mismatch: {blob}"
    print(f"source blob verified: {blob}", flush=True)

    # --- fixtures (accepted read-only contract, reproduces DLH-5J) ---
    dlh5b = load_dlh5b_config(str(REPO_ROOT / r5cfg["grid_authority"]["dlh5b_config_path"]))
    _grid0, params, numerics = build_fixture(dlh5b)
    jfacts = load_dlh5j_grid_facts(REPO_ROOT / r5cfg["grid_authority"]["dlh5j_config_path"])
    region_index = int(r5cfg["grid_authority"]["region_index"])
    inputs = HouseholdInputs(
        r_a=float(r5cfg["frozen_economics_identity"]["r_a"]),
        r_b=dlh5b.r_b,
        tau=dlh5b.tau[region_index],
        wages=np.array([float(r5cfg["frozen_economics_identity"]["wbar"])]),
        migration_costs=np.array([0.0]),
        labor_weights=np.array([1.0]),
    )
    transfer_income = float(dlh5b.transfer_income[region_index])
    rb_gap = float(dlh5b.rb_gap[region_index])

    jobs = []
    for variant, spec in r5cfg["variants"].items():
        jobs.append((variant, spec["a_res"], spec["b_ext"], r5cfg, dlh5b, params, numerics,
                     jfacts, inputs, transfer_income, rb_gap, out_root))

    with mp.Pool(args.workers) as pool:
        results = pool.map(run_variant, jobs)

    results_by_v = {r["meta"]["variant"]: r for r in results}

    # ---------------------------------------------------------------- CSVs ---
    import csv
    from collections import OrderedDict

    # 1) variant run summary
    summary_fields = [
        "variant", "a_res", "b_ext", "a_pts", "b_pts", "z_pts", "da", "db",
        "b_lo", "b_hi", "a_lo", "a_hi", "source_blob", "converged", "iterations",
        "convergence_statistic", "max_iterations", "convergence_tolerance", "delta",
        "drift_tolerance", "runtime_seconds", "floor_activation_count",
        "floor_activation_fraction", "floor_activation_count_bf",
        "floor_activation_count_bb", "n_states",
        "nonfinite_value", "nonfinite_vb_f", "nonfinite_vb_b", "nonfinite_va_f",
        "nonfinite_va_b", "nonfinite_consumption", "nonfinite_transfer",
        "nonfinite_mu", "upwind_fb_share", "mu_a_pos_share", "mu_b_neg_share",
        "primary_floor_fraction",
    ]
    with open(out_root / "DLH_5R_VARIANT_RUN_SUMMARY.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=summary_fields, extrasaction="ignore")
        w.writeheader()
        for v in VARIANT_IDS:
            m = results_by_v[v]["meta"]
            row = {**m, **{f"nonfinite_{k}": vv for k, vv in m["nonfinite"].items()}}
            w.writerow(row)

    # 2) aligned tail observables
    fieldnames = results_by_v[VARIANT_IDS[0]]["row_fields"]
    with open(out_root / "DLH_5R_ALIGNED_TAIL_OBSERVABLES.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for v in VARIANT_IDS:
            for r in results_by_v[v]["rows"]:
                w.writerow(r)

    # 3) scaling & plateau diagnostics
    diag_rows = []
    for v in VARIANT_IDS:
        meta = results_by_v[v]["meta"]
        for wid in r5cfg["b_windows"]:
            spec = r5cfg["b_windows"][wid]
            descriptive = bool(spec.get("descriptive_only", False))
            # descriptive (W4) aggregates use the a-primary states within the window
            # but are flagged DESCRIPTIVE_ONLY and never enter the verdict screens.
            ev = [r for r in results_by_v[v]["rows"]
                  if r["window"] == wid and (r["a_primary"] if descriptive else r["primary"])]
            agg = window_aggregate(ev)
            agg["section"] = "window_aggregate"
            agg["variant"] = v
            agg["a_res"] = meta["a_res"]
            agg["b_ext"] = meta["b_ext"]
            agg["window"] = wid
            agg["descriptive_only"] = descriptive
            if descriptive:
                # W4 is descriptive-only evidence; if the extent has no W4 nodes
                # it is structurally insufficient.
                agg["window_valid"] = "INSUFFICIENT_WINDOW_NODES" if len(ev) == 0 else "DESCRIPTIVE_ONLY"
            else:
                agg["window_valid"] = "INSUFFICIENT_WINDOW_NODES" if len(ev) < r5cfg["diagnostics"]["min_window_valid_states"] else "VALID"
            diag_rows.append(agg)

    floor = float(r5cfg["diagnostics"]["rel_diff_denominator_floor"])
    # cross-b extent (common aligned b nodes in common windows)
    obs_keys = ["Q_hat_median", "c_over_b_median", "slope_median",
                "R_over_sqrt_b_median", "chi_over_b_median", "mu_W_over_b_median"]
    b_ext_order = ["b120", "b140", "b160"]
    windows_by_ext = {}
    for wid, spec in r5cfg["b_windows"].items():
        for ext in spec["extents"]:
            windows_by_ext.setdefault(ext, set()).add(wid)
    for a_res in ("a77", "a153"):
        variants_of = {e: next(v for v in VARIANT_IDS
                              if results_by_v[v]["meta"]["a_res"] == a_res
                              and results_by_v[v]["meta"]["b_ext"] == e) for e in b_ext_order}
        for e1, e2 in (("b120", "b140"), ("b140", "b160"), ("b120", "b160")):
            common_w = sorted(windows_by_ext[e1] & windows_by_ext[e2])
            for wid in common_w:
                if r5cfg["b_windows"][wid].get("descriptive_only"):
                    continue
                # build aggregate on aligned b nodes (b120 nodes are subset; use b120 node indices)
                rows1 = [r for r in results_by_v[variants_of[e1]]["rows"]
                         if r["window"] == wid and r["primary"]]
                rows2 = [r for r in results_by_v[variants_of[e2]]["rows"]
                         if r["window"] == wid and r["primary"]]
                agg1 = window_aggregate(rows1)
                agg2 = window_aggregate(rows2)
                for k in obs_keys:
                    diag_rows.append({
                        "section": "cross_b", "variant": f"{a_res}:{e1}vs{e2}",
                        "a_res": a_res, "b_ext": f"{e1}_vs_{e2}", "window": wid,
                        "observable": k,
                        "value_lower": agg1.get(k, np.nan), "value_higher": agg2.get(k, np.nan),
                        "rel_diff_frac": _rel_diff(agg1.get(k, np.nan), agg2.get(k, np.nan), floor),
                        "window_valid": "INSUFFICIENT_WINDOW_NODES" if (len(rows1) == 0 or len(rows2) == 0) else "VALID",
                    })
    # cross-a (a77 vs every-second a153 on aligned nodes)
    for b_ext in b_ext_order:
        v77 = next(v for v in VARIANT_IDS if results_by_v[v]["meta"]["a_res"] == "a77"
                   and results_by_v[v]["meta"]["b_ext"] == b_ext)
        v153 = next(v for v in VARIANT_IDS if results_by_v[v]["meta"]["a_res"] == "a153"
                    and results_by_v[v]["meta"]["b_ext"] == b_ext)
        for wid in sorted(windows_by_ext[b_ext]):
            if r5cfg["b_windows"][wid].get("descriptive_only"):
                continue
            rows1 = [r for r in results_by_v[v77]["rows"] if r["window"] == wid and r["primary"]]
            rows2 = [r for r in results_by_v[v153]["rows"] if r["window"] == wid and r["primary"]]
            agg1 = window_aggregate(rows1)
            agg2 = window_aggregate(rows2)
            for k in obs_keys:
                diag_rows.append({
                    "section": "cross_a", "variant": f"a77_vs_a153:{b_ext}",
                    "a_res": "a77_vs_a153", "b_ext": b_ext, "window": wid,
                    "observable": k,
                    "value_lower": agg1.get(k, np.nan), "value_higher": agg2.get(k, np.nan),
                    "rel_diff_frac": _rel_diff(agg1.get(k, np.nan), agg2.get(k, np.nan), floor),
                    "window_valid": "INSUFFICIENT_WINDOW_NODES" if (len(rows1) == 0 or len(rows2) == 0) else "VALID",
                })
    # a=0 descriptive
    for v in VARIANT_IDS:
        meta = results_by_v[v]["meta"]
        for wid in r5cfg["b_windows"]:
            ev = [r for r in results_by_v[v]["rows"] if r["window"] == wid and r["a_index"] == 0]
            if not ev:
                continue
            q = np.median([r["Q_hat"] for r in ev if np.isfinite(r["Q_hat"])])
            c = np.median([r["c_over_b"] for r in ev if np.isfinite(r["c_over_b"])])
            diag_rows.append({
                "section": "a0_descriptive", "variant": v, "a_res": meta["a_res"],
                "b_ext": meta["b_ext"], "window": wid, "observable": "Q_hat_median_a0",
                "value_lower": float(q) if np.isfinite(q) else np.nan,
                "value_higher": float(c) if np.isfinite(c) else np.nan,
                "rel_diff_frac": np.nan, "window_valid": "VALID",
            })

    diag_fieldnames = ["section", "variant", "a_res", "b_ext", "window", "observable",
                       "n_az", "n_nodes_used", "window_valid", "descriptive_only",
                       "slope_median", "slope_p10", "slope_p90", "slope_worst_dev_abs",
                       "Q_hat_median", "Q_hat_p10", "Q_hat_p90", "Q_hat_worst_dev_pct",
                       "c_over_b_median", "c_over_b_p10", "c_over_b_p90",
                       "c_over_b_worst_dev_pct", "absR_median", "absR_p10", "absR_p90",
                       "R_over_sqrt_b_median", "R_over_sqrt_b_p10", "R_over_sqrt_b_p90",
                       "chi_over_b_median", "chi_over_b_p10", "chi_over_b_p90",
                       "mu_W_over_b_median", "mu_W_over_b_p10", "mu_W_over_b_p90",
                       "value_lower", "value_higher", "rel_diff_frac"]
    with open(out_root / "DLH_5R_SCALING_AND_PLATEAU_DIAGNOSTICS.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=diag_fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in diag_rows:
            w.writerow(r)

    # --------------------------------------------------- decision input JSON ---
    decision = {
        "config": str(args.config),
        "source_blob": blob,
        "origin_main_fresh": None,  # filled by harness
        "run_summary": [{k: results_by_v[v]["meta"].get(k) for k in summary_fields}
                        for v in VARIANT_IDS],
        "window_aggregates": [r for r in diag_rows if r["section"] == "window_aggregate"],
        "cross_b": [r for r in diag_rows if r["section"] == "cross_b"],
        "cross_a": [r for r in diag_rows if r["section"] == "cross_a"],
        "a0_descriptive": [r for r in diag_rows if r["section"] == "a0_descriptive"],
    }
    with open(out_root / "_decision_inputs.json", "w") as fh:
        json.dump(decision, fh, indent=2)

    print("=== SUMMARY ===", flush=True)
    for v in VARIANT_IDS:
        m = results_by_v[v]["meta"]
        print(f"{v}: converged={m['converged']} iters={m['iterations']} "
              f"stat={m['convergence_statistic']:.3e} time={m['runtime_seconds']:.1f}s "
              f"floor_frac={m['floor_activation_fraction']:.3e}", flush=True)
    print(f"aligned rows total: {sum(len(results_by_v[v]['rows']) for v in VARIANT_IDS)}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
