# DLH-3D-R1A — Evidence Manifest (files inspected, read-only)

- Date: 2026-08-20
- Authority: GitHub Issue #14 (OPEN); canonical spec `tasks/DLH_3B_R1_HA_ALGORITHM_PARITY_AUDIT_2026_08_20.md`
- Principle: every listed path was inspected read-only; no file was modified; legacy source roots untouched.

## 1. Repository governance / authority (fresh origin/main `d727dda28738bbdad126c784f0366f0e21be3e1d`)

- `project_rules/PROJECT_RULE_INDEX_CURRENT.md` + all `PROJECT_RULE_*_CURRENT.md`
- `tasks/TASK_INDEX_CURRENT.md` (still `ACTIVE_GITHUB_ISSUE_13__DLH_3D_MINIMAL_HANK_MONETARY_GE` — Task-Index pointer lag documented as an observation)
- `tasks/DLH_3B_R1_HA_ALGORITHM_PARITY_AUDIT_2026_08_20.md` (canonical execution specification; activated by Issue #14 comment `5355380189`)
- `docs/governance/DLH_STARTUP_SNAPSHOT_CURRENT.md`, `docs/roadmaps/DLH_MASTER_ROADMAP_INITIAL_2026_08_19.md`
- GitHub Issue #14 body + comments (fresh via `gh`); Issue #13 body/comments (context)

## 2. Accepted DLH-3A contracts (origin/main)

- `docs/specifications/DLH_3_MINIMAL_GENUINE_HANK_ARCHITECTURE_2026_08_19.md`
- `docs/specifications/DLH_3_ASSET_FISCAL_AND_NOMINAL_SEMANTICS_CONTRACT_2026_08_19.md`
- `docs/specifications/DLH_3_STEADY_STATE_AND_DYNAMIC_EQUATION_CONTRACT_2026_08_19.md`
- `docs/specifications/DLH_3_VALIDATION_LIMITING_CASE_AND_GRID_CONTRACT_2026_08_19.md`

## 3. Current Python source (audited)

| Path | Role |
|---|---|
| `src/deep_learning_hank/solvers/hank_household_steady_state.py` | one-asset HJB + endogenous static labor + generator |
| `src/deep_learning_hank/solvers/hank_steady_state.py` | nested brentq equilibrium (r, N) |
| `src/deep_learning_hank/solvers/distribution_kfe.py` | stationary KFE `G^T g = 0` |
| `src/deep_learning_hank/solvers/household_hjb.py` | Tier-0 one-asset HJB (reference family) |
| `src/deep_learning_hank/solvers/steady_state.py` | Tier-0 equilibrium (K root) |
| `src/deep_learning_hank/solvers/hank_household_transition.py` | DLH-3C backward implicit HJB |
| `src/deep_learning_hank/solvers/hank_kfe_transition.py` | DLH-3C forward implicit KFE |
| `src/deep_learning_hank/solvers/hank_nkpc_transition.py` | DLH-3D backward NKPC + Taylor/Fisher |
| `src/deep_learning_hank/solvers/hank_ge_transition.py` | DLH-3D krylov path root + residuals |
| `src/deep_learning_hank/diagnostics/hank_ge_transition.py` | DLH-3D gates |
| `src/deep_learning_hank/diagnostics/hank_transition.py` | DLH-3C gates + `BaselineInfo`/`load_baseline` |
| `src/deep_learning_hank/economics/{preferences,grids,firm,fiscal,hank_firm,hank_fiscal,hank_nominal}.py` | economics building blocks |
| `src/deep_learning_hank/{config,hank_config,hank_transition_config,hank_ge_config}.py` | config classes |
| `configs/dlh_3b_hank_steady_state_validation.toml` | 3B fixture (SHA-256 `82AB4A02F9D08FBBAED1349BC027FACE5361B1AB24C710C4CEA6958481CD5FC1`) |
| `configs/dlh_3c_hank_transition_validation.toml` | 3C fixture (SHA-256 `C7AA76DF3758F46FCBA827872FC0FD0078EDD5309CCFAD04E32C42F5CB4D39A2`) |
| `configs/dlh_3d_hank_monetary_ge_validation.toml` | 3D fixture (SHA-256 `D19F555C29D25604EC276D7036161A070510D4DC5BC4F4F51476BA3981A207D1`) |

## 4. Accepted / fail-closed evidence reports (inspected read-only)

- `reports/dlh_3b_hank_steady_state_2026_08_20/DLH_3B_EXECUTION_REPORT.md` (+ `DLH_3B_DIAGNOSTICS.csv`)
- `reports/dlh_3c_hank_transition_2026_08_20/` (accepted transition evidence)
- `reports/dlh_3d_hank_monetary_ge_2026_08_20/DLH_3D_EXECUTION_REPORT.md`, `DLH_3D_RESIDUAL_AMPLITUDE_SUMMARY.csv`, `DLH_3D_REPRODUCIBILITY_SUMMARY.csv`, `DLH_3D_PATH_DIAGNOSTICS.csv`, `DLH_3D_FORBIDDEN_OPERATION_CHECK.md` (fail-closed candidate, commit `9f767d1e12354b7170cf4b79a2db1df7028395ea`)

## 5. Legacy Matlab reference (read-only; hashes recorded; nothing modified)

Root: `D:\MatlabProgram\2023年12月2日 多省份神经网络HANK`

| Path (relative to root) | SHA-256 |
|---|---|
| `HANK_2ASSETS_HJB.m` | `049136B769560040BC678F828F5D3EC5338DDCAA2090D6BED4E40732F56C3EAE` |
| `HANK3_FOC.m` | `772B7B7BBF528DFDD246BD152B3E3026035012FE50F30DA808C1EE18C0F8463D` |
| `HANK3_cost.m` | `3504A74BB2DB9FBEE3B292AB68D758954248643D6A5178E42554E0D4794F9A3C` |
| `HANK_firm.m` | `EE02C15414ADF9F99AADE04F1F22E64FA7094C8AB77753B6130BC4BFA6CE7BD5` |
| `lab_solve2.m` | `74FD6AE8D76AB50A571831FAB95464AE4FCE919F3E70B660E5ABF6B9C5662C20` |
| `multi_prov_HANK_12sts.m` | `3C44449CFD4047B5C9E17E540AFEA2F50B4251150F8F74AB8CCEED26E15DEC97` |
| `mpHANK_equilibrium_2000.m` | `26EA44552DA33919F8CCD777C084E15ECA0EA9575FEE80A07F9E0056F3F97DE5` |
| `mpHANK_shock_2000.m` | `5909A972854B56E3E86F8EDA127A2A8AEAED236BFE1E7AA8C04A26DB750E9173` |
| `main.m` | `5C49CEAEDA9B43ED615E5DD376498D45F0E01D9A2F469C0FBB617C02110D5E12` |
| `12年稳态值.xlsx` (exported steady-state GDP table, province × years) | `FF65B8A0BC27CF9A382C5F00FE1E377575517EE9B5A568976452BFFEAA83CE4B` |

Thesis PDF (located for terminology alignment; **text extraction not performed** — no PDF text library available in the environment and the Matlab source already provides the terminology):
`D:\Zotero-Analytical-Workflow\inputs\urhank_rejected_manuscript\URHANK.pdf` SHA-256 `FA026EF643D70E385073B269B62AFBEF92D5F08C4AD2D24F1D289D2F489F4D29` (2,610,109 bytes).

## 6. Verification of legacy integrity

- Legacy source-root read-only policy honored: only `Get-Content`/`Get-FileHash`/directory listing were used; no write, no execution, no MATLAB run (task file §4 forbids running legacy MATLAB unless separately authorized).
- All SHA-256 hashes above were recorded **before** this audit's outputs were created; nothing in the legacy roots was touched.

## 7. Limitations / unresolved questions

1. **Static audit**: no numerical execution was performed in this task (Issue #14 forbids DLH-3D reruns; the audit is source/evidence-based). All numerical statements cite accepted/fail-closed recorded evidence.
2. **Thesis PDF**: identified and hashed, but text extraction was not performed (no PDF tooling); terminology alignment was done from the Matlab source and the accepted DLH-3 contracts.
3. **Task Index pointer lag**: `tasks/TASK_INDEX_CURRENT.md` on fresh `origin/main` still points to Issue #13, even though Issue #14's authoritative comment activates this audit. Recorded as an observation for the reviewer; the Issue comment itself is the activation authority.
4. **Unresolved scientific question**: whether the (un-audited here) two-asset Matlab transition/shock engine (`mpHANK_shock_2000.m`) shares the Python dynamic KFE timing is not established — the audited Matlab steady-state file is the authorized reference; the shock file is listed for completeness only.
