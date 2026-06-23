# Final Audit

Date: 2026-06-23

Version: v5_expanded

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Validated Artifacts

- PDF: `C:/Users/wangz/Downloads/112.pdf`
- SHA256: `43EB404BF1B1B34E7642EB0D3D6BC2561E2962103A69054AB991DA226D199C10`
- Pages: 25
- Validator: `python scripts\validate_submission_artifacts.py` passed.
- Visual QA: sampled title/citation page, gate table page, mid-paper figure page, appendix page, and bibliography page rendered without clipping or unreadable content.
- Artifact placement: no `112.pdf` exists on Desktop, factory root, or child repo root.

## Frozen Local Result

- Proposed: `side_effect_causal_preference_model_v5`.
- Strongest non-oracle: `proposed_side_effect_preference_model_v4`.
- Hard success: `0.63901` vs `0.60294`.
- Hard utility: `0.69629` vs `0.62443`.
- Paired hard utility wins: `10/10`.
- Local gates: all pass.
- Scope gate: fails honestly.

## Scope Failures

The paper still needs real human labels, real label-disagreement analysis, robot or accepted high-fidelity downstream evaluation, calibrated deployment logs, trained checkpoints, and rollout evidence before it can be treated as ICLR-main ready.
