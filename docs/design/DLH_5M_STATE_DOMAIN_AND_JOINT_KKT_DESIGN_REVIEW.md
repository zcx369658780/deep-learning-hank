# DLH-5M / Issue #39 — State-Domain Geometry and Joint HJB/KKT Boundary-Law Design Review

**Task type:** `SCIENTIFIC_DESIGN_REVIEW__STATE_DOMAIN_GEOMETRY_AND_JOINT_KKT`
**Date:** 2026-09-02
**Branch:** `dsh/issue-39-dlh-5m-domain-kkt-design-review-2026-09-02`
**Fresh `origin/main` baseline:** `a82acf829d4e68789b420843e8d5b47c338a50f8`

This is a **model-design review, not an implementation task**. No source mutation, no
HJB/KFE/grid run, no new state is authorized. It compares two coherent candidate
state-domain geometries for the accepted two-asset household, derives their
state-constraint HJB/KKT laws generically, maps the accepted DLH-5K/DLH-5L evidence to
both candidates, and produces an explicit Owner decision packet. No recommendation
freezes or changes the model.

**Revision (2026-09-02, reviewer comment `5501914968`):** this candidate applies the
bounded corrections requested by the fresh review: (1) upper-face KKT multiplier sign
corrected to the maximization convention `L = H - lambda*g` (effective gradients
`V - lambda`, not `V + lambda`); (2) `lambda_W` cancellation from the linear transfer
term preserved, with its effect retained through the adjustment cost, and `d` is not
described as fully free because `chi(d,a)` keeps the W constraint dependent on `d`;
(3) W-face activity recorded only as the `W_max`-conditional (`W_s = a+b` per state);
(4) intersections, the W2 trapezoid and the taper effect qualified as conditional on
`W_max` / dependent only on `a`; (5) a finite rectangular state constraint
distinguished from an economic asset cap (numerical closure whose influence must be
shown to vanish with truncation). No accepted DLH-5K/5L numerical evidence is changed.

---

## 0. Controlling accepted evidence and identities

Controlling accepted source (immutable, read-only):

- `src/deep_learning_hank/two_asset/matlab_faithful_two_asset_ha.py`
  - blob `76ae5b149993a7edeeb337f1b02b3fe33c51e`
  - SHA-256 `1795718C469FC3B427CAB8E3D5957C133BEAD6EACC9EF0A25A3EDB7211D1A024`

Controlling accepted analytical evidence (read-only):

- `reports/dlh_5k_high_wealth_corner_closure_diagnostic_2026_09_01/`
- `reports/dlh_5l_total_wealth_domain_geometry_diagnostic_2026_09_01/`

Accepted (Issue #38 / DLH-5L, verdict `DLH_5L_ISSUE_38_IMPLEMENTATION_ACCEPTED__TOTAL_ASSET_DRIFT_INWARD_ON_PREFROZEN_HIGH_WEALTH_STATE_SET__RECTANGULAR_B_VIOLATION_REINTERPRETED_AS_COMPONENTWISE_REALLOCATION__CROSS_A_TOTAL_DRIFT_SENSITIVITY_REMAINS__DOMAIN_KKT_DESIGN_REVIEW_REQUIRED`):

1. On the pre-frozen 105-state high-wealth evidence set, every material positive-`mu_b`
   state has `mu_W = mu_a + mu_b <= 0`; no inspected state has positive `mu_W`.
2. All 17 top-layer upper-b offenders violate rectangular `mu_b <= 0` while satisfying
   `mu_a <= 0` and `mu_W <= 0`.
3. The linear transfer control cancels one-for-one in `mu_W`; adjustment cost remains.
4. This is finite-state/source-accounting evidence, not an infinite-domain
   mean-reversion theorem and not stationary-tail proof.
5. Cross-a `mu_W` differences are smaller in absolute magnitude than `mu_b`
   differences but remain above the pre-registered 1e-2 diagnostic threshold on
   16/24 aligned pairs.
6. No production-domain replacement, HJB/KFE mutation, taper/FOC/adjustment-cost
   change, or stationary re-entry is accepted.
7. Pure larger-b-grid continuation remains CLOSED.
8. Stationary KFE remains NOT AUTHORIZED under Issue #27.

Accepted accounting identities (implemented-source):

```text
mu_a = r_a_eff(a)*a + d
mu_b = r_b*b + labor_income - d - adjustment_cost(d,a) - (consumption - transfer_income)
mu_W = mu_a + mu_b
     = r_a_eff(a)*a + r_b*b + labor_income - adjustment_cost(d,a) - (consumption - transfer_income)
r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)     (accepted a_max-normalized taper, a_max = 10)
labor_income = (1 - tau)*wbar*z*labor
b >= b_min (b_min = -2.0),  a >= 0 (a_bar = 1e-6 numerical floor),  a <= a_max = 10
```

---

## 1. Boundary classification: economic constraint vs computational truncation

The review must not silently treat a computational truncation as an economic
constraint. The full classification is in
`reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_CONSTRAINT_CLASSIFICATION.md`.
Summary:

| Boundary | Classification | Justification |
|---|---|---|
| `a >= 0` (floor `a_bar=1e-6`) | **Structural / economic (non-negativity)** | Illiquid capital cannot be negative; the accepted floor is a numerical representation of `a >= 0`. |
| `b >= b_min = -2.0` | **Structural / economic borrowing floor** | A liquidity/borrowing limit is a genuine economic constraint (a stock floor, unlike the transfer flow `d`). |
| `a <= a_max = 10` | **Computational truncation + modeling normalization anchor (taper)** | No economic reason bars illiquid holdings above 10; the accepted taper normalizes `r_a` by `a_max`, so `a_max` is a modeling normalization anchor. The taper decays but does not extinguish returns at `a_max` (`r_a_eff(a_max) = 0.9*r_a`). |
| `b <= b_max` (route ceiling, b160 = 1075/19) | **Computational truncation (pure)** | No economic reason bars liquid wealth above `b_max`; the outward liquid drift at this face is a truncation response. This is the face at issue. |
| accepted `a_max`-normalized illiquid-return taper | **Numerical stabilization / modeling normalization** | Anchors return decay on `a`; it is not itself a state constraint and does not stabilize the `b`-or `W`-face. |

The distinction matters — with a precise caveat: a finite rectangular
state-constraint condition need **not** be interpreted as an economic law if it is
treated as a numerical boundary closure at a computational truncation whose influence
is shown to vanish as the truncation recedes. Under the current rectangle the
upper-`b` face is a truncation, so a rectangular tangent-cone law `mu_b <= 0` would
either be a numerical closure (legitimate only if its influence is shown to vanish
with truncation) or an economic constraint (only if the Owner accepts the rectangle as
the true state domain). The accepted evidence establishes neither. That is the central
tension the design review must resolve, not assume away.

---

## 2. Candidate Design R — rectangular componentwise state constraints

Full derivation in
`reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_GEOMETRY_CANDIDATES.md`
and
`reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_JOINT_KKT_BOUNDARY_LAWS.md`.

Geometric model: the computational domain is a rectangle in `(a,b)` with faces
`a=0`, `a=a_max`, `b=b_min`, `b=b_max`. The admissible tangent cone at an active
face forces the state drift inward:

```text
upper-a face (a=a_max):  mu_a <= 0
upper-b face (b=b_max):  mu_b <= 0
joint upper corner:      mu_a <= 0 AND mu_b <= 0
lower-b face:            mu_b >= 0
lower-a face:            mu_a >= 0
```

Generic constrained HJB/KKT statement (Design R): on each active face the household
solves the HJB supremum over controls admissible to the active tangent cone,
with the drift constraint imposed as a state-constraint (Carathéodory /
Crandall–Liggett viscosity) condition, not by post-hoc clipping or branch forcing.

Which controls enter each drift:

- `mu_a = r_a_eff(a)*a + d` — control `d` enters linearly `(+1)`.
- `mu_b = r_b*b + labor_income - d - adjustment_cost(d,a) - (consumption - transfer_income)`
  — `d` enters through `-d - adjustment_cost(d,a)` (the transfer FOC trades `V_b`
  against the marginal adjustment cost), consumption `c` enters through
  `-(c - transfer_income)`, labor `l` through `labor_income`.
- `mu_W = mu_a + mu_b` — `d` cancels one-for-one; `c`, `l` and adjustment cost remain.

Joint control feasibility / KKT at the upper-b face: at `b = b_max`, `mu_b <= 0`
is the active constraint. The unconstrained interior FOCs
(`u'(c) = V_b`; transfer FOC `V_a - V_b = marginal adjustment cost`) are modified at
the face by a KKT multiplier `lambda_b >= 0` on the drift constraint `mu_b <= 0`.
Because this is a maximization problem with an upper constraint `g = mu_b <= 0`, the
consistent KKT Lagrangian subtracts the multiplier times the constraint,
`L = H - lambda_b*mu_b`, so the boundary Hamiltonian is

```text
H = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + V_b*mu_b - lambda_b*mu_b }   (b=b_max active)
  = sup_{c,l,d} { u(c) - v_l*l + V_a*mu_a + (V_b - lambda_b)*mu_b }
```

with complementarity `lambda_b * mu_b = 0`. Equivalently, on the face the effective
value-gradient along `b` is `V_b - lambda_b <= V_b` (the shadow price of `b` is reduced
at the cap, since further `b` accumulation is inadmissible); the constraint binds
exactly when the unconstrained drift would exit the domain.

Is the current MATLAB-faithful upper-b/upper-a ordering equivalent to this constrained
problem? **No.** The accepted DLH-5K evidence (`joint_corner_feasibility`, Phase D)
shows the selected transfer candidate fails joint rectangular inwardness at all 17
offenders (infeasible corner `x` vs `x_b_simplified`), and the current solver closes
the upper-b boundary with a one-sided finite-difference value reconstruction
(`vb_boundary_closure` vs `vb_backward`) rather than a KKT multiplier on `mu_b <= 0`.
The current boundary treatment therefore does not implement the rectangular
tangent-cone/KKT constrained problem; it imposes the HJB at the boundary under the
truncation's implied absorbing/reflecting convention. Retaining Design R would require
a genuine state-constraint HJB/KKT reformulation of the boundary value problem (an
implementation task under separate authority, not authorized here).

What must change conceptually if rectangular geometry is retained: a
well-posed constrained Hamiltonian with tangent-cone admissibility at every active
face, a principled KKT multiplier structure (including at the joint corner where two
constraints are simultaneously active), and boundary conditions consistent with that
formulation in both HJB and KFE.

---

## 3. Candidate Design W — hybrid joint-wealth truncation

Full derivation in `DLH_5M_GEOMETRY_CANDIDATES.md` and `DLH_5M_JOINT_KKT_BOUNDARY_LAWS.md`.

Candidate domain:

```text
D_W = { a >= 0,  b >= b_min,  a <= a_max,  a + b <= W_max }
```

with required normal/tangent conditions:

```text
W face (a + b = W_max):  mu_W = mu_a + mu_b <= 0
upper-a face (a = a_max): mu_a <= 0
intersection a=a_max and W=W_max:  mu_a <= 0 AND mu_W <= 0
lower-b face:  mu_b >= 0
lower-a face:  mu_a >= 0
```

Source facts supporting `W = a + b` as an accounting coordinate: the accepted
accounting gives `mu_W = mu_a + mu_b` with the *linear* part of the transfer `d`
cancelling one-for-one, so the total-wealth drift does not depend on the linear
reallocation component; it still depends on `d` through the adjustment cost
`chi(d,a)` (and on consumption net of transfer income and on labor income). This is a
genuine accounting-additivity fact about the drift decomposition — and it is exactly
why at a W face `lambda_W` cancels from the linear transfer FOC but survives in the
adjustment-cost term.

Mandatory distinction: accounting additivity is **not** the economic claim that `W`
must be the production truncation variable. The accepted evidence shows `mu_W < 0` on
the pre-frozen finite high-wealth set — consistent with `W` being a good truncation
coordinate — but this is not an infinite-domain theorem and does not by itself
establish that `W` (rather than `b`) is the right variable against which to truncate.
That economic claim requires additional theory (Section 7) and ultimately an Owner
decision.

Compatibility with the accepted `a_max`-normalized taper: in `D_W` the illiquid
support `a <= a_max` is retained as a separate face, so the taper is unchanged on the
`a` coordinate. The taper `r_a_eff(a) = r_a*(1 - 0.1*(a/a_max)^9)` depends **only on
`a`** and does not strengthen as `b` or `W` increases; it therefore does not stabilize
the slanted `W` face, and `mu_W <= 0` on that face must be enforced by the constraint
itself. No conflict with the taper, but no stabilization help from it.

Geometry of the slanted W boundary: in `(a,b)`, `a + b = W_max` is the line of slope
`-1`. Which active-constraint intersections exist depends on the (here symbolic) value
of `W_max`; without choosing `W_max` they are stated as conditions, not asserted to all
exist: `W` ∩ `{b=b_min}` at `a = W_max - b_min` (on the `b=b_min` face for the
`W_max`-range that keeps it inside `D_W`); `W` ∩ `{a=a_max}` at `b = W_max - a_max`
(the upper-right corner, where `mu_a <= 0` and `mu_W <= 0` are both active, only for
`W_max >= a_max + b_min`); `W` ∩ `{a=0}` at `b = W_max`. Wherever an intersection
exists, two constraints are active and both KKT multipliers enter the boundary
Hamiltonian.

Generic constrained HJB/KKT at the W face: at `a + b = W_max`, the household
maximizes subject to `mu_W <= 0`. Because the *linear* part of `d` cancels from
`mu_W`, the W-face constraint does not tax the linear transfer directly; `d` still
enters `mu_W` through the adjustment cost `chi(d,a)`, so the reallocation is **not
fully free** — the transfer FOC governs `d` with the adjustment-cost term scaled by
`(V_b - lambda_W)` (see `DLH_5M_JOINT_KKT_BOUNDARY_LAWS.md` §3.1). This is the key
economic difference from Design R: at the corner the rectangular tangent cone
`mu_b <= 0` forbids net `b` accumulation even when financed by `a` drawdown, whereas
the `W`-face law does not tax the linear transfer and limits only total-wealth growth
via `mu_W <= 0` (up to adjustment cost).

KFE generator/tangent-flow requirements if `W` were selected later (design only, not
implemented): the generator on `D_W` must be conservative, with the flux through the
slanted `W` face matched to the controlled dynamics (`normal flux = mu_W` on the face),
and the HJB and KFE must share exactly the same controlled domain and boundary law
(controlled-process matching). These requirements are stated here as design
constraints; no generator is built in DLH-5M.

---

## 4. Candidate representation options for Design W

Full comparison in `DLH_5M_GEOMETRY_CANDIDATES.md`.

### W1 — masked `(a,b)` tensor grid

Retain the tensor lattice but treat states beyond `a + b <= W_max` as outside the
controlled domain. Assessment:

- stencil loss near the slanted boundary: the 45° cut removes neighbors for points on
  the `W` face, producing asymmetric one-sided stencils;
- generator conservation: conservative discretization of the slanted face requires
  explicit flux bookkeeping (the face is not coordinate-aligned), otherwise
  mass leaks;
- boundary-neighbor topology: the neighbor set changes discontinuously across the cut;
- exact HJB/KFE process matching: harder, because the discrete process must respect
  the same slanted face in both operators.

### W2 — transformed `(a,W)` representation

Set `b = W - a` analytically. Transformed drifts: `mu_a` unchanged; the `W`
coordinate has drift `mu_W = mu_a + mu_b` (the total drift; `d` absent). Transformed
domain:

```text
a in [0, a_max],  W in [W_lower(a), W_max],  W_lower(a) = a + b_min
faces: a=0, a=a_max, W=W_max (flat, coordinate-aligned), and W = a + b_min (slanted)
```

Assessment:

- the `W` cap becomes a flat coordinate-aligned face (the key high-wealth boundary
  becomes simple);
- the borrowing floor `b >= b_min` becomes the slanted face `W = a + b_min` — the
  geometric difficulty moves from the top cap to the lower floor, it does not
  disappear;
- the domain is a trapezoid with two vertical sides, a flat top, and a slanted bottom;
- the accepted taper and transfer FOC are `a`-based and survive unchanged, but the
  transfer FOC couples the `a`- and `W`-coordinates (since `d` appears in `mu_a` and
  not in `mu_W`, the a-evolution is directly affected by reallocation while the
  W-evolution is not);
- net: not unambiguously simpler; it trades a slanted high-wealth cap for a slanted
  borrowing floor.

Neither representation is selected in DLH-5M; both require additional design work
before implementation authority can exist.

---

## 5. Geometry-consistency rejection test

Shortcut under test: keep the rectangular domain but, only at the joint upper corner,
replace `mu_b <= 0` by `mu_W <= 0`.

Analysis. The rectangular tangent cone at the corner is the intersection of the two
half-spaces

```text
C_rect = { (v_a, v_b) : v_a <= 0 AND v_b <= 0 }.
```

The shortcut condition (keeping `mu_a <= 0` and replacing `mu_b <= 0` by
`mu_W <= 0`) is

```text
C_shortcut = { (v_a, v_b) : v_a <= 0 AND v_a + v_b <= 0 }.
```

`C_rect` is a proper subset of `C_shortcut`: e.g. `(v_a, v_b) = (-1, +0.5)` satisfies
`v_a <= 0` and `v_a + v_b = -0.5 <= 0` but violates `v_b <= 0`. Hence the shortcut
admits corner states with **positive** `b`-drift while the true rectangular tangent
cone requires componentwise inwardness. The accepted offenders have `mu_a < 0`,
`mu_b > 0`, `mu_W < 0` — they lie in `C_shortcut` but not in `C_rect`.

Conclusion: **the shortcut is geometry-inconsistent.** It is a PASS-seeking
relabeling that makes the accepted offenders pass by enlarging the admissible cone at
the corner. It must be rejected and must not be recommended merely because it would
make the accepted offender states pass. (Equivalently, any condition of the form
`mu_W <= 0` alone is strictly weaker at the corner than the rectangular tangent cone,
so it cannot represent "rectangle with a correct corner law".)

---

## 6. Accepted-evidence mapping

Full mapping persisted in
`reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_ACCEPTED_EVIDENCE_MAPPING.csv`
(65 rows: 17 top-layer offenders + 24 aligned cross-a pairs, both a77 and a153
legs). Evidence mapping only — no new HJB run, no new state.

Key facts reproduced from accepted evidence:

- **All 17 top-layer upper-b offenders:** `mu_a < 0` (rectangular upper-a satisfied),
  `mu_b > 0` (rectangular upper-b violated), `mu_W < 0` (joint-W satisfied). Under R
  the active constraint is the upper-b face (upper-b+upper-a at the joint corner,
  e.g. J3_A153_B120 b=119 a=152).
- **All 48 aligned cross-a states:** `mu_W < 0` (joint-W satisfied on both a77 and
  a153 legs). Under R the active face is upper-b (upper-b+upper-a at the corner
  a=10).
- **Under W, activity is unresolved** because `W_max` is not chosen. For each state
  only `W_s = a + b` is recorded, with the conditional: `W_max > W_s` ⇒ W face
  inactive; `W_max = W_s` ⇒ W face active; `W_max < W_s` ⇒ state outside `D_W`.
  `mu_W < 0` is reported as W-face inwardness *if active*, not as a determination of
  activity. (For `a = a_max` states the upper-a face is active regardless of `W_max`;
  the W face joins it only when `W_max = W_s`.)
- The 16/24 aligned pairs where `rel_diff_mu_W > 1e-2` (cross-a total-drift
  sensitivity remains) are preserved in the mapping; this is a robustness gap that
  must be closed before W (or R) can be frozen.

This mapping shows the accepted evidence is **consistent with W-inwardness on the
inspected finite set** but does **not** distinguish, by itself, whether R or W is the
correct geometry: the offenders violate R's componentwise law and satisfy W's
total-drift law on the pre-frozen set, which is exactly the evidence-level tension the
Owner decision must resolve.

---

## 7. Decision criteria and impact matrix

The 12 criteria of Issue #39 §9 are scored for Design R and Design W in
`reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_IMPLEMENTATION_IMPACT_MATRIX.csv`
(each with a one-line evidence-based rationale). Highlights:

1. **Economic interpretation:** W is economically more coherent (the upper-b cap is a
   truncation, not an established economic constraint); R's componentwise law at the
   truncation face is unestablished (its influence as a numerical closure is not shown
   to vanish with truncation, and its economic status is unresolved).
2. **Consistency with accepted accounting:** both are consistent; W exploits the
   `d`-cancellation more directly.
3. **Consistency with transfer/rebalancing economics:** W does not tax the linear
   rebalancing at the cap (`lambda_W` cancels from the linear transfer FOC; the
   adjustment cost keeps `mu_W` dependent on `d`); R's corner `mu_b <= 0` makes net
   b-accumulation inadmissible even when a-financed — in tension with the
   reallocation interpretation accepted in DLH-5L.
4. **Consistency with the accepted `a_max` taper:** both retain `a_max`; W's cap is
   not taper-stabilized.
5. **HJB state-constraint/KKT correctness:** both require a genuine KKT formulation;
   neither is implemented today (R's current ordering is not KKT-equivalent).
6. **Exact HJB/KFE controlled-process matching:** R matches on the rectangle but the
   rectangle is not the true unbounded process; W requires slanted-face process
   matching.
7. **Generator conservativity:** R has axis-aligned faces (feasible); W's slanted face
   is hard (W1) or moved (W2).
8. **Numerical implementation complexity:** R low (existing grid + KKT);
   W higher (new geometry, W_max, slanted boundary).
9. **Resolution-robustness risk:** R leaves offenders that persist across a77/a153
   (cross-a sensitivity remains); W is untested at other resolutions.
10. **Risk of an artificial wealth cap with economic consequences:** W introduces
    `W_max` (an artificial cap with potential stationary consequences); R introduces no
    new cap but leaves the truncation artifact unresolved.
11. **Compatibility with future multi-region / learned blocks:** R's rectangle is the
    standard lattice; W propagates a non-standard domain through all downstream
    modules.
12. **Recovery of an interpretable infinite-domain/truncation limit:** W has a clean
    `W_max -> infinity` limit if inwardness persists; R's rectangle limit is
    problematic because the constraint binds at finite `b_max` with outward drift.

Overall: the two designs trade off economic coherence (W) against numerical
standardness (R), and **neither can be frozen on the accepted evidence alone** —
which drives the recommendation below.

---

## 8. Required scientific recommendation

Exact recommendation:

`DLH_5M_DOMAIN_GEOMETRY_DESIGN_EVIDENCE_INSUFFICIENT__OWNER_SCIENTIFIC_DECISION_REQUIRED`

Rationale (also persisted in `DLH_5M_SCIENTIFIC_RECOMMENDATION.md`):

- **Design R is not recommended:** the upper-b cap is a computational truncation. A
  finite rectangular state constraint need not be interpreted as an economic law if
  treated as a numerical closure whose influence vanishes with truncation — but the
  accepted evidence provides no such truncation-vanishing argument, and it shows the
  offenders violate R's componentwise law while satisfying total-wealth inwardness.
  The current solver is also not equivalent to the rectangular KKT problem, and R
  leaves the accepted offenders as genuine KKT violations at a face whose economic
  status is unresolved. Freezing R is not justified by the accepted evidence.
- **Design W is the more economically coherent hypothesis but cannot be frozen yet:**
  (i) `mu_W <= 0` is established only on a pre-frozen finite state set, not as an
  infinite-domain theorem; (ii) no principled `W_max` selection exists (and none may
  be invented here); (iii) cross-a relative total-drift sensitivity remains above the
  pre-registered threshold on 16/24 aligned pairs; (iv) the W1/W2 representation
  tradeoffs are unresolved; (v) conservative generator / controlled-process matching on
  the slanted boundary is undeveloped. Freezing W would outrun the evidence.
- **Blocked (`BLOCKED_DLH_5M_SOURCE_OR_ACCEPTED_EVIDENCE_INCONSISTENCY`) does not
  apply:** the accepted source and evidence are internally consistent (J0–J5 reproduce
  exactly; `mu_W` identities hold to machine precision; transfer cancels one-for-one).

Therefore **U** is the scientifically honest terminal: additional theoretical work is
required before either candidate can be scientifically frozen, and the domain/boundary
choice is an Owner scientific decision.

---

## 9. Explicit Owner decision packet

Full packet in `reports/dlh_5m_state_domain_joint_kkt_design_review_2026_09_02/DLH_5M_OWNER_DECISION_PACKET.md`.
Summary:

- **Recommended design:** none frozen; **U (evidence insufficient)**.
- **Strongest evidence in favor of the W direction:** every inspected state
  (105/105) has `mu_W <= 0`; transfer cancels one-for-one in `mu_W`; W-inwardness is
  consistent with rebalancing economics.
- **Strongest argument against freezing anything:** finite-state evidence only; no
  infinite-domain theorem; `W_max` undefined; cross-a `mu_W` sensitivity remains;
  R's componentwise law is unestablished at the truncation face (no
  vanishing-influence argument, and offenders satisfy total-wealth inwardness
  instead).
- **Equations/state constraints that would become controlling if Owner accepts W**
  (illustrative, not selected): `D_W = {a>=0, b>=b_min, a<=a_max, a+b<=W_max}` with
  `mu_W <= 0` on the W face, `mu_a <= 0` on `a=a_max`, and joint conditions at
  intersections.
- **What remains unchanged:** the current rectangular computational domain, the
  MATLAB-faithful HJB source, frozen D0 economics, the accepted taper.
- **What implementation task would follow** (only after Owner decision): a separate
  scientific implementation Issue for the chosen design (R or W), including the full
  state-constraint HJB/KKT formulation and its KFE counterpart, under fresh review.
- **What falsification / numerical validation would be required after
  implementation:** inward drift on every active face, resolution robustness across
  mature a-lattices, conservative generator, exact HJB/KFE controlled-process
  matching, and then Issue #27 stationary re-entry (recurrent-class/nullspace, pin,
  ORIGINAL `Q^T g`, mass/non-negativity, stationary tail) with no grandfathered
  aggregates.
- **Why stationary KFE still cannot begin immediately:** no accepted domain/boundary
  controlled process exists yet; the HJB↔KFE contract of Issue #27 requires an
  accepted, implemented, validated process first.

---

## 10. Required additional theory before any domain choice (the U-path)

The Owner decision packet identifies the concrete theory gaps that must be closed
(analytically, not by grid extension) before R or W can be frozen:

1. **Infinite-domain / asymptotic total-wealth analysis:** establish conditions under
   which `mu_W <= 0` persists as `W -> infinity` along the accepted a-lattice (using
   the transfer FOC, the taper structure, and the boundary consumption/wealth
   relationship), or exhibit a counterexample family. This is a theorem task, not a
   grid task.
2. **Principled `W_max` selection as a computational truncation:** a dimensionless /
   economic criterion (e.g. the smallest `W` beyond which the stationary mass is
   provably negligible, or where `mu_W` is inward with a required margin), noting
   stationary is blocked, so this must be an a-priori argument; alternatively a
   `W_max -> infinity` convergence argument.
3. **Formal joint HJB/KKT statements:** the full constrained Hamiltonian for W (W face
   + intersections) and for R (rectangular faces + corner), including the transfer FOC
   coupling and taper compatibility, and whether the MATLAB-faithful ordering can be
   made equivalent to either.
4. **Generator / process-matching analysis:** conservative generator on the chosen
   domain (flux through slanted faces) and the HJB↔KFE duality on that domain.
5. **(Owner-scoped economic modeling decision):** whether `W` is a legitimate
   *production* truncation variable or only a computational device.

None of this work is authorized in DLH-5M; it is the recommended next-gate content
after the Owner decision.

---

## 11. Scientific ceiling / forbidden operations (DLH-5M)

Per Issue #39 §12, DLH-5M performed none of the following: no modification of any
existing tracked file; no HJB/KFE/regional source mutation; no taper/FOC/adjustment-
cost/economics/price change; no production-domain selection or implementation; no
numerical `W_max`; no new or rerun grid, extent or resolution (no J0–J5 rerun); no
boundary-KKT implementation; no upper-b branch patch; no clipping; no stationary
KFE/nullspace/pin/density/tail/aggregates; no D1-D3, regional GE or multi-province
audit; no network training; no nominal HANK/calibration/policy/welfare/Results; no
self-accept/merge/close/PR/successor. See
`DLH_5M_FORBIDDEN_OPERATION_CHECK.md`.

This document and the accompanying report are the complete DLH-5M deliverable.
**The Builder stops here for fresh ChatGPT review and an Owner scientific decision.**
