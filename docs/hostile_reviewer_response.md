# Hostile Reviewer Response

Paper: 112 Preference Learning Physical Side Effects

## Strongest Technical Threats

- This may be just side-effect classification.
- Constraint-aware planners may already reduce damage.
- Query cost may become impractical.
- No real human labels are used.

## Response

The v4 rebuild includes side-effect classification as the strongest non-oracle baseline. The proposed model improves combined-stress success by `0.066 +/- 0.010`, improves recall by `0.132`, and lowers violations, damage, false alarms, and query cost.

## Honest Action

Mark as `STRONG_REVISE`, not ready acceptance. Submission requires real human-label and robot/high-fidelity validation.
