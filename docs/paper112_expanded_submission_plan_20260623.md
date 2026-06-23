# Paper 112 Expanded Submission Plan

Date: 2026-06-23

Paper: `112_preference_learning_physical_side_effects`

Target venue posture: ICLR-main hostile-review readiness audit.

## Goal

Rebuild Paper 112 as a 25+ page, evidence-bound submission artifact about preference learning for physical side effects. The rebuild must improve theory, experiment breadth, baseline strength, ablation coverage, stress testing, and artifact validation while preserving the honest conclusion that the paper is not ICLR-main ready without real human labels and robot or accepted high-fidelity downstream validation.

## Frozen Method Hypothesis

Generic preference learning can overfit to visible task success and miss physical side effects that humans care about. A useful robotics preference model should represent side-effect mechanisms causally: contact damage, displaced objects, clutter, instability, irreversible changes, human-workspace disruption, delayed visibility, and latent material state. The proposed v5 method, `side_effect_causal_preference_model_v5`, must outperform both generic preference baselines and the v4.1 proposed model under hostile side-effect splits.

## Frozen Experimental Scope

- Main audit: 10 tasks x 8 side-effect regimes x 8 deployment splits x 16 methods x 10 seeds = 102,400 cell rows.
- Main aggregation: 10,240 task/regime/split/method rows, 1,280 method/split/seed rows, and 128 method/split metric rows.
- Hard aggregate: 160 method/seed rows, 16 method rows, and 15 paired comparisons against the proposed v5 method.
- Ablations: 10 variants x 10 tasks x 8 regimes x 10 seeds = 8,000 cell rows.
- Stress sweep: 6 stress levels x 10 methods x 10 tasks x 8 regimes x 10 seeds = 48,000 cell rows.
- Fixed-risk audit: 4 deployment budgets x 16 methods x 10 tasks x 8 regimes x 10 seeds = 51,200 cell rows.
- Failure analysis: 24 predefined boundary cases spanning hidden damage, disagreement, delayed effects, tactile-only signals, overcautious rejection, covariate shift, and oracle headroom.

## Strong Baselines

The non-oracle comparator set includes success-only control, generic pairwise preferences, RLHF reward modeling, uncertainty querying, constraint-aware planning, failure prediction, side-effect classification, inverse reward design, conservative safety filtering, preference transformers without side-effect mechanisms, maximum-uncertainty human querying, physical affordance penalties, risk-calibrated reward modeling, and `proposed_side_effect_preference_model_v4`.

## Frozen Gates

The paper may remain `STRONG_REVISE` only if all local gates pass:

- Hard success margin over the strongest non-oracle baseline is at least 0.030.
- Hard utility margin over the strongest non-oracle baseline is at least 0.050.
- Side-effect recall improves by at least 0.050 or side-effect violation falls by at least 0.030.
- Damage, false alarms, query cost, and preference regret do not increase.
- Proposed v5 wins at least 8/10 paired hard utility seeds.
- The best removed-component ablation remains below the full method by at least 0.010 success or 0.040 utility.
- Stress endpoint utility margin is at least 0.050.
- Fixed-risk deployment coverage is at least 0.300 and below 0.950, with positive fixed-risk utility margin.

## Scope Gate

The scope gate is intentionally separate and must fail for this local-only rebuild. The manuscript and ledgers must state that ICLR-main readiness remains `no` because the work lacks real human preference labels, label-disagreement audits on actual labels, robot or accepted high-fidelity downstream evaluation, calibrated deployment logs, trained policy checkpoints, and rollout-video evidence.

## Artifact Rules

- Build the manuscript from generated CSVs and tables, not hand-entered result prose.
- Use bright boxed clickable citations.
- Validate LaTeX, BibTeX, page count, PDF hash, CSV row counts, numeric finiteness, gates, and artifact location.
- Keep the final numbered PDF only at `C:/Users/wangz/Downloads/112.pdf`; no visible Desktop copy.
