# DLH-5E — Forbidden-Operation / Scope Check (Issue #28)

DSH did NOT perform any of the following during DLH-5E execution:

| Forbidden operation | Status |
|---|---|
| Modify `matlab_faithful_two_asset_ha.py` | NOT performed (immutable) |
| Modify any existing HJB/local-policy code | NOT performed |
| Modify regional fixed-point code/config | NOT performed (read-only reference) |
| Integrate the candidate into production household routing | NOT performed (candidate only) |
| Silently clip a boundary-policy violation into acceptance | NOT performed (fail-closed blocker) |
| Auto-expand grids | NOT performed |
| Retune parameters/prices/tolerances | NOT performed |
| Regularization / jitter / pseudoinverse | NOT performed |
| Change contamination constant to seek PASS | NOT performed (`c=0.007` frozen) |
| Auto-select a replacement production pin | NOT performed |
| Run two-region outer iteration | NOT performed |
| OD / learned W^L / larger regions / nominal HANK / calibration / policy / welfare / Results | NOT performed |
| `git add .` / `git add -A` | NOT performed (explicit staging only) |
| Self-accept / merge / close Issue / PR / successor Issue | NOT performed |

Terminal classification: `BLOCKED_DLH_5E_BOUNDARY_POLICY_VIOLATION__OWNER_BOUNDARY_POLICY_DECISION_REQUIRED`
