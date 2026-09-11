# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.35  
**Date:** 2026-09-11  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** POST-DLH-5V-D — `T_realloc` CONTROL-DEPENDENT RATE / CONSERVATIVE GENERATOR CONTRACT ACCEPTED; REMAINING REGULAR SECTOR NEXT

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

Accepted regular local adjacency includes left/down at all regular W-active classes, plus phase-dependent diagonal/shared-face neighbors. The physical displacement map is `((10/19) Delta j,(7/19) Delta i)`.

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

## 4. Accepted W1 forward wide-stencil regular feasibility — DLH-5V-C / Issue #51

Accepted candidate:

`2134a4b249eb0a79dc20d60ba1fdee830304f261`

Reviewer acceptance:

`5630191586`

Acceptance integration:

`cdbf1906963a9bf06cf117ba63072d2f1542d501`

Accepted primitive exact tangent:

```text
10 Delta j + 7 Delta i = 0
(Delta j,Delta i)=(-7,+10)
w_T=(-70/19,+70/19).
```

For regular W-active states with `j>=7`, destination `(j-7,i+10)` is represented, the straight segment stays in `D_W`, `a+b` is constant, and period-7 class/top-subtop offset is preserved. The finite lower-a endpoint band `j in {0,...,6}` remains deferred.

Together with local inward

```text
w_in=(-10/19,0),
```

the accepted cone satisfies

```text
cone{w_in,w_T}=T_realloc
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}.
```

The wide edge is a **boundary wide-stencil Markov transition**, not an ordinary shared-face FV flux. Under fixed-aspect refinement its physical jump is `O(h)` and drift-matching rate is `O(1/h)`.

---

## 5. Accepted `T_realloc` rate / generator contract — DLH-5V-D / Issue #52

Issue #52 is CLOSED completed.

Accepted candidate:

`81705b0c1671a8ee09ee5c2f05953f3e4f9f1e8b`

Reviewer acceptance:

`5631523081`

Acceptance integration:

`d58bd962be3acc8b6f646b66643bbc96f121be57`

Accepted verdict:

`DLH_5VD_ACCEPTED__OUTCOME_A_CONFIRMED__REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

Accepted terminal:

`DLH_5VD_REGULAR_REALLOCATION_CONTROL_DEPENDENT_RATE_AND_CONSERVATIVE_GENERATOR_CONTRACT_FROZEN__READY_FOR_REMAINING_REGULAR_SECTOR_GATE`

### 5.1 Candidate-control rate map

For every admissible candidate with drift in `T_realloc`:

```text
q_T  = 19*mu_b/70
q_in = 19*(-mu_W)/10.
```

The first moment is exact, rates are nonnegative, and the two-ray decomposition is unique. Under symbolic fixed-aspect refinement both rates scale by `1/h`.

### 5.2 Discrete-Hamiltonian semantics

DLH-5V-D freezes a **sector-candidate scoring rule**, not the global regular-W-boundary argmax. Each in-sector candidate is scored using its own rates inside the discrete `H_h` before maximization.

Continuously admissible candidates outside `T_realloc` remain in the future global HJB choice set. After all regular sectors receive accepted rate contracts, one global discrete-Hamiltonian argmax may choose among all sector-scored candidates.

### 5.3 Conservative one-Q contract

For any eventually selected candidate:

```text
Q_ij >= 0, i!=j
Q_ii = -sum of actual represented outgoing rates
Q1=0 by construction.
```

The exact selected backward `Q` is the sole future KFE process input; future forward operator is exactly `Q^T`. KFE must not rebuild boundary rates from drifts. Pin/normalization is downstream scale fixing only, never leakage repair.

---

## 6. Independent KFE methodology cross-check

The separately stabilized Chapter-5 two-asset HANK clean/source-free KFE implementation reinforces, but does not replace, project authority:

```text
Q backward; Q^T forward
off-diagonal >= 0
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

## 7. Current roadmap position

```text
MATLAB-faithful two-asset household economics                 ACCEPTED
finite W-domain + continuous tangent/KKT law                 ACCEPTED
same-process HJB <=> KFE principle                           ACCEPTED
restricted-Voronoi state partition                           ACCEPTED
regular W-frontier phase / adjacency                         ACCEPTED
local shared-face moment cone                                OBSTRUCTION ACCEPTED
W1 exact-tangent forward wide-stencil feasibility            ACCEPTED
T_realloc control-dependent rates + conservative Q           ACCEPTED (DLH-5V-D)
remaining admissible regular W-boundary sector(s)             NEXT BOUNDED GATE
endpoint / joint-boundary closure                            PENDING
full regular-boundary global discrete-HJB selection          PENDING UNTIL SECTORS CLOSE
boundary-HJB / finite-process implementation                 PENDING
KKT + same-process generator validation                      PENDING
nested Wmax / resolution robustness                          PENDING
conservative stationary-generator validation                 PENDING
Issue #27 stationary KFE                                     NOT AUTHORIZED
stationary C,L,A,B                                           PENDING
two-region structural anchor rebuild                         PENDING
3–5 province integration                                     PENDING
learned regional W^L                                         PENDING
```

---

## 8. Recommended next bounded gate — remaining regular sector

The regular tangent cone is

```text
T_W={mu_W<=0}.
```

The already closed sector is

```text
T_realloc={mu_a<=0,mu_b>=0,mu_W<=0}.
```

The exact remaining regular sector is

```text
T_rem = T_W \ T_realloc = {mu_b<0,mu_W<=0}.
```

It decomposes into:

```text
R_reverse = {mu_a>0,mu_b<0,mu_W<=0}
R_deplete = {mu_a<=0,mu_b<0}.
```

### 8.1 Reverse reallocation candidate

The mirror lattice tangent

```text
(Delta j,Delta i)=(+7,-10)
w_RT=(+70/19,-70/19)
```

is only a **candidate**. The next gate must prove/refute represented destination availability away from endpoint/joint-boundary regions, full path admissibility, period-7 class preservation, and exact cone/rate representation. It must identify precisely the finite regions near `b=b_min`, `a=a_max`, or other joint boundaries where the mirror edge cannot be used and defer them rather than forcing a regular failure.

For a target reverse-reallocation drift, a plausible symbolic decomposition to audit is

```text
mu = q_RT*w_RT + q_bdown*(0,-7/19),
```

with candidate coefficients inferred from first-moment matching. They are not accepted until the next gate proves them.

### 8.2 Both-inward depletion candidate

All accepted regular W-active classes have local left and down transitions. The next gate should audit whether

```text
w_left=(-10/19,0)
w_down=(0,-7/19)
```

already generate the full both-inward sector with unique nonnegative rates, avoiding unnecessary wide transitions.

### 8.3 Closure target

If both remaining sub-sectors pass, the gate may establish full **regular** W-face sector coverage:

```text
T_W = T_realloc union R_reverse union R_deplete
```

with sector-specific candidate scoring rules. Only then may the global regular-W-boundary discrete-Hamiltonian argmax be frozen over all admissible regular candidates, producing one selected control/rate row and one backward `Q` for later implementation/KFE handoff.

Endpoint/joint-boundary closure remains separate even if regular coverage closes.

---

## 9. Downstream route after regular-sector closure

If the remaining regular-sector gate passes:

```text
full regular W-face sector contracts accepted
-> endpoint/joint-boundary closure
-> boundary-HJB / finite-process implementation
-> same-process Q validation + SCC/closed-class diagnostics
-> Wmax/resolution robustness
-> conservative stationary-generator validation
-> Issue #27 stationary KFE
-> stationary aggregates
-> two-region structural anchor rebuild
-> 3–5 province integration
-> learned W^L
```

If a recurring regular-sector obstruction is found, return to Owner route decision rather than hiding it downstream in KFE.

---

## 10. Planned conversation handoff checkpoint

Because the present conversation is already long, choose the **post-remaining-regular-sector acceptance** point as the session handoff checkpoint. This is scientifically natural because it finishes one coherent block: all recurring regular W-frontier sectors.

Immediately before handoff, refresh:

1. `tasks/TASK_INDEX_CURRENT.md`;
2. `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`;
3. this Master Roadmap;
4. a dedicated current project/session handoff snapshot recording live `main`, accepted candidate/integration SHAs, Issue states, remaining endpoint/joint-boundary work, KFE safeguards, and the exact next authorized route.

A downloadable project-source handoff Markdown/ZIP should be generated at that checkpoint if useful, so the next conversation does not rely on long-chat memory.

---

## 11. Scientific ceiling

Until a successor Owner-authorized Issue is activated, do not mutate accepted household economics/source; implement the remaining-sector remedy; close endpoint/corner behavior; execute HJB/KFE/stationary; select numerical production `W_max`; compute aggregates/GE; or enter multi-province/neural/nominal/calibration/policy/welfare/Results.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.
