# Deep Learning + HANK — Current Master Roadmap

**Version:** V0.22  
**Date:** 2026-09-03  
**Project:** Deep Learning + HANK / Network-Structured Regional HANK (NSR-HANK)  
**Repository:** `zcx369658780/deep-learning-hank`  
**Status:** CURRENT OWNER-APPROVED ROUTE D — DLH-5T FINITE PRODUCTION-DOMAIN / SAME-PROCESS BOUNDARY DESIGN ACTIVE

---

## 0. Long-run objective

Build a data-to-structural-model calibration and regional-network HANK platform in which household HJB/KFE, aggregation, firm/accounting blocks and later nominal-HANK equations remain explicit structural economics, while difficult cross-regional mappings become interpretable learned modules only after household and equilibrium foundations pass scientific and numerical validation.

The first learned object remains the regional labor/spatial rule `W^L`; capital-network learning `W^K`, nominal HANK, calibration, policy and welfare remain downstream.

---

## 1. Accepted household foundation through DLH-5S

Accepted MATLAB-faithful household source:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding Issue #27 law:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED** until one controlled finite household process is separately selected, implemented and validated.

### Accepted DLH-5S / Issue #45

Accepted candidate:

`160781a89c6e22b5f17b4259500893140fcb9c01`

Reviewer acceptance comment:

`5519142363`

Acceptance integration:

`75bedf6e3bb97d024dc8af3afa30f7398f205846`

Accepted verdict:

`DLH_5S_REV3_ACCEPTED__OUTCOME_B_CONFIRMED__SCALED_TAIL_STRUCTURE_ACCEPTED__P2_REALIZATION_REMAINS_OPEN`

Accepted terminal:

`DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED`

Accepted exact scaled structure includes:

```text
H=-bV
Q=b^2 V_b
H_s=H-Q
c/b=Q^(-1/2)
p_eff=2-dlog(Q)/dlog(b)
(rho I-S)H=F(Q)+E
F'(Q)Q_s=F(Q)-rho Q+S Q+E-E_s
```

The reduced `E=0`, z-symmetric system has positive fixed point

```text
K*=4/(rho+r_b)^2=3265.3061224489797
```

with local homogeneous mean eigenvalue `-7`; the local homogeneous z-difference eigenvalue is about `-273.67`. These are local/unforced rates only. If `E,E_s->0`, the asymptotic limit is the **z-coupled vector system**, not automatically the scalar mean system.

S1+S2+S3 do not establish Q tightness, Q non-degeneracy, regular-sector selection, `E_s->0`, global z synchronization or p=2 basin entry. No analytic obstruction/counterexample was established. The infinite-domain p=2 realization caveat therefore remains unresolved and is preserved through Route D.

---

## 2. KFE interpretation entering Route D

The current KFE blocker is **not** the existence of singularity and is **not** MATLAB-style row contamination itself.

Accepted Issue #27 interpretation:

- a conservative generator is expected to be singular;
- MATLAB-style contaminated-row / pin normalization is allowed in principle as a numerical scale-fixing device;
- later stationary acceptance requires the ORIGINAL unmodified residual `Q^T g`, mass normalization, non-negativity and admissible-pin diagnostics;
- contamination is downstream of the controlled-process definition.

The material blocker exposed by DLH-5E is boundary-policy inconsistency: the accepted finite-grid HJB can request materially outward asset drift at artificial finite boundaries. A KFE-only conservative clipping rule would then describe a different controlled process. Route D therefore freezes the finite-domain HJB and KFE boundary law jointly before any stationary execution resumes.

---

## 3. Owner Route-D decision after DLH-5S

Owner selected:

`APPROVE_ROUTE_D_FINITE_PRODUCTION_DOMAIN_AND_JOINT_HJB_KFE_BOUNDARY_DESIGN`

Scientific interpretation:

1. preserve the unresolved infinite-domain p=2 caveat rather than treating it as theorem closure;
2. move to a transparent finite numerical production-domain contract;
3. prefer total-wealth truncation over the old rectangular upper-b cap;
4. use native `(a,b)` masked representation as the primary first design candidate;
5. define the HJB boundary problem and KFE transition law as the same controlled process;
6. retain contamination as downstream normalization only;
7. select future production-domain extent by pre-registered adequacy tests, not by convenience or PASS-seeking.

---

## 4. Immediate active gate — DLH-5T / Issue #46

### Name

**Finite Production-Domain Geometry and Same-Process HJB–KFE Boundary Contract**

Task type:

`SCIENTIFIC_DESIGN__FINITE_PRODUCTION_DOMAIN_AND_SAME_PROCESS_HJB_KFE_BOUNDARY_CONTRACT`

Dedicated branch:

`dsh/issue-46-dlh-5t-finite-domain-same-process-boundary-2026-09-03`

DLH-5T is **design-only**. It does not authorize implementation or numerical execution.

### 4.1 Primary production-domain candidate

```text
D_W(W_max) = {
    0 <= a <= a_max,
    b >= b_min,
    a+b <= W_max
}
```

Interpretation:

- `a<=a_max` retains the accepted illiquid-support/taper specification;
- `b>=b_min` is the economic liquid borrowing floor;
- `a+b<=W_max` is an artificial numerical production-domain truncation;
- `W_max` is not a household primitive, not a calibrated structural parameter and is not selected in DLH-5T.

### 4.2 Primary representation candidate — W1

Use native `(a,b)` tensor coordinates and represent only states satisfying `a+b<=W_max`.

Reason for the design preference:

- keep the economically important borrowing floor `b=b_min` coordinate-aligned;
- keep the accepted a-based taper in native coordinates;
- concentrate slanted-boundary/stencil complexity on the artificial numerical upper boundary rather than moving it onto the borrowing floor.

W2 `(a,W)` is not silently substituted if W1 proves incomplete; that requires an explicit future decision.

### 4.3 Continuous tangent-cone boundary laws

DLH-5T must derive/audit and, if scientifically coherent, freeze:

```text
a=0:          mu_a >= 0
b=b_min:      mu_b >= 0
a=a_max:      mu_a <= 0
a+b=W_max:    mu_W=mu_a+mu_b <= 0
```

All active constraints apply jointly at every feasible face intersection. Boundary controls must be obtained from the constrained Hamiltonian/KKT problem itself; unconstrained policy selection followed by clipping is forbidden.

### 4.4 Same-process law

Central Route-D identity:

```text
controlled process selected by boundary HJB
        ==
controlled process represented by KFE generator
```

Consequences:

- no KFE-only suppression of a materially outward HJB policy;
- every KFE off-diagonal transition corresponds to an admitted HJB-controlled transition;
- diagonals use only actually admitted represented rates;
- omitted masked destinations cannot leave retained exit rates;
- future KFE remains the adjoint `Q^T g` of the same backward generator `Q V`.

### 4.5 Wmax adequacy protocol

DLH-5T freezes a future nested-domain selection method, not a number. Future candidate domains must be evaluated in stages:

```text
HJB shared-interior policy stability
-> boundary influence localization
-> stationary-tail influence after KFE authorization
-> aggregate stability C,L,A,B
-> GE/two-region price-state stability
```

A production `W_max` should ultimately be the smallest pre-registered candidate satisfying all relevant accepted adequacy gates.

---

## 5. Expected sequence after DLH-5T

If DLH-5T reaches an implementation-ready design terminal, the intended household sequence is:

```text
DLH-5T finite-domain / same-process scientific design
-> separate boundary-consistent HJB implementation authority
-> boundary KKT/complementarity validation
-> nested Wmax / resolution robustness
-> conservative same-process generator implementation
-> Issue #27 stationary KFE validation
-> recurrent-class / nullspace / admissible-pin / original Q^T g residual
-> mass / non-negativity / stationary-tail diagnostics
-> recompute C,L,A,B
-> rebuild two-region structural anchor
```

No historical stationary aggregate is grandfathered.

A successor implementation Issue is **not** created automatically by Builder; DLH-5T must first be independently reviewed and accepted.

---

## 6. Regional / Deep Learning architecture after household recovery

The long-run hybrid architecture remains:

```text
learned regional mapping W^L
        ↓
composite regional wage / flow interface
        ↓
structural regional two-asset HA (HJB/KFE)
        ↓
C_i, L_i^home, A_i, B_i
        ↓
labor-flow allocation + structural firm block
        ↓
w_i, r_i^a
        ↓
outer equilibrium fixed point
        ↓
back to HA
```

Deep Learning does **not** initially replace HJB/KFE. The first learned object remains the interpretable interregional labor-allocation network; the HA block is the structural response operator inside the regional equilibrium loop.

Permanent scaling hierarchy remains:

```text
2-region unit fixture
-> 3–5 province integration fixture
-> 31-province empirical/source benchmark
-> learned W^L
-> later W^K / nominal HANK / calibration / policy / welfare
```

---

## 7. Scientific ceiling during DLH-5T

Do not:

- mutate accepted household/HJB/KFE/regional/GE source;
- execute HJB, KFE, stationary density or grid/domain experiments;
- choose a numerical `W_max`;
- reopen b160 / create b180 or b200 / alter grid or taper;
- implement W1 masking, KKT boundary controls or a conservative generator;
- run contamination/pin sensitivity experiments;
- compute stationary aggregates;
- rebuild two-region GE;
- run multi-province execution;
- train neural networks;
- enter nominal HANK, calibration, policy, welfare or Results;
- PR / merge / Issue close / successor Issue / self-accept from Builder.

Working scientific label remains **Network-Structured Regional HANK (NSR-HANK)**.

---

## 8. Governance status

Issue #46 / DLH-5T is the current intended Builder design task. Builder authority requires:

1. Issue #46 OPEN;
2. CURRENT Task Index / Startup identity synchronized;
3. authoritative activation comment present.

The Issue body is the exact task specification. Chat text alone does not create Builder authority.
