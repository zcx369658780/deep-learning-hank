# DLH-5P Phase G — Owner Decision Packet (Rev 2)

**Issue #42 Phase G (Rev 2).** Compares S1/S2/S3 for the Owner decision. Builder may
recommend a candidate, but the recommendation is **not a model freeze**; the Owner
remains final authority for any model-defining analytic specification. No
recommendation creates accepted analytic-model authority.

## G1. Comparison across the required axes (Rev 2)

| Axis | S1 (minimal) | S2 (transversality) | S3 (derivative-controlled) |
|---|---|---|---|
| **Economic interpretation** | continuous extension of the accepted interior economics; no tail law; `V->0` NOT forced | adds a proposed discounted-value verification/selection condition (mapped to the household's own `rho`-discounting; necessity NOT proved) | adds a bounded/sub-root transfer-ratio admissible class (bounded-transfer rationale is motivation, not derivation) |
| **Faithfulness to accepted household economics** | high (interior economics only) | high (uses the household's own discounting; verification status is a hypothesis) | high (uses the accepted transfer FOC and adjustment cost; the class is an admissibility restriction, not a modification) |
| **New model authority introduced** | state-space extension + growth class (A14, A18); `b_lo=-2` analytic adoption (step 24) | + verification/selection condition (A15, needs Owner + proof of necessity) | + derivative-control class (A21 as an Owner-adopted primitive) |
| **Risk of circularly assuming the desired `p=2` result** | none | low | explicit: the class excludes the `m=1/2` family; `p=2` uniqueness is imposed by the primitive, not derived |
| **Mathematical tractability** | high but underdetermined (no uniqueness) | medium (level uniqueness via the condition, IF proved) | medium-high (class gives the coefficient theorem, conditional) |
| **Treatment of P-TR** | not assumed, not derived | not derived (condition does not control `R`) | Owner-adopted primitive; preferred `R=O(1)`; not independently justified by any ruling-out |
| **Treatment of critical `m=1/2` branch** | admissible/unresolved | admissible/unresolved | excluded only by the adopted class |
| **Uniqueness of the tail coefficient** | NOT unique (family; `m=1/2` admissible) | NOT unique (branch admissible; level only selected) | unique within the class, imposed by the primitive (not derived) |
| **Compatibility with later HJB<->KFE same-process requirements** | compatible (same interior process) | compatible (same-process value-selection) | compatible (same-process; the class restricts the value gradient, not the process) |
| **Compatibility with eventual R/W domain design** | neutral (no domain authority) | neutral | neutral (a tail admissibility class does not select R/W/`W_max`) |
| **Falsifiability and reproducibility** | falsifiable (m=1/2 family is a live counterexample class) | falsifiable | falsifiable (Phase F F2.1-F2.5); exclusionary cost is explicit |

## G2. Builder recommendation (Rev 2)

**Recommendation B — the critical transfer branch remains admissible, so the tail
specification is not unique under S1/S2; uniqueness is only available through an
explicit Owner-adopted S3/P-TR primitive (or a future Phase F resolution).**

```text
DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED
```

Rationale:

1. The Rev 1 ruling-out of the `m=1/2` branch is **withdrawn** (reviewer
   `5504929967`, Blocking corrections 1-2). The branch is realizable by the
   remainder-derivative mechanism (`V_b = K b^{-p} + M b^{-p-1/2} + ...`) with Clairaut
   satisfied for arbitrary `p`; for the `p=2` base it yields the altered system
   `(rho+r_b)K - 2 sqrt(K) = S*K + 0.5 a L^2 K/chi_1` (`L = -(2/3)M_a/K`), coherent on
   the compact interior with `L ~ a^{-1/2}` families and a continuum of coefficients
   `c/b != (rho+r_b)/2`.
2. Under S1 and S2 the branch is **admissible/unresolved**; neither candidate selects a
   unique tail coefficient.
3. Under S3 the `p=2` coefficient follows **only because the class excludes the
   branch** — uniqueness is imposed by an Owner-adopted admissibility primitive, not
   derived. That is scientifically legitimate **if the Owner adopts it knowingly**, but
   it is not an independent justification.
4. Therefore Recommendation A (candidate ready without relying on invalid uniqueness
   claims) is **not** available: the only uniqueness available is the conditional one
   under an explicit Owner-imposed S3/P-TR primitive, which Recommendation B states
   exactly.

**Caveats to the Owner:** adopting S3/P-TR (or `R=O(1)`) is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`
(A21); it excludes the `m=1/2` family by class, and its scientific cost should be
weighed (the bounded-transfer rationale is motivation, not proof). A full-`[0,10]`
uniform theorem requires the `a_max` upper-`a` endpoint law (Phase C). No freeze is
implied.

## G3. Exact recommendation terminal (exactly one)

```text
DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED
```

**Why Recommendation B and not A/C/Blocked:**

- **Not A** (`DLH_5P_ANALYTIC_HJB_SPECIFICATION_CANDIDATE_READY__OWNER_MODEL_DEFINITION_DECISION_REQUIRED`):
  Recommendation A in Rev 1 rested on the (invalid) claim that the `m=1/2` branch is
  ruled out and hence the tail is unique. With that claim withdrawn, no candidate is
  "ready" with uniqueness except S3-with-explicitly-imposed-P-TR, which is exactly the
  Owner-adoption scenario Recommendation B asks the Owner to decide. (An A-with-
  explicit-Owner-imposed-S3 variant is available only after the Owner opts into the
  primitive.)
- **Not C** (`DLH_5P_ANALYTIC_HJB_SPECIFICATION_EVIDENCE_INSUFFICIENT__OWNER_DECISION_REQUIRED`):
  the evidence is sufficient to characterize the options precisely (S1/S2 non-unique,
  S3 unique-by-primitive, `m=1/2` branch admissible and balance-consistent); the
  decision is an Owner judgment between imposing the primitive and funding the Phase F
  resolution, not a lack of evidence.
- **Not Blocked** (`BLOCKED_DLH_5P_ACCEPTED_ECONOMICS_OR_AUTHORITY_INCONSISTENCY`):
  no accepted-economics or authority inconsistency was found; the accepted source and
  DLH-5N/DLH-5O packages are internally consistent and unchanged.

**What the recommendation does and does not do:** it reports that the critical branch
remains admissible and the tail specification is not unique without an Owner-adopted
primitive. It does NOT freeze, implement, or adopt the specification, does NOT select
R/W/W1/W2/`W_max`, does NOT create HJB/domain/stationary authority, and does NOT close
the Issue.

## G4. Illustrative Owner decision paths (for reference, not binding)

1. **Adopt S3 primitive (path A):** "Adopt S3 with the derivative-control class
   `R=O(1)` (preferred) / P-TR fallback, plus S2's verification condition (subject to
   proof), as the fixed-`a` unbounded-liquid analytic HJB specification; uniqueness of
   the `p=2` coefficient is thereby imposed by the adopted primitive and the Phase F
   theorem gates (existence/comparison/regularity/uniformity/resolution of the
   `m=1/2` remainder) are opened."
2. **Fund resolution (path B):** "Keep S1/S2 as the candidate base; open a research
   gate to resolve the `m=1/2` branch (complete its asymptotic series, test
   transversality, and determine whether it is realized) before any coefficient is
   adopted."
3. **Both:** adopt S3 provisionally while funding the Phase F resolution to test
   whether the primitive is justified.

These paths are illustrative only; the Owner retains final authority.
