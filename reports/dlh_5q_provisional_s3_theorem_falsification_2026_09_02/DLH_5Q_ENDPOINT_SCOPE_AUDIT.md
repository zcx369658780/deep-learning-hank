# DLH-5Q Phase F — Endpoint Theorem Scope Audit

**Issue #43 Phase F (step 23).** Audits the theorem scope separately for compact
interior-`a`, `a=0`, `a=10`, and the lower liquid bound. If current authority only
supports an interior-`a` theorem, state that precisely. Do NOT upgrade finite-grid
endpoint semantics into analytic boundary authority.

---

## F0. Scope question

The `p=2` conditional balance (Phase C/D) is derived on the interior
`(b_lo,+inf) x (0,a_max) x {z}`. The question is how far it extends toward the
boundaries of the illiquid support `[0,10]`.

---

## F1. Compact interior `a in [a_min, 10-eps]` (`a_min > 0`)

- The `R=O(1)` class and the interior balance are coherent here; `K` is `a`-independent
  (forced by `R=O(1)`, Phase C C4), and the conditional `p=2` coefficient system
  (Phase D) holds pointwise on the interior.
- **This is the natural domain for any conditional theorem statement.**
- Required (theorem gates): uniformity of the estimates over
  `[a_min, 10-eps]`, absence of endpoint influence from `a_min` and `10-eps`, and the
  Phase B existence/comparison framework.
- **Status: interior-`a` theorem SUPPORTED only conditionally** (on Phase B/C gates).

---

## F2. `a = 0` bare-`a` corner

- Accepted: `d = a*T(q)/chi_1 = 0` for any `R`, `chi = 0`, `mu_a = 0`; `R` is vacuous
  at `a=0`; the balance at `a=0` is the P-TR form `(rho+r_b)K - 2 sqrt(K) = S*K`.
- `V_b*b^2 -> K` is consistent at `a=0`; the corner does not break the `p=2` tail.
- A theorem must state a corner convention (treat `a=0` by continuity from the
  interior, or as a limit); **no new law is invented**.
- **Status: compatible but requires an explicit corner convention (a mild
  convention decision, not a new economic law).**

---

## F3. `a = a_max = 10` upper endpoint

- Accepted: `r_a_eff(10) = 0.027 > 0`; the finite-grid `at_upper_a` branch restricts
  `d < 0` and is `INHERITED_FINITE_GRID_NUMERICAL_SEMANTICS_ONLY`.
- **No analytic `a=10` boundary law is invented in DLH-5Q.** A full-`[0,10]` uniform
  theorem cannot be stated without one.
- **Status: `a=10` endpoint authority is an OWNER DECISION item
  (`NEW_ANALYTIC_MODEL_DEFINITION_REQUIRES_OWNER`).**

---

## F4. Lower liquid bound `b_lo = -2`

- The borrowing-rate gap (`0.025` for `b<0`) is accepted economics; the `b_lo`
  marginal-utility closure is numerical semantics only.
- Adopting `b_lo=-2` as the continuous analytic lower boundary is new model definition.
- The tail (`b -> +inf`) should be `b_lo`-independent; **b_lo-independence of the tail
  is a robustness/falsifiability gate** (a future numerical protocol tests it).
- **Status: `b_lo` lower-bound adoption is an Owner decision item; tail should not
  depend on it.**

---

## F5. Full `[0,10]` vs interior-`a` theorem scope

| Scope | Status |
|---|---|
| Compact interior-`a` conditional theorem | SUPPORTED only if Phase B/C gates close |
| `a=0` corner | compatible; corner convention needed |
| `a=10` endpoint | NOT supported; analytic `a=10` law is an Owner decision |
| `b_lo` lower bound | adoption is an Owner decision; tail must be `b_lo`-independent |
| Full `[0,10]` uniform theorem | NOT SUPPORTED from current authority |

**Conclusion:** the maximum currently supportable statement is a **compact
interior-`a` conditional theorem**. Full-`[0,10]` authority requires Owner decisions
on the `a=10` upper-`a` law (and the `b_lo` lower-bound adoption). This is recorded as
an explicit endpoint Owner-decision requirement and is one of the reasons the DLH-5Q
theorem is not closed.

---

## F6. Bottom line (Phase F)

Endpoint well-posedness holds cleanly only on the compact interior-`a` set. The `a=0`
corner is compatible (convention needed), `a=10` and `b_lo` are Owner-decision
endpoint items, and no full-`[0,10]` uniform theorem is currently supported. No
analytic `a=10` law is invented; no finite-grid endpoint semantics are upgraded into
analytic authority.
