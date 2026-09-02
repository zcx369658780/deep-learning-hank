# DLH-5N Phase D — Theorem / Conditional-Theorem / Counterexample Matrix

**Issue #40 Phase D.** Builds the matrix of what is provable, what is provable only
under an explicit (unproven) assumption, and whether a source-consistent asymptotic
counterexample family exists. All statements are about the fixed-`a` liquid tail
(`a in [0,10]` fixed, `z in {0.8,1.3}`, `b -> +infinity`), derived only from the
accepted source identities and frozen D0 inputs (read-only). No HJB/grid run.

Controlling identity (frozen fixture `transfer_income = 0.0`):

```text
mu_W = r_a_eff(a)*a + r_b*b + labor_income - chi(d,a) - consumption
```

Notation: `q = V_a/V_b - 1`, `T(q) = min(q+chi_0,0) + max(q-chi_0,0)`,
`d = a*T(q)/chi_1`, `chi(d,a) = chi_0|d| + 0.5 chi_1 d^2 / max(a,a_bar)`,
`consumption = V_b^(-1/2)`.

---

## M1. Provable source facts (no assumptions)

**M1.1** `r_b*b = 0.015*b = O(b)`, strictly positive, `-> +inf`. *(frozen r_b > 0)*

**M1.2** `0 <= r_a_eff(a)*a <= 0.27` for all `a in [0,10]`. *(compact support, taper
frozen; maximum at `a=10`: `0.03*10*(1-0.1) = 0.27`)*

**M1.3** `transfer_income = 0.0` (fixed scalar, region 0) is `O(1)` and
state-independent.

**M1.4** `V_b > 0` wherever the consumption FOC applies.

**M1.5 (no unconditional theorem)** There is **no accepted-authority proof** that
`mu_W < 0` for all large `b`: the negative terms `consumption + chi - labor_income`
are not characterized by accepted authority (Phase C: C4, C8 unidentified).

> Status: **PROVABLE** (M1.1-M1.4); **Outcome A not provable** (M1.5).

---

## M2. Conditional theorem (sufficient condition for inwardness)

**Statement (Conditional Inwardness):** Assume there exist `eta > 0` and `b0 > 0`
such that for all `b > b0`, uniformly over `a in [0,10]` and `z in {0.8,1.3}`,

```text
consumption - labor_income + chi(d,a) - transfer_income
    >= (r_b + eta)*b + r_a_eff(a)*a        (eventually)
```

(equivalently, the asymptotic consumption-wealth ratio is bounded below by `r_b`
with a positive margin, net of labor income and adjustment cost). Then

```text
mu_W <= -eta*b < 0   for all large b  (strict fixed-a liquid-tail inwardness).
```

**In value-derivative terms (with bounded transfer ratio `q = O(1)`):** the condition
is implied by `V_b = O(b^{-(2+delta)})` for some `delta > 0` (i.e. `V_b` decays
faster than `b^{-2}`), which gives `consumption = O(b^{1+delta/2})` growing faster
than linearly.

> Status: **PROVABLE AS A CONDITIONAL** — the premise is an explicit assumption that
> is **NOT established by current accepted authority** (it concerns the HJB solution
> tail, deferred to Route N-B). It is not a free theorem.

---

## M3. Conditional theorem (sufficient condition for outwardness)

**Statement (Conditional Outwardness / non-mean-reversion):** Assume there exist
`0 < p < 2` and constants such that `V_b ~ b^{-p}` in the tail (i.e. `V_b` decays
slower than `b^{-2}`), and `V_a/V_b = o(b)` (so `d = o(b)`, `chi = o(b)`). Then

```text
mu_W = r_b*b + o(b) + O(1) -> +infinity > 0   (fixed-a liquid tail is OUTWARD).
```

The minimal sufficient conditions are:
- `consumption = o(b)`, equivalently `V_b^{-1} = o(b^2)` (i.e. `V_b` decays slower
  than `b^{-2}`); and
- `d = o(b)` (equivalently `T(V_a/V_b - 1) = o(b)`, so the adjustment cost
  `chi = o(b)`), and
- `labor_income = o(b)` (holds for `V_b = o(b^5)`, essentially all plausible decay).

> Status: **PROVABLE AS A CONDITIONAL** — valid under explicit unproven assumptions
> about `V_b` and `V_a/V_b`.

---

## M4. Source-consistent asymptotic family (counterexample direction)

**Construction:** choose any positive, increasing (in `b`), concave value function
`V(b,a,z)` on the fixed `a`-support with

```text
V_b ~ K_z(a) * b^{-p},  0 < p < 2,   and   V_a/V_b = o(b)   (e.g. V_a/V_b = O(1)),
```

and evaluate the accepted formulas pointwise:
`c = V_b^(-1/2)`, `l = (V_b*0.85*z)^(1/5)`, `d = a*T(V_a/V_b-1)/chi_1`,
`chi = 0.1|d| + d^2/max(a,a_bar)`. Then:

- `c = o(b)`, `l/labor_income = o(b)`, `d = o(b)`, `chi = o(b)`; and
- `mu_W = r_b*b + o(b) + O(1) -> +infinity > 0`.

This family **satisfies every accepted pointwise control formula and the accepted
drift identity** (no accepted equation is violated), yet produces a non-inward
(`mu_W > 0`) fixed-`a` liquid tail.

**Crucial caveat:** this family is constructed at the **formula level** — it is not
shown to satisfy the full HJB Bellman equation (the accepted model includes the HJB
PDE, not only the pointwise FOCs). Whether an HJB-consistent solution with such a
slow `V_b` decay exists is **UNIDENTIFIED** (it is precisely the Route N-B question).
Therefore M4 is a **conditional / formula-level counterexample**, **not an
established model-level counterexample**, and does **not** justify Outcome C.

---

## M5. The knife-edge and the single decisive object

With `V_b ~ b^{-p}` and bounded transfer (`q = O(1)`):

| `p` | `consumption ~ b^{p/2}` | Leading-order `mu_W` | Fixed-`a` liquid tail |
|---|---|---|---|
| `0 < p < 2` | `o(b)` | `r_b*b + O(1)` | OUTWARD (`+inf`) |
| `p = 2` | `O(b)` | `(r_b - c/b)*b` | BORDERLINE (sign = sign(r_b - c/b)) |
| `p > 2` | `> O(b)` | `-inf` | INWARD |

The mean-reversion hypothesis corresponds to `p = 2` with `c/b > r_b` (consumption a
constant fraction of liquid wealth exceeding the liquid return). This is the natural
conjecture for a constant-return CRRA household, but it is a conjecture about the HJB
solution tail, **not accepted authority**. The decisive missing object is the tail
decay exponent `p` of `V_b` (equivalently the asymptotic `c/b`), and the tail behavior
of `V_a/V_b`.

---

## M6. Uniformity and the two-asset caveat

- **Uniformity over `(a,z)`:** `a` is compact and `z` is finite; any pointwise rate
  established with uniform constants extends uniformly. The conditional statements
  M2/M3 are stated uniformly. This is a compactness remark, not a substitute for the
  missing rate.
- **Fixed-`a` vs two-asset theorem:** even a positive M2-type result establishes only
  a fixed-`a` liquid-tail statement. A full two-asset infinite-domain theorem requires
  characterizing both coordinates to infinity and is strictly outside DLH-5N.

---

## Matrix summary

| Row | Statement | Status |
|---|---|---|
| M1 | `r_b*b = O(b)>0`, `r_a_eff*a = O(1)>=0`, `transfer_income = O(1)`; **no unconditional inwardness theorem** | PROVABLE |
| M2 | `mu_W < 0` eventually under explicit fast-`V_b`-decay condition | CONDITIONAL THEOREM (premise not established) |
| M3 | `mu_W > 0` eventually under explicit slow-`V_b`-decay condition | CONDITIONAL THEOREM (premise not established) |
| M4 | formula-level source-consistent family with `mu_W -> +inf` | CONDITIONAL COUNTEREXAMPLE (not HJB-verified; Outcome C not justified) |
| M5 | knife-edge exponent `p = 2`, sign = `sign(r_b - c/b)` | UNRESOLVED (decisive missing object) |
| M6 | uniformity over compact `(a,z)`; fixed-`a` only, not two-asset | META-STATEMENT |

**Conclusion:** the sign of `mu_W` in the fixed-`a` liquid tail is **conditional** on
the (unestablished) tail decay of `V_b` and the tail behavior of `V_a/V_b`; accepted
authority does not determine it. This selects **Outcome B**.
