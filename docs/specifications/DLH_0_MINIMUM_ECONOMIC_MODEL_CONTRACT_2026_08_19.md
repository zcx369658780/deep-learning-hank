# DLH-0R1 — Minimum Economic Model Contract — NSR-HANK (Candidate)

- Date: 2026-08-19 (R1 revision)
- Author: DSH (bounded Builder)
- Status: CANDIDATE for Owner/ChatGPT decision — specification only, no implementation.

> R1 correction basis: Issue #2 authoritative revision comment + `DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`. Items are DECIDED (baseline) or CAVEATED (deferred/undecided). No legacy calibration, no legacy outputs, no simulation.

## C. Provincial structural hard modules (unchanged principle, now first-class)

The following remain **structural hard economic modules** — neural networks do not replace or re-derive them:

- household optimization; HJB; KFE / stationary distribution; household budget constraint;
- firm production / FOC;
- market clearing; accounting identities;
- minimal genuine-HANK nominal block (only at the DLH-3 layer);
- fiscal accounting.

Neural role = learn **interregional connection mechanisms** (flow networks), nothing inside the province.

## C.1 Benchmark vs genuine HANK tiering (R1 correction)

- **Tier 0 — one-region real one-asset HA/Aiyagari computational benchmark** (DLH-2): transparent, deterministic, diagnostics. **It is a computational benchmark, NOT the substantive/genuine HANK model.**
- **Tier 1 — minimal genuine single-region HANK** (DLH-3): same household/distribution kernel + minimal New Keynesian nominal layer (nominal rigidity, monetary/fiscal closure). Separate structural layer; required before learned multi-region HANK claims.
- **Tier 2 — small multi-region NSR-HANK** (DLH-4→6): hand-specified `W^L` 2-region prototype -> learned `W^L` -> 3–5 region equilibrium integration.

## C.2 Household block (baseline contract)

- **DECIDED (Tier-0 benchmark):** one liquid asset `a` on grid; idiosyncratic productivity `z` (finite-state Markov); controls consumption `c` and saving; CRRA; **inelastic labor supply** (exogenous, normalized).
- **DECIDED (regional model):** household **home-region identity is fixed**; **labor services may be allocated across provinces** through the structural two-stage flow model (roadmap §3.1):
  - Stage 1: share of home-region labor services leaving the province: `m^L_i,t = sigma(g_L(Z_i,t ; phi_L))`.
  - Stage 2: destination allocation: `W^L_ij,t = exp(s^L_ij,t) / sum_{j != i} exp(s^L_ij,t)`, with `s^L_ij,t = f_L(x_ij,t ; theta_L)`.
  - Flow: `F^L_ij,t = L^home_i,t * m^L_i,t * W^L_ij,t`.
- CAVEAT: permanent migration, hukou change, housing choice, and household-distribution transfer between provinces are **deferred** (not in first generation).
- Whether the substantive (Tier-1/Tier-2) household block remains one-asset/inelastic is **NOT frozen**; depends on the paper question and DLH-1A literature evidence.

## C.3 Borrowing / asset boundaries

- **DECIDED (benchmark):** exogenous borrowing limit `a >= a_bar` (candidate `a_bar <= 0`), explicit boundary treatment at implementation; boundary feasibility mandatory (mass at bound, no violation).

## C.4 Stationary distribution

- **DECIDED:** KFE `A' g = 0` per province, `mass = 1`, non-negativity, moment checks.

## C.5 Firm block

- **DECIDED:** representative competitive firm per province, Cobb-Douglas `Y = A K^alpha L^(1-alpha)`; capital rental, wage; province-local production/FOC structural.

## C.6 Nominal rigidity

- **DECIDED:** deferred from Tier-0 benchmark; enters at Tier-1 minimal genuine HANK (DLH-3) as the nominal layer.

## C.7 Fiscal block — central-government allocation layer (R1 correction)

- **DECIDED:** fiscal transfers modeled as a separate central-government allocation layer:
  `Province taxes/revenue -> Central Government -> Province transfers`.
- Initial treatment: observed transfers as exogenous/data-constraint objects; whether `W^G` becomes learned is decided only after labor and capital networks are stable.
- **Explicitly NOT folded into `W^K`.**

## C.8 Market clearing / conservation (regional)

- Province-local: goods, capital, labor markets clear; accounting identities.
- Regional: **labor conservation** (`sum_j F^L_ij,t = L^home_i,t * m^L_i,t`; province `j` receives `sum_i F^L_ij,t`), capital conservation (once `W^K` exists), national identities; fiscal accounting.
- Residual diagnostics for every identity.

## C.9 Steady state / yearly equilibrium

- **DECIDED:** stationary equilibrium per province; national equilibrium = fixed point `X*_t = T(X*_t ; theta, Z_t)`.
- **DECIDED (cross-year contract):** each year `t` solves a **separate conditional equilibrium** `X*_t`; learned structural parameters `theta` are **shared across years**; `W^L_t` varies with year-specific observables. Not a full dynamic transition system (2010→2011→2012 not modeled as one dynamic system in the first generation).

## C.10 Transition concept

- CAVEAT: transition/experiment concept remains open at Tier-1/Tier-2 until the nominal/HANK layer and paper question are decided; benchmark uses one-innovation conditional path. No simulation in DLH-0R1.

## D. Regional / spatial dimension (R1 corrected — `W^L` first)

### D.1 Sequence (roadmap §10)
hand-specified `W^L` in a 2-region prototype -> learned `W^L` -> 3–5 region equilibrium integration -> learned `W^K` -> fiscal module -> full 31 provinces (year-by-year equilibrium panel).

### D.2 Link semantics (spec level only; no empirical construction)

| Link | Role | Row/column semantics | Diagonal | Normalization | Accounting role |
|---|---|---|---|---|---|
| `W^L` (first learned) | interregional labor-flow allocation | row = home region `i`, column = destination region `j` (`j != i`) | none (home retained via `1 - m^L_i,t`) | row-normalized softmax over `j != i`; plus `m^L_i,t in (0,1)` | labor conservation: outflows = `L^home_i,t * m^L_i,t`; inflows to `j` = `sum_i F^L_ij,t` |
| `W^K` (later) | interregional capital-flow allocation | to be frozen at DLH-7 (row = source, column = destination convention) | own-region share allowed | transparent rules first (distance, return gap, gravity/exposure), learned later | capital conservation; national capital clearing |
| `W^G` (central fiscal) | central-government transfer allocation | province revenue -> central -> province transfers | n/a | observed transfers as data constraints initially | fiscal accounting; separation from `W^K` mandatory |
| `S` (shock exposure) | region `i` exposure to common/aggregate shocks | row = region, column = shock index | own loading | normalize to unit variance of common shock | separates shock exposure from endogenous links |

- CAVEAT: row/column orientation, diagonal, normalization, non-negativity/sign restrictions, exogenous-vs-endogenous status, and separation from shock loading are explicit freeze items at the respective DLH stage. Historical `rah`/`inter_prv_ratio` is reference only, not binding.

## E. Shock / experiment concept

### E.1 Benchmark (Tier 0)
- **DECIDED:** aggregate log-TFP AR(1) as the benchmark shock; freeze contract at DLH-3: variable, frequency (candidate annual), mean (log mean 0), `rho` (candidate 0.9), innovation normalization (`eps ~ N(0,1)`), `sigma` (candidate 0.01), exposure semantics, conditional-path vs stochastic-realization interpretation explicit in every output.

### E.2 Substantive experiments (Tier 1/2)
- CAVEAT: genuine-HANK shock and regional experiments (common shock with regional exposure via `S`, region-specific shocks) remain open until the nominal/HANK layer and paper question are decided. No shock simulation in DLH-0R1.

## G.0 Learning / identification contract (R1 mandatory)

A. **Flow-supervised pretraining:** `theta_L = argmin L_flow` on `(i,j,t,F^L_ij,t)`; report flow prediction, origin-share error, destination-share error, hold-out year/pair performance, feature sensitivity, interpretable partial effects.
B. **GE embedding:** embed `W^L(theta_hat_L)` in the regional HA/HANK system; solve `X*_t(theta_hat_L)`; check province output/labor/capital/wage/return/distribution/national clearing.
C. **Bounded equilibrium fine-tuning** (only after A/B pass): `L = lambda_F*L_flow + lambda_M*L_macro + lambda_E*L_equilibrium + lambda_R*R(theta)`.

**Macro aggregates `Y/K/L` must NOT be the sole identifiers of `W^L`.** Flow-data discipline is preserved so a better GDP fit cannot freely destroy the observed migration network.

## G.1 Contract discipline notes
- Every freeze item is a candidate; freezing happens at the respective DLH stage after review.
- No legacy Matlab equation, parameter, or output inherits authority; every retained mechanism is re-defined and re-tested in this project.
- Existing single-province Python HJB/firm code: candidate reusable kernel, **subject to DLH-1B audit** (provenance, equation/closure, I/O contract, deterministic fixture, HJB residual, KFE mass/non-negativity, firm identity, removal of legacy global state) before any migration.
