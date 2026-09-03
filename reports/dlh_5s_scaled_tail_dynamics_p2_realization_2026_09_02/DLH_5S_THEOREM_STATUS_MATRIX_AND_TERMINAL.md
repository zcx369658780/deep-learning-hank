# DLH-5S — Theorem-Status Matrix and Terminal (Phase H)

**Issue #45, Phase H (bounded Rev 2 per review `5516660741`).** One matrix over
the gate's components, then exactly one terminal. Rev 2 withdraws the overclaims
flagged by the review (labor convention, S3 sign, branch classification, net-
remainder sign, full-HJB rates, "minimality") and re-selects the terminal.

## 1. Theorem-status matrix

| # | Component | Status | Supporting file / result |
|---|---|---|---|
| 1 | Exact scaled identities | **EXACT** | `DLH_5S_SCALED_VARIABLE_IDENTITIES.md`: `dH/ds=H-Q`, `c/b=Q^(-1/2)`, `p_eff=2-dlogQ/dlogb`, `m=Q/H`, `dlogH/ds=1-m`; do NOT imply S2 or control `H/b` |
| 2 | Exact scaled HJB | **EXACT** | `DLH_5S_REMAINDER_BOOTSTRAP...`: `(rho-S)H=F(Q)+E`, `F(Q)=2sqrt(Q)-r_b Q`, S-sign verified |
| 3 | Exact remainder decomposition | **EXACT** | `DLH_5S_AUTHORITY_FREEZE.md` + Remainder file: `E = E_labor+E_illiquid+E_transfer_adj`; `E_labor<0` exact; `E_illiquid` magnitude `O(1/b)` under S3+bounded-Q+compact-a, **sign not determined by S3**; `E_transfer_adj` non-positive under `a_min>a_bar` (simplified form, not globally exact) |
| 4 | Exact vector Q-flow | **EXACT** | Remainder file: `F'(Q)dQ/ds = F(Q)-rho Q + S Q + E - dE/ds`; reduces to the candidate formula for `E=0,S=0` (verified); **net forcing is `S Q + E - E_s`, no sign identified** |
| 5 | Scalar reduced-system fixed point | **EXACT** | `DLH_5S_SCALAR_REDUCED_DYNAMICS.md`: `H*=Q*=K*=4/(rho+r_b)^2=3265.3061224489797`; `(0,0)` degenerate; K* on the reduced lower branch; **uniqueness of the positive fixed point in the regular lower sector recorded** |
| 6 | Scalar local stability | **EXACT (reduced, local/homogeneous)** | **unforced local** eigenvalue `-7` in s near K* (stable node); local linearization only; NOT a global trajectory rate or a full-HJB rate |
| 7 | Scalar basin/trapping result | **EXACT (reduced)** | lower branch `(0, 1/r_b^2)`; `Q<K* => Q` increasing; `K*<Q<1/r_b^2 => Q` decreasing; upper branch run-away at `Q>1/r_b^2`; `Q=0` repelling |
| 8 | z-mode stability | **LINEARIZED/LOCAL** | `DLH_5S_Z_MODE_STABILITY.md`: **homogeneous** mean eigenvalue `-7`, **homogeneous** difference eigenvalue `-273.67`, `Delta_H` slaved; coefficient synchronization conditional; no generic full-HJB rate |
| 9 | Remainder magnitude `E->0` | **CONDITIONAL (non-circular)** | follows from S3 + `Q`-bounded + compact a (`E_labor=O(b^(-7/5))`, `E_illiquid=O(1/b)` magnitude, `E_transfer_adj=O(1/b)` under `a_min>a_bar`); NOT from S3 alone |
| 10 | Derivative-remainder `dE/ds -> 0` | **CONDITIONAL (class B)** | primitive assumption (or componentwise `R_s`, `d_s`, `chi_s`, `Q_s` regularity); **NOT derived from level boundedness** |
| 11 | Asymptotic autonomy | **CONDITIONAL** | given 9+10; limit system = **`E=0` z-coupled vector system** `F'(Q)Q_s = F(Q)-rho Q+S Q`; the scalar z-symmetric reduced system is an invariant subsystem / asymptotic reduction **conditional on z-difference synchronization** (Rev 3) |
| 12 | S3 sufficiency vs extra assumptions | **S3 ALONE INSUFFICIENT** | S3 gives `R=O(1)` and magnitude decay of E once Q-bounded; tightness/non-degeneracy/branch-selection/derivative-control/basin are extra (B) |
| 13 | p=2 realization | **NOT CLOSED from S1+S2+S3**; conditional given B-assumptions | controlling unproved objects: scaled-tail tightness of `Q`, non-degeneracy, regular lower sector / branch selection, `E_s->0`, coupled-limit/basin entry |
| 14 | Coefficient convergence (`Q->K*`, `c/b->0.0175`) | **CONDITIONAL** | no generic full-system rate; **local** homogeneous mean rate `-7` near K* only; forcing can dominate (Phase F forcing-rate options); `Q->K*>0` alone does not imply `p_eff->2` (needs `dlogQ/dlogb->0`) |
| 15 | Exclusion of broader exotic tails | **NOT CLOSED** | open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate; sharpened to an explicit coupled-limit/omega-limit basin condition (B) + uniqueness of the positive fixed point in the regular lower sector (A); no in-class counterexample constructed |
| 16 | Endpoint / full-support authority | **NOT CLOSED / OUT OF SCOPE** | compact interior a only (`a_min > a_bar` where the simplified transfer form is used); `a=10` law, `b_lo` law, `a=0` corner = Owner decision (unchanged from DLH-5Q) |
| 17 | Compatibility with DLH-5R finite-window evidence | **QUALITATIVE ONLY** | `DLH_5S_PREASYMPTOTIC_INTERPRETATION.md`: `c/b=Q^(-1/2)` reproduced to reported precision; directions all p=2-facing; observed range compatible with reduced lower-sector `Q`-range; full-system remainder/coupling modifies/retards the approach (net sign not identified); labor treatment identical in solver and theory |

## 2. Route recommendation / sharpening relative to DLH-5Q

DLH-5S sharpens the DLH-5Q `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gap from
"broader non-power/exotic tails are not excluded" to an **explicit, non-circular
sufficient dynamical condition set** (no formal minimality is claimed):

```text
(i)   scaled-tail precompactness / Q upper tightness: Q = b^2 V_b bounded above
      on the compact-interior-a tail
(ii)  Q bounded away from zero
(iii) eventual regular lower sector: Q stays a positive distance below 1/r_b^2,
      i.e. F'(Q_z) >= delta > 0 (lower-branch selection)
(iv)  E -> 0 uniformly (magnitude; non-circular under (i)+S3+compact-a)
(v)   E_s -> 0 uniformly (primitive derivative-remainder assumption)
(vi)  coupled-limit / omega-limit basin condition: the full trajectory enters and
      stays in the basin of the positive p=2 fixed point of the **`E=0` z-coupled
      vector limit system** `F'(Q)Q_s = F(Q)-rho Q+S Q` (regular lower sector,
      with z-difference synchronization `Delta_Q -> 0`)
```

Each is explicit and non-circular (none assumes `Q->K*`, `H->K*`, or
`V_b~K*/b^2`). Under (i)-(vi), the exact scaled machinery gives `E->0`,
asymptotic autonomy (limit = the `E=0` z-coupled vector system), and tracking
of its positive p=2 attractor (scalar z-symmetric invariant subsystem with
z-difference synchronization); the realized convergence rate is **not** asserted
generically (local homogeneous `-7` / `-273.67` only, or explicit forcing-rate
option in Phase F). None of (i)-(vi) follows from S1+S2+S3 alone.

**What is now materially sharper than DLH-5Q (honest statement):** the vague
"no exotic regime" gap is replaced by a precise condition set whose individual
roles are verified (tightness → E magnitude decay → asymptotic autonomy; reduced
attractor structure and uniqueness in the regular lower sector; z-difference
damping at linear order; explicit derivative-remainder and basin-entry
conditions). **What remains controlling and unproved:** the class-B objects
(i)-(iii), (v), (vi) — above all scaled-tail tightness and the coupled
basin-entry/branch-selection — are **assumptions**, not consequences of
S1+S2+S3. The package does **not** close interior realization to theorem level.

## 3. Terminal (exactly one)

```text
DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED
```

**Justification (mapping to the pre-registered Outcome B criteria):**

1. *The transformed dynamics are useful* — YES: exact scaled HJB, exact vector
   Q-flow, verified candidate `dQ/ds` identity, reduced attractor `K*` with
   **local** homogeneous eigenvalue `-7` (near K*) and reduced basin
   `(0,1/r_b^2)`, **local** homogeneous z-difference damping `-273.67`, and a
   materially sharper explicit sufficient condition set than DLH-5Q's generic
   gap.
2. *But the controlling unproved object remains the scaled-tail tightness /
   branch selection / coupled basin-entry* — YES: after Rev 2 (withdrawing the
   S3-sign, net-remainder-sign, branch-classification, and full-HJB-rate
   overclaims) and Rev 3 (local-only `-7`; conditional `p_eff -> 2`; asymptotic
   limit = `E=0` z-coupled vector system with scalar reduction conditional on
   z-difference synchronization), S1+S2+S3 alone do **not** establish (i)-(iii),
   (v), (vi). In
   particular the trajectory's entry into the p=2 attractor's basin (of the
   `E=0` z-coupled limit) is an
   assumed coupled-limit/omega-limit condition, not a derived consequence. This
   is exactly Outcome B's trigger: "the transformed dynamics are useful but
   S1+S2+S3 cannot establish the needed scaled-tail tightness, branch selection,
   remainder decay, or asymptotic compactness."
3. *Outcome A not selected*: A would require that the remaining assumptions be
   "materially sharper" **and** that the closure genuinely holds conditional on
   them with the controlling object resolved. Here the controlling object
   (basin entry / tightness / branch selection) remains an unproved assumption
   requiring further work or Owner route decision; A would overstate the
   package. A is not forced.
4. *Outcome C not selected*: no genuine analytic obstruction/counterexample was
   constructed (consistent with DLH-5Q).
5. *Outcome D not selected*: interior realization is **not** closed to theorem
   level (tightness/branch selection/basin entry remain class-B inputs).

**Explicitly NOT claimed:**
- p=2 realization is **not** proved from S1+S2+S3 alone; the closure is
  conditional on the explicit non-circular sufficient set, whose controlling
  elements are unproved assumptions.
- This is **not** a theorem acceptance, a model freeze, or a domain
  implementation; provisional S3 remains falsifiable working authority.
- No terminal in this Issue authorizes endpoint laws, R/W/W1/W2/`W_max`,
  production-domain implementation, or stationary KFE.
- The terminal records that **Owner route decision is required** for any future
  step (e.g. a successor gate attempting to establish tightness/basin
  numerically or by a new analytic argument), which DSH does not create now.

**Route note:** no numerical-domain expansion is needed for (and none is
authorized by) this structural conclusion. Any future attempt to *verify*
tightness/basin numerically would require a new Owner decision and successor
authority.
