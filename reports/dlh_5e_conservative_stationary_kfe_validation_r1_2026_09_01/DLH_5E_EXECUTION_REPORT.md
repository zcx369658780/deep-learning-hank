# DLH-5E — Conservative Stationary-KFE Validator and Canonical Boundary-Policy Gate (Issue #28)

This is an implementation-validation candidate gate, not production integration. The accepted MATLAB-faithful HJB source is immutable and reused read-only.

Overall terminal classification: `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`

R1 run (2026-09-01): boundary coordinate reconstruction corrected to C-order `np.unravel_index`; complete offending-state sets persisted; reproducibility extended to the full boundary evidence. Predecessor root `reports/dlh_5e_conservative_stationary_kfe_validation_2026_09_01` preserved unchanged; this R1 root contains the same eight evidence filenames.

## Case status

| case | wbar | r_a | HJB converged | iters | boundary gate | max requested outward | generator row-sum max-abs | generator neg-offdiag max-mag | terminal |
|---|---|---|---|---|---|---|---|---|---|
| d0 | 1.000000000 | 0.030000000 | True | 11 | VIOLATION | 3.537e-01 | 6.106e-16 | 0.000e+00 | BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED |
| d1 | 0.997727839 | 0.029912763 | — | — | NOT_EVALUATED | — | — | — | NOT_REACHED__D0_BLOCKED |
| d2 | 0.998807521 | 0.029964195 | — | — | NOT_EVALUATED | — | — | — | NOT_REACHED__D0_BLOCKED |
| d3 | 1.001194155 | 0.030035653 | — | — | NOT_EVALUATED | — | — | — | NOT_REACHED__D0_BLOCKED |

## Boundary-policy diagnostics (Phase B/D)

Requested outward boundary rates are reconstructed from post-convergence `mu_b`/`mu_a` as `max(-mu_b,0)/db`, `max(mu_b,0)/db`, `max(-mu_a,0)/da`, `max(mu_a,0)/da` and are NEVER clipped or mutated. Boundary requested outward rates are exactly the lower-b/upper-b/lower-a/upper-a slices.

| case | boundary | requested outward max | count > 1e-10 | argmax coords | requested at max |
|---|---|---|---|---|---|
| d0 | lower_b | 0.000e+00 | 0 | (0, 0, 0) | 0.0 |
| d0 | upper_b | 3.537e-01 | 3 | (19, 19, 1) | 0.3537477040220836 |
| d0 | lower_a | 0.000e+00 | 0 | (0, 0, 0) | 0.0 |
| d0 | upper_a | 2.641e-01 | 28 | (14, 19, 1) | 0.2640718827021816 |

### Complete offending states (requested outward rate > 1e-10)

Coordinates are exact `(b_index, a_index, z_index)` recovered with `np.unravel_index(..., order='C')` on the actual 2-D boundary slice shape (`(a,z)` for b-boundaries, `(b,z)` for a-boundaries).

| case | boundary | direction | b_index | a_index | z_index | requested outward rate |
|---|---|---|---|---|---|---|
| d0 | upper_b | b_forward | 19 | 17 | 1 | 1.157606987e-01 |
| d0 | upper_b | b_forward | 19 | 18 | 1 | 2.718687236e-01 |
| d0 | upper_b | b_forward | 19 | 19 | 1 | 3.537477040e-01 |
| d0 | upper_a | a_forward | 5 | 19 | 1 | 3.175106194e-03 |
| d0 | upper_a | a_forward | 6 | 19 | 1 | 1.034225218e-01 |
| d0 | upper_a | a_forward | 7 | 19 | 0 | 2.940147623e-02 |
| d0 | upper_a | a_forward | 7 | 19 | 1 | 1.460640158e-01 |
| d0 | upper_a | a_forward | 8 | 19 | 0 | 9.009153816e-02 |
| d0 | upper_a | a_forward | 8 | 19 | 1 | 1.763017040e-01 |
| d0 | upper_a | a_forward | 9 | 19 | 0 | 1.367105809e-01 |
| d0 | upper_a | a_forward | 9 | 19 | 1 | 2.031466324e-01 |
| d0 | upper_a | a_forward | 10 | 19 | 0 | 1.732706282e-01 |
| d0 | upper_a | a_forward | 10 | 19 | 1 | 2.253730726e-01 |
| d0 | upper_a | a_forward | 11 | 19 | 0 | 2.021709716e-01 |
| d0 | upper_a | a_forward | 11 | 19 | 1 | 2.429588552e-01 |
| d0 | upper_a | a_forward | 12 | 19 | 0 | 2.248302109e-01 |
| d0 | upper_a | a_forward | 12 | 19 | 1 | 2.558509867e-01 |
| d0 | upper_a | a_forward | 13 | 19 | 0 | 2.419158557e-01 |
| d0 | upper_a | a_forward | 13 | 19 | 1 | 2.634259008e-01 |
| d0 | upper_a | a_forward | 14 | 19 | 0 | 2.533455404e-01 |
| d0 | upper_a | a_forward | 14 | 19 | 1 | 2.640718827e-01 |
| d0 | upper_a | a_forward | 15 | 19 | 0 | 2.580826964e-01 |
| d0 | upper_a | a_forward | 15 | 19 | 1 | 2.546689128e-01 |
| d0 | upper_a | a_forward | 16 | 19 | 0 | 2.537143916e-01 |
| d0 | upper_a | a_forward | 16 | 19 | 1 | 2.305539903e-01 |
| d0 | upper_a | a_forward | 17 | 19 | 0 | 2.352871698e-01 |
| d0 | upper_a | a_forward | 17 | 19 | 1 | 1.867536785e-01 |
| d0 | upper_a | a_forward | 18 | 19 | 0 | 1.907037702e-01 |
| d0 | upper_a | a_forward | 18 | 19 | 1 | 1.206860239e-01 |
| d0 | upper_a | a_forward | 19 | 19 | 0 | 8.783338931e-02 |
| d0 | upper_a | a_forward | 19 | 19 | 1 | 3.635781425e-02 |

**Global max requested outward boundary rate:** 3.537e-01 (boundary upper_b).

**Boundary-policy gate: VIOLATION.** The frozen threshold is `max requested outward boundary rate <= 1e-10`. The D0 requested outward rate exceeds it materially, so the task fail-closes with `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`. No stationary density is accepted from the mechanically clipped candidate generator; no `C/L/A/B`, no `Z*/delta*`, no D1-D3, no two-region iteration are computed. This is a valid scientific completion.

## Conservative generator mechanical diagnostics (Phase C)

The candidate generator `Q_c` omits outward destinations outside the represented grid AND omits their rate from the diagonal (`Q_c[i,i] = -sum` of ACTUALLY ADMITTED off-diagonal rates); the accepted z-switch block is included.

| case | row-sum max abs | neg offdiag max mag | neg offdiag count | row-sum min | row-sum max | nnz |
|---|---|---|---|---|---|---|
| d0 | 6.106e-16 | 0.000e+00 | 0 | -6.106e-16 | 2.776e-16 | 3114 |
| d1 | — | — | — | — | — | — |
| d2 | — | — | — | — | — | — |
| d3 | — | — | — | — | — | — |

Required invariants (DLH-5D): `row_sum max abs <= 1e-12`, `negative offdiag magnitude <= 1e-12`. The generator is mechanically conservative independent of the boundary-policy gate; it is a diagnostic/candidate only and never accepted as the stationary density when the gate blocks.

## Stationary / pin / aggregate gates (NOT REACHED)

Because the D0 boundary-policy gate blocks, stationary uniqueness, contamination/pin admissibility, aggregate recomputation and the candidate anchor are NOT reached in this run. The corresponding synthetic unit tests exercise those code paths.

## Predecessor vs R1 comparison (preserved predecessor root read-only)

- D0 HJB convergence: predecessor `True` (iters `11`) vs R1 `True` (iters `11`).
- global boundary max: predecessor `3.537477e-01` vs R1 `3.537477e-01`.
- conservative Q_c row-sum max abs: predecessor `6.106e-16` vs R1 `6.106e-16`; neg off-diagonal max mag `0.000e+00` vs R1 `0.000e+00`.
- terminal classification: predecessor `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED` vs R1 `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`.

| boundary | predecessor max | R1 max | predecessor count | R1 count | predecessor argmax | R1 argmax (corrected) | argmax changed | complete R1 offending count |
|---|---|---|---|---|---|---|---|---|
| lower_b | 0.000000e+00 | 0.000000e+00 | 0 | 0 | (0, 0, 0) | [0, 0, 0] | False | 0 |
| upper_b | 3.537477e-01 | 3.537477e-01 | 3 | 3 | (19, 19, 1) | [19, 19, 1] | False | 3 |
| lower_a | 0.000000e+00 | 0.000000e+00 | 0 | 0 | (0, 0, 0) | [0, 0, 0] | False | 0 |
| upper_a | 2.640719e-01 | 2.640719e-01 | 28 | 28 | (9, 19, 1) | [14, 19, 1] | True | 28 |

Corrected argmax coordinates changed only where the predecessor Fortran-style `% first_len` reconstruction was wrong; rates and counts are identical to predecessor because the underlying drifts are unchanged.

## Reproducibility

- randomness: `NOT_APPLICABLE`; repeat pass: `True`; terminal run1/run2: `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED` / `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`.
- d0: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
  - boundary repeat compare pass `True`: lower_a: direction True, count True, argmax True, coords exact True, offending 0, max rate diff 0.000e+00, exact True, rate pass True, lower_b: direction True, count True, argmax True, coords exact True, offending 0, max rate diff 0.000e+00, exact True, rate pass True, upper_a: direction True, count True, argmax True, coords exact True, offending 28, max rate diff 0.000e+00, exact True, rate pass True, upper_b: direction True, count True, argmax True, coords exact True, offending 3, max rate diff 0.000e+00, exact True, rate pass True
- d1: structural identical True, max numeric diff 0.000e+00, aligned non-finite 5, mismatched 0, pass True.
  - boundary repeat compare pass `True`: 
- d2: structural identical True, max numeric diff 0.000e+00, aligned non-finite 5, mismatched 0, pass True.
  - boundary repeat compare pass `True`: 
- d3: structural identical True, max numeric diff 0.000e+00, aligned non-finite 5, mismatched 0, pass True.
  - boundary repeat compare pass `True`: 

## Artifact integrity

- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` re-verified read-only under DLH-5E (unchanged from the Issue #26 accepted state).
- no existing file modified; dedicated branch `dsh/issue-28-dlh-5e-conservative-kfe-validation-2026-09-01`; allowlist-only additions (4 artifacts, 8 evidence files).

DLH-5E implements NO repair: the accepted HJB/local-policy source is immutable; no conservative assembler is integrated into production; no alternative pin is selected; no regularization/jitter/pseudoinverse.