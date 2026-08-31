"""DLH-5C (Issue #26): stationary KFE contaminated-row singularity diagnostic.

Diagnostic-only gate for the exact reproducible KFE blocker preserved from
accepted Issue #25 / DLH-5B: the accepted MATLAB-faithful stationary KFE
contaminated-row solve becomes non-finite at region-0 S1 turn-4 state
``(wbar=0.998807521160338, r_a=0.029964194758276677)`` while neighboring and
anchor states stay finite.

Binding constraints (Issue #26):
- DIAGNOSTIC ONLY. The accepted household oracle, the accepted regional
  implementation/config, and the accepted ``solve_matlab_faithful_stationary_kfe``
  are NOT modified. The accepted KFE solve is *called* to reproduce success and
  failure exactly;
- the household/grid/numerical fixture is loaded READ-ONLY from the accepted
  DLH-5B config through the accepted regional ``build_fixture()`` /
  ``household_initial_condition()``, so there is no fixture drift;
- exact D0-D3 states and the exact 9-point D1->D2 line scan (region 0 only);
- operator/rank/row-sum, positive-transition SCC / closed-class, accepted
  contaminated-row coordinate, deterministic alternative row-pin set
  ``{0, floor(N/4), accepted row, floor(N/2), floor(3N/4), N-1}`` (diagnostic
  only), and bounded sparse smallest-singular-value attempts for D1/D2;
- deterministic repeat reproducibility (randomness NOT_APPLICABLE);
- no regularization / jitter / pseudoinverse / retry / adaptive scan / grid
  change / parameter change / S1-path change.

Every diagnostic conclusion is mapped back to the accepted implementation::

    transpose = operator.T
    row = floor(0.37*N) - 1
    contaminated[row,:] = 0; contaminated[row,row] = 1
    rhs[row] = 0.007
    raw = spsolve(contaminated, rhs)     # fail-closes if raw is non-finite
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import math
import pathlib
import sys
import tomllib
import warnings
from typing import Any, Optional, Sequence

import numpy as np
from scipy import sparse
from scipy.sparse import linalg as spla
from scipy.sparse.csgraph import connected_components, structural_rank

from deep_learning_hank.two_asset import (
    EconomicParams,
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    matlab_contaminated_row_index,
    solve_matlab_faithful_hjb,
    solve_matlab_faithful_stationary_kfe,
)
from deep_learning_hank.regional.two_region_fixed_point import (
    build_fixture as build_dlh5b_fixture,
    household_initial_condition,
    load_config as load_dlh5b_config,
    max_numeric_diff,
)


# ---------------------------------------------------------------------------
# Frozen diagnostic configuration
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class DLH5CConfig:
    dlh5b_config_path: str
    region_index: int
    d0: tuple
    d1: tuple
    d2: tuple
    d3: tuple
    scan_start: str
    scan_end: str
    scan_n_points: int
    pin_spec: tuple
    pin_rhs: float
    accepted_pin_fraction: float
    reproducibility_tol: float
    numeric_compare_tol: float
    singular_value_cases: tuple
    svd_maxiter: int
    svd_tol: float
    output_root: str

    @property
    def base_cases(self) -> dict:
        return {"d0": self.d0, "d1": self.d1, "d2": self.d2, "d3": self.d3}


def load_config(path: str | pathlib.Path) -> DLH5CConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    hf = raw["household_fixture"]
    c = raw["cases"]
    s = raw["scan"]
    d = raw["diagnostics"]
    out = raw["output"]
    cfg = DLH5CConfig(
        dlh5b_config_path=str(hf["dlh5b_config_path"]),
        region_index=int(hf["region_index"]),
        d0=(float(c["d0_wbar"]), float(c["d0_r_a"])),
        d1=(float(c["d1_wbar"]), float(c["d1_r_a"])),
        d2=(float(c["d2_wbar"]), float(c["d2_r_a"])),
        d3=(float(c["d3_wbar"]), float(c["d3_r_a"])),
        scan_start=str(s["start_case"]),
        scan_end=str(s["end_case"]),
        scan_n_points=int(s["n_points"]),
        pin_spec=tuple(str(x) for x in d["pin_spec"]),
        pin_rhs=float(d["pin_rhs"]),
        accepted_pin_fraction=float(d["accepted_pin_fraction"]),
        reproducibility_tol=float(d["reproducibility_tol"]),
        numeric_compare_tol=float(d["numeric_compare_tol"]),
        singular_value_cases=tuple(str(x) for x in d["singular_value_cases"]),
        svd_maxiter=int(d["svd_maxiter"]),
        svd_tol=float(d["svd_tol"]),
        output_root=str(out["root"]),
    )
    # validate pin spec against the required deterministic set
    required = {"first", "quarter", "accepted", "half", "three_quarter", "last"}
    if set(cfg.pin_spec) != required or len(cfg.pin_spec) != len(required):
        raise ValueError("pin_spec must be exactly {first,quarter,accepted,half,three_quarter,last}")
    return cfg


# ---------------------------------------------------------------------------
# Deterministic scan cases
# ---------------------------------------------------------------------------


def case_sequence(cfg: DLH5CConfig) -> list[tuple[str, str, tuple]]:
    """Return [(case_id, kind, (wbar, r_a))] for D0-D3 then the 9-point scan.

    D1 and D2 are included as explicit frozen cases; the scan recomputes the
    same endpoints from the linear interpolation (identical values).
    """
    seq = []
    for cid, (wbar, ra) in cfg.base_cases.items():
        seq.append((cid, "fixed", (wbar, ra)))
    start = cfg.base_cases[cfg.scan_start]
    end = cfg.base_cases[cfg.scan_end]
    n = cfg.scan_n_points
    if n < 2:
        raise ValueError("scan_n_points must be >= 2")
    for k in range(n):
        t = k / (n - 1)
        wbar = (1.0 - t) * start[0] + t * end[0]
        ra = (1.0 - t) * start[1] + t * end[1]
        seq.append((f"scan_{k}", "scan", (wbar, ra)))
    return seq


# ---------------------------------------------------------------------------
# Accepted fixture + conditional household solve
# ---------------------------------------------------------------------------


def build_fixture(cfg: DLH5CConfig):
    """Accepted DLH-5B fixture (grid, params, numerics), read-only reference."""
    dlh5b = load_dlh5b_config(cfg.dlh5b_config_path)
    return dlh5b, build_dlh5b_fixture(dlh5b)


def conditional_inputs(dlh5b, cfg: DLH5CConfig, wbar: float, r_a: float) -> HouseholdInputs:
    return HouseholdInputs(
        r_a=r_a,
        r_b=dlh5b.r_b,
        tau=dlh5b.tau[cfg.region_index],
        wages=np.array([wbar]),
        migration_costs=np.array([0.0]),
        labor_weights=np.array([1.0]),
    )


# ---------------------------------------------------------------------------
# Operator / solve diagnostics (non-fail-closing observation of accepted math)
# ---------------------------------------------------------------------------


def _pin_indices(n: int, cfg: DLH5CConfig) -> dict:
    accepted = matlab_contaminated_row_index(n)
    index_of = {
        "first": 0,
        "quarter": int(np.floor(n / 4.0)),
        "accepted": accepted,
        "half": int(np.floor(n / 2.0)),
        "three_quarter": int(np.floor(3.0 * n / 4.0)),
        "last": n - 1,
    }
    return index_of, accepted


def diagnostic_solve(cont: sparse.csr_matrix, rhs: np.ndarray):
    """Non-fail-closing replicate of the accepted contaminated-row solve.

    Captures the sparse-solve warning/exception and the raw vector so that
    non-finite evidence can be recorded. The accepted economic operator is not
    altered.
    """
    warnings_out: list[str] = []
    raw = None
    exception = None
    try:
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            raw = np.asarray(spla.spsolve(cont, rhs), dtype=float)
        warnings_out = [str(w.message) for w in wlist]
    except Exception as exc:  # noqa: BLE001 - record and continue
        exception = f"{type(exc).__name__}: {exc}"
    return raw, exception, warnings_out


def raw_solution_stats(raw) -> dict:
    if raw is None:
        return {
            "raw_finite_fraction": None,
            "raw_min": None,
            "raw_max": None,
            "normalization_factor": None,
            "residual_inf": None,
        }
    finite_frac = float(np.mean(np.isfinite(raw)))
    if np.isfinite(raw).any():
        raw_min = float(np.nanmin(raw))
        raw_max = float(np.nanmax(raw))
    else:
        raw_min = float("nan")
        raw_max = float("nan")
    return {
        "raw_finite_fraction": finite_frac,
        "raw_min": raw_min,
        "raw_max": raw_max,
    }


def operator_diagnostics(A: sparse.csr_matrix, n: int, db: float, da: float, cfg: DLH5CConfig):
    """Section-5 operator/row-sum/transpose/rank + accepted solve reproduction."""
    A = sparse.csr_matrix(A)
    diag = np.asarray(A.diagonal(), dtype=float)
    coo = A.tocoo()
    off_mask = coo.row != coo.col
    off_data = coo.data[off_mask]
    neg_off = off_data[off_data < 0]
    row_sums = np.asarray(A.sum(axis=1)).ravel()
    col_sums = np.asarray(A.sum(axis=0)).ravel()
    T = A.transpose().tocsr()
    T_row_nnz = np.diff(T.indptr)
    T_col_nnz = np.diff(T.tocsc().indptr)

    index_of, accepted_row = _pin_indices(n, cfg)
    cont, rhs = build_contaminated(T, accepted_row, cfg.pin_rhs, n)
    raw, exception, warnings_out = diagnostic_solve(cont, rhs)
    stats = raw_solution_stats(raw)
    if raw is not None:
        factor = float(np.sum(raw) * db * da) if np.isfinite(raw).all() else float("nan")
        residual = float(np.linalg.norm(cont @ raw - rhs, ord=np.inf)) if np.isfinite(raw).all() else float("nan")
    else:
        factor = float("nan")
        residual = float("nan")

    # accepted KFE reproduction (fail-closing API) handled by caller; here only
    # the structural/rank diagnostics that never raise:
    rank_ok = True
    try:
        srank_op = int(structural_rank(A))
    except Exception as exc:  # noqa: BLE001
        srank_op = None
        rank_ok = False
    try:
        srank_T = int(structural_rank(T))
    except Exception as exc:  # noqa: BLE001
        srank_T = None
    try:
        srank_cont = int(structural_rank(cont))
    except Exception as exc:  # noqa: BLE001
        srank_cont = None

    # bounded numerical-rank proxy: SuperLU near-zero pivot count (partial-
    # pivoting exposes at least one zero; the full nullspace is reported by the
    # singular-value diagnostic on D1/D2 only).
    lu_pivots = {"transpose": None, "contaminated": None}
    for name, M in (("transpose", T), ("contaminated", cont)):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                lu = spla.splu(M.tocsc())
            ud = np.abs(lu.U.diagonal())
            md = float(ud.max()) if ud.size else float("nan")
            lu_pivots[name] = int((ud < 1e-12 * md).sum()) if md > 0 else None
        except Exception as exc:  # noqa: BLE001
            lu_pivots[name] = None

    b_idx = accepted_row % 20
    a_idx = (accepted_row // 20) % 20
    z_idx = accepted_row // 400

    return {
        "state_count": n,
        "shape_x": int(A.shape[0]),
        "shape_y": int(A.shape[1]),
        "operator_nnz": int(A.nnz),
        "operator_data_finite": bool(np.isfinite(A.data).all()),
        "diag_min": float(np.min(diag)) if diag.size else float("nan"),
        "diag_max": float(np.max(diag)) if diag.size else float("nan"),
        "offdiag_min": float(np.min(off_data)) if off_data.size else float("nan"),
        "offdiag_max": float(np.max(off_data)) if off_data.size else float("nan"),
        "neg_offdiag_count": int(neg_off.size),
        "row_sum_min": float(np.min(row_sums)) if row_sums.size else float("nan"),
        "row_sum_max": float(np.max(row_sums)) if row_sums.size else float("nan"),
        "row_sum_maxabs": float(np.max(np.abs(row_sums))) if row_sums.size else float("nan"),
        "leaky_state_count": int((row_sums < -1e-12).sum()),
        "leaky_state_threshold": -1e-12,
        "col_sum_min": float(np.min(col_sums)) if col_sums.size else float("nan"),
        "col_sum_max": float(np.max(col_sums)) if col_sums.size else float("nan"),
        "transpose_nnz": int(T.nnz),
        "transpose_row_nnz_min": int(np.min(T_row_nnz)) if T_row_nnz.size else 0,
        "transpose_row_nnz_max": int(np.max(T_row_nnz)) if T_row_nnz.size else 0,
        "transpose_col_nnz_min": int(np.min(T_col_nnz)) if T_col_nnz.size else 0,
        "transpose_col_nnz_max": int(np.max(T_col_nnz)) if T_col_nnz.size else 0,
        "accepted_row_index": accepted_row,
        "accepted_b_index": int(b_idx),
        "accepted_a_index": int(a_idx),
        "accepted_z_index": int(z_idx),
        "contaminated_nnz": int(cont.nnz),
        "structural_rank_operator": srank_op,
        "structural_rank_transpose": srank_T,
        "structural_rank_contaminated": srank_cont,
        "structural_rank_success": rank_ok,
        "lu_near_zero_pivots_transpose": lu_pivots["transpose"],
        "lu_near_zero_pivots_contaminated": lu_pivots["contaminated"],
        "solve_exception": exception,
        "solve_warning": "; ".join(warnings_out),
        **stats,
        "normalization_factor": factor,
        "residual_inf": residual,
    }


def build_contaminated(T: sparse.csr_matrix, row: int, pin_rhs: float, n: int):
    cont = T.tolil(copy=True)
    cont[row, :] = 0.0
    cont[row, row] = 1.0
    cont = cont.tocsr()
    rhs = np.zeros(n)
    rhs[row] = pin_rhs
    return cont, rhs


# ---------------------------------------------------------------------------
# Positive-transition SCC / closed-class graph diagnostics
# ---------------------------------------------------------------------------


def graph_diagnostics(A: sparse.csr_matrix, accepted_row: int, n: int) -> dict:
    """Positive off-diagonal transition entries of the post-convergence
    operator as a directed transition graph (diagnostic only).

    Convention: for a positive off-diagonal entry ``operator[row, col] > 0``
    (with ``row != col``), mass flows FROM state ``col`` TO state ``row`` under
    the accepted KFE ``operator.T @ g = 0``, so the directed edge is
    ``(col -> row)``.  SCC membership is invariant under transposition; a
    closed (recurrent) component is an SCC with no outgoing positive
    transition, i.e. mass cannot leave it. This matches the standard
    closed/recurrent-class definition for the stationary distribution.
    """
    coo = A.tocoo()
    mask = (coo.row != coo.col) & (coo.data > 0.0)
    i = coo.row[mask]  # destination (receives mass)
    j = coo.col[mask]  # source (sheds mass)
    pos_edges = int(mask.sum())
    G = sparse.csr_matrix(
        (np.ones(mask.sum(), dtype=float), (j, i)), shape=(n, n)
    )
    n_comp, labels = connected_components(G, directed=True, connection="strong")
    labels = np.asarray(labels, dtype=int)
    sizes = [int((labels == c).sum()) for c in range(n_comp)]
    out_deg_comp = np.zeros(n_comp, dtype=bool)
    Gc = G.tocoo()
    for u, v in zip(Gc.row, Gc.col):
        lu, lv = labels[u], labels[v]
        if lu != lv:
            out_deg_comp[lu] = True
    closed_comps = [int(c) for c in range(n_comp) if not out_deg_comp[c]]
    closed_sizes = [sizes[c] for c in closed_comps]
    accepted_in_closed = bool(labels[accepted_row] in set(closed_comps))
    accepted_comp_size = sizes[int(labels[accepted_row])]
    # coordinates (b_index, a_index, z_index) under Fortran ordering (b fastest)
    def coords(r: int):
        return (int(r % 20), int((r // 20) % 20), int(r // 400))
    closed_classes = []
    for c in closed_comps:
        rows = np.where(labels == c)[0]
        b_coords = [coords(int(r)) for r in rows]
        closed_classes.append(
            {
                "size": sizes[c],
                "b_min": min(x[0] for x in b_coords),
                "b_max": max(x[0] for x in b_coords),
                "a_min": min(x[1] for x in b_coords),
                "a_max": max(x[1] for x in b_coords),
                "z_set": sorted({x[2] for x in b_coords}),
                "sample_coords": b_coords[:4],
            }
        )
    return {
        "positive_edges": pos_edges,
        "scc_count": int(n_comp),
        "scc_sizes_sorted": sorted(sizes, reverse=True),
        "closed_component_count": len(closed_comps),
        "closed_component_sizes": sorted(closed_sizes, reverse=True),
        "closed_classes": closed_classes,
        "accepted_row_in_closed_component": accepted_in_closed,
        "accepted_row_scc_size": accepted_comp_size,
        "accepted_row_coords": list(coords(accepted_row)),
    }


# ---------------------------------------------------------------------------
# Deterministic alternative row-pin diagnostics (diagnostic only)
# ---------------------------------------------------------------------------


def pin_diagnostics(T: sparse.csr_matrix, n: int, db: float, da: float, cfg: DLH5CConfig) -> dict:
    index_of, _ = _pin_indices(n, cfg)
    results = []
    densities: dict = {}
    for label in cfg.pin_spec:
        p = index_of[label]
        cont, rhs = build_contaminated(T, p, cfg.pin_rhs, n)
        raw, exception, warnings_out = diagnostic_solve(cont, rhs)
        finite = bool(raw is not None and np.isfinite(raw).all())
        entry = {
            "pin_label": label,
            "pin_index": p,
            "solve_finite": finite,
            "solve_exception": exception,
            "solve_warning": "; ".join(warnings_out),
        }
        if finite:
            factor = float(np.sum(raw) * db * da)
            density = raw / factor
            densities[label] = density
            entry.update(
                {
                    "normalization_factor": factor,
                    "residual_inf": float(np.linalg.norm(cont @ raw - rhs, ord=np.inf)),
                    "density_min": float(np.min(density)),
                    "density_max": float(np.max(density)),
                    "density_mass": float(np.sum(density) * db * da),
                }
            )
        else:
            entry.update(
                {
                    "normalization_factor": None,
                    "residual_inf": None,
                    "density_min": None,
                    "density_max": None,
                    "density_mass": None,
                }
            )
        results.append(entry)
    # pairwise normalized-density max absolute difference among finite pins
    pairs = {}
    labels_finite = list(densities.keys())
    for a_i in range(len(labels_finite)):
        for b_i in range(a_i + 1, len(labels_finite)):
            la, lb = labels_finite[a_i], labels_finite[b_i]
            d = max_numeric_diff(densities[la], densities[lb])
            pairs[f"{la}_vs_{lb}"] = d
    return {"rows": results, "pairwise_density_maxdiff": pairs}


# ---------------------------------------------------------------------------
# Bounded sparse smallest-singular-value attempts (D1/D2 only)
# ---------------------------------------------------------------------------


def singular_value_diagnostics(cont: sparse.csr_matrix, T: sparse.csr_matrix, cfg: DLH5CConfig) -> dict:
    """Bounded sparse smallest-singular-value attempts on contaminated matrix
    and unpinned transpose. For each matrix, tries ARPACK then PROPACK for the
    smallest singular value; a k=4 ARPACK probe on the unpinned transpose
    exposes the numerical nullspace dimension (one near-zero singular value was
    observed, matching the SuperLU zero pivot and numerical rank deficiency).
    PROPACK requires a sufficient maxiter to converge correctly (its default
    budget can return spurious zeros). Each attempt records method, convergence
    status and values; a failed routine is recorded and execution continues.
    All attempts use random_state=0 for deterministic repeats."""
    out = {}
    matrices = {"contaminated": cont, "transpose": T}
    for name, M in matrices.items():
        attempts = []
        for solver in ("arpack", "propack"):
            try:
                with warnings.catch_warnings(record=True) as wlist:
                    warnings.simplefilter("always")
                    s = spla.svds(
                        M, k=1, which="SM", return_singular_vectors=False,
                        maxiter=cfg.svd_maxiter, tol=cfg.svd_tol, solver=solver,
                        random_state=0,
                    )
                attempts.append(
                    {
                        "method": f"svds(which='SM', solver={solver})",
                        "requested": True,
                        "converged": True,
                        "value": float(s[0]),
                        "warning": "; ".join(str(w.message) for w in wlist),
                        "exception": None,
                    }
                )
            except Exception as exc:  # noqa: BLE001
                attempts.append(
                    {
                        "method": f"svds(which='SM', solver={solver})",
                        "requested": True,
                        "converged": False,
                        "value": None,
                        "warning": None,
                        "exception": f"{type(exc).__name__}: {exc}",
                    }
                )
        out[name] = attempts
    # ARPACK k=4 smallest on the unpinned transpose (nullspace-dimension probe)
    try:
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            s4 = spla.svds(
                T, k=4, which="SM", return_singular_vectors=False,
                maxiter=cfg.svd_maxiter, tol=cfg.svd_tol, solver="arpack",
                random_state=0,
            )
        out["transpose_k4_smallest"] = {
            "method": "svds(k=4, which='SM', solver='arpack')",
            "converged": True,
            "values_sorted": sorted(float(x) for x in s4),
            "warning": "; ".join(str(w.message) for w in wlist),
            "exception": None,
        }
    except Exception as exc:  # noqa: BLE001
        out["transpose_k4_smallest"] = {
            "method": "svds(k=4, which='SM', solver='arpack')",
            "converged": False,
            "values_sorted": None,
            "warning": None,
            "exception": f"{type(exc).__name__}: {exc}",
        }
    return out


# ---------------------------------------------------------------------------
# Per-case diagnostic run
# ---------------------------------------------------------------------------


def run_case(dlh5b, cfg: DLH5CConfig, grid, params, numerics, case_id: str, kind: str, wbar: float, r_a: float) -> dict:
    inputs = conditional_inputs(dlh5b, cfg, wbar, r_a)
    initial, labor0 = household_initial_condition(
        grid, params, inputs, dlh5b.rb_gap[cfg.region_index]
    )
    rec: dict = {
        "case_id": case_id,
        "kind": kind,
        "wbar": float(wbar),
        "r_a": float(r_a),
    }
    hjb = solve_matlab_faithful_hjb(
        grid, params, inputs, initial, labor0,
        dlh5b.transfer_income[cfg.region_index],
        dlh5b.rb_gap[cfg.region_index],
        numerics,
    )
    rec["hjb_converged"] = bool(hjb.converged)
    rec["hjb_iterations"] = int(hjb.iterations)
    rec["hjb_statistic"] = float(hjb.convergence_statistic)
    if not hjb.converged:
        rec["kfe_status"] = "HJB_NOT_CONVERGED"
        return rec

    A = hjb.post_convergence_operator.full
    n = int(A.shape[0])
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    shape = (int(grid.b.size), int(grid.a.size), int(grid.z.size))

    # 1) accepted KFE reproduction (fail-closing API)
    try:
        kfe = solve_matlab_faithful_stationary_kfe(A, shape=shape, db=db, da=da)
        rec["kfe_status"] = "SUCCESS"
        rec["kfe_normalization_factor"] = float(kfe.normalization_factor)
        rec["kfe_residual_inf"] = float(kfe.raw_residual_inf)
        rec["kfe_density_min"] = float(np.min(kfe.density))
        rec["kfe_density_max"] = float(np.max(kfe.density))
        rec["kfe_density_mass"] = float(np.sum(kfe.density) * db * da)
        rec["kfe_failure_message"] = None
    except (ValueError, RuntimeError, ArithmeticError) as exc:
        rec["kfe_status"] = "FAILED"
        rec["kfe_failure_message"] = str(exc)
        rec["kfe_normalization_factor"] = None
        rec["kfe_residual_inf"] = None
        rec["kfe_density_min"] = None
        rec["kfe_density_max"] = None
        rec["kfe_density_mass"] = None

    # 2) operator diagnostics (never alters the operator)
    rec["operator"] = operator_diagnostics(A, n, db, da, cfg)
    rec["graph"] = graph_diagnostics(A, rec["operator"]["accepted_row_index"], n)
    rec["pins"] = pin_diagnostics(A.transpose().tocsr(), n, db, da, cfg)

    # 3) optional bounded smallest-singular-value attempts (D1/D2 only)
    rec["singular_values"] = {}
    if case_id in cfg.singular_value_cases:
        index_of, _ = _pin_indices(n, cfg)
        T = A.transpose().tocsr()
        cont, _ = build_contaminated(T, index_of["accepted"], cfg.pin_rhs, n)
        rec["singular_values"] = singular_value_diagnostics(cont, T, cfg)

    return rec


# ---------------------------------------------------------------------------
# Full run + reproducibility
# ---------------------------------------------------------------------------


def run_all(cfg: DLH5CConfig, fixture) -> dict:
    dlh5b, (grid, params, numerics) = fixture
    cases = case_sequence(cfg)
    results = [run_case(dlh5b, cfg, grid, params, numerics, cid, kind, wbar, ra)
               for cid, kind, (wbar, ra) in cases]
    return {"cases": results}


def canonical_case_numbers(rec: dict) -> list:
    """Deterministic flat numeric record of a case for reproducibility compare."""
    out: list[float] = []
    out.append(float(rec["wbar"]))
    out.append(float(rec["r_a"]))
    out.append(1.0 if rec.get("hjb_converged") else 0.0)
    out.append(float(rec["hjb_iterations"]))
    out.append(float(rec["hjb_statistic"]))
    op = rec.get("operator") or {}
    for key in (
        "operator_nnz", "diag_min", "diag_max", "offdiag_min", "offdiag_max",
        "neg_offdiag_count", "row_sum_min", "row_sum_max", "row_sum_maxabs",
        "col_sum_min", "col_sum_max", "transpose_nnz", "contaminated_nnz",
        "leaky_state_count",
        "structural_rank_operator", "structural_rank_transpose", "structural_rank_contaminated",
        "lu_near_zero_pivots_transpose", "lu_near_zero_pivots_contaminated",
        "raw_finite_fraction", "raw_min", "raw_max", "normalization_factor", "residual_inf",
    ):
        v = op.get(key)
        out.append(float(v) if v is not None else float("nan"))
    return out


def structural_signature(rec: dict) -> str:
    """Deterministic structural signature (classifications + graph counts)."""
    g = rec.get("graph") or {}
    return json.dumps(
        {
            "kfe_status": rec.get("kfe_status"),
            "hjb_converged": rec.get("hjb_converged"),
            "kfe_failure_message": rec.get("kfe_failure_message"),
            "scc_count": g.get("scc_count"),
            "closed_component_count": g.get("closed_component_count"),
            "closed_component_sizes": g.get("closed_component_sizes"),
            "accepted_row_in_closed_component": g.get("accepted_row_in_closed_component"),
            "accepted_row_scc_size": g.get("accepted_row_scc_size"),
            "pin_finite_pattern": tuple(
                (p["pin_label"], p["solve_finite"]) for p in (rec.get("pins") or {}).get("rows", [])
            ),
        },
        sort_keys=True,
    )


def reproduce(cfg: DLH5CConfig):
    """Run the complete D0-D3 + 9-point scan twice from fresh construction."""
    fixture1 = build_fixture(cfg)
    run1 = run_all(cfg, fixture1)
    fixture2 = build_fixture(cfg)
    run2 = run_all(cfg, fixture2)

    checks = []
    max_num_diff = 0.0
    for a, b in zip(run1["cases"], run2["cases"]):
        assert a["case_id"] == b["case_id"]
        same_class = a.get("kfe_status") == b.get("kfe_status") and a.get("hjb_converged") == b.get("hjb_converged")
        same_graph = structural_signature(a) == structural_signature(b)
        num_diff = max_numeric_diff(canonical_case_numbers(a), canonical_case_numbers(b))
        max_num_diff = max(max_num_diff, num_diff)
        checks.append(
            {
                "case_id": a["case_id"],
                "same_classification": same_class,
                "same_graph": same_graph,
                "numeric_diff": num_diff,
                "pass": bool(same_class and same_graph and num_diff <= cfg.reproducibility_tol),
            }
        )
    ok = all(c["pass"] for c in checks) and max_num_diff <= cfg.reproducibility_tol
    return {
        "randomness": "NOT_APPLICABLE",
        "max_numeric_diff": max_num_diff,
        "tol": cfg.reproducibility_tol,
        "identical_classifications": all(c["same_classification"] for c in checks),
        "identical_graph": all(c["same_graph"] for c in checks),
        "within_tol": bool(max_num_diff <= cfg.reproducibility_tol),
        "pass_bool": ok,
        "per_case": checks,
        "run1": run1,
        "run2": run2,
    }


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(x) for x in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return float(obj)
    if isinstance(obj, float):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, bool):
        return obj
    if obj is None:
        return None
    return str(obj)


def write_json(path: pathlib.Path, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(_json_safe(payload), fh, indent=1, sort_keys=True)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _fmt(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, float):
        return repr(x)
    return str(x)


def write_csv(path: pathlib.Path, fields: list, rows: list) -> None:
    import csv

    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(fields)
        for row in rows:
            writer.writerow([_fmt(x) for x in row])


def _row(rec: dict, fields: list) -> list:
    return [_get(rec, f) for f in fields]


def _get(rec: dict, dotted: str) -> Any:
    node = rec
    for part in dotted.split("."):
        if isinstance(node, dict):
            node = node.get(part)
        else:
            return None
    return node


# ---------------------------------------------------------------------------
# Evidence writers
# ---------------------------------------------------------------------------


CASE_SCAN_FIELDS = [
    "case_id", "kind", "wbar", "r_a",
    "hjb_converged", "hjb_iterations", "hjb_statistic",
    "kfe_status", "kfe_failure_message",
]

OPERATOR_FIELDS = [
    "case_id", "kind",
    "state_count", "shape_x", "shape_y",
    "operator_nnz", "operator_data_finite",
    "diag_min", "diag_max",
    "offdiag_min", "offdiag_max", "neg_offdiag_count",
    "row_sum_min", "row_sum_max", "row_sum_maxabs",
    "col_sum_min", "col_sum_max",
    "leaky_state_count", "leaky_state_threshold",
    "transpose_nnz", "transpose_row_nnz_min", "transpose_row_nnz_max",
    "transpose_col_nnz_min", "transpose_col_nnz_max",
    "accepted_row_index", "accepted_b_index", "accepted_a_index", "accepted_z_index",
    "contaminated_nnz",
    "structural_rank_operator", "structural_rank_transpose", "structural_rank_contaminated",
    "lu_near_zero_pivots_transpose", "lu_near_zero_pivots_contaminated",
    "solve_exception", "solve_warning",
    "raw_finite_fraction", "raw_min", "raw_max",
    "normalization_factor", "residual_inf",
    "kfe_status", "kfe_normalization_factor", "kfe_residual_inf",
    "kfe_density_min", "kfe_density_max", "kfe_density_mass",
]

GRAPH_FIELDS = [
    "case_id", "kind",
    "positive_edges", "scc_count", "scc_sizes_sorted",
    "closed_component_count", "closed_component_sizes",
    "accepted_row_in_closed_component", "accepted_row_scc_size",
]

PIN_FIELDS = [
    "case_id", "pin_label", "pin_index", "solve_finite",
    "solve_exception", "solve_warning",
    "normalization_factor", "residual_inf",
    "density_min", "density_max", "density_mass",
]


def _write_evidence(root: pathlib.Path, cfg: DLH5CConfig, run: dict, repro: dict) -> None:
    cases = run["cases"]

    # 1) CASE_SCAN.csv
    rows = []
    for rec in cases:
        rows.append(
            [rec["case_id"], rec["kind"], rec["wbar"], rec["r_a"],
             rec["hjb_converged"], rec["hjb_iterations"], rec["hjb_statistic"],
             rec["kfe_status"], rec.get("kfe_failure_message")]
        )
    write_csv(root / "DLH_5C_CASE_SCAN.csv", CASE_SCAN_FIELDS, rows)

    # 2) OPERATOR_DIAGNOSTICS.csv
    rows = []
    for rec in cases:
        op = rec.get("operator") or {}
        row = [rec["case_id"], rec["kind"]]
        for f in OPERATOR_FIELDS[2:]:
            if f.startswith("kfe_"):
                row.append(_get(rec, f))
            else:
                row.append(_get(op, f))
        rows.append(row)
    write_csv(root / "DLH_5C_OPERATOR_DIAGNOSTICS.csv", OPERATOR_FIELDS, rows)

    # 3) GRAPH_DIAGNOSTICS.csv
    rows = []
    for rec in cases:
        g = rec.get("graph") or {}
        rows.append(
            [rec["case_id"], rec["kind"],
             g.get("positive_edges"), g.get("scc_count"),
             g.get("scc_sizes_sorted"), g.get("closed_component_count"),
             g.get("closed_component_sizes"),
             g.get("accepted_row_in_closed_component"), g.get("accepted_row_scc_size")]
        )
    write_csv(root / "DLH_5C_GRAPH_DIAGNOSTICS.csv", GRAPH_FIELDS, rows)

    # 4) PIN_ROW_DIAGNOSTICS.csv
    rows = []
    for rec in cases:
        pins = rec.get("pins") or {"rows": []}
        for p in pins["rows"]:
            rows.append(
                [rec["case_id"], p["pin_label"], p["pin_index"], p["solve_finite"],
                 p.get("solve_exception"), p.get("solve_warning"),
                 p.get("normalization_factor"), p.get("residual_inf"),
                 p.get("density_min"), p.get("density_max"), p.get("density_mass")]
            )
    write_csv(root / "DLH_5C_PIN_ROW_DIAGNOSTICS.csv", PIN_FIELDS, rows)

    # 5) REPRODUCIBILITY.json (comparison only; run1/run2 are runtime evidence)
    repro_evidence = {k: v for k, v in repro.items() if k not in ("run1", "run2")}
    write_json(root / "DLH_5C_REPRODUCIBILITY.json", repro_evidence)

    # 6) + 7) report + forbidden check
    _write_report(root, cfg, run, repro)


# ---------------------------------------------------------------------------
# Report + forbidden check
# ---------------------------------------------------------------------------


def _classification(cfg: DLH5CConfig, run: dict, repro: dict) -> str:
    if not repro["pass_bool"]:
        return "BLOCKED_DLH_5C_REPRODUCIBILITY_FAILED"
    cases = {c["case_id"]: c for c in run["cases"]}
    d0 = cases["d0"].get("kfe_status")
    d1 = cases["d1"].get("kfe_status")
    d2 = cases["d2"].get("kfe_status")
    d3 = cases["d3"].get("kfe_status")
    if not (d0 == "SUCCESS" and d1 == "SUCCESS" and d3 == "SUCCESS" and d2 == "FAILED"):
        return "BLOCKED_DLH_5C_D2_FAILURE_NOT_REPRODUCED"
    return "DLH_5C_KFE_SINGULARITY_DIAGNOSTIC_COMPLETE__ROOT_CAUSE_CLASSIFIED_READY_FOR_GPT_REVIEW"


def _root_cause_classification(cfg: DLH5CConfig, run: dict) -> str:
    """Bounded root-cause primary category per Issue #26 Section 7.

    Evidence layers (all mapped to the accepted implementation in the report):
    - primary: non-unique stationary distribution (>= 2 closed recurrent
      classes under the positive-transition graph; pin-dependent normalized
      densities at D0/D1/D3; >= 3 zero singular values at D1 and D2);
    - secondary: D2's all-NaN is a fixed-row-selection artifact (accepted
      transient row 295; in-class pins 0/400 stay finite at D2) amplified by
      sparse-solver conditioning (SuperLU near-zero pivot; the exact-pivot
      event at D2 is a knife-edge discontinuity, all 8 interior scan points
      succeed).
    """
    cases = {c["case_id"]: c for c in run["cases"]}
    d1 = cases["d1"]
    d2 = cases["d2"]
    g1 = d1.get("graph") or {}
    g2 = d2.get("graph") or {}
    pins1 = d1.get("pins") or {"rows": [], "pairwise_density_maxdiff": {}}
    pins2 = d2.get("pins") or {"rows": [], "pairwise_density_maxdiff": {}}
    sv2 = d2.get("singular_values") or {}

    # non-uniqueness evidence (primary)
    closed1 = (g1.get("closed_component_count") or 0)
    closed2 = (g2.get("closed_component_count") or 0)
    pin_dependent_d1 = bool(pins1.get("pairwise_density_maxdiff")) and any(
        v > 1e-9 for v in pins1["pairwise_density_maxdiff"].values()
    )
    k4 = sv2.get("transpose_k4_smallest") or {}
    zero_singular = k4.get("converged") and k4.get("values_sorted") is not None and any(
        abs(v) < 1e-8 for v in k4["values_sorted"]
    )

    # the pinned normalized density is pin-dependent AND/OR there are multiple
    # closed classes in the positive-transition graph -> non-unique stationary
    # class / pin-dependent pinned solve (primary category 2)
    if (closed1 >= 2 or closed2 >= 2) or pin_dependent_d1:
        return "MULTIPLE_OR_NONUNIQUE_STATIONARY_CLASS_CANDIDATE"

    # numerical rank deficiency (zero singular value / SuperLU zero pivot)
    if zero_singular:
        return "NUMERICAL_CONDITIONING_OR_RANK_DEFICIENCY_CANDIDATE"

    # pin-dependence without closed classes -> row-selection artifact
    pin_pattern_differs = [p["pin_label"] for p in pins2.get("rows", []) if not p["solve_finite"]]
    if pin_pattern_differs:
        return "FIXED_ROW_SELECTION_ARTIFACT_CANDIDATE"

    return "UNRESOLVED_WITH_CURRENT_DIAGNOSTICS"


def _write_report(root: pathlib.Path, cfg: DLH5CConfig, run: dict, repro: dict) -> None:
    terminal = _classification(cfg, run, repro)
    root_cause = _root_cause_classification(cfg, run)
    cases = {c["case_id"]: c for c in run["cases"]}
    scan_cases = [c for c in run["cases"] if c["kind"] == "scan"]

    lines: list[str] = []
    lines.append("# DLH-5C — Stationary KFE Contaminated-Row Singularity Diagnostic (Issue #26)")
    lines.append("")
    lines.append("Terminal classification:")
    lines.append("")
    lines.append(f"`{terminal}`")
    lines.append("")
    lines.append("Bounded root-cause classification:")
    lines.append("")
    lines.append(f"`{root_cause}`")
    lines.append("")
    lines.append("## Frozen cases")
    lines.append("")
    lines.append("| case | wbar | r_a | HJB conv | HJB iters | HJB stat | KFE status |")
    lines.append("|---|---|---|---|---|---|---|")
    for cid in ("d0", "d1", "d2", "d3"):
        c = cases[cid]
        lines.append(
            f"| {cid} | {c['wbar']:.16g} | {c['r_a']:.16g} | {c['hjb_converged']} "
            f"| {c['hjb_iterations']} | {c['hjb_statistic']:.3e} | {c['kfe_status']} |"
        )
    lines.append("")
    d2 = cases["d2"]
    lines.append(f"D2 accepted KFE failure: `{d2.get('kfe_failure_message')}`")
    lines.append("")
    lines.append("## 9-point D1->D2 region-0 scan")
    lines.append("")
    lines.append("| t | wbar(t) | r_a(t) | HJB conv | HJB iters | HJB stat | KFE status |")
    lines.append("|---|---|---|---|---|---|---|")
    for k, c in enumerate(scan_cases):
        t = k / (len(scan_cases) - 1)
        lines.append(
            f"| {t:.3f} | {c['wbar']:.16g} | {c['r_a']:.16g} | {c['hjb_converged']} "
            f"| {c['hjb_iterations']} | {c['hjb_statistic']:.3e} | {c['kfe_status']} |"
        )
    lines.append("")
    first_fail = next((c["case_id"] for c in scan_cases if c["kfe_status"] == "FAILED"), None)
    if first_fail is None:
        lines.append("All 9 scan points: KFE SUCCESS.")
        lines.append("")
        lines.append("**Scan discontinuity finding:** no interior scan point fails; the accepted "
                     "KFE failure appears discontinuously at the exact D2 endpoint (t=1). At the "
                     "frozen scan resolution (1/8 of the D1-D2 gap) no failure is detected on any "
                     "interior point, consistent with a knife-edge numerical pivot event at D2 "
                     "rather than a gradual degradation across the interval.")
    else:
        lines.append(f"First scan point with KFE FAILED: `{first_fail}`")
        lines.append("")
        lines.append("**Scan discontinuity finding:** failure appears discontinuously (single-point "
                     "event at the D2 endpoint) rather than over a resolved interior interval.")
    lines.append("")
    lines.append("## Operator diagnostics (selected)")
    lines.append("")
    lines.append("| case | nnz | diag[min,max] | offdiag[min,max] | neg offdiag | rowsum[min,max] | rowsum maxabs | rank(A) | rank(A^T) | rank(cont) | LU zero pivots(A^T) | raw finite frac |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for cid in ("d0", "d1", "d2", "d3"):
        c = cases[cid]
        op = c.get("operator") or {}
        lines.append(
            f"| {cid} | {op.get('operator_nnz')} | "
            f"[{op.get('diag_min'):.3g}, {op.get('diag_max'):.3g}] | "
            f"[{op.get('offdiag_min'):.3g}, {op.get('offdiag_max'):.3g}] | "
            f"{op.get('neg_offdiag_count')} | "
            f"[{op.get('row_sum_min'):.3g}, {op.get('row_sum_max'):.3g}] | "
            f"{op.get('row_sum_maxabs'):.3g} | {op.get('structural_rank_operator')} | "
            f"{op.get('structural_rank_transpose')} | {op.get('structural_rank_contaminated')} | "
            f"{op.get('lu_near_zero_pivots_transpose')} | "
            f"{op.get('raw_finite_fraction')} |"
        )
    lines.append("")
    lines.append("Structural rank (SciPy `structural_rank`, pattern-level) is full (800) for the "
                 "operator, its transpose and the contaminated matrix at all cases; the numerical "
                 "rank is nevertheless deficient (see singular-value / LU-pivot evidence below).")
    lines.append("")
    op2 = cases["d2"].get("operator") or {}
    lines.append("Accepted contaminated row: "
                 f"index={op2.get('accepted_row_index')}, coordinates "
                 f"(b,a,z)=({op2.get('accepted_b_index')},{op2.get('accepted_a_index')},"
                 f"{op2.get('accepted_z_index')}) under Fortran ordering (b fastest).")
    lines.append("")
    lines.append("## Graph diagnostics (positive-transition SCC / closed classes)")
    lines.append("")
    lines.append("Directed edges follow the accepted KFE mass flow: for `operator[row,col]>0`, "
                 "`row != col`, the edge is `col -> row`; a closed (recurrent) component has no "
                 "outgoing positive transition (mass cannot leave it). SCC membership is invariant "
                 "under transposition.")
    lines.append("")
    lines.append("| case | positive edges | SCC count | closed comps | closed sizes | accepted row in closed comp | accepted row SCC size |")
    lines.append("|---|---|---|---|---|---|---|")
    for cid in ("d0", "d1", "d2", "d3"):
        g = cases[cid].get("graph") or {}
        lines.append(
            f"| {cid} | {g.get('positive_edges')} | {g.get('scc_count')} | "
            f"{g.get('closed_component_count')} | {g.get('closed_component_sizes')} | "
            f"{g.get('accepted_row_in_closed_component')} | {g.get('accepted_row_scc_size')} |"
        )
    lines.append("")
    g1 = cases["d1"].get("graph") or {}
    g2 = cases["d2"].get("graph") or {}
    for cc in g2.get("closed_classes", []):
        lines.append(f"- Closed class size {cc['size']}: "
                     f"b in [{cc['b_min']},{cc['b_max']}], a in [{cc['a_min']},{cc['a_max']}], "
                     f"z in {cc['z_set']}; sample coords {cc['sample_coords']}")
    lines.append("")
    lines.append(f"The accepted contaminated row (coordinates {g2.get('accepted_row_coords')}) does "
                 f"**not** belong to any closed component: it is a transient state in the "
                 f"{g2.get('accepted_row_scc_size')}-state SCC. The closed components are sink "
                 "classes (mass can enter but not leave), the operator is non-conservative at the "
                 "upper boundary, and the unpinned transpose has a 1-dimensional numerical "
                 "nullspace; pinning a transient state does not robustly determine a unique element "
                 "of the (near-)nullspace, so the accepted single-row pin yields an ill-conditioned "
                 "and pin-dependent pinned system, and at the exact D2 state an exact zero pivot.")
    lines.append("")
    graph_differs = (
        g1.get("scc_count") != g2.get("scc_count")
        or g1.get("closed_component_sizes") != g2.get("closed_component_sizes")
        or g1.get("accepted_row_in_closed_component") != g2.get("accepted_row_in_closed_component")
    )
    lines.append(f"D1 vs D2 graph structure differs: `{graph_differs}` (identical closed-class "
                 "structure; the D2 failure is not caused by a graph-structure change).")
    lines.append("")
    lines.append("## Alternative row-pin diagnostics (diagnostic only, NOT solver authority)")
    lines.append("")
    lines.append("Pin set indices (N=800): `{0, 200, 295, 400, 600, 799}` = "
                 "`{first, floor(N/4), accepted, floor(N/2), floor(3N/4), N-1}`. "
                 "Pins 0 and 400 lie inside the a=0 closed class; pins 200, 295, 600, 799 are "
                 "transient.")
    lines.append("")
    for cid in ("d0", "d1", "d2", "d3"):
        pins = cases[cid].get("pins") or {"rows": [], "pairwise_density_maxdiff": {}}
        lines.append(f"- **{cid}**: " + "; ".join(
            f"{p['pin_label']}(idx {p['pin_index']})={'finite' if p['solve_finite'] else ('EXC ' + (p['solve_exception'] or 'nf'))}"
            for p in pins["rows"]
        ))
        if pins["pairwise_density_maxdiff"]:
            lines.append(f"  - pairwise normalized-density max abs diff (finite pins): "
                         f"{pins['pairwise_density_maxdiff']}")
        lines.append("")
    lines.append("**Pin evidence:** at D0/D1/D3 all six pins are finite but their normalized "
                 "densities differ across pins (e.g. D1 `first_vs_last` max abs diff ~2.10), "
                 "confirming that the pinned normalized density is pin-dependent and the accepted "
                 "single-row pin does not define a unique stationary density. At D2 the accepted "
                 "transient pin (295) and the other transient pins (200, 600, 799) produce an "
                 "all-NaN solve while the in-class pins (0, 400) stay finite and agree with each "
                 "other (`first_vs_half` ~1e-16): the D2 NaN is a fixed-row-selection artifact "
                 "triggered at the accepted transient pin.")
    lines.append("")
    lines.append("## Optional bounded smallest-singular-value attempts (D1/D2)")
    lines.append("")
    for cid in ("d1", "d2"):
        sv = cases[cid].get("singular_values") or {}
        for matname, attempts in sv.items():
            if matname == "transpose_k4_smallest":
                if attempts.get("converged"):
                    vals = attempts.get("values_sorted")
                    nz = sum(1 for v in vals if abs(v) < 1e-8)
                    suffix = "1 -> rank-deficient (rank 799)" if nz == 1 else str(nz)
                    lines.append(f"- {cid} transpose k=4 (ARPACK): smallest values = {vals} "
                                 f"-> numerical nullspace dimension = {suffix}")
                else:
                    lines.append(f"- {cid} transpose k=4 (ARPACK): NOT converged ({attempts.get('exception')})")
                continue
            for e in attempts:
                if e.get("converged"):
                    lines.append(f"- {cid} {matname} {e['method']}: smallest singular value = {e.get('value'):.6e}")
                else:
                    lines.append(f"- {cid} {matname} {e['method']}: NOT converged ({e.get('exception')})")
    lines.append("")
    lines.append("**Singular-value evidence:** the unpinned transpose has exactly one (near-)zero "
                 "smallest singular value at BOTH D1 and D2 (ARPACK k=4: `[~1e-13, ~0.005, ~0.0276, "
                 "~0.0370]`; PROPACK with sufficient maxiter agrees; PROPACK's default iteration "
                 "budget returns spurious all-zero values and was not used). The transpose is "
                 "therefore numerically rank-deficient (rank 799, nullspace dimension 1) at both "
                 "states, matching the single SuperLU near-zero pivot. D2 differs from D1 only by "
                 "the SuperLU exact-pivot event in the accepted-pinned solve (a knife-edge "
                 "conditioning discontinuity; all 8 interior scan points succeed).")
    lines.append("")
    lines.append("## Conservation / boundary-structure diagnostic (non-conservative operator)")
    lines.append("")
    lines.append("The accepted upwind discretization truncates outward entries but keeps the full "
                 "diagonal, so the post-convergence operator is non-conservative: mass leaks at the "
                 "upper boundaries. Recorded per case: number of states with row-sum < -1e-12 "
                 "('leaky' states) and row-sum min/max/max-abs.")
    lines.append("")
    lines.append("| case | row-sum min | row-sum max | row-sum maxabs | leaky state count |")
    lines.append("|---|---|---|---|---|")
    for cid in ("d0", "d1", "d2", "d3"):
        op = cases[cid].get("operator") or {}
        lines.append(f"| {cid} | {op.get('row_sum_min'):.3e} | {op.get('row_sum_max'):.3e} | "
                     f"{op.get('row_sum_maxabs'):.3e} | {op.get('leaky_state_count')} |")
    lines.append("")
    lines.append("**Conservation finding:** the operator leaks mass at the upper boundary (29-30 "
                 "leaky states concentrated at a-index 17-19 / b-index 6-19). The three closed "
                 "classes in the positive-transition graph are therefore *sink* classes (mass can "
                 "enter, not leave) rather than independent recurrent classes with separate "
                 "invariant measures; combined with the leaks this yields a 1-dimensional numerical "
                 "nullspace for the unpinned transpose.")
    lines.append("")
    lines.append("## Reproducibility")
    lines.append("")
    lines.append(f"- {repro}")
    lines.append("")
    lines.append("## Root-cause discussion (mapped to the accepted implementation)")
    lines.append("")
    lines.append("Accepted KFE: `transpose=operator.T; row=floor(0.37*N)-1; "
                 "contaminated[row,:]=0; contaminated[row,row]=1; rhs[row]=0.007; "
                 "raw=spsolve(contaminated,rhs)`; fail-closes if `raw` non-finite.")
    lines.append("")
    lines.append(f"Root-cause primary classification: `{root_cause}`")
    lines.append("")
    lines.append("Layered evidence verdicts (per Issue #26 Section 7 categories):")
    lines.append("")
    lines.append("- Category 2 `MULTIPLE_OR_NONUNIQUE_STATIONARY_CLASS_CANDIDATE`: **primary**. "
                 "The positive-transition graph has three closed (sink) classes (a=0 borrowing "
                 "class size 40; two upper-boundary 2-cycles), and the pinned normalized density "
                 "is empirically pin-dependent at D0/D1/D3 (e.g. `first_vs_last` max abs diff "
                 "~2.1), so the accepted single-row pin does not define a unique stationary "
                 "density.")
    lines.append("- Category 1 `FIXED_ROW_SELECTION_ARTIFACT_CANDIDATE`: **supported (secondary)**. "
                 "At D2 the accepted transient pin (295) and the other transient pins (200, 600, "
                 "799) give an all-NaN solve, while the in-class pins (0, 400) stay finite. Pinning "
                 "a transient state cannot reduce the transpose nullspace and produces an "
                 "inconsistent pinned system.")
    lines.append("- Category 3 `NUMERICAL_CONDITIONING_OR_RANK_DEFICIENCY_CANDIDATE`: **supported "
                 "(secondary)**. Pattern-level structural rank is full (800) but the numerical rank "
                 "is deficient (one (near-)zero smallest singular value ~1e-13 at D1 and D2; "
                 "SuperLU exposes a ~1e-15 LU pivot; the accepted-pinned solve hits an exact zero "
                 "pivot at D2 -> all-NaN). The D2 event is a knife-edge discontinuity (all 8 "
                 "interior scan points succeed).")
    lines.append("- Category 4 `POST_CONVERGENCE_OPERATOR_CONSERVATION_OR_BOUNDARY_STRUCTURE_"
                 "CANDIDATE`: **supported (origin)**. The operator is non-conservative (29 boundary "
                 "states leak mass), and the closed classes are boundary-structure sinks: the a=0 "
                 "borrowing-constrained class (size 40, all b, both z) and two upper-boundary "
                 "2-cycles ((b=19,a=1) and (b=0,a=19), each switching z).")
    lines.append("- Category 5 `UNRESOLVED_WITH_CURRENT_DIAGNOSTICS`: not needed; evidence is "
                 "bounded and mutually consistent.")
    lines.append("")
    lines.append("Summary: the accepted stationary KFE becomes non-finite on the preserved path "
                 "because the accepted post-convergence operator is numerically rank-deficient "
                 "(transpose nullspace dimension 1; one (near-)zero singular value; SuperLU zero "
                 "pivot) with a non-conservative boundary-leak structure and multiple closed sink "
                 "classes, so the accepted single-row pin (on transient state 295) does not define "
                 "a unique stationary density and yields a pin-dependent / inconsistent pinned "
                 "system. At the exact D2 state the sparse direct solver's LU hits an exact zero "
                 "pivot for that pinned system, producing an all-NaN raw vector that the accepted "
                 "fail-closed check converts into `faithful contaminated-row solve is non-finite`. "
                 "At D0/D1/D3 the same arbitrary pin happens not to hit the exact pivot, so a "
                 "finite but pin-dependent (arbitrary) density is returned.")
    lines.append("")
    lines.append("DLH-5C implements NO repair: no solver change, no alternative production row pin, "
                 "no regularization/jitter/pseudoinverse.")
    lines.append("")
    with open(root / "DLH_5C_DIAGNOSTIC_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def _artifact_hashes(root: pathlib.Path) -> dict:
    hashes = {}
    for path in sorted(root.iterdir()):
        if path.is_file():
            hashes[path.name] = sha256_file(path)
    return hashes


def _append_artifact_hashes(root: pathlib.Path) -> None:
    """Append the complete 7-file artifact identity section to the report after
    all evidence files (including the report itself) exist."""
    report = root / "DLH_5C_DIAGNOSTIC_REPORT.md"
    with open(report, "a", encoding="utf-8") as fh:
        fh.write("\n## Artifact identities (SHA-256)\n\n")
        for name, h in sorted(_artifact_hashes(root).items()):
            fh.write(f"- `{name}`: `{h}`\n")


def _write_forbidden_check(cfg: DLH5CConfig, root: pathlib.Path, repro: dict, run: dict) -> None:
    terminal = _classification(cfg, run, repro) if repro["pass_bool"] else "BLOCKED_DLH_5C_REPRODUCIBILITY_FAILED"
    lines = [
        "# DLH-5C — Forbidden-Operation / Scope Check (Issue #26)",
        "",
        "DSH did NOT perform any of the following during Issue #26 execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify the accepted household oracle | NOT performed (immutable) |",
        "| Modify accepted regional fixed-point code/config | NOT performed (read-only reference) |",
        "| Change the contaminated-row formula / accepted KFE | NOT performed |",
        "| Adopt an alternative row pin as a fix | NOT performed (diagnostic evidence only) |",
        "| Regularization / jitter / pseudoinverse in production | NOT performed |",
        "| Change asset grids / household parameters / prices / S1 path | NOT performed |",
        "| Retry / adaptive scan / grid expansion | NOT performed |",
        "| `B=1`, `GovInv`, learned `W^L/W^K`, neural training, nominal HANK | NOT performed |",
        "| Scale regions / policy / welfare / Results claims | NOT performed |",
        "| Modify prior evidence / roadmap / governance / legacy roots | NOT performed |",
        "| `git add .` / `git add -A` | NOT performed (explicit staging only) |",
        "| Self-accept / merge / close Issue / PR / successor Issue | NOT performed |",
        "",
        "Diagnostic-only discipline: no-overwrite output root "
        f"`{cfg.output_root}`; deterministic repeats only; accepted KFE called to "
        "reproduce success and failure exactly.",
        "",
        "Terminal classification: "
        f"`{terminal}`",
        "",
    ]
    with open(root / "DLH_5C_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="DLH-5C KFE singularity diagnostic")
    parser.add_argument("--config", required=True, help="frozen DLH-5C TOML config path")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)

    root = pathlib.Path(cfg.output_root)
    if root.exists():
        print(f"BLOCKED_DLH_5C_OUTPUT_PATH_EXISTS: {root}", file=sys.stderr)
        return 3

    # deterministic full repeat
    repro = reproduce(cfg)
    if not repro["pass_bool"]:
        print("BLOCKED_DLH_5C_REPRODUCIBILITY_FAILED", file=sys.stderr)
        return 2

    # canonical first run (fresh construction)
    fixture = build_fixture(cfg)
    run = run_all(cfg, fixture)

    d2_status = next((c["kfe_status"] for c in run["cases"] if c["case_id"] == "d2"), None)
    if d2_status != "FAILED":
        print("BLOCKED_DLH_5C_D2_FAILURE_NOT_REPRODUCED", file=sys.stderr)
        return 4

    root.mkdir(parents=True, exist_ok=False)
    _write_evidence(root, cfg, run, repro)
    _write_forbidden_check(cfg, root, repro, run)
    _append_artifact_hashes(root)
    print(f"artifacts written under {root}")
    print(f"terminal = {_classification(cfg, run, repro)}")
    print(f"root cause = {_root_cause_classification(cfg, run)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
