# Submission Readiness Audit v4.1

Paper: 112 `preference_learning_physical_side_effects`

Date: 2026-06-15

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

Command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\112_preference_learning_physical_side_effects_continuation_rerun_20260615.log
```

## Integrity Gates

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1,575 rows.
- `seed_task_regime_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 30 rows.
- `stress_sweep_seed_metrics.csv`: 7,350 task/regime/seed rows.
- `failure_cases.csv`: 8 rows.
- Numeric sanity: no NaN or infinite values found.

## Result Gates

- Strongest non-oracle baseline: `side_effect_classifier_baseline`.
- Combined-stress success: `0.581 +/- 0.007` proposed vs `0.515 +/- 0.006` baseline.
- Side-effect recall: `0.601` proposed vs `0.469` baseline.
- Side-effect violation: `0.048` proposed vs `0.092` baseline.
- Damage rate: `0.047` proposed vs `0.066` baseline.
- False alarm: `0.085` proposed vs `0.097` baseline.
- Query cost: `0.228` proposed vs `0.268` baseline.
- Paired success gain: `0.066 +/- 0.010`, 7/7 seed wins.
- Ablation margin over best removed component: `0.024`.
- Max stress success: `0.569 +/- 0.008` proposed vs `0.501 +/- 0.007` side-effect classifier and `0.659 +/- 0.006` oracle.

## Submission Decision

The local evidence clears the strong-revise gate: strongest-baseline margin, side-effect diagnostic improvements, safety/cost non-regression, paired-seed wins, ablation margin, expanded stress detail, and failure-case documentation all pass.

The paper is not ICLR-main ready. It still needs real human preference labels, label-disagreement analysis, robot or independent high-fidelity validation, and a deeper manual related-work treatment before submission.

## Artifact Gate

- PDF: `C:/Users/wangz/Downloads/112.pdf`.
- SHA256: `52B2E473119F55397476C7446E1CB3FFFEEE9F96B84F4941E597DBF1F43E8112`.
- Size: `404159` bytes.
- Desktop copy: absent.
- LaTeX scan: no substantive warnings; only the `rerunfilecheck` package line matched the warning scan.
- BibTeX scan: `warning$ -- 0`; `missing$ -- 5` is the style's built-in function-call counter.
