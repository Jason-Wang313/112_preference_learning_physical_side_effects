# Claims

## Supported Local Claims

- `side_effect_causal_preference_model_v5` beats the strongest non-oracle baseline, `proposed_side_effect_preference_model_v4`, on hard-split success and utility.
- The local audit supports a causal side-effect mechanism story: explicit taxonomy, counterfactual pairs, labeler-disagreement weighting, delayed-effect memory, benign-change calibration, and deployment-risk budgeting all contribute to the v5 result.
- The v5 method improves side-effect recall and lowers damage, false alarms, query cost, and preference regret relative to the strongest non-oracle baseline.
- The fixed-risk audit reports coverage and deployment utility together, preventing conservative refusal from masquerading as safety.

## Unsupported Claims

- No claim of ICLR-main readiness.
- No claim of real human preference validation.
- No claim of real label-disagreement validation.
- No claim of robot hardware or accepted high-fidelity simulator validation.
- No claim of trained downstream policy deployment.
- No claim that the side-effect taxonomy is complete.
