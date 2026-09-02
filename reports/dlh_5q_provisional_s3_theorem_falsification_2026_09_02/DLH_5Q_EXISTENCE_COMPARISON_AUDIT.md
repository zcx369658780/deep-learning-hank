# DLH-5Q Phase B — Existence / Comparison / Uniqueness Audit (Rev 2)

**Issue #43 Phase B (steps 21-23).** Determines whether the provisional S1+S2+S3
analytic problem currently has enough specification to support existence of an
admissible value solution, comparison/uniqueness, value-level uniqueness under
`V_inf=0`, and endpoint compatibility. No theorem may be claimed from `V_inf=0` alone
(Issue #42 acceptance item 6 controls). Missing assumptions are identified rather than
importing textbook results silently. **Rev 2 corrects the PDE characterization: the
frozen analytic problem is a first-order regime-switching HJB (no second-order term in
the accepted authority), so any proposed viscosity/comparison framework must match
that first-order structure** (reviewer `5506978886`).

---

## B0. What the accepted authority actually provides

The accepted source (`matlab_faithful_two_asset_ha.py`, blob `76ae5b14…`) is a
**MATLAB-faithful finite-grid** HJB solver on `[b_lo,b_max] x [0,a_max] x {z}`. Its
converged fixed point yields a **derivable interior identity** (subject to upwind
finite-difference semantics and smooth-continuum regularity):

```text
rho*V = u + (r_b*b + labor - c)*V_b + r_a_eff(a)*a*V_a + V_b*[d*(R-1)-chi] + S*V.
```

The source authorizes: the exact drift/utility/FOC objects; the algebraic form of the
interior identity including the combined transfer Hamiltonian; and the finite-grid
boundary closures at `b_lo`/`b_max`/`a=0`/`a_max` as **numerical semantics only**.

The source does NOT authorize: an unbounded-`b` asymptotic boundary/transversality
condition; an analytic upper-`a` endpoint law; an analytic lower-`b` law; a
comparison/uniqueness framework; or any statement about the infinite-domain problem.

---

## B1. Existence audit

**Question:** does the provisional problem (S1+S2+S3 on `(b_lo,+inf) x (0,a_max) x {z}`)
currently support existence of an admissible value solution?

**Verdict: NOT ESTABLISHED from current authority.**

The provisional class specifies the operator, the admissibility class (bounded
monotone `V`, `V_inf=0`, `R=O(1)`), and the interior balance. This is close to a
well-posed analytic *statement*, but a rigorous existence theorem for the **continuous
unbounded-`b`** problem requires ingredients that are not adopted:

1. **A solution notion on the unbounded domain.** The frozen analytic problem in this
   Issue is a **first-order** (in the continuous asset variables `(b,a)`) HJB system
   with finite-state Markov switching in `z` — there is no second-order/diffusion term
   in the accepted authority:
   `rho*V = u + (r_b*b + labor - c)*V_b + r_a_eff(a)*a*V_a + V_b*[d*(R-1)-chi] + S*V`.
   It is NOT a second-order degenerate HJB. The natural candidate is therefore a
   viscosity solution (or classical `C^1` solution under additional regularity) of this
   **first-order regime-switching HJB**. The provisional class adopts `C^1` (via S1) as
   an ansatz-level condition, not as a proved existence theorem. A viscosity/comparison
   route (e.g., Perron's method / finite-difference viscosity convergence) may be
   proposed, but it must be stated for the actual first-order regime-switching HJB, and
   on an unbounded domain it still needs a comparison framework and growth/boundary
   data that are not part of current authority.
2. **Boundary data.** The `a=10` upper-`a` law, the `b_lo` lower-`b` law, and the
   `b -> +inf` tail condition (`V_inf=0`) are the boundary data. Two of these
   (`a=10`, `b_lo`) are unresolved endpoint authority (Phase A A4), so the boundary
   value problem is not fully specified.
3. **Uniformity/regularity.** A continuum-existence statement requires uniform
   estimates (e.g., `C^{0,alpha}` bounds, derivative bounds consistent with `R=O(1)`)
   that are theorem-assumption items (Phase A A3.4-A3.7).
4. **No silent import.** We do NOT import a textbook existence theorem (e.g., a
   standard optimal-control HJB existence result) because the provisional authority
   does not adopt the corresponding structural hypotheses (state-space compactness or
   a compatible growth class at `+inf`, Lipschitz control/transition data, boundary
   compatibility), and because `a=10`/`b_lo` endpoint authority is missing.

**What IS supported:** the finite-grid solver converges on its finite grid (accepted
numerical behavior), and the provisional class is a coherent analytic *candidate
problem*. Existence on the continuous unbounded domain is a missing theorem gate.

---

## B2. Comparison / uniqueness audit

**Verdict: NOT ESTABLISHED.** `V_inf=0` alone is NOT a comparison or uniqueness
theorem.

1. **`V_inf=0` pins the value level, not the tail.** Adding a constant to a solution
   changes `V_inf`; imposing `V_inf=0` selects the level (zero constant). But it does
   not distinguish tails with the same `V_inf=0` (e.g., the `p=2` tail and the
   `m=1/2` critical tail both have `V_inf=0`). So `V_inf=0` is a
   level/boundary selection, not a realized-tail uniqueness statement.
2. **A comparison principle would need:** (i) a notion of viscosity (or classical)
   solution for which a comparison theorem holds on the unbounded domain; (ii)
   structural conditions on the Hamiltonian (monotonicity, continuity, and the
   handling of the nonconvex transfer Hamiltonian `V_b[d(R-1)-chi]` near the `chi_0`
   kink and the `max(a,a_bar)` floor); (iii) compatible boundary data (`a=10`, `b_lo`,
   `+inf`); (iv) the `R=O(1)` class used consistently as an admissibility restriction
   on both compared functions. None of (i)-(iv) is established.
3. **Value-level uniqueness under `V_inf=0`:** even granting a comparison principle,
   `V_inf=0` would give level uniqueness only within that framework. Since the
   framework is missing, level uniqueness is not established either.
4. **Missing assumptions (exact list):**
   - a comparison theorem for the degenerate HJB operator on
     `(b_lo,+inf) x (0,a_max) x {z}` with the `V_inf=0` tail data (or an equivalent
     selection argument, e.g., a constructive uniqueness route);
   - resolution of the `a=10` and `b_lo` boundary data (endpoint authority);
   - a proof or justified adoption that the actual solution lies in the `R=O(1)`
     class (S3 necessity/realization), otherwise comparison across classes is moot;
   - derivative-remainder control so that `V_a/V_b` and the coefficient equation are
     well-defined at the required orders.

---

## B3. Endpoint well-posedness audit (step 23, separately)

| Endpoint | Well-posedness status |
|---|---|
| **Compact interior `a in [a_min, 10-eps]`** | The interior balance and the `R=O(1)` class are coherent here; this is the natural domain for any conditional theorem. Endpoint influence from `a_min>0` and `10-eps<10` must be shown absent (or controlled) — a theorem item. |
| **`a=0` bare-`a` corner** | `d=0` for any `R`, `chi=0`, `mu_a=0`; `R` is vacuous; the balance at `a=0` is the P-TR form. The corner does not break the `p=2` tail; `V_b*b^2 -> K` is consistent at `a=0`. Corner conventions must be stated (e.g., treat `a=0` by continuity or as a limit of the interior). No new law. |
| **`a=10` upper endpoint** | `r_a_eff(10)=0.027>0`; the finite-grid `at_upper_a` (`d<0`) branch is numerical semantics only. **No analytic `a=10` law is invented.** A full-`[0,10]` theorem cannot be stated without one; this is an Owner-decision endpoint item. |
| **Lower liquid bound `b_lo=-2`** | The borrowing gap is accepted economics; the `b_lo` marginal-utility closure is numerical semantics only; adopting `b_lo=-2` as continuous analytic lower boundary is new model definition. The tail (`b -> +inf`) should be `b_lo`-independent; this is a robustness/falsifiability gate. |

**Conclusion:** the only currently well-posed analytic domain for a (conditional)
theorem is the compact interior-`a` set, and even there existence/comparison remain
open gates. Full-`[0,10]` authority is absent (endpoint Owner decisions required).

---

## B4. Bottom line (Phase B)

- Existence on the continuous unbounded-`b` problem: **NOT established**; missing
  assumptions enumerated (B1.1-B1.4).
- Comparison/uniqueness: **NOT established**; `V_inf=0` is a level selection, not a
  uniqueness theorem (B2).
- Endpoint well-posedness: only compact interior-`a` is currently well-posed;
  `a=10` and `b_lo` are unresolved endpoint authority; `a=0` is the bare-`a` corner.
- These are precisely the `MISSING_EXISTENCE_COMPARISON` components of the DLH-5Q
  terminal.
