# DLH-5V-F — Scoring, Conservative-Row and Same-Process One-Q Contract (Issue #54)

Companion report 4 of 5. Records the exact candidate-control rate contracts for the
**closable** deferred classes, the discrete-`H_h` scoring order, the conservative-row
construction, and the one-backward-`Q` same-process law, and states the precise
consequence of the obstruction for the unclosable classes.

---

## 1. Closable deferred classes and their exact rate contracts

Notation (accepted DLH-5V-D/E sector formulas, unchanged): for an admissible
candidate control with drift `(mu_a, mu_b)` at a state whose available transitions
are as shown, the nonnegative rates are:

```text
reverse sector   (j = 0, a=0 x W):  transitions (w_RT, w_down)
    q_RT  = 19*mu_a/70              >= 0  (a=0 face: mu_a >= 0)
    q_down = 19*(-mu_W)/7           >= 0  (W face: mu_W <= 0)
    cone{w_RT, w_down} = { mu_a >= 0, mu_b <= 0, mu_W <= 0 } = admissible at j = 0

T_realloc sector (b=b_min W-cell (19,0)):  transitions (w_left, w_T)
    q_in = 19*(-mu_W)/10            >= 0
    q_T  = 19*mu_b/70               >= 0  (b=b_min face: mu_b >= 0)
    cone{w_left, w_T} = { mu_a <= 0, mu_b >= 0, mu_W <= 0 } = admissible at (19,0)

a=a_max face (j = 19):  transitions (w_left, w_down, w_T)
    mu_b >= 0:  q_in = 19*(-mu_W)/10,  q_T = 19*mu_b/70        (T_realloc branch)
    mu_b <  0:  q_left = 19*(-mu_a)/10, q_down = 19*(-mu_b)/7  (R_deplete branch)
    cone{w_left, w_down, w_T} = { mu_a <= 0, mu_W <= 0 } = admissible at j = 19
```

At each closable class the continuous admissible cone (joint active-face KKT) equals
the cone of the accepted transitions (cone-equality verified in the audit report §7):
the economic-face multiplier cuts off exactly the drift region the missing wide
stencil would serve. All rates are candidate-specific, nonnegative, and exact.

**Seam consistency.** The formulas above are identical to the regular-region formulas
(accepted DLH-5V-D/E): `j=0` uses the same reverse-sector rates as regular `j=7`;
`j=19` uses the same T_realloc/deplete rates as regular `j=12`; the b-min face cell
uses the same T_realloc rates as any regular b-min-adjacent state. No seam
discontinuity exists on the closable side; the seam discontinuity is entirely
concentrated at the unclosable classes (Section 3).

## 2. Discrete-`H_h` scoring and one global argmax (accepted semantics)

At every state, for **each candidate control**:

1. check continuous admissibility on the actually active economic faces (joint KKT);
2. compute candidate-specific represented nonnegative rates (Section 1 formulas for
   closable classes; Section 3 for the status at unclosable classes);
3. score the candidate's discrete `H_h` term using those rates;
4. only **after** all candidates are scored, take ONE global statewise argmax;
5. the selected control's rates form the row of the **one** conservative backward
   generator `Q`.

The future KFE consumes exactly `Q^T` (`p_dot = Q^T p`), with `Q V` the
backward/HJB transition term and `p = M g` (accepted same-process law). Stationary
execution remains outside this Issue.

## 3. Status at the unclosable classes (consequence of the obstruction)

At the obstruction classes (audit report §4–§5) there is **no** coherent
candidate-specific nonnegative represented rate/scoring contract: the continuously
admissible candidate whose drift is the exact W-tangent sliding ray of the missing
orientation has no representation in `C_rep(s)`. Consequences:

- the discrete-`H_h` score of that candidate is **undefined** (no rates exist);
- the global statewise argmax is therefore **not well-defined** at those states;
- the one-backward-`Q` law cannot be completed on the deferred complement.

The Builder does **not** repair this here: no clipping, no omitted destination with
retained diagonal escape, no ghost/interpolation/virtual state, no inward-normal
first-moment injection, no KFE-only boundary repair, no second boundary process.
This is the content of the obstruction and the reason an Owner route decision is
required (Outcome C terminal).

## 4. Conservative-row construction (closable classes)

For a closable row with rates `q_1, ..., q_m` on actual destinations
`d_1, ..., d_m` and `q_0 = sum_k q_k`:

```text
Q[s, s]     = -q_0
Q[s, d_k]   = +q_k
row sum     = 0  (conservative by construction)
```

Every off-diagonal entry corresponds to an actual represented native-grid
destination; no diagonal-escape-with-omitted-destination pattern is used; rows are
constructed from actual outgoing rates only. This is the same construction as the
accepted regular region.

## 5. One backward Q (design-level)

Exactly one backward generator `Q` is selected at the design level: its rows are the
rows of Section 4 on the closable states and the accepted regular-region rows
elsewhere. The unclosable states block the completion of `Q` (Section 3) — hence the
obstruction. No alternative `Q`, no KFE-side correction, no second process.

## 6. Interaction with the joint-boundary KKT

At joint intersections (`a=0 x W`, `a=a_max x W`, `b=b_min x W`) the rates of
Section 1 are derived under the **joint** KKT: each multiplier is nonnegative,
complementarity holds, and the effective-gradient convention is the accepted
`L = H - sum lambda_j g_j` form (lower faces `V + lambda`, upper/W faces
`V - lambda`). The cone equalities of Section 1 are exactly the joint-cone statements
of the accepted DLH-5T boundary laws, so the endpoint contracts inherit the joint
law without modification on the closable side.

## 7. Interpretation ceiling

The contracts in this report are design-level. They do not establish implemented
boundary-HJB correctness, global discrete-HJB correctness, numerical `W_max`
adequacy, SCC / closed recurrent-class structure, stationary existence/uniqueness,
stationary KFE authorization, or any aggregates/GE/policy/Results claim.
