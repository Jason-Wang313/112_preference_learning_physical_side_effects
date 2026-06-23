# Paper 112 Expanded-Standard v5 Plan

Build paper 112 `preference_learning_physical_side_effects` into a real submission-candidate artifact, not a cosmetic length expansion. Use CPU-only, RAM-light synthetic/local evidence and keep the terminal decision honest.

Frozen v5 rule:
- treat the old v4.1 proposed method as a strong non-oracle baseline, not as the final method;
- introduce the v5 method only if it has a clear mechanism: causal physical side-effect taxonomy, counterfactual preference pairs, labeler-disagreement weighting, delayed-effect memory, calibrated benign-change exceptions, and deployment-risk budgeting;
- run a larger deterministic audit: 10 tasks, 8 side-effect regimes, 8 deployment splits, 16 methods, 10 paired seeds, 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases;
- require hard-split success and utility margins over the strongest non-oracle baseline;
- require diagnostic gains, no damage/false-alarm/query/regret regression, paired hard-seed wins, ablation support, stress-endpoint support, and fixed-risk coverage;
- generate a 25+ page ICLR-style PDF with bright boxed clickable citations and tables grounded in the frozen CSVs;
- copy only the numbered PDF to `C:/Users/wangz/Downloads/112.pdf`;
- keep `ICLR main ready: no` unless real human preference labels, label-disagreement audits, robot or accepted high-fidelity downstream evaluation, deployment logs, and rollout evidence exist.

Terminal decision policy:
- `STRONG_REVISE` if all frozen local gates pass but the scope gate fails.
- `KILL_ARCHIVE` if any frozen local gate fails.
