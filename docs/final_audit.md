# Final Audit

Paper: 112 preference_learning_physical_side_effects

Decision: STRONG_REVISE

The v4 rebuild adds a local physical side-effect preference benchmark with paired seeds, strong local baselines, ablations, stress sweeps, failure cases, LaTeX tables, and figures. The proposed side-effect preference model beats the strongest non-oracle baseline, `side_effect_classifier_baseline`, by `0.066 +/- 0.010` paired success under combined stress.

Side-effect diagnostics pass: recall improves by `0.132`, violation falls by `0.044`, damage falls by `0.018`, false alarms fall by `0.012`, and query cost falls by `0.041`.

Remaining blocker: the evidence is local. The paper should not be submitted to ICLR main without real human labels and robot or independent high-fidelity validation.
