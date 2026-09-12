# DLH-5V-H — Terminal and Forbidden Check (Micro-Rev Rev 4)

**Issue:** #56 / DLH-5V-H — State-Constraint HJB Boundary-Consistency Target Audit (Route E)
**Micro-Rev Rev 4:** Reviewer comment `5642868947` — `DLH_5VH_OUTCOME_B_NOT_ACCEPTED__FALSE_GLOBAL_BUDGET_FEASIBILITY_AND_HAMILTONIAN_EFFECTIVE_DOMAIN_FIX_REQUIRED`; bounded same-Issue/same-branch revision on top of Rev 3 `dd3aa425a869a2d5a09835efc667c4ff1c2bb5b3`.

---

## 1. Exactly one terminal (Rev 4)

`DLH_5VH_THEORY_AUDIT_PARTIAL__ONE_BOUNDED_BOUNDARY_CONSISTENCY_OR_COMPARISON_GAP_REMAINS`

**Verdict rationale (one paragraph):** Rev 4 removes the false global static-budget compactification and re-audits the true Hamiltonian. (1) **True control domain:** the full interior controls are c > 0, l ≥ 0, d ∈ R with the source-exact drift μ_b = r_b·b + labor_income − d − χ(d,a) − c; the Rev-3 inequality c + χ + d ≤ y + r_b·b + τ is removed (it is μ_b ≥ 0, a tangent law only at b = b_min — the accepted W-boundary sectors explicitly contain R_reverse/R_deplete with μ_b < 0); τ is the wage wedge inside effective wages, not additive resources; no hard l_max/d_min/d_max bounds are installed; the Hamiltonian is written with sup until attainment is proved. (2) **Effective-domain audit (exact, frozen γ_c = 2):** H_proj(x,p) < ∞ ⟺ p_b > 0 or (p_b = 0, p_a = 0); H_proj = +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0} — the consumption term u(c) − p_b·c is coercive only for p_b > 0 (γ_c = 2), the transfer term (p_a−p_b)d − p_b·χ(d,a) is quadratically coercive for p_b > 0 and quadratically POSITIVE (sup = +∞) for p_b < 0. (3) **Local effective compactness (PROVED — the preferred route):** on compact gradient sets K_p ⊂ {p_b ≥ η > 0}, the FOC-derived maximizers (c* = p_b^{−1/2}, l_j* = (p_b·net_wage_j·z/ω_j)^{1/φ}, |d*| ≤ (s/χ_1)(|p_a−p_b|/η + χ_0)) lie in a common compact effective optimizer set; sup = max there; |μ| ≤ M. (4) **Hamiltonian regularity (PROVED on the effective region):** H_proj jointly continuous/USC in (x,p) and Lipschitz in p; the uniform max second-moment bound O(1/m) holds with the SAME domain restriction (test gradients p_b ≥ η > 0). (5) **Boundary transfer (honest):** the restriction H_m ≤ H_proj is trivial on the true control set (buffered candidate set ⊆ full control set); the transfer is PROVED on {p_b ≥ η > 0} and overall CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY — the condition is the relevant-viscosity-gradient restriction (p_b ≥ η > 0), which the classical FOC cannot prove (it presumes V_b > 0) and which belongs to the Outcome-B block. (6) **Soner assumption mapping:** Soner Part I assumes a compact control space and bounded drift/running cost; the project's raw controls are not compact — whether the local effective compactification suffices to map the project into the theorem or an extension is required must be resolved; do not cite Soner as directly applicable until then. (7) **Tangent recovery:** preserved and re-audited against the true control domain (c > 0, l ≥ 0, genuine face laws only; no global μ_b ≥ 0, no budget) — all strict and all tangent controls at every family remain PROVED (exact-arithmetic verified). Outcome A is not authorized by the current evidence; the single bounded block is the Hamiltonian-effective-domain / state-constraint-comparison application block (relevant-viscosity-gradient restriction; Soner-II/CDL comparison applicability with the compact-control mapping; constrained H_T characterization as the coupled optional sublemma). **Outcome B.**

## 2. Forbidden-operation check

| Forbidden operation | Status |
|---|---|
| Household / economic / D_W mutation | NOT performed (blob re-verified: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`; χ/μ formulas re-read from source lines 80–157) |
| Turn μ_b ≥ 0 into a global constraint | NOT performed — the Rev-3 static-budget Γ is REMOVED |
| Add hard l/d bounds not in accepted authority | NOT performed — l_max/d_min/d_max not introduced as feasibility; bounds only derived effectively from the frozen objective |
| Grid / aspect / state-family redesign, state augmentation, coordinate transformation | NOT performed (frozen geometry consumed) |
| Numerical production W_max | NOT used (W_max symbolic; W_max ∈ {8, 10, 12} only in scratch enumeration) |
| Implementation / solver-source mutation | NOT performed (no source files touched) |
| Production-Q assembly/run, HJB/KFE/stationary solve | NOT performed |
| KFE-only repair, pin/normalization leakage repair | NOT performed |
| Aggregates / GE / multi-region / neural / nominal / calibration / policy / welfare / Results | NOT performed |
| PR / merge / close / successor / self-accept | NOT performed (same branch amended; STOP for fresh ChatGPT review) |
| Stationary KFE | NOT AUTHORIZED, NOT performed |
| Copyrighted theory PDFs / long quotations in repo | NOT committed (metadata/DOI + concise standard-content statements only) |
| Silent revision of Issue #54 / #55 accepted verdicts | NOT performed (both consumed; the necessity question is answered, not their verdicts revised) |
| New Issue / new branch / branch reset / discard of Rev 0–3 candidates | NOT performed (Rev-4 commit is on top of `dd3aa42` on the SAME branch) |

## 3. Rev-4 deliverables checklist (Reviewer comment `5642868947`)

| Reviewer item | Status |
|---|---|
| 1. Remove the global static inequality c + χ + d ≤ … from the full interior control correspondence | DONE — removed; the true domain is c > 0, l ≥ 0, d ∈ R; no state-drift restriction outside the active faces |
| 2. Do not introduce unsupported l_max, d_min, d_max as frozen economics | DONE — no hard bounds installed; optimizer bounds derived EFFECTIVELY from the frozen objective (§D.4.2) |
| 3. Define the true full control domain from accepted authority; use sup, not max, until attainment/effective compactness is proved | DONE — H_proj written with sup; the sup becomes max only on the effective region where attainment is proved |
| 4. Analyze the Hamiltonian effective domain honestly (p_b > 0 / p_b = 0 / p_b < 0, consumption + quadratic-transfer terms) | DONE — exact statements for the frozen specification: finite ⟺ p_b > 0 or (p_b = 0, p_a = 0); +∞ on {p_b < 0} ∪ {p_b = 0, p_a ≠ 0} |
| 5. Prove a local effective-compactness/coercivity lemma for gradients in a compact set with p_b ≥ η > 0; derive local continuity/USC and the uniform second-moment bound there | DONE — Lemma (§D.4.2): common compact K_alpha(K_p) from FOC-derived bounds; H_proj joint continuity/USC and Lipschitz in p; uniform O(1/m) max moment with the same restriction |
| 6. Either prove the relevant test gradients lie in the effective domain or leave this in the Outcome-B block | DONE — left in the Outcome-B block (routes A–D documented; the classical FOC presumes V_b > 0 and is not a proof) |
| 7. Re-state boundary transfer as PROVED only on the proved gradient region; otherwise CONDITIONAL | DONE — PROVED on {p_b ≥ η > 0}; overall CONDITIONAL_ON_EFFECTIVE_DOMAIN_REGULARITY |
| 8. Preserve the exact-χ tangent-recovery work unless a fresh contradiction appears | DONE — preserved; re-audited against the true control domain; no contradiction found; ledger unchanged (all PROVED) |
| 9. τ / transfer-income correction | DONE — τ is the wage wedge inside effective wages; no additive τ in μ_b; transfer_income named separately only if ever authorized (none introduced) |
| 10. Terminal discipline / honest ledger | DONE — Outcome B; PROVED/UNRESOLVED ledger matches the evidence; the Soner compact-control assumption mapping is explicitly not assumed |

## 4. PROVED / UNRESOLVED ledger (matches the evidence)

**PROVED:** Soner sign mapping (explicit transform); raw-graph non-necessity mechanism (BS operator structure + corrected toy + corrected half-relaxed-limit algebra — never via the unresolved block); monotonicity (order-preserving scaled operator, M-matrix residual, no ρ ≥ Σq); stability (max-principle); interior consistency; stencil destination availability; finite-m rate algebra conditional on a locally admissible candidate; local-state same-candidate recovery (ALL strict and ALL tangent controls at every family, exact χ algebra, TRUE control domain); TRUE Hamiltonian effective domain (exact by p_b sign for the frozen γ_c = 2); local effective compactness/coercivity on compact K_p ⊂ {p_b ≥ η > 0} (FOC-derived c/l/d bounds, sup = max, |μ| ≤ M); H_proj joint continuity/USC and Lipschitz in p on the effective region; uniform O(1/m) max second-moment bound with the same domain restriction; boundary subsolution transfer on the closure w.r.t. H_proj on the effective gradient region (trivial restriction + USC + recovery); interior supersolution; composite H_T ≤ liminf H_R ≤ limsup H_R ≤ H_proj on the effective region.

**UNRESOLVED (the single bounded Outcome-B block):** (i) relevant-viscosity-gradient restriction — test functions used by the state-constraint consistency/comparison arguments having p_b ≥ η > 0 (routes: value-monotonicity-in-b, Inada lower bound, effective-domain-formulated comparison — none established in scope; the classical FOC presumes V_b > 0); (ii) project-specific state-constraint comparison/unique-continuation applicability — including the Soner compact-control/mapping question (raw controls not compact; whether the local effective compactification suffices or an extension is required); (iii) constrained characterization ρV ≤ H_T at the boundary (coupled sublemma of the same block; not needed for the transfer).

## 5. Fresh-state evidence (at candidate time)

- Fresh live `main`: `5d38c644ec1a06359241f9c3418dcd815c938ec6` (fresh fetch; unchanged).
- Issue #56: OPEN; task type `SCIENTIFIC_THEORY_AUDIT__STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET`; activation comments `5641527846`, `5641534701`; Reviewer comments `5641997550`, `5642335215`, `5642677284`, `5642868947`; authority marker `DLH_5VH_ROUTE_E_STATE_CONSTRAINT_HJB_CONSISTENCY_TARGET_AUDIT_AUTHORIZED`.
- Previous candidates: `bc281a693b2d9281b6e180bc62996d503dfab7fe` (Rev 0), `5d1e4822dcc94aa16d30837e9c524baaefe5fa3d` (Rev 1), `52cfbf4cb4a1bcdb36bd77211869e8ac0f51b317` (Rev 2), `dd3aa425a869a2d5a09835efc667c4ff1c2bb5b3` (Rev 3; kept; Rev 4 on top).
- Household blob: `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` ✓ (χ/μ formulas re-verified from source lines 80–157; parameters validated: χ_0 ≥ 0, χ_1 > 0, a_bar > 0, γ_c = 2 frozen, φ = 5 frozen).
- Only the six allowlist paths modified; staged explicitly; remote SHA = local SHA verified after push.

## 6. Companion reports (this package)

- `DLH_5VH_AUTHORITY_AND_PRIMARY_THEORY_CAPSULE.md` (B: provenance, sign mapping, H_T downgrade, status labels, Rev-4 ledger)
- `DLH_5VH_CONTINUOUS_STATE_CONSTRAINT_HJB_AND_VISCOSITY_TARGET.md` (A: continuous target, Soner transform, H_T auxiliary, true control domain + effective-domain audit §3.5)
- `DLH_5VH_STRONG_GRAPH_TARGET_NECESSITY_AUDIT.md` (C: trichotomy — over-strong; operator-level restatement on the true domain; raw-graph scoping)
- `DLH_5VH_MONOTONE_SCHEME_BOUNDARY_CONSISTENCY_AND_FROZEN_PROCESS_TEST.md` (D+E+F: corrected quantifier, exact-χ recovery ledger on the true domain, effective-domain regularity, toy)
- `docs/theory/DLH_5VH_STATE_CONSTRAINT_HJB_BOUNDARY_CONSISTENCY_TARGET_AUDIT.md` (umbrella)
