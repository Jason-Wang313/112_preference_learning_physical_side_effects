# Paper 112 Rebuild Plan: Preference Learning Physical Side Effects

Started: 2026-06-15 02:09:00 +0100

## Goal

Rebuild Paper 112 from a v3 archive into an evidence-backed ICLR-main-target submission candidate, or keep it archived if evidence fails. The paper will remain explicitly not submission-ready without real human preference labels or robot/high-fidelity validation.

## Core Claim To Test

Robotic preference learning can overfit to visible task success and miss physical side effects: scuffs, displaced objects, excess force, irreversible clutter, unstable placements, and human-workspace disruption. A preference model should represent side-effect mechanisms explicitly rather than relying on generic pairwise outcome preferences.

## Proposed Method

`proposed_side_effect_preference_model`

The method combines:
- Physical side-effect taxonomy over force damage, object displacement, clutter, instability, irreversibility, and human-workspace disruption.
- Counterfactual side-effect labels that compare successful trajectories with different physical costs.
- Query selector that asks humans about ambiguous side effects rather than easy success/failure pairs.
- Constraint-aware preference aggregator that separates task preference from side-effect aversion.
- Calibration guard that avoids over-constraining benign physical changes.

## Benchmark Design

Run a local side-effect preference benchmark with:
- Five tasks: table clearing, drawer retrieval, cable routing, tool handoff, and mobile shelf placement.
- Seven side-effect regimes: nominal, force damage, object displacement, clutter accumulation, unstable placement, irreversible change, and combined side-effect stress.
- Five deployment splits: nominal, seen shift, unseen object, unseen side effect, and combined stress.
- Nine methods: success-only policy, generic pairwise preference model, reward-model RLHF surrogate, uncertainty-query preference learner, constraint-aware planner, failure-prediction shield, side-effect classifier baseline, proposed model, and oracle side-effect preference judge.
- Seven paired seeds with 84 evaluation episodes per task/regime/split/method.

## Primary Metrics

- Task success.
- Side-effect violation rate.
- Preference regret.
- Side-effect recall.
- False side-effect alarm rate.
- Query cost.
- Damage rate.
- Regret to oracle side-effect judge.

## Decision Gates

Mark `STRONG_REVISE` only if all are true:
- Success margin over the strongest non-oracle baseline is at least 0.030 on combined stress.
- Side-effect recall improves by at least 0.050 or side-effect violation falls by at least 0.050.
- Damage, false side-effect alarms, and query cost do not increase versus the strongest non-oracle baseline.
- Proposed method wins at least 5 of 7 paired seeds versus the strongest non-oracle baseline.
- Removing the side-effect taxonomy reduces success by at least 0.020.

Otherwise mark `KILL_ARCHIVE`.

## Manuscript Changes

- Replace archive framing with a full paper about physical side-effect preferences.
- Add related work around preference learning, RLHF, constraint learning, assistance preferences, and safe robot learning.
- Include local evidence tables, stress curves, ablation figures, failure cases, and limitations.
- Keep the limitation explicit: no real human-label or robot validation yet.

## Artifact Requirements

- Produce `C:/Users/wangz/Downloads/112.pdf` only.
- Do not copy a PDF to the visible Desktop.
- Update `README.md`, `child_status.md`, paper docs, and root reports after the terminal decision.
- Commit and push the public GitHub repo only after local audits pass.
