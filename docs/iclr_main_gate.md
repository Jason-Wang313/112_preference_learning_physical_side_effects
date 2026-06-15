# ICLR Main Gate

Paper: 112 preference_learning_physical_side_effects

Previous v3 decision: KILL_ARCHIVE

Gate verdict after v4.1 rebuild: STRONG_REVISE

Evidence digest: local physical side-effect preference benchmark, 5 tasks, 7 regimes, 5 splits, 9 methods, 7 paired seeds, 84 episodes per group, 7,350 task/regime/seed stress rows, and 8 failure cases.

Gate outcomes:
- Success margin over strongest non-oracle baseline: PASS (`0.066`).
- Diagnostic improvement: PASS (`+0.132` side-effect recall).
- Damage/false-alarm/query-cost non-regression: PASS.
- Pairwise seeds: PASS (7/7 wins).
- Ablation margin: PASS (`0.024`).
- Expanded stress coverage: PASS (`7,350` detailed rows).
- Failure-case coverage: PASS (`8` rows).
- Numeric integrity: PASS (no NaN or infinite values).

ICLR main ready: NO. Real human labels and robot validation are still required.
