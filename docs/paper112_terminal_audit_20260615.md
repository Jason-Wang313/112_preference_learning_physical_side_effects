# Paper 112 Terminal Audit - 2026-06-15

Paper: `preference_learning_physical_side_effects`

Terminal state: STRONG_REVISE

ICLR main ready: no

## What Passed

- Code compiled with `python -m py_compile src\run_experiment.py`.
- Experiment reran successfully under low-RAM thread caps.
- All expected CSV row counts passed.
- Numeric audit found no NaN or infinite values.
- Proposed method beats the strongest non-oracle baseline under combined stress.
- Proposed method wins 7/7 paired seeds over the strongest non-oracle baseline.
- Core ablations remain below the full method.
- Stress evidence now includes 7,350 task/regime/seed rows.
- Failure-case documentation now includes 8 concrete boundaries.
- Numbered PDF exists at `C:/Users/wangz/Downloads/112.pdf`.
- PDF SHA256 is `52B2E473119F55397476C7446E1CB3FFFEEE9F96B84F4941E597DBF1F43E8112`.
- No `C:/Users/wangz/Desktop/112.pdf` copy exists.

## What Did Not Pass

- No real human preference labels.
- No label-disagreement study.
- No real robot or independent high-fidelity simulator validation.
- No evidence that the local generated benchmark transfers to physical deployment.

## Decision

Mark as `STRONG_REVISE`. Do not claim ICLR-main submission readiness until real label and robot/high-fidelity validation gates are satisfied.
