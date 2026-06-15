# Final Audit

Paper: 112 preference_learning_physical_side_effects

Decision: STRONG_REVISE

The v4.1 rebuild adds a local physical side-effect preference benchmark with paired seeds, strong local baselines, ablations, expanded stress sweeps, failure cases, LaTeX tables, and figures. The proposed side-effect preference model beats the strongest non-oracle baseline, `side_effect_classifier_baseline`, by `0.066 +/- 0.010` paired success under combined stress.

Side-effect diagnostics pass: recall improves by `0.132`, violation falls by `0.044`, damage falls by `0.018`, false alarms fall by `0.012`, and query cost falls by `0.041`.

Coverage audit passes: `metrics.csv` has 45 rows; `seed_task_regime_metrics.csv` has 11,025 rows; `ablation_task_regime_seed_metrics.csv` has 1,715 rows; `stress_sweep_seed_metrics.csv` has 7,350 task/regime/seed rows; `failure_cases.csv` has 8 rows; numeric checks found no NaN or infinite values.

Artifact audit passes: `C:/Users/wangz/Downloads/112.pdf` exists, is 404,159 bytes, has SHA256 `52B2E473119F55397476C7446E1CB3FFFEEE9F96B84F4941E597DBF1F43E8112`, and `C:/Users/wangz/Desktop/112.pdf` is absent.

Remaining blocker: the evidence is local. The paper should not be submitted to ICLR main without real human labels and robot or independent high-fidelity validation.
