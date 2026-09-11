# DLH-5V-G — Authority Capsule

**Issue:** deep-learning-hank #55 / DLH-5V-G — OPEN.
**Task type:** `SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`
**Owner decision:** `APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`
**Activation:** comment `5634144909` (authority marker `DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_APPROXIMATION_AUTHORIZED`) + refresh `5634171277`.
**Fresh `origin/main` (FINAL CURRENT SYNC):** `c8c5c3f8d3a002a7efcb93682ff42d50c3667602` — recorded at startup, matches the authoritative refresh comment.
**Dedicated Builder branch:** `dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11` (created from `origin/main`, 0 ahead/behind at start).

## Digest (authority in 12 lines)

1. Issue #55 is the sole Builder authority; body + comments `5634144909` / `5634171277` are binding.
2. Current governance (Task Index, Startup Snapshot, Master Roadmap V0.40, all CURRENT rules) identifies Issue #55 / this task type / this branch; no conflict.
3. Accepted household source immutable; blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified at startup.
4. DLH-5V-F accepted and controlling (candidate `b9dab7b6cf5d724074765ddb88d6f300175f6c6f`, acceptance `5633995486`, integration `4e77d9c753f81eb2517a8b90a0827db6af8faed4`); consumed, not reopened.
5. Scientific object: symbolic fixed-aspect refinement family `da_m = 10/(19m)`, `db_m = 7/(19m)`, `N_m = floor(19m*(W_max-b_min))`, nodes `10j + 7i <= N_m`; no numerical `W_max`.
6. Route A tested first: numerical candidate-admissibility buffer (A1), applied before scoring, distinct from true economic faces.
7. **A1 PASSES**: every admitted endpoint candidate has an exact represented native-grid first-moment contract; endpoint physical width `ell_m = 70/(19m) -> 0`; exact regular contract recovered away from endpoints; tangent-cone, generator/operator, jump/rate/second-moment scaling, monotonicity, conservation, one-Q and seam consistency all proved.
8. A2 (explicit moment defect) is NOT invoked, per Issue §5.5.
9. Design only; no implementation, no production `Q`, no HJB/KFE/stationary solve, no numerical production `W_max`.
10. Terminal (exactly one): `DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_SAME_PROCESS_CONTRACT_FROZEN__READY_FOR_BOUNDARY_HJB_IMPLEMENTATION_GATE`.
11. Six-file allowlist written; no existing tracked file modified; explicit staging only.
12. STOP for fresh ChatGPT review. No merge, no close, no successor, no self-accept.

## Evidence produced

- Closed-form analytic proof (in `m`) of the A1 contract: cases L (reverse sector), U (T_realloc/deplete), B (T_realloc) and interior cells; cone equalities with explicit nonnegative rates; exact first moments.
- Structural facts F1–F4 (layer membership and generator availability) proved and spot-verified exactly (tiny `%TEMP%` scripts, never committed): `m in {1..7}`, all residues `N_m = 190m + s`, `s in {0..13}` — 0 violations; sector-generator availability 795 + 931 + 980 + 28 checks, 0 missing; buffered-drift-in-destination-cone exact separation tests 158 checks, 0 failures.
- Scaling verified: rate `O(m)`, second moment `O(1/m)` with `m * (2nd moment)` exactly constant over `m in {1..32}`.

## Governance / binding law (unchanged)

```text
HJB boundary policy <=> KFE boundary transition law
Q backward; Q^T forward; Q_ij >= 0 for i != j
Q_ii = -sum of ACTUAL represented outgoing rates; Q1 = 0
HJB and KFE consume the SAME Q
```

Pinning/normalization may fix scale only; stationary KFE remains NOT AUTHORIZED.

## Related accepted provenance

- DLH-5V-A (`reports/dlh_5va_regular_voronoi_frontier_2026_09_10/`): phase facts `i_t(j)`, `r_j`, period 7, W-active classes.
- DLH-5V-E (`docs/design/DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE.md`): regular T_realloc/R_reverse/R_deplete contracts.
- DLH-5V-F (`docs/design/DLH_5VF_ENDPOINT_BAND_AND_JOINT_BOUNDARY_FINITE_PROCESS_CLOSURE.md`): accepted endpoint obstruction.
