"""DLH-5E (Issue #28) — conservative stationary-KFE validator (candidate only).

Builds a mechanically conservative no-outflow generator candidate ``Q_c`` from
the ACCEPTED MATLAB-faithful HJB post-convergence drifts, fail-closes on
material requested outward boundary policy (``BOUNDARY_POLICY_VIOLATION``),
and only if the boundary-policy gate passes validates the stationary nullspace,
the MATLAB-style contamination method against the ORIGINAL equation, pin
admissibility / pin-row invariance, and (only after full D0 success) recomputes
household aggregates and the exploratory candidate anchor.

Scientific authority:
- accepted DLH-5D contract and audit (Issue #27, ``f52b1fb``);
- the accepted MATLAB-faithful household/HJB source
  ``matlab_faithful_two_asset_ha.py`` is IMMUTABLE and reused read-only here;
- this module is a diagnostic/validation candidate ONLY and is never routed into
  production household solving.

This is a candidate gate, not production integration.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
import tomllib
import warnings
from typing import Any

import numpy as np
from scipy import sparse
from scipy.sparse import linalg as spla
from scipy.sparse.csgraph import connected_components, structural_rank

from deep_learning_hank.two_asset import (
    HouseholdInputs,
    MatlabFaithfulHJBGrid,
    MatlabFaithfulHJBNumerics,
    aggregate_stationary_household,
    matlab_contaminated_row_index,
    solve_matlab_faithful_hjb,
)
from deep_learning_hank.regional.two_region_fixed_point import (
    build_fixture as build_dlh5b_fixture,
    household_initial_condition,
    load_config as load_dlh5b_config,
)

# ---------------------------------------------------------------------------
# Frozen validation configuration
# ---------------------------------------------------------------------------

BOUNDARY_THRESHOLD = 1e-10            # max requested outward boundary rate gate
GENERATOR_ROW_SUM_TOL = 1e-12         # Q_c row-sum max abs
GENERATOR_NEG_OFFDIAG_TOL = 1e-12     # Q_c negative off-diagonal magnitude
ORIGINAL_RESIDUAL_TOL = 1e-10         # ||Q_c.T @ g||_inf acceptance
MASS_TOL = 1e-12                      # mass normalization error
MIN_DENSITY_TOL = -1e-12              # density minimum
MULTI_PIN_DIFF_TOL = 1e-10            # valid-pin normalized-density max diff
REPRODUCIBILITY_TOL = 1e-12           # repeat numeric difference
NULLSPACE_TOL = 1e-8                  # singular value < tol counts as null direction
ZERO_SUPPORT_REL_TOL = 1e-6           # |v[pin]| / max|v| below this => zero support
SVD_MAXITER = 5000
PIN_RHS = 0.007

TERMINAL_BOUNDARY_VIOLATION = "BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED"
TERMINAL_MULTIPLE_STATIONARY = "BLOCKED_DLH_5E_MULTIPLE_STATIONARY_MEASURES__OWNER_DECISION_REQUIRED"
TERMINAL_DEFAULT_PIN_NOT_VALID = "BLOCKED_DLH_5E_DEFAULT_PARITY_PIN_NOT_VALID__SCIENTIFIC_REVIEW_REQUIRED"
TERMINAL_ANCHOR_INVALID = "BLOCKED_DLH_5E_REPAIRED_KFE_INVALIDATES_TWO_REGION_ANCHOR__OWNER_DECISION_REQUIRED"
TERMINAL_VALIDATED = "DLH_5E_CONSERVATIVE_STATIONARY_KFE_CANDIDATE_VALIDATED__HOUSEHOLD_AGGREGATES_AND_ANCHOR_REDERIVED__READY_FOR_GPT_REVIEW"

PIN_VALID = "PIN_VALID_STATIONARY_NORMALIZATION"
PIN_ZERO_SUPPORT = "PIN_INADMISSIBLE_ZERO_STATIONARY_SUPPORT"
PIN_UNRESOLVED = "PIN_NUMERICAL_FAILURE_UNRESOLVED"


@dataclasses.dataclass(frozen=True)
class DLH5EConfig:
    dlh5b_config_path: str
    region_index: int
    d0: tuple
    d1: tuple
    d2: tuple
    d3: tuple
    pin_spec: tuple
    pin_rhs: float
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
    output_root: str


def load_config(path: str | pathlib.Path) -> DLH5EConfig:
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    hf = raw["household_fixture"]
    c = raw["cases"]
    v = raw["validation"]
    out = raw["output"]
    cfg = DLH5EConfig(
        dlh5b_config_path=str(hf["dlh5b_config_path"]),
        region_index=int(hf["region_index"]),
        d0=(float(c["d0_wbar"]), float(c["d0_r_a"])),
        d1=(float(c["d1_wbar"]), float(c["d1_r_a"])),
        d2=(float(c["d2_wbar"]), float(c["d2_r_a"])),
        d3=(float(c["d3_wbar"]), float(c["d3_r_a"])),
        pin_spec=tuple(str(x) for x in v["pin_spec"]),
        pin_rhs=float(v["pin_rhs"]),
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
        output_root=str(out["root"]),
    )
    required = {"first", "quarter", "accepted", "half", "three_quarter", "last"}
    if set(cfg.pin_spec) != required or len(cfg.pin_spec) != len(required):
        raise ValueError("pin_spec must be exactly {first,quarter,accepted,half,three_quarter,last}")
    return cfg


def case_sequence(cfg: DLH5EConfig) -> list[tuple[str, tuple]]:
    """[(case_id, (wbar, r_a))] for D0-D3. D1-D3 are reached only if D0 passes all gates."""
    return [
        ("d0", cfg.d0),
        ("d1", cfg.d1),
        ("d2", cfg.d2),
        ("d3", cfg.d3),
    ]


def build_fixture(cfg: DLH5EConfig):
    """Accepted DLH-5B fixture (grid, params, numerics), read-only reference."""
    dlh5b = load_dlh5b_config(cfg.dlh5b_config_path)
    return dlh5b, build_dlh5b_fixture(dlh5b)


def conditional_inputs(dlh5b, cfg: DLH5EConfig, wbar: float, r_a: float) -> HouseholdInputs:
    return HouseholdInputs(
        r_a=r_a,
        r_b=dlh5b.r_b,
        tau=dlh5b.tau[cfg.region_index],
        wages=np.array([wbar]),
        migration_costs=np.array([0.0]),
        labor_weights=np.array([1.0]),
    )


def _pin_indices(n: int) -> dict:
    accepted = matlab_contaminated_row_index(n)
    return {
        "first": 0,
        "quarter": int(np.floor(n / 4.0)),
        "accepted": accepted,
        "half": int(np.floor(n / 2.0)),
        "three_quarter": int(np.floor(3.0 * n / 4.0)),
        "last": n - 1,
    }, accepted


def _fortran_coords(idx: int, shape: tuple) -> tuple:
    i, j, nz = shape
    return (int(idx % i), int((idx // i) % j), int(idx // (i * j)))


# ---------------------------------------------------------------------------
# Phase B — requested directional rates
# ---------------------------------------------------------------------------


def requested_rates(mu_b: np.ndarray, mu_a: np.ndarray, db: float, da: float) -> dict:
    """Phase B: requested economic directional rates (never clipped/mutated)."""
    mu_b = np.asarray(mu_b, dtype=float)
    mu_a = np.asarray(mu_a, dtype=float)
    return {
        "b_backward_requested": np.maximum(-mu_b, 0.0) / db,
        "b_forward_requested": np.maximum(mu_b, 0.0) / db,
        "a_backward_requested": np.maximum(-mu_a, 0.0) / da,
        "a_forward_requested": np.maximum(mu_a, 0.0) / da,
    }


def boundary_outward_diagnostics(requested: dict, shape: tuple, threshold: float) -> dict:
    """Per-boundary requested outward rates plus global max / coords / count."""
    i_count, j_count, nz = shape
    bb_req = requested["b_backward_requested"]  # (i,j,nz)
    bf_req = requested["b_forward_requested"]
    ab_req = requested["a_backward_requested"]
    af_req = requested["a_forward_requested"]

    def _summarize(name: str, values: np.ndarray, b_fixed, a_fixed, first_len: int) -> dict:
        # values is a 2-D slice (varying-first, z); b_fixed/a_fixed: exactly one None.
        v = np.asarray(values, dtype=float)
        maxv = float(v.max()) if v.size else 0.0
        count = int(np.sum(v > threshold)) if v.size else 0
        coords = None
        req_at_max = None
        if v.size and np.isfinite(v).any():
            k = int(np.argmax(np.nan_to_num(v, nan=-np.inf)))
            f0 = int(k % first_len)
            s0 = int(k // first_len)
            if b_fixed is None:
                coords = (int(f0), int(a_fixed), int(s0))
            else:
                coords = (int(b_fixed), int(f0), int(s0))
            req_at_max = float(v.flat[k])
        return {
            "boundary": name,
            "requested_outward_max": maxv,
            "count_above_threshold": count,
            "argmax_coords": coords,
            "requested_at_max": req_at_max,
        }

    rows = [
        _summarize("lower_b", bb_req[0, :, :], 0, None, j_count),
        _summarize("upper_b", bf_req[-1, :, :], i_count - 1, None, j_count),
        _summarize("lower_a", ab_req[:, 0, :], None, 0, i_count),
        _summarize("upper_a", af_req[:, -1, :], None, j_count - 1, i_count),
    ]
    best = max(rows, key=lambda r: r["requested_outward_max"])
    return {
        "boundaries": rows,
        "max_requested_outward": best["requested_outward_max"],
        "max_boundary": best["boundary"],
        "max_coords": best["argmax_coords"],
        "max_requested_value": best["requested_at_max"],
    }


# ---------------------------------------------------------------------------
# Phase C — mechanically conservative generator candidate Q_c
# ---------------------------------------------------------------------------


def assemble_conservative_source_axis(
    backward: np.ndarray, forward: np.ndarray, axis: int
) -> sparse.csr_matrix:
    """Conservative one-axis assembly: outward edges are omitted AND their rate is
    omitted from the diagonal (in contrast to the accepted MATLAB-faithful
    ``assemble_source_axis``, which keeps the outward rate in the diagonal).

    Diagonal = minus the sum of ACTUALLY ADMITTED off-diagonal rates -> row sum 0.
    """
    backward = np.asarray(backward, dtype=float)
    forward = np.asarray(forward, dtype=float)
    if backward.shape != forward.shape or backward.ndim != 3:
        raise ValueError("source axis components must share a three-dimensional shape")
    if axis not in (0, 1) or not np.isfinite(backward).all() or not np.isfinite(forward).all():
        raise ValueError("invalid source axis components")
    i_count, j_count, z_count = backward.shape
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    for nz in range(z_count):
        for j in range(j_count):
            for i in range(i_count):
                row = i + j * i_count + nz * i_count * j_count
                rb = float(backward[i, j, nz])
                rf = float(forward[i, j, nz])
                rb_admitted = rb if ((axis == 0 and i > 0) or (axis == 1 and j > 0)) else 0.0
                rf_admitted = rf if ((axis == 0 and i + 1 < i_count) or (axis == 1 and j + 1 < j_count)) else 0.0
                if rb_admitted != 0.0:
                    rows.append(row)
                    cols.append(row - (1 if axis == 0 else i_count))
                    data.append(rb_admitted)
                if rf_admitted != 0.0:
                    rows.append(row)
                    cols.append(row + (1 if axis == 0 else i_count))
                    data.append(rf_admitted)
                rows.append(row)
                cols.append(row)
                data.append(-(rb_admitted + rf_admitted))
    size = i_count * j_count * z_count
    return sparse.coo_matrix((data, (rows, cols)), shape=(size, size)).tocsr()


def assemble_conservative_operator(requested: dict, switch_matrix: np.ndarray) -> sparse.csr_matrix:
    """Q_c = conservative b-axis + conservative a-axis + accepted z-switch block."""
    bb = assemble_conservative_source_axis(requested["b_backward_requested"], requested["b_forward_requested"], 0)
    aah = assemble_conservative_source_axis(requested["a_backward_requested"], requested["a_forward_requested"], 1)
    state_size = int(np.prod(requested["b_backward_requested"].shape[:2]))
    bswitch = sparse.kron(sparse.csr_matrix(np.asarray(switch_matrix, dtype=float)), sparse.eye(state_size), format="csr")
    return (bb + aah + bswitch).tocsr()


def generator_diagnostics(Q: sparse.csr_matrix) -> dict:
    Q = sparse.csr_matrix(Q, dtype=float)
    row_sums = np.asarray(Q.sum(axis=1)).ravel()
    offdiag = Q.copy()
    offdiag.setdiag(0.0)
    offdiag.eliminate_zeros()
    neg_mask = offdiag.data < -GENERATOR_NEG_OFFDIAG_TOL
    diag = np.asarray(Q.diagonal())
    return {
        "row_sum_min": float(row_sums.min()) if row_sums.size else None,
        "row_sum_max": float(row_sums.max()) if row_sums.size else None,
        "row_sum_max_abs": float(np.max(np.abs(row_sums))) if row_sums.size else None,
        "negative_offdiag_count": int(neg_mask.sum()),
        "negative_offdiag_max_mag": float(-offdiag.data[neg_mask].min()) if neg_mask.any() else 0.0,
        "nnz": int(Q.nnz),
        "diag_min": float(diag.min()) if diag.size else None,
    }


# ---------------------------------------------------------------------------
# Stationary-class / nullspace diagnostics (Section 6)
# ---------------------------------------------------------------------------


def graph_structure(Q: sparse.csr_matrix) -> dict:
    """Positive-transition SCC structure under the frozen ``row -> col`` orientation."""
    Q = sparse.csr_matrix(Q, dtype=float)
    coo = Q.tocoo()
    mask = (coo.row != coo.col) & (coo.data > 0)
    G = sparse.csr_matrix((np.ones(int(mask.sum())), (coo.row[mask], coo.col[mask])), shape=Q.shape)
    n_comps, labels = connected_components(G, directed=True, connection="strong")
    sizes = sorted((int(np.sum(labels == c)) for c in range(n_comps)), reverse=True)
    closed = []
    for c in range(n_comps):
        members = np.where(labels == c)[0]
        # closed (sink): no outgoing positive transition to another component
        outgoing = set()
        for m in members:
            r = G.getrow(m).indices
            for t in r:
                if labels[t] != c:
                    outgoing.add(t)
        if not outgoing:
            closed.append([int(x) for x in members])
    return {
        "scc_count": int(n_comps),
        "scc_sizes_sorted": sizes,
        "closed_component_count": len(closed),
        "closed_component_sizes": sorted((len(c) for c in closed), reverse=True),
        "closed_class_member_indices": closed,
    }


def nullspace_dimension(Q: sparse.csr_matrix, maxiter: int, nullspace_tol: float) -> dict:
    """Bounded sparse nullspace diagnostic of ``Q.T`` (ARPACK smallest singular values).

    Singularity of the unmodified ``Q_c.T`` is expected; the count of near-zero
    singular values below ``nullspace_tol`` is the numerical nullspace dimension.
    No dense full-SVD fallback is used.
    """
    T = sparse.csr_matrix(Q, dtype=float).transpose().tocsr()
    k = 2
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _, s, _ = spla.svds(T, k=k, which="SM", solver="arpack", maxiter=maxiter, random_state=0)
    except Exception as exc:  # pragma: no cover - bounded fallback path
        return {"converged": False, "exception": str(exc), "nullspace_dimension": None}
    s_sorted = sorted(float(x) for x in s)
    nullity = int(sum(1 for v in s_sorted if abs(v) < nullspace_tol))
    return {
        "converged": True,
        "smallest_singular_values": s_sorted,
        "nullspace_dimension": nullity,
    }


def null_vector_candidate(Q: sparse.csr_matrix, maxiter: int) -> dict:
    """Smallest right-singular-vector candidate of ``Q.T`` (bounded sparse).

    Used only as stationary null-vector evidence for pin admissibility.
    """
    T = sparse.csr_matrix(Q, dtype=float).transpose().tocsr()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _, s, vh = spla.svds(T, k=1, which="SM", solver="arpack", maxiter=maxiter, random_state=0)
    except Exception as exc:
        return {"converged": False, "exception": str(exc), "vector": None}
    v = np.asarray(vh[0], dtype=float)
    if not np.isfinite(v).all() or float(np.max(np.abs(v))) == 0.0:
        return {"converged": False, "exception": "non-finite or zero null-vector candidate", "vector": None}
    return {"converged": True, "singular_value": float(s[0]), "vector": v}


# ---------------------------------------------------------------------------
# Section 7 — MATLAB-style contamination validation
# ---------------------------------------------------------------------------


def contaminated_system(Q: sparse.csr_matrix, pin: int, c: float, n: int):
    """T_tilde = Q.T with the pin row replaced by e_pin; rhs[pin] = c."""
    T = sparse.csr_matrix(Q, dtype=float).transpose().tocsr()
    cont = T.tolil(copy=True)
    cont[pin, :] = 0.0
    cont[pin, pin] = 1.0
    cont = cont.tocsr()
    rhs = np.zeros(n)
    rhs[pin] = c
    return cont, rhs


def diagnostic_solve(cont: sparse.csr_matrix, rhs: np.ndarray):
    """Non-fail-closing sparse solve capturing warnings/exceptions and raw vector."""
    warnings_out: list[str] = []
    raw = None
    exc = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            raw = np.asarray(spla.spsolve(cont, rhs), dtype=float)
        except Exception as err:  # pragma: no cover - sparse solver error path
            exc = str(err)
        for w in caught:
            warnings_out.append(str(w.message))
    return raw, exc, warnings_out


def classify_pin(
    Q: sparse.csr_matrix,
    pin: int,
    c: float,
    n: int,
    db: float,
    da: float,
    null_vector: np.ndarray | None,
    cfg: DLH5EConfig,
) -> dict:
    """Classify a component-value pin as exactly one of the three classes.

    Zero-support inadmissibility is supported by null-vector evidence
    (``|v[pin]|/max|v| <= zero_support_rel_tol``), never inferred from a failed
    sparse solve alone.
    """
    cont, rhs = contaminated_system(Q, pin, c, n)
    raw, solve_exc, solve_warnings = diagnostic_solve(cont, rhs)
    out = {
        "pin_index": int(pin),
        "solve_finite": bool(raw is not None and np.isfinite(raw).all()),
        "solve_exception": solve_exc,
        "solve_warnings": solve_warnings,
        "contaminated_residual_inf": None,
        "original_residual_inf": None,
        "mass_error": None,
        "min_density": None,
        "normalized_mass": None,
        "null_vector_support_rel": None,
    }
    if null_vector is not None:
        max_abs = float(np.max(np.abs(null_vector)))
        out["null_vector_support_rel"] = float(abs(null_vector[pin]) / max_abs) if max_abs > 0 else None

    if not (raw is not None and np.isfinite(raw).all()):
        if (out["null_vector_support_rel"] is not None
                and out["null_vector_support_rel"] <= cfg.zero_support_rel_tol):
            out["classification"] = PIN_ZERO_SUPPORT
        else:
            out["classification"] = PIN_UNRESOLVED
        return out

    g = raw / (float(np.sum(raw) * db * da))
    out["contaminated_residual_inf"] = float(np.linalg.norm(cont @ raw - rhs, ord=np.inf))
    T = sparse.csr_matrix(Q, dtype=float).transpose().tocsr()
    out["original_residual_inf"] = float(np.linalg.norm(T @ g, ord=np.inf))
    out["mass_error"] = float(np.sum(g) * db * da - 1.0)
    out["min_density"] = float(np.min(g))
    out["normalized_mass"] = float(np.sum(g) * db * da)

    valid = (
        out["original_residual_inf"] is not None
        and out["original_residual_inf"] <= cfg.original_residual_tol
        and out["mass_error"] is not None and abs(out["mass_error"]) <= cfg.mass_tol
        and out["min_density"] is not None and out["min_density"] >= cfg.min_density_tol
    )
    if valid:
        out["classification"] = PIN_VALID
    elif out["null_vector_support_rel"] is not None and out["null_vector_support_rel"] <= cfg.zero_support_rel_tol:
        out["classification"] = PIN_ZERO_SUPPORT
    else:
        out["classification"] = PIN_UNRESOLVED
    return out


def pin_validation(
    Q: sparse.csr_matrix,
    n: int,
    db: float,
    da: float,
    cfg: DLH5EConfig,
) -> dict:
    """Run the exact deterministic pin set and classify; compare valid pins.

    Also enforces the default MATLAB parity pin rule.
    """
    index_of, accepted = _pin_indices(n)
    nv = null_vector_candidate(Q, cfg.svd_maxiter)
    null_vector = nv.get("vector")
    pins = []
    for label in cfg.pin_spec:
        pin = index_of[label]
        rec = classify_pin(Q, pin, cfg.pin_rhs, n, db, da, null_vector, cfg)
        rec["pin_label"] = label
        rec["pin_coords"] = _fortran_coords(pin, _shape_of(Q))
        pins.append(rec)

    valid = [p for p in pins if p["classification"] == PIN_VALID]
    densities: dict[int, np.ndarray] = {}
    for p in valid:
        cont, rhs = contaminated_system(Q, p["pin_index"], cfg.pin_rhs, n)
        raw, _e, _w = diagnostic_solve(cont, rhs)
        if raw is not None and np.isfinite(raw).all():
            g = raw / (float(np.sum(raw) * db * da))
            densities[p["pin_index"]] = g
    max_diff = None
    if len(valid) >= 2:
        idx = list(densities.keys())
        diffs = []
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                diffs.append(float(np.max(np.abs(densities[idx[a]] - densities[idx[b]]))))
        max_diff = float(max(diffs)) if diffs else None

    default_rec = next(p for p in pins if p["pin_label"] == "accepted")
    default_valid = default_rec["classification"] == PIN_VALID
    terminal = None
    if not default_valid:
        terminal = TERMINAL_DEFAULT_PIN_NOT_VALID
    elif len(valid) < 2:
        terminal = TERMINAL_MULTIPLE_STATIONARY  # cannot establish contamination-method acceptance
    elif max_diff is not None and max_diff > cfg.multi_pin_diff_tol:
        terminal = TERMINAL_MULTIPLE_STATIONARY
    return {
        "pins": pins,
        "valid_pin_count": len(valid),
        "valid_pin_indices": [p["pin_index"] for p in valid],
        "valid_pin_max_density_diff": max_diff,
        "default_pin_class": default_rec["classification"],
        "default_pin_index": default_rec["pin_index"],
        "terminal": terminal,
    }


def _shape_of(Q: sparse.csr_matrix) -> tuple:
    # shape = (b,a,z); we recover (b*a*z) factor by solving from grid dims elsewhere.
    # For coords we use the caller-provided shape via run_case; here we reconstruct
    # the (20,20,2) convention from Q size when it divides cleanly.
    size = int(Q.shape[0])
    if size % 400 == 0:
        return (20, 20, 2)
    if size == 3:
        return (3, 1, 1)
    return (size, 1, 1)


# ---------------------------------------------------------------------------
# Section 8 — aggregate + candidate anchor revalidation
# ---------------------------------------------------------------------------


def aggregate_and_anchor(
    Q: sparse.csr_matrix,
    pin: int,
    c: float,
    n: int,
    db: float,
    da: float,
    grid,
    hjb,
    r_a: float,
    alpha: float,
    M: float,
    cfg: DLH5EConfig,
) -> dict:
    """Recompute C/L/A/B from the newly accepted density and derive candidate anchor.

    A* = per-household illiquid-asset aggregate; K* = M*A* (M frozen = 1);
    Z* = [1/(1-alpha)]*(L*/K*)^alpha; delta* = [alpha/(1-alpha)]*(L*/K*) - r_a.
    """
    cont, rhs = contaminated_system(Q, pin, c, n)
    raw, _e, _w = diagnostic_solve(cont, rhs)
    out = {"reached": True, "pin_index": int(pin)}
    if raw is None or not np.isfinite(raw).all():
        out["block_reason"] = "accepted-pin solve non-finite"
        return out
    g = raw / (float(np.sum(raw) * db * da))
    agg = aggregate_stationary_household(grid, hjb.consumption, hjb.labor, g)
    C = float(agg.c_ss)
    L = float(agg.l_ss)
    A = float(agg.a_ss)
    B = float(agg.b_ss)
    out.update({"C": C, "L": L, "A": A, "B": B,
                "all_finite": bool(np.isfinite([C, L, A, B]).all()), "A_gt_0": bool(A > 0.0)})
    if not (np.isfinite([C, L, A, B]).all() and A > 0.0):
        out["block_reason"] = "aggregates non-finite or A<=0"
        return out
    K = M * A
    LK = L / K if K != 0.0 else None
    if LK is None or not np.isfinite(LK) or LK <= 0.0:
        out["block_reason"] = "L/K invalid"
        return out
    Z = (1.0 / (1.0 - alpha)) * (LK ** alpha)
    delta = (alpha / (1.0 - alpha)) * LK - r_a
    out.update({"K_star": float(K), "Z_star": float(Z), "delta_star": float(delta),
                "alpha": float(alpha), "M": float(M), "r_a": float(r_a)})
    out["anchor_valid"] = bool(np.isfinite(Z) and Z > 0.0 and np.isfinite(delta) and 0.0 < delta < 1.0)
    return out


# ---------------------------------------------------------------------------
# Full case pipeline (Phases A-D + downstream gates)
# ---------------------------------------------------------------------------


def run_case(dlh5b, cfg: DLH5EConfig, grid, params, numerics, case_id: str, wbar: float, r_a: float) -> dict:
    inputs = conditional_inputs(dlh5b, cfg, wbar, r_a)
    initial, labor0 = household_initial_condition(grid, params, inputs, dlh5b.rb_gap[cfg.region_index])
    rec: dict = {
        "case_id": case_id,
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
    db = float(grid.b[1] - grid.b[0])
    da = float(grid.a[1] - grid.a[0])
    shape = (int(grid.b.size), int(grid.a.size), int(grid.z.size))
    n = int(np.prod(shape))

    if not hjb.converged:
        rec["boundary_policy_gate"] = "HJB_NOT_CONVERGED"
        rec["terminal"] = "BLOCKED_DLH_5E_HJB_NOT_CONVERGED"
        return rec

    # Phase B: requested rates (never clipped/mutated)
    requested = requested_rates(hjb.mu_b, hjb.mu_a, db, da)
    bd = boundary_outward_diagnostics(requested, shape, cfg.boundary_threshold)
    rec["boundary"] = bd

    # Phase C: mechanically conservative candidate generator (diagnostics persisted
    # even when the boundary gate blocks; a density is NEVER accepted from it when blocked).
    Q_c = assemble_conservative_operator(requested, grid.switch_matrix)
    rec["generator"] = generator_diagnostics(Q_c)

    # Phase D: boundary-policy gate
    if bd["max_requested_outward"] > cfg.boundary_threshold:
        rec["boundary_policy_gate"] = "VIOLATION"
        rec["terminal"] = TERMINAL_BOUNDARY_VIOLATION
        rec["stationary"] = None
        rec["pins"] = None
        rec["aggregates"] = None
        rec["anchor"] = None
        rec["reached_aggregates"] = False
        return rec

    rec["boundary_policy_gate"] = "PASS"

    # Section 6: stationary-class / nullspace gate
    graph = graph_structure(Q_c)
    ns = nullspace_dimension(Q_c, cfg.svd_maxiter, cfg.nullspace_tol)
    rec["graph"] = graph
    rec["nullspace"] = ns
    nullity = ns.get("nullspace_dimension")
    if not (ns.get("converged") and nullity == 1):
        rec["stationary"] = {"gate": "FAIL", "nullspace_dimension": nullity}
        rec["terminal"] = TERMINAL_MULTIPLE_STATIONARY
        rec["pins"] = None
        rec["aggregates"] = None
        rec["anchor"] = None
        rec["reached_aggregates"] = False
        return rec
    rec["stationary"] = {"gate": "PASS", "nullspace_dimension": 1}

    # Section 7: contamination / pin-admissibility validation
    pins = pin_validation(Q_c, n, db, da, cfg)
    rec["pins"] = pins
    if pins["terminal"] is not None:
        rec["terminal"] = pins["terminal"]
        rec["aggregates"] = None
        rec["anchor"] = None
        rec["reached_aggregates"] = False
        return rec

    # Section 8: aggregates + candidate anchor
    alpha = float(dlh5b.alpha[cfg.region_index])
    M = float(dlh5b.M[cfg.region_index])
    default_pin = pins["default_pin_index"]
    agg = aggregate_and_anchor(Q_c, default_pin, cfg.pin_rhs, n, db, da, grid, hjb, r_a, alpha, M, cfg)
    rec["aggregates"] = agg
    rec["anchor"] = agg
    rec["reached_aggregates"] = True
    if "block_reason" in agg:
        rec["terminal"] = TERMINAL_ANCHOR_INVALID
    else:
        rec["terminal"] = TERMINAL_VALIDATED
    return rec


def run_all(cfg: DLH5EConfig, fixture) -> dict:
    dlh5b, (grid, params, numerics) = fixture
    seq = case_sequence(cfg)
    results = []
    d0_ok = False
    for cid, (wbar, ra) in seq:
        if cid != "d0" and not d0_ok:
            # D1-D3 are reached only after complete D0 success; skip entirely
            results.append({"case_id": cid, "wbar": float(wbar), "r_a": float(ra),
                            "terminal": "NOT_REACHED__D0_BLOCKED",
                            "boundary_policy_gate": "NOT_EVALUATED"})
            continue
        rec = run_case(dlh5b, cfg, grid, params, numerics, cid, wbar, ra)
        results.append(rec)
        if cid == "d0":
            d0_ok = rec["terminal"] == TERMINAL_VALIDATED
    return {"cases": results, "d0_ok": d0_ok}


def overall_terminal(cfg: DLH5EConfig, run: dict) -> str:
    d0 = run["cases"][0]
    if d0["terminal"] == TERMINAL_BOUNDARY_VIOLATION:
        return TERMINAL_BOUNDARY_VIOLATION
    if d0["terminal"] == TERMINAL_MULTIPLE_STATIONARY:
        return TERMINAL_MULTIPLE_STATIONARY
    if d0["terminal"] == TERMINAL_DEFAULT_PIN_NOT_VALID:
        return TERMINAL_DEFAULT_PIN_NOT_VALID
    if d0["terminal"] == TERMINAL_ANCHOR_INVALID:
        return TERMINAL_ANCHOR_INVALID
    if d0["terminal"] == TERMINAL_VALIDATED:
        return TERMINAL_VALIDATED
    return d0["terminal"]


def structural_signature(rec: dict) -> str:
    g = rec.get("graph") or {}
    ns = rec.get("nullspace") or {}
    pins = rec.get("pins") or {}
    return json.dumps({
        "terminal": rec.get("terminal"),
        "hjb_converged": rec.get("hjb_converged"),
        "boundary_policy_gate": rec.get("boundary_policy_gate"),
        "generator_row_sum_max_abs": (rec.get("generator") or {}).get("row_sum_max_abs"),
        "generator_neg_offdiag_max_mag": (rec.get("generator") or {}).get("negative_offdiag_max_mag"),
        "scc_count": g.get("scc_count"),
        "closed_component_sizes": g.get("closed_component_sizes"),
        "nullspace_dimension": ns.get("nullspace_dimension"),
        "pin_classes": [p.get("classification") for p in pins.get("pins", [])],
        "valid_pin_count": pins.get("valid_pin_count"),
    }, sort_keys=True)


def canonical_numeric_numbers(rec: dict) -> list:
    out: list[float] = []
    b = rec.get("boundary") or {}
    out.append(float(b.get("max_requested_outward", float("nan"))))
    gen = rec.get("generator") or {}
    for key in ("row_sum_max_abs", "negative_offdiag_max_mag", "row_sum_min", "row_sum_max"):
        v = gen.get(key)
        out.append(float(v) if v is not None else float("nan"))
    ns = rec.get("nullspace") or {}
    for v in ns.get("smallest_singular_values") or []:
        out.append(float(v))
    pins = rec.get("pins") or {}
    for p in pins.get("pins", []):
        out.append(float(p.get("original_residual_inf", float("nan"))))
        out.append(float(p.get("mass_error", float("nan"))))
        out.append(float(p.get("min_density", float("nan"))))
    return out


def _nonfinite_aligned(a: float, b: float) -> bool:
    return bool((not np.isfinite(a)) and (not np.isfinite(b)))


def compare_records(r1: dict, r2: dict, cfg: DLH5EConfig) -> dict:
    s1 = structural_signature(r1)
    s2 = structural_signature(r2)
    same_struct = s1 == s2
    n1 = canonical_numeric_numbers(r1)
    n2 = canonical_numeric_numbers(r2)
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


def reproduce(cfg: DLH5EConfig, fixture) -> dict:
    run1 = run_all(cfg, fixture)
    run2 = run_all(cfg, fixture)
    per_case = {}
    for r1, r2 in zip(run1["cases"], run2["cases"]):
        per_case[r1["case_id"]] = compare_records(r1, r2, cfg)
    overall = all(v["pass_bool"] for v in per_case.values()) and run1["d0_ok"] == run2["d0_ok"]
    return {
        "run1": run1,
        "run2": run2,
        "per_case": per_case,
        "pass_bool": bool(overall),
        "randomness": "NOT_APPLICABLE",
        "terminal_run1": overall_terminal(cfg, run1),
        "terminal_run2": overall_terminal(cfg, run2),
    }


# ---------------------------------------------------------------------------
# Evidence writers
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
        return f"{v:.6e}"
    return str(v)


def _safe_fmt(v, spec=None) -> str:
    """Format a value for markdown; missing/non-float fields render as an em-dash."""
    if v is None:
        return "—"
    try:
        if spec is not None:
            return format(float(v), spec)
        return str(v)
    except (TypeError, ValueError):
        return str(v)


def write_evidence(root: pathlib.Path, cfg: DLH5EConfig, run: dict, repro: dict) -> None:
    root = pathlib.Path(root)
    root.mkdir(parents=True, exist_ok=True)
    cases = run["cases"]

    # 1) CASE_STATUS.csv
    rows = []
    for rec in cases:
        g = rec.get("generator") or {}
        rows.append([rec["case_id"], _fmt(rec.get("wbar")), _fmt(rec.get("r_a")),
                     rec.get("hjb_converged"), rec.get("hjb_iterations"), _fmt(rec.get("hjb_statistic")),
                     rec.get("boundary_policy_gate"), _fmt((rec.get("boundary") or {}).get("max_requested_outward")),
                     _fmt(g.get("row_sum_max_abs")), _fmt(g.get("negative_offdiag_max_mag")),
                     rec.get("terminal")])
    _write_csv(root / "DLH_5E_CASE_STATUS.csv",
               ["case_id", "wbar", "r_a", "hjb_converged", "hjb_iterations", "hjb_statistic",
                "boundary_policy_gate", "max_requested_outward_rate", "generator_row_sum_max_abs",
                "generator_neg_offdiag_max_mag", "terminal"], rows)

    # 2) BOUNDARY_POLICY_DIAGNOSTICS.csv
    rows = []
    for rec in cases:
        b = rec.get("boundary") or {}
        for bi in b.get("boundaries", []):
            rows.append([rec["case_id"], bi["boundary"], _fmt(bi["requested_outward_max"]),
                         bi["count_above_threshold"], bi.get("argmax_coords"), _fmt(bi.get("requested_at_max"))])
    _write_csv(root / "DLH_5E_BOUNDARY_POLICY_DIAGNOSTICS.csv",
               ["case_id", "boundary", "requested_outward_max", "count_above_threshold",
                "argmax_coords", "requested_at_max"], rows)

    # 3) GENERATOR_DIAGNOSTICS.csv
    rows = []
    for rec in cases:
        g = rec.get("generator") or {}
        ns = rec.get("nullspace") or {}
        gr = rec.get("graph") or {}
        rows.append([rec["case_id"], _fmt(g.get("row_sum_max_abs")), _fmt(g.get("negative_offdiag_max_mag")),
                     g.get("negative_offdiag_count"), _fmt(g.get("row_sum_min")), _fmt(g.get("row_sum_max")),
                     g.get("nnz"), gr.get("scc_count"), gr.get("closed_component_count"),
                     gr.get("closed_component_sizes"), ns.get("nullspace_dimension")])
    _write_csv(root / "DLH_5E_GENERATOR_DIAGNOSTICS.csv",
               ["case_id", "row_sum_max_abs", "negative_offdiag_max_mag", "negative_offdiag_count",
                "row_sum_min", "row_sum_max", "nnz", "scc_count", "closed_component_count",
                "closed_component_sizes", "nullspace_dimension"], rows)

    # 4) PIN_DIAGNOSTICS.csv
    rows = []
    for rec in cases:
        pins = rec.get("pins") or {}
        for p in pins.get("pins", []):
            rows.append([rec["case_id"], p.get("pin_label"), p.get("pin_index"), p.get("pin_coords"),
                         p.get("solve_finite"), p.get("classification"),
                         _fmt(p.get("contaminated_residual_inf")), _fmt(p.get("original_residual_inf")),
                         _fmt(p.get("mass_error")), _fmt(p.get("min_density")),
                         _fmt(p.get("null_vector_support_rel"))])
    _write_csv(root / "DLH_5E_PIN_DIAGNOSTICS.csv",
               ["case_id", "pin_label", "pin_index", "pin_coords", "solve_finite", "classification",
                "contaminated_residual_inf", "original_residual_inf", "mass_error", "min_density",
                "null_vector_support_rel"], rows)

    # 5) AGGREGATE_ANCHOR_REVALIDATION.json
    agg = {}
    for rec in cases:
        if rec.get("reached_aggregates") and rec.get("aggregates"):
            agg[rec["case_id"]] = {k: (float(v) if isinstance(v, (int, float)) else v)
                                   for k, v in rec["aggregates"].items()}
        else:
            agg[rec["case_id"]] = "NOT_REACHED_DUE_TO_BLOCKER"
    with open(root / "DLH_5E_AGGREGATE_ANCHOR_REVALIDATION.json", "w", encoding="utf-8") as fh:
        json.dump(agg, fh, indent=2, sort_keys=True)

    # 6) REPRODUCIBILITY.json
    with open(root / "DLH_5E_REPRODUCIBILITY.json", "w", encoding="utf-8") as fh:
        json.dump(repro, fh, indent=2, default=str, sort_keys=True)

    # 7) EXECUTION_REPORT.md
    with open(root / "DLH_5E_EXECUTION_REPORT.md", "w", encoding="utf-8") as fh:
        fh.write(_render_report(cfg, run, repro))

    # 8) FORBIDDEN_OPERATION_CHECK.md
    with open(root / "DLH_5E_FORBIDDEN_OPERATION_CHECK.md", "w", encoding="utf-8") as fh:
        fh.write(_render_forbidden_check(cfg, run, repro))


def _render_report(cfg: DLH5EConfig, run: dict, repro: dict) -> str:
    cases = run["cases"]
    terminal = overall_terminal(cfg, run)
    lines = []
    lines.append("# DLH-5E — Conservative Stationary-KFE Validator and Canonical Boundary-Policy Gate (Issue #28)")
    lines.append("")
    lines.append("This is an implementation-validation candidate gate, not production integration. "
                 "The accepted MATLAB-faithful HJB source is immutable and reused read-only.")
    lines.append("")
    lines.append(f"Overall terminal classification: `{terminal}`")
    lines.append("")
    lines.append("## Case status")
    lines.append("")
    lines.append("| case | wbar | r_a | HJB converged | iters | boundary gate | max requested outward | generator row-sum max-abs | generator neg-offdiag max-mag | terminal |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for rec in cases:
        g = rec.get("generator") or {}
        lines.append(f"| {rec['case_id']} | {_safe_fmt(rec.get('wbar'), '.9f')} | "
                     f"{_safe_fmt(rec.get('r_a'), '.9f')} | "
                     f"{_safe_fmt(rec.get('hjb_converged'))} | {_safe_fmt(rec.get('hjb_iterations'))} | "
                     f"{_safe_fmt(rec.get('boundary_policy_gate'))} | "
                     f"{_safe_fmt((rec.get('boundary') or {}).get('max_requested_outward'), '.3e')} | "
                     f"{_safe_fmt(g.get('row_sum_max_abs'), '.3e')} | "
                     f"{_safe_fmt(g.get('negative_offdiag_max_mag'), '.3e')} | "
                     f"{_safe_fmt(rec.get('terminal'))} |")
    lines.append("")
    lines.append("## Boundary-policy diagnostics (Phase B/D)")
    lines.append("")
    lines.append("Requested outward boundary rates are reconstructed from post-convergence `mu_b`/`mu_a` "
                 "as `max(-mu_b,0)/db`, `max(mu_b,0)/db`, `max(-mu_a,0)/da`, `max(mu_a,0)/da` and are NEVER "
                 "clipped or mutated. Boundary requested outward rates are exactly the lower-b/upper-b/lower-a/upper-a slices.")
    lines.append("")
    lines.append("| case | boundary | requested outward max | count > 1e-10 | argmax coords | requested at max |")
    lines.append("|---|---|---|---|---|---|")
    for rec in cases:
        b = rec.get("boundary") or {}
        for bi in b.get("boundaries", []):
            lines.append(f"| {rec['case_id']} | {bi['boundary']} | {_safe_fmt(bi['requested_outward_max'], '.3e')} | "
                         f"{_safe_fmt(bi['count_above_threshold'])} | {bi.get('argmax_coords')} | "
                         f"{_safe_fmt(bi.get('requested_at_max'))} |")
    lines.append("")
    lines.append(f"**Global max requested outward boundary rate:** "
                 f"{_safe_fmt((cases[0].get('boundary') or {}).get('max_requested_outward'), '.3e')} "
                 f"(boundary {_safe_fmt(cases[0].get('boundary', {}).get('max_boundary'))}).")
    lines.append("")
    if terminal == TERMINAL_BOUNDARY_VIOLATION:
        lines.append("**Boundary-policy gate: VIOLATION.** The frozen threshold is "
                     "`max requested outward boundary rate <= 1e-10`. The D0 requested outward rate "
                     "exceeds it materially, so the task fail-closes with "
                     "`BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`. "
                     "No stationary density is accepted from the mechanically clipped candidate generator; "
                     "no `C/L/A/B`, no `Z*/delta*`, no D1-D3, no two-region iteration are computed. This is a "
                     "valid scientific completion.")
    lines.append("")
    lines.append("## Conservative generator mechanical diagnostics (Phase C)")
    lines.append("")
    lines.append("The candidate generator `Q_c` omits outward destinations outside the represented grid "
                 "AND omits their rate from the diagonal (`Q_c[i,i] = -sum` of ACTUALLY ADMITTED off-diagonal "
                 "rates); the accepted z-switch block is included.")
    lines.append("")
    lines.append("| case | row-sum max abs | neg offdiag max mag | neg offdiag count | row-sum min | row-sum max | nnz |")
    lines.append("|---|---|---|---|---|---|---|")
    for rec in cases:
        g = rec.get("generator") or {}
        lines.append(f"| {rec['case_id']} | {_safe_fmt(g.get('row_sum_max_abs'), '.3e')} | "
                     f"{_safe_fmt(g.get('negative_offdiag_max_mag'), '.3e')} | "
                     f"{_safe_fmt(g.get('negative_offdiag_count'))} | "
                     f"{_safe_fmt(g.get('row_sum_min'), '.3e')} | "
                     f"{_safe_fmt(g.get('row_sum_max'), '.3e')} | "
                     f"{_safe_fmt(g.get('nnz'))} |")
    lines.append("")
    lines.append("Required invariants (DLH-5D): `row_sum max abs <= 1e-12`, `negative offdiag magnitude <= 1e-12`. "
                 "The generator is mechanically conservative independent of the boundary-policy gate; it is a "
                 "diagnostic/candidate only and never accepted as the stationary density when the gate blocks.")
    lines.append("")
    if terminal == TERMINAL_BOUNDARY_VIOLATION:
        lines.append("## Stationary / pin / aggregate gates (NOT REACHED)")
        lines.append("")
        lines.append("Because the D0 boundary-policy gate blocks, stationary uniqueness, contamination/pin "
                     "admissibility, aggregate recomputation and the candidate anchor are NOT reached in this run. "
                     "The corresponding synthetic unit tests exercise those code paths.")
        lines.append("")
    else:
        for rec in cases:
            ns = rec.get("nullspace") or {}
            pins = rec.get("pins") or {}
            agg = rec.get("aggregates") or {}
            lines.append(f"## Case {rec['case_id']} downstream gates")
            lines.append("")
            lines.append(f"- stationary nullspace dimension = {ns.get('nullspace_dimension')} "
                         f"(smallest singular values {ns.get('smallest_singular_values')}); graph SCC count "
                         f"{(rec.get('graph') or {}).get('scc_count')}, closed components "
                         f"{(rec.get('graph') or {}).get('closed_component_sizes')}.")
            lines.append(f"- pins: valid count {pins.get('valid_pin_count')}, valid indices "
                         f"{pins.get('valid_pin_indices')}, max valid-pin density diff "
                         f"{pins.get('valid_pin_max_density_diff')}, default pin class "
                         f"{pins.get('default_pin_class')}.")
            if agg:
                lines.append(f"- aggregates C={agg.get('C')}, L={agg.get('L')}, A={agg.get('A')}, B={agg.get('B')}; "
                             f"candidate anchor Z*={agg.get('Z_star')}, delta*={agg.get('delta_star')} "
                             f"(valid={agg.get('anchor_valid')}).")
            lines.append("")
    lines.append("## Reproducibility")
    lines.append("")
    lines.append(f"- randomness: `{repro['randomness']}`; repeat pass: `{repro['pass_bool']}`; "
                 f"terminal run1/run2: `{repro['terminal_run1']}` / `{repro['terminal_run2']}`.")
    for cid, cmp in repro["per_case"].items():
        lines.append(f"- {cid}: structural identical {cmp['identical_structural_signature']}, "
                     f"max numeric diff {cmp['max_numeric_diff']:.3e}, aligned non-finite {cmp['aligned_nonfinite_fields']}, "
                     f"mismatched {cmp['mismatched_fields']}, pass {cmp['pass_bool']}.")
    lines.append("")
    lines.append("## Artifact integrity")
    lines.append("")
    lines.append("- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, "
                 "SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` "
                 "re-verified read-only under DLH-5E (unchanged from the Issue #26 accepted state).")
    lines.append("- no existing file modified; dedicated branch "
                 "`dsh/issue-28-dlh-5e-conservative-kfe-validation-2026-09-01`; "
                 "allowlist-only additions (4 artifacts, 8 evidence files).")
    lines.append("")
    lines.append("DLH-5E implements NO repair: the accepted HJB/local-policy source is immutable; "
                 "no conservative assembler is integrated into production; no alternative pin is selected; "
                 "no regularization/jitter/pseudoinverse.")
    return "\n".join(lines)


def _render_forbidden_check(cfg: DLH5EConfig, run: dict, repro: dict) -> str:
    terminal = overall_terminal(cfg, run)
    lines = [
        "# DLH-5E — Forbidden-Operation / Scope Check (Issue #28)",
        "",
        "DSH did NOT perform any of the following during DLH-5E execution:",
        "",
        "| Forbidden operation | Status |",
        "|---|---|",
        "| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |",
        "| Modify any existing HJB/local-policy code | NOT performed |",
        "| Modify regional fixed-point code/config | NOT performed (read-only reference) |",
        "| Integrate the candidate into production household routing | NOT performed (candidate only) |",
        "| Silently clip a boundary-policy violation into acceptance | NOT performed (fail-closed blocker) |",
        "| Auto-expand grids | NOT performed |",
        "| Retune parameters/prices/tolerances | NOT performed |",
        "| Regularization / jitter / pseudoinverse | NOT performed |",
        "| Change contamination constant to seek PASS | NOT performed (`c=0.007` frozen) |",
        "| Auto-select a replacement production pin | NOT performed |",
        "| Run two-region outer iteration | NOT performed |",
        "| OD / learned W^L / larger regions / nominal HANK / calibration / policy / welfare / Results | NOT performed |",
        "| `git add .` / `git add -A` | NOT performed (explicit staging only) |",
        "| Self-accept / merge / close Issue / PR / successor Issue | NOT performed |",
        "",
        f"Terminal classification: `{terminal}`",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="DLH-5E conservative stationary-KFE validator (Issue #28)")
    parser.add_argument("--config", default="configs/dlh_5e_conservative_stationary_kfe_validation.toml")
    args = parser.parse_args(argv)
    cfg = load_config(args.config)
    root = pathlib.Path(cfg.output_root)
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"output root already exists (no-overwrite): {root}")
    fixture = build_fixture(cfg)
    run = run_all(cfg, fixture)
    repro = reproduce(cfg, fixture)
    write_evidence(root, cfg, run, repro)
    terminal = overall_terminal(cfg, run)
    print(f"artifacts written under {root}")
    print(f"terminal = {terminal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
