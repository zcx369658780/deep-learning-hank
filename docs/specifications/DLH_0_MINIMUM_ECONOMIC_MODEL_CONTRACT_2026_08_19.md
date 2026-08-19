# DLH-0 — Minimum Economic Model Contract (Candidate)

- Date: 2026-08-19
- Author: DSH (bounded Builder)
- Status: CANDIDATE for Owner/ChatGPT decision — specification only, no implementation.

> Every item is either DECIDED (baseline) or CAVEATED (explicitly deferred/undecided). Decisions here are candidate specifications, not frozen authority. No legacy calibration, no legacy outputs, no simulation.

## C. Minimum HANK economic structure — baseline contract

### C.1 Household asset dimensionality
- **DECIDED (baseline): one-liquid-asset** continuous-time household block (single productive asset `a`, Aiyagari-style capital closure).
- CAVEAT: the historical Matlab model was **two-asset** (liquid `b` + illiquid/productive `ah`). Two-asset is retained as the **first documented extension** (REUSE_CONCEPT from historical evidence), not the baseline, because the baseline must be the smallest model that supports HJB + KFE + clearing + a neural approximation target with hard diagnostics. Owner may override to two-asset-first.

### C.2 Idiosyncratic state(s)
- **DECIDED (baseline):** labor productivity `z` as a finite-state Markov chain (candidate 2–3 states, transition matrix to be frozen at DLH-3). Asset `a` is the continuous idiosyncratic state on a bounded grid `[a_min, a_max]`.
- CAVEAT: number of `z` states and transition parametrization are freeze items for DLH-3 (evidence: historical `la_mat`/`Bswitch` semantics are reference only).

### C.3 Household controls
- **DECIDED (baseline):** consumption `c` and saving `da` (continuous-time drift); portfolio choice excluded (single asset).
- CAVEAT: if the two-asset extension is adopted, illiquid-asset adjustment (HANK-style infrequent/flow adjustment) becomes an additional control — deferred.

### C.4 Utility / labor-supply role
- **DECIDED (baseline):** CRRA consumption utility `u(c) = c^(1-gamma)/(1-gamma)`; **inelastic labor supply** (exogenous, normalized), so no labor FOC in the household block.
- CAVEAT: elastic labor with separable disutility is a documented extension (feeds `W_labor`); historical labor-allocation mechanism (`Lt_seperate`) is reference only.

### C.5 Borrowing / asset boundaries
- **DECIDED (baseline):** exogenous borrowing limit `a >= a_bar` with candidate `a_bar <= 0`; boundary behavior of the HJB scheme (state-dependent vs natural limit) must be explicitly specified at implementation.
- CAVEAT: endogenous/natural borrowing limit and its interaction with the neural surrogate are DLH-3 freeze items; boundary feasibility is a mandatory diagnostic (mass at the bound, no violation).

### C.6 Stationary distribution representation
- **DECIDED (baseline):** Kolmogorov-forward equation (KFE) `A' g = 0` on the (a, z) state space, normalized `mass = 1`; non-negativity and moment checks mandatory.

### C.7 Firm production block
- **DECIDED (baseline):** representative competitive firm per region, Cobb-Douglas `Y = A K^alpha L^(1-alpha)`; capital rental rate `r`, wage `w`; investment/savings feed the capital stock from household asset holdings.
- CAVEAT: historical `HANK_firm.m` block (NKPC-style marginal cost, price-adjustment cost, profits/taxes/dividends) is reference input only; nominal rigidity explicitly deferred (C.8).

### C.8 Nominal rigidity
- **DECIDED (baseline): DEFER** — baseline is a real model; no NKPC, no price/wage stickiness in the first baseline.
- CAVEAT: nominal rigidity is a candidate extension (minimal NKPC later); monetary-policy experiments are NOT part of DLH-0–DLH-2 scope.

### C.9 Fiscal block
- **DECIDED (baseline): minimal** — balanced-budget lump-sum transfer/govt spending, no debt dynamics, no distortionary taxation in the baseline.
- CAVEAT: richer fiscal closure (historical `fiscal` REDESIGN item) deferred; accounting identity of the fiscal block must be explicit when added.

### C.10 Market-clearing identities
- **DECIDED (baseline):** goods market (aggregate supply = consumption + investment + govt), capital market (household aggregate asset = aggregate capital), labor market (aggregate inelastic labor = firm labor demand), asset-market clearing identity. Each must have a residual diagnostic.
- CAVEAT: regional market clearing (asset flows, trade balance, labor-market balance) enters only with the regional extension (D).

### C.11 Steady-state concept
- **DECIDED:** stationary equilibrium = value function solves HJB; distribution stationary under KFE; aggregates consistent; markets clear; fixed point of the outer loop converges with documented tolerance.

### C.12 Transition concept
- **DECIDED:** conditional perfect-foresight transition path following a one-innovation shock from the stationary equilibrium; terminal/transversality conditions explicit.
- CAVEAT: stochastic-realization simulation and full distributional dynamics are deferred; historical R5 conditional-IRF principle is a design reference only, not binding.

## D. Regional / spatial dimension (spec-level only)

### D.1 First scientific baseline
- **DECIDED: single-region HANK first.** Small multi-region (2–3 regions) is the documented second stage; full province dimension only after validation (DLH-7).

### D.2 Candidate link definitions (spec-level semantics only — no empirical construction in DLH-0)

| Link | Intended role (candidate) | Row/column semantics | Diagonal | Normalization | Accounting role |
|---|---|---|---|---|---|
| `W_asset` | cross-region capital / asset-return exposure | row = exposed region `i`, column = capital-origin region `j` | own-region share (allowed nonzero) | candidate: rows sum to 1 (portfolio/exposure weights) | regional asset-market clearing; returns consistent across regions |
| `W_labor` | labor-demand / labor-market linkage | row = labor-importing region `i`, column = labor-supplying region `j` | own-region labor share | candidate: rows sum to 1 | regional labor-market balance (only if elastic labor adopted) |
| `W_trade` | goods / demand linkage | row = demand-origin region `i`, column = supply region `j` | own-region demand share | candidate: rows sum to 1 | regional goods-market clearing / trade balance |
| `S` (shock exposure) | exposure of region `i` to aggregate or common shocks (NOT inter-region endogenous links) | row = region `i`, column = shock index | own shock loading | candidate: normalize to unit variance of the common shock | separates shock exposure from endogenous spatial links |

- CAVEAT: orientation (row/column) of every retained matrix must be re-confirmed at DLH-3; diagonal, normalization, non-negativity/sign restrictions, exogenous-vs-endogenous status and separation from shock loading are explicit freeze items. The historical `rah`/`inter_prv_ratio` mechanism is reference only and NOT automatically binding.
- For the first baseline none of `W_asset/W_labor/W_trade` is active (single region); the extension activates at most one link first (recommended: `W_asset`), others deferred.

## E. Shock / experiment concept (first)

### E.1 First working concept
- **DECIDED:** aggregate log-TFP `AR(1)`, one-innovation **conditional (perfect-foresight) transition path** from the stationary equilibrium.

### E.2 Freeze contract for future implementation (DLH-3, not calibrated here)
- variable: log aggregate TFP (candidate `z_t` or `A_t`; must not collide with idiosyncratic `z` naming — freeze exact symbol);
- frequency: candidate **annual** (consistent with historical national-accounts flavor; quarterly is an alternative freeze choice);
- mean: log mean normalized to 0 (level mean 1);
- persistence `rho`: candidate freeze value `0.9` (range tests later);
- innovation: `eps_t ~ N(0,1)` i.i.d.; conditional path = single realized innovation at `t=0`, perfect foresight thereafter; `sigma` candidate freeze value `0.01` (std of TFP innovation);
- exposure semantics: single-region = scalar; regional extension uses exposure matrix `S` (D.2) — freeze `S` semantics and normalization at DLH-3;
- interpretation: **conditional-path vs stochastic-realization** must be explicit in every output; stochastic-realization simulation is deferred.

### E.3 Second / third concepts (documented, not active)
- common shock with heterogeneous regional exposure (activates `S`);
- region-specific shock (deferred).
- No shock simulation in DLH-0.

## G.0 Contract discipline notes
- Every freeze item above is a *candidate*; freezing happens at DLH-3 after Owner/ChatGPT decision and independent review of DLH-0.
- No legacy Matlab equation, parameter, or output inherits authority; every mechanism retained is re-defined and re-tested in this project.
