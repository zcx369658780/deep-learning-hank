# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.36  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT DLH-5V-E ACTIVE — REMAINING REGULAR W-BOUNDARY SECTOR CLOSURE

---

## 0. Long-run objective

Build a hybrid structural–learned regional HANK platform in which household HJB/KFE, aggregation, firm/accounting and later nominal-HANK equations remain explicit structural economics, while hard-to-specify cross-regional mappings become learned modules only after the household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains regional labor/spatial mapping `W^L`. Neural training remains downstream.

---

## 1. Accepted household / finite-domain foundation

Accepted household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted finite production-domain family:

```text
D_W(W_max) = {0<=a<=a_max, b>=b_min, a+b<=W_max}
```

Accepted continuous W-face tangent law:

```text
mu_W = mu_a + mu_b <= 0.
```

Restricted-Voronoi cells remain the state partition / mass-volume geometry. The same controlled backward generator `Q` must define the discrete HJB transition term and forward mass dynamics `p_dot=Q^T p`.

---

## 2. Accepted regular-frontier geometry — DLH-5V-A / Issue #49

Accepted candidate `58a0efe2e85b497d8b19c306a831d865ed65136d`; reviewer acceptance `5628285587`; integration `46d6961100d1a050e6b313fa2e321180ed255226`.

Exact grid:

```text
da=10/19, db=7/19, da/db=10/7.
```

Regular W-frontier phase is period 7. Endpoints/corners remain separately deferred.

---

## 3. Accepted local shared-face obstruction — DLH-5V-B / Issue #50

Accepted candidate `6bc8612dc10de6d72d27c9c47d1b4d598a70a15d`; reviewer acceptance `5628629099`; integration `ff0afdf6d3fa0d770654613e42109318d638639d`.

Accepted local shared-face cones:

```text
A^F: K = {7 mu_a + 10 mu_b <= 0}
A^L: K = {mu_a <= 0, 7 mu_a + 10 mu_b <= 0}
B^W: K = R^2.
```

Exact sliding `(-u,+u)` is outside recurring top-cell shared-face cones. This rejected shared-face-only transition geometry but did not invalidate the W-domain or every W1 discretization.

---

## 4. Accepted forward wide-stencil regular feasibility — DLH-5V-C / Issue #51

Accepted candidate `2134a4b249eb0a79dc20d60ba1fdee830304f261`; reviewer acceptance `5630191586`; integration `cdbf1906963a9bf06cf117ba63072d2f1542d501`.

Accepted primitive exact tangent:

```text
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19).
```

For regular W-active states with `j>=7`, destination `(j-7,i+10)` is represented, path stays in `D_W`, `a+b` is constant, and period-7 class/top-subtop offset are preserved. Lower-a endpoint band `j in {0,...,6}` is deferred.

Together with local inward `w_in=(-10/19,0)`, this closes

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}.
```

---

## 5. Accepted `T_realloc` control-dependent rate / generator contract — DLH-5V-D / Issue #52

Issue #52 is CLOSED completed.

Accepted candidate:

`81705b0c1671a8ee09ee5c2f05953f3e4f9f1e8b`

Reviewer acceptance:

`5631523081`

Acceptance integration:

`d58bd962be3acc8b6f646b66643bbc96f121be57`

Accepted verdict:

`DLH_5VD_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

For every admissible candidate in `T_realloc`:

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10.
```

These rates are exact, nonnegative and unique, and score the candidate in discrete `H_h` before selection. The gate does not freeze the global regular-W-boundary argmax because the remaining regular sector is still open.

Conservative one-Q semantics are frozen:

```text
Q_ij>=0 for i!=j
Q_ii=-sum actual represented outgoing rates
Q1=0 by construction
future forward operator = exactly Q^T.
```

---

## 6. Independent KFE methodology cross-check

The separately stabilized Chapter-5 clean/source-free KFE implementation reinforces, but does not replace, project authority:

```text
Q backward; Q^T forward
off-diagonal >=0
diagonal = -sum actual outgoing
Q1=0
same Q HJB/KFE
mass-first stationary object
SCC/closed recurrent classes before uniqueness
original source-free residual downstream
pin/normalization != leakage repair.
```

MATLAB-faithful contaminated-row reproduction logic is not imported. Issue #27 component-pin authority remains unchanged.

---

## 7. Owner continuation decision

Owner approved:

`APPROVE_DLH_5VE_REMAINING_REGULAR_W_BOUNDARY_SECTOR_CLOSURE_GATE`

The active gate closes only the remaining recurring **regular** W-frontier sectors. Endpoint/joint-boundary states remain separate and downstream.

---

## 8. Active gate — DLH-5V-E / Issue #53

Task type:

`SCIENTIFIC_DESIGN__REMAINING_REGULAR_W_BOUNDARY_SECTORS_AND_FULL_REGULAR_SCORING_CLOSURE`

Dedicated branch:

`dsh/issue-53-dlh-5ve-remaining-regular-sector-2026-09-11`

### 8.1 Remaining sector

The full regular tangent cone is

```text
T_W={mu_W<=0}.
```

The accepted sector is

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}.
```

The exact remaining sector is

```text
T_rem={mu_b<0,mu_W<=0}
```

with

```text
R_reverse={mu_a>0,mu_b<0,mu_W<=0}
R_deplete={mu_a<=0,mu_b<0}.
```

### 8.2 Reverse reallocation candidate

Audit, do not assume:

```text
(Delta j,Delta i)=(+7,-10)
w_RT=(+70/19,-70/19)
(j,i)->(j+7,i-10).
```

Required objects:

- exact represented-destination conditions;
- lower-b / upper-a / joint-boundary exclusions;
- full straight-path admissibility in `D_W`;
- `r_{j+7}=r_j` and class/top-subtop preservation if valid;
- exact nonnegative first-moment representation.

Candidate rates to prove/refute:

```text
q_RT   = 19*mu_a/70
q_down = 19*(-mu_W)/7.
```

If feasible, freeze a reverse-sector candidate scoring rule in discrete `H_h`; do not freeze a separate sector argmax.

### 8.3 Both-inward depletion candidate

Audit the purely local basis

```text
w_left=(-10/19,0)
w_down=(0,-7/19)
```

and candidate rates

```text
q_left = 19*(-mu_a)/10
q_down = 19*(-mu_b)/7.
```

Prove/refute exact coverage, uniqueness, equality cases and represented local destinations on the regular region.

### 8.4 Full regular closure target

If both sub-sectors pass, prove that every continuously admissible regular W-face candidate with `mu_W<=0` has a coherent, single-valued sector-specific rate/scoring contract, with shared boundaries assigned consistently.

Only then freeze the future regular composition:

```text
all admissible regular candidates
 -> sector-specific discrete-H_h scores
 -> ONE global regular argmax
 -> selected control + already-defined rates
 -> ONE conservative backward Q
 -> future KFE consumes exactly Q^T.
```

No HJB solve is authorized in this gate.

---

## 9. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
local shared-face moment cone                                OBSTRUCTION ACCEPTED
forward exact-tangent wide-stencil feasibility               ACCEPTED
T_realloc control-dependent rates + conservative Q           ACCEPTED
remaining regular W-boundary sectors                         ACTIVE (DLH-5V-E)
endpoint / joint-boundary closure                            PENDING
boundary-HJB / finite-process implementation                 PENDING
global discrete-HJB implementation                           PENDING
same-process Q validation + SCC diagnostics                  PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

---

## 10. Downstream route if DLH-5V-E passes

```text
full recurring regular W-frontier sector contracts accepted
-> endpoint/joint-boundary closure
-> boundary-HJB / finite-process implementation
-> one-Q same-process validation + SCC/closed-class diagnostics
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> Issue #27 stationary KFE
-> stationary aggregates
-> two-region structural anchor rebuild
-> 3–5 province integration
-> learned W^L
```

If a recurring regular-sector obstruction is proved, return to Owner route decision rather than hiding it downstream in KFE.

---

## 11. Planned conversation handoff checkpoint

Because the present conversation is already long, the selected handoff checkpoint is **immediately after Issue #53 is independently accepted and post-acceptance governance is synchronized**.

Before handoff, update:

1. `tasks/TASK_INDEX_CURRENT.md`;
2. `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`;
3. this Master Roadmap;
4. a dedicated current project/session handoff snapshot recording live `main`, accepted candidate/integration SHAs, Issue states, KFE safeguards, unresolved endpoint/joint-boundary work, and the exact next route.

Also generate a current project-source handoff Markdown/ZIP if useful, so the next conversation does not depend on long-chat memory.

This checkpoint is scientifically natural because it closes the full recurring regular W-frontier design block before endpoint/joint-boundary work begins.

---

## 12. Scientific ceiling during DLH-5V-E

Do not mutate accepted economics/source; change production grid/aspect ratio; implement/execute mirror or local remaining-sector transitions; assemble production `Q`; execute HJB/KFE/stationary; redesign endpoint/joint-boundary states; select numerical `W_max`; redesign Issue #27 pinning; import contaminated-row KFE production logic; compute aggregates/GE; enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
