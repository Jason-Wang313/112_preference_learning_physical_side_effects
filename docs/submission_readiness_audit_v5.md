# Submission Readiness Audit v5

Paper: 112 `preference_learning_physical_side_effects`

Date: 2026-06-23

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python src\run_experiment.py
python scripts\generate_manuscript.py
```

## Integrity Gates

- `dataset_summary.csv`: 80 rows.
- `cell_metrics.csv`: 102,400 rows.
- `main_group_metrics.csv`: 10,240 rows.
- `seed_metrics.csv`: 1,280 rows.
- `metrics.csv`: 128 rows.
- `hard_seed_metrics.csv`: 160 rows.
- `hard_aggregate_metrics.csv`: 16 rows.
- `hard_pairwise_stats.csv`: 15 rows.
- `ablation_cell_metrics.csv`: 8,000 rows.
- `stress_sweep_cell_metrics.csv`: 48,000 rows.
- `fixed_risk_cell_metrics.csv`: 51,200 rows.
- `failure_cases.csv`: 24 rows.
- Numeric sanity: validator found no NaN or infinite values.

## Result Gates

- Strongest non-oracle baseline: `proposed_side_effect_preference_model_v4`.
- Hard success: `0.63901` proposed vs `0.60294` baseline.
- Hard utility: `0.69629` proposed vs `0.62443` baseline.
- Side-effect recall delta: `+0.06755`.
- Side-effect violation delta: `-0.01735`.
- Damage delta: `-0.01309`.
- False alarm delta: `-0.01943`.
- Query cost delta: `-0.01485`.
- Preference regret delta: `-0.01079`.
- Paired hard utility wins: `10/10`.
- Stress endpoint utility margin: `+0.06804`.
- Strict fixed-risk coverage: `0.84000`.
- Strict fixed-risk utility margin: `+0.41944`.

## Artifact Gate

- PDF: `C:/Users/wangz/Downloads/112.pdf`.
- SHA256: `43EB404BF1B1B34E7642EB0D3D6BC2561E2962103A69054AB991DA226D199C10`.
- Pages: 25.
- Desktop copy: absent.
- Validator: passed.
