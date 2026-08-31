# DLH-4D-R3 — Phase E: Frozen GE Re-execution Report (INCONCLUSIVE)

- **Issue:** #23 (DLH-4D-R3: repair MATLAB-faithful transfer-FOC liquid-derivative semantics)
- **Branch:** `dsh/issue-23-dlh-4d-r3-matlab-transfer-foc-repair-2026-08-30` (working tree, not yet committed)
- **Frozen GE path:** `src/deep_learning_hank/ge/two_asset_single_region.py::solve_ge` — **unchanged**
- **Frozen fixture:** `configs/dlh_4d_two_asset_single_region_ge_validation.toml` (Issue #20; **not modified**)
- **Oracle:** repaired `matlab_faithful_two_asset_ha.py` (post-repair blob `76ae5b14…`, SHA-256 `1795718C…`)

## 1. Disposition (Owner instruction)

Phase E was stopped by the Owner **before reaching a terminal E1/E2 state**, after
the Owner-set bounded execution ceiling (~8 h) had elapsed and the run still had no
terminal result. Per the Owner instruction, the incomplete run is **not interpreted
as GE PASS and not interpreted as E2**. This report preserves the run evidence as an
explicit INCONCLUSIVE item for a later gate.

## 2. How Phase E was executed (frozen-path integrity)

1. The frozen `GeConfig` was loaded from the unmodified TOML (frozen identities
   intact: `immutable_oracle_sha256=276D2244…`, blob `57e32076…` — the Issue #20
   frozen values).
2. A fresh in-memory config was built with `dataclasses.replace(..., immutable_oracle_sha256=
   <post-repair SHA>, immutable_oracle_blob=<post-repair blob>)`. **The TOML file was
   never written.** Issue #23 authorizes this identity override as the narrow,
   sole exception to the frozen-household gate.
3. `solve_ge(config)` was invoked exactly as the frozen GE path defines it: same
   nested R1(outer)/R3(middle)/R2(inner) brentq structure, same
   `bracket_scan_points=9`, same domains, same tolerances, same gates. No solver
   parameter, domain, economics, or gate was changed.
4. No other code path (no `evaluate_ge` shortcut, no reduced scan, no tuned
   bracket) was used.

## 3. Run evidence

| Metric | Value |
|---|---|
| Start (UTC+8) | 2026-08-31 06:26:48 |
| Stopped (Owner request) | after **8.77 h** wall |
| Total CPU consumed | **508.4 CPU-min** (~0.97 core average, steady) |
| Working-set memory | ~61 MB (stable; no leak) |
| Threads observed | 39 |
| Terminal `phaseE.json` | **NOT written** — no E1 root, no E2 fail-closed |
| Last-observed runtime warnings | `MatrixRankWarning: Matrix is exactly singular` (KFE `spsolve` on singular candidate operators) and `RuntimeWarning: divide by zero` (`transfer_candidate` IEEE zero-divisor at `v_b = 0` cells) — both expected under the repaired IEEE semantics |

The run consumed roughly **1.73× the full 729-candidate scan estimate** (~293
CPU-min, measured from the Phase D reclassification run) without reaching a
terminal state, consistent with `solve_ge` having entered nested brentq
refinement, where each residual evaluation re-runs nested full household solves
(30–130 s on non-convergent/singular candidates under the repaired oracle). This
is a legitimate, bounded property of the frozen GE path on the repaired oracle;
it is not a code defect.

## 4. What Phase E did NOT establish

- **No E1:** no GE root was found/validated, so **no** Issue #20 gate results are
  reported (root_norm, market/resource/fiscal/wealth gates are **not claimed**).
- **No E2:** the frozen path did not fail-closed with a RootBracketError /
  `GeSolveError` before being stopped, so the "still blocked" classification is
  **not claimed** either.
- Phase E therefore contributes **no PASS or FAIL conclusion** to Issue #23. It is
  a recorded, reproducible attempt whose completion is deferred.

## 5. Why Phase E is slow on the repaired oracle (explanatory, non-tuning)

Under the pre-repair oracle, most domain candidates guard-failed almost
instantly (`v_b ≤ 0` → exception → non-finite), so `solve_ge`'s scan was cheap and
failed closed quickly. The repair removed those guards, so the frozen scan now
runs **full household solves** on candidates that previously short-circuited:
finite candidates cost seconds each, while the 168 non-convergent and 60
singular-KFE candidates cost 30–130 s each. The 8.77 h run is therefore a direct,
expected consequence of the parity repair — not a regression introduced by the
GE path (which is untouched) and not a tuning opportunity within Issue #23's
scope.

## 6. Recommended next gate (non-binding)

1. Let the frozen `solve_ge` re-execution run to a **terminal** state with an
   unbounded/adequate window (or on a dedicated machine), then classify E1 or E2
   with the Issue #20 gate evidence.
2. Optional (requires a future Issue/authority): evaluate whether the frozen GE
   scan could be made practical (e.g., an explicit non-convergence fast-fail in
   the household oracle's return path) — this is a solver/household change outside
   Issue #23's narrow mandate and must not be done here.

## 7. Integrity statements

- Frozen fixture file, GE module, and solver domains: **untouched** (verified).
- No fixture/domain/GE-economics tuning; no PASS-seeking.
- Phase E result is preserved as INCONCLUSIVE; nothing in this report should be
  read as a GE PASS or as an E2 blocker.
