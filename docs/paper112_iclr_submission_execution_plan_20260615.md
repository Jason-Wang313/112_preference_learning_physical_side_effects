# Paper 112 ICLR Submission-Readiness Execution Plan

Date: 2026-06-15

Paper: `112_preference_learning_physical_side_effects`

Working title: Preference Learning for Physical Side Effects

## Goal

Re-audit Paper 112 as if preparing an ICLR-main submission, while keeping the decision evidence-bound. The paper may remain `STRONG_REVISE` only if the rerun reproduces a decisive local side-effect-aware preference-learning advantage over the strongest non-oracle baseline without increasing damage, false side-effect alarms, or query cost. It must not be marked ICLR-main-ready without real human preference labels and robot or independent high-fidelity validation.

## Current Hypothesis

Robotic preference learning can overfit to visible task success and miss physical side effects such as scuffed surfaces, displaced objects, clutter, unstable placements, irreversible changes, and human-workspace disruption. The proposed `proposed_side_effect_preference_model` should improve preference learning by representing physical side-effect mechanisms explicitly rather than relying on generic pairwise outcome preferences.

## Evidence To Rebuild

- Compile-check `src/run_experiment.py`.
- Re-run the full local benchmark from scratch with fixed threading.
- Verify CSV coverage for metrics, per-task/regime records, seed-level splits, paired comparisons, ablations, stress sweep, and failure cases.
- Confirm the strongest non-oracle baseline under combined stress.
- Confirm success, side-effect violation, preference regret, side-effect recall, false alarm, query cost, damage rate, and regret-to-oracle results.
- Confirm pairwise seed wins and 95 percent confidence intervals.
- Confirm every removed-component ablation remains below the full method.
- Confirm the stress sweep preserves ordering through maximum side-effect stress.
- Confirm the PDF rebuild uses the ICLR style, has no fatal LaTeX/BibTeX issues, and is copied only to `C:/Users/wangz/Downloads/112.pdf`.
- Confirm no `112.pdf` exists on the visible Desktop.
- Confirm the public GitHub repo is current after any edits.

## Decision Gates

Keep `STRONG_REVISE` only if all gates pass:

- Success margin over strongest non-oracle baseline is at least `0.030` on combined stress.
- Side-effect recall improves by at least `0.050` or side-effect violation falls by at least `0.050`.
- Damage, false side-effect alarms, and query cost do not increase versus the strongest non-oracle baseline.
- Proposed method wins at least `5/7` paired seeds against the strongest non-oracle baseline.
- Removing the side-effect taxonomy reduces success by at least `0.020`.

Mark `KILL_ARCHIVE` if any gate fails.

Do not mark ICLR-main-ready unless the side-effect taxonomy and preference model are validated with real human labels, label-disagreement analysis, and robot or high-fidelity downstream evaluations. The current local benchmark can support only `STRONG_REVISE`.

## Execution Steps

1. Audit the repository state and prior v4 documents for stale or inflated claims.
2. Run `python -m py_compile src/run_experiment.py`.
3. Run `python src/run_experiment.py` with `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` set to `1`, logging to the root `logs` directory.
4. Programmatically validate result files for row counts, finite numeric values, strongest-baseline identity, gate outcomes, pairwise statistics, ablations, stress sweep, and failure cases.
5. Patch recoverable rigor gaps, especially stress-sweep granularity or failure-case coverage, then rerun if needed.
6. Patch `README.md`, `child_status.md`, `plan.md`, `docs/submission_readiness_decision.md`, `docs/final_audit.md`, `docs/iclr_main_gate.md`, `docs/submission_version_log.md`, and `paper/main.tex` to reflect the verified rerun.
7. Add a terminal audit document and a v4.1 submission-readiness audit document.
8. Rebuild the paper with `pdflatex`, `bibtex`, `pdflatex`, and `pdflatex`.
9. Scan `main.log` and `main.blg`; fix recoverable Overfull/Underfull, undefined-reference, citation, or bibliography issues.
10. Copy only `paper/main.pdf` to `C:/Users/wangz/Downloads/112.pdf`.
11. Hash `C:/Users/wangz/Downloads/112.pdf`, confirm file size, and confirm `C:/Users/wangz/Desktop/112.pdf` is absent.
12. Commit and push the child repository to its public GitHub repo.
13. Update the root `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, and `MASTER_SUBMISSION_REPORT.md` through Paper 112.

## Expected Terminal Wording

If the rerun matches the prior evidence, the honest terminal state is:

`STRONG_REVISE`: local physical-side-effect preference evidence supports continuing, but the paper is not ICLR-main-ready because it lacks real human labels and robot or independent high-fidelity validation.
