# DLH-5P Phase G — Owner Decision Packet

**Issue #42 Phase G.** Compares S1/S2/S3 for the Owner decision. Builder may recommend a
candidate, but the recommendation is **not a model freeze**; the Owner remains final
authority for any model-defining analytic specification. No recommendation creates
accepted analytic-model authority.

## G1. Comparison across the required axes

| Axis | S1 (minimal) | S2 (transversality) | S3 (derivative-controlled) |
|---|---|---|---|
| **Economic interpretation** | continuous extension of the accepted interior economics; no tail law | adds the household's own discounted-value transversality / no-Ponzi (mapped, not textbook) | adds a bounded/sub-root transfer-ratio admissible class (bounded-transfer rationale: adjustment cost penalizes unbounded transfer rates) |
| **Faithfulness to accepted household economics** | high (interior economics only) | high (uses the household's own `rho`-discounting) | high (uses the accepted transfer FOC and adjustment cost; the class is an admissibility restriction, not a modification) |
| **New model authority introduced** | state-space extension + growth class (A14, A18) | + transversality/no-Ponzi law (A15) | + derivative-control class (A21 as model primitive) |
| **Risk of circularly assuming the desired `p=2` result** | none | low | moderate (class contains `p=2`; mitigated by explicit premise, derived coefficient, and the Phase E independent ruling-out) |
| **Mathematical tractability** | high but underdetermined (no uniqueness) | medium (uniqueness via transversality) | medium-high (class gives the coefficient theorem) |
| **Treatment of P-TR** | not assumed, not derived | not derived (transversality does not control `R`) | assumed (admissibility); preferred `R=O(1)`; partially derived at the dominant-balance level (Phase D/E) |
| **Treatment of critical `m=1/2` branch** | ruled out as a smooth dominant balance (Phase E) | same | same + excluded by the class |
| **Compatibility with later HJB<->KFE same-process requirements** | compatible (same interior process) | compatible (same-process value-selection) | compatible (same-process; the class restricts the value gradient, not the process) |
| **Compatibility with eventual R/W domain design** | neutral (no domain authority) | neutral | neutral (a tail admissibility class does not select R/W/`W_max`) |
| **Falsifiability and reproducibility** | falsifiable (constructed alternative tails) | falsifiable | falsifiable (Phase F F2.1-F2.5); the class is explicit and reproducible |

## G2. Builder recommendation

**Recommended package: S3** (derivative-controlled admissibility, preferred subcase
`R = V_a/V_b = O(1)` uniformly; weaker fallback `P-TR: R = o(sqrt(b))` uniformly),
**with S2's economically mapped transversality as the selection law and S1 as the
minimal base.**

Rationale:

1. S1 alone is necessary but insufficient (no uniqueness; the `p=2` coefficient does
   not follow).
2. S2 supplies the selection law needed for a unique value solution and is economically
   faithful, but it does not control the transfer ratio.
3. S3 supplies the derivative-control class under which the accepted DLH-5O coefficient
   theorem holds; the DLH-5P Phase E ruling-out of the critical `m=1/2` branch (and the
   power branches) removes the main obstruction to uniqueness, so the `p=2` tail is the
   **unique** smooth self-consistent dominant balance among the analyzed classes.
4. The circularity risk is explicit and mitigated (Phase D/E), and the class is
   falsifiable (Phase F).

**Caveats to the Owner:** the S3 class is `NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`
(A21); adopting it does not prove P-TR — it makes it an admissibility primitive with
partial dominant-balance-level justification. The full-`[0,10]` uniform theorem
requires the `a_max` upper-`a` endpoint law to be chosen (Phase C). No freeze is
implied.

## G3. Exact recommendation terminal (exactly one)

```text
DLH_5P_ANALYTIC_HJB_SPECIFICATION_CANDIDATE_READY__OWNER_MODEL_DEFINITION_DECISION_REQUIRED
```

**Why Recommendation A and not B or C:**

- **Not B** (`DLH_5P_CRITICAL_TRANSFER_BRANCH_REMAINS_ADMISSIBLE__TAIL_SPECIFICATION_NOT_UNIQUE__OWNER_DECISION_REQUIRED`):
  the critical `m=1/2` branch is **ruled out** as a smooth, uniform dominant balance
  (Phase E: Clairaut forces `p=1/2`; the `O(b^{1/2})` balance is `a`-dependent and
  forces `L=0`; equivalently `(rho - r_b/2)K = S*K` with `0.0125 notin {0,-2/3}` has
  only `K=0`). It therefore does **not** prevent a unique tail specification; the `p=2`
  bounded/sub-root-transfer balance is the unique smooth self-consistent dominant
  balance among the analyzed classes.
- **Not C** (`DLH_5P_ANALYTIC_HJB_SPECIFICATION_EVIDENCE_INSUFFICIENT__OWNER_DECISION_REQUIRED`):
  the evidence is sufficient to propose a defensible candidate package (S3 + S2 + S1)
  with explicit state space, HJB, admissibility class, P-TR treatment, endpoint audit,
  and falsification contract.
- **Not Blocked** (`BLOCKED_DLH_5P_ACCEPTED_ECONOMICS_OR_AUTHORITY_INCONSISTENCY`):
  no accepted-economics or authority inconsistency was found; the accepted source and
  DLH-5N/DLH-5O packages are internally consistent and unchanged.

**What the recommendation does and does not do:** it presents a candidate analytic
specification for the Owner's decision. It does NOT freeze, implement, or adopt the
specification, does NOT select R/W/W1/W2/`W_max`, does NOT create HJB/domain/stationary
authority, and does NOT close the Issue.

## G4. Recommended Owner decision text (for reference, not binding)

If the Owner wishes to proceed, a decision along the lines of:

> "Adopt the DLH-5P recommended analytic candidate (S3 derivative-controlled
> admissibility with `R=O(1)` preferred / P-TR fallback, S2 transversality selection,
> S1 base) as the fixed-`a` unbounded-liquid analytic HJB specification, pending fresh
> ChatGPT review, and open the Phase F theorem gate (existence/uniqueness/regularity/
> uniformity/coefficient convergence)."

would convert the conditional DLH-5O result into a theorem candidate under an
Owner-endorsed analytic authority. This text is illustrative only; the Owner retains
final authority.
