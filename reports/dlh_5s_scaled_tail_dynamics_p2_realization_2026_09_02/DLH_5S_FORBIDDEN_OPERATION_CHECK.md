# DLH-5S — Forbidden-Operation / Scope Check (Issue #45 §13)

**Rev 2 (review `5516660741`):** same scope. This bounded revision only
corrects analytic statements inside the same nine allowlist files (labor
convention, S3-sign, branch classification, net-remainder sign, full-HJB rates,
"minimality", terminal A -> B). No forbidden operation was performed in Rev 2.

**Rev 3 (review `5518243412`):** documentation/theory correction only inside
the same nine allowlist files — (i) the local `b^(-7)` estimate near K* is no
longer extrapolated (the `Q(b) ~ K* + (315-K*)(b/20)^(-7)` and "by b~30"
claims are deleted); (ii) `Q -> K*` alone no longer implies `p_eff -> 2`
(requires additionally `d log Q/d log b -> 0`); (iii) the asymptotically
autonomous limit is stated as the `E=0` z-coupled vector system, with the
scalar z-symmetric system as an invariant subsystem / conditional reduction.
Terminal B preserved. No forbidden operation was performed in Rev 3.

DLH-5S is **analytic theory work only**. DSH performed NONE of the following;
no accepted source, economics, domain, numerical, or governance object was
modified, and no numerical experiment was run.

| Forbidden operation (Issue #45 §13) | Status |
|---|---|
| Modify accepted HJB/KFE/regional source or household economics | NOT PERFORMED — accepted source read-only; blob `76ae5b149993a7edeeb337f1b02b3fe33c51e` unchanged |
| Modify utility / FOCs / adjustment cost / taper / prices / taxes / calibration | NOT PERFORMED — frozen D0 objects used verbatim |
| Run any new HJB/grid/resolution experiment | NOT PERFORMED — no solver call, no grid, no numerical execution |
| Rerun J0-J5 as new scientific evidence | NOT PERFORMED — DLH-5R medians used as read-only evidence context only |
| Reopen b160 / create b180/b200 / alter b_lo/db/a_max/a resolution / adaptive or root-seeking domain search | NOT PERFORMED — no domain change of any kind; b160 remains the pre-existing ceiling |
| Choose or implement R/W/W1/W2/`W_max` | NOT PERFORMED |
| Invent/implement endpoint KKT or state-domain laws | NOT PERFORMED — compact interior `a` only; `a=10`/`b_lo`/`a=0` remain Owner-decision items |
| Run stationary KFE / nullspace / pin / density / tail mass / aggregates | NOT PERFORMED — stationary KFE remains NOT AUTHORIZED (Issue #27) |
| Enter regional GE / multi-province audit / neural training / nominal HANK / calibration / policy / welfare / Results | NOT PERFORMED |
| Create PR / merge / close Issue #45 / successor Issue / self-accept | NOT PERFORMED — DSH stops for fresh ChatGPT review |
| Modify any existing tracked file | NOT PERFORMED — only the exact nine Issue #45 allowlist files created |
| Commit large numerical arrays | NOT PERFORMED — no numerical arrays produced |

**Scope compliance summary:** the analysis is restricted to the accepted
analytic interior HJB and its scaled-variable consequences; compact interior
`a`; no endpoint law; no numerical expansion; no model promotion/freeze. The
`ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate is sharpened to an explicit
non-circular assumption set; the terminal states a **conditional** closure, not
a theorem, and no terminal authorizes production-domain implementation or
stationary KFE.

**Completion:** explicit-stage only the exact nine Issue #45 allowlist paths,
commit, push the dedicated branch
`dsh/issue-45-dlh-5s-scaled-tail-p2-realization-2026-09-02`, and **STOP for
fresh ChatGPT review**.
