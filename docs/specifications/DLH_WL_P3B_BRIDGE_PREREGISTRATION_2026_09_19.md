# DLH-WL-P3B — bridge and source preregistration for Branch B

Issue: **#81 / `DLH-WL-P3B`** — bridge / source preregistration gate.
Owner route: `DLH-WL-V1-20260918`.
Authority marker: `DLH_WL_P3B_BRIDGE_SOURCE_PREREGISTRATION_AUTHORIZED`.
Reviewer final activation comment: **`5741234971`**.
Operative baseline: `1f4bee7290da7143fab9612157bd99f83e3216b4`.
Dedicated branch: `dsh/issue-81-dlh-wl-p3b-bridge-preregistration-2026-09-19`.

Status: **preregistration only.** No real label was constructed. No empirical adapter was
written. No model was fitted or trained. No dataset was downloaded, scraped, purchased,
ingested or opened. Scientific / model / training calls = **0**.

Companion documents:

1. this preregistration;
2. `docs/data/DLH_WL_P3B_SOURCE_BRIDGE_SENSITIVITY_MATRIX_2026_09_19.md` — source × bridge ×
   sensitivity matrix;
3. `docs/data/DLH_WL_P3B_REGION_MELL_PROVENANCE_CONTRACT_2026_09_19.md` — region dictionary,
   `m`/`ell` provenance, weights / harmonization / leakage contract;
4. `reports/dlh_wl_p3b_2026_09_19/DLH_WL_P3B_REPORT.md` — Issue report and terminal.

---

## 0. Decision

```
DLH_WL_P3B_BRIDGE_PREREGISTRATION__PASS__CANDIDATE_AVAILABLE
```

At least one source family (T — the NBS census / 1% sample bilateral multi-year transition
object) carries a mathematically explicit bridge candidate with named assumptions, named
failure conditions and named sensitivity axes. **This does not authorize empirical fitting.**
It means only that a later, separately authorized source-verification / adapter Issue could
implement the preregistered design once the E3/source-schema, region-dictionary, `m`/`ell`
and weighting requirements of the companion documents are satisfied.

The three bridges are treated as **logically separate and individually non-automatic**, per
Issue #81 §1.

### 0.1 Frozen vocabularies used without modification

**P1B six-class label-semantic taxonomy** (accepted, closed):

```
TRUE_ANNUAL_OD_FLOW                  ANNUAL_OD_STOCK_OR_SAMPLE_CROSSTAB
MULTIYEAR_TRANSITION_OR_DERIVED_PROXY  PROVINCIAL_AGGREGATE_PROXY
RULE_GENERATED                       SYNTHETIC
```

`RULE_GENERATED` and `SYNTHETIC` are project-internal classes (`N/A` for real-data bridge
design); they are carried through P3A's classification of the six real-data candidates and
appear here only so the closed set is complete.

**Bridge vocabulary** (Issue #80 §4, reused unchanged by Issue #81):

```
NONE                     no bridge required (only a TRUE_ANNUAL_OD_FLOW object)
STOCK_TO_FLOW            snapshot -> flow / duration-turnover bridge
ANNUALIZATION            multi-year object -> annual object
SPATIAL_DECOMPOSITION    marginals -> pair distribution (modelling assumption, not mechanical)
OTHER                    a declared bridge outside the four above
```

**Assignment of the bridge vocabulary to the source families and bridges of this Issue** —
this mapping is part of the preregistration and may not be changed after any outcome:

| Bridge / family | `bridge_required` | Why |
|---|---|---|
| time bridge, family T | **`OTHER`** (equivalently, a k-year→annual *timing* bridge) | the object is a residence **transition**, not a count to be annualized. `ANNUALIZATION` is reserved for count-like objects; a stochastic root or generator-based annualization is a timing model, so the P3A assignment `OTHER` is carried forward |
| stock bridge, families S and C | **`STOCK_TO_FLOW`** | snapshot → flow requires a duration/turnover statement |
| population → labor-service, all families | **`OTHER`** | a unit/subpopulation bridge, neither spatial nor temporal |
| family T3 (multi-year proxy) | **`NONE`** *for the proxy itself*, but the proxy is not the target | T3 requires no bridge because it makes no annual claim; that is precisely why it cannot be `W^L` |
| geodoi aggregate components | **`SPATIAL_DECOMPOSITION`** if ever attempted, and **excluded from pair-label design** | marginals never identify the pair distribution |
| a hypothetical `TRUE_ANNUAL_OD_FLOW` source | **`NONE`** | not available for any Chinese province source (P3A) |

## 1. Notation and the target

Regions `i, j ∈ 𝓡` (`|𝓡| = n`); time index `t`; period length one year unless stated. The
frozen V1 object (P1B §1.1):

```
W^L_ii,t = 0 ;  W^L_ij,t >= 0 ;  sum_{j != i} W^L_ij,t = 1
P_ii,t = 1 - m_i,t ;  P_ij,t = m_i,t * W^L_ij,t  (j != i) ;  F_ij,t = ell_i,t * P_ij,t
```

Define, for any row-stochastic annual matrix `P` on `𝓡`:

- `h_i := 1 - P_ii` — the annual **outflow probability** of origin `i`, i.e. the candidate
  `m_i,t` if `P` is authorized;
- `W_ij := P_ij / h_i` (`j ≠ i`) — the annual **conditional destination share** implied by `P`;
- for an integer `k ≥ 1`, `W^(k)_ij := (P^k)_ij / (1 - (P^k)_ii)` — the **k-year conditional
  destination share** implied by `P`.

Observed objects are written:

- `T^(k)` — a **k-year residence-transition matrix** (rows sum to 1, diagonal = those who did
  not change residence province, off-diagonal = those who did, over a window of length `k`);
- `S` — a **stock / sample cross-tab** (persons present at one moment, classified by origin and
  destination), no time dimension of moves;
- `ℓ` — a **people-based OD object** of either kind, viewed as a unit question.

Three distinct obstacles separate an observed object from `W^L`:

| Obstacle | From | To | Section |
|---|---|---|---|
| **time** | `T^(k)` (k-year transitions) | annual `P`, hence annual `W` and `m` | §2 |
| **stock→flow** | `S` (presence) | annual `F`, hence annual `W` | §3 |
| **population→labor-service** | persons | labor services | §4 |

## 2. Time bridge (family T): `T^(k) → P → (m, W)`

### 2.1 The inverse problem, stated exactly

Given `T^(k)`, an **admissible annualization** is any `P` satisfying

```
(A1) P >= 0                      (non-negativity)
(A2) P · 1 = 1                   (row stochasticity)
(A3) P_ij = 0 wherever the support mask forbids the pair   (support admissibility)
(A4) P^k = T^(k)                 (window consistency)
```

`P3B concern`: (A1)–(A3) are checkable; (A4) is a system of `n²` polynomial equations in `n²`
unknowns, and its solution set is what determines identifiability.

### 2.2 T1 — stochastic annualization by matrix root

**Definition.** `𝓕(T^(k)) := {P : (A1)–(A4)}`. The bridge is *identified* iff `|𝓕| = 1`, or
iff every `P ∈ 𝓕` induces the same `(m, W)`.

**Finding T1-a — existence is NOT guaranteed.** Row-stochasticity of `T^(k)` does not imply
`𝓕 ≠ ∅`.

*Proof for the 2-region exchange object.* Let `T = [[0,1],[1,0]]` and suppose `P` satisfies
(A1), (A2), (A4). Write `P = [[x, 1-x],[1-y, y]]` with `x, y ∈ [0,1]`. From `(P²)_11 = 0`:
`x² + (1-x)(1-y) = 0`. Both terms are non-negative, so `x = 0` and `(1-x)(1-y) = 0`, hence
`y = 1`. Then `(P²)_21 = (1-y)(x+y) = 0`, but `T_21 = 1`. Contradiction. ∎

Equivalently, by the eigenvalue argument: `T` has eigenvalue `-1`; a stochastic `P` has
spectral radius 1, so `P²`'s eigenvalues are squares of `P`'s, forcing `P` to have the
eigenvalues `±i`. A real `2×2` matrix with eigenvalues `±i` has trace 0 and determinant 1,
hence `bc = -1 - a² < 0`, so `b` and `c` cannot both be non-negative. ∎

*Interpretation.* A window in which the two regions essentially exchange their populations
cannot be annualized by any real non-negative stochastic root. **Admissibility of the bridge
is an empirical question about the observed matrix, to be checked, not assumed.**

**Finding T1-b — when a solution exists it need not be unique.**

*Exact counterexample (2 regions, k = 2).* Let

```
T^(2) = [[5/8, 3/8],
         [3/8, 5/8]]
```

Then **both**

```
P_A = [[1/4, 3/4],        P_B = [[3/4, 1/4],
       [3/4, 1/4]]               [1/4, 3/4]]
```

satisfy (A1)–(A4): `(P_A)² = (P_B)² = T^(2)` (verified by direct multiplication:
`1/16 + 9/16 = 10/16 = 5/8` and `3/16 + 3/16 = 6/16 = 3/8`). They are distinct and both
non-negative and row-stochastic. The implied accounting input differs by a **factor of three**:

```
m_i from P_A = 1 - 1/4 = 3/4
m_i from P_B = 1 - 3/4 = 1/4
```

So from identical two-year data the annual outflow share is either `3/4` or `1/4`. Note also
that the naive "divide the k-year off-diagonal by k" rule would give `3/16`, which is neither
root: **the naive rule is not a valid annualization.**

*General structural reading — algebraic versus admissible roots.* For `n = 2` and `k = 2` the
solution set can be characterized exactly. Write the annual matrix and the observation as

```
P = [[1-a, a],        T^(2) = [[1-A, A],
     [b, 1-b]]                 [1-B, B]]        s := a + b
```

Then `T_12 = a(2-s) = A` and `T_21 = b(2-s) = B`, so for a stochastic `T^(2)` (which forces
`0 ≤ A, B ≤ 1`) the system reduces to

```
s² - 2s + (A + B) = 0          =>   s = 1 ± sqrt(1 - A - B)      (real iff A + B <= 1)
a = A / (2 - s),   b = B / (2 - s)
```

Two facts must be kept apart and are binding on any later implementation:

1. **two ALGEBRAIC roots** `s = 1 ± √(1-A-B)` exist whenever `A + B < 1`; but
2. a root is an **ADMISSIBLE stochastic root** only if, componentwise,
   `a = A/(2-s) ∈ [0,1]` **and** `b = B/(2-s) ∈ [0,1]`. Both roots have `0 < s < 2`, so
   `2 - s > 0` and `a, b ≥ 0` hold automatically; the binding requirement is
   `max(A,B) ≤ 2 - s`.

It follows that the low-`s` root `s₋ = 1 - √(1-A-B)` is admissible for **every** admissible
`T^(2)` (because `2 - s₋ = 1 + √(1-A-B) ≥ 1 ≥ max(A,B)`), so exactly one admissible stochastic
root always exists, while a **second** admissible root exists iff

```
max(A,B) <= 1 - sqrt(1 - A - B)      equivalently      m*² - 2 m* + (A + B) >= 0,
                                                       m* := max(A,B)
```

(the equivalence follows from `1 - m* ≥ √(1-A-B) ≥ 0` after squaring both sides).

**Concrete one-root example.** `A = 0.90`, `B = 0.01`, so `A + B = 0.91 < 1`. The algebraic
roots are `s = 1 ± √0.09 = 0.7` and `1.3`. For `s = 1.3`, `2 - s = 0.7` and
`a = 0.90/0.7 ≈ 1.286 > 1` — the high-`s` root is **not** stochastic. Only `s = 0.7` is
admissible, with `a ≈ 0.6923`, `b ≈ 0.0077`.

**Concrete two-root example.** `A = B = 3/8`, so `A + B = 0.75`. Roots `s = 0.5` and `1.5`, giving
`a = b = 0.25` and `a = b = 0.75` — both componentwise admissible. This is the case used in
Finding T1-b above.

**Correct non-uniqueness statement.** Multiplicity **can occur**, and occurs on a nonempty
admissible subset (e.g. `A = B = 3/8`); it is **not** claimed for every `A + B < 1`. That is all
the identification argument needs: a single admissible two-root case suffices to show that the
observation does not determine the annualization, so the bridge must enumerate the admissible set
rather than assume a unique root.

**Finding T1-c — the continuous-time (generator) route restricts but does not rescue
identification.** Require additionally that `P = exp(Q)` for a generator `Q` (off-diagonal
`≥ 0`, rows sum to 0), i.e. `T^(k) = exp(kQ)` — the Markov-embedding problem.

- Necessary condition: `det(T^(k)) = exp(k · tr Q) = exp(-k Σ_i λ_i) > 0`, where
  `λ_i = Σ_{j≠i} Q_ij ≥ 0`. A **zero, negative or non-real determinant excludes embedding**.
  The exchange object of Finding T1-a has `det = -1` and is therefore excluded on this route
  as well.
- For the `T^(2)` of Finding T1-b: `det = 1/4 > 0`, and the generator route is available:
  `e^{-4q} = 1/4` gives `q = (ln 4)/4`, so the embedded annual matrix is
  `P = [[3/4, 1/4],[1/4, 3/4]] = P_B`. The embedding route therefore selects **one** of the
  two discrete roots — and it selects the low-mobility one, off-diagonal `1/4`, not `3/4`.
- But embeddability is **not** implied by row-stochasticity, and the embedding itself is not
  unique in general (complex-logarithm branches can yield real generators when eigenvalues
  have equal modulus). It may reduce multiplicity; it may not be assumed to eliminate it.

**Finding T1-d — what multiplicity does to the training target.** Even when `|𝓕| > 1`, the
**k-year** conditional share is the same for every member of `𝓕`, because it is a function of
`T^(k)` alone. The **annual** conditional share is not. In Finding T1-b the annual share is
trivially `1` for the single foreign destination, so the multiplicity shows up in `m`, not in
`W`. For `n ≥ 3` both can differ; the identification statement that must be preregistered is
therefore:

```
the time bridge alone identifies NEITHER W nor m unless
   (i)  |F(T^(k))| = 1, or
   (ii) a selection rule is preregistered in advance (section 2.6), and
   (iii) the induced spread of (m, W) over F is reported and within the preregistered
         tolerance.
```

**Finding T1-e — a single k cannot identify `P` from a sequence of windows either.** The
available waves (T family) are all `k = 5`. Consecutive non-overlapping windows give
`P_1^5 = T_1`, `P_2^5 = T_2`, … — one equation per window, no nested structure, so no
additional restriction on any single `P_w`. Observing the **same** window at two different `k`
would constrain `P` much more strongly, but no candidate source documents a second reference
length, so that route is currently **unavailable**.

### 2.3 T2 — low-mobility hazard approximation

**Definition.** For a k-year window, the first-order (Poisson / low-mobility) annualization

```
P̂ := I + (T^(k) - I)/k        i.e.   P̂_ij = T^(k)_ij / k  (j != i),
                                     P̂_ii = 1 - (1 - T^(k)_ii)/k
```

**Admissibility.** `P̂` **always satisfies (A1) non-negativity and (A2) row-stochasticity** for
every `k ≥ 1` (`T^(k)_ij ≥ 0`, and `1 - (1-T^(k)_ii)/k ≥ 0`). It does **not** automatically
satisfy (A3) support admissibility, and it generally **fails (A4)**:

- **(A1), (A2) automatic.** As stated.
- **(A3) NOT automatic.** If the declared annual support mask forbids the pair `i→j`, an indirect
  k-year path can still produce `T^(k)_ij > 0`, and then `P̂_ij = T^(k)_ij/k > 0`, which violates
  the annual support mask. `P̂` therefore satisfies (A3) **iff every positive off-diagonal entry
  of `T^(k)` is support-admissible under the declared annual mask**. This is a checkable
  condition on the observed object, not a property of the formula. When it fails, the observed
  window already contradicts the declared support and the block must fail closed (§5 of the
  region contract); the support mask is a design object (P1B §3.4) and may not be widened to
  accommodate an observation.
- **(A4) generally fails.** `P̂^k ≠ T^(k)` in general; the residual order is given below.

**Error, with the two distinct orders stated separately.** Write the exact annual matrix as `P`
with `T^(k) = P^k` and let `A := P - I` (so `A_ij = P_ij ≥ 0` for `i ≠ j`, `A_ii = -h_i ≤ 0`).
Then `T^(k) - I = kA + C(k,2)A² + O(k³‖A‖³)` and

```
(1) one-year matrix error
      P̂ = I + A + ((k-1)/2) A² + O(‖A‖³)
      P̂ - P = ((k-1)/2) A² + O(‖A‖³)              =  O(k ‖A‖²)
```

The one-year error is **second order in the annual hazard scale** `‖A‖`. Equivalently, since
`h_i = 1 - P_ii` and `1 - T^(k)_ii ≈ k h_i` for small mobility, it is `O((π^(k))²/k)` where
`π^(k) := max_i (1 - T^(k)_ii)` is the largest k-year one-way outflow probability.

```
(2) k-step reconstruction residual
      let  delta := P̂ - P = ((k-1)/2) A² + O(‖A‖³)
      P̂^k - P^k  =  SUM_{r=0}^{k-1} P^r  delta  P^(k-1-r)  +  O(‖delta‖²)
                  =  O( k * ‖delta‖ )  =  O( k² ‖A‖² )        (generically)
```

Each `P^r` is stochastic, so `‖P^r‖ = O(1)` for every `r`, and the k-term sum contributes a
factor `k` on top of `‖δ‖ = O(k‖A‖²)`. The k-step residual is therefore **second order** in
`‖A‖` with a `k²` factor, **not** third order. It is an `O(·)` statement, not an identity: it is
the first-order-in-`δ` bound, attained generically, and P3B does not claim a matching lower bound
or any cancellation.

**Consequence for use.** Because the residual is `O(k²‖A‖²)`, a T2-annualized matrix must never be
re-substituted into `P^k` and compared with `T^(k)` as a self-consistency test: that test would
reject valid inputs and accept nothing. The admissible consistency checks are (a) the one-year
error bound (1), (b) `C1`, and (c) the (A3) support check above.

**Preregistered applicability condition (must be checked at adapter time, not assumed).**

```
C1:  pi^(k) := max_i ( 1 - T^(k)_ii )  <=  pi_max
```

with `pi_max` frozen by Reviewer authority **before** any outcome is computed (P3B
deliberately does not choose a numeric `pi_max`: choosing it now, with no data, would be
arbitrary, and choosing it after seeing results would be outcome-driven — see §2.6).

**Failure conditions for T2.**

- `C1` violated → the second-order term is not negligible and T2 must **not** be used;
- some `T^(k)_ij > 0` on a pair forbidden by the annual support mask (A3 not satisfied) → the
  observed window contradicts the declared support and the block must **fail closed** (§5 of the
  region contract);
- `T^(k)_ij` negative or non-finite, or a row sum departing from 1 beyond the frozen numerical
  tolerance → the observation is not a valid k-year transition matrix and the block fails closed.

### 2.4 T3 — direct multi-year conditional share as a proxy

**Definition.** `W^(k)_ij := T^(k)_ij / Σ_{l≠i} T^(k)_il`.

**T3 requires no annualization and therefore has no numerical error.** It nevertheless does
**not** equal the annual conditional share, and the discrepancy is **structural, not
numerical**.

**Exact demonstration.** Let `P = circ(1/2, 3/10, 1/5)` on three regions, i.e.

```
P = [[1/2, 3/10, 1/5],
     [1/5, 1/2, 3/10],
     [3/10, 1/5, 1/2]]
```

`P` is row-stochastic and non-negative, so it is an exact, known annual matrix with

```
W_12 = (3/10)/(1/2) = 3/5 = 0.600,      W_13 = (1/5)/(1/2) = 2/5 = 0.400
```

Its two-year transition matrix is `P² = circ(37/100, 34/100, 29/100)` (exact: the cyclic
convolution of `(1/2,3/10,1/5)` with itself is `(0.37, 0.34, 0.29)`). Hence

```
W^(2)_12 = 0.34/(1 - 0.37) = 34/63 ≈ 0.53968
W^(2)_13 = 0.29/(1 - 0.37) = 29/63 ≈ 0.46032
```

so `W^(2)_12` understates `W_12` by `(0.600 - 0.53968)/0.600 ≈ 10.05 %`, **with the annual
matrix known exactly and no annualization error whatsoever**. The distortion is caused purely
by aggregating a year's moves into a five-year endpoint: a person who moves `i → l → j` inside
the window is recorded as `i → j`, and a person who moves `i → j → i` is recorded as a
non-mover, shrinking the apparent mover denominator.

For the same `P`, extending the window to `k = 5` gives `P⁵ = circ(0.333250, 0.334120,
0.332630)` (the cyclically-convoluted fifth power), so

```
W^(5)_12 = 0.334120/(1 - 0.333250) ≈ 0.50112
```

i.e. a `≈ 16.5 %` understatement at `k = 5`. **In this constructed circulant example** the
distortion increases from `k = 2` (`10.05 %`) to `k = 5` (`16.48 %`), and its limit is explicit:
as `k → ∞` with `P` **irreducible and aperiodic**, `(P^k)_ij → π_j` (the stationary
distribution), so

```
W^(k)_ij  →  π_j / Σ_{l≠i} π_l
```

which no longer depends on the origin's *current* conditional split at all. **The multi-year
proxy converges to an ergodic composition, deleting exactly the origin-conditional variation
the model is meant to learn.**

**Monotonicity is NOT claimed in general.** Convergence to the ergodic limit does not imply that
the absolute distortion increases monotonically in `k` for every admissible `P`. A subdominant
eigenvalue that is negative or complex makes `P^k` (and hence `W^(k)`) converge
**non-monotonically, possibly oscillatorily**, so the distortion can rise and fall with `k`. What
is claimed in general is only:

- `W^(k) → π_j/Σ_{l≠i}π_l` under irreducibility and aperiodicity (without aperiodicity, `P^k`
  need not converge and only the Cesàro mean does);
- `W^(1) = W` exactly (the window of length one carries no aggregation bias);
- therefore the distortion is zero at `k = 1` and non-zero in general for `k ≥ 2`;
- and the observed `k = 2 → k = 5` growth is a property of **this example**, reported as such.

Any future claim about the direction or monotonicity of the T3 distortion for a real window must
be established for that window, not inherited from the illustration.

**First-order decomposition of the bias (small mobility).** With `A = P - I`, `h_i = 1 - P_ii`,
`ρ_i^ret := Σ_{l≠i} W_il P_li` (annual return propensity of origin `i`) and
`R_ij := Σ_{l≠i,j} P_il P_lj` (two-step routing through a third region), expanding
`W^(k)_ij = (P^k)_ij / (1 - (P^k)_ii)` to first order in `‖A‖` gives, up to the normalization
constant fixed by `Σ_j W^(k)_ij = 1`:

```
W^(k)_ij  ∝  W_ij * [ 1 + ((k-1)/2) * ( rho_i^ret - h_j ) ]  +  ((k-1)/2) * R_ij / h_i
```

The three channels are interpretable: **return migration** (`ρ_i^ret`, inflating the apparent
stay count and hence shrinking the denominator), **destination turnover** (`h_j`, a
destination that itself loses population quickly accumulates less of the k-year endpoint), and
**multi-step routing** (`R_ij`, which makes an indirect route look direct). The bias is
**first order** in the mobility scale — one order worse than the T1/T2 annualization error,
which is second order. This is the quantitative reason T3 must not be treated as an
acceptable substitute for annualizing first.

**Magnitude caveat (stated honestly).** The illustrative `P` above has annual off-diagonal
probabilities of 20–30 %, far above real interprovincial annual migration. Its error
*magnitudes* are therefore not a forecast. What it establishes is structural: the bias is
non-zero, is systematic rather than noise, has a known ergodic limit, and is **not repairable by
better annualization**. A real magnitude — including whether the distortion rises or falls across
the window lengths a source actually offers — must be quantified at adapter time under the
preregistered sensitivity design.

### 2.5 What each time-bridge family may claim

| Family | Mathematical status | Claim ceiling | Usable as `W^L`? |
|---|---|---|---|
| T1 (stochastic root / embedding) | explicit; existence checkable; multiplicity must be enumerated | an **annual** transition matrix on the covered support, conditional on the preregistered selection rule and the reported spread | **candidate**, not identified by data alone |
| T2 (low-mobility) | explicit with `O(k‖A‖²)` error; validity conditional on `C1` | an **annual** transition matrix within the stated error, **only** after `C1` is verified | **candidate, conditional on `C1`** |
| T3 (proxy) | exact, but structurally biased and non-repairable | a **k-year** conditional destination share among k-year residence changers | **NO** — proxy only; may not be relabelled annual and may not silently become the empirical target |

### 2.6 Preregistered selection rule (fixed before any outcome is seen)

If and only if a later Issue is authorized to build the T bridge, the annualization must be
selected by the following **deterministic, outcome-independent** rule, applied identically to
every window and every sensitivity replicate:

```
S1. Enumerate F_enum := all admissible annualizations found by the preregistered search
    (principal real k-th root; generator-based exp(Q) when embeddable; the T2 approximation
    P_hat; and any further roots located by the preregistered numerical procedure).
S2. If F_enum = {} -> the bridge does not exist for that window; FAIL CLOSED (no bridge).
S3. Preference order, applied without reference to any outcome:
      (a) the generator-based annualization exp(Q) if T^(k) is embeddable; else
      (b) the principal real non-negative k-th root if it is stochastic; else
      (c) the T2 approximation P_hat, provided C1 holds; else
      (d) FAIL CLOSED.
S4. Regardless of the selection, REPORT every member of F_enum and the induced spread of
    (m, W) across F_enum.
S5. If |F_enum| > 1 and the induced spread of any W_ij exceeds the tolerance tau_W, the
    window is declared NOT IDENTIFIED and its empirical target is withheld.
```

`tau_W`, `pi_max`, and the numerical search parameters are **frozen by Reviewer authority
before execution**. P3B does not fix their numeric values, and states why: with no data, any
numeric choice would be arbitrary, and any choice made after seeing results would be
outcome-driven selection, which Issue #81 §9 forbids.

**Prohibitions attached to §2.**

- no assumption that a stochastic root exists;
- no assumption that a stochastic root is unique;
- no assumption that the embedding is unique;
- no use of a multi-year proxy as an annual `W^L`;
- no choice of annualization, selection rule, tolerance or sensitivity level after seeing any
  outcome.

## 3. Stock→flow bridge (families S and C): `S → F → W`

### 3.1 Accounting statement and the exact equality condition

`S_ij(t)` counts persons **present at `t`** whose origin is `i` and destination is `j`; it
carries no information about when or whether a move occurred in the current period. Let
`F_ij(t)` be the annual i→j flow (new moves realized in `t`) and `D_ij(t)` the mean duration
of stay in `j` of completed i→j episodes (the time a person remains counted in `S_ij`).

**Little's law applied per origin–destination cell** (valid for a stationary or
slowly-varying system, and exactly valid in steady state):

```
S_ij  =  F_ij * D_ij
```

**Proposition (equal shares ⟺ equal durations on the positive-flow support).** Fix origin `i`
and assume the total outflow is positive, `Φ_i := Σ_{l≠i} F_il > 0`. Then

```
F_ij / Σ_{l≠i} F_il  =  S_ij / Σ_{l≠i} S_il     for every j ≠ i with F_ij > 0
        if and only if   D_ij = D_il   for all j, l with F_ij > 0 and F_il > 0.
```

*Proof.* `S_ij = F_ij D_ij`. For a cell with `F_ij > 0`, equality of the two normalized shares is
`F_ij D_ij / Σ_l F_il D_il = F_ij / Φ_i`, i.e. (multiplying through by the positive quantities
`Φ_i` and `Σ_l F_il D_il`, and cancelling the positive `F_ij`) `D_ij Φ_i = Σ_l F_il D_il`, i.e.
`D_ij` equals the `F`-weighted mean of the durations over the **positive-flow** destinations.
Holding for every positive-flow `j` is exactly the statement that all positive-flow durations are
equal. ∎

**Zero-flow cells impose no duration restriction.** If `F_ij = 0` then `S_ij = F_ij D_ij = 0` and
both normalized shares are `0` regardless of the value of `D_ij`. The equality therefore says
nothing about `D_ij` for a zero-flow destination, and such a cell must not be used either to
assert or to reject duration equality. (An unobserved cell and a genuinely zero-flow cell are also
different objects under P1B §3.4: `MISSING` versus `OBSERVED_ZERO`.)

**Exact ratio on positive-flow cells.** Dividing the two normalized shares gives, for every `j`
with `F_ij > 0`,

```
stock_share_ij / flow_share_ij  =  D_ij / E_F[ D_i ]
```

where `E_F[D_i] := ( Σ_{l: F_il > 0} F_il D_il ) / ( Σ_{l: F_il > 0} F_il )` is the
flow-weighted mean duration over the positive-flow destinations of origin `i`. So a destination
whose duration exceeds the origin's flow-weighted mean duration is **over-represented** in the
stock share by exactly `D_ij / E_F[D_i]`, independently of its flow share; equality for all
positive-flow cells holds iff `D_ij = E_F[D_i]` for all of them. For a zero-flow cell the ratio is
`0/0` and is left **undefined**, not set to 1.

Equivalently, the **stock-based share is a duration-reweighted version of the flow share**:

```
S_ij / Σ_l S_il  =  ( F_ij D_ij ) / Σ_l ( F_il D_il )       (over positive-flow cells)
```

### 3.2 Identification requirements

To recover `W` from `S` one needs `D_ij` per pair. `D` is **not** observable from a single
snapshot. The admissible routes, in declining order of strength:

| Route | Object required | Status |
|---|---|---|
| d1 | an **individual panel** tracking the same persons across ≥ 2 periods | not documented for any candidate source |
| d2 | a **duration / arrival-time question** in the survey instrument | not documented; questionnaire wording `NOT_VERIFIED_EXTERNAL` |
| d3 | **two or more consecutive snapshots** of the *same* population definition, with individual linkage | requires a panel; see below |
| d4 | a **declared constant-duration assumption** `D_ij = D` | admissible only as an explicitly preregistered assumption with full sensitivity over duration heterogeneity — never as a convenience |

**Finding S-1 — repeated cross-sections do NOT identify turnover.** With two consecutive
snapshots `S(t)` and `S(t+1)` of the same population definition, the cell accounting is

```
S_ij(t+1)  =  S_ij(t)  -  Out_ij(t)  +  In_ij(t)
```

one equation with two unknowns per cell. Only the **net** change is identified; inflow and
outflow cannot be separated, hence neither can turnover nor duration. The CMDS and the
single-year floating-population OD are documented as **cross-sections**, not panels, so
**route d3 is unavailable** to families S and C as currently documented. This is a decisive
negative finding, not a caveat.

**Consequence.** Under currently documented evidence:

```
stock -> flow is NOT_IDENTIFIED for S and for C.
```

`S_ij/Σ_l S_il` remains a **stock share**, may never be reported as an annual flow share, and
may never be substituted for `W^L` (P1B §2.2 items 1–2).

### 3.3 Hukou-origin stock ≠ previous-residence flow

Two different objects are routinely conflated:

- `S^h_ij`: persons in `j` whose **hukou registration** is `i`;
- `S^r_ij`: persons in `j` whose **previous residence** was `i`.

A person whose path was `i → k → j` contributes to `S^h_ij` but not to `S^r_ij`. Therefore
`S^h ≠ S^r` whenever intermediate moves exist, and the difference is `O(η²)` in the mobility
scale — small but **systematically biased**: origins that supply long chains of onward moves
are over-counted in `S^h` relative to `S^r`. A bridge must therefore declare which object it
uses, and the census/floating-population and CMDS objects must be classified explicitly
(companion matrix §3).

### 3.4 Sensitivity axes for the stock bridge

Fixed in advance; all evaluated and reported, none selected on the basis of any outcome:

| Axis | Levels to preregister |
|---|---|
| duration heterogeneity across destinations | ratio `max_j D_ij / min_j D_ij` swept over a preregistered grid, including the value `1` (the equal-duration idealization) |
| duration heterogeneity across origins | same sweep on the origin axis |
| duration–flow correlation | `corr(D_ij, F_ij)` swept from strongly negative through zero to strongly positive |
| duration definition | time since last move / time in current province / time since hukou separation — treated as **distinct** objects |
| origin-type definition | `S^h` versus `S^r` |
| snapshot spacing (if a panel ever exists) | at least two spacings |

## 4. Population → labor-service bridge (mandatory, all families)

### 4.1 The observed unit, per family

| Family | Object | Observed unit | Declared |
|---|---|---|---|
| T | census long-form / 1 % sample migration item | **all persons** (full enumeration / 1 % person sample) — includes children, retirees, non-workers, dependents, students | `ALL_PERSONS` |
| S | single-year floating-population stock OD | **floating population** (residence ≠ hukou), all persons in that category | `FLOATING_POPULATION_ALL_PERSONS` |
| C | CMDS repeated migrant cross-section | documented frame = **migrants only**; whether the issued unit is workers, labor force or all migrants is `NOT_VERIFIED_EXTERNAL` pending codebook verification (DLH-1A E3 queue item 2) | `MIGRANTS__UNIT_NOT_VERIFIED_EXTERNAL` |
| geodoi | provincial aggregate components | no pair dimension | excluded from pair-label bridge design |

### 4.2 The required assumption, stated exactly

Define, for a mover from `i` to `j`, the **expected labor service per observed person**:

```
lambda_ij  :=  E[ labor service | i -> j ]
           =  rho_ij * phi_ij
```

where

- `rho_ij` = the probability that an observed i→j mover is employed (or in the labor force,
  per the declared basis) — the **participation/employment margin**;
- `phi_ij` = `E[ efficiency-labor intensity | i→j and employed ]` > 0 (hours × efficiency) —
  the **intensity margin conditional on being employed**.

So `lambda_ij` carries both margins in one object. Person-based and labor-service destination
shares coincide iff

```
(P-L)   lambda_ij  =  lambda_il      for all l with F_ij > 0 and F_il > 0   (within origin i)
```

i.e. iff expected labor service per observed mover is **constant across the destinations of the
same origin** (on the positive mover support). If `(P-L)` holds, the person-based share **is**
the labor-service share and no bridge is needed. If it fails, the exact correction is

```
W^L_ij  ∝  W^persons_ij * lambda_ij            normalized over j ≠ i
        =  W^persons_ij * rho_ij * phi_ij  /  Σ_{l≠i} W^persons_il * rho_il * phi_il
```

with the same positive-support caveat: for a cell with `W^persons_ij = 0` both shares are `0` and
`lambda_ij` is not identified by the equality.

*Why both margins are needed.* Writing `phi` as "hours × efficiency" while ignoring
participation would silently assume that the employment margin is destination-invariant. It is
not: if employment rates differ across destinations for the same origin, then `rho_ij` varies and
`E[phi | i→j]` alone cannot restore share equality. The Reviewer's HOLD identified exactly this
gap; it is now closed by carrying both margins inside `lambda`.

*Equivalent single-margin formulation.* If instead `phi` is **redefined** to include zero service
for non-workers — i.e. `phi_ij := E[labor service | i→j]` over *all* observed movers, with
`phi = 0` for non-workers — then `lambda_ij ≡ phi_ij` and the separate `rho_ij` is **redundant**
and must be dropped. P3B fixes the two-margin form `lambda = rho · phi` as canonical and requires
any implementation to declare which of the two encodings it uses; the two must not be mixed
inside one evaluation set.

**Finding L-1 — the pair-level and origin-level requirements are related but NOT the same
object.** What the correction above requires is the **pair-level** `lambda_ij`: conditional
expected labor service per observed mover, used to reweight destination shares. What
`ell_i` requires (companion contract §3) is an **origin-level** total labor amount used in
`F_ij = ell_i P_ij`, which additionally involves the origin population/labor basis and, depending
on the accounting, home/stayer labor that the mover-based pair data cannot observe at all.

These are **logically distinct moments**:

| | pair-level `lambda_ij` | origin-level `ell_i` |
|---|---|---|
| what it measures | conditional labor service per **observed mover/person** to destination `j` | **total** origin labor amount entering `F_ij = ell_i P_ij` |
| conditioning | destination `j` within origin `i` | origin `i` only, no destination dimension |
| does it include stayers? | no — movers only | yes, via `P_ii = 1 − m_i` (home retention) |
| used for | reweighting destination shares | scaling the origin's total flow |

A sufficiently rich joint microdata or administrative **labor/employment data system could supply
both coherently**, and pair-level labor-intensity information may aggregate into an origin-level
basis **if** the population frame is complete and weights and stayers are covered. But neither
mechanically identifies the other. P3B therefore preregisters:

```
two LINKED provenance requirements:
   R-lambda : pair-level     lambda_ij  (destination-varying, on the observed mover frame)
   R-ell    : origin-level   ell_i      (total origin labor, consistent with m_i and with the
                                        home/stayer share 1 - m_i)
Both remain separately required fields until a future source proves they come from ONE coherent
frame. Neither may be inferred from the other; neither may be substituted for the other.
```

**Frozen consistency condition.** Let `N_ij` be the observed i→j mover count and `𝓜_i = {j :
N_ij > 0}`. Define the mover-implied labor leaving `i` as

```
ell_i^movers  :=  Σ_{j ∈ M_i}  N_ij * lambda_ij
```

Then any design using both objects must satisfy, with every term declared from the same `(i, t)`:

```
(C-LINK)   ell_i  =  ell_i^movers  +  ell_i^stay  +  ell_i^unobserved
```

where `ell_i^stay` is the home/stayer labor carried by `P_ii = 1 − m_i`, and
`ell_i^unobserved` covers movers outside the observed frame (for a mover-only frame such as S or
C this term is not zero a priori). A design must either (a) supply all three components from one
coherent frame, or (b) **declare which components are unobserved and treat (C-LINK) as a
consistency check with a reported residual** — never as an equality assumed by construction.
`(C-LINK)` is a consistency condition, not an identification of either object.

**Finding L-2 — the failure direction is not innocuous.** If `lambda` rises with destination wage
or return — the very mechanism the model is meant to capture — then `lambda_ij` is positively
correlated with the destination's attractiveness, and the person-based share **systematically
understates** high-wage destinations' labor-service share. The bias is therefore correlated with
the model's own explanatory variables, so it is not a random measurement error and it will not
average out. Report it, do not absorb it silently.

### 4.3 Statements the bridge must make (per Issue #81 §5)

For every family, the bridge preregistration must state:

1. **who is excluded** — children, retirees, non-workers, dependents, students, and (for the
   floating/migrant frames) all non-movers;
2. **whether a mover-only frame distorts destination shares relative to origin labor** — for
   families S and C the frame contains movers only, while `W^L` conditions on the origin's
   labor total `ell_i`; the mapping from a mover-only frame onto origin labor must be declared
   explicitly, and with no real `ell` provenance it currently cannot be;
3. **whether weights can recover the intended labor population** — survey weights can
   reweight *sampled persons* to a *person* population; they cannot invent labor-force status
   that was not collected, so weights can only recover the labor population if the labor
   variables exist in the instrument;
4. **whether efficiency-labor weighting is ignored, approximated, or externally supplied** —
   one of the three must be declared; "ignored" is admissible only as an explicitly
   preregistered approximation with the `(P-L)` assumption and full sensitivity over `lambda`
   (and, if the two-margin encoding is used, over `rho` and `phi` separately).

**Conclusion of §4.** A defensible formulation of the bridge exists (the `(P-L)` assumption on
`lambda_ij` plus the correction formula, or the observable-subpopulation route). Its
**execution** is blocked by two **linked but distinct** missing provenance requirements — the
pair-level `lambda_ij` and the origin-level `ell_i` — which are related through the consistency
condition `(C-LINK)` but neither of which identifies the other. Per Issue #81 §5, this alone
would block empirical `W^L` fitting even if a clean bilateral pair matrix existed.

## 5. Which bridge is preregisterable, and the decision

| Bridge | Explicit mathematics | Named assumptions | Named failure conditions | Sensitivity axes | Candidate? |
|---|---|---|---|---|---|
| T1 time (root / embedding) | yes (§2.2) | time-homogeneous Markov; (A1)–(A4); preregistered selection rule | non-existence (proved); non-uniqueness (proved); non-embeddability | root family; selection rule; spread over `𝓕` | **yes** |
| T2 time (low mobility) | yes (§2.3) | `C1`; `‖A‖` small | `C1` violation; support contradiction | `pi_max`; window `k` | **yes, conditional on `C1`** |
| T3 multi-year proxy | yes (§2.4) | none beyond the observed object | structurally biased, non-repairable, zero at `k = 1`, ergodic limit under irreducibility + aperiodicity; monotonicity in `k` **not** claimed in general | `k` | **no** — proxy only |
| S/C stock→flow | yes (§3) | Little's law; duration structure | turnover not identified from cross-sections (proved); hukou-vs-residence mismatch | duration heterogeneity; correlation; definition | **candidate as a conditional design; `NOT_IDENTIFIED` under current evidence** |
| L population→labor | yes (§4) | `(P-L)`: `lambda_ij = rho_ij phi_ij` constant across destinations within origin, or an observable worker subpopulation | `(P-L)` violation correlated with attractiveness; two linked but distinct missing provenance requirements (`lambda_ij` pair-level, `ell_i` origin-level) related only by `(C-LINK)` | `lambda` gradient; `rho` and `phi` separately | **candidate as a conditional design; execution blocked** |

**Decision.** At least one source family (T) carries a mathematically explicit bridge
candidate with named assumptions, failure conditions and sensitivity axes, and the terminal is
therefore

```
DLH_WL_P3B_BRIDGE_PREREGISTRATION__PASS__CANDIDATE_AVAILABLE
```

The alternative

```
DLH_WL_P3B_BRIDGE_PREREGISTRATION__PASS__NO_DEFENSIBLE_BRIDGE_YET
```

is **not** selected, because the T-family bridges T1 and T2 are explicit and constructible in
principle: T1 admits a fully specified solution set and selection rule, and T2 has a proved
error term with an explicit applicability condition. "Defensible" in Issue #81 §10 means
*mathematically explicit with named assumptions, failure conditions and sensitivity axes*, and
that test is met.

```
DLH_WL_P3B_BRIDGE_PREREGISTRATION__REVIEW_REQUIRED
```

is **not** selected: no internal contradiction was found between the accepted P3A package, the
P1B taxonomy and this analysis. P3A's Branch-B qualification — that Branch B means a bridge
could be *specified*, not that one exists — is exactly what this document formalizes, and the
P3A-flagged closeness of the B/P boundary is unaffected: the identification results in §2–§4
make the "no empirical `W^L` fit now" conclusion strictly stronger, not weaker.

## 6. What this decision does and does not authorize

**Does not authorize:** any empirical fitting or training; any real label set; any empirical
adapter; any download, scrape, purchase or ingestion; any HJB/KFE/GE/MATLAB/household call; any
full-suite run; any automatic P3C successor.

**Does authorize (only):** a later, **separately authorized** Issue to verify the source schema
at E3, instantiate the region dictionary, establish `m`/`ell` provenance, freeze `tau_W`,
`pi_max` and the search parameters, and implement the preregistered bridge — with the
selection rule, the enumeration of `𝓕`, and the sensitivity design of this document applied
unchanged. Until every one of those preconditions holds, the pair target remains
`UNRESOLVED` and empirical `W^L` work remains forbidden.

## 7. Hard prohibitions restated as preregistration invariants

| Invariant | Statement |
|---|---|
| P1 | no silent stock→flow equality: a stock share may never be reported as an annual flow share |
| P2 | no stochastic-root uniqueness assumption without enumeration and proof |
| P3 | no stochastic-root **existence** assumption either: `𝓕 = ∅` must fail closed |
| P4 | no multi-year conditional share relabelled annual, and no use of T3 as the empirical target |
| P5 | no population share relabelled a labor-service share without the explicit `(P-L)` bridge on `lambda_ij` or an observable worker subpopulation |
| P11 | no claim that the pair-level `lambda_ij` and the origin-level `ell_i` are the same object, and no inference of one from the other; both are separately required until a source proves one coherent frame |
| P12 | `P̂ = I + (T^(k) − I)/k` may not be assumed to satisfy the support condition (A3); the positive off-diagonals of `T^(k)` must be checked against the declared annual support mask |
| P6 | no total population substituted for `ell` |
| P7 | no region crosswalk guessed, and no un-mappable label silently merged |
| P8 | no outcome-driven bridge, annualization, selection-rule, tolerance or sensitivity-level choice |
| P9 | no automatic successor; no empirical fit under this Issue |
| P10 | every bridge output carries its class, its assumption record and its claim ceiling |
