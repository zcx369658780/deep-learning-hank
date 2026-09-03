# Deep Learning + HANK Task Index

Status: `NO_ACTIVE_BUILDER_ISSUE__DLH_5S_ACCEPTED__OWNER_ROUTE_DECISION_REQUIRED`

Last synchronized: 2026-09-03

Repository: `zcx369658780/deep-learning-hank`

## Builder authority

**NONE.**

Issue #45 / DLH-5S is accepted and CLOSED completed. DSH must remain stopped until the Owner selects a next scientific route and a successor Issue is separately published, CURRENT Task Index / Startup Snapshot are synchronized to it, and an authoritative activation comment is posted.

Chat text alone does not create Builder authority.

## Latest accepted task — Issue #45 / DLH-5S

Title:

`DLH-5S: Analyze provisional-S3 pre-asymptotic dynamics and p=2 realization`

Task type:

`SCIENTIFIC_THEORY_ANALYSIS__PROVISIONAL_S3_PREASYMPTOTIC_DYNAMICS_AND_P2_REALIZATION`

Accepted candidate:

`160781a89c6e22b5f17b4259500893140fcb9c01`

Reviewer acceptance comment:

`5519142363`

Acceptance integration commit:

`75bedf6e3bb97d024dc8af3afa30f7398f205846`

Acceptance level:

`L3_COMMIT_VERIFIED__SCIENTIFIC_THEORY_ANALYSIS_ACCEPTED`

Accepted reviewer verdict:

`DLH_5S_REV3_ACCEPTED__OUTCOME_B_CONFIRMED__SCALED_TAIL_STRUCTURE_ACCEPTED__P2_REALIZATION_REMAINS_OPEN`

Accepted terminal:

`DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED`

## Accepted DLH-5S scientific state

Accepted household source remains immutable/read-only:

`src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`

Git blob:

`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`

Binding Issue #27 law remains:

```text
HJB boundary policy <=> KFE boundary transition law
```

Stationary KFE remains **NOT AUTHORIZED**.

Accepted DLH-5S theory-analysis content:

1. Exact scaled variables and identities:
   - `H=-bV`
   - `Q=b^2 V_b`
   - `H_s=H-Q`
   - `c/b=Q^(-1/2)`
   - `p_eff=2-dlog(Q)/dlog(b)` where regular.
2. Exact scaled HJB:
   - `(rho I-S)H=F(Q)+E`
   - `F(Q)=2sqrt(Q)-r_b Q`.
3. Exact vector Q-flow:
   - `F'(Q)Q_s=F(Q)-rho Q+S Q+E-E_s`.
4. Reduced `E=0`, z-symmetric scalar system has the positive fixed point
   - `K*=4/(rho+r_b)^2=3265.3061224489797`,
   - on the reduced regular lower sector,
   - with local homogeneous mean eigenvalue `-7` near `K*`.
5. The local homogeneous z-difference eigenvalue near the candidate is about `-273.67`; this is not a generic full-HJB convergence rate.
6. If `E->0` and `E_s->0`, the asymptotically autonomous limit is the **E=0 z-coupled vector system** `F'(Q)Q_s=F(Q)-rho Q+S Q`; the scalar z-symmetric dynamics are an invariant subsystem / conditional asymptotic reduction only after z-difference synchronization.
7. `Q->K*>0` alone does not imply `p_eff->2`; derivative-regular convergence such as `dlog(Q)/dlog(b)->0` is additionally required.
8. S1+S2+S3 do **not** establish:
   - scaled-tail upper tightness / precompactness of Q;
   - Q non-degeneracy;
   - eventual regular-lower-sector branch selection;
   - `E_s->0`;
   - coupled-global synchronization / omega-limit basin entry.
9. No analytic obstruction/counterexample was established; provisional S3 remains falsifiable working authority and is not promoted/frozen.
10. DLH-5R finite-window directions are qualitatively compatible with, but do not prove, eventual p=2 realization.

## Owner checkpoint after DLH-5S

No next route is selected yet. A future Owner decision may choose, for example:

- further bounded analytic work on tightness / compactness / coupled basin entry;
- a separately authorized numerical diagnostic of the remaining scaled-tail conditions without silently enlarging the domain;
- return to model-defining R/W domain and joint HJB/KFE boundary-law design while preserving the unresolved asymptotic caveat;
- defer p=2 realization work and hold at the current provisional scientific boundary.

Any such route requires new explicit authority. Do **not** create a successor Issue automatically.

## Scientific ceiling at this checkpoint

Until a new Owner route decision and exact successor authority exist, do not:

- mutate accepted household economics/source;
- reopen b160 or create a larger numerical domain;
- choose/implement R/W/W1/W2/`W_max`;
- invent endpoint/state-domain laws;
- run stationary KFE/nullspace/pin/density/tail mass/aggregates;
- enter regional GE / multi-province execution;
- train neural networks;
- enter nominal HANK, calibration, policy, welfare, or Results.

Current Startup Snapshot:

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`

Current Master Roadmap:

`docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md`
