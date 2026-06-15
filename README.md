# 112 Preference Learning Physical Side Effects

Submission-hardening version: v4

Terminal decision: STRONG_REVISE for ICLR main-conference development.

This rebuild replaces the v3 archive with a local physical side-effect preference benchmark. The paper is still not ICLR-main-ready because it lacks real human preference labels and real robot or independent high-fidelity validation, but the local evidence supports continued development.

## Evidence Snapshot

- Benchmark: 5 tasks x 7 side-effect regimes x 5 deployment splits x 9 methods.
- Seeds: 7 paired seeds, 84 evaluation episodes per task/regime/split/method group.
- Strongest non-oracle baseline: `side_effect_classifier_baseline`.
- Proposed: `proposed_side_effect_preference_model`.
- Combined-stress success: `0.581 +/- 0.007` proposed vs `0.515 +/- 0.006` strongest baseline.
- Side-effect recall: `0.601` proposed vs `0.469` strongest baseline.
- Side-effect violation: `0.048` proposed vs `0.092` strongest baseline.
- Pairwise wins: 7/7 seeds over the strongest baseline.
- Best removed-component ablation: `minus_ambiguous_query_selector`; full method remains ahead by `0.024` success.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/112.pdf`
