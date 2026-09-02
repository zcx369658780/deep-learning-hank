# DLH-5S — Theorem-Status Matrix and Terminal (Phase H)

**Issue #45, Phase H.** One matrix over the gate's components, then exactly one
terminal.

## 1. Theorem-status matrix

| # | Component | Status | Supporting file / result |
|---|---|---|---|
| 1 | Exact scaled identities | **EXACT** | `DLH_5S_SCALED_VARIABLE_IDENTITIES.md`: `dH/ds=H-Q`, `c/b=Q^(-1/2)`, `p_eff=2-dlogQ/dlogb`, `m=Q/H`, `dlogH/ds=1-m` |
| 2 | Exact scaled HJB | **EXACT** | `DLH_5S_REMAINDER_BOOTSTRAP...`: `(rho-S)H=F(Q)+E`, `F(Q)=2sqrt(Q)-r_b Q`, S-sign verified |
| 3 | Exact remainder decomposition | **EXACT** | `DLH_5S_AUTHORITY_FREEZE.md` + Remainder file: `E = E_labor+E_illiquid+E_transfer_adj`, all signs audited, no `o(1/b)` assumption |
| 4 | Exact vector Q-flow | **EXACT** | Remainder file: `F'(Q)dQ/ds = F(Q)-rho Q + S Q + E - dE/ds`; reduces to the candidate formula for `E=0,S=0` (verified) |
| 5 | Scalar reduced-system fixed point | **EXACT** | `DLH_5S_SCALAR_REDUCED_DYNAMICS.md`: `H*=Q*=K*=4/(rho+r_b)^2=3265.3061224489797`; `(0,0)` degenerate; K* on lower branch |
| 6 | Scalar local stability | **EXACT (reduced)** | eigenvalue `-7` in s on lower branch (stable node, `b^(-7)` approach) |
| 7 | Scalar basin/trapping result | **EXACT (reduced)** | lower branch `(0, 1/r_b^2)`; `Q<K* => Q` increasing; `K*<Q<1/r_b^2 => Q` decreasing; upper branch run-away at `Q>1/r_b^2`; `Q=0` repelling |
| 8 | z-mode stability | **LINEARIZED/LOCAL** | `DLH_5S_Z_MODE_STABILITY.md`: mean eigenvalue `-7`, difference eigenvalue `-273.67` (strongly damped), `Delta_H` slaved; coefficient synchronization conditional |
| 9 | Remainder smallness `E->0` | **CONDITIONAL (non-circular)** | follows from S3 + `Q`-bounded + compact a (`E_labor=O(b^(-7/5))`, `E_illiquid=O(1/b)`, `E_transfer_adj=O(1/b)`); NOT from S3 alone |
| 10 | Derivative-remainder `dE/ds -> 0` | **CONDITIONAL (class B)** | needs bounded `dlogQ/ds`, `H_a`, `R` along the flow |
| 11 | Asymptotic autonomy | **CONDITIONAL** | given 9+10; limit system = reduced scalar (mean) dynamics |
| 12 | S3 sufficiency vs extra assumptions | **S3 ALONE INSUFFICIENT** | S3 gives `R=O(1)` and R-decay of E once Q-bounded; Q-tightness/branch-selection/derivative-control/no-exotic are extra (B) |
| 13 | p=2 realization | **NOT CLOSED from S1+S2+S3**; conditional given B-assumptions | sharpest non-circular blocker: scaled-tail tightness of `Q` (upper + non-degenerate) + lower-branch selection |
| 14 | Coefficient convergence (`Q->K*`, `c/b->0.0175`) | **CONDITIONAL** | mean-mode rate `-7` in s given 9-11 |
| 15 | Exclusion of broader exotic tails | **NOT CLOSED** | open `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gate; sharpened here to explicit no-exotic-forcing assumption (B); no in-class counterexample constructed |
| 16 | Endpoint / full-support authority | **NOT CLOSED / OUT OF SCOPE** | compact interior a only; `a=10` law, `b_lo` law, `a=0` corner = Owner decision (unchanged from DLH-5Q) |
| 17 | Compatibility with DLH-5R finite-window evidence | **QUALITATIVE ONLY** | `DLH_5S_PREASYMPTOTIC_INTERPRETATION.md`: `c/b=Q^(-1/2)` reproduced to reported precision; directions all p=2-facing; reduced flow slower-than-observed indicates active negative remainder; compatibility is not proof |

## 2. Route recommendation / sharpening relative to DLH-5Q

DLH-5S sharpens the DLH-5Q `ASYMPTOTIC_REALIZATION / NO-EXOTIC-REGIME` gap from
"broader non-power/exotic tails are not excluded" to a **precise, non-circular,
minimal condition set**:

```text
(i)  scaled-tail tightness: Q = b^2 V_b bounded above on the compact-interior-a tail
(ii) non-degeneracy: Q bounded away from 0 and away from 1/r_b^2 (branch turning point)
(iii) eventual lower-branch selection
(iv) derivative-remainder control: dE/ds -> 0 uniformly
(v)  absence of persistent exotic/oscillatory forcing (z-difference decay + no NO-EXOTIC-REGIME counterexample)
```

Each is explicit and non-circular (does not assume `Q->K*`, `H->K*`, or
`V_b~K*/b^2`). Under (i)-(iii) and (iv)-(v), the exact scaled machinery
guarantees: `E->0`, asymptotic autonomy, and tracking of the reduced lower-branch
p=2 attractor (`Q->K*` at rate `b^(-7)` in the limit, with z-difference damped
at `b^(-273.67)`). None of (i)-(iii), (iv)-(v) follows from S1+S2+S3 alone.

**The conditional analytic closure is materially strengthened** relative to the
generic DLH-5Q gap: the missing ingredients are no longer a vague "no exotic
regime"; they are exactly the tightness/branch-selection/derivative/no-exotic
inputs enumerated above, with the reduced attractor and z-damping verified.

## 3. Terminal (exactly one)

```text
DLH_5S_SCALED_TAIL_DYNAMICS_SUPPORT_P2_ATTRACTOR__MINIMAL_NONCIRCULAR_REALIZATION_ASSUMPTIONS_IDENTIFIED__NO_NUMERICAL_EXPANSION_NEEDED
```

**Justification (mapping to the pre-registered Outcome A criteria):**

1. *Reduced/coupled dynamics are correctly derived* — YES: exact scaled HJB,
   exact vector Q-flow, candidate `dQ/ds` identity verified as exact, z-mode
   mean/difference decomposition with verified `S` sign.
2. *p=2 is an attracting candidate in the relevant branch* — YES: stable lower-
   branch node with eigenvalue `-7` in s, basin `(0, 1/r_b^2)`, z-difference
   strongly damped (`-273.67`); `K* = 3265.3061224489797` verified.
3. *Remaining assumptions are explicit, non-circular, and materially sharper
   than the generic DLH-5Q "no exotic regime" gap* — YES: the five-condition
   set above, each class-B (not class-C), with the exact role of each shown.

**Explicitly NOT claimed:**
- p=2 realization is **not** proved from S1+S2+S3 alone; the closure is
  **conditional** on the identified non-circular assumptions.
- This is **not** a theorem acceptance, a model freeze, or a domain
  implementation; provisional S3 remains falsifiable working authority.
- No terminal in this Issue authorizes endpoint laws, R/W/W1/W2/`W_max`,
  production-domain implementation, or stationary KFE.
- Outcome B is not selected because the transformed dynamics ARE correctly
  derived and the gap IS sharpened to a minimal non-circular set (A's criteria);
  Outcome C is not selected because no analytic contradiction/counterexample is
  demonstrated; Outcome D is not selected because interior realization is not
  closed to theorem level (tightness/branch selection remain class-B inputs).

**Route note:** no numerical-domain expansion is needed for this structural
conclusion (and none is authorized). Any future attempt to *verify* tightness
numerically would require a new Owner decision and successor authority, which
DSH does not create.
