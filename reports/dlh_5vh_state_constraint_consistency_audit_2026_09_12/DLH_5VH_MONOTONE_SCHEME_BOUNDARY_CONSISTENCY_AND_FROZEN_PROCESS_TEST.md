# DLH-5V-H — Monotone-Scheme Boundary Consistency and Frozen-Process Test (Micro-Rev Rev 1)

**Sequence steps D, E, F of Issue #56; Micro-Rev tasks C, D, E, F, and the toy tightening.** Defines the weakest defensible numerical target (D) with the corrected monotonicity and a convention-explicit half-relaxed-limit derivation; tests the frozen finite-process architecture against it (E) with the control/payoff-level bridge under the frozen finite-m taxonomy; supplies the mandatory analytic toy discriminator with a full component proof (F).

---

## Part D — The weakest defensible numerical target

### D.1 Scheme operator and corrected monotonicity (Task D)

Let u_m be the discrete value function. The scheme is the discounted Bellman fixed point, written in two equivalent forms:

```text
Residual form:    S_m(s, u) = ρ u(s) − max_α { g(s,α) + Σ_{j≠s} q_α(s,j) (u(j) − u(s)) } = 0.
Scaled form:      u(s) = T_m(u)(s),   T_m(u)(s) = max_α { [ g(s,α) + Σ_{j≠s} q_α(s,j) u(j) ] / [ ρ + Σ_{j≠s} q_α(s,j) ] }.
```

with q_α(s,j) ≥ 0 (nonnegative Markov off-diagonals) and ρ > 0.

**Correct monotonicity statement (replaces the earlier row-sum claim).** For each fixed candidate α the residual is

```text
S_m^α(s,u) = ρ u(s) − g(s,α) − Σ_j q_α(s,j)(u(j) − u(s))
           = (ρ + Σ_j q_α(s,j)) u(s) − Σ_j q_α(s,j) u(j) − g(s,α),
```

which has **positive diagonal coefficient** ρ + Σ_j q_α(s,j) ≥ ρ > 0 and **nonpositive off-diagonal coefficients** −q_α(s,j) ≤ 0 — the proper (M-matrix) structure. **The condition `ρ ≥ Σ q` is NOT imposed**: it is unnecessary for this structure and incompatible with the accepted refinement scaling Σ q = O(m) at fixed ρ.

The monotonicity used by the convergence framework is **order-preservation of the scaled operator**:

- weights w_α(s,j) := q_α(s,j)/(ρ + Σ_j q_α(s,j)) ≥ 0, sum Σ_j w_α(s,j) < 1;
- if u ≥ v pointwise then T_m(u)(s) ≥ T_m(v)(s) for every s (all weights nonnegative; the max preserves order) — T_m is **nondecreasing**;
- ‖T_m(u) − T_m(v)‖∞ ≤ max_α [Σ q / (ρ + Σ q)] ‖u − v‖∞ with modulus < 1 — strict contraction, hence the fixed point u_m exists and is unique.

(Convention note: the scheme is written as the fixed point u = T_m(u); the order-preservation of T_m is the property invoked by the half-relaxed-limit arguments below and by the Barles–Souganidis-type framework for this operator form. The residual sign convention is fixed by the project convention F = ρu − H, subsolution = F ≤ 0 — continuous-target report §2.3.)

**Stability.** Max-principle bound: if u_m attains its maximum at s, then at s the residual gives ρ u_m(s) = g + Σ q (u_m(j) − u_m(s)) ≤ g + 0 (neighbors ≤ max), so u_m(s) ≤ ‖g‖∞/ρ; symmetrically u_m ≥ −‖g‖∞/ρ. Hence ‖u_m‖∞ ≤ ‖g‖∞/ρ uniformly in m.

### D.2 Interior and boundary consistency; half-relaxed-limit derivation (fixed convention)

**Interior consistency.** For every x̂ ∈ D_W° and every φ ∈ C², for every sequence of interior states s_m → x̂:

```text
S_m(s_m, φ) → F(x̂, φ(x̂), Dφ(x̂)) = ρφ(x̂) − H(x̂, Dφ(x̂)),   H = sup_α { g + Dφ·μ },
with remainder |S_m(s_m,φ) − [ρφ(s_m) − H(s_m, Dφ(s_m))]| ≤ ½ ‖D²φ‖ · max_α Σ_j q_α |w_αj|² = O(1/m)
(frozen scaling: rates O(m), steps O(1/m), second moments O(1/m)).
```

**Half-relaxed-limit derivation (subsolution direction).** Let ū = limsup* u_m. Take x̂ ∈ D̄ and φ touching ū from above; set φ_ε = φ + ε|x−x̂|² so that ū − φ_ε has a strict local max at x̂. Let s_m be maximizers of u_m − φ_ε near x̂, so s_m → x̂ and c_m := (u_m − φ_ε)(s_m) → 0 with u_m ≤ φ_ε + c_m near s_m. From the fixed-point equation at s_m:

```text
u_m(s_m) = max_α { [g + Σ_j q_α u_m(j)] / [ρ + Σ_j q_α] } ≤ max_α { [g + Σ_j q_α (φ_ε(j) + c_m)] / [ρ + Σ_j q_α] }
```

so for EVERY candidate α: (ρ + Σ_j q_α) φ_ε(s_m) ≤ g(s_m,α) + Σ_j q_α φ_ε(j) + o(1). Taylor-expanding φ_ε at s_m (Σ_j q_α (x_j − x_s) = μ_α(s_m) exact first moment; Σ_j q_α |x_j − x_s|² → 0):

```text
ρφ_ε(s_m) ≤ g(s_m,α) + Dφ_ε(s_m)·μ_α(s_m) + o(1)   for every α,
⟹  ρφ(x̂) ≤ g(x̂,α) + Dφ(x̂)·μ(x̂,α)   for every limiting candidate,
⟹  ρφ(x̂) ≤ H_lim(x̂, Dφ(x̂)),   H_lim = limit of the discrete Hamiltonians at the visited states.
```

So **ū is a viscosity subsolution w.r.t. H_lim** (project convention: ρū ≤ H_lim at touching-from-above test functions). The supersolution direction for u̲ = liminf* u_m is symmetric (near-minimizer sequences, same Taylor estimate), giving ρφ(x) ≥ H_proj(x, Dφ) at interior test points x ∈ D°.

**Boundary one-sided consistency.** At x̂ ∈ ∂D, the maximizer sequence visits either interior states (H_lim = H_proj — the subsolution inequality ρV ≤ H_proj holds by the Soner-form authority, continuous-target report §2.2) or W-contact states (H_lim = H_R — the inequality ρV ≤ H_R requires the constrained characterization ρV ≤ H_T plus the control-level bridge liminf H_R ≥ H_T; the bridge is proved in §E.4, the characterization is the Outcome-B gap). The target therefore requires:

1. interior consistency at interior states (both directions);
2. the control-level bridge at boundary-contact states: `liminf H_R ≥ H_T` with the SAME candidate payoffs (proved in §E.4);
3. a comparison principle for the limit problem (hypothesis; the project-specific verification is part of the Outcome-B gap).

**What is NOT part of the legitimate target:** Kuratowski outer/limsup + recovery/liminf of admissible-drift sets at arbitrary convergent state sequences (the Issue-#55 raw target); equality of interior-state admissible cones with the boundary tangent cone; any invented min/max boundary operator not derived from the Soner one-sided form and the candidate structure (none is introduced).

---

## Part E — Frozen-process test against the legitimate target

### E.1 Mandatory question 1: `s_m = (0, i_t^m(0) − 2), μ = (0, 1)`

**Only the raw graph test is violated; the operator-consistency components are not.** The state is interior (non-W-active). Its frozen cone is exactly {μ_a ≥ 0} (three-neighbor {w_right, w_up, w_down}). The drift μ = (0, 1): μ_a = 0 ≥ 0 — admitted; represented by w_up = (0, 7/(19m)) with q_up = 19m/7, first moment (0, 1). **μ_W = μ_a + μ_b = 1** (physical units; the jump size 7/(19m) is a distinct object — corrected per Task F). Interior consistency at s_m holds with the a=0-face operator (O(1/m) remainder); the boundary subsolution at the corner via interior maximizer sequences holds by the Soner authority; via W-contact sequences it is gated by the Outcome-B gap. The raw graph condition fails because μ_W = 1 > 0 at the corner limit — that is exactly the over-strong content (necessity audit §4).

### E.2 Mandatory question 2: upper-corner analogue

`s_m = (19m, i_t^m(19m) − 2), μ = (−1, 2)` → (a_max, W_max − a_max): interior state, own cone {μ_a ≤ 0} (a_max face law); operator-consistent; raw graph test violated; boundary transfer gated by the same gap.

### E.3 Mandatory question 3: interior states approaching a boundary

**YES** — interior grid states approaching a constrained boundary may remain interior-consistent without their admissible set equaling the boundary tangent cone. The mechanism: (i) the subsolution inequality is one-sided and holds with the unrestricted H (Soner authority) at interior-state limits; (ii) the supersolution is required only in the interior; (iii) the boundary constraint is carried by the W-contact states' own operators and by the control-level bridge. The toy (§Part F) demonstrates the mechanism in minimal form.

### E.4 Mandatory question 4: control/payoff-level bridge at the W-contact states (Task C)

**Geometric cone inclusion is not enough.** The object needed is the discrete Bellman Hamiltonian: max over candidates of {running payoff + drift score}. The bridge is proved at the control/payoff level:

**Lower-a × W corner (0, W_max).** For every viable control α at x̂ (drift μ(x̂,α) ∈ REV = {μ_a ≥ 0, μ_W ≤ 0} — the accepted lower-corner law), the frozen process at every lower-a W-contact cell s_m (j ∈ {0,…,6}, top/sub-top with the W-active/class conditions) represents the SAME household candidate α with:

```text
rates:      q_RT = 19m·μ_a/70 ≥ 0 (mirror (j+7, i−10)),   q_down = 19m·(−μ_W)/7 ≥ 0 (down (j, i−1));
payoff:     g_m(s_m, α) = g(x̂, α)          (same candidate (c, l, d), same running payoff);
first moment: q_RT·w_RT + q_down·w_down = (μ_a, −μ_a) + (0, μ_W) = (μ_a, μ_b) = μ(x̂, α)   EXACT;
second moment: q_RT|w_RT|² + q_down|w_down|² = [2660μ_a + 133(−μ_W)]/(361m) = O(1/m)   (accepted 5V-G Case L scaling).
```

Hence for every test function φ ∈ C² and every viable α at the corner:

```text
g(s_m,α) + Σ_r q(s_m,r;α)(φ(r) − φ(s_m)) = g(x̂,α) + Dφ(x̂)·μ(x̂,α) + O(1/m)  →  g + Dφ·μ,
so the discrete candidate Hamiltonian converges to the continuous candidate Hamiltonian, and
liminf_m H_R(s_m, Dφ) ≥ sup_{α : μ(x̂,α) ∈ REV} { g(x̂,α) + Dφ·μ(x̂,α) } = H_T(x̂, Dφ).
```

Availability facts (exact enumeration, frozen taxonomy): mirror requires j ≤ 19m−7 and i ≥ 10; down requires i ≥ 1 — both hold at every lower-a W-contact cell (j ∈ {0,…,6}: i_t(j) ≥ ⌊(19m(W_max+2) − 60)/7⌋ ≥ 17 for W_max ≥ 8, sub-top i ≥ 16). **0 violations** (m ≤ 25, W_max ∈ {8,10,12}).

**Upper-a × W corner (a_max, W_max − a_max).** For every viable α with μ(x̂,α) ∈ TDEP = {μ_a ≤ 0, μ_W ≤ 0}, the frozen process at every upper-a W-contact cell s_m (j ∈ {19m−6,…,19m}, top/sub-top with the W-active/class conditions) represents the SAME candidate α with the two-case Case-U contract:

```text
if μ_b ≥ 0 (W-tangent part):  q_T = 19m·μ_b/70 ≥ 0 (forward (j−7, i+10)),  q_left = 19m·(−μ_W)/10 ≥ 0 (left (j−1, i)),  q_down = 0;
if μ_b < 0 (deplete part):    q_left = 19m·(−μ_a)/10 ≥ 0 (left),           q_down = 19m·(−μ_b)/7 ≥ 0 (down),          q_T = 0.
First moment (check, μ_b ≥ 0 case): q_T·w_T + q_left·w_left = (−μ_b, μ_b) + (μ_W, 0) = (μ_a, μ_b)   EXACT; symmetric for μ_b < 0.
payoff:   g_m(s_m, α) = g(x̂, α);   second moment: O(1/m) (accepted 5V-G Case U scaling);
liminf_m H_R(s_m, Dφ) ≥ H_T(x̂, Dφ).
```

Availability: forward at j ≥ 7 ✓ (upper-a cells j ≥ 19m−6 ≥ 7), left at j ≥ 1 ✓, down at i ≥ 1 ✓ (W-contact cells have i ≥ 10).

**b_min triple corner (a_max, b_min).** W_max = 8: true cone = TREA = {μ_a ≤ 0, μ_b ≥ 0, μ_W ≤ 0} = cone{w_left, w_T} — represented at the W-active lower-b cells (the (19m−7, 9) sub-top family has i_t = 10, r_j = 0 for W_max = 8) with the accepted Case B contract; W_max > 8: the W-active lower-b cells vanish for m > 69/(19(W_max − 8)) (accepted fact F5) and the remaining cells carry their own-position face-law cones ({μ_a ≤ 0} at j = 19m, {μ_b ≥ 0} at i = 0, full plane interior, exact triple at (19m, 0)), each containing the true corner cone {μ_a ≤ 0, μ_b ≥ 0} — subsolution-safe at the cone level (the operator-level transfer remains gated by the Outcome-B gap as everywhere at the boundary).

**Regular W-band (7 ≤ j ≤ 19m−7).** The accepted sector contracts (T_realloc ∪ R_reverse ∪ R_deplete) represent the full W-face tangent cone {μ_W ≤ 0} exactly with the same-payoff candidates (accepted 5V-A..E algebra; geometric prerequisites {w_T, w_RT, w_left, w_down} verified present — 0 violations).

**Face laws.** a=0, a=a_max, b=b_min interior-face states carry the exact face-law cones {μ_a ≥ 0}, {μ_a ≤ 0}, {μ_b ≥ 0} (exact three/four-neighbor representations, accepted 5V-G Case A/B algebra).

**Result:** the control-level bridge `liminf H_R ≥ H_T` holds at both W-corners and the face laws are exact; the one-sided boundary transfer `ρV ≤ H_R` additionally requires the constrained characterization `ρV ≤ H_T` — the single bounded Outcome-B gap, declared explicitly (not carried forward).

### E.5 Mandatory question 5: the Issue-54 obstruction under the operator target

**The finite-m lattice obstruction does not damage the control-level bridge at the W-corners.** The missing orientations are exactly the directions the corner laws exclude:

- w_T = (−70/(19m), +70/(19m)) has μ_a = −70/19 < 0 ⟹ **w_T ∉ REV** (lower corner requires μ_a ≥ 0);
- w_RT = (+70/(19m), −70/(19m)) has μ_a = +70/19 > 0 ⟹ **w_RT ∉ TDEP** (upper corner requires μ_a ≤ 0).

The corner cones' generators (w_RT, w_down at the lower corner; w_left, w_down, w_T at the upper corner) are represented at the exact-frontier cells (mirror ΔW = 0 available at i ≥ 10; forward ΔW = 0 available at j ≥ 7), so the §E.4 bridge holds at the exact-frontier cells too. The Issue-54 obstruction concerns exact pointwise first-moment representability of *every* tangent direction at *every* endpoint cell — a finite-m lattice identity, different from the operator-level object here.

---

## Part F — Mandatory toy discriminator (analytic; no simulation)

### F.1 Toy definition

1D state-constrained problem: state x ∈ [0, 1]; control d ∈ [−1, 1]; drift μ(x,d) = d; state constraint x(t) ∈ [0, 1]. Tangent cones: T(0) = [0, 1], T(1) = [−1, 0], T(x) = [−1, 1] for x ∈ (0, 1). Running payoff g(d) bounded, concave; discount ρ > 0. Continuous authority (Soner form): ρV = max_{d ∈ T(x)}{g + V'd}; V subsolution on [0,1], supersolution in (0,1).

Scheme: grid x_i = i/m (i = 0..m); upwind differences (forward for d > 0, backward for d < 0); discrete admissible sets A_m(x_i) = T(x_i) (boundary nodes restricted, interior nodes full):

```text
u_m(x_i) = max_{d ∈ A_m(x_i)} { [ g(d) + m·d⁺ u_m(x_{i+1}) + m·d⁻ u_m(x_{i−1}) ] / [ ρ + m·|d| ] }   (scaled Bellman form)
```

### F.2 Component proof (Task 8 of the Micro-Rev)

1. **Scheme definition:** as above; the fixed point exists uniquely (order-preserving contraction, §D.1).
2. **Monotonicity:** the scaled operator has nonnegative weights m·d⁺/(ρ+m|d|), m·d⁻/(ρ+m|d|) and is nondecreasing (order-preserving); the residual form has positive diagonal ρ + m|d| and nonpositive off-diagonals — no row-sum condition imposed.
3. **Stability:** max-principle gives |u_m| ≤ ‖g‖∞/ρ uniformly.
4. **Interior consistency:** at x ∈ (0,1), for φ ∈ C²: S_m(x_i, φ) → ρφ(x) − max_{d ∈ [−1,1]}{g(d) + φ'(x)d} (Taylor, upwind exactness, O(1/m) remainder) — both inequality directions at interior test points.
5. **State-constraint boundary half-relaxed-limit inequality:** at x̂ = 0, φ touching ū from above. Maximizer sequences visit either x_0 = 0 (boundary node; operator limit H_T(0, φ') = max_{d ∈ [0,1]}{g + φ'd}; the boundary inequality ρV(0) ≤ H_T(0, φ') holds for the toy by the elementary argument: the optimal control at 0 exists (compact [0,1]) with drift d* ∈ [0,1] (viability), and the DP gives ρV(0) = g(d*) + V'(0+)·d* ≤ g(d*) + φ'(0)d* ≤ H_T(0,φ')) or interior nodes x_i → 0 (operator limit H_int = max_{d ∈ [−1,1]}{g + φ'd} ≥ H_T by cone containment [0,1] ⊆ [−1,1], so ρV(0) ≤ H_T ≤ H_int a fortiori). **Both branches give limsup S_m ≤ 0** — the boundary one-sided inequality is satisfied. (At x̂ = 1 symmetric.)
6. **Comparison assumption/theorem:** the scalar state-constrained problem has the Soner-type comparison (subsolution on [0,1] vs supersolution in (0,1) — standard for the 1D discounted problem; cited to the primary references in the capsule). With it, the Barles–Souganidis framework yields ū ≤ u̲, hence u_m → V.

### F.3 Role and scope

The toy's role is **only to falsify necessity of the raw Issue-#55 graph condition**: interior points x_i → 0 admit d < 0 (raw graph failure: limsup A_m(x_i) ⊇ [−1,1] ⊄ [0,1] = T(0)), yet all operator-consistency components hold. The toy does NOT prove the project's 2D frozen architecture converges — the project's boundary transfer has the Outcome-B gap (§E.4), explicitly not claimed here.

---

## Summary of Part D+E+F (Micro-Rev)

- Legitimate target: order-preserving (monotone) + stable + interior-consistent + one-sided boundary consistency via the control/payoff-level bridge + comparison hypothesis — all stated in the fixed project convention (Task D corrected).
- Frozen process: all consistency components verified at the control level under the frozen finite-m taxonomy (0 violations); the control-level bridge liminf H_R ≥ H_T holds at both W-corners (Task C); the counterexample drift is corrected (μ_W = 1, Task F); the taxonomy is relabeled (endpoint layers vs physical limit-region partitions, Task E).
- Single bounded gap (Outcome B): the constrained characterization ρV ≤ H_T at the boundary and the comparison for the project's continuous limit problem — blocks the W-contact-state branch of the boundary subsolution transfer, declared explicitly.
- Toy: YES with the full component proof (Task 8).
