# DLH-5V-H — Terminal and Forbidden Check (Micro-Rev Rev 2)

**Issue:** #56 / DLH-5V-H — State-Constraint HJB Boundary-Consistency Target Audit (Route E)
**Micro-Rev Rev 2:** Reviewer comment `5642335215` — `DLH_5VH_OUTCOME_B_NOT_YET_ACCEPTED__LOCAL_STATE_CANDIDATE_BRIDGE_AND_HALF_RELAXED_QUANTIFIER_FIX_REQUIRED`; bounded same-Issue/same-branch revision on top of Rev 1 `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d`.

---

## 1. Exactly one terminal (Rev 2)

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

**Verdict rationale (one paragraph):** Rev 2 repairs the two load-bearing proof defects found in Rev 1. (1) The half-relaxed-limit derivation no longer infers per-candidate inequalities from a max: the contact step holds candidatewise, the outer max is retained, the Taylor expansion is performed candidatewise inside the max, and the limit object is H_lim = limsup of the discrete Bellman Hamiltonians at the visited states; both the subsolution and supersolution directions are corrected, and the boundary subsolution on the closure w.r.t. the full Hamiltonian H_proj is obtained in both branches via the restriction H_m(s_m, p) ≤ H_proj(s_m, p) → H_proj(x̂, p) (buffered candidate sets ⊆ full candidate sets; Hausdorff convergence of the feasibility bounds) — WITHOUT the constrained characterization ρV ≤ H_T. (2) The W-contact control/payoff bridge is rewritten as a genuine local-state same-candidate recovery lemma: for every viable control at a corner/face limit point, explicit α_m at the actual states s_m (strict controls: α_m = α eventually, by the source-verified drift continuity; tangent controls: explicit inward perturbations c → c + δ_m / d → d − ε_m, with the lower-corner a-side tangent handled by the formula r_a_eff(a) ≥ 0), ALL rates computed from μ(s_m, α_m) with EXACT first moment and O(1/m) second moment (exact-arithmetic verified), respecting the binding law candidate → admissibility → local drift → rates → score → ONE argmax → ONE Q. The composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj holds at the corners/faces; the triple corner (W_max = 8) is treated with the Case-B forward/left contract (i = 9, no mirror). The raw Issue-#55 graph target remains shown over-strong (sufficient, not necessary) for the operator-consistency components, scoped strictly to the Barles–Souganidis operator structure, the corrected toy, and the corrected half-relaxed-limit algebra. **One bounded block remains**, declared explicitly: the project-specific application of the state-constraint comparison/unique-continuation theorem for the project's continuous limit problem, with the constrained characterization ρV ≤ H_T at the boundary as a tightly coupled sublemma of the same block (not established; not load-bearing for the transfer). Per the Reviewer's own instruction, the gap is returned as Outcome B rather than carried into the next gate; Outcome A is not authorized by the current evidence.

---

## 2. Forbidden-operation check

| Forbidden operation | Status |
|---|---|
| Household / economic / D_W mutation | NOT performed (blob re-verified: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`) |
| Grid / aspect / state-family redesign, state augmentation, coordinate transformation | NOT performed (frozen geometry consumed; taxonomy relabeled, not redesigned) |
| Numerical production W_max | NOT used (W_max symbolic; W_max ∈ {8, 10, 12} only in scratch enumeration) |
| Implementation / solver-source mutation | NOT performed (no source files touched) |
| Production-Q assembly/run, HJB/KFE/stationary solve | NOT performed |
| KFE-only repair, pin/normalization leakage repair | NOT performed |
| Aggregates / GE / multi-region / neural / nominal / calibration / policy / welfare / Results | NOT performed |
| PR / merge / close / successor / self-accept | NOT performed (same branch amended; STOP for fresh ChatGPT review) |
| Stationary KFE | NOT AUTHORIZED, NOT performed |
| Copyrighted theory PDFs / long quotations in repo | NOT committed (metadata/DOI + concise standard-content statements only) |
| Silent revision of Issue #54 / #55 accepted verdicts | NOT performed (both consumed; the necessity question is answered, not their verdicts revised) |
| New Issue / new branch / branch reset / discard of candidates `bc281a6` / `5d1e482` | NOT performed (Rev-2 commit is on top of `5d1e482` on the SAME branch) |

## 3. Rev-2 deliverables checklist (Reviewer comment `5642335215`)

| Reviewer item | Status |
|---|---|
| 1. Correct the §D.2 max/quantifier argument | DONE — max retained throughout; no per-candidate inference; both directions corrected; H_lim = limsup of the discrete Bellman Hamiltonians (monotone-scheme report §D.2) |
| 2. Rewrite §E.4 with actual local-state drifts μ(s_m, α_m) and prove a genuine local-candidate recovery bridge, or explicitly downgrade it into the gap | DONE — recovery lemma PROVED at the design level (strict: α_m = α eventually; tangent: explicit δ_m/ε_m inward perturbations; rates from μ(s_m, α_m); exact first moment; O(1/m) second moment; source-verified drift continuity H1–H3) |
| 3. Do not count finite enumeration as proof of local-control recovery | DONE — enumeration explicitly labeled as supplementing destination availability only (§E.4 preamble, §E.5) |
| 4. Keep the corrected Soner sign transform, H_T downgrade, monotonicity, taxonomy, and physical-drift units | DONE — preserved verbatim in the package |
| 5. Re-evaluate the terminal honestly; Outcome B available if one bounded project-specific boundary-consistency/comparison theorem gap | DONE — Outcome B with the narrowed single block (comparison/unique-continuation application + coupled constrained-characterization sublemma); Outcome A NOT claimed |

## 4. PROVED / UNRESOLVED ledger (matches the evidence)

**PROVED:** Soner sign mapping (explicit transform); raw graph condition non-necessity mechanism (BS operator structure + corrected toy + corrected half-relaxed-limit algebra — not via the 2D boundary transfer); monotonicity (order-preserving scaled operator, M-matrix residual, no ρ ≥ Σq); stability (max-principle ‖u_m‖∞ ≤ ‖g‖∞/ρ); interior consistency; stencil destination availability; finite-m rate algebra conditional on a locally admissible candidate; **local-state same-candidate recovery (strict + tangent)**; boundary subsolution transfer on the closure w.r.t. H_proj (both branches, restriction argument); interior supersolution; composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj at the corners/faces.

**UNRESOLVED (the single bounded Outcome-B block):** project-specific state-constraint comparison/unique-continuation applicability for the project's continuous limit problem; constrained characterization ρV ≤ H_T at the boundary (coupled sublemma of the same block; not needed for the transfer).

## 5. Fresh-state evidence (at candidate time)

- Fresh live `main`: `5d38c644ec1a06359241f9c3418dcd815c938ec6` (fresh fetch; unchanged).
- Issue #56: OPEN; task type `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`; activation comments `5641527846`, `5641534701`; first Micro-Rev comment `5641997550`; latest Reviewer comment `5642335215`; authority marker `DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT_AUTHORIZED`.
- Previous candidates: `bc281a693b2d9281b6e180bc62996d503dfab7fe` (Rev 0), `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` (Rev 1; kept; Rev 2 on top).
- Household blob: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` ✓ (drift formulas re-verified from source lines 80–157 for the recovery lemma).
- Only the six allowlist paths modified; staged explicitly; remote SHA = local SHA verified after push.

## 6. Companion reports (this package)

- `DLH_5VH_AUTHORITY_AND_PRIMARY_THEORY_CAPSULE.md` (B: provenance, sign mapping, H_T downgrade, status labels, Rev-2 ledger)
- `DLH_5VH_CONTINUOUS_STATE_CONSTRAINT_HJB_AND_VISCOSITY_TARGET.md` (A: continuous target, Soner transform, H_T auxiliary, boundary transfer)
- `DLH_5VH_STRONG_GRAPH_TARGET_NECESSITY_AUDIT.md` (C: trichotomy — over-strong; operator-level restatement; raw-graph scoping)
- `DLH_5VH_MONOTONE_SCHEME_BOUNDARY_CONSISTENCY_AND_FROZEN_PROCESS_TEST.md` (D+E+F: corrected quantifier, recovery lemma, toy)
- `docs/theory/DLH_5VH_STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET_AUDIT.md` (umbrella)
