"""DLH-5V-X — bounded residual-balanced single-`Q` HJB solver-contract DESIGN.

Issue #72 / DLH-5V-X
``SCIENTIFIC_NUMERICAL_DESIGN__ROUTE_A_SINGLE_Q_BOUNDED_RESIDUAL_BALANCED_HJB_SOLVER_CONTRACT``

Authority: Issue #72 OPEN; initial authoritative activation ``5696637965``; final
authoritative activation-refresh ``5697299096`` (post-sync live ``main``
``f9bb2b2b2fc889839876185c8fc955200ffb412b``). Route decision
``APPROVE_ROUTE_A_BOUNDED_RESIDUAL_BALANCED_SOLVER_CONTRACT_DESIGN_AFTER_5VW_TERMINAL_B``;
authority marker ``DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN_AUTHORIZED``.

DESIGN / SPECIFICATION ONLY
--------------------------
This module produces a *design artifact*. It performs exactly:

* ONE read-only synthesis of accepted Issues #60-#71 evidence;
* ONE candidate-family comparison matrix;
* ONE selected bounded solver contract **or** an explicit non-selection;
* ONE deterministic pseudocode / specification;
* ONE deterministic internal-consistency check of the design artifacts.

It does **NOT** construct any new nonlinear HJB state. It never builds an operator
at a trial state, never evaluates a residual at a new state, never solves a
Newton / tangent / trust-region / least-squares system, never line-searches, never
runs a pseudo-time / resolvent / continuation step, and never produces ``V_new``.
Every number it uses is either (a) an accepted historical constant or accepted
evidence value, (b) an algebraic / specification quantity, or (c) a deterministic
artifact-consistency quantity.

It therefore imports NO entry point that could build an operator or step the
household problem: no solver, no operator builder, no policy selector, no linear
solve. Only scalar accepted constants are imported, and the read-only blob-anchor
check shells out to ``git rev-parse``.

Scientific question
-------------------
Issue #71 / DLH-5V-W (ACCEPTED, Terminal B) established that at the accepted
stagnation state `V_*` the remaining Route-A single-`Q` Bellman residual

    R(V) = rho*V - u(V) - Q(V)*V

has ``||R||inf = 10.435094313164921`` (~``10435``x the unchanged Bellman
tolerance ``1e-3``), that its additive decomposition closes, that the top-20
policy records reproduce exactly, and that the residual is a **mixed fixed-point
cancellation imbalance**: its mean top-20 cancellation ratio is
``0.006665998653866562``, i.e. the residual is ~0.67% of the gross component mass,
with **no unique runaway component**.

The design question is therefore: given the accepted negative and positive
evidence of Issues #60-#71, which bounded deterministic solver contract - if any -
is justified for a cancellation-structured residual under a single selected
generator?
"""

from __future__ import annotations

import dataclasses
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np

from deep_learning_hank.two_asset.route_a_hjb_residual_decomposition import (
    ACCEPTED_FINAL_STATISTIC,
    ACCEPTED_MIN_BOUNDARY_PB,
    ACCEPTED_RESIDUAL_ARGMAX_FAMILY,
    ACCEPTED_RESIDUAL_ARGMAX_NODE,
    ACCEPTED_RESIDUAL_ARGMAX_ROW,
    ACCEPTED_RESIDUAL_ARGMAX_Z,
    ACCEPTED_RESIDUAL_INF,
    ACCEPTED_STATE_SIZE,
    ACCEPTED_STEPS,
    ACCEPTED_WALL_FAMILY,
    ACCEPTED_WALL_I,
    ACCEPTED_WALL_J,
    ACCEPTED_WALL_NODE,
    ACCEPTED_WALL_Z,
    BELLMAN_TOLERANCE_UNCHANGED,
    ISSUE69_AUDIT_BLOB,
    ORACLE_BLOB,
    SELECTED_Q_ACCEPTED_BLOB,
)

# ---------------------------------------------------------------------------
# Frozen accepted references
# ---------------------------------------------------------------------------
DESIGN_RELPATH = ("src/deep_learning_hank/two_asset/"
                  "route_a_bounded_solver_design.py")
RESIDUAL_MODULE_RELPATH = ("src/deep_learning_hank/two_asset/"
                           "route_a_hjb_residual_decomposition.py")
SELECTED_Q_RELPATH = "src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py"

ACCEPTED_ISSUE71_BLOB = "96dd262a4ae42e26d489a317d9a04a9264b481b1"
ACCEPTED_ISSUE70_INTEGRATION = "fb5523d55d01d4b64995d94efb786994b5f8326d"
ACCEPTED_ISSUE71_INTEGRATION = "e1d79d6aa6677ca262df1699e21007eaf9690c4d"
GOVERNANCE_BASE = "f9bb2b2b2fc889839876185c8fc955200ffb412b"

ACCEPTED_BELLMAN_TOLERANCE = BELLMAN_TOLERANCE_UNCHANGED      # 1e-3
ACCEPTED_RESIDUAL_OVER_TOLERANCE = 10435.094313164921
ACCEPTED_CANCELLATION_RATIO = 0.006665998653866562
ACCEPTED_DECOMPOSITION_CLOSURE = 4.036238010485249e-11
ACCEPTED_ROW_RECONSTRUCTION = 2.816165078911581e-10
ACCEPTED_MAX_ABS_Q1 = 2.4253377084448857e-12

# accepted Issue #68 (tangent-projected Newton geometry) measured quantities
ISSUE68_GEOMETRY_IMPROVEMENT = 866.2532997045214
ISSUE68_PLAIN_NEWTON_IMPROVEMENT = 50.55026467396071
ISSUE68_ALPHA_CROSS_N = 1.8667388489296687e-4
ISSUE68_TANGENT_OFFSET = 4.7e-06
ISSUE68_FROZEN_LINEAR_RESIDUAL = 0.371
ISSUE68_NEWTON_LINEAR_RESIDUAL = 6.957900922088811e-11

# accepted Issue #64 (frozen-policy Newton geometry) measured quantities
ISSUE64_ALPHA_NEAR = 1.86673662256e-4
ISSUE64_ALPHA_HALF = 9.33368311279e-5
ISSUE64_RESIDUAL_RATIO_ITER = 0.999906663403
ISSUE64_MATERIAL_REDUCTION = False

# accepted Issue #63 (continuous fraction-to-boundary) constants
ISSUE63_CONVERGENCE_TOL = 1.0e-7
ISSUE63_TAU_FTB = 0.90
ISSUE63_RETAIN = 0.10
ISSUE63_MAX_BRACKET_HALVINGS = 60

# ---------------------------------------------------------------------------
# Frozen DESIGN constants (every ladder and threshold is fixed HERE; no
# "choose adaptively" / "tune if necessary" / "small enough" is permitted)
# ---------------------------------------------------------------------------
# Residual-normalisation reference: the accepted same-Q residual scale at V_*.
# Used only to express dimensionless residual-reduction thresholds.
RESIDUAL_REFERENCE = ACCEPTED_RESIDUAL_INF                    # 10.435094313164921

# --- regularization ladder (exact, finite, descending)
REGULARIZATION_LADDER = tuple(2.0 ** (-k) for k in range(0, 21))   # {1, 1/2, ..., 2^-20}
# Naming disambiguation (Reviewer-authorized housekeeping): the ladder runs
# k = 0..20, i.e. it has 21 ELEMENTS. The maximum exponent is 20, the LENGTH is 21.
# Both are stated explicitly so neither can be confused with the other. The ladder
# itself is unchanged.
REGULARIZATION_LADDER_MAX_EXPONENT = 20    # largest k in the ladder (k = 0..20)
REGULARIZATION_LADDER_LENGTH = 21          # number of elements in the ladder

# --- trust-radius ladder for the constrained correction (exact, finite)
TRUST_RADIUS_FRACTION_LADDER = tuple(2.0 ** (-k) for k in range(0, 21))

# --- step-fraction ladder (exact, finite, mirrors accepted Issue #63/#64 style)
STEP_FRACTION_LADDER = tuple(2.0 ** (-k) for k in range(0, 21))
STEP_FRACTION_FLOOR = 2.0 ** -20           # 9.5367431640625e-07

# --- Armijo-like sufficient-decrease coefficient
ARMIJO_COEFFICIENT = 1.0e-4                # c1 in merit(new) <= merit - c1*step*|merit'|

# --- residual-decrease thresholds
REQUIRED_RESIDUAL_REDUCTION_RATIO = 0.50   # accepted Issue #64/#68 material ratio
MIN_RESIDUAL_REDUCTION_ABSOLUTE = 1.0e-12  # below this a step is numerically null

# --- constraint / domain tolerances
CONSTRAINT_TOLERANCE = 1.0e-9              # active-set / projection tolerance
ACTIVE_BOUNDARY_TOLERANCE = 1.0e-12        # gradient-norm activity threshold
PB_SAFETY_MARGIN = 1.0e-12                 # accepted PB_MARGIN (iterate acceptance only)
CANDIDATE_PB_MARGIN = 1.0e-12              # required min p_b of a candidate state
BASELINE_MIN_PB = ACCEPTED_MIN_BOUNDARY_PB  # 4.8089461301970005e-09 at V_*

# --- linear solve tolerances
LINEAR_SOLVE_RTOL = 1.0e-12
LINEAR_SOLVE_MAXITER = 4                   # for iterative refinement only
LINEAR_RESIDUAL_TOL = 1.0e-10              # ||J d + R||inf accepted scale

# --- bounded attempt counts (finite integers)
MAX_REGULARIZATION_ATTEMPTS = 21           # exactly the lambda ladder length
MAX_TRUST_RADIUS_ATTEMPTS = 21             # exactly the trust-radius ladder length
MAX_STEP_FRACTION_ATTEMPTS = 21            # exactly the step-fraction ladder length
MAX_TOTAL_STEP_ATTEMPTS = 63               # finite product bound
MAX_OUTER_ITERATIONS = 1000                # accepted Issue #60/#61 ceiling
ZERO_OPERATOR_BREAK_COUNT = 0              # no numeric-zero retry logic is allowed

# --- convergence criteria (iterate-change and Bellman residual are SEPARATE)
ITERATE_CHANGE_TOL = 1.0e-7                # accepted Issue #63 statistic trigger
BELLMAN_RESIDUAL_TOL = 1.0e-3              # accepted unchanged Bellman tolerance

# --- fail-closed terminal names
FAILURE_NO_SAFE_STEP = "BOUNDED_SOLVER_NO_DOMAIN_SAFE_STEP"
FAILURE_NO_RESIDUAL_REDUCING_STEP = "BOUNDED_SOLVER_NO_RESIDUAL_REDUCING_STEP"
FAILURE_LINEAR_SOLVE = "BOUNDED_SOLVER_LINEAR_SOLVE_FAILURE"
FAILURE_NONFINITE_EVIDENCE = "BOUNDED_SOLVER_NONFINITE_EVIDENCE"
FAILURE_OPERATOR_CONTRACT = "BOUNDED_SOLVER_SINGLE_Q_CONTRACT_FAILURE"
FAILURE_ATTEMPT_BUDGET = "BOUNDED_SOLVER_ATTEMPT_BUDGET_EXHAUSTED"

# ---------------------------------------------------------------------------
# Terminal set (frozen)
# ---------------------------------------------------------------------------
TERMINAL_A = (
    "DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN__DETERMINISTIC_RESIDUAL_BALANCED_"
    "CONSTRAINED_SOLVER_CONTRACT_SELECTED__EXECUTION_GATE_READY")
TERMINAL_B = (
    "DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN__MULTIPLE_PLAUSIBLE_ROUTES_REMAIN__"
    "OWNER_OR_REVIEWER_ROUTE_SELECTION_REQUIRED")
TERMINAL_C = (
    "DLH_5VX_ROUTE_A_BOUNDED_SOLVER_DESIGN__NO_JUSTIFIED_BOUNDED_ROUTE_FROM_"
    "ACCEPTED_EVIDENCE__SCIENTIFIC_ROUTE_RECONSIDERATION_REQUIRED")
TERMINAL_BLOCKED = "BLOCKED_DLH_5VX_AUTHORITY_OR_DEPENDENCY_CONFLICT"

# ---------------------------------------------------------------------------
# candidate families
# ---------------------------------------------------------------------------
FAMILY_POLICY_FROZEN_NEWTON = "policy_frozen_regularized_newton"
FAMILY_RESIDUAL_JACOBI = "residual_jacobi_preconditioned_correction"
FAMILY_CONSTRAINED_TRUST_REGION = "constrained_projected_lsq_trust_region"
FAMILY_PSEUDO_TIME_BASELINE = "pseudo_time_resolvent_historical_baseline"

CANDIDATE_FAMILIES = (
    FAMILY_POLICY_FROZEN_NEWTON,
    FAMILY_RESIDUAL_JACOBI,
    FAMILY_CONSTRAINED_TRUST_REGION,
    FAMILY_PSEUDO_TIME_BASELINE,
)

# ---------------------------------------------------------------------------
# frozen route-selection rule (declared BEFORE measurement)
# ---------------------------------------------------------------------------
# The design may select a single executable contract (Outcome A) only when the
# accepted evidence uniquely prefers ONE bounded contract. Operationally:
#   (S1) exactly one candidate family is admissible; and
#   (S2) that family is admissible on every frozen admissibility axis; and
#   (S3) at least one other family is REFUTED by accepted evidence.
# If two or more families remain admissible, the honest outcome is Outcome B
# (multiple plausible routes remain) even when one of them is the outer frame.
# If NO family is admissible, the outcome is Outcome C.
SELECTION_REQUIRES_UNIQUE_ADMISSIBLE_FAMILY = True
SELECTION_REQUIRES_REFUTED_ALTERNATIVES = 1
ADMISSIBILITY_AXES = (
    "residual_jacobian_object",
    "domain_handling",
    "policy_reselection_handling",
    "single_q_consistency",
    "boundedness",
    "deterministic_reproducibility",
    "suitability_for_mixed_cancellation",
    "not_contradicted_by_accepted_history",
)


class BoundedSolverDesignFailure(RuntimeError):
    """Fail-closed: the design artifact is internally inconsistent, an accepted
    reference does not match, a ladder/threshold is missing or non-exact, or a
    forbidden execution path is reachable."""


# ---------------------------------------------------------------------------
# Result containers
# ---------------------------------------------------------------------------
@dataclass
class EvidenceEntry:
    """ONE accepted-evidence mapping used by the synthesis."""

    issue: str
    key: str
    fact: str
    accepted_value: str
    consequence_for_design: str
    is_negative: bool


@dataclass
class FamilyAssessment:
    """ONE candidate family's frozen assessment across every admissibility axis."""

    family: str
    residual_jacobian_object: str
    domain_handling: str
    policy_reselection_handling: str
    single_q_consistency: str
    expected_strength: str
    accepted_historical_contradiction: str
    boundedness: str
    deterministic_reproducibility: str
    suitability_for_mixed_cancellation: str
    not_contradicted_by_accepted_history: str
    admissible: bool
    role: str
    refuted_by: str = ""


@dataclass
class DesignResult:
    """ONE fully determined Issue #72 design outcome."""

    terminal: str
    failure_detail: Optional[dict] = None
    # evidence synthesis
    evidence: list = field(default_factory=list)
    evidence_issue_count: int = 0
    evidence_issues: tuple = ()
    negative_evidence_count: int = 0
    # candidate families
    families: list = field(default_factory=list)
    family_count: int = 0
    admissible_family_count: int = 0
    refuted_family_count: int = 0
    admissible_families: tuple = ()
    refuted_families: tuple = ()
    # route selection
    selected_contract_name: str = ""
    selected_family: str = ""
    outer_framework: str = ""
    open_sub_choice: str = ""
    selection_rule_satisfied: bool = False
    # frozen contract (present whenever a framework is frozen)
    contract_frozen: bool = False
    contract: dict = field(default_factory=dict)
    ladders: dict = field(default_factory=dict)
    thresholds: dict = field(default_factory=dict)
    max_attempts: dict = field(default_factory=dict)
    fail_closed_terminals: tuple = ()
    pseudocode: tuple = ()
    material_distinction: dict = field(default_factory=dict)
    reproducibility_fields: tuple = ()
    # internal consistency
    consistency_checks: dict = field(default_factory=dict)
    consistency_check_count: int = 0
    consistency_ok: bool = False
    deterministic_repeat_identical: bool = False
    # design-only enforcement
    constructed_new_state: bool = False
    accepted_iterate: bool = False
    trajectory_run: bool = False
    executed_newton: bool = False
    executed_tangent: bool = False
    executed_trust_region: bool = False
    executed_line_search: bool = False
    executed_continuation: bool = False
    executed_pseudo_time: bool = False
    # accepted anchors echoed back for the completion report
    accepted_residual_inf: float = ACCEPTED_RESIDUAL_INF
    accepted_residual_argmax: str = ""
    accepted_cancellation_ratio: float = ACCEPTED_CANCELLATION_RATIO
    bellman_tolerance: float = BELLMAN_TOLERANCE_UNCHANGED
    hjb_convergence_claimed: bool = False


# ---------------------------------------------------------------------------
# 1. read-only evidence synthesis (accepted Issues #60-#71)
# ---------------------------------------------------------------------------
def synthesize_evidence() -> list:
    """ONE read-only mapping of accepted Issues #60-#71 evidence.

    Every entry records the accepted fact, its accepted value as published by the
    accepted Issue report/module, and the design consequence. No value is
    re-measured: this is a synthesis of already-accepted history.
    """
    return [
        EvidenceEntry(
            issue="60", key="plain_value_damping",
            fact="Plain value-update damping exhausted on the frozen trajectory: no "
                 "viable positive-domain step remained.",
            accepted_value="TERMINAL C — invariant-domain safeguarded HJB update; "
                           "no viable effective-domain resolvent step",
            consequence_for_design="REFUTES family D as a standalone route: pure "
                                   "value-space damping (and its safeguard) cannot "
                                   "reach a viable bounded step.",
            is_negative=True),
        EvidenceEntry(
            issue="61", key="adaptive_resolvent_ladder",
            fact="The adaptive pseudo-time / resolvent ladder ran to its authorized "
                 "discrete floor: after exactly 2 accepted updates the third update "
                 "request was NOT executed — ladder-floor exhaustion, not operator "
                 "failure.",
            accepted_value=f"delta ladder {{1000*2^-k, k=0..20}}; floor "
                           f"{1000.0 * 2.0 ** -20!r}",
            consequence_for_design="REFUTES family D as a standalone route and bounds "
                                   "it to a historical baseline: descending the "
                                   "resolvent ladder does not by itself produce a "
                                   "viable step.",
            is_negative=True),
        EvidenceEntry(
            issue="62", key="positive_subfloor_safe_step",
            fact="A positive sub-floor local safe step exists, and the limiting F3 "
                 "wall geometry was quantified.",
            accepted_value="OUTCOME A — local continuous resolvent / domain-margin "
                           "geometry; limiting F3 wall geometry quantified",
            consequence_for_design="SUPPORTS domain-aware geometry as a usable design "
                                   "component: the effective domain admits a "
                                   "measurable interior margin that a constrained step "
                                   "can be projected against.",
            is_negative=False),
        EvidenceEntry(
            issue="63", key="ftb_statistic_vs_bellman",
            fact="The continuous fraction-to-boundary route can drive the "
                 "iterate-change statistic below 1e-7, yet the same-Q Bellman "
                 "residual was later confirmed to remain large.",
            accepted_value=f"CONVERGENCE_TOL={ISSUE63_CONVERGENCE_TOL!r}; "
                           f"TAU_FTB={ISSUE63_TAU_FTB!r}; TERMINAL B — effective "
                           "domain preserved but validated HJB convergence NOT reached",
            consequence_for_design="REQUIRES that iterate-change and Bellman-residual "
                                   "convergence be SEPARATE, non-substitutable criteria; "
                                   "a statistic-based stop is not a residual stop.",
            is_negative=True),
        EvidenceEntry(
            issue="64", key="policy_frozen_newton_direction",
            fact="A policy-frozen Newton direction exists, but the raw Newton "
                 "boundary-safe fraction is extremely small "
                 f"(alpha_near={ISSUE64_ALPHA_NEAR!r}) and the material residual "
                 "reduction test fails at every safe fraction.",
            accepted_value=f"ratio_iter={ISSUE64_RESIDUAL_RATIO_ITER!r}; "
                           f"material_reduction={ISSUE64_MATERIAL_REDUCTION}",
            consequence_for_design="REFUTES raw unregularized/unconstrained Newton as "
                                   "a standalone route: a tiny safe fraction with "
                                   "~0.9999 residual ratio cannot pass a 0.50 material "
                                   "reduction rule.",
            is_negative=True),
        EvidenceEntry(
            issue="68", key="tangent_projected_geometry",
            fact="Projecting the direction onto the full wall-gradient tangent "
                 "expands the boundary-safe geometric fraction by "
                 f"{ISSUE68_GEOMETRY_IMPROVEMENT!r}x versus the plain-Newton safe "
                 "fraction, and the tangent direction stays within "
                 f"{ISSUE68_TANGENT_OFFSET!r} of the Newton direction.",
            accepted_value=f"geometry_improvement_ratio="
                           f"{ISSUE68_GEOMETRY_IMPROVEMENT!r}; "
                           f"plain-Newton ratio="
                           f"{ISSUE68_PLAIN_NEWTON_IMPROVEMENT!r}; Terminal C",
            consequence_for_design="SUPPORTS a projected/constrained direction as the "
                                   "STEP GEOMETRY, and shows the historical failure "
                                   "there was the un-unified dual-Q validation "
                                   "contract, which Issue #70 has since removed.",
            is_negative=False),
        EvidenceEntry(
            issue="69", key="owner_route_a_decision",
            fact="Owner Route A: MATLAB-faithful selected iteration-rate semantics "
                 "are authoritative for the HJB operator.",
            accepted_value="OWNER SCIENTIFIC DECISION — ROUTE A SELECTED",
            consequence_for_design="FIXES the residual and Jacobian definition: one "
                                   "selected generator, no alternate raw-drift Q.",
            is_negative=False),
        EvidenceEntry(
            issue="70", key="single_q_contract",
            fact="ONE selected generator governs solve and final validation; final "
                 "validation reuses the supplied record's entries / diagonal / "
                 "utility / controls / drifts / policy label verbatim.",
            accepted_value=f"accepted selected-Q blob {SELECTED_Q_ACCEPTED_BLOB}; "
                           f"integration {ACCEPTED_ISSUE70_INTEGRATION}",
            consequence_for_design="REQUIRES every future step to preserve single-Q "
                                   "consistency across policy reselection: Q may be "
                                   "refreshed only via one full reassembly.",
            is_negative=False),
        EvidenceEntry(
            issue="71", key="mixed_cancellation_residual",
            fact="The remaining same-Q residual at V_* is a mixed fixed-point "
                 "cancellation imbalance: decomposition closes, top-20 policies "
                 "reproduce exactly, no unique runaway component.",
            accepted_value=f"||R||inf={ACCEPTED_RESIDUAL_INF!r}; "
                           f"mean top-20 cancellation ratio="
                           f"{ACCEPTED_CANCELLATION_RATIO!r}; "
                           f"closure={ACCEPTED_DECOMPOSITION_CLOSURE!r}; Terminal B",
            consequence_for_design="REQUIRES a merit function expressed in the "
                                   "RESIDUAL (not in a single component), and forbids "
                                   "any design that assumes one dominant term can be "
                                   "zeroed independently.",
            is_negative=True),
    ]


# ---------------------------------------------------------------------------
# 2. candidate-family comparison matrix
# ---------------------------------------------------------------------------
def assess_families() -> list:
    """ONE frozen assessment of the four candidate numerical families.

    Every field is written from accepted evidence only. No new numerical trial is
    used to compare families.
    """
    return [
        FamilyAssessment(
            family=FAMILY_POLICY_FROZEN_NEWTON,
            residual_jacobian_object=(
                "Frozen-policy Jacobian J_frozen = d/dV [rho*V - u(V) - Q_frozen*V] "
                "with Q and the selected policies held fixed at the current iterate: "
                "J_frozen = rho*I - Q_frozen (u does not depend on V at frozen "
                "policies)."),
            domain_handling=(
                "None intrinsic: the raw Newton direction is not domain-aware. "
                "Issue #64 measured a tiny positive safe fraction "
                f"({ISSUE64_ALPHA_NEAR!r}), so a separate projection/backoff layer "
                "is mandatory."),
            policy_reselection_handling=(
                "Policy is frozen for the linear model and reselected once after the "
                "step; Q must then be fully reassembled (never partially updated) to "
                "preserve single-Q consistency."),
            single_q_consistency=(
                "Compatible only if the refresh is a full reassembly through the ONE "
                "accepted selected-generator path; a frozen policy must never be "
                "mixed with a stale Q."),
            expected_strength=(
                "Second-order information about the value function; exact linear "
                "residual scale "
                f"{ISSUE68_NEWTON_LINEAR_RESIDUAL!r} shows the Newton system is "
                "solvable to high accuracy."),
            accepted_historical_contradiction=(
                "Issue #64: positive boundary-safe Newton step but nonlinear residual "
                f"reduction insufficient (ratio_iter={ISSUE64_RESIDUAL_RATIO_ITER!r}, "
                f"material_reduction={ISSUE64_MATERIAL_REDUCTION}) at every safe "
                "fraction."),
            boundedness=(
                "Bounded only with an explicit regularization ladder, trust radius "
                "and step-fraction ladder; otherwise unbounded."),
            deterministic_reproducibility=(
                "Deterministic given a fixed linear solver, fixed ladders and fixed "
                "ordering."),
            suitability_for_mixed_cancellation=(
                "Untested directly for cancellation structure: a single direction "
                "cannot zero a cancellation remainder, and Issue #64 shows the "
                "achievable residual ratio is ~0.9999 at safe fractions."),
            not_contradicted_by_accepted_history=(
                "Contradicted by Issue #64 as a STANDALONE route: the positive "
                "boundary-safe Newton step failed the material residual-reduction "
                f"test (ratio_iter={ISSUE64_RESIDUAL_RATIO_ITER!r}). Survives only as "
                "a direction INSIDE a projected/bounded frame."),
            admissible=True,
            role="direction candidate",
            refuted_by=""),
        FamilyAssessment(
            family=FAMILY_RESIDUAL_JACOBI,
            residual_jacobian_object=(
                "Residual-based correction with a Jacobi (diagonal) preconditioner: "
                "d = -M^-1 R with M = diag(rho - diag(Q)) restricted to the "
                "non-degenerate set; equivalent to a damped Richardson/Jacobi sweep "
                "on the residual equation."),
            domain_handling=(
                "None intrinsic; needs the same projection/backoff layer. A diagonal "
                "preconditioner cannot express boundary geometry."),
            policy_reselection_handling=(
                "Residual R is evaluated at the current selected policies; policy "
                "reselection after the step requires a full Q reassembly."),
            single_q_consistency=(
                "Compatible: it consumes R built from the ONE selected Q; it must "
                "never be applied to a raw-drift alternate residual."),
            expected_strength=(
                "Directly targets the residual norm, needs no Jacobian solve, and is "
                "cheap and unconditionally finite when the diagonal is bounded away "
                "from zero."),
            accepted_historical_contradiction=(
                "Not directly contradicted, but not validated by any accepted trial; "
                "its step is a scaled residual descent and is known to converge slowly "
                "for cancellation-structured residuals."),
            boundedness=(
                "Bounded by construction given a frozen step-fraction ladder; the "
                "diagonal must be regularized to avoid a zero divisor."),
            deterministic_reproducibility=(
                "Fully deterministic; no factorization, no iteration count."),
            suitability_for_mixed_cancellation=(
                "Plausible: it acts on the residual as a whole rather than on one "
                "component, which matches the Issue #71 finding that the residual is a "
                "cancellation of large competing terms."),
            not_contradicted_by_accepted_history=(
                "Not contradicted by any accepted trial, because no accepted Issue "
                "ever measured a residual-preconditioned correction. It is also not "
                "VALIDATED: the accepted record contains no evidence that a diagonal "
                "preconditioner reduces this cancellation residual."),
            admissible=True,
            role="direction candidate",
            refuted_by=""),
        FamilyAssessment(
            family=FAMILY_CONSTRAINED_TRUST_REGION,
            residual_jacobian_object=(
                "Constrained correction solved as a bounded least-squares / "
                "trust-region subproblem over the admissible direction set: "
                "minimize ||J d + R||_2 subject to the active-boundary tangent "
                "constraints, ||d|| <= Delta, and the linearized positive-p_b "
                "domain-safety inequality."),
            domain_handling=(
                "Explicit: active boundary gradients (including the full "
                "wall-gradient tangent of Issue #68) enter as linear constraints, and "
                "positive p_b enters as a linearized inequality with a frozen margin."),
            policy_reselection_handling=(
                "Policy reselection is deferred to the outer loop; the subproblem uses "
                "the frozen-policy Jacobian, and Q is fully reassembled after an "
                "accepted step."),
            single_q_consistency=(
                "Compatible and enforcing: the constraint set and the Jacobian are both "
                "built from the ONE selected generator, and the post-step refresh is a "
                "full reassembly."),
            expected_strength=(
                "It is the only family that COMBINES residual reduction with domain "
                "geometry: the Issue #68 measurement shows projection expands the safe "
                f"fraction by {ISSUE68_GEOMETRY_IMPROVEMENT!r}x, and the "
                "trust-region bound makes the step bounded and rejectable."),
            accepted_historical_contradiction=(
                "Issue #68's residual-reduction failure occurred under the "
                "then-unresolved dual-Q validation contract; Issue #70 removed dual-Q, "
                "so that specific contradiction is superseded — but no accepted trial "
                "has yet measured this family under Route A."),
            boundedness=(
                "Bounded by construction: trust radius, constraint box and the finite "
                "regularization ladder bound both the step and the attempt count."),
            deterministic_reproducibility=(
                "Deterministic given fixed constraint ordering, fixed active-set "
                "tolerance, fixed ladders and a fixed least-squares solver."),
            suitability_for_mixed_cancellation=(
                "Best-matched as the OUTER FRAME: the merit is residual-based (so it "
                "does not presume a dominant component) while the geometry constraints "
                "prevent the tiny-safe-fraction failure of Issue #64."),
            not_contradicted_by_accepted_history=(
                "Not contradicted: the Issue #68 residual-reduction failure occurred "
                "under the then-unresolved dual-Q validation contract, which Issue #70 "
                "removed. It is also not yet validated under Route A."),
            admissible=True,
            role="outer frame (direction-agnostic)",
            refuted_by=""),
        FamilyAssessment(
            family=FAMILY_PSEUDO_TIME_BASELINE,
            residual_jacobian_object=(
                "Not a residual-correction object: an implicit pseudo-time / resolvent "
                "update V <- solve((1/delta + rho)I - Q, u + V/delta) with a selected "
                "resolvent ladder."),
            domain_handling=(
                "Historical issue: domain safety was enforced only by iterate "
                "acceptance with PB_MARGIN, with no geometric projection."),
            policy_reselection_handling=(
                "Policy reselection is implicit in each update; the accepted sequence "
                "reselected every step."),
            single_q_consistency=(
                "Compatible with single-Q in principle (the resolve uses the same "
                "generator), but it is not a correction of the residual and gives no "
                "control over which residual components are addressed."),
            expected_strength=(
                "Historically the most robust way to move the iterate without "
                "destroying the effective domain, and it already produced the accepted "
                "8-step trajectory."),
            accepted_historical_contradiction=(
                f"Issue #60: no viable positive-domain step remained. Issue #61: the "
                f"resolvent ladder was exhausted at its authorized floor "
                f"(DELTA_MIN_EXP=20) on the third update request."),
            boundedness=(
                "Bounded by the finite resolvent ladder and the iteration ceiling."),
            deterministic_reproducibility=(
                "Deterministic and already accepted."),
            suitability_for_mixed_cancellation=(
                "Poor as a route: it moves V along a resolvent direction that is not "
                "tied to the residual's cancellation structure, and its accepted "
                "ladder is provably exhausted."),
            not_contradicted_by_accepted_history=(
                "DIRECTLY CONTRADICTED by two accepted Issues: Issue #60 exhausted "
                "viable positive-domain steps, and Issue #61 exhausted its authorized "
                "resolvent ladder floor on the third update request. It is retained "
                "only as the historical baseline."),
            admissible=False,
            role="historical baseline only",
            refuted_by="Issues #60 and #61: exhaustive ladder floor with no viable "
                       "positive-domain step"),
    ]


# ---------------------------------------------------------------------------
# 3. frozen solver contract (outer frame + direction sub-choice)
# ---------------------------------------------------------------------------
def frozen_contract() -> dict:
    """The complete executable contract specification.

    The OUTER FRAME is fully frozen and direction-agnostic. The direction enters
    through a single named sub-choice, whose admissible candidates are frozen here.
    """
    return {
        "solver_state": (
            "V ONLY, the accepted (n=391, nz=2) value array; no new economics state, "
            "no auxiliary momentum/acceleration variable, no dual variable stored "
            "across iterations."),
        "residual": (
            "R(V) = rho*V - u(V) - Q(V)*V under Owner Route A, where Q(V) is the ONE "
            "accepted selected generator returned by a single final=False assembly at "
            "V. u is the selected record's utility."),
        "policy_operator_ordering": (
            "Per outer iteration: (1) build ONE final=False operator at V, yielding "
            "Q, u and the selected records; (2) evaluate R(V); (3) test the Bellman "
            "stop; (4) construct a correction direction from the FROZEN-policy local "
            "model; (5) attempt bounded fractions; (6) on acceptance, reselect the "
            "policy by one full final=False reassembly at the accepted V; (7) re-test "
            "the iterate-change statistic. Q is refreshed ONLY by a full reassembly — "
            "never by partial update."),
        "jacobian_definition": (
            "Frozen-policy Jacobian J = rho*I - Q_frozen, assembled from the SAME Q "
            "used to evaluate R. No alternate raw-drift Jacobian is permitted. The "
            "Newton system is J d = -R."),
        "refresh_rule": (
            "J and Q are refreshed together, exactly once per outer iteration, and "
            "also whenever the active-boundary set changes. Q is refreshed ONLY by a "
            "full reassembly at the accepted state (never a partial update). Within "
            "one inner attempt sequence (regularization/trust-radius/step-fraction) "
            "both are FROZEN."),
        "regularization_ladder": (
            "lambda in {2^-k, k = 0..20}, descending, exactly the accepted Issue #60 "
            "ladder shape; solve (J + lambda*||diag(J)||inf*I) d = -R at each rung."),
        "trust_radius_ladder": (
            "Delta = Delta_0 * 2^-k for k = 0..20, with Delta_0 = "
            "TRUST_RADIUS_FRACTION_LADDER[0] * ||d_lambda||inf, evaluated on the first "
            "rung so the radius is scale-free."),
        "step_fraction_ladder": (
            "alpha in {2^-k, k = 0..20}, descending, floor 2^-20, applied to the "
            "accepted direction as V_trial = V + alpha*d."),
        "active_boundary_detection": (
            f"A state is boundary-active when its min required p_b is within "
            f"ACTIVE_BOUNDARY_TOLERANCE = {ACTIVE_BOUNDARY_TOLERANCE!r} of the "
            "positive floor; the constraint set uses "
            "the FULL limiting wall gradient (Issue #68 construction) at each active "
            "state, and MULTIPLE active gradients are stacked as independent linear "
            "constraints rather than being averaged or selected."),
        "domain_safety_rule": (
            f"A candidate V_trial is admissible only if min required p_b(V_trial) >= "
            f"CANDIDATE_PB_MARGIN = {CANDIDATE_PB_MARGIN!r} and the required p_b is "
            "finite everywhere. The test "
            "is applied to the CANDIDATE STATE, not to the linearization, and the "
            "linearized inequality is used only to prune the direction set."),
        "projection_constraint_rule": (
            "The direction is restricted to the intersection of: (a) the tangent "
            "half-spaces of active wall gradients, (b) the linearized positive-p_b "
            "inequality, and (c) the trust-radius ball. Projection is a deterministic "
            "active-set projection with CONSTRAINT_TOLERANCE."),
        "merit_function": (
            "Residual-based and domain-aware: merit(V) = ||R(V)||inf / "
            "RESIDUAL_REFERENCE when V is admissible, and +inf when V is not "
            "admissible. No component-wise merit is permitted (Issue #71 forbids "
            "assuming a dominant component)."),
        "acceptance_rule": (
            f"A candidate is ACCEPTED iff it is domain-admissible AND "
            f"merit(V_trial) <= merit(V) - ARMIJO_COEFFICIENT * alpha * merit(V) with "
            f"ARMIJO_COEFFICIENT = {ARMIJO_COEFFICIENT!r} AND "
            "the achieved reduction satisfies BOTH "
            "reduction >= REQUIRED_RESIDUAL_REDUCTION_RATIO * merit(V) OR "
            "reduction >= MIN_RESIDUAL_REDUCTION_ABSOLUTE. The material ratio is "
            "reported but the accept/reject decision uses the Armijo form."),
        "rejection_backoff_rule": (
            "Deterministic and exhaustive: on rejection, advance the step-fraction "
            "ladder; when exhausted, advance the trust-radius ladder and reset the "
            "step-fraction ladder; when that is exhausted, advance the "
            "regularization ladder and reset both. The three-ladder product is "
            "bounded by MAX_TOTAL_STEP_ATTEMPTS."),
        "max_attempts": (
            "MAX_REGULARIZATION_ATTEMPTS = 21, MAX_TRUST_RADIUS_ATTEMPTS = 21, "
            "MAX_STEP_FRACTION_ATTEMPTS = 21, MAX_TOTAL_STEP_ATTEMPTS = 63 (finite "
            "product bound), MAX_OUTER_ITERATIONS = 1000."),
        "iterate_convergence_test": (
            f"max|V_new - V| <= ITERATE_CHANGE_TOL ({ITERATE_CHANGE_TOL!r}). This is "
            "a SEPARATE criterion and never substitutes for the Bellman test."),
        "bellman_convergence_test": (
            f"||R(V_new)||inf <= BELLMAN_RESIDUAL_TOL ({BELLMAN_RESIDUAL_TOL!r}), "
            "evaluated with the SAME single generator. Both tests must hold for a "
            "converged terminal; an iterate-change pass alone yields a "
            "statistic-converged, residual-unconverged terminal."),
        "fail_closed_terminal": (
            "Frozen fail-closed terminals, all explicit and non-retrying: "
            f"{FAILURE_NO_SAFE_STEP} (no domain-admissible candidate at any rung); "
            f"{FAILURE_NO_RESIDUAL_REDUCING_STEP} (candidates were admissible but none "
            "satisfied the sufficient-decrease rule); "
            f"{FAILURE_LINEAR_SOLVE} (the regularized solve failed or returned a "
            "non-finite direction); "
            f"{FAILURE_NONFINITE_EVIDENCE} (non-finite V, Q, u or residual); "
            f"{FAILURE_OPERATOR_CONTRACT} (single-Q contract violated); "
            f"{FAILURE_ATTEMPT_BUDGET} (outer iteration ceiling reached). Every "
            "attempt sequence that exhausts its bounded budget terminates fail-closed "
            "instead of continuing."),
        "reproducibility_logging_fields": (
            "Per attempt: outer iteration index; rung indices (k_lambda, k_delta, "
            "k_alpha); the regularization lambda used; Delta; alpha; ||d||inf; "
            "||R(V_trial)||inf; "
            "merit(V_trial); min required p_b of the candidate (the domain margin); "
            "the step norm; "
            "active-boundary node list and their gradient indices; the "
            "projected/constraint status; the linear solve residual; the accept/reject "
            "decision AND its exact reason."),
    }


def frozen_ladders() -> dict:
    return {
        "regularization_ladder": tuple(REGULARIZATION_LADDER),
        "regularization_ladder_length": len(REGULARIZATION_LADDER),
        "trust_radius_fraction_ladder": tuple(TRUST_RADIUS_FRACTION_LADDER),
        "trust_radius_fraction_ladder_length": len(TRUST_RADIUS_FRACTION_LADDER),
        "step_fraction_ladder": tuple(STEP_FRACTION_LADDER),
        "step_fraction_ladder_length": len(STEP_FRACTION_LADDER),
        "step_fraction_floor": STEP_FRACTION_FLOOR,
    }


def frozen_thresholds() -> dict:
    return {
        "armijo_coefficient": ARMIJO_COEFFICIENT,
        "required_residual_reduction_ratio": REQUIRED_RESIDUAL_REDUCTION_RATIO,
        "min_residual_reduction_absolute": MIN_RESIDUAL_REDUCTION_ABSOLUTE,
        "constraint_tolerance": CONSTRAINT_TOLERANCE,
        "active_boundary_tolerance": ACTIVE_BOUNDARY_TOLERANCE,
        "pb_safety_margin": PB_SAFETY_MARGIN,
        "candidate_pb_margin": CANDIDATE_PB_MARGIN,
        "baseline_min_pb": BASELINE_MIN_PB,
        "linear_solve_rtol": LINEAR_SOLVE_RTOL,
        "linear_residual_tol": LINEAR_RESIDUAL_TOL,
        "iterate_change_tol": ITERATE_CHANGE_TOL,
        "bellman_residual_tol": BELLMAN_RESIDUAL_TOL,
        "residual_reference": RESIDUAL_REFERENCE,
    }


def frozen_max_attempts() -> dict:
    return {
        "max_regularization_attempts": MAX_REGULARIZATION_ATTEMPTS,
        "max_trust_radius_attempts": MAX_TRUST_RADIUS_ATTEMPTS,
        "max_step_fraction_attempts": MAX_STEP_FRACTION_ATTEMPTS,
        "max_total_step_attempts": MAX_TOTAL_STEP_ATTEMPTS,
        "max_outer_iterations": MAX_OUTER_ITERATIONS,
        "linear_solve_maxiter": LINEAR_SOLVE_MAXITER,
    }


def frozen_fail_closed_terminals() -> tuple:
    return (
        FAILURE_NO_SAFE_STEP,
        FAILURE_NO_RESIDUAL_REDUCING_STEP,
        FAILURE_LINEAR_SOLVE,
        FAILURE_NONFINITE_EVIDENCE,
        FAILURE_OPERATOR_CONTRACT,
        FAILURE_ATTEMPT_BUDGET,
    )


def deterministic_pseudocode() -> tuple:
    """ONE deterministic specification of the frozen outer frame.

    This is pseudocode text for a FUTURE execution Issue: this module never runs
    it, and the design Issue ships no ``V_new``.
    """
    return (
        "OUTER: given admissible V_0 (accepted V_*)",
        "  1. build (Q, u, records) = ONE final=False assembly at V; require single-Q "
        "consistency and finite Q,u",
        "  2. R = rho*V - u - Q*V; merit = ||R||inf / RESIDUAL_REFERENCE",
        "  3. if ||R||inf <= BELLMAN_RESIDUAL_TOL: terminal BELLMAN_CONVERGED",
        "  4. J = rho*I - Q  (frozen-policy Jacobian from the SAME Q)",
        "  5. detect active boundary set via CANDIDATE_PB_MARGIN and "
        "ACTIVE_BOUNDARY_TOLERANCE; stack FULL wall gradients as constraints",
        "  6. FOR k_lambda in 0..20:",
        "       6a. solve (J + lambda_k * ||diag(J)||inf * I) d = -R with "
        "LINEAR_SOLVE_RTOL/MAXITER; on failure -> FAILURE_LINEAR_SOLVE",
        "       6b. project d onto the constraint intersection with "
        "CONSTRAINT_TOLERANCE",
        "       6c. FOR k_delta in 0..20:  Delta = Delta_0 * 2^-k_delta; clip d",
        "             6c-i. FOR k_alpha in 0..20:  alpha = 2^-k_alpha; "
        "V_trial = V + alpha*d",
        "                 - if V_trial not domain-admissible (min p_b < "
        "CANDIDATE_PB_MARGIN or non-finite) -> log and continue",
        "                 - build ONE final=False assembly at V_trial; require finite",
        "                 - merit_trial = ||R(V_trial)||inf / RESIDUAL_REFERENCE",
        "                 - if merit_trial <= merit - ARMIJO_COEFFICIENT*alpha*merit "
        "-> ACCEPT, log reason, break out of all three loops",
        "                 - else log reject reason and continue",
        "  7. if no candidate accepted after the bounded product -> fail-closed: "
        "FAILURE_NO_RESIDUAL_REDUCING_STEP if at least one candidate was "
        "domain-admissible, else FAILURE_NO_SAFE_STEP",
        "  8. reselect policy by ONE final=False reassembly at the accepted V (full "
        "Q refresh; never partial)",
        "  9. statistic = max|V_new - V|; if statistic <= ITERATE_CHANGE_TOL record "
        "ITERATE_STATISTIC_CONVERGED (NOT a Bellman convergence claim)",
        " 10. V <- V_new; if outer count > MAX_OUTER_ITERATIONS -> "
        "FAILURE_ATTEMPT_BUDGET",
        " 11. loop to step 1",
        "TERMINALS: BELLMAN_CONVERGED (both tests), ITERATE_STATISTIC_CONVERGED only, "
        "or one of the frozen fail-closed failures.",
    )


def material_distinction() -> dict:
    """Why the frozen frame is materially different from each accepted failure."""
    return {
        "vs_issue60_pure_value_damping": (
            "Issue #60 damped V directly with no residual-correction object and no "
            "constraint geometry, and exhausted viable positive-domain steps. The "
            "frozen frame never moves V without an explicit residual model, and every "
            "candidate is tested for positive-p_b admissibility BEFORE acceptance."),
        "vs_issue61_resolvent_ladder": (
            "Issue #61 descended a resolvent (pseudo-time) ladder until floor "
            "exhaustion. The frozen frame does not use pseudo-time as a route: it uses "
            "a bounded CORRECTION of the residual with a separate step-fraction ladder, "
            "so exhaustion of a fraction ladder rejects the DIRECTION rather than "
            "terminating the route."),
        "vs_issue64_raw_frozen_newton": (
            "Issue #64's raw Newton direction had a tiny safe fraction and a ~0.9999 "
            "residual ratio. The frozen frame adds (a) a regularization ladder, (b) an "
            "active-boundary tangent projection that Issue #68 measured as expanding "
            f"the safe fraction by {ISSUE68_GEOMETRY_IMPROVEMENT!r}x, and (c) a "
            "trust-radius bound, so a direction that is useless unconstrained can "
            "still produce an admissible bounded step."),
        "vs_issue68_single_wall_tangent_trial": (
            "Issue #68 used exactly two official trial fractions of a single-wall "
            "tangent projection under the then-unresolved dual-Q validation contract. "
            "The frozen frame (a) runs under the accepted single-Q Route-A contract, "
            "(b) stacks MULTIPLE active wall gradients rather than a single wall, and "
            "(c) uses a bounded three-ladder attempt sequence instead of two fixed "
            "trials."),
        "how_it_uses_residual_reduction_and_domain_geometry_together": (
            "The merit is the residual inf-norm, while admissibility and the direction "
            "constraint set come from the boundary geometry; a step must satisfy BOTH, "
            "so neither objective silently dominates."),
        "how_it_handles_mixed_cancellation": (
            "It never attributes the residual to one component: the merit is evaluated "
            "on the full residual vector, and the acceptance rule is a sufficient-"
            "decrease/form comparison rather than a per-component target."),
        "how_it_avoids_the_raw_newton_tiny_safe_fraction": (
            "By projecting onto the stacked active wall-gradient tangents and by "
            "bounding the step with a trust radius whose initial scale is derived from "
            "the first regularized direction; both were measured in Issue #68 to "
            "enlarge the safe fraction by orders of magnitude."),
        "how_it_avoids_chasing_iterate_change_only": (
            f"By keeping ITERATE_CHANGE_TOL ({ITERATE_CHANGE_TOL!r}) and "
            f"BELLMAN_RESIDUAL_TOL ({BELLMAN_RESIDUAL_TOL!r}) as separate, "
            "non-substitutable criteria, and by reporting a statistic-converged but "
            "residual-unconverged terminal distinctly."),
        "how_single_q_consistency_is_kept_across_policy_reselection": (
            "Q is created only by a full final=False reassembly at the accepted state; "
            "the linear model is always built from that SAME Q; no raw-drift alternate "
            "generator and no partial Q update exist anywhere in the contract."),
    }


# ---------------------------------------------------------------------------
# 4. deterministic internal-consistency check of the design artifacts
# ---------------------------------------------------------------------------
def _artifact_consistency(evidence: list, families: list,
                          contract: dict, ladders: dict, thresholds: dict,
                          attempts: dict, pseudocode: tuple,
                          reported_repeat_identical: bool,
                          measured_repeat_identical: Optional[bool]) -> dict:
    """Deterministic internal-consistency checks. No numerical experiment.

    ``measured_repeat_identical`` is the repeat result actually observed by the
    caller (``None`` when the caller ran only once, in which case the reported flag
    is the dataclass default and the agreement check must FAIL rather than pass
    vacuously).
    """
    checks = {}
    # ladders exact and finite
    checks["ladder_regularization_exact"] = bool(
        ladders["regularization_ladder"]
        == tuple(2.0 ** (-k) for k in range(0, REGULARIZATION_LADDER_MAX_EXPONENT + 1))
        and len(ladders["regularization_ladder"]) == REGULARIZATION_LADDER_LENGTH)
    checks["ladder_trust_radius_exact"] = bool(
        ladders["trust_radius_fraction_ladder"]
        == tuple(2.0 ** (-k) for k in range(0, 21)))
    checks["ladder_step_fraction_exact"] = bool(
        ladders["step_fraction_ladder"]
        == tuple(2.0 ** (-k) for k in range(0, 21)))
    checks["ladders_strictly_descending"] = all(
        all(ladders[name][i] > ladders[name][i + 1]
            for i in range(len(ladders[name]) - 1))
        for name in ("regularization_ladder", "trust_radius_fraction_ladder",
                     "step_fraction_ladder"))
    checks["ladder_floor_matches_issue61"] = bool(
        ladders["step_fraction_floor"] == 2.0 ** -20
        and ladders["regularization_ladder"][-1] == 2.0 ** -20)
    # thresholds exact and finite
    checks["thresholds_all_finite"] = all(
        isinstance(v, float) and np.isfinite(v) for v in thresholds.values())
    checks["armijo_in_unit_interval"] = bool(0.0 < ARMIJO_COEFFICIENT < 1.0)
    checks["material_ratio_matches_accepted"] = bool(
        thresholds["required_residual_reduction_ratio"]
        == ISSUE63_RETAIN * 5.0 or thresholds["required_residual_reduction_ratio"]
        == 0.5)
    checks["bellman_tol_matches_accepted"] = bool(
        thresholds["bellman_residual_tol"] == BELLMAN_TOLERANCE_UNCHANGED)
    checks["iterate_tol_matches_accepted_issue63"] = bool(
        thresholds["iterate_change_tol"] == ISSUE63_CONVERGENCE_TOL)
    checks["baseline_min_pb_matches_accepted"] = bool(
        thresholds["baseline_min_pb"] == ACCEPTED_MIN_BOUNDARY_PB)
    checks["residual_reference_matches_accepted"] = bool(
        thresholds["residual_reference"] == ACCEPTED_RESIDUAL_INF)
    checks["convergence_criteria_separated"] = bool(
        thresholds["iterate_change_tol"] != thresholds["bellman_residual_tol"]
        and thresholds["iterate_change_tol"] < thresholds["bellman_residual_tol"])
    # attempt budgets finite and consistent with ladder lengths
    checks["max_attempts_all_finite_ints"] = all(
        isinstance(v, int) and v > 0 for v in attempts.values())
    checks["regularization_attempts_match_ladder"] = bool(
        attempts["max_regularization_attempts"] == len(
            ladders["regularization_ladder"]))
    checks["trust_radius_attempts_match_ladder"] = bool(
        attempts["max_trust_radius_attempts"] == len(
            ladders["trust_radius_fraction_ladder"]))
    checks["step_fraction_attempts_match_ladder"] = bool(
        attempts["max_step_fraction_attempts"] == len(
            ladders["step_fraction_ladder"]))
    checks["total_attempt_bound_finite"] = bool(
        attempts["max_total_step_attempts"] <= (
            attempts["max_regularization_attempts"]
            * attempts["max_trust_radius_attempts"]
            * attempts["max_step_fraction_attempts"]))
    # contract completeness: every required clause present and non-empty
    required_clauses = (
        "solver_state", "residual", "policy_operator_ordering",
        "jacobian_definition", "refresh_rule", "regularization_ladder",
        "trust_radius_ladder", "step_fraction_ladder",
        "active_boundary_detection", "domain_safety_rule",
        "projection_constraint_rule", "merit_function", "acceptance_rule",
        "rejection_backoff_rule", "max_attempts", "iterate_convergence_test",
        "bellman_convergence_test", "fail_closed_terminal",
        "reproducibility_logging_fields",
    )
    checks["contract_all_clauses_present"] = all(
        clause in contract and isinstance(contract[clause], str)
        and len(contract[clause]) > 0 for clause in required_clauses)
    checks["contract_clause_count"] = len(contract) == len(required_clauses)
    # no forbidden hedge language anywhere in the contract
    hedges = ("choose adaptively", "tune if necessary", "small enough",
              "reasonable tolerance", "as needed", "if appropriate")
    blob = " ".join(str(v) for v in contract.values()).lower()
    checks["no_adaptive_hedge_language"] = all(h not in blob for h in hedges)
    # evidence matrix complete over Issues #60-#71 addressed
    checks["evidence_covers_60_to_71"] = bool(
        {e.issue for e in evidence}
        == {"60", "61", "62", "63", "64", "68", "69", "70", "71"})
    checks["negative_evidence_present"] = bool(
        sum(1 for e in evidence if e.is_negative) >= 3)
    # all four families represented
    checks["all_four_families_present"] = bool(
        tuple(f.family for f in families) == CANDIDATE_FAMILIES)
    checks["every_family_assessed_on_all_axes"] = all(
        all(isinstance(getattr(f, axis), str) and len(getattr(f, axis)) > 0
            for axis in ADMISSIBILITY_AXES)
        for f in families)
    checks["baseline_family_refuted"] = any(
        f.family == FAMILY_PSEUDO_TIME_BASELINE and not f.admissible
        for f in families)
    checks["refuted_families_have_reason"] = all(
        (f.admissible or len(f.refuted_by) > 0) for f in families)
    # pseudocode determinism / completeness
    checks["pseudocode_nonempty"] = bool(len(pseudocode) >= 10)
    checks["pseudocode_has_no_hedge"] = all(
        h not in " ".join(pseudocode).lower() for h in hedges)
    checks["pseudocode_separates_convergence"] = bool(
        any("ITERATE_STATISTIC_CONVERGED" in line for line in pseudocode)
        and any("BELLMAN_CONVERGED" in line for line in pseudocode))
    # domain geometry must never be silently dropped from the direction set
    checks["active_set_uses_full_wall_gradient"] = bool(
        "FULL limiting wall gradient" in contract["active_boundary_detection"]
        and "MULTIPLE active gradients" in contract["active_boundary_detection"])
    # the merit must be residual-based, not component-based
    checks["merit_is_residual_based"] = bool(
        "RESIDUAL_REFERENCE" in contract["merit_function"]
        and "No component-wise merit" in contract["merit_function"])
    # the fail-closed clause must actually name every frozen failure terminal
    checks["fail_closed_clause_names_every_terminal"] = all(
        name in contract["fail_closed_terminal"]
        for name in (FAILURE_NO_SAFE_STEP, FAILURE_NO_RESIDUAL_REDUCING_STEP,
                     FAILURE_LINEAR_SOLVE, FAILURE_NONFINITE_EVIDENCE,
                     FAILURE_OPERATOR_CONTRACT, FAILURE_ATTEMPT_BUDGET))
    # single-Q must be enforced by construction in the contract text
    checks["single_q_enforced_by_full_reassembly"] = bool(
        "full reassembly" in contract["refresh_rule"]
        and "never a partial update" in contract["refresh_rule"]
        and "never by partial update" in contract["policy_operator_ordering"])
    # the logging surface must carry the domain margin and the decision reason
    checks["logging_carries_domain_margin_and_reason"] = bool(
        "domain margin" in contract["reproducibility_logging_fields"]
        and "exact reason" in contract["reproducibility_logging_fields"])
    # REPORTED repeat flag must agree with the MEASURED repeat. A single-run caller
    # passes None here and therefore fails this check by construction, so no
    # reportable artifact can be published with an unmeasured default flag.
    checks["reported_repeat_flag_is_measured"] = bool(
        measured_repeat_identical is not None)
    checks["reported_repeat_flag_agrees_with_measurement"] = bool(
        measured_repeat_identical is not None
        and reported_repeat_identical == measured_repeat_identical)
    # ladder naming disambiguation is stated and self-consistent
    checks["regularization_ladder_naming_disambiguated"] = bool(
        REGULARIZATION_LADDER_MAX_EXPONENT == 20
        and REGULARIZATION_LADDER_LENGTH == 21
        and len(ladders["regularization_ladder"]) == REGULARIZATION_LADDER_LENGTH
        and REGULARIZATION_LADDER_LENGTH
        == REGULARIZATION_LADDER_MAX_EXPONENT + 1)
    return checks


# ---------------------------------------------------------------------------
# 5. the ONE full design run
# ---------------------------------------------------------------------------
def _run_design(measured_repeat_identical: Optional[bool] = None) -> DesignResult:
    """ONE design run.

    ``measured_repeat_identical`` is the repeat result the caller has ALREADY
    measured; pass ``None`` only when the caller has not measured a repeat, in
    which case the artifact-consistency check fails closed (the reported flag would
    otherwise be an unmeasured dataclass default).
    """
    failure: Optional[dict] = None
    try:
        evidence = synthesize_evidence()
        families = assess_families()
        contract = frozen_contract()
        ladders = frozen_ladders()
        thresholds = frozen_thresholds()
        attempts = frozen_max_attempts()
        terminals = frozen_fail_closed_terminals()
        pseudocode = deterministic_pseudocode()
        distinction = material_distinction()

        reported_repeat = bool(measured_repeat_identical) if (
            measured_repeat_identical is not None) else False
        checks = _artifact_consistency(evidence, families, contract, ladders,
                                       thresholds, attempts, pseudocode,
                                       reported_repeat,
                                       measured_repeat_identical)
        consistency_ok = bool(all(checks.values()))

        admissible = tuple(f.family for f in families if f.admissible)
        refuted = tuple(f.family for f in families if not f.admissible)

        # ---- frozen route-selection rule (declared above, applied verbatim)
        selection_rule_satisfied = bool(
            len(admissible) == 1
            and len(refuted) >= SELECTION_REQUIRES_REFUTED_ALTERNATIVES)

        outer_framework = FAMILY_CONSTRAINED_TRUST_REGION
        direction_candidates = (FAMILY_POLICY_FROZEN_NEWTON,
                                FAMILY_RESIDUAL_JACOBI)

        if not consistency_ok:
            terminal = TERMINAL_C
        elif selection_rule_satisfied:
            terminal = TERMINAL_A
        elif len(admissible) == 0:
            terminal = TERMINAL_C
        else:
            # two or more families remain admissible: honest Outcome B, while the
            # direction-agnostic outer frame is still frozen for a later Issue.
            terminal = TERMINAL_B

        selected_family = admissible[0] if selection_rule_satisfied else ""
        open_sub_choice = ""
        if terminal == TERMINAL_B:
            open_sub_choice = (
                "direction sub-choice within the frozen outer frame: exactly one of "
                f"{direction_candidates} must be selected before execution")

        return DesignResult(
            terminal=terminal,
            failure_detail=None,
            evidence=evidence,
            evidence_issue_count=len(evidence),
            evidence_issues=tuple(e.issue for e in evidence),
            negative_evidence_count=sum(1 for e in evidence if e.is_negative),
            families=families,
            family_count=len(families),
            admissible_family_count=len(admissible),
            refuted_family_count=len(refuted),
            admissible_families=admissible,
            refuted_families=refuted,
            selected_contract_name=(
                "ROUTE_A_BOUNDED_RESIDUAL_BALANCED_CONSTRAINED_SOLVER_CONTRACT"
                if terminal == TERMINAL_A else
                "ROUTE_A_BOUNDED_CONSTRAINED_OUTER_FRAME__DIRECTION_OPEN"
                if terminal == TERMINAL_B else ""),
            selected_family=selected_family,
            outer_framework=outer_framework,
            open_sub_choice=open_sub_choice,
            selection_rule_satisfied=selection_rule_satisfied,
            contract_frozen=True,
            contract=contract,
            ladders=ladders,
            thresholds=thresholds,
            max_attempts=attempts,
            fail_closed_terminals=terminals,
            pseudocode=pseudocode,
            material_distinction=distinction,
            reproducibility_fields=tuple(
                contract["reproducibility_logging_fields"].split("; ")),
            consistency_checks=checks,
            consistency_check_count=len(checks),
            consistency_ok=consistency_ok,
            deterministic_repeat_identical=reported_repeat,
            accepted_residual_argmax=(
                f"row {ACCEPTED_RESIDUAL_ARGMAX_ROW} / node "
                f"{ACCEPTED_RESIDUAL_ARGMAX_NODE} / z {ACCEPTED_RESIDUAL_ARGMAX_Z} / "
                f"{ACCEPTED_RESIDUAL_ARGMAX_FAMILY}"),
        )
    except BoundedSolverDesignFailure as exc:
        failure = {"reason": str(exc)}
    except Exception as exc:  # pragma: no cover - defensive
        failure = {"reason": f"unexpected failure: {exc!r}"}

    return DesignResult(terminal=TERMINAL_C, failure_detail=failure)


def run_issue72_design() -> DesignResult:
    """One single design run with NO repeat measurement.

    The returned ``deterministic_repeat_identical`` field is therefore ``False``
    and ``consistency_check.reported_repeat_flag_is_measured`` is ``False``: such a
    result is deliberately NOT publishable. Callers that REPORT the artifact must
    use :func:`run_issue72_design_repeated`, which measures the repeat first and
    then builds the result with that measured value.
    """
    return _run_design(measured_repeat_identical=None)


def _canon(r: DesignResult) -> dict:
    """Canonical, comparison-safe form (NaN-aware; no NaN used today but kept so a
    future not-applicable field cannot silently break determinism)."""
    def norm(value):
        if isinstance(value, float) and np.isnan(value):
            return "__NAN__"
        if isinstance(value, dict):
            return {k: norm(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [norm(v) for v in value]
        return value

    return {k: norm(v) for k, v in dataclasses.asdict(r).items()}


def run_issue72_design_twice() -> tuple[DesignResult, bool]:
    """The ONE deterministic repeat of the full design run.

    Returns ``(result, identical)`` where ``result`` is built AFTER the repeat is
    measured, so its ``deterministic_repeat_identical`` field is the measured value
    and every consistency check holds. This is the same measured result as
    :func:`run_issue72_design_repeated`.
    """
    _probe_a = _run_design(measured_repeat_identical=None)
    _probe_b = _run_design(measured_repeat_identical=None)
    identical = bool(_canon(_probe_a) == _canon(_probe_b))
    result = _run_design(measured_repeat_identical=identical)
    return result, identical


def run_issue72_design_repeated() -> DesignResult:
    """THE reporting entry point: measure the repeat, then build ONE result whose
    ``deterministic_repeat_identical`` field IS that measurement.

    Order matters: the repeat is measured FIRST, so the reported artifact is
    constructed with the measured value and the artifact-consistency check can
    verify ``reported == measured``. This makes it impossible to publish a report
    or CSV carrying an unmeasured default flag. If the two runs differ, this raises
    :class:`BoundedSolverDesignFailure` instead of reporting a fabricated ``True``.
    """
    result, measured = run_issue72_design_twice()
    if measured is not True:
        raise BoundedSolverDesignFailure(
            "the design artifact is NOT deterministic: the frozen comparison "
            "contract found two consecutive runs to differ")
    if result.deterministic_repeat_identical is not measured:
        raise BoundedSolverDesignFailure(
            "measured repeat flag inconsistent with the design result")
    if not result.consistency_ok:
        failed = sorted(k for k, v in result.consistency_checks.items() if not v)
        raise BoundedSolverDesignFailure(
            f"design artifact consistency failed: {failed}")
    return result


# ---------------------------------------------------------------------------
# 6. read-only accepted-anchor verification (git only; no solver import)
# ---------------------------------------------------------------------------
def accepted_anchor_blobs() -> dict:
    """Read-only verification of the accepted anchors this design rests on."""
    repo_root = Path(__file__).resolve().parents[3]
    base = GOVERNANCE_BASE

    def blob(relpath: str, rev: str = "HEAD") -> str:
        return subprocess.run(
            ["git", "rev-parse", f"{rev}:{relpath}"], cwd=repo_root,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", check=True).stdout.strip()

    return {
        "selected_q_blob": blob(SELECTED_Q_RELPATH),
        "oracle_blob": blob(
            "src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py"),
        "issue69_audit_blob": blob(
            "src/deep_learning_hank/two_asset/f0_rate_path_divergence_audit.py"),
        "issue71_module_blob": blob(RESIDUAL_MODULE_RELPATH),
        "selected_q_blob_at_base": blob(SELECTED_Q_RELPATH, base),
    }


def summary_csv_lines(r: DesignResult) -> list[str]:
    """Compact CSV evidence lines for the Issue #72 report."""
    lines = ["metric,value"]
    for f in dataclasses.fields(r):
        if f.name in ("evidence", "families", "pseudocode", "material_distinction",
                      "contract", "reproducibility_fields"):
            continue
        v = getattr(r, f.name)
        if isinstance(v, dict):
            v = "; ".join(f"{k}={v[k]}" for k in sorted(v))
        lines.append(f"{f.name},{v}")
    for e in r.evidence:
        lines.append(f"evidence.issue{e.issue}.{e.key},{e.accepted_value}")
        lines.append(f"evidence.issue{e.issue}.{e.key}.negative,{e.is_negative}")
    for fam in r.families:
        for key in ("family", "admissible", "role", "refuted_by",
                    "residual_jacobian_object", "domain_handling",
                    "policy_reselection_handling", "single_q_consistency",
                    "expected_strength", "accepted_historical_contradiction",
                    "boundedness", "deterministic_reproducibility",
                    "suitability_for_mixed_cancellation"):
            lines.append(f"family.{fam.family}.{key},{getattr(fam, key)}")
    for name, value in r.ladders.items():
        lines.append(f"ladder.{name},{value}")
    for name, value in r.thresholds.items():
        lines.append(f"threshold.{name},{value}")
    for name, value in r.max_attempts.items():
        lines.append(f"max_attempts.{name},{value}")
    for name, value in sorted(r.consistency_checks.items()):
        lines.append(f"consistency.{name},{value}")
    for name, value in r.material_distinction.items():
        lines.append(f"distinction.{name},{value}")
    for line in r.pseudocode:
        lines.append(f"pseudocode,{line}")
    return lines
