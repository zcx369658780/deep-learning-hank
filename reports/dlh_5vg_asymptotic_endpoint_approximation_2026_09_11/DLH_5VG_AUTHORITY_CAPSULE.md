# DLH-5V-G — Authority Capsule (Rev 1: bounded reanalysis of comment `5634957294`)

**Issue:** deep-learning-hank #55 / DLH-5V-G — OPEN.
**Task type:** `SCIENTIFIC_DESIGN__SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_MARKOV_APPROXIMATION`
**Owner decision:** `APPROVE_DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_DESIGN_GATE`
**Activation:** comment `5634144909` (authority marker `DLH_5VG_ROUTE_A_SHRINKING_ENDPOINT_LAYER_ASYMPTOTIC_APPROXIMATION_AUTHORIZED`) + refresh `5634171277`.
**Reviewer verdict (controlling):** `DLH_5VG_OUTCOME_A_NOT_ACCEPTED__A1_TANGENT_CONE_GRAPH_CONSISTENCY_COUNTEREXAMPLE__BOUNDED_REANALYSIS_REQUIRED` (comment `5634957294`).
**Fresh `origin/main`:** `c8c5c3f8d3a002a7efcb93682ff42d50c3667602` (FINAL CURRENT SYNC, unchanged).
**Dedicated Builder branch:** `dsh/issue-55-dlh-5vg-asymptotic-endpoint-approximation-2026-09-11` (same branch; Rev 1 edits only the six allowlist files).

## Digest (authority in 12 lines)

1. Issue #55 remains the sole Builder authority; body + comments `5634144909` / `5634171277` / `5634957294` are binding.
2. Current governance identifies Issue #55 / this task type / this branch; no conflict.
3. Accepted household source immutable; blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` verified at startup and unchanged.
4. DLH-5V-F accepted and controlling (candidate `b9dab7b6cf5d724074765ddb88d6f300175f6c6f`, acceptance `5633995486`, integration `4e77d9c753f81eb2517a8b90a0827db6af8faed4`); consumed, not reopened.
5. Scientific object: frozen fixed-aspect family `da_m = 10/(19m)`, `db_m = 7/(19m)`, `N_m = floor(19m*(W_max-b_min))`; no numerical `W_max`.
6. Reviewer counterexample confirmed: `s_m = (0, i_t^m(0) - 2)`, `mu = (0, +1)` is A1-admitted, exactly represented (`q_up = 19m/7`), and `x_m -> (0, W_max)` with `mu_W = +1 > 0` — outer/limsup fails.
7. Generalization: every fixed-`j` cell `(j, i_t(j) - 2)` (including regular-region `j = 7, ...`) converges to `(0, W_max)`; the frozen accepted interior contract itself violates the global outer condition — not repairable by endpoint-layer changes.
8. Impossibility: no per-state admissible-set rule (row-count, shrinking/fixed W-distance, W-activity) can satisfy both outer/limsup (Family C, `W-dist -> 0`) and recovery/liminf (Family F, `W-dist -> c > 0`) — §3.3 of the umbrella.
9. A2 cannot repair: a first-moment defect does not change admissibility; the counterexample drift is exactly representable with zero defect.
10. **A1 fails; no permitted Route-A contract meets the graph-consistency requirements.**
11. Terminal (exactly one): `DLH_5VG_ROUTE_A_ASYMPTOTIC_ENDPOINT_APPROXIMATION_OBSTRUCTION__OWNER_ROUTE_REDECISION_REQUIRED`.
12. Six-file allowlist edited on the same branch; no existing tracked file modified outside it; explicit staging only; STOP for fresh ChatGPT review. No merge, no close, no successor, no self-accept.

## Evidence produced (Rev 1)

- Mandatory counterexample test (reviewer item 1) verified exactly over `m in {1,2,5,20,100}`: `W-dist = (r_0^m + theta_m + 14)/(19m)` from 0.789 down to 0.008; `q_up = 19m/7`; destination `(0, i+1)` represented at every level.
- Generalization to all fixed `j` (incl. regular `j = 7, 12, 30`) and to the upper corner `(19m, i_t(19m)-2)` with `mu = (-1, +2)` (exact via `w_left` + `w_up`).
- Escape-sequence analysis for candidate buffers: fixed row-count `K` escaped by `k = sqrt(mK)`; shrinking `delta_m` escaped by `k = m/f(m)`, `f -> oo` arbitrarily slow; fixed `delta` over-constrains Family F with `c < delta`.
- Finite-m algebra (rates/moments/scaling/monotonicity/conservation/one-Q) retained from Rev 0; corner and interior-layer taxonomy corrected per reviewer item 6; operator bound made pure `C^2` (item 7); floor proofs rewritten with exact inequalities (item 8).
- Exact `%TEMP%` spot-checks only (never committed).

## Governance / binding law (unchanged)

```text
HJB boundary policy <=> KFE boundary transition law
Q backward; Q^T forward; Q_ij >= 0 for i != j
Q_ii = -sum of ACTUAL represented outgoing rates; Q1 = 0
HJB and KFE consume the SAME Q
```

Pinning/normalization may fix scale only; stationary KFE remains NOT AUTHORIZED.

## Related accepted provenance

- DLH-5V-A phase facts; DLH-5V-E regular sector contracts; DLH-5V-F accepted endpoint obstruction; DLH-5T continuous KKT boundary laws (corner semantics per §6 of the umbrella).
