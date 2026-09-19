# DLH-WL-P2B — clean replication of the frozen synthetic prototype — GATE FAIL evidence

## 0. Terminal

```
DLH_WL_P2B_CLEAN_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED
```

The single authorized science invocation executed the complete frozen 12-fit program —
the durable ledger proves 12 attempts started and 12 completed — and then the run
**failed in a post-fit harness accounting step**, so `RAW_RESULTS` was never written and
the publication artifacts could not be rendered.

Per Issue #77 there is **no second science invocation and no science retry** after the
first optimizer step. The Builder did not rerun science, did not tune, and did not
touch the ledger. This report is the Gate Fail evidence package.

## 1. What was executed

| Item | Value |
|---|---|
| Issue | #77 / `DLH-WL-P2B` |
| authority marker | `DLH_WL_P2B_CLEAN_IMMUTABLE_REPLICATION_AUTHORIZED` |
| activation comment | `5740223593` |
| operative baseline | `38e8d75a918e859b36a363d309589a8bd6cf2b1b` |
| **PRE_RUN_FREEZE SHA** | **`1f7c802784f9a07a98bf4b0dab8de029fd3aad8b`** |
| science code identity | the PRE_RUN_FREEZE SHA, executed from a clean detached worktree |
| science invocations | **1 attempted, 0 completed** |
| science retries | **0** |
| second science invocation | **not attempted** |
| fit attempts started / completed / failed | **12 / 12 / 0** |

Pre-run gates, all green before the freeze: focused protocol tests `22 passed` (zero
optimizer steps), science `--validate-only` zero optimizer steps / zero fits with
module blob `MATCH`, render-only `--validate-only` `renderer_imports_fitters = false`.

## 2. Frozen-identity verification (before `--execute-science`)

Executed in a clean detached worktree at the exact PRE_RUN_FREEZE SHA, with an empty
`git status`:

| Object | Blob | Status |
|---|---|---|
| scientific module `labor_destination_p2.py` | `b1f2cd043605c511e4965254657d12306170609b` | **MATCH** (accepted #76 module, byte-for-byte) |
| frozen config `dlh_wl_p2_offline_prototype.toml` | `bb5dbbd0746e9d92874f94b03a1d54f3d382c4a8` | MATCH |
| frozen contract | `99b62bd8cc294e5518b3548ce7f6098784ccd561` | MATCH |
| frozen schema | `862debb5aacb47fc5de906127dca10690324965c` | MATCH |
| P1A accounting module | `7522dd9331504bd64f2ac933ed3c010605bc097d` | MATCH |

## 3. Durable attempt ledger (immutable)

`reports/dlh_wl_p2b_2026_09_19/DLH_WL_P2B_ATTEMPT_LEDGER.jsonl`, 24 records:
`FIT_ATTEMPT_STARTED` before each fit and `FIT_COMPLETED` after it, each appended with
flush + fsync, carrying `pre_run_freeze_sha = 1f7c8027…`.

```
ledger records      : 24  (12 started + 12 completed, 0 failed)
started indices     : 1..12 exactly
completed indices   : 1..12 exactly, each after its STARTED record
ledger SHA-256 (LF) : 3920DB9C4EFF4CB346139DE2C1EDA0975679A1457743472C7428D329254773A5
```

All twelve frozen fits completed: 2 parametric primaries, 2 parametric verification
repeats, 6 neural primaries (seeds 0/1/2 × S0/S1) and 2 neural seed-0 verification
repeats. The ledger was not modified after the failure.

## 4. Failure

- **stage**: post-fit harness accounting, after all 12 fits had completed;
- **component**: `scripts/run_dlh_wl_p2b_replication_science.py`;
- **function**: `_constraint_diagnostics`;
- **exception**: `KeyError: 'metrics'`;
- **cause**: the harness passed the per-fit metrics mapping (`fit_key -> {split: metrics}`)
  to a helper written to consume `{split: metrics}` entries. The helper itself was unit
  tested, but the post-fit aggregation call path was never exercised by a zero-fit test
  before the freeze, so the defect was not caught pre-run;
- **classification**: harness/accounting defect — not a scientific, numerical or
  environment failure;
- **scientific outcome consulted**: no; **configuration or results tuned**: no;
- **RAW_RESULTS written**: no;
- **wall clock**: ~1.33 s for the science process, well inside the 1800 s ceiling.

## 5. Why this is Gate Fail and not a rerun

Issue #77 fixes the boundary: *"If the science process fails after any fit begins, P2B
terminates Gate Fail/Blocked using the durable ledger. Do not rerun science."* and
*"No second science invocation is authorized under any circumstance."*

A patch-and-rerun was therefore not performed. It would also have re-attempted twelve
fits that the ledger already records, which is exactly the #76 failure mode the
adjudication rejected. The durable ledger is the load-bearing record of what actually
happened.

## 6. Evidence preserved

| Path | Role |
|---|---|
| `reports/dlh_wl_p2b_2026_09_19/DLH_WL_P2B_ATTEMPT_LEDGER.jsonl` | durable, immutable record of the 12 started and 12 completed fits |
| `reports/dlh_wl_p2b_2026_09_19/DLH_WL_P2B_SCIENCE_RUN_FAILURE.json` | structured record of the invocation, the failure, the counts and the boundary respected |

`DLH_WL_P2B_RAW_RESULTS.json`, `DLH_WL_P2B_RESULTS.json`, `DLH_WL_P2B_MANIFEST.json`
and `DLH_WL_P2B_REPORT.md` were **not** produced: the raw science artifact was never
written and the renderer fails closed without it (`--render-only` returned
`BLOCKED_DLH_WL_P2B_PRE_RUN_OR_ENVIRONMENT`; its `--validate-only` reported
`raw_present = false`, `ledger_present = true`, `optimizer_steps_performed = 0`,
`fit_attempts_performed = 0`).

## 7. Immutability audit

Unchanged since the PRE_RUN_FREEZE commit, verified by blob comparison:

- `scripts/run_dlh_wl_p2b_replication_science.py`
- `scripts/render_dlh_wl_p2b_replication.py`
- `tests/test_dlh_wl_p2b_replication_protocol.py`
- `src/deep_learning_hank/regional/labor_destination_p2.py`
- `configs/dlh_wl_p2_offline_prototype.toml`

No contract, config, scientific-module or test mutation occurred. No real data, no
HJB/KFE/GE/MATLAB/household call, no full suite, no tuning, no extra seed.

## 8. Interpretation ceiling

The 12 completed fits produced no persisted scientific output, so **no scientific claim
of any kind is made here** — not about the neural mapping, not about the parametric
baseline, and not about replication of the #76 observations. The #76 observational
metrics remain audit context only.

Forbidden and not claimed: empirical China; annual OD data availability; unseen-region;
causal or economic mechanism; HJB/KFE/GE/household policy or welfare; any tuning based
on #76 or P2B outcomes.

## 9. Suggested direction (Reviewer decision required)

The twelve fits were executed and are durably recorded, so completing this replication
faithfully would mean **reusing** those already-attempted fits rather than running
thirteen or more. That requires one of:

1. a Reviewer amendment/successor that treats the durable ledger as the attempt record
   and adds a **zero-fit accounting path** which evaluates constraints and metrics from
   persisted per-fit predictions (mechanically this is what `--render-only` already is,
   minus the in-process constraint evaluation that failed); or
2. a Reviewer decision that this replication cannot be completed as specified and a
   fresh, separately authorized replication is required.

The Builder has **no authority to choose between these or to act on either**. No
design change is required by option 1.

## 10. Terminal

```
DLH_WL_P2B_CLEAN_REPLICATION__GATE_FAIL__NO_SCIENCE_RERUN_AUTHORIZED
```
