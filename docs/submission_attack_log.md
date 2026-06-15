# Submission Attack Log

## Attack: This is just side-effect classification.

Response: Side-effect classification is the strongest non-oracle baseline and is beaten by `0.066 +/- 0.010` paired success.

## Attack: Query cost is too high.

Response: Query cost is lower than the strongest baseline locally, but real human-label studies are still required.

## Attack: The benchmark is local.

Response: Correct. This is why the decision is `STRONG_REVISE`, not ready acceptance.

## Attack: Human preferences may disagree.

Response: Correct. Real submission needs label-variance and disagreement analysis.

## Attack: The stress and failure analysis is too thin.

Response: v4.1 expands the stress audit to 7,350 task/regime/seed rows and 8 failure cases. This improves local rigor but still does not replace real labels or robot/high-fidelity validation.
