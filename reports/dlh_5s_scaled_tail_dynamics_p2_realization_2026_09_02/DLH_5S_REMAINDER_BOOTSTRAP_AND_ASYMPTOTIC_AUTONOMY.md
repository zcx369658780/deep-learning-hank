# DLH-5S — Scaled HJB, Remainder, and Bootstrap / Asymptotic Autonomy (Phases C & F)

**Issue #45, Phases C & F (bounded Rev 2 per review `5516660741`).** Derives
the exact scaled HJB and normalized remainder, then tests whether a
non-circular asymptotic-autonomy closure of the p=2 realization follows from
S1+S2+S3 — and, where it does not, records the precise sufficient condition set
that would close it.

## 1. Exact scaled HJB (Phase C)

Multiply the exact decomposition (Phase A)
`rho*V = -2*sqrt(V_b) + r_b*b*V_b + S*V + REM_FULL` by `-b`, using
`H=-bV`, `Q=b^2 V_b`, `b*sqrt(V_b)=sqrt(Q)` (b>0), `S` z-only
(`-b*S*V = S*H`):

```text
rho*H = 2*sqrt(Q) - r_b*Q + S*H - b*REM_FULL

(rho*I - S) H = F(Q) + E,
F(Q) = 2*sqrt(Q) - r_b*Q,
E(b,a,z) = -b * REM_FULL(b,a,z)
```

**S-sign convention verified:** the `S*V` term of the accepted HJB becomes
`+S*H` in scaled form and appears as `-S*H` on the left, i.e. the operator is
`(rho - S)`. On the mean (eigenvalue 0) it is `rho`; on the z-difference
(eigenvalue -2/3) it is `rho + 2/3` (used in Phase E).

## 2. Exact remainder components (every term derived; signs only where determined)

From `REM_FULL = L(V_b,z) + r_a_eff(a)*a*V_a + V_b*[d*(R-1) - chi]`
(Phase A), with `V_a = R*V_b = R*Q/b^2` and `H_a = -b*V_a`:

```text
E = E_labor + E_illiquid + E_transfer_adj

E_labor(b,a,z)        = -b * L(V_b,z)
                      = -(5/6) * (0.85*z)^(6/5) * Q^(6/5) * b^(-7/5)       < 0
E_illiquid(b,a,z)     = -b * r_a_eff(a)*a*V_a
                      = r_a_eff(a) * a * H_a
                      = -r_a_eff(a) * a * R * Q / b                         (magnitude O(1/b); sign open)
E_transfer_adj(b,a,z) = -b * V_b * [d*(R-1) - chi]
                      = (Q/b) * [chi - d*(R-1)]
```

**Sign audit (corrected):**
- `E_labor < 0`: exact (labor net surplus `L > 0` enters `rho*V` positively,
  hence `E = -b*REM` negatively).
- `E_illiquid`: **magnitude `O(1/b)` under S3 + bounded Q + compact interior
  a**; **sign is NOT determined by S3 alone**, because S3 (`R = V_a/V_b = O(1)`)
  carries no sign restriction on `R` or `V_a`. Any signed statement about
  `E_illiquid` requires an independent, explicitly-labelled sign assumption (or
  the accepted numerical evidence `R > 0`, `V_a = R*V_b > 0` on the accessible
  states — evidence, not an S3 implication). This package makes **no** analytic
  sign claim for `E_illiquid`.
- `E_transfer_adj = (Q/b)[chi - d*(R-1)]`: on the **active** bare-a transfer
  branch, `q = R-1` satisfies `q = sign(d)*chi_0 + chi_1*d/a`, so exactly
  `chi - d*q = 0.5*chi_1*d^2/max(a,a_bar) - chi_1*d^2/a`, i.e.
  `E_transfer_adj = (Q/b)[0.5*chi_1*d^2/max(a,a_bar) - chi_1*d^2/a]`. For
  `a >= a_bar` this is `-(Q/b)*0.5*chi_1*d^2/a <= 0`. The simplified
  non-positive form is valid only under the explicit **compact-interior scope
  `a_min > a_bar`** and is **not** globally exact. On the inaction branch
  (`|R-1| <= chi_0`) `d=0` and the term is 0.
- **No global sign of `E`** is inferred in this package. (The DLH-5Q/analytic
  `E_labor < 0` plus the scope-restricted non-positive `E_transfer_adj` plus
  an *empirically* positive `R` would point to `E < 0` on the evidence states,
  but that is evidence, not a theorem, and the net forcing of the flow is
  `S Q + E - E_s` anyway — see section 4.)

**z-symmetric vs z-dependent:** `E_labor` carries `z` explicitly (through
`(0.85 z)^(6/5)`); `E_illiquid` and `E_transfer_adj` carry `z` only through
`H_a`, `R`, `Q`, `d`. In mean/difference decomposition (Phase E) `Delta E`
drives the z-difference mode; `E_bar` drives the mean mode.

## 3. Remainder magnitude — the weakest sufficient conditions

Do **not** assume p=2. The following are sufficient for `E -> 0` in **magnitude**
(with `a` on a fixed compact interior set `a_min > a_bar` for the simplified
transfer form):

- **(R1) S3:** `R = O(1)` uniformly.
- **(R2) Scaled-tail tightness (upper):** `Q = b^2*V_b` bounded above uniformly
  on the tail.
- **(R3) compact interior a** (given by the gate scope).

Then:

```text
E_labor      = O(Q^(6/5) * b^(-7/5)) = O(b^(-7/5))      -> 0
E_illiquid   = -r_a_eff(a)*a*R*Q/b   = O(1/b)           -> 0   (magnitude)
E_transfer_adj = (Q/b)[chi - d(R-1)] = O(1/b)           -> 0   (d, chi bounded under R1+R3)
```

**Statement:** under S3 + Q-bounded + compact a, `E -> 0` in magnitude,
uniformly in s. This uses only R1 (S3), R2 (new tightness), R3 (scope). It does
**not** assume p=2 and is **non-circular**. **S3 alone does NOT imply `E->0`**:
without R2, `Q` could grow (e.g. `V_b` decaying slower than `1/b^2`), in which
case the decay rates above fail.

**Derivative-remainder (corrected).** `E -> 0` alone does **not** give
`E_s -> 0`; differentiation introduces `R_s`, `d_s`, `chi_s`, `Q_s`. Bounded
**levels** of `R`, `d`, `chi`, `H_a` are **not** sufficient. Preferred clean
authority: treat

```text
E_s -> 0 uniformly          (primitive class-B derivative-remainder assumption)
```

as a primitive non-circular assumption. Optionally it may be derived from
componentwise regularity strong enough to imply it, e.g. uniform boundedness of
`R_s` and `d_s`, `chi_s`, plus bounded `Q_s` (equivalently bounded
`d log Q/d s`) and bounded `H_a`, `R`, `d`, `chi` along the flow; but this
package does **not** silently derive `E_s -> 0` from level boundedness alone.

## 4. Exact vector Q-flow (asymptotic-autonomy limit system)

Differentiate the scaled HJB `(rho - S)H = F(Q) + E` in `s` (commuting with the
z-only `S`) and substitute the exact kinematic identity `dH/ds = H - Q`
(Phase B):

```text
(rho - S) dH/ds = F'(Q) dQ/ds + dE/ds
(rho - S)(H - Q) = F'(Q) dQ/ds + dE/ds
[F(Q) + E] - (rho - S) Q = F'(Q) dQ/ds + dE/ds

F'(Q) dQ/ds = F(Q) - rho*Q + S*Q + E - dE/ds,
F'(Q) = 1/sqrt(Q) - r_b
```

This is the **exact vector scaled-tail flow** (a system across z), valid away
from `F'(Q)=0` (`Q != 1/r_b^2`) wherever the s-differentiation is legitimate.

- **Reduced limit (E=0, S=0, z-symmetric):** reduces exactly to the Phase D
  candidate formula
  `dQ/ds = Q[2 - (rho+r_b) sqrt(Q)]/[1 - r_b sqrt(Q)]` — cross-check PASS.
- **Mean-mode linearization at K\*:** `dQ_bar/ds = -7 (Q_bar - K*) +
  400 (E_bar - dE_bar/ds)` (Phase E) — the **local** homogeneous eigenvalue
  with remainder forcing, valid near the candidate.
- **Asymptotic autonomy (corrected, Rev 3):** if `E -> 0` and `E_s -> 0`
  uniformly (R1–R3 + primitive derivative-remainder assumption), the system is
  asymptotically autonomous with limit system the **E=0 z-coupled vector
  system** `F'(Q) Q_s = F(Q) - rho Q + S Q` — NOT automatically the scalar
  mean dynamics, because `F` is nonlinear and mean/difference modes do not
  decouple in general. The scalar z-symmetric reduced system is exactly (a) an
  **invariant/reduced subsystem** of that limit (the `Delta_Q = 0` surface is
  invariant), and (b) an **asymptotic reduction** only **conditional on
  z-difference synchronization** (`Delta_Q -> 0`), an unproved class-B
  condition (Phase F).
- **Net forcing interpretation (corrected).** The realized motion of the full
  system is driven by the **net forcing** `S Q + E - E_s`, not by `E` alone.
  Observed motion slower than the unforced `E=0, S=0` reduced flow therefore
  does **not** imply `E < 0`; the sign of the net forcing is **not identified**
  from the accepted DLH-5R medians alone. Statements of the form "negative E
  retards the approach" are withdrawn in favor of: "the nonzero full-system
  remainder/coupling materially modifies or retards the accessible-range motion;
  its net sign is not identified from the accepted medians alone."

## 5. Bootstrap theorem attempt — condition classification (Phase F)

Attempt a full compact-interior-a p=2 realization theorem from S1+S2+S3+HJB.
For each candidate condition, classify: **A** derivable from S1+S2+S3+HJB;
**B** genuinely new but non-circular sufficient assumption; **C** circular
(effectively assumes p=2); **D** false / contradicted by a construction.

| # | Candidate condition | Needed for | Classification |
|---|---|---|---|
| 1 | Exact scaled identities (`dH/ds=H-Q`, `p_eff=2-dlogQ/dlogb`, `c/b=Q^(-1/2)`) | bookkeeping | **A** (mechanical) |
| 2 | Exact scaled HJB `(rho-S)H = F(Q)+E` and exact Q-flow | limit system | **A** (given regularity to differentiate) |
| 3 | p=2 fixed point `K* = 4/(rho+r_b)^2`, lower-branch stability (homogeneous eigenvalue -7), reduced basin `(0,1/r_b^2)`; **uniqueness of the positive fixed point in the regular lower sector** | attractor identification | **A** (reduced-system algebra; only fixed points in `(0,1/r_b^2)` are `(0,0)` and `(K*,K*)`) |
| 4 | z-difference homogeneous damping (eigenvalue -273.67) and coefficient synchronization | z-constant leading coefficient | **A at linear order**; global/nonlinear version needs 5-7 |
| 5 | `Q = b^2 V_b` bounded above (scaled-tail tightness, upper) | E_labor->0, E_illiquid->0, E_transfer->0 (magnitude) | **B** (NOT implied by S1+S2+S3) |
| 6 | `Q` bounded away from 0 (non-degeneracy) | F'(Q) regular, c/b bounded, exclude Q->0 branch | **B** (NOT implied by S1+S2+S3) |
| 7 | Regular lower sector: `Q` stays a positive distance below `1/r_b^2`, i.e. `F'(Q_z) >= delta > 0` (eventual lower-branch selection) | exclude reduced-singularity and upper-branch runaway | **B** (NOT implied by S1+S2+S3) |
| 8 | `R=O(1)` uniform | S3 (given); magnitude of E_illiquid, E_transfer | **A** (S3, given) |
| 9 | `E -> 0` uniformly in magnitude | asymptotic autonomy | **A given 5+8+compact-a** (derived); NOT from S3 alone |
| 10 | `E_s -> 0` uniformly (derivative-remainder control) | asymptotically autonomous limit | **B** (primitive; or derived from bounded/decaying `R_s`, `d_s`, `chi_s`, `Q_s` — not from levels alone) |
| 11 | Coupled-limit / omega-limit basin condition: the full trajectory enters and stays in the basin of the positive p=2 fixed point of the **`E=0` z-coupled vector limit system** `F'(Q) Q_s = F(Q)-rho Q+S Q` (regular lower sector, with z-difference synchronization `Delta_Q -> 0`) | place trajectory in the attractor's basin | **B** (non-circular; replaces the vague "absence of persistent exotic forcing") |
| 12 | `Q -> K*`, `H -> K*`, `V_b ~ K*/b^2`, `c/b -> 0.0175` | conclusion | **C** (circular — must NOT be assumed) |
| 13 | any in-class S3 counterexample to the attractor picture | falsification | **D** (none constructed; consistent with DLH-5Q) |

**Controlling unproved object.** The theorem does **not** close from S1+S2+S3
alone. The controlling unproved objects are exactly the class-**B** items:
**scaled-tail tightness of `Q`** (5), **non-degeneracy** (6), **regular lower
sector / branch selection** (7), **derivative-remainder `E_s -> 0`** (10), and
the **coupled-limit/omega-limit basin condition** (11). None follows from
S1+S2+S3, none is circular (none assumes `Q->K*`, `H->K*`, or `V_b~K*/b^2`),
and no in-class counterexample (**D**) was constructed among the correctly
analyzed families.

**Uniqueness of the positive fixed point in the regular lower sector (recorded,**
**derivable as A):** in the reduced scalar system on the regular lower sector
`(0, 1/r_b^2)` with `F'(Q) > 0`, the only fixed points of `H = Q` are `Q = 0`
(repelling, degenerate) and `Q = K*` (attracting). Hence in the regular lower
sector the positive p=2 fixed point is **unique**. What remains missing is the
**coupled-global** statement: for the full `E != 0`, z-coupled flow, a
verified omega-limit/basin entry condition (11) that the trajectory reaches the
regular lower sector and is captured by K* — not merely the uniqueness/local
stability of K* in the reduced system. That coupled-global result is the
explicitly stated open item.

**Language (corrected):** the assumption set is presented as an **explicit
non-circular sufficient dynamical condition set** — no formal minimality is
claimed (necessity/minimality of any single condition is not proved here).

## 6. What S3 alone does and does not give

- **Does give:** `R=O(1)` (by definition); with `Q` bounded, the **magnitude**
  `E_illiquid = O(1/b)` and `E_transfer_adj = O(1/b)` (under `a_min > a_bar`);
  the exact scaled structure.
- **Does NOT give:** `Q`-boundedness (tightness), `Q` away from 0 / from the
  singularity, regular-lower-sector branch selection, `E_s -> 0`, or the
  coupled-limit/basin entry. Hence S3 alone does NOT imply `E->0` as a theorem,
  does NOT imply the trajectory is captured by the p=2 attractor, and does NOT
  imply p=2 realization.
