# R5-1 Legacy Migration Status — Historical Reference

Provenance commit: `48bf56c03a28a3256c601f1299c275edeb058173`.

Historical verdict: `DISSERTATION_CH5_R5_LEGACY_EQUATION_AND_DEPENDENCY_MIGRATION_INVENTORY_PASS`

Historical classification: `R5_LEGACY_EQUATIONS_DEPENDENCIES_AND_MECHANISMS_MAPPED_READY_FOR_PYTHON_REPOSITORY_AND_TESTABLE_SCAFFOLD_GATE`

Evidence: `D1_LEGACY_SOURCE_AND_SPECIFICATION_MAPPING_NO_MODEL_OR_OUTPUT_AUTHORITY`.

Historical bounded read summary:

- 32 `.m` sources, 104,770 bytes, read as text/metadata under the original read-only root.
- 10 core equation rows, 9 variable rows, 11 static dependency edges.
- Decisions: RETAIN 3; REDESIGN 14; DROP 3; UNRESOLVED 0.
- Household HJB/KFE and production meaning were retained economically.
- `GovInv`, `rah/inter_prv_ratio`, nominal/fiscal closure, fixed-point diagnostics, shock and transition were marked for redesign.
- Old outputs were explicitly not authoritative.

Especially useful historical design decision:

`inter_prv_ratio` was per-capita-capital based and `rah` blended own/outside returns, but orientation, diagonal, normalization and separation from shock loading were not explicit. The R5 planning route therefore proposed replacing them with an explicit exposure matrix `W` with documented orientation and accounting tests. The new Deep Learning + HANK project may reconsider this idea, but it is **not automatically binding**.
