# Submission Version Log

## v3

Decision: KILL_ARCHIVE

Reason: synthetic/template evidence and no real or high-fidelity validation.

## v4

Decision: STRONG_REVISE

Changes:
- Added physical side-effect preference benchmark.
- Added success-only, generic preference, RLHF, uncertainty-query, constraint, failure-shield, and side-effect classifier baselines.
- Added paired-seed success tests.
- Added side-effect, damage, false-alarm, and query-cost gates.
- Added ablations, stress sweep, failure cases, figures, and generated tables.
- Rewrote manuscript and docs around a narrow physical side-effect preference claim.

Remaining blocker: no real human-label or robot validation.

## v4.1

Decision: STRONG_REVISE

Changes:
- Reran the experiment with low-RAM thread caps.
- Expanded `stress_sweep_seed_metrics.csv` from seed-level aggregation to 7,350 task/regime/seed rows.
- Expanded `failure_cases.csv` from 4 to 8 concrete boundaries.
- Re-audited row counts, finite numerics, strongest-baseline comparison, paired seeds, ablation margin, stress sweep, and artifact rules.
- Preserved the honest non-ready decision because real human-label and robot/high-fidelity evidence are still absent.
