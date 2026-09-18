# DLH-WL-P1A — Frozen-household evidence registry (read-only)

Issue: **#74 / `DLH-WL-P1A`** — OPEN / ACTIVE / OPERATIVE.
Owner route: **`DLH-WL-V1-20260918`**.
Authority marker: `DLH_WL_P1A_OFFLINE_ACCOUNTING_AND_HOUSEHOLD_REGISTRY_AUTHORIZED`.
Operative baseline: **`e046feccf9f98adad0d7db713eca427e0e7f1e36`**.

This registry **records existing repository evidence only**. No household solver,
HJB, KFE, GE, MATLAB or training code was executed to produce it; the household
solver was deliberately **not** run to "complete" the registry. Evidence sources
are the current contracts, the governance snapshot/handoff on the operative
baseline, and static file/git metadata of the named source files.

Fields that existing evidence does not support are marked `NOT_VERIFIED`. Nothing
here creates a solved-checkpoint claim, a new applicability range, or a new API
declaration.

---

## 1. Frozen reference objects and accepted provenance

| Object | Path | Identity |
|---|---|---|
| reference household oracle | `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py` | git blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` |
| independent experimental selected-Q | `src/deep_learning_hank/two_asset/boundary_hjb_selected_q.py` | git blob `7857cabb4d28af99cb9d59e2d1c3024b05787c11` |
| Issue #69 audit module | `src/deep_learning_hank/two_asset/f0_rate_path_divergence_audit.py` | git blob `83e9be0febcc03eb721265d3558887bd6b1586a4` |
| Issue #71 residual-decomposition module | `src/deep_learning_hank/two_asset/route_a_hjb_residual_decomposition.py` | git blob `96dd262a4ae42e26d489a317d9a04a9264b481b1` |
| Issue #72 bounded solver-design module | `src/deep_learning_hank/two_asset/route_a_bounded_solver_design.py` | git blob `f99ff6eb0d0a74cccc400ba83162a8affa9c6924` |

Historical accepted household commit (Issue #23):
`b038db800da3760cebee484b1c7a76bf7c1529d0`; the oracle blob at that commit is
`76ae5b149993a7edeeb8eb337f1b02b3fe33c51e`, i.e. **identical** to the blob at the
operative baseline. No oracle change since #23 is evidenced.

### 1.1 Reference SHA-256 of the oracle — verified, with one encoding caveat

The frozen dependency contract states reference SHA-256
`1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`.

Static verification on the operative baseline:

| Measurement | Value |
|---|---|
| git blob (canonical content) | `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` — **matches the contract** |
| SHA-256 of the git blob bytes (LF, 29 065 bytes) | `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024` — **matches the contract** |
| SHA-256 of the on-disk Windows working-tree file (CRLF, 29 714 bytes) | `620C43919A2F1E33DA39147F39C6CC6932AABD4002886274CA4484EE0666BF4C` |

Interpretation: the contract's reference hash is the **canonical LF** hash of the
accepted blob. The difference on disk is purely the repository's
`core.autocrlf=true` checkout conversion (649 CRLF line endings), not a content
change. During this Issue **no hash was recomputed to make a check pass** and no
protected hash was rewritten; the discrepancy is recorded as an encoding fact.

### 1.2 Issue #73 module identity — `NOT_VERIFIED`

`docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md` lists retained identities for the
oracle, selected-Q, #69, #71 and #72 modules. It does **not** name a #73 module
blob. The #73 module present on the operative baseline is:

```
src/deep_learning_hank/two_asset/route_a_one_step_projected_regularized_newton.py
git blob 59676b1becf6e49226cfc40f3bb84aa8b908c694
```

**`NOT_VERIFIED`**: no accepted-artifact registry entry names this blob. It is
recorded as an observed identity, not as an accepted one. The #73 accepted
candidate/integration commit remains
`838764a9a489b771de852a684a2d2cc99703c168` (Reviewer acceptance `5728591018`,
integration `5728595318`), and that is the durable accepted-artifact anchor for
the #72 guard.

---

## 2. Freeze classification carried forward (unchanged)

| Class | Meaning | Status in this Issue |
|---|---|---|
| **A** | economic equations / state domain / boundary / policy selection / operator and convergence definitions are frozen | inherited unchanged; **not** re-audited, **not** re-run, **not** modified |
| **B** | code identity, interface/unit/ordering/failure and provenance registration | inherited; the actual I/O, ordering, failure fields and validation configuration of the household remain **`NOT_VERIFIED`** at field level (see §5) |
| **C** | for a specific use, an accepted HJB + final same policy/Q + legal terminal distribution + aggregation bound to one checkpoint | **no new C in this Issue**; none of the historical C claims is re-used as truth here |

Repository files touched by this Issue are **outside** the household package:
`src/deep_learning_hank/regional/labor_destination.py` and its test file. The
`two_asset` package was read as text for identity/registry purposes only.

### 2.1 Known unfrozen production gaps (carried forward, not resolved)

- the limited-domain family `0 <= a <= 10`, `b >= -2`, `a + b <= W_max` is an
  **experimental contract**; the production `W_max` has **not** been selected;
- historical price-sampling passes are not a theorem over a price interval
  (**no** established applicable price range);
- the selected-Q fixed-point gap remains open;
- unbounded-control / state-constraint applicability remains open.

---

## 3. Known allowed read-only uses

| Use | Boundary |
|---|---|
| reading source code, contracts, historical artifact identities | allowed within task scope |
| using a **given** exogenous labor total to test the `W^L` accounting interface | allowed and independent: no household call, and the output must **not** be described as an equilibrium outcome |
| static `git`/file/`AST` metadata inspection of the household package | allowed (this registry) |
| keeping ONE MATLAB-faithful selected generator as the governing solve/validation object | retained; this Issue neither changes nor exercises it |

---

## 4. Known unsupported or forbidden uses

| Use | Status |
|---|---|
| using the #73 candidate as optimal-policy truth, training label, GE household solution or welfare baseline | **forbidden** — the candidate is not an HJB solution; residual `10.435094313164921 -> 10.435094286652339`, `HJB convergence = FALSE`, `material reduction <= 0.5 = FALSE` |
| using any intermediate Q's stationary mass to claim the HJB is solved | **forbidden** |
| calling the reference oracle under new prices/grids as an economic solution | requires purpose-specific evidence and separate authorization; a single tested point does not extend to a continuous range |
| Dual-Q semantics | **forbidden**; ONE selected-Q only |
| stationary KFE, GE / learned-HANK coupling | **not authorized**; separate check required before P4 |
| full-suite / historical Issue #73 experiment / solver refinement | **not authorized** in this Issue (solver-refinement budget is 0) |
| importing accepted/frozen state, parameters, code, checkpoints or acceptance from the neighbouring dissertation project | **forbidden**; the Owner-provided cross-project guide transfers method only |
| treating code freeze as convergence | **forbidden** — Freeze-A/B does not imply a solved household |

---

## 5. Interface / provenance fields — explicit verification status

Recorded because the frozen contract requires P1 to register the real I/O, ordering
and failure fields from existing evidence. Fields without supporting evidence are
`NOT_VERIFIED` rather than invented:

| Field | Status |
|---|---|
| contract/version, grid/domain, numerics provenance | exists in the household module's own dataclasses/numerics containers (static reading confirmed the presence of `EconomicParams`, `HouseholdInputs`, `MatlabFaithfulHJBGrid`, `MatlabFaithfulHJBNumerics`, `MatlabFaithfulHJBResult`); exact accepted values **`NOT_VERIFIED`** here |
| structural I/O of a household solve | static surface only: `solve_household_steady_state(...)` and `solve_matlab_faithful_hjb(...)` exist; **accepted input ordering, units and defaults `NOT_VERIFIED`** |
| ordering / unit declarations actually enforced at runtime | **`NOT_VERIFIED`** — would require executing the household, which this Issue must not do |
| failure taxonomy of the household/HJB path in runtime terms | only the existence of fail-closed types is visible statically (`BoundaryHJBFailure`, and result containers such as `MatlabFaithfulHJBResult` / `MatlabFaithfulKFEResult`); the **runtime mapping of failure reasons is `NOT_VERIFIED`** |
| validation configuration behind historical accepted states | **`NOT_VERIFIED`**; no re-run was performed |
| stationary mass / aggregates availability | **unavailable** unless a legal accepted use exists; this Issue provides none and does not run KFE |
| wage / return / tax / transfer unit conventions for household inputs | **`NOT_VERIFIED`** |
| applicable price range for the frozen oracle | **`NOT_VERIFIED`** (no established interval) |

Deliberate non-actions that keep this list honest: no KFE run "for interface
completeness", no solver run to fill a field, no import of any scientific module
to probe an API.

---

## 6. Purpose registration for the P1A deliverable

| Purpose | Boundary |
|---|---|
| offline conditional destination-share accounting (`W^L`), given `m` and `ell` | **authorized by #74**; implemented in `src/deep_learning_hank/regional/labor_destination.py`, fully offline, no household call |
| household-dependency evidence registry | **authorized by #74**; this file, read-only |
| learning/training `W^L` (any architecture, loss, split or budget) | **not authorized**; requires a later activated Issue with pre-frozen configuration and budget |
| economic coupling of a learned `W^L` into HJB/KFE/GE | **not authorized**; requires purpose-adapted household evidence, one legal same-process Q, a legal terminal distribution, accounting evidence and explicit authorization |
| empirical identification of annual bilateral OD flows | **not claimed**; two-region cases are accounting-only and non-degenerate conditional learning would need at least three regions |

---

## 7. Sources read for this registry

- `docs/contracts/DLH_FROZEN_HOUSEHOLD_DEPENDENCY_CONTRACT_CURRENT.md` (operative baseline);
- `docs/contracts/DLH_WL_CONDITIONAL_DESTINATION_V1_CURRENT.md`;
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`;
- `docs/handoffs/DLH_SESSION_HANDOFF_CURRENT.md` and
  `docs/handoffs/DLH_SESSION_HANDOFF_POST_5VY_2026_09_18.md`;
- `docs/roadmaps/DLH_MASTER_ROADMAP_CURRENT_2026_09_01.md` (locked route block);
- `docs/decisions/DLH_OWNER_ROUTE_FREEZE_WL_V1_2026_09_18.md` and
  `docs/governance/DLH_ROUTE_LOCK_MANIFEST.json`;
- GitHub Issue #74 full body plus both comments (staging and final activation);
- static `git`/file metadata of the five named `two_asset` modules and the #73 module;
- `src/deep_learning_hank/regional/__init__.py` and the existing regional package listing.

Route-lock verification performed at the operative baseline (static only):

```
Owner decision blob 038aad696dc66eeacabdf25bd7b96a49bd9d9c4c
Owner decision SHA-256 4b87eab29d46e8e53d5da77a7c6210cc9dbaee5b12d852379528d36c25ebd38c  == manifest  PASS
Roadmap locked block SHA-256 4d2ef5c125bfbf0bbb59bbb416734485ad3df6b4c4b50b17c760d4718b555ce8 == manifest  PASS
locked block byte-identical to the original publication 01daaf10c5854437870039a46435a075c664d9a3    PASS
no route amendment present
```

This registry does not change the Owner route, any contract, or any hash.
