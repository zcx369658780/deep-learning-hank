# DLH-5S / Issue #45 — Provisional-S3 Pre-Asymptotic Dynamics and p=2 Realization

**Task type:** `SCIENTIFIC_THEORY_ANALYSIS__PROVISIONAL_S3_PREASYMPTOTIC_DYNAMICS_AND_P2_REALIZATION`
**Date:** 2026-09-02; **bounded Rev 2:** 2026-09-03 (per fresh review `5516660741`)
**Branch:** `dsh/issue-45-dlh-5s-scaled-tail-p2-realization-2026-09-02`
**Fresh `origin/main` baseline:** `20dc202547f3d7a21bbe80c843c442bc986983a3`
**Authoritative activation comment (Issue #45):** `5510733437`
**Owner route decision:** `APPROVE_R_C1_BOUNDED_ANALYTIC_ASYMPTOTIC_REALIZATION_CLOSURE__NO_NUMERICAL_DOMAIN_EXPANSION` (Issue #44 comment `5510675566`)
**Accepted predecessor:** Issue #44 / DLH-5R, candidate `6b79b7b1ff388174b5460a32de547a25ecb8a097`, acceptance `5510368753`, integration `96f0adb855233da06e96b71c6d8b6fe6aa540fc7`.

**This is analytic theory work only.** No new HJB/grid execution, no rerun of
J0-J5 as new evidence, no domain expansion, no stationary KFE, no endpoint law,
no R/W/W1/W2/`W_max` choice. Builder completion is not theorem acceptance;
provisional S3 remains falsifiable working authority.

**Rev 2 corrections (review `5516660741`):** (a) the claimed fixed-`labor0`
finite-grid convention is withdrawn — the accepted solver uses the **same
endogenous labor FOC** on B/F branches; (b) S3 implies **no sign** of `R`/`V_a`,
so `E_illiquid` is `O(1/b)` in magnitude with undetermined sign; (c) the DLH-5R
`Q` range is "compatible with the reduced lower-sector `Q`-range", not "on the
lower branch"; (d) slower-than-reduced motion does **not** identify `E<0` (net
forcing is `S Q + E - E_s`); (e) `-7` / `-273.67` are homogeneous/local
eigenvalues, not full-HJB rates; (f) `E_s -> 0` is a primitive assumption, not a
consequence of level boundedness; (g) "minimality" is withdrawn; (h) the
terminal is re-selected A -> B (controlling tightness/branch-selection/basin
remains unproved).

---

## 1. Controlling authority (verified)

- Accepted immutable household source blob `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` (verified at HEAD).
- Controlling theory: `docs/theory/DLH_5Q_PROVISIONAL_S3_TAIL_THEOREM_AND_FALSIFICATION.md`.
- Evidence context: `reports/dlh_5r_provisional_s3_hjb_tail_falsification_2026_09_02/`.
- Provisional working authority: S1 (base class: `V<0`, `V_b>0`, bounded `V_inf`), S2 (`V_inf=0`, provisional), S3 (`R=V_a/V_b=O(1)`, **no sign restriction**), P-TR sensitivity `R=o(sqrt(b))`, critical `R~Theta(sqrt(b))` outside S3 as benchmark.

## 2. Executive summary

1. **Phase A — exact HJB decomposition.** From the accepted interior HJB
   `rho*V = u + (r_b b + labor - c)V_b + r_a_eff a V_a + V_b[d(R-1)-chi] + S V`
   (endogenous labor `l=(0.85 z V_b)^(1/5)`, `c=V_b^(-1/2)`), the exact identity
   `rho*V = -2 sqrt(V_b) + r_b b V_b + S V + REM_FULL` holds with
   `REM_FULL = L(V_b,z) + r_a_eff(a) a V_a + V_b[d(R-1)-chi]`,
   `L(V_b,z) = (5/6)(0.85 z V_b)^(6/5)` (labor net surplus). Signs audited; no
   `o(1/b)` assumed at the outset. **Labor: solver and analytic theory use the
   same endogenous FOC; the fixed-labor0 claim is withdrawn.** S3 carries no
   sign of `R`/`V_a`; the transfer active-branch expression is exact in general
   bare-a form and simplified only under `a_min > a_bar`.
2. **Phase B — exact scaled identities.** With `H=-bV`, `Q=b^2 V_b`, `s=log b`:
   `dH/ds = H - Q`, `c/b = Q^(-1/2)`, `p_eff = 2 - dlogQ/dlogb`, `m=Q/H`,
   `dlogH/ds = 1 - m`. None of these imply `V_inf=0`, control `H/b`, or imply
   p=2; they are exact bookkeeping.
3. **Phase C — exact scaled HJB.** `(rho I - S)H = F(Q) + E` with
   `F(Q) = 2 sqrt(Q) - r_b Q`, `E = -b REM_FULL`, and the exact remainder
   `E = E_labor + E_illiquid + E_transfer_adj`:
   `E_labor = -(5/6)(0.85z)^(6/5) Q^(6/5) b^(-7/5) < 0`;
   `E_illiquid = r_a_eff(a) a H_a = -r_a_eff(a) a R Q/b` — **magnitude `O(1/b)`
   under S3+bounded-Q+compact-a, sign NOT determined by S3**;
   `E_transfer_adj = (Q/b)[chi - d(R-1)]` — non-positive under `a_min > a_bar`
   (simplified form, not globally exact). **S3 alone does NOT imply `E->0`**;
   `E->0` (magnitude) follows from S3 + `Q`-bounded + compact `a` (non-circular).
4. **Phase D — scalar reduced dynamics.** Reduced (z-symmetric, `E=0`) system:
   branches `Q_±(H)` with turning point `(H,Q) = (1/(rho r_b), 1/r_b^2) =
   (3333.3, 4444.4)`; fixed points `(0,0)` and `(K*,K*)` with
   `K* = 4/(rho+r_b)^2 = 3265.3061224489797` (verified, on the reduced lower
   branch; unique positive fixed point in the regular lower sector). The
   candidate `dQ/ds = Q[2-(rho+r_b)sqrt(Q)]/[1-r_b sqrt(Q)]` is **verified
   exact**. K* is a stable node with **homogeneous** eigenvalue `-7` in s
   (`b^(-7)` approach for the *unforced* reduced system); reduced basin
   `(0, 1/r_b^2)`; `Q<K* => Q` increasing; upper branch `Q>1/r_b^2` is run-away.
5. **Phase E — z-modes.** Mean/difference decomposition with `S` spectrum
   `{0,-2/3}`: **homogeneous** mean eigenvalue `-7`, **homogeneous**
   z-difference eigenvalue `-273.67` in s (strongly damped), `Delta_H` slaved to
   `Delta_Q`; coefficient synchronization holds conditionally. These are
   unforced/local relaxation rates — **no generic full-HJB rate is claimed**
   (a slowly-decaying forcing can dominate; forcing-rate options are explicit in
   Phase F). No nonresonance assumption needed at linear order; the DLH-5Q
   O(1/b) nonresonance `(rho+r_b)/2 = 0.0175 notin {0,-2/3}` is preserved.
6. **Phase F — bootstrap.** The exact vector Q-flow is
   `F'(Q) dQ/ds = F(Q) - rho Q + S Q + E - dE/ds`; the **net forcing is
   `S Q + E - E_s`**, whose sign is not identified from the accepted medians. A
   full compact-interior-a p=2 realization theorem does **not** close from
   S1+S2+S3. The controlling unproved objects are the explicit non-circular
   sufficient conditions: (i) scaled-tail precompactness / `Q` upper tightness,
   (ii) `Q` away from 0, (iii) regular lower sector (`F'(Q_z) >= delta > 0`,
   i.e. positive distance below `1/r_b^2`), (iv) `E->0` uniformly (derived from
   (i)+S3+compact-a), (v) `E_s -> 0` uniformly (primitive derivative-remainder
   assumption), (vi) coupled-limit/omega-limit basin entry into the positive
   p=2 attractor of the `E=0` coupled limit system. Each is classified
   (A/B/C/D); none is circular; no in-class counterexample (D) was constructed;
   no formal minimality is claimed.
7. **Phase G — DLH-5R interpretation.** The accepted medians are exactly
   consistent with the identities: `c/b = Q^(-1/2)` (reproduced to reported
   precision), `p_eff = 2 - dlogQ/dlogb < 2` with `Q` increasing, and the
   reduced lower-branch prediction `Q<K* => Q` increasing. The observed `Q`
   range is **compatible with the reduced lower-sector `Q`-range**. The observed
   trajectory is **qualitatively compatible** with a long pre-asymptotic
   approach to the p=2 attractor, but the reduced flow is faster than observed —
   the full-system remainder/coupling materially modifies/retards the motion
   (**net sign not identified**; no labor-convention explanation). Compatibility
   is **not** proof.
8. **Phase H — matrix and terminal.** See below (terminal re-selected A -> B).

---

## 3. Terminal (exactly one)

```text
DLH_5S_P2_REALIZATION_NOT_CLOSED__SCALED_TAIL_TIGHTNESS_OR_BRANCH_SELECTION_REMAINS_UNPROVED__OWNER_ROUTE_DECISION_REQUIRED
```

**Selection rationale (pre-registered Outcome B criteria):** (1) the
reduced/coupled scaled dynamics are useful and correctly derived (exact HJB,
exact vector Q-flow, candidate `dQ/ds` identity verified as exact, z-mode
decomposition with verified `S` sign, reduced attractor `K*` with homogeneous
eigenvalue `-7`, homogeneous z-difference damping `-273.67`); (2) but the
**controlling unproved object** — scaled-tail tightness of `Q`, non-degeneracy,
regular-lower-sector branch selection, `E_s -> 0`, and the coupled
basin-entry/omega-limit condition — remains an **assumption**, not a
consequence of S1+S2+S3. After Rev 2 (withdrawal of the S3-sign, net-remainder-
sign, branch-classification, and full-HJB-rate overclaims), the package does not
close interior p=2 realization to theorem level; per the pre-registered rule,
Outcome A must not be forced, so the terminal is **B** (Owner route decision
required for any future step toward establishing tightness/basin). Outcome C is
not selected (no obstruction/counterexample constructed); Outcome D is not
selected (interior realization not closed).

**What this terminal does NOT claim:**
- p=2 realization is **not** proved from S1+S2+S3 alone; the closure is
  **conditional** on the explicit non-circular sufficient set, whose controlling
  elements are unproved assumptions.
- S3 is **not** promoted or frozen; it remains falsifiable working authority.
- No endpoint law, R/W/W1/W2/`W_max`, production-domain implementation, or
  stationary KFE is authorized by this terminal.
- DSH does not create the successor/owner decision; it only records that one is
  required.

---

## 4. Deliverables (Issue #45 allowlist, exactly nine)

1. `docs/theory/DLH_5S_SCALED_TAIL_DYNAMICS_AND_P2_REALIZATION.md` (this file)
2. `reports/dlh_5s_scaled_tail_dynamics_p2_realization_2026_09_02/DLH_5S_AUTHORITY_FREEZE.md`
3. `.../DLH_5S_SCALED_VARIABLE_IDENTITIES.md`
4. `.../DLH_5S_SCALAR_REDUCED_DYNAMICS.md`
5. `.../DLH_5S_Z_MODE_STABILITY.md`
6. `.../DLH_5S_REMAINDER_BOOTSTRAP_AND_ASYMPTOTIC_AUTONOMY.md`
7. `.../DLH_5S_PREASYMPTOTIC_INTERPRETATION.md`
8. `.../DLH_5S_THEOREM_STATUS_MATRIX_AND_TERMINAL.md`
9. `.../DLH_5S_FORBIDDEN_OPERATION_CHECK.md`

No existing tracked file was modified. No numerical execution was performed.
