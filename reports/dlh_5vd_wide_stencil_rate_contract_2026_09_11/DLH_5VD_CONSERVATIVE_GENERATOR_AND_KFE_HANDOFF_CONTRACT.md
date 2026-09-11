# DLH-5V-D — Conservative Generator and KFE Handoff Contract

**Issue:** deep-learning-hank #52 (DLH-5V-D) · **Branch:** `dsh/issue-52-dlh-5vd-wide-stencil-rate-contract-2026-09-11`
Covers Issue §6.5 (conservative row construction), §6.6 (same-Q KFE handoff), §6.7 (mass/density downstream),
§6.8 (future validation gates — record only), §6.9 (scope-sufficiency warning / remaining sector). Design-only;
nothing here is executed.

---

## 1. Conservative row construction (Issue §6.5) — frozen, by construction

For every selected control in the frozen sector, the **actual represented asset off-diagonal rates** are exactly

```
q_in >= 0   (edge s -> s_in = (j-1,i))
q_T  >= 0   (edge s -> s_T  = (j-7,i+10))
```

(both destinations are represented in the regular region, so there are no outside/off-grid asset destinations).
The asset diagonal is defined as the negative sum of these actual outgoing rates:

```
Q_ss(asset) = -(q_in + q_T) = -sum_{r != s, asset edges} Q_sr.
```

With productivity switching included downstream, the full row obeys

```
Q_ss = -sum_{r != s} Q_sr        (over all actual represented outgoing rates)
Q 1 = 0                           BY CONSTRUCTION, not by later repair.
```

**Forbidden failure mode (explicitly):** omitting an outside/off-grid destination while retaining its negative
diagonal escape rate — i.e., a diagonal entry that includes an exit rate whose destination is not an actual
represented state. In the frozen sector this cannot arise (both destinations represented); the rule is frozen
to prevent leakage in any later endpoint/implementation stage. No later row-sum repair is permitted.

## 2. Same-Q KFE handoff (Issue §6.6) — frozen (conditional on full regular-sector closure)

The one-`Q` principle is frozen **conditionally on full regular-sector closure**. This Issue freezes only the
`sector-candidate scoring rule` for the `T_realloc` sector (see the rate-decomposition report); the global
regular-W-boundary maximization is deferred until the remaining sector `{mu_b < 0, mu_W <= 0}` receives its own
accepted transition/rate contract. After that closure:

```
all admissible candidates (all regular sectors)
 -> sector-specific candidate-control rates inside H_h (before maximization)
 -> ONE global discrete H_h argmax
 -> selected control + its already-defined sector-specific rates
 -> ONE backward generator Q
 -> future KFE consumes exactly Q^T
```

- KFE must **not** rebuild boundary rates from drifts independently; the converged/accepted `Q` is the **sole
  forward-process input**.
- This preserves the accepted binding law `HJB boundary policy <=> KFE boundary transition law` with one
  controlled process and one generator.

## 3. Mass / density downstream semantics (Issue §6.7) — frozen, not executed

```
p = M g
p_dot = Q^T p
future stationary source-free equation: Q^T p = 0
```

- Aggregates use mass weights `p` (density via cell weights / mass matrix `M`).
- A pin/normalization operation is **downstream scale fixing only** and must validate the **original**
  `Q^T p` residual afterward; it may never repair leakage.
- Issue #27 component-pin authority remains unchanged and downstream; this Issue does not redesign pinning.

## 4. Future generator/KFE validation gates (Issue §6.8) — record only, not executed

Future implementation acceptance must record at least:

- finite entries;
- nonnegative off-diagonal rates (`Q_ij >= 0`, `i != j`);
- `||Q 1||_inf` / row-sum conservation;
- orientation/flattening contract;
- exact same `Q` handed from HJB to KFE;
- SCC / closed recurrent-class diagnostics (before any uniqueness claim);
- stationary original-equation residual `Q^T p` (source-free);
- mass normalization and nonnegativity;
- density conversion using cell weights.

None of these downstream numerical gates are run in this Issue.

## 5. Scope-sufficiency warning — remaining regular sector (Issue §6.9)

The continuous tangent cone at the W-frontier (away from other economic boundaries) is the half-plane
`{mu_W <= 0}`. This Issue freezes only the reallocation sector

```
T_realloc = {mu_a <= 0, mu_b >= 0, mu_W <= 0}.
```

**Other admissible regular W-boundary drift sectors remain outside this contract.** Precisely, the
tangent-admissible complement is

```
{mu_W <= 0} \ T_realloc = {mu_b < 0, mu_W <= 0} = {mu_b < 0, mu_a <= -mu_b},
```

decomposing into two sub-sectors:

1. **reverse reallocation (b -> a):** `mu_a > 0, mu_b < 0, mu_a + mu_b <= 0` (the Issue's example
   `mu_a>0, mu_b<0, mu_W<=0`); a reverse tangent would require the mirror wide stencil `(+7,-10)` — **not designed
   here**;
2. **both-inward depletion:** `mu_a <= 0, mu_b < 0, mu_W <= 0` — b decreasing with a non-increasing, moving off the
   frontier.

(The sub-sector `{mu_a > 0, mu_b >= 0, mu_W <= 0}` is empty within the tangent cone: `mu_a>0` and `mu_b>=0` imply
`mu_W > 0`.)

**Statement:** this Issue does **not** claim full regular-boundary closure — prior accepted authority proves the
`T_realloc` sector only. The remaining regular-sector object `{mu_b < 0, mu_W <= 0}` is identified explicitly as
the **next bounded scientific object** (a remaining-sector/reverse-tangent gate), and no remedy is designed here
(per Issue §10 forbidden list).

## 6. Cross-project KFE safeguards (Issue §4) — adopted, not imported as authority

The independently supplied Chapter-5 clean/source-free KFE contract contributes **design constraints only**,
consistent with existing authority:

```
Q backward; Q^T forward; off-diagonal >= 0; diagonal = -sum of actual outgoing; Q 1 = 0;
same Q for HJB/KFE; stationary object = mass p (Q^T p = 0); pin/normalization = scale fixing only,
never leakage repair; original source-free residual must be validated downstream.
```

The MATLAB-faithful contaminated-row/pinning reproduction logic from that other project is **not** imported as
production KFE design; Issue #27 component-pin authority remains unchanged and downstream.
