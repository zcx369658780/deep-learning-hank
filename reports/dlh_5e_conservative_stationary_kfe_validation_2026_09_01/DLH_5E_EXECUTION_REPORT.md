# DLH-5E — Conservative Stationary-KFE Validator and Canonical Boundary-Policy Gate (Issue #28)

This is an implementation-validation candidate gate, not production integration. The accepted MATLAB-faithful HJB source is immutable and reused read-only.

Overall terminal classification: `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`

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
| d0 | upper_a | 2.641e-01 | 28 | (9, 19, 1) | 0.2640718827021816 |

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

## Reproducibility

- randomness: `NOT_APPLICABLE`; repeat pass: `True`; terminal run1/run2: `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED` / `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`.
- d0: structural identical True, max numeric diff 0.000e+00, aligned non-finite 0, mismatched 0, pass True.
- d1: structural identical True, max numeric diff 0.000e+00, aligned non-finite 5, mismatched 0, pass True.
- d2: structural identical True, max numeric diff 0.000e+00, aligned non-finite 5, mismatched 0, pass True.
- d3: structural identical True, max numeric diff 0.000e+00, aligned non-finite 5, mismatched 0, pass True.

## Artifact integrity

- accepted MATLAB-faithful oracle blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` re-verified read-only under DLH-5E (unchanged from the Issue #26 accepted state).
- no existing file modified; dedicated branch `dsh/issue-28-dlh-5e-conservative-kfe-validation-2026-09-01`; allowlist-only additions (4 artifacts, 8 evidence files).

DLH-5E implements NO repair: the accepted HJB/local-policy source is immutable; no conservative assembler is integrated into production; no alternative pin is selected; no regularization/jitter/pseudoinverse.