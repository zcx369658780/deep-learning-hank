"""DLH-5V-P — FTB stagnation residual decomposition + frozen-policy Newton
boundary geometry diagnostic.

Issue #64 / DLH-5V-P
``SCIENTIFIC_NUMERICAL_DIAGNOSTIC__FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY``

Authority: Issue #64 OPEN; initial activation ``5652648524``; final
authoritative activation-refresh ``5652783829`` (post-sync live ``main``
``7e82d606874d7b2347ba331678456b46529538c9``). Route decision
``APPROVE_FTB_STAGNATION_RESIDUAL_DECOMPOSITION_AND_FROZEN_POLICY_NEWTON_GEOMETRY_AFTER_5VO_TERMINAL_B``;
authority marker ``DLH_5VP_STAGNATION_NEWTON_GEOMETRY_DIAGNOSTIC_AUTHORIZED``.

Scientific object (binding, Issue #64 sections 3-8), in exactly this order:

1. deterministic reconstruction of the accepted Issue #63 stagnation state:
   replay the accepted continuous fraction-to-boundary trajectory and STOP
   immediately after accepted FTB step 8, before any new HJB iterate is
   accepted; preserve the pre-step-8 F0 policy records (the final=False build
   at the iterate before step 8) required to reproduce the accepted Issue #63
   final-validation semantics exactly;
2. iteration-vs-final residual / operator decomposition at ``V_*``:
   ``R_iter = rho*V_* - [u_iter + Q_iter V_*]`` with ``Q_iter,u_iter`` built
   EXACTLY ONCE from ``V_*`` with accepted ``final=False`` semantics, and
   ``R_final = rho*V_* - [u_final + Q_final V_*]`` with accepted Issue #63
   final-validation semantics (``final=True`` with the preserved pre-step-8 F0
   records) — must reproduce the accepted ``~490.756`` final validation
   residual;
3. F0-vs-boundary residual decomposition (total / F0-only / boundary-only inf
   norms and argmax state/family/z for ``R_iter``, ``R_final`` and
   ``R_final - R_iter``);
4. exactly ONE frozen-policy Newton direction: ``J_iter d_N = -R_iter`` with
   ``J_iter = rho I - Q_iter`` (exact Newton step for the frozen linear
   policy/operator, NOT a nonlinear Newton theorem); verify the linear
   residual ``||J_iter d_N + R_iter||_inf``;
5. ONE boundary-crossing calculation with the accepted Issue #62 derivative
   semantics: regular backward finite-difference boundary states use the
   linear difference of ``d_N``; ``i==0`` V-independent ``p_b`` states have
   directional derivative exactly 0; ``alpha_cross_i =
   (p_b(V_*) - PB_MARGIN)/(-dp_b(d_N))`` over required states with
   ``dp_b(d_N) < 0``; ``alpha_cross = min`` positive finite
   ``alpha_cross_i``;
6. exactly TWO diagnostic trial fractions ``alpha_half`` and ``alpha_near``
   (frozen: ``PB_MARGIN=1e-12``, ``EPS_ALPHA=1e-6``, ``HALF_ALPHA=0.5``,
   ``MATERIAL_REDUCTION_RATIO=0.50``; ``alpha_near = min(1,
   (1-EPS_ALPHA)*alpha_cross)`` if a finite positive crossing exists,
   otherwise ``1``; ``alpha_half = 0.5*alpha_near``; NO line search, NO alpha
   tuning); for each: form ``V_trial = V_* + alpha*d_N``, directly verify all
   required boundary ``p_b`` finite and ``> PB_MARGIN``, verify the frozen
   residual relation ``R_iter(V_trial; frozen) = (1-alpha) R_iter(V_*)``,
   perform exactly ONE ``final=False`` nonlinear policy re-selection
   (``R_reselect``), compute the accepted final-validation-style residual at
   the same trial with the TRIAL re-selected records as the F0 policy input
   (``R_final_trial``), and record residual ratios and policy/sector switching;
7. ONE deterministic repeat of the full diagnostic.

Trial states are diagnostic only — NEVER accepted as new HJB iterates. No
multi-step Newton / policy-iteration / semismooth / trust-region solver, no
adaptive line search, no alpha / material-threshold tuning, no
economics/prices/grid/domain/``PB_MARGIN`` change, no Issue #63 controller
change, no clip/floor of ``p_b``. The household oracle, selected-Q source and
the accepted Issue #61 / #62 / #63 implementations are imported read-only and
never modified. No KFE / stationary KFE / steady state.

FAIL-CLOSED: any non-finite required boundary p_b, non-finite directional
evidence, or failed Newton solve raises ``NewtonGeometryFailure`` (surfaced
explicitly, never misread as feasible). Non-identical deterministic repeat is
treated as internally inconsistent evidence.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from scipy import sparse
from scipy.sparse import linalg

from deep_learning_hank.two_asset.boundary_hjb_selected_q import (
    BoundaryHJBFailure,
    BoundaryHJBSolver,
)
from deep_learning_hank.two_asset.adaptive_resolvent_hjb import (
    CENTRAL_CONFIG,
    PB_MARGIN,
    _state_info,
    final_bellman_validation,
    min_boundary_pb,
    min_boundary_pb_state,
)
from deep_learning_hank.two_asset.continuous_ftb_resolvent_hjb import (
    FTBStepConstructionFailure,
    construct_ftb_step,
)
from deep_learning_hank.two_asset.local_resolvent_domain_geometry import (
    boundary_direction_matrix,
)

# ---------------------------------------------------------------------------
# Frozen diagnostic constants (Issue #64 section 6) — do NOT change
# ---------------------------------------------------------------------------
EPS_ALPHA = 1.0e-6                    # interior factor for alpha_near
HALF_ALPHA = 0.5                      # alpha_half = HALF_ALPHA * alpha_near
MATERIAL_REDUCTION_RATIO = 0.50       # frozen ex ante dual material-reduction threshold
RECONSTRUCT_STEPS = 8                 # accepted Issue #63 FTB steps to reproduce
NEWTON_SOLVE_TOL = 1.0e-8             # declared ||J_iter d_N + R_iter||_inf tolerance
SCALING_CHECK_TOL = 1.0e-6            # declared |R_frozen_trial - (1-alpha) R_iter|_inf tolerance

# ---------------------------------------------------------------------------
# Terminals (Issue #64 section 11) — exactly ONE returned by the run
# ---------------------------------------------------------------------------
TERMINAL_A = ("DLH_5VP_STAGNATION_NEWTON_GEOMETRY__BOUNDARY_SAFE_NEWTON_"
              "DIRECTION_MATERIALLY_REDUCES_RESELECTED_RESIDUALS__NEWTON_"
              "TRUST_REGION_DESIGN_GATE_READY")
TERMINAL_B = ("DLH_5VP_STAGNATION_NEWTON_GEOMETRY__POSITIVE_BOUNDARY_SAFE_"
              "NEWTON_STEP_BUT_NONLINEAR_RESIDUAL_REDUCTION_INSUFFICIENT__"
              "FURTHER_DIRECTION_DESIGN_REQUIRED")
TERMINAL_C = ("DLH_5VP_STAGNATION_NEWTON_GEOMETRY__NONFINITE_INCONSISTENT_OR_"
              "NO_POSITIVE_BOUNDARY_SAFE_NEWTON_GEOMETRY__BOUNDARY_HJB_ROUTE_"
              "REVIEW_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VP_AUTHORITY_OR_DEPENDENCY_CONFLICT"


class NewtonGeometryFailure(RuntimeError):
    """Fail-closed: non-finite / internally inconsistent local evidence, a
    failed Newton linear solve, or a domain-safe-trial verification failure."""


def _sector_seq(records: list) -> tuple:
    return tuple((r.family, r.sector) if r is not None else ("?", "?")
                 for r in records)


def _sector_switches(records_a: list, records_b: list) -> int:
    """Count states whose (family, sector) record differs between two builds."""
    switches = 0
    for a, b in zip(records_a, records_b):
        ka = (a.family, a.sector) if a is not None else (None, None)
        kb = (b.family, b.sector) if b is not None else (None, None)
        if ka != kb:
            switches += 1
    return switches


# ---------------------------------------------------------------------------
# 1. Deterministic reconstruction of the accepted Issue #63 stagnation state
# ---------------------------------------------------------------------------
def reconstruct_issue63_stagnation_state() -> dict:
    """Deterministically reconstruct the accepted Issue #63 trajectory and STOP
    immediately after accepted FTB step 8, before any new HJB iterate is
    accepted. Returns solver / labor0 / V_star (= V8) / the preserved
    pre-step-8 F0 policy records / the 8-row trace / rho.

    The trace mirrors the accepted Issue #63 continuation trace row-for-row
    (identical build-once-and-reuse contract, identical step construction), so
    the reproduced numbers must match the accepted
    ``DLH_5VO_CONTINUATION_TRACE.csv``.
    """
    solver = BoundaryHJBSolver(CENTRAL_CONFIG)
    labor0 = solver.build_labor0(0.0, 0.0)
    V0 = solver.build_initial_value(labor0, 0.0, 0.0)
    rho = float(solver.config.params.rho)
    v0_pb = min_boundary_pb(solver, V0, labor0)
    V = V0.copy()
    trace: list[dict] = []
    prev_sector: Optional[tuple] = None
    records: list = [None] * solver.state_size
    min_accepted_pb = float("inf")
    for iteration in range(1, RECONSTRUCT_STEPS + 1):
        # accepted selected policy / utility / conservative backward Q,u built
        # EXACTLY ONCE per accepted iterate; the step construction reuses it
        Q, u, diag, records = solver.build_operator_and_u(
            V, labor0, 0.0, 0.0, final=False)
        max_q1 = float(np.max(np.abs(np.asarray(Q.sum(axis=1)).ravel())))
        expansions = int(diag["total_expansions"])
        bindings = int(diag["artificial_binding"])
        sector_now = _sector_seq(records)
        changes = (sum(1 for x, y in zip(prev_sector, sector_now) if x != y)
                   if prev_sector is not None else 0)
        prev_sector = sector_now
        direction_norm = float(np.max(np.abs(
            u + Q.dot(V.ravel(order="F")) - rho * V.ravel(order="F"))))
        worst_before = min_boundary_pb_state(solver, V, labor0)
        step = construct_ftb_step(solver, V, labor0, Q, u, rho)
        V_new = step["V_new"]
        statistic = float(np.max(np.abs((V_new - V).ravel())))
        pb_new = min_boundary_pb(solver, V_new, labor0)
        min_accepted_pb = min(min_accepted_pb, pb_new)
        worst_after = min_boundary_pb_state(solver, V_new, labor0)
        trace.append({
            "iteration": iteration,
            "path": step["path"],
            "min_pb_Vn": float(min_boundary_pb(solver, V, labor0)),
            "m0": step["m0"],
            "m_target": step["m_target"],
            "h_cap": step["h_cap"],
            "cap_direct": step["cap_direct"],
            "halving_count": step["halving_count"],
            "delta_lo": step["delta_lo"],
            "delta_hi": step["delta_hi"],
            "delta_ftb": step["delta_ftb"],
            "delta_selected": step["delta_selected"],
            "accepted_max_stat": statistic,
            "selected_min_pb": step["selected_min_pb"],
            "retained_margin": step["retained_margin"],
            "retained_ratio": step["retained_ratio"],
            "worst_before": _state_info(solver, worst_before[1], worst_before[2]),
            "worst_after": _state_info(solver, worst_after[1], worst_after[2]),
            "max_abs_q1": max_q1,
            "expansions": expansions,
            "artificial_bindings": bindings,
            "sector_changes": changes,
            "direction_norm": direction_norm,
        })
        V = V_new
    # V = V8 (after accepted step 8); records = the final=False build at V7,
    # i.e. the preserved pre-step-8 F0 policy records used by the accepted
    # Issue #63 final-validation semantics.
    return {
        "solver": solver, "labor0": labor0, "V_star": V.copy(),
        "records_pre_step8": records, "trace": trace, "rho": rho,
        "v0_min_boundary_pb": v0_pb, "min_accepted_boundary_pb": min_accepted_pb,
    }


# ---------------------------------------------------------------------------
# 2/3. Residual / operator decomposition at the frozen stagnation state
# ---------------------------------------------------------------------------
def residual_stats(solver: BoundaryHJBSolver, R: np.ndarray) -> dict:
    """Total / F0-only / boundary-only max-abs stats of a residual vector.

    State-vector layout is z-major, node-fastest: row = nz*n + node. Returns
    dicts of {"max_abs": float, "argmax_state": dict} for each subset.
    """
    n, nz = solver.n, solver.nz
    g = solver.grid
    fam = np.array([str(g.families[node]) for node in range(n)])
    # state layout is z-major, node-fastest: row = z*n + node
    f0_mask = np.tile(fam == "F0", nz)
    bnd_mask = ~f0_mask

    def _stat(mask: np.ndarray) -> dict:
        rows = np.nonzero(mask)[0]
        if rows.size == 0:
            return {"max_abs": 0.0, "argmax_state": None}
        idx = int(np.argmax(np.abs(R[rows])))
        row = int(rows[idx])
        node, nz_i = row % n, row // n
        return {"max_abs": float(np.abs(R[row])),
                "argmax_state": _state_info(solver, node, nz_i)}

    return {
        "total": _stat(np.ones(R.size, dtype=bool)),
        "f0": _stat(f0_mask),
        "boundary": _stat(bnd_mask),
    }


def residual_decomposition(solver: BoundaryHJBSolver, V_star: np.ndarray,
                           labor0: np.ndarray, records_pre_step8: list,
                           rho: float) -> dict:
    """Iteration-vs-final residual / operator decomposition at ``V_*``.

    - ``Q_iter,u_iter`` built EXACTLY ONCE (accepted ``final=False``
      semantics); ``R_iter = rho*V_* - [u_iter + Q_iter V_*]``;
    - ``Q_final,u_final`` built with accepted Issue #63 final-validation
      semantics (``final=True`` with the preserved pre-step-8 F0 records);
      ``R_final = rho*V_* - [u_final + Q_final V_*]`` (must reproduce
      ~490.756);
    - total / F0-only / boundary-only max-abs stats for ``R_iter``,
      ``R_final`` and ``R_final - R_iter``, plus the operator diagnostics.

    FAIL-CLOSED on any non-finite residual component.
    """
    n, nz = solver.n, solver.nz
    V_flat = V_star.ravel(order="F")
    Q_iter, u_iter, diag_iter, records_iter = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=False)
    R_iter = rho * V_flat - (u_iter + Q_iter.dot(V_flat))
    Q_final, u_final, diag_final, records_final = solver.build_operator_and_u(
        V_star, labor0, 0.0, 0.0, final=True, f0_policies=records_pre_step8)
    R_final = rho * V_flat - (u_final + Q_final.dot(V_flat))
    for R in (R_iter, R_final):
        if not np.isfinite(R).all():
            raise NewtonGeometryFailure(
                "non-finite residual component in the decomposition")
    dR = R_final - R_iter
    return {
        "Q_iter": Q_iter, "u_iter": u_iter, "records_iter": records_iter,
        "diag_iter": diag_iter,
        "Q_final": Q_final, "u_final": u_final, "records_final": records_final,
        "diag_final": diag_final,
        "R_iter": R_iter, "R_final": R_final, "dR": dR,
        "stats_iter": residual_stats(solver, R_iter),
        "stats_final": residual_stats(solver, R_final),
        "stats_diff": residual_stats(solver, dR),
        "max_abs_q1_iter": float(np.max(np.abs(
            np.asarray(Q_iter.sum(axis=1)).ravel()))),
        "max_abs_q1_final": float(np.max(np.abs(
            np.asarray(Q_final.sum(axis=1)).ravel()))),
        "expansions_iter": int(diag_iter["total_expansions"]),
        "bindings_iter": int(diag_iter["artificial_binding"]),
        "expansions_final": int(diag_final["total_expansions"]),
        "bindings_final": int(diag_final["artificial_binding"]),
    }


# ---------------------------------------------------------------------------
# 4. Exactly ONE frozen-policy Newton direction
# ---------------------------------------------------------------------------
def frozen_policy_newton_direction(solver: BoundaryHJBSolver,
                                   Q_iter: sparse.csr_matrix, u_iter: np.ndarray,
                                   V_star: np.ndarray, R_iter: np.ndarray,
                                   rho: float) -> dict:
    """Solve ``J_iter d_N = -R_iter`` with ``J_iter = rho I - Q_iter``.

    Exact Newton step for the frozen linear policy/operator (NOT a nonlinear
    Newton theorem). FAIL-CLOSED on non-finite output or a failed solve.
    """
    S = solver.state_size
    J = rho * sparse.eye(S, format="csr") - Q_iter
    rhs = -R_iter
    try:
        dN = linalg.spsolve(J, rhs)
    except Exception as exc:  # pragma: no cover - defensive
        raise NewtonGeometryFailure(
            f"Newton linear solve raised: {exc!r}") from exc
    if dN.shape != (S,) or not np.isfinite(dN).all():
        raise NewtonGeometryFailure("non-finite Newton direction d_N")
    lin_res = J.dot(dN) + R_iter
    return {
        "J": J, "dN": dN,
        "dN_max_abs": float(np.max(np.abs(dN))),
        "lin_res_max_abs": float(np.max(np.abs(lin_res))),
        "lin_res_ok": bool(np.max(np.abs(lin_res)) <= NEWTON_SOLVE_TOL),
    }


# ---------------------------------------------------------------------------
# 5. ONE boundary-crossing calculation (accepted Issue #62 semantics)
# ---------------------------------------------------------------------------
def boundary_crossing(solver: BoundaryHJBSolver, V_star: np.ndarray,
                      labor0: np.ndarray, dN: np.ndarray) -> dict:
    """alpha_cross over the accepted required boundary states.

    - required states = non-F0 nodes x z, p_b = vb_b(V_*) (finite required);
    - dp_b(d_N): regular backward finite-difference states use the linear
      difference of ``d_N``; ``i==0`` V-independent states are exactly 0
      (accepted Issue #62 ``boundary_direction_matrix`` semantics);
    - ``alpha_cross_i = (p_b(V_*) - PB_MARGIN)/(-dp_b(d_N))`` for every state
      with ``dp_b(d_N) < 0``; ``alpha_cross = min`` positive finite
      ``alpha_cross_i``;
    - ``alpha_near = min(1, (1-EPS_ALPHA)*alpha_cross)`` if a finite positive
      crossing exists, otherwise ``1``; ``alpha_half = HALF_ALPHA*alpha_near``.

    FAIL-CLOSED on any non-finite required p_b or directional evidence.
    """
    n, nz = solver.n, solver.nz
    g = solver.grid
    pb_star, node0, nz0 = min_boundary_pb_state(solver, V_star, labor0)
    if not np.isfinite(pb_star):
        raise NewtonGeometryFailure(
            f"non-finite required boundary p_b(V_star): {pb_star!r} at "
            f"node {node0} z {nz0}")
    _, pb_matrix, _, _ = solver.compute_derivatives(V_star, labor0, 0.0, 0.0)
    dp_matrix = boundary_direction_matrix(
        solver, dN.reshape((n, nz), order="F"))
    required = 0
    zero_count = 0
    negative_count = 0
    crossing_items: list[tuple[float, int, int]] = []
    for node in range(solver.n):
        if g.families[node] == "F0":
            continue
        for nz_i in range(solver.nz):
            required += 1
            p = float(pb_matrix[node, nz_i])
            if not np.isfinite(p):
                raise NewtonGeometryFailure(
                    f"non-finite boundary p_b at node {node} z {nz_i}: {p!r}")
            dp = float(dp_matrix[node, nz_i])
            if not np.isfinite(dp):
                raise NewtonGeometryFailure(
                    f"non-finite directional evidence at node {node} z {nz_i}: "
                    f"{dp!r}")
            if dp == 0.0:
                zero_count += 1            # V-independent boundary rule (i==0)
            if dp < 0.0:
                negative_count += 1
                ac = (p - PB_MARGIN) / (-dp)
                crossing_items.append((ac, node, nz_i))
    finite_positive = [it for it in crossing_items
                       if np.isfinite(it[0]) and it[0] > 0.0]
    if finite_positive:
        best = min(finite_positive, key=lambda it: it[0])
        alpha_cross = float(best[0])
        alpha_cross_state = _state_info(solver, best[1], best[2])
    else:
        alpha_cross = None
        alpha_cross_state = None
    alpha_near = (min(1.0, (1.0 - EPS_ALPHA) * alpha_cross)
                  if alpha_cross is not None else 1.0)
    alpha_half = HALF_ALPHA * alpha_near
    return {
        "pb_star": float(pb_star),
        "terminal_state": _state_info(solver, node0, nz0),
        "dpb_required_count": required,
        "dpb_negative_count": negative_count,
        "dpb_zero_count": zero_count,
        "alpha_cross": alpha_cross,
        "alpha_cross_state": alpha_cross_state,
        "alpha_near": float(alpha_near),
        "alpha_half": float(alpha_half),
        "positive_finite_crossing_count": len(finite_positive),
    }


# ---------------------------------------------------------------------------
# 6. Exactly TWO diagnostic trial fractions (alpha_half, alpha_near)
# ---------------------------------------------------------------------------
def _trial_domain_check(solver: BoundaryHJBSolver, V_trial: np.ndarray,
                        labor0: np.ndarray) -> tuple[float, dict]:
    """All required boundary p_b finite and > PB_MARGIN (fail closed)."""
    pb, node, nz = min_boundary_pb_state(solver, V_trial, labor0)
    if not np.isfinite(pb):
        raise NewtonGeometryFailure(
            f"non-finite required boundary p_b at trial state: {pb!r}")
    return float(pb), _state_info(solver, node, nz)


def evaluate_trial(solver: BoundaryHJBSolver, labor0: np.ndarray, rho: float,
                   V_star: np.ndarray, dN: np.ndarray, R_iter: np.ndarray,
                   R_final: np.ndarray, Q_iter: sparse.csr_matrix,
                   u_iter: np.ndarray, records_iter: list,
                   alpha: float, name: str) -> dict:
    """One diagnostic trial at fraction ``alpha`` (exactly once).

    1. V_trial = V_* + alpha*d_N;
    2. directly verify all required boundary p_b finite and > PB_MARGIN;
    3. verify the frozen residual relation
       R_iter(V_trial; frozen Q_iter,u_iter) = (1-alpha) R_iter(V_*);
    4. exactly ONE ``final=False`` nonlinear policy re-selection ->
       R_reselect;
    5. accepted final-validation-style residual at the SAME trial with the
       TRIAL re-selected records as the F0 policy input -> R_final_trial;
    6. record residual ratios and policy/sector switching counts.

    The trial state is diagnostic only and is never accepted as a new HJB
    iterate. FAIL-CLOSED on any contract violation.
    """
    n, nz = solver.n, solver.nz
    V_trial = (V_star.ravel(order="F") + alpha * dN).reshape((n, nz), order="F")
    trial_min_pb, trial_min_pb_state = _trial_domain_check(
        solver, V_trial, labor0)
    domain_safe = bool(trial_min_pb > PB_MARGIN)
    if not domain_safe:
        raise NewtonGeometryFailure(
            f"trial {name} at alpha={alpha:.12g} leaves the effective domain "
            f"(min p_b = {trial_min_pb:.12g} <= PB_MARGIN)")

    V_flat = V_trial.ravel(order="F")
    # 3. frozen residual scaling (linear operator identity, up to the Newton
    #    solve residual)
    R_frozen_trial = rho * V_flat - (u_iter + Q_iter.dot(V_flat))
    expected = (1.0 - alpha) * R_iter
    dev = R_frozen_trial - expected
    dev_max = float(np.max(np.abs(dev)))
    rel_dev_max = float(np.max(np.abs(dev) / (np.abs(expected) + 1e-300)))
    if not (dev_max <= SCALING_CHECK_TOL):
        raise NewtonGeometryFailure(
            f"trial {name}: frozen residual does not scale as (1-alpha): "
            f"max|dev| = {dev_max:.6e} > {SCALING_CHECK_TOL:.6e}")

    # 4. exactly ONE final=False nonlinear policy re-selection
    Q_res, u_res, diag_res, records_trial = solver.build_operator_and_u(
        V_trial, labor0, 0.0, 0.0, final=False)
    R_reselect = rho * V_flat - (u_res + Q_res.dot(V_flat))
    if not np.isfinite(R_reselect).all():
        raise NewtonGeometryFailure(
            f"trial {name}: non-finite re-selected residual")

    # 5. final-validation-style residual with the TRIAL re-selected records
    Q_ft, u_ft, diag_ft, records_ft = solver.build_operator_and_u(
        V_trial, labor0, 0.0, 0.0, final=True, f0_policies=records_trial)
    R_final_trial = rho * V_flat - (u_ft + Q_ft.dot(V_flat))
    if not np.isfinite(R_final_trial).all():
        raise NewtonGeometryFailure(
            f"trial {name}: non-finite final-validation-style residual")

    r_iter_inf = float(np.max(np.abs(R_iter)))
    r_final_inf = float(np.max(np.abs(R_final)))
    ratio_iter = (float(np.max(np.abs(R_reselect))) / r_iter_inf
                  if r_iter_inf > 0.0 else None)
    ratio_final = (float(np.max(np.abs(R_final_trial))) / r_final_inf
                   if r_final_inf > 0.0 else None)
    material = bool(
        ratio_iter is not None and ratio_final is not None
        and ratio_iter <= MATERIAL_REDUCTION_RATIO
        and ratio_final <= MATERIAL_REDUCTION_RATIO)
    return {
        "name": name,
        "alpha": float(alpha),
        "trial_min_pb": trial_min_pb,
        "trial_min_pb_state": trial_min_pb_state,
        "domain_safe": domain_safe,
        "frozen_dev_max_abs": dev_max,
        "frozen_rel_dev_max_abs": rel_dev_max,
        "r_reselect_inf": float(np.max(np.abs(R_reselect))),
        "ratio_iter": ratio_iter,
        "r_final_trial_inf": float(np.max(np.abs(R_final_trial))),
        "ratio_final": ratio_final,
        "sector_switches_vs_iter": _sector_switches(records_iter, records_trial),
        "artificial_bindings_trial": int(diag_res["artificial_binding"]),
        "expansions_trial": int(diag_res["total_expansions"]),
        "max_abs_q1_trial": float(np.max(np.abs(
            np.asarray(Q_res.sum(axis=1)).ravel()))),
        "f0_rows_final_trial": int(sum(
            1 for r in records_ft if r is not None and r.family == "F0")),
        "material_reduction": material,
        "R_reselect": R_reselect, "R_final_trial": R_final_trial,
        "records_trial": records_trial, "V_trial": V_trial,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
@dataclass
class NewtonGeometryResult:
    outcome: str
    # -- reconstruction ------------------------------------------------------
    iterations: int
    trace: list[dict]
    v0_min_boundary_pb: float
    min_accepted_boundary_pb: float
    final_statistic: Optional[float]
    min_boundary_pb_star: float
    wall_state: Optional[dict]
    final_validation_residual: Optional[float]
    # -- residual decomposition ----------------------------------------------
    r_iter_inf: Optional[float]
    r_iter_argmax: Optional[dict]
    r_iter_f0_max: Optional[float]
    r_iter_f0_argmax: Optional[dict]
    r_iter_boundary_max: Optional[float]
    r_iter_boundary_argmax: Optional[dict]
    r_final_inf: Optional[float]
    r_final_argmax: Optional[dict]
    r_final_f0_max: Optional[float]
    r_final_f0_argmax: Optional[dict]
    r_final_boundary_max: Optional[float]
    r_final_boundary_argmax: Optional[dict]
    r_diff_inf: Optional[float]
    r_diff_argmax: Optional[dict]
    r_diff_f0_max: Optional[float]
    r_diff_boundary_max: Optional[float]
    max_abs_q1_iter: Optional[float]
    max_abs_q1_final: Optional[float]
    expansions_iter: Optional[int]
    bindings_iter: Optional[int]
    expansions_final: Optional[int]
    bindings_final: Optional[int]
    # -- Newton direction ----------------------------------------------------
    dN_max_abs: Optional[float]
    lin_res_max_abs: Optional[float]
    lin_res_ok: Optional[bool]
    # -- boundary crossing ---------------------------------------------------
    dpb_required_count: Optional[int]
    dpb_negative_count: Optional[int]
    dpb_zero_count: Optional[int]
    alpha_cross: Optional[float]
    alpha_cross_state: Optional[dict]
    alpha_near: Optional[float]
    alpha_half: Optional[float]
    positive_finite_crossing_count: Optional[int]
    # -- trials --------------------------------------------------------------
    trials: list[dict] = field(default_factory=list)
    material_reduction_any: bool = False
    # -- determinism ----------------------------------------------------------
    deterministic_repeat_identical: bool = False
    failure_detail: Optional[dict] = None

    def to_summary_csv_lines(self) -> list[str]:
        """Key/value summary CSV (DLH_5VP_NEWTON_GEOMETRY_SUMMARY.csv)."""

        def st(d: Optional[dict]) -> str:
            if d is None:
                return ""
            return (f"node={d.get('node')},j={d.get('j')},i={d.get('i')},"
                    f"z={d.get('z')},family={d.get('family')}")

        def f(x) -> str:
            return "" if x is None else f"{x:.12g}"

        rows: list[tuple[str, str]] = [
            ("outcome", self.outcome),
            ("reconstruction.iterations", str(self.iterations)),
            ("reconstruction.v0_min_boundary_pb", f(self.v0_min_boundary_pb)),
            ("reconstruction.min_accepted_boundary_pb", f(self.min_accepted_boundary_pb)),
            ("reconstruction.final_statistic", f(self.final_statistic)),
            ("reconstruction.min_boundary_pb_star", f(self.min_boundary_pb_star)),
            ("reconstruction.wall_state", st(self.wall_state)),
            ("reconstruction.final_validation_residual", f(self.final_validation_residual)),
            ("residual_iter.inf_norm", f(self.r_iter_inf)),
            ("residual_iter.argmax", st(self.r_iter_argmax)),
            ("residual_iter.f0_max", f(self.r_iter_f0_max)),
            ("residual_iter.f0_argmax", st(self.r_iter_f0_argmax)),
            ("residual_iter.boundary_max", f(self.r_iter_boundary_max)),
            ("residual_iter.boundary_argmax", st(self.r_iter_boundary_argmax)),
            ("residual_final.inf_norm", f(self.r_final_inf)),
            ("residual_final.argmax", st(self.r_final_argmax)),
            ("residual_final.f0_max", f(self.r_final_f0_max)),
            ("residual_final.f0_argmax", st(self.r_final_f0_argmax)),
            ("residual_final.boundary_max", f(self.r_final_boundary_max)),
            ("residual_final.boundary_argmax", st(self.r_final_boundary_argmax)),
            ("residual_diff.inf_norm", f(self.r_diff_inf)),
            ("residual_diff.argmax", st(self.r_diff_argmax)),
            ("residual_diff.f0_max", f(self.r_diff_f0_max)),
            ("residual_diff.boundary_max", f(self.r_diff_boundary_max)),
            ("operator.max_abs_q1_iter", f(self.max_abs_q1_iter)),
            ("operator.max_abs_q1_final", f(self.max_abs_q1_final)),
            ("operator.expansions_iter", str(self.expansions_iter)),
            ("operator.bindings_iter", str(self.bindings_iter)),
            ("operator.expansions_final", str(self.expansions_final)),
            ("operator.bindings_final", str(self.bindings_final)),
            ("newton.dN_max_abs", f(self.dN_max_abs)),
            ("newton.lin_res_max_abs", f(self.lin_res_max_abs)),
            ("newton.lin_res_ok", str(self.lin_res_ok).lower()),
            ("boundary.dpb_required_count", str(self.dpb_required_count)),
            ("boundary.dpb_negative_count", str(self.dpb_negative_count)),
            ("boundary.dpb_zero_count", str(self.dpb_zero_count)),
            ("boundary.alpha_cross", f(self.alpha_cross)),
            ("boundary.alpha_cross_state", st(self.alpha_cross_state)),
            ("boundary.alpha_near", f(self.alpha_near)),
            ("boundary.alpha_half", f(self.alpha_half)),
            ("boundary.positive_finite_crossing_count",
             str(self.positive_finite_crossing_count)),
            ("trial_count", str(len(self.trials))),
        ]
        for t in self.trials:
            prefix = f"trial.{t['name']}"
            rows.append((f"{prefix}.alpha", f(t["alpha"])))
            rows.append((f"{prefix}.trial_min_pb", f(t["trial_min_pb"])))
            rows.append((f"{prefix}.trial_min_pb_state", st(t["trial_min_pb_state"])))
            rows.append((f"{prefix}.domain_safe", str(t["domain_safe"]).lower()))
            rows.append((f"{prefix}.frozen_dev_max_abs", f(t["frozen_dev_max_abs"])))
            rows.append((f"{prefix}.frozen_rel_dev_max_abs", f(t["frozen_rel_dev_max_abs"])))
            rows.append((f"{prefix}.r_reselect_inf", f(t["r_reselect_inf"])))
            rows.append((f"{prefix}.ratio_iter", f(t["ratio_iter"])))
            rows.append((f"{prefix}.r_final_trial_inf", f(t["r_final_trial_inf"])))
            rows.append((f"{prefix}.ratio_final", f(t["ratio_final"])))
            rows.append((f"{prefix}.sector_switches_vs_iter", str(t["sector_switches_vs_iter"])))
            rows.append((f"{prefix}.artificial_bindings_trial", str(t["artificial_bindings_trial"])))
            rows.append((f"{prefix}.expansions_trial", str(t["expansions_trial"])))
            rows.append((f"{prefix}.max_abs_q1_trial", f(t["max_abs_q1_trial"])))
            rows.append((f"{prefix}.material_reduction", str(t["material_reduction"]).lower()))
        rows.append(("material_reduction_any", str(self.material_reduction_any).lower()))
        rows.append(("deterministic_repeat_identical",
                     str(self.deterministic_repeat_identical).lower()))
        return [",".join([k, v]) for (k, v) in rows]


def run_issue64_diagnostic() -> NewtonGeometryResult:
    """Exactly one full Issue #64 diagnostic:
    1) reconstruction, 2) residual/operator decomposition, 3) Newton
    direction, 4) boundary crossing, 5) exactly two trial fractions."""
    failure_detail: Optional[dict] = None
    try:
        rec = reconstruct_issue63_stagnation_state()
        solver: BoundaryHJBSolver = rec["solver"]
        labor0: np.ndarray = rec["labor0"]
        V_star: np.ndarray = rec["V_star"]
        records_pre: list = rec["records_pre_step8"]
        rho: float = rec["rho"]
        trace: list = rec["trace"]
        # accepted final-validation residual (preserved pre-step-8 records)
        val = final_bellman_validation(solver, V_star, labor0, records_pre)
        # 2/3. decomposition
        dec = residual_decomposition(solver, V_star, labor0, records_pre, rho)
        # 4. exactly ONE frozen-policy Newton direction
        newt = frozen_policy_newton_direction(
            solver, dec["Q_iter"], dec["u_iter"], V_star, dec["R_iter"], rho)
        # 5. ONE boundary-crossing calculation
        bd = boundary_crossing(solver, V_star, labor0, newt["dN"])
        # 6. exactly TWO diagnostic trials
        trials = [
            evaluate_trial(
                solver, labor0, rho, V_star, newt["dN"], dec["R_iter"],
                dec["R_final"], dec["Q_iter"], dec["u_iter"],
                dec["records_iter"], bd["alpha_half"], "alpha_half"),
            evaluate_trial(
                solver, labor0, rho, V_star, newt["dN"], dec["R_iter"],
                dec["R_final"], dec["Q_iter"], dec["u_iter"],
                dec["records_iter"], bd["alpha_near"], "alpha_near"),
        ]
        material_any = any(t["material_reduction"] for t in trials)
        wall_pb, wall_node, wall_nz = min_boundary_pb_state(solver, V_star, labor0)
        return NewtonGeometryResult(
            outcome="", iterations=RECONSTRUCT_STEPS, trace=trace,
            v0_min_boundary_pb=float(rec["v0_min_boundary_pb"]),
            min_accepted_boundary_pb=float(rec["min_accepted_boundary_pb"]),
            final_statistic=float(trace[-1]["accepted_max_stat"]),
            min_boundary_pb_star=float(wall_pb),
            wall_state=_state_info(solver, wall_node, wall_nz),
            final_validation_residual=float(val["bellman_residual"]),
            r_iter_inf=dec["stats_iter"]["total"]["max_abs"],
            r_iter_argmax=dec["stats_iter"]["total"]["argmax_state"],
            r_iter_f0_max=dec["stats_iter"]["f0"]["max_abs"],
            r_iter_f0_argmax=dec["stats_iter"]["f0"]["argmax_state"],
            r_iter_boundary_max=dec["stats_iter"]["boundary"]["max_abs"],
            r_iter_boundary_argmax=dec["stats_iter"]["boundary"]["argmax_state"],
            r_final_inf=dec["stats_final"]["total"]["max_abs"],
            r_final_argmax=dec["stats_final"]["total"]["argmax_state"],
            r_final_f0_max=dec["stats_final"]["f0"]["max_abs"],
            r_final_f0_argmax=dec["stats_final"]["f0"]["argmax_state"],
            r_final_boundary_max=dec["stats_final"]["boundary"]["max_abs"],
            r_final_boundary_argmax=dec["stats_final"]["boundary"]["argmax_state"],
            r_diff_inf=dec["stats_diff"]["total"]["max_abs"],
            r_diff_argmax=dec["stats_diff"]["total"]["argmax_state"],
            r_diff_f0_max=dec["stats_diff"]["f0"]["max_abs"],
            r_diff_boundary_max=dec["stats_diff"]["boundary"]["max_abs"],
            max_abs_q1_iter=dec["max_abs_q1_iter"],
            max_abs_q1_final=dec["max_abs_q1_final"],
            expansions_iter=dec["expansions_iter"], bindings_iter=dec["bindings_iter"],
            expansions_final=dec["expansions_final"], bindings_final=dec["bindings_final"],
            dN_max_abs=newt["dN_max_abs"], lin_res_max_abs=newt["lin_res_max_abs"],
            lin_res_ok=newt["lin_res_ok"],
            dpb_required_count=bd["dpb_required_count"],
            dpb_negative_count=bd["dpb_negative_count"],
            dpb_zero_count=bd["dpb_zero_count"],
            alpha_cross=bd["alpha_cross"], alpha_cross_state=bd["alpha_cross_state"],
            alpha_near=bd["alpha_near"], alpha_half=bd["alpha_half"],
            positive_finite_crossing_count=bd["positive_finite_crossing_count"],
            trials=trials, material_reduction_any=material_any,
        )
    except (NewtonGeometryFailure, FTBStepConstructionFailure,
            BoundaryHJBFailure) as exc:
        failure_detail = {"message": str(exc)}
        return NewtonGeometryResult(
            outcome=TERMINAL_C, iterations=0, trace=[], v0_min_boundary_pb=0.0,
            min_accepted_boundary_pb=0.0, final_statistic=None,
            min_boundary_pb_star=0.0, wall_state=None,
            final_validation_residual=None, r_iter_inf=None, r_iter_argmax=None,
            r_iter_f0_max=None, r_iter_f0_argmax=None, r_iter_boundary_max=None,
            r_iter_boundary_argmax=None, r_final_inf=None, r_final_argmax=None,
            r_final_f0_max=None, r_final_f0_argmax=None,
            r_final_boundary_max=None, r_final_boundary_argmax=None,
            r_diff_inf=None, r_diff_argmax=None, r_diff_f0_max=None,
            r_diff_boundary_max=None, max_abs_q1_iter=None,
            max_abs_q1_final=None, expansions_iter=None, bindings_iter=None,
            expansions_final=None, bindings_final=None, dN_max_abs=None,
            lin_res_max_abs=None, lin_res_ok=None, dpb_required_count=None,
            dpb_negative_count=None, dpb_zero_count=None, alpha_cross=None,
            alpha_cross_state=None, alpha_near=None, alpha_half=None,
            positive_finite_crossing_count=None, trials=[],
            material_reduction_any=False, failure_detail=failure_detail,
        )


def _canon(r: NewtonGeometryResult):
    def c(x):
        if isinstance(x, dict):
            return tuple(sorted((k, c(v)) for k, v in x.items()))
        if isinstance(x, list):
            return tuple(c(v) for v in x)
        if isinstance(x, float):
            return ("f", repr(x))
        if isinstance(x, np.ndarray):
            return ("a", repr(x.tolist()))
        return (type(x).__name__, str(x))

    return (
        c(r.trace), c(r.iterations), c(r.final_statistic),
        c(r.min_boundary_pb_star), c(r.wall_state),
        c(r.final_validation_residual), c(r.r_iter_inf), c(r.r_iter_argmax),
        c(r.r_iter_f0_max), c(r.r_iter_f0_argmax), c(r.r_iter_boundary_max),
        c(r.r_iter_boundary_argmax), c(r.r_final_inf), c(r.r_final_argmax),
        c(r.r_final_f0_max), c(r.r_final_f0_argmax), c(r.r_final_boundary_max),
        c(r.r_final_boundary_argmax), c(r.r_diff_inf), c(r.r_diff_argmax),
        c(r.r_diff_f0_max), c(r.r_diff_boundary_max), c(r.max_abs_q1_iter),
        c(r.max_abs_q1_final), c(r.expansions_iter), c(r.bindings_iter),
        c(r.expansions_final), c(r.bindings_final), c(r.dN_max_abs),
        c(r.lin_res_max_abs), c(r.lin_res_ok), c(r.dpb_required_count),
        c(r.dpb_negative_count), c(r.dpb_zero_count), c(r.alpha_cross),
        c(r.alpha_cross_state), c(r.alpha_near), c(r.alpha_half),
        c(r.positive_finite_crossing_count), c(r.trials),
        c(r.material_reduction_any),
    )


def finalize_outcome(r1: NewtonGeometryResult,
                     repeat_identical: bool) -> str:
    """Exactly one Issue #64 terminal from the local evidence (fail closed)."""
    if not repeat_identical:
        return TERMINAL_C           # deterministic repeat mismatch = inconsistency
    if r1.failure_detail is not None:
        return TERMINAL_C
    # reconstruction must reproduce the accepted Issue #63 stagnation state
    trace = r1.trace
    recon_ok = (
        len(trace) == RECONSTRUCT_STEPS
        and trace[-1]["path"] == "root"
        and trace[-1]["cap_direct"] is False
        and r1.final_statistic is not None
        and abs(r1.final_statistic - 3.6614352438846254e-08)
        / 3.6614352438846254e-08 <= 1e-6
        and r1.final_validation_residual is not None
        and abs(r1.final_validation_residual - 490.7560425919994)
        / 490.7560425919994 <= 1e-9
        and r1.wall_state is not None
        and r1.wall_state["node"] == 332
        and r1.wall_state["family"] == "F3"
        and r1.wall_state["i"] == 13
        and r1.wall_state["j"] == 13
        and r1.wall_state["z"] == 1
    )
    if not recon_ok:
        return TERMINAL_C
    if r1.lin_res_ok is not True:
        return TERMINAL_C           # Newton solve evidence outside tolerance
    if (r1.alpha_cross is None or r1.alpha_near is None
            or not (np.isfinite(r1.alpha_cross) and r1.alpha_cross > 0.0)
            or not (np.isfinite(r1.alpha_near) and r1.alpha_near > 0.0)):
        return TERMINAL_C           # no strictly positive boundary-safe fraction
    if len(r1.trials) != 2:
        return TERMINAL_C
    if not all(t["domain_safe"] for t in r1.trials):
        return TERMINAL_C           # trial states must be strictly domain-safe
    if r1.material_reduction_any:
        return TERMINAL_A
    return TERMINAL_B


def run_issue64_diagnostic_twice() -> tuple[NewtonGeometryResult, bool]:
    """One full diagnostic + one deterministic repeat (bit-identical);
    returns (finalized result with exactly one terminal, repeat_identical)."""
    r1 = run_issue64_diagnostic()
    r2 = run_issue64_diagnostic()
    identical = bool(_canon(r1) == _canon(r2))
    outcome = finalize_outcome(r1, identical)
    return (
        dataclasses.replace(
            r1, outcome=outcome,
            deterministic_repeat_identical=identical),
        identical,
    )
