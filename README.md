# 112 Preference Learning Physical Side Effects

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE for ICLR main-conference development.

ICLR main ready: no.

This rebuild expands Paper 112 into a 25-page ICLR-style audit of causal preference learning for physical side effects in robot tasks. It is a stronger local evidence package than v4.1, but it is still not submission-ready because it lacks real human preference labels, real label-disagreement audits, robot or accepted high-fidelity downstream evaluation, calibrated deployment logs, trained policy checkpoints, and rollout evidence.

## Evidence Snapshot

- Proposed: `side_effect_causal_preference_model_v5`.
- Strongest non-oracle baseline: `proposed_side_effect_preference_model_v4`.
- Oracle: `oracle_human_side_effect_judge`.
- Main audit: 10 tasks x 8 side-effect regimes x 8 deployment splits x 16 methods x 10 seeds = 102,400 cell rows.
- Aggregates: 10,240 main group rows, 1,280 seed metric rows, 128 method/split metric rows.
- Hard audit: 160 hard seed rows, 16 hard aggregate rows, 15 paired comparisons.
- Extra evidence: 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, 24 failure cases.
- Hard success: `0.63901` proposed vs `0.60294` strongest non-oracle vs `0.71629` oracle.
- Hard utility: `0.69629` proposed vs `0.62443` strongest non-oracle vs `0.79124` oracle.
- Key deltas vs strongest non-oracle: success `+0.03607`, utility `+0.07187`, side-effect recall `+0.06755`, violation `-0.01735`, damage `-0.01309`, false alarm `-0.01943`, query cost `-0.01485`, preference regret `-0.01079`.
- Paired hard utility wins: `10/10`.
- Ablation margin: success `+0.02060`, utility `+0.03881`.
- Stress endpoint utility margin: `+0.06804`.
- Strict fixed-risk budget: `0.08`; coverage `0.84000`, breach `0.18000`, utility margin `+0.41944`.

## Reproduce

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item paper\main.pdf C:\Users\wangz\Downloads\112.pdf -Force
python scripts\validate_submission_artifacts.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/112.pdf`

PDF SHA256: `43EB404BF1B1B34E7642EB0D3D6BC2561E2962103A69054AB991DA226D199C10`

PDF pages: `25`

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
