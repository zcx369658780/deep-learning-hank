# DLH-5S — Authority Freeze and Exact Continuum HJB Decomposition (Phase A)

**Issue #45, Phase A (bounded Rev 2 per fresh review `5516660741`).** Persists
the accepted interior continuum HJB and freezes the provisional working
authority. Analytic theory work only; no numerical execution.

## 1. Controlling accepted authority (verified read-only)

- Fresh `origin/main`: `20dc202547f3d7a21bbe80c843c442bc986983a3`
- Dedicated branch: `dsh/issue-45-dlh-5s-scaled-tail-p2-realization-2026-09-02`
- Issue #45 OPEN; activation `5510733437`
  (`APPROVE_R_C1_BOUNDED_ANALYTIC_ASYMPTOTIC_REALIZATION_CLOSURE__NO_NUMERICAL_DOMAIN_EXPANSION`).
- Controlling accepted predecessor: Issue #44 / DLH-5R, accepted candidate
  `6b79b7b1ff388174b5460a32de547a25ecb8a097`, reviewer acceptance `5510368753`,
  integration `96f0adb855233da06e96b71c6d8b6fe6aa540fc7`.
- Accepted theory package (read-only):
  `docs/theory/DLH_5Q_PROVISIONAL_S3_TAIL_THEOREM_AND_FALSIFICATION.md`.
- Accepted numerical evidence (read-only):
  `reports/dlh_5r_provisional_s3_hjb_tail_falsification_2026_09_02/`.
- Accepted household source (immutable): blob
  `76ae5b149993a7edeeb8eb337f1b02b3fe33c51e` (verified at HEAD).
- Stationary KFE remains NOT AUTHORIZED (Issue #27 contract binding).

## 2. Frozen provisional working authority (unchanged from DLH-5Q)

1. **S1 base:** fixed finite illiquid support, compact interior `a`; unbounded
   positive-`b` tail; accepted interior HJB; `V < 0`, `V_b > 0`, `V` increasing
   and bounded above so `V_inf(a,z) = lim_{b->+inf} V(b,a,z) in [-C,0]`.
2. **S2 selection (provisional):** `V_inf(a,z) = 0`. Not a proved necessity;
   not a comparison/uniqueness theorem.
3. **S3 primary derivative-control class:** `R = V_a/V_b = O(1)` uniformly over
   the claimed compact interior-`a` support. **S3 contains no sign restriction**
   on `R` (and hence none on `V_a`); signs, where used, must be stated
   separately and labelled.
4. **P-TR sensitivity envelope:** `R = o(sqrt(b))` is sensitivity only.
5. **Critical `R ~ Theta(sqrt(b))` family** remains outside S3, preserved as the
   exclusion-cost benchmark; not declared impossible.

DLH-5S does **not** promote or freeze S3; it analyzes what the accepted HJB can
and cannot imply about the long pre-asymptotic transition and eventual p=2
realization.

## 3. Exact accepted interior HJB (DLH-5Q combined form)

```text
rho*V = u + (r_b*b + labor - c)*V_b + r_a_eff(a)*a*V_a + V_b*[d*(R-1) - chi] + S*V,
R = V_a/V_b,
```

with the accepted read-only objects (verified against the immutable source):

- `u = c^(1-gamma_c)/(1-gamma_c) - sum_z w_z l_z^(1+phi)/(1+phi)`,
  `gamma_c = 2`, `phi = 5`, `w = labor_weights = [1.0]`;
- `c = V_b^(-1/2)` (consumption FOC, `consumption_from_vb`);
- `l = (V_b * 0.85 * z / w)^(1/5)` (labor FOC, `labor_from_vb`,
  `net_wage = wages*(1-tau-migration_costs)*z = 0.85 z`);
- `d = a*T(R-1)/chi_1`, `T(q) = min(q+chi_0,0) + max(q-chi_0,0)`
  (`transfer_candidate`, evaluated on **raw** `V_a,V_b`, no floor);
- `chi = chi_0*|d| + 0.5*chi_1*d^2/max(a,a_bar)` (`adjustment_cost`);
- `r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)` (`matlab_faithful_illiquid_return`);
- `r_b_eff = r_b + rb_gap*1_{b<0}` (b>0 tail: `r_b`);
- `mu_b = r_b*b + labor - d - chi - c`, `mu_a = r_a_eff(a)*a + d`;
- `S` = frozen two-state symmetric z-switch generator, rate `1/3`, spectrum
  `{0, -2/3}` (`switch_matrix = [[-1/3,1/3],[1/3,-1/3]]`).

Frozen anchors: `rho=0.02, r_b=0.015, r_a=0.03, chi_0=0.1, chi_1=2.0,
a_bar=1e-6, a_max=10, z in {0.8,1.3}`.

**Labor treatment (corrected per review `5516660741`).** The accepted
finite-grid solver and the analytic HJB use the **same endogenous labor FOC**.
`solve_matlab_faithful_hjb` passes the raw forward/backward `V_b` to
`select_matlab_faithful_local_policy`, which computes
`labor_b = labor_from_vb(vb_b, ...)` and `labor_f = labor_from_vb(vb_f, ...)`
and selects those endogenous controls on the B/F liquid branches;
`baseline_labor` is used only on the zero-liquid ("0") branch and in the
b-boundary marginal-utility closures. There is therefore **no
fixed-labor0-vs-endogenous-labor distinction** between the numerical solution
and the analytic theory. The only remaining finite-grid vs continuum
differences are: (i) upwind finite differences and the `MATLAB_DERIVATIVE_FLOOR`
applied to consumption/labor controls only (never to the transfer FOC), (ii)
the b-boundary marginal-utility closures, (iii) finite truncation at
`b_max`/`a_max`, and (iv) the discrete branch selection. None of these is used
here to "explain" the slow DLH-5R approach; that approach is analyzed purely
through the exact full-system remainder/coupling (Phase C/F).

## 4. Exact remainder decomposition (derived, not guessed)

Fold the labor income + labor disutility into the **labor net surplus**
(maximized over `l` given `V_b`):

```text
L(V_b,z) := max_l [ (1-tau)*w*z*l*V_b - w_z*l^(1+phi)/(1+phi) ]
          = (phi/(1+phi)) * [(1-tau)*w*z*V_b]^((1+phi)/phi)
          = (5/6) * (0.85*z*V_b)^(6/5)            (phi=5, (1-tau)w=0.85, w_z=1)
```

With `c = V_b^(-1/2)`:

```text
u + (labor - c)*V_b  =  [-1/c - c*V_b] + L(V_b,z)
                     =  -2*sqrt(V_b) + L(V_b,z)
```

Substituting into the accepted HJB gives the **exact identity** (no `o(1/b)`
assumption at the outset):

```text
rho*V = -2*sqrt(V_b) + r_b*b*V_b + S*V + REM_FULL
```

```text
REM_FULL(b,a,z) = L(V_b,z) + r_a_eff(a)*a*V_a + V_b*[d*(R-1) - chi]
```

with

```text
L(V_b,z)            = (5/6)*(0.85*z*V_b)^(6/5)                    > 0
r_a_eff(a)*a*V_a    = r_a*(1 - 0.1*(a/a_max)^9) * a * V_a          (sign of V_a open under S3)
V_b*[d*(R-1)-chi]   = transfer+adjustment net contribution
```

**Sign audit (every term; signs only where determined):**
- `-2*sqrt(V_b)` < 0: `u(c) - c*V_b = -V_b^(1/2) - V_b^(1/2)` (consumption flow
  net of `c*V_b`), exact for `gamma_c=2`.
- `+r_b*b*V_b` > 0: liquid-return term in `mu_b` (b>0 tail), exact.
- `+S*V`: z-switching; `S` acts on `z` only.
- `+L(V_b,z)` > 0: labor net surplus (income − disutility), exact for the
  endogenous labor FOC.
- `+r_a_eff(a)*a*V_a`: illiquid-return term, bounded in magnitude on compact
  interior `a` under S3; **sign not determined by S3 alone** (S3 does not imply
  `V_a > 0`).
- `+V_b*[d*(R-1)-chi]`: on the **active** bare-a transfer branch
  (`q = R-1`, `q = sign(d)*chi_0 + chi_1*d/a`), the exact expression is
  `d*(R-1) - chi = chi_1*d^2/a - 0.5*chi_1*d^2/max(a,a_bar)`; for `a >= a_bar`
  this reduces to `0.5*chi_1*d^2/a >= 0`. The simplified form is used only
  under the explicit **compact-interior scope `a_min > a_bar`** and is **not**
  called globally exact. On the inaction branch (`|R-1| <= chi_0`) `d=0` and
  the term is 0.

This is the **exact** decomposition used by every subsequent phase. No term is
assumed `o(1/b)` at this stage; the decay of `REM_FULL` (equivalently of the
normalized remainder `E`) is analyzed separately in Phase C/F.

## 5. What is frozen vs. assumed vs. open (per Issue #45 §4)

- **Identities (mechanical):** the decomposition above; the scaled-variable
  identities of Phase B; the scaled HJB of Phase C; the reduced-system
  fixed-point algebra of Phase D.
- **Consequences of S1/S2/S3:** `R=O(1)` (S3) gives the **magnitude** `O(1/b)`
  of the illiquid term given bounded `Q`; S2 `V_inf=0` is **not** inferred from
  any identity (it remains provisional input).
- **New assumptions introduced in this gate:** only the explicit non-circular
  sufficient conditions of Phase F (scaled-tail tightness of `Q`,
  non-degeneracy, regular lower sector, `E->0`, derivative-remainder `E_s->0`,
  and a coupled-limit/basin condition); each is flagged, never silently assumed.
- **Finite-grid evidence only:** the DLH-5R medians (Phase G) are read-only
  evidence context; they support qualitative compatibility only.

## 6. Scope

Analysis is restricted to compact interior `a in (a_bar, a_max - eps]` (with
`a_min > a_bar` when the simplified transfer form is used; the `a=10` upper law
and `a=0` bare-`a` corner are NOT invented or implemented). No endpoint law, no
`R/W/W1/W2/W_max` choice, no numerical execution.
