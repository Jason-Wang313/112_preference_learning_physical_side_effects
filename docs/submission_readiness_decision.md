# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

Reason: The v4.1 local benchmark supports the mechanism against strong local baselines and ablations, with `7,350` task/regime/seed stress rows, `8` failure cases, no numeric-integrity issues, and 7/7 paired-seed wins over the strongest non-oracle baseline. Real human preference labels and robot/high-fidelity validation are still missing.

Honest terminal action: continue as a strong-revise project. Do not submit to ICLR main until real labels and validation exist.

Revival condition for submission: validate the side-effect taxonomy and preference model with human labels, label-disagreement analysis, and robot or high-fidelity downstream evaluations.
