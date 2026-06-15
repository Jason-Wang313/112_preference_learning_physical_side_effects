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
