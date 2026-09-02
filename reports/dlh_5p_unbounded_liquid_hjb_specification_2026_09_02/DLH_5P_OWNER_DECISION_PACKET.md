# DLH-5P Phase G — Owner Decision Packet (Rev 4)

**Issue #42 Phase G (Rev 4).** Compares S1/S2/S3 for the Owner decision. Builder may
recommend a candidate, but the recommendation is **not a model freeze**; the Owner
remains final authority for any model-defining analytic specification. No
recommendation creates accepted analytic-model authority. Rev 4 reflects the Rev 3
corrections (S1 derived global boundedness, S2 tail-value selection `V_inf = 0` with
the discounted-value condition vacuous under S1, S3 excluding `m=1/2` by class without
proving the realized tail is `p=2`) plus the **Rev 4 sign correction** of the
critical-branch `O(1/b)` equation (transfer Hamiltonian enters the HJB positively;
`c/b = (rho+r_b + 0.5 C/chi_1)/2`; `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0`, inward).

## G1. Comparison across the required axes (Rev 4)

| Axis | S1 (minimal) | S2 (tail-value selection) | S3 (derivative-controlled) |
|---|---|---|---|
| **Economic interpretation** | continuous extension of the accepted interior economics; no tail law; `V_inf` free in `[-C,0]` | adds explicit tail-value vanishing `V_inf = 0` (assumption, not proved necessity; distinct from asset no-Ponzi) | adds a bounded/sub-root transfer-ratio admissible class (bounded-transfer rationale is motivation, not derivation) |
| **Faithfulness to accepted household economics** | high (interior economics only) | high (value-level tail selection; necessity unproved) | high (uses the accepted transfer FOC and adjustment cost; the class is an admissibility restriction, not a modification) |
| **Boundedness of admissible V** | **derived** (monotone in `b`, `V_b>0`, `V<0`, finite `b_lo`, compact `a,z` => globally bounded) | inherited from S1 | inherited from S1 |
| **New model authority introduced** | state-space extension + class (A14, A18); `b_lo=-2` analytic adoption (step 24) | + `V_inf = 0` tail-value selection (new model definition; no necessity claim) | + derivative-control class (A21 as an Owner-adopted primitive) |
| **Risk of circularly assuming the desired `p=2` result** | none | low | explicit: the class excludes the `m=1/2` family; `p=2` uniqueness is imposed by the primitive, not derived (and still not a proved realized-tail statement) |
| **Mathematical tractability** | high but underdetermined (no uniqueness) | medium (level selection; `R` uncontrolled) | medium-high (class gives the coefficient, conditional on full DLH-5O premises) |
| **Treatment of P-TR** | not assumed, not derived | not derived (tail-value selection does not control `R`) | Owner-adopted primitive; preferred `R=O(1)`; excludes `m=1/2` by class; does NOT prove realized tail is `p=2` |
| **Treatment of critical `m=1/2` branch** | admissible/unresolved | admissible/unresolved (`V_inf=0` family passes) | excluded only by the adopted class |
| **Uniqueness of the tail coefficient** | NOT unique (family; `m=1/2` admissible) | NOT unique (branch admissible) | `m=1/2` excluded by primitive; **actual tail uniqueness remains to be proved** |
| **`mu_W/b` sign of the critical family** | n/a (no tail law) | n/a (level selection only) | n/a (class excludes it); outside the class, `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` (inward; no mean-reversion reversal) |
| **Compatibility with later HJB<->KFE same-process requirements** | compatible (same interior process) | compatible (same-process value-selection) | compatible (same-process; the class restricts the value gradient, not the process) |
| **Compatibility with eventual R/W domain design** | neutral (no domain authority) | neutral | neutral (a tail admissibility class does not select R/W/`W_max`) |
| **Falsifiability and reproducibility** | falsifiable (m=1/2 family is a live counterexample class) | falsifiable | falsifiable (Phase F F2.1-F2.5); exclusionary cost is explicit |

## G2. Builder recommendation (Rev 4)

**Recommendation B — the critical transfer branch remains admissible, so the tail /
analytic coefficient specification is not unique under S1/S2; uniqueness is only
available through an explicit Owner-adopted S3/P-TR primitive (and even then the
realized-tail statement must be proved, Phase F), or through a future Phase F
resolution.**

```text
DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED
```

Rationale:

1. The Rev 1 ruling-out of the `m=1/2` branch is **withdrawn** (reviewer
   `5504929967`); the branch is realizable by the remainder-derivative mechanism with
   Clairaut satisfied for arbitrary `p`, and for the `p=2` base yields the altered
   system `(rho+r_b)K - 2 sqrt(K) = S*K - 0.5*C*K/chi_1` (sign corrected in Rev 4:
   `L = -(2/3)M_a/K`, `C = aL^2`), coherent on the compact interior with
   `L ~ a^{-1/2}` families and a continuum of consumption ratios
   `c/b = (rho+r_b + 0.5 C/chi_1)/2`.
2. Under S1 and S2 the branch is **admissible/unresolved**; neither candidate selects a
   unique tail coefficient. (S2's `V_inf = 0` selection is genuine for the level but
   does not control `R`; the family passes it.)
3. Under S3 the `p=2` coefficient is available **only** because the class excludes the
   branch — and even then it is conditional on the full DLH-5O theorem premise set and
   the realized-tail statement remains to be proved (Phase F). This is legitimate
   **if the Owner adopts the primitive knowingly**, but it is not an independent
   derivation.
4. **Mean-reversion sign is NOT unresolved:** the demonstrated compact-interior critical
   family has `mu_W/b = -0.0025 - 3C/(4 chi_1) < 0` (inward) for `C >= 0` because the
   adjustment cost is `O(b)` (`chi/b = 0.5 C/chi_1`). Recommendation B therefore means
   "tail coefficient / analytic specification non-unique" — it does **NOT** mean
   "mean-reversion sign unresolved." No branch with `mu_W/b >= 0` is demonstrated.

**Caveats to the Owner:** adopting S3/P-TR (or `R=O(1)`) is
`NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER` (A21); it excludes the `m=1/2` family by
class and does not prove the realized tail is `p=2`. A full-`[0,10]` uniform theorem
requires the `a_max` upper-`a` endpoint law (Phase C). No freeze is implied.

## G3. Exact recommendation terminal (exactly one)

```text
DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED
```

**Why Recommendation B and not A/C/Blocked:**

- **Not A** (`DLH_5P_ANALYTIC_HJB_SPECIFICATION_CANDIDATE_READY__OWNER_MODEL_DEFINITION_DECISION_REQUIRED`):
  Recommendation A in Rev 1 rested on the (invalid) claim that the `m=1/2` branch is
  ruled out and hence the tail is unique. With that claim withdrawn, no candidate is
  "ready" with a proved unique tail: S1/S2 are non-unique, and S3 is unique only via an
  explicitly adopted primitive whose realized-tail statement remains unproved. An
  A-with-explicit-Owner-imposed-S3 variant is available only after the Owner opts into
  the primitive and the Phase F gates are met.
- **Not C** (`DLH_5P_ANALYTIC_HJB_SPECIFICATION_EVIDENCE_INSUFFICIENT__OWNER_DECISION_REQUIRED`):
  the evidence is sufficient to characterize the options precisely (S1/S2 non-unique,
  S3 unique-by-primitive, `m=1/2` branch admissible and balance-consistent with inward
  `mu_W`); the decision is an Owner judgment between imposing the primitive and funding
  the Phase F resolution, not a lack of evidence.
- **Not Blocked** (`BLOCKED_DLH_5P_ACCEPTED_ECONOMICS_OR_AUTHORITY_INCONSISTENCY`):
  no accepted-economics or authority inconsistency was found; the accepted source and
  DLH-5N/DLH-5O packages are internally consistent and unchanged.

**What the recommendation does and does not do:** it reports that the critical branch
remains admissible, the tail/analytic coefficient specification is not unique without an
Owner-adopted primitive, and — importantly — the demonstrated critical family still has
inward `mu_W/b < 0` (so mean-reversion sign is not part of the non-uniqueness). It does
NOT freeze, implement, or adopt the specification, does NOT select R/W/W1/W2/`W_max`,
does NOT create HJB/domain/stationary authority, and does NOT close the Issue.

## G4. Illustrative Owner decision paths (for reference, not binding)

1. **Adopt S3 primitive (path A):** "Adopt S3 with the derivative-control class
   `R=O(1)` (preferred) / P-TR fallback, plus S2's tail-value selection `V_inf = 0`,
   as the fixed-`a` unbounded-liquid analytic HJB specification; uniqueness of the `p=2`
   coefficient is thereby imposed by the adopted primitive, and the Phase F theorem
   gates (existence/comparison/regularity/uniformity/asymptotic realization/coefficient
   convergence) are opened to prove the realized tail."
2. **Fund resolution (path B):** "Keep S1/S2 as the candidate base; open a research
   gate to resolve the `m=1/2` branch (complete its asymptotic series, test the
   `V_inf=0` selection, and determine whether it is realized) before any coefficient is
   adopted."
3. **Both:** adopt S3 provisionally while funding the Phase F resolution to test
   whether the primitive is justified.

These paths are illustrative only; the Owner retains final authority.
