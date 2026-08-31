# DLH-5B — Forbidden-Operation / Scope Check (Issue #25)

DSH did NOT perform any of the following during Issue #25 execution (including R1 repair):

| Forbidden operation | Status |
|---|---|
| Modify the accepted two-asset household oracle | NOT performed (immutable) |
| Reintroduce `B_hh=B_gov=1` / fixed bond-supply GE root | NOT performed |
| Brent/Newton/fsolve for the outer regional fixed point | NOT performed (fixed damping only; Brent used solely in the accepted household initial-value fixture) |
| Change scientific/numerical fixture fields after seeing results | NOT performed (config frozen; only `output.root` mutated for the R1 root) |
| Adaptive damping / automatic retry | NOT performed (`NO_AUTOMATIC_RETRY`) |
| Grid expansion | NOT performed |
| `GovInv` / GDP-target controller | NOT performed |
| `W^K` / capital-flow learning | NOT performed |
| Neural network / learned `W^L` | NOT performed |
| Nominal rigidity / Phillips / Taylor / Fisher / new debt closure | NOT performed |
| 31-region scaling | NOT performed |
| Policy/welfare/Results claims | NOT performed |
| Modify existing single-region GE code (`src/deep_learning_hank/ge/**`) | NOT performed |
| Modify accepted household source / prior configs/tests/reports / roadmap / governance / legacy roots | NOT performed |
| Overwrite predecessor evidence root (`reports/dlh_5b_two_region_fixed_point_2026_08_31`) | NOT performed (preserved unchanged) |
| `git add .` / `git add -A` | NOT performed (explicit staging only) |
| Self-accept / merge / close Issue / PR / successor Issue | NOT performed |

Execution discipline: no-overwrite output root `reports/dlh_5b_two_region_fixed_point_r1_2026_08_31` (STOP if pre-existing), `NO_AUTOMATIC_RETRY`.

Fail-closed gates: S0 validity bundle + residuals, S1 per-turn validity bundle, S2 order invariance, S0/S1 reproducibility.

Terminal classification: `DLH_5B_TWO_REGION_ARCHITECTURE_VALIDATED__PERTURBED_PATH_HOUSEHOLD_BLOCKED_READY_FOR_GPT_REVIEW`
