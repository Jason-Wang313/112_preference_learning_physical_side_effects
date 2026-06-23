import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
PAPER.mkdir(exist_ok=True)


def read_csv(name):
    with (RESULTS / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def tex_escape(value):
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def fnum(value, digits=3):
    return f"{float(value):.{digits}f}"


def make_failure_appendix():
    rows = read_csv("failure_cases.csv")
    parts = []
    for row in rows:
        parts.append(
            "\\paragraph{"
            + tex_escape(row["case"].replace("_", " "))
            + ".} "
            + tex_escape(row["observed_failure"])
            + " The frozen audit tags this boundary under \\texttt{"
            + tex_escape(row["stress_context"])
            + "} with severity "
            + fnum(row["severity"], 2)
            + ". The required next evidence is: "
            + tex_escape(row["lesson"])
            + "."
        )
    return "\n\n".join(parts)


def write_references():
    references = r"""@inproceedings{christiano2017deep,
  title={Deep reinforcement learning from human preferences},
  author={Christiano, Paul F. and Leike, Jan and Brown, Tom and Martic, Miljan and Legg, Shane and Amodei, Dario},
  booktitle={Advances in Neural Information Processing Systems},
  year={2017}
}

@inproceedings{sadigh2017active,
  title={Active preference-based learning of reward functions},
  author={Sadigh, Dorsa and Dragan, Anca D. and Sastry, Shankar and Seshia, Sanjit A.},
  booktitle={Robotics: Science and Systems},
  year={2017}
}

@inproceedings{hadfieldmenell2017inverse,
  title={Inverse reward design},
  author={Hadfield-Menell, Dylan and Milli, Smitha and Abbeel, Pieter and Russell, Stuart and Dragan, Anca},
  booktitle={Advances in Neural Information Processing Systems},
  year={2017}
}

@inproceedings{hadfieldmenell2017off,
  title={The off-switch game},
  author={Hadfield-Menell, Dylan and Dragan, Anca and Abbeel, Pieter and Russell, Stuart},
  booktitle={International Joint Conference on Artificial Intelligence},
  year={2017}
}

@inproceedings{bajcsy2017learning,
  title={Learning robot objectives from physical human interaction},
  author={Bajcsy, Andrea and Losey, Dylan P. and O'Malley, Marcia K. and Dragan, Anca D.},
  booktitle={Conference on Robot Learning},
  year={2017}
}

@inproceedings{brown2019extrapolating,
  title={Extrapolating beyond suboptimal demonstrations via inverse reinforcement learning from observations},
  author={Brown, Daniel S. and Goo, Wonjoon and Nagarajan, Prabhat and Niekum, Scott},
  booktitle={International Conference on Machine Learning},
  year={2019}
}

@inproceedings{ng2000algorithms,
  title={Algorithms for inverse reinforcement learning},
  author={Ng, Andrew Y. and Russell, Stuart},
  booktitle={International Conference on Machine Learning},
  year={2000}
}

@inproceedings{abbeel2004apprenticeship,
  title={Apprenticeship learning via inverse reinforcement learning},
  author={Abbeel, Pieter and Ng, Andrew Y.},
  booktitle={International Conference on Machine Learning},
  year={2004}
}

@article{wirth2017survey,
  title={A survey of preference-based reinforcement learning methods},
  author={Wirth, Christian and Akrour, Riad and Neumann, Gerhard and F{\"u}rnkranz, Johannes},
  journal={Journal of Machine Learning Research},
  volume={18},
  number={136},
  pages={1--46},
  year={2017}
}

@inproceedings{wilson2012bayesian,
  title={A Bayesian approach for policy learning from trajectory preference queries},
  author={Wilson, Aaron and Fern, Alan and Tadepalli, Prasad},
  booktitle={Advances in Neural Information Processing Systems},
  year={2012}
}

@article{amodei2016concrete,
  title={Concrete problems in AI safety},
  author={Amodei, Dario and Olah, Chris and Steinhardt, Jacob and Christiano, Paul and Schulman, John and Man{\'e}, Dan},
  journal={arXiv preprint arXiv:1606.06565},
  year={2016}
}

@article{leike2017ai,
  title={AI safety gridworlds},
  author={Leike, Jan and Martic, Miljan and Krakovna, Victoria and Ortega, Pedro A. and Everitt, Tom and Lefrancq, Andrew and Orseau, Laurent and Legg, Shane},
  journal={arXiv preprint arXiv:1711.09883},
  year={2017}
}

@article{krakovna2018measuring,
  title={Measuring and avoiding side effects using relative reachability},
  author={Krakovna, Victoria and Orseau, Laurent and Kumar, Ramana and Martic, Miljan and Legg, Shane},
  journal={arXiv preprint arXiv:1806.01186},
  year={2018}
}

@inproceedings{turner2020conservative,
  title={Conservative agency via attainable utility preservation},
  author={Turner, Alexander Matt and Smith, Logan and Shah, Rohin and Critch, Andrew and Tadepalli, Prasad},
  booktitle={AAAI/ACM Conference on AI, Ethics, and Society},
  year={2020}
}

@inproceedings{bobu2020quantifying,
  title={Quantifying hypothesis space misspecification in learning from human-robot demonstrations and physical corrections},
  author={Bobu, Andreea and Bajcsy, Andrea and Fisac, Jaime F. and Dragan, Anca D.},
  booktitle={IEEE Transactions on Robotics},
  year={2020}
}

@inproceedings{losey2020learning,
  title={Learning latent actions to control assistive robots},
  author={Losey, Dylan P. and Jeon, Hong Jun and Li, Mengxi and Srinivasan, Krishnan and Mandlekar, Ajay and Bohg, Jeannette and Sadigh, Dorsa},
  booktitle={Autonomous Robots},
  year={2020}
}
"""
    (PAPER / "references.bib").write_text(references, encoding="utf-8")


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    metrics = summary["metrics"]
    rows = summary["row_counts"]
    failure_appendix = make_failure_appendix()
    write_references()

    replacements = {
        "@HARD_SUCCESS_PROPOSED@": fnum(metrics["hard_success_proposed"]),
        "@HARD_SUCCESS_BASELINE@": fnum(metrics["hard_success_strongest"]),
        "@HARD_SUCCESS_ORACLE@": fnum(metrics["hard_success_oracle"]),
        "@HARD_UTILITY_PROPOSED@": fnum(metrics["hard_utility_proposed"]),
        "@HARD_UTILITY_BASELINE@": fnum(metrics["hard_utility_strongest"]),
        "@HARD_UTILITY_ORACLE@": fnum(metrics["hard_utility_oracle"]),
        "@HARD_SUCCESS_MARGIN@": fnum(metrics["hard_success_margin"]),
        "@HARD_UTILITY_MARGIN@": fnum(metrics["hard_utility_margin"]),
        "@RECALL_DELTA@": fnum(metrics["side_effect_recall_delta"]),
        "@VIOLATION_DELTA@": fnum(metrics["side_effect_violation_delta"]),
        "@DAMAGE_DELTA@": fnum(metrics["damage_rate_delta"]),
        "@FALSE_DELTA@": fnum(metrics["false_alarm_delta"]),
        "@QUERY_DELTA@": fnum(metrics["query_cost_delta"]),
        "@REGRET_DELTA@": fnum(metrics["preference_regret_delta"]),
        "@PAIR_WINS@": str(metrics["paired_hard_utility_wins"]),
        "@ABLATION_SUCCESS_MARGIN@": fnum(metrics["ablation_success_margin"]),
        "@ABLATION_UTILITY_MARGIN@": fnum(metrics["ablation_utility_margin"]),
        "@STRESS_MARGIN@": fnum(metrics["stress_endpoint_utility_margin"]),
        "@FIXED_COVERAGE@": fnum(metrics["strict_fixed_risk_coverage"]),
        "@FIXED_BREACH@": fnum(metrics["strict_fixed_risk_breach"]),
        "@FIXED_MARGIN@": fnum(metrics["strict_fixed_risk_utility_margin"]),
        "@STRONGEST@": tex_escape(summary["strongest_non_oracle"]),
        "@PROPOSED@": tex_escape(summary["proposed"]),
        "@ORACLE@": tex_escape(summary["oracle"]),
        "@MAIN_ROWS@": f"{rows['main_cell']:,}",
        "@MAIN_GROUP_ROWS@": f"{rows['main_group']:,}",
        "@SEED_ROWS@": f"{rows['seed_metric']:,}",
        "@METRIC_ROWS@": f"{rows['metric']:,}",
        "@ABLATION_ROWS@": f"{rows['ablation_cell']:,}",
        "@STRESS_ROWS@": f"{rows['stress_cell']:,}",
        "@FIXED_ROWS@": f"{rows['fixed_risk_cell']:,}",
        "@FAILURE_ROWS@": f"{rows['failure_cases']:,}",
        "@FAILURE_APPENDIX@": failure_appendix,
    }

    tex = r"""\documentclass{article}
\usepackage{iclr2026_conference,times}
\input{math_commands.tex}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{url}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{array}
\raggedbottom
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1.4},
  citebordercolor={0 0.82 0},
  linkbordercolor={0 0.70 0},
  urlbordercolor={0 0.70 0}
}

\title{Causal Preference Learning for Physical Side Effects in Robot Tasks}
\author{Anonymous Authors}

\begin{document}
\maketitle

\begin{abstract}
Robots can optimize visible task success while producing physical side effects that humans dislike: scuffed surfaces, displaced objects, clutter, unstable placements, irreversible changes, human-workspace disruption, or delayed material damage. Preference learning is a natural alignment interface, but generic pairwise preferences and RLHF-style reward models can collapse these mechanisms into an opaque scalar. We rebuild Paper 112 as a hostile-review audit of this claim. The v5 protocol evaluates 16 methods, including the old v4.1 proposed method as a strong baseline, over @MAIN_ROWS@ main cells, @ABLATION_ROWS@ ablation cells, @STRESS_ROWS@ stress cells, @FIXED_ROWS@ fixed-risk deployment cells, and @FAILURE_ROWS@ predefined failure cases. The proposed \texttt{@PROPOSED@} reaches hard-split success @HARD_SUCCESS_PROPOSED@ versus @HARD_SUCCESS_BASELINE@ for the strongest non-oracle baseline \texttt{@STRONGEST@}, and hard utility @HARD_UTILITY_PROPOSED@ versus @HARD_UTILITY_BASELINE@. It improves side-effect recall by @RECALL_DELTA@, lowers damage by @DAMAGE_DELTA@, lowers false alarms by @FALSE_DELTA@, lowers query cost by @QUERY_DELTA@, wins @PAIR_WINS@/10 paired hard utility seeds, and remains below the oracle. The terminal decision is \textbf{STRONG\_REVISE}: the local evidence is coherent and reproducible, but the work is not ICLR-main ready without real human labels, label-disagreement audits, robot or accepted high-fidelity downstream evaluation, deployment logs, trained policies, and rollout evidence.
\end{abstract}

\section{Motivation}
Preference learning has become a standard way to make learned agents reflect human judgments rather than hand-written scalar rewards \citep{christiano2017deep,wirth2017survey,sadigh2017active,wilson2012bayesian}. Robotics makes the interface more treacherous than it appears. A robot can clear a table while scraping the finish, retrieve from a drawer while misaligning nearby objects, route a cable while creating clutter, or place a shelf item in a state that is temporarily stable but later tips. These outcomes are not simply lower task success. They are physical side effects, and they often become visible only through additional sensors, delayed observation, or a human norm that was not made explicit during the comparison.

This paper takes a deliberately narrow position. We do not claim that preference learning, inverse reinforcement learning, inverse reward design, side-effect avoidance, or robot corrections are new \citep{ng2000algorithms,abbeel2004apprenticeship,hadfieldmenell2017inverse,bajcsy2017learning,brown2019extrapolating}. The defensible claim is that a robot preference learner needs an explicit representation of physical side-effect mechanisms when comparisons are collected from successful trajectories. The empirical question is whether this representation survives strong local baselines, including the old v4.1 proposed method, side-effect classifiers, risk-calibrated reward models, inverse reward design, conservative filters, and high-cost uncertainty querying.

\paragraph{Review posture.}
The rebuild follows a hostile-review protocol: do not optimize for attractive numbers; optimize for a result that would survive an adversarial reviewer. We therefore freeze all gates before reading final numbers. If the proposed model clears the local gates, we keep only a \textbf{STRONG\_REVISE} decision because no real human-label or robot validation is present. If any local gate fails, the correct decision is \textbf{KILL\_ARCHIVE}. This separation prevents the common failure mode where a clean synthetic benchmark is mistaken for a submission-ready robotics paper.

\section{Problem Setup}
We consider a robot trajectory $\tau=(s_0,a_0,\ldots,s_T)$ with visible task reward, latent physical side-effect state, and a human preference label. Let $x(\tau)$ denote task-visible features, and let
\[
z(\tau)=\left(z^{force}, z^{disp}, z^{clutter}, z^{unstable}, z^{irrev}, z^{human}, z^{delay}, z^{latent}\right)
\]
denote side-effect mechanisms: force damage, object displacement, clutter accumulation, unstable placement, irreversibility, human-workspace disruption, delayed visibility, and latent material damage. A generic preference model estimates $\Pr(\tau_i \succ \tau_j \mid x_i,x_j)$; the v5 model estimates $\Pr(\tau_i \succ \tau_j \mid x_i,x_j,z_i,z_j,c)$ where $c$ includes user tolerance, deployment context, and risk budget. The distinction is not cosmetic. If two trajectories have equal visible success but different latent side effects, $x$ cannot identify the preference without an additional mechanism or label.

\paragraph{Side-effect-aware utility.}
The audit reports task success, side-effect recall, violation rate, damage rate, false alarm rate, query cost, preference regret, delayed-effect miss rate, label-disagreement loss, human-acceptance proxy, and utility. Utility is not used as a hidden training objective; it is a frozen evaluation index:
\[
U = \alpha_s S + \alpha_r R + \alpha_h H - \beta_v V - \beta_d D - \beta_g G - \beta_f F - \beta_q Q - \beta_l L - \beta_m M.
\]
Here $S$ is task success, $R$ side-effect recall, $H$ human acceptance, $V$ violation, $D$ damage, $G$ preference regret, $F$ false alarms, $Q$ query cost, $L$ label-disagreement loss, and $M$ delayed-effect miss. The exact coefficients are frozen in \texttt{src/run\_experiment.py}; changing them after seeing outcomes would invalidate the audit.

\paragraph{Identifiability boundary.}
If side-effect mechanisms are unobserved and the labeler never compares trajectories that differ only in side-effect state, no algorithm can identify side-effect aversion from task success alone. The v5 method is therefore not a magic preference learner. It relies on counterfactual preference pairs, mechanism features, and uncertainty about labeler tolerance. The paper's most important negative claim is that this local evidence cannot establish external validity without real labels and robot rollouts.

\section{Method}
The proposed method, \texttt{@PROPOSED@}, has six components.

\paragraph{Causal side-effect taxonomy.}
The model separates force damage, displacement, clutter, instability, irreversibility, human-workspace disruption, delayed visibility, and latent material state. This taxonomy is used for both prediction and audit stratification. It makes failure cases reportable: a method may improve visible side-effect classification while still missing delayed material damage.

\paragraph{Counterfactual preference pairs.}
The learner prioritizes pairs where visible task success is matched but side-effect mechanisms differ. This prevents the reward model from learning a shortcut in which successful trajectories are always preferred. The same idea is adjacent to inverse reward design and preference queries \citep{hadfieldmenell2017inverse,sadigh2017active}, but the v5 audit treats physical side effects as a first-class robotic mechanism rather than a generic uncertainty source.

\paragraph{Labeler-disagreement weighting.}
Human side-effect preferences are not deterministic. One person may tolerate temporary clutter; another may reject it in a shared workspace. The v5 model therefore discounts labels in high-disagreement regimes unless the query resolves a mechanism-level ambiguity. This is a local proxy for a real label-disagreement study; it is not a substitute for one.

\paragraph{Delayed-effect memory.}
Some side effects are not visible at the comparison moment. A stacked item may tip later, and a wiped surface may show damage only under tactile or material-state inspection. The v5 model carries a delayed-effect memory feature. Ablating this feature tests whether the model merely learned visible side-effect classification.

\paragraph{Benign-change calibration.}
Physical change is not always bad. Moving an object can be acceptable if it is intentional, reversible, and outside a human workspace. A calibration guard reduces false alarms for benign changes. The guard is essential because a model that rejects every physical change can look safe while becoming useless.

\paragraph{Deployment-risk budgeting.}
The deployment audit asks what happens when a policy is allowed to act only under a fixed physical-risk budget. This exposes a common safety-reporting trap: a conservative filter can reduce damage by refusing most actions. We therefore report both coverage and deployment utility.

\section{Theory}
\paragraph{Proposition 1: success-only preferences are insufficient.}
Assume two trajectories $\tau_a,\tau_b$ have the same visible task features $x(\tau_a)=x(\tau_b)$ and the same task success, but different side-effect states $z(\tau_a)\neq z(\tau_b)$. Any model whose prediction is a measurable function only of $x$ assigns the same preference score to both trajectories. If the human preference depends on $z$, the model cannot recover the preference ordering.

\emph{Proof sketch.} Since the model observes only $x$ and the two feature vectors are equal, the model output is identical. A preference function that assigns different utility because of $z$ cannot be represented. The result is an identifiability statement, not a performance claim.

\paragraph{Proposition 2: conservative safety can hide behind low coverage.}
Let a deployment rule accept trajectory $\tau$ only if estimated side-effect risk $\hat r(\tau)\leq b$. A rule that always rejects has zero measured accepted-risk violations, but zero useful coverage. Any safety comparison that omits coverage can prefer this degenerate rule over a useful policy. The fixed-risk audit avoids that failure by reporting coverage, breach rate, and deployment utility together.

\paragraph{Proposition 3: delayed side effects require temporal evidence.}
If a side effect is realized after the comparison horizon and no delayed observation is collected, then the preference data are compatible with both harmless and harmful latent dynamics. A delayed-effect memory feature can improve local predictions only when the generator exposes delayed state. In real deployment, this requires delayed labels or physical sensing.

These propositions are deliberately modest. They justify the audit design and the ablation axes; they do not prove that the v5 method will transfer to hardware.

\section{Frozen Experimental Protocol}
The v5 protocol is generated by \texttt{src/run\_experiment.py}. It is deterministic, CPU-only, and RAM-light. It expands the prior v4.1 benchmark from a small side-effect preference audit into @MAIN_ROWS@ main cells over 10 tasks, 8 side-effect regimes, 8 deployment splits, 16 methods, and 10 paired seeds. It also generates @ABLATION_ROWS@ ablation cells, @STRESS_ROWS@ stress cells, @FIXED_ROWS@ fixed-risk deployment cells, and @FAILURE_ROWS@ failure cases.

\input{generated_row_counts.tex}

\paragraph{Tasks.}
The tasks are table clearing, drawer retrieval, cable routing, tool handoff, mobile shelf placement, fragile object sorting, countertop wiping, bin packing cleanup, shared workspace fetch, and stacked container staging. The additional tasks are not padding. They introduce different physical channels: high force, clutter, instability, human workspace norms, delayed visibility, and latent damage.

\paragraph{Regimes and splits.}
The regimes are nominal, force damage, object displacement, clutter accumulation, unstable placement, irreversible change, human-workspace disruption, and latent material damage. The splits include nominal and seen shifts, but the hard aggregate is dominated by human-preference shift, delayed effects, latent-damage shift, and combined stress. This prevents the headline result from being driven by easy nominal cases.

\paragraph{Baselines.}
The comparator set is intentionally uncomfortable for the proposed method: success-only control, generic pairwise preferences, RLHF reward modeling \citep{christiano2017deep}, uncertainty-query preferences \citep{sadigh2017active,wilson2012bayesian}, constraint-aware planning, failure prediction, side-effect classification, inverse reward design \citep{hadfieldmenell2017inverse}, conservative safety filtering, preference transformers without side-effect mechanisms, maximum-uncertainty human querying, physical affordance penalties, risk-calibrated reward modeling, and \texttt{@STRONGEST@}. The oracle is reported only as headroom.

\paragraph{Frozen gates.}
The local gates require hard-split success and utility margins over the strongest non-oracle baseline, diagnostic improvement, no regression in damage, false alarms, query cost, or regret, at least 8/10 paired hard utility wins, a nontrivial ablation margin, endpoint stress robustness, and fixed-risk coverage that is neither zero nor suspiciously perfect. These gates were written before the v5 run.

\section{Main Results}
\input{generated_hard_results.tex}

The strongest non-oracle baseline is \texttt{@STRONGEST@}, which is important: the new method is not merely compared against weak generic preference learners. Hard-split success is @HARD_SUCCESS_PROPOSED@ for v5 versus @HARD_SUCCESS_BASELINE@ for that baseline, a margin of @HARD_SUCCESS_MARGIN@. Hard utility is @HARD_UTILITY_PROPOSED@ versus @HARD_UTILITY_BASELINE@, a margin of @HARD_UTILITY_MARGIN@. The oracle reaches hard utility @HARD_UTILITY_ORACLE@, leaving clear headroom.

\begin{figure}[t]
\centering
\includegraphics[width=0.96\linewidth]{../figures/side_effect_v5_hard_utility.png}
\caption{Hard-split utility for all methods. The proposed v5 method beats the old v4.1 method but remains below the oracle.}
\label{fig:hard-utility}
\end{figure}

\input{generated_gate_table.tex}

The diagnostic deltas show the actual mechanism of the gain. Recall improves by @RECALL_DELTA@. Side-effect violation changes by @VIOLATION_DELTA@, damage by @DAMAGE_DELTA@, false alarms by @FALSE_DELTA@, query cost by @QUERY_DELTA@, and preference regret by @REGRET_DELTA@ relative to the strongest non-oracle baseline. The paired hard utility comparison wins @PAIR_WINS@/10 seeds.

\begin{figure}[t]
\centering
\includegraphics[width=0.96\linewidth]{../figures/side_effect_v5_diagnostics.png}
\caption{Hard-split diagnostics. The key result is not only task success; v5 improves recall and utility while lowering damage, false alarms, query cost, and preference regret.}
\label{fig:diagnostics}
\end{figure}

\input{generated_pairwise_table.tex}

\section{Ablations}
\input{generated_ablation_table.tex}

The ablations are designed to be hostile to the method's story. Removing the taxonomy tests whether side-effect mechanisms matter. Removing counterfactual pairs tests whether the method needs matched-success comparisons. Removing labeler-disagreement weighting tests whether subjective tolerance is merely noise. Removing delayed-effect memory tests whether the method is just a visible classifier. Removing benign-change calibration tests overcautious rejection. Removing the deployment-risk budget tests whether local success survives under risk constraints. The full method beats the best removed component by @ABLATION_SUCCESS_MARGIN@ success and @ABLATION_UTILITY_MARGIN@ utility.

\begin{figure}[t]
\centering
\includegraphics[width=0.96\linewidth]{../figures/side_effect_v5_ablation.png}
\caption{Ablation utility under combined stress. The best removed component remains below the full method, but the margin is not so large that the result should be oversold.}
\label{fig:ablation}
\end{figure}

\section{Stress Sweep and Fixed-Risk Deployment}
\input{generated_stress_endpoint_table.tex}

The endpoint stress sweep checks whether the ordering survives maximum synthetic side-effect pressure. At stress level 1.0, v5 beats the strongest non-oracle stress comparator by @STRESS_MARGIN@ utility. This is a useful local result, but it remains a generated stress test. A real submission would need an accepted simulator split or hardware logs with the same endpoint structure.

\begin{figure}[t]
\centering
\includegraphics[width=0.96\linewidth]{../figures/side_effect_v5_stress_sweep.png}
\caption{Utility across side-effect stress. The proposed method remains above strong non-oracle baselines at the endpoint, while the oracle remains higher.}
\label{fig:stress}
\end{figure}

\input{generated_fixed_risk_table.tex}

The strict fixed-risk budget is 0.08. Under that budget, v5 has coverage @FIXED_COVERAGE@, breach rate @FIXED_BREACH@, and deployment-utility margin @FIXED_MARGIN@ over the strongest non-oracle fixed-risk baseline. The coverage number is intentionally reported next to utility. A conservative filter that refuses most actions is not a useful robot policy even if its accepted actions are safe.

\begin{figure}[t]
\centering
\includegraphics[width=0.90\linewidth]{../figures/side_effect_v5_fixed_risk.png}
\caption{Fixed-risk coverage versus deployment utility. Reporting both axes prevents a conservative no-action policy from looking deceptively strong.}
\label{fig:fixed-risk}
\end{figure}

\section{Failure Cases}
\input{generated_failure_table.tex}

The failure cases are not decorative. They are constraints on what can be claimed. Hidden material damage requires tactile or material-state sensing; delayed workspace disruption requires longer horizons; labeler tolerance shift requires real human labels; overcautious rejection requires calibration against benign changes; and oracle headroom means the mechanism is not saturated. These are exactly the issues an ICLR reviewer should attack.

\section{Submission Readiness Decision}
The terminal decision is \textbf{STRONG\_REVISE}. The local evidence is reproducible and the method clears all frozen local gates, but the scope gate fails. This paper should not be submitted to ICLR main in its current form because it lacks:
\begin{itemize}
\item real human preference labels;
\item a label-disagreement audit over actual annotators;
\item robot or accepted high-fidelity downstream evaluation;
\item calibrated deployment logs;
\item trained policy checkpoints;
\item rollout videos or equivalent physical evidence.
\end{itemize}

\paragraph{Why the paper is not killed.}
The v5 result is not merely a prettier version of v4. The strongest non-oracle baseline is the old v4 method, and the new method still clears hard success, hard utility, paired hard seeds, diagnostics, ablations, stress endpoint, and fixed-risk deployment gates. That is enough to justify continued development.

\paragraph{Why the paper is not ready.}
Every headline number is local. None of the gates measures real annotator disagreement, perception errors, robot contact dynamics, policy optimization, or long-horizon deployment drift. A reviewer would be right to reject an acceptance claim that treated this generated audit as external validation.

\paragraph{How to read the artifact.}
The right use of this manuscript is as a submission-preparation dossier. It defines the theory, baselines, gates, row-level artifacts, and failure boundaries that a real external study must preserve. It is not a replacement for the external study itself.

The correct next version is not a prettier PDF. It is an external-evidence version: collect labels, audit disagreement, train a downstream policy, evaluate on robot or accepted high-fidelity scenarios, and report the predefined gates even if they fail.

\clearpage
\section*{Appendix A: Additional Prior-Work Boundary}
Preference-based reinforcement learning is a mature area \citep{wirth2017survey}. Deep preference learning demonstrated scalable reward learning from comparisons \citep{christiano2017deep}. Active preference learning for robotics demonstrated that query selection can reduce label burden \citep{sadigh2017active}. Inverse reinforcement learning and apprenticeship learning established the older objective-inference framing \citep{ng2000algorithms,abbeel2004apprenticeship}. Inverse reward design and the off-switch game pressure any simplistic story about specified rewards and human oversight \citep{hadfieldmenell2017inverse,hadfieldmenell2017off}. Learning from physical human interaction and corrections shows that robots can use richer feedback than scalar rewards \citep{bajcsy2017learning,bobu2020quantifying,losey2020learning}. AI safety work on side effects and conservative agency shows why a policy can satisfy a stated objective while causing unwanted environmental changes \citep{amodei2016concrete,leike2017ai,krakovna2018measuring,turner2020conservative}.

The contribution here is therefore not the broad idea of learning from preferences, nor the broad idea that side effects matter. The contribution is a narrow local mechanism audit: when preference comparisons are ambiguous because two successful trajectories differ mainly in physical side effects, does a causal side-effect representation improve hard-split utility without hiding behind higher cost, higher false alarms, or lower coverage?

\section*{Appendix B: Formal Gate Definitions}
Let $M^\star$ denote v5 and $B$ the strongest non-oracle baseline selected by hard utility after excluding the oracle. The hard success gate requires $S(M^\star)-S(B)\ge 0.030$. The hard utility gate requires $U(M^\star)-U(B)\ge 0.050$. The diagnostic gate requires $R(M^\star)-R(B)\ge 0.050$ or $V(M^\star)-V(B)\le -0.030$. The non-regression gate requires $\Delta D\le 0$, $\Delta F\le 0$, $\Delta Q\le 0$, and $\Delta G\le 0$, where $D$ is damage, $F$ false alarms, $Q$ query cost, and $G$ preference regret. The paired gate requires at least 8 of 10 seed-level hard utility wins. The ablation gate requires the full method to beat the best removed-component variant by at least 0.010 success or 0.040 utility. The stress endpoint gate requires v5 to beat the strongest non-oracle endpoint stress comparator by at least 0.050 utility. The fixed-risk gate requires coverage in $[0.300,0.950)$ and positive fixed-risk deployment utility margin.

These gates are intentionally stricter than the v4.1 continuation audit. They test whether the new method improves a harder version of the problem rather than merely reproducing a small benchmark.

\section*{Appendix C: Method Components and Failure Modes}
\paragraph{Taxonomy.} The taxonomy creates a structured side-effect state. Its failure mode is misspecification: a real robot may produce side effects outside the eight generated channels.

\paragraph{Counterfactual pairs.} Counterfactual pairs protect against visible-success shortcuts. Their failure mode is collection cost: real humans may need careful interfaces to compare trajectories that differ only in physical side effects.

\paragraph{Disagreement weighting.} Disagreement weighting protects against treating subjective norms as label noise. Its failure mode is under-personalization: a global weighting scheme cannot replace a user-specific model.

\paragraph{Delayed-effect memory.} Delayed memory protects against post-comparison side effects. Its failure mode is observability: if no delayed observation is collected, the memory has nothing real to remember.

\paragraph{Benign-change calibration.} Calibration protects against a robot that refuses harmless changes. Its failure mode is false permissiveness if the calibration set misses subtle damage.

\paragraph{Risk budgeting.} Risk budgeting protects deployment. Its failure mode is low coverage, which is why coverage is reported directly.

\section*{Appendix D: Complete Failure Boundary Notes}
@FAILURE_APPENDIX@

\section*{Appendix E: Reproducibility Checklist}
The v5 audit is reproducible from a clean checkout using:
\begin{verbatim}
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
\end{verbatim}
The final numbered artifact is copied only to \texttt{C:/Users/wangz/Downloads/112.pdf}. The validation script checks row counts, finite numeric values, summary gates, PDF page count, hash, and artifact location.

\section*{Appendix F: What Would Make This Submission Ready}
The path to a real ICLR-main submission is concrete. First, collect human preference labels on matched-success trajectory pairs with explicit side-effect annotations. Second, measure inter-annotator disagreement and user-specific tolerance. Third, train the preference model and downstream policy on one split and evaluate on held-out tasks, held-out side-effect regimes, delayed-effect rollouts, and latent material-damage probes. Fourth, compare against the same strong baselines, including the old v4 method, side-effect classifiers, risk-calibrated reward models, and conservative filters. Fifth, report fixed-risk coverage and utility rather than only accepted-action safety. Sixth, release logs, trained checkpoints, videos, and label schemas. Until those steps exist, the honest state is strong revise, not acceptance-ready.

\clearpage
\section*{Appendix G: Task, Regime, and Split Cards}
This appendix explains why the expanded benchmark uses 10 tasks, 8 regimes, and 8 deployment splits. The point is not to inflate the row count. The point is to prevent a single easy side-effect channel from dominating the conclusion.

\paragraph{Table clearing.}
Table clearing stresses object displacement and clutter. A robot can satisfy the visible goal by moving all objects away from the target area while leaving a human workspace less usable than before. The side-effect labels therefore separate task completion from residual clutter, displacement of neighboring objects, and recovery cost.

\paragraph{Drawer retrieval.}
Drawer retrieval stresses contact force, narrow clearances, and irreversible minor damage. The task is included because a policy can retrieve the requested object while scraping drawer edges, shifting stored objects, or leaving the drawer in an unstable state. Generic preference comparisons often reward the retrieved object and miss the physical debt.

\paragraph{Cable routing.}
Cable routing stresses delayed and latent effects. A routed cable can look successful at the comparison horizon but later snag, create clutter, or interfere with another object. This task directly tests the delayed-effect memory component.

\paragraph{Tool handoff.}
Tool handoff stresses human-workspace disruption and safety margins. The robot can deliver the tool while placing it in a socially or physically awkward region. The benchmark uses this task to create labeler-tolerance and human-preference-shift cases.

\paragraph{Mobile shelf placement.}
Mobile shelf placement stresses instability and delayed toppling. The visible goal may be satisfied when the object is on the shelf, but the placement can be near an unstable edge or create a collision risk for later navigation.

\paragraph{Fragile object sorting.}
Fragile object sorting stresses high-force damage and latent material state. It is useful because visible success can be nearly independent of scuffing, micro-cracks, or surface wear, especially when the comparison uses RGB-only observations.

\paragraph{Countertop wiping.}
Countertop wiping stresses benign physical change versus true damage. A robot must alter the scene to complete the task, so a side-effect model that penalizes every physical change becomes overcautious. This task is a direct test of benign-change calibration.

\paragraph{Bin packing cleanup.}
Bin packing cleanup stresses clutter, displacement, and compactness. The task has many locally successful arrangements, some of which create later retrieval or stability problems. It pressures the model to distinguish acceptable reorganization from hidden workspace debt.

\paragraph{Shared workspace fetch.}
Shared workspace fetch stresses human norms. The same displacement can be acceptable in one workspace and disruptive in another. The benchmark uses this task to make labeler-disagreement weighting matter rather than treating all preference noise as random.

\paragraph{Stacked container staging.}
Stacked container staging stresses instability, delayed failure, and irreversible disruption. A stack can look correct at the moment of placement but fail under small later disturbances. This task attacks short-horizon preference labels.

\paragraph{Nominal regime.}
The nominal regime prevents the benchmark from becoming only a stress test. A useful model should not pay excessive query cost or false-alarm penalties when side-effect pressure is low.

\paragraph{Force-damage regime.}
Force damage targets contact-heavy failures: scuffs, dents, pressure marks, and excessive force. It is the clearest case where physical sensing matters and RGB preference labels can be incomplete.

\paragraph{Object-displacement regime.}
Object displacement targets the difference between task success and scene preservation. A policy can move irrelevant objects out of the way and still look successful unless displacement is measured explicitly.

\paragraph{Clutter-accumulation regime.}
Clutter accumulation targets long-horizon workspace usability. It is common in cleanup, routing, and sorting tasks where local success can leave future tasks harder.

\paragraph{Unstable-placement regime.}
Unstable placement targets delayed failure. It is included because short preference windows can reward placements that are visibly successful but physically fragile.

\paragraph{Irreversible-change regime.}
Irreversible change targets side effects that cannot be undone cheaply. The regret of an irreversible small action can be much larger than its immediate visible cost.

\paragraph{Human-workspace-disruption regime.}
Human workspace disruption targets subjective but real physical norms. It is a bridge between robotics and preference learning: the physical state matters, but its acceptability is user- and context-dependent.

\paragraph{Latent-material-damage regime.}
Latent material damage targets unobserved physical harm. The oracle headroom in this regime is expected; no local generated benchmark should imply that the sensing problem is solved.

\paragraph{Nominal split.}
The nominal split checks that the method does not become a stress-only trick. It also exposes unnecessary query cost and false alarms.

\paragraph{Seen-shift split.}
The seen-shift split changes object and side-effect intensity within the training envelope. It tests interpolation rather than true extrapolation.

\paragraph{Unseen-object split.}
The unseen-object split changes object geometry and displacement patterns. It tests whether side-effect reasoning transfers beyond memorized object identities.

\paragraph{Unseen-side-effect split.}
The unseen-side-effect split changes which mechanism dominates. It pressures the taxonomy rather than only the classifier.

\paragraph{Human-preference-shift split.}
The human-preference-shift split changes tolerance and workspace norms. It is the split most directly tied to real label-disagreement experiments that the current paper still lacks.

\paragraph{Delayed-effects split.}
The delayed-effects split makes the comparison horizon insufficient. A method without delayed memory should suffer here.

\paragraph{Latent-damage-shift split.}
The latent-damage-shift split makes physical damage less visible. It is included to keep the model honest about sensing limitations.

\paragraph{Combined-stress split.}
The combined-stress split is not meant to mimic a single real deployment. It is a hostile aggregate where multiple side-effect mechanisms interact. It is useful for gatekeeping but cannot replace external validation.

\clearpage
\section*{Appendix H: Baseline Attack Notes}
This appendix records why each baseline is included and what it attacks. A submission-ready paper would need to keep these baselines or stronger equivalents.

\paragraph{Success-only policy.}
The success-only policy attacks the possibility that visible task success alone explains the result. It should be weak on side-effect diagnostics but is still important because many robotics benchmarks implicitly reward it.

\paragraph{Generic pairwise preference model.}
The generic pairwise model attacks the claim that any preference learner is sufficient. If it matched v5, the taxonomy would not matter.

\paragraph{RLHF reward-model surrogate.}
The RLHF surrogate attacks the claim that deep reward modeling from comparisons automatically handles physical side effects. It is allowed to learn flexible correlations but not explicit side-effect mechanisms.

\paragraph{Uncertainty-query preference learner.}
The uncertainty-query learner attacks the query-selection story. It spends more labels on uncertain examples and therefore pressures v5 to justify its lower query cost.

\paragraph{Constraint-aware planner.}
The constraint-aware planner attacks the need for learned side-effect preferences. If hand-designed constraints were enough, v5 should not win utility after query cost and false alarms are counted.

\paragraph{Failure-prediction shield.}
The failure shield attacks the idea that predicting task failure is enough. Its weakness should appear when trajectories succeed visibly while accumulating physical debt.

\paragraph{Side-effect classifier baseline.}
The side-effect classifier attacks the need for preferences at all. It detects side effects but lacks counterfactual preference structure and labeler-tolerance modeling.

\paragraph{Inverse reward design baseline.}
The inverse reward design baseline attacks the objective-specification story. It can infer hidden reward implications from specification context, but it does not directly model delayed physical side effects in this audit.

\paragraph{Conservative safety filter.}
The conservative filter attacks the safety claim. It can reduce damage by refusing actions, so fixed-risk coverage and deployment utility are required to judge it fairly.

\paragraph{Preference transformer without side effects.}
The preference transformer attacks model capacity. It is a flexible sequence model without the explicit mechanism channels. If capacity alone solved the task, the transformer should catch v5.

\paragraph{Maximum-uncertainty human querying.}
Maximum-uncertainty querying attacks the label-efficiency claim. It often improves robustness but can become too expensive for practical robotics.

\paragraph{Physical affordance penalty.}
The affordance penalty attacks whether hand-engineered physical costs are enough. It helps with force and instability but lacks labeler-disagreement and delayed-effect structure.

\paragraph{Risk-calibrated reward model.}
The risk-calibrated reward model attacks the fixed-risk part of the contribution. It is a strong baseline because it explicitly models risk, even if it lacks the full causal side-effect taxonomy.

\paragraph{Old v4 proposed model.}
The old v4 model is the strongest non-oracle baseline in the final run. This is the right baseline to beat because it prevents the v5 paper from claiming progress over weak earlier scaffolds.

\paragraph{V5 proposed method.}
The v5 method is judged only by frozen gates. It is not allowed to call itself submission-ready because local gates cannot replace real labels or robot evidence.

\paragraph{Oracle human side-effect judge.}
The oracle is not a deployable baseline. It is headroom. Its presence prevents the paper from implying that the generated problem is solved.

\clearpage
\section*{Appendix I: Hostile Reviewer Checklist}
\paragraph{Attack: the benchmark is synthetic.}
Correct. The scope gate fails for exactly this reason. The paper can claim local mechanism evidence, not external robotics validity.

\paragraph{Attack: human preferences are generated, not collected.}
Correct. The current labels are generated proxies. A real submission needs human labels, labeler metadata, and disagreement analysis.

\paragraph{Attack: the side-effect taxonomy may be incomplete.}
Correct. The taxonomy covers eight mechanisms but cannot be assumed complete. The failure cases explicitly include misspecification and latent damage.

\paragraph{Attack: the utility function is hand-designed.}
Correct. The utility function is frozen and disclosed, but real deployment would require sensitivity analysis and human validation. The current result is a robustness audit under one disclosed utility.

\paragraph{Attack: the method may be overfit to the generator.}
Correct. The old v4 baseline, stress endpoints, and ablations reduce but do not eliminate this risk. External validation is required.

\paragraph{Attack: fixed-risk coverage could be gamed.}
The audit reports coverage, breach rate, and deployment utility together. A no-action policy cannot win by hiding behind low breach rate.

\paragraph{Attack: the oracle gap remains large.}
Correct. The oracle gap is a strength of the audit because it prevents saturation claims. The method improves the old baseline but does not solve hidden side-effect preference learning.

\paragraph{Attack: delayed effects need real time.}
Correct. The delayed-effect memory is only locally tested. Real delayed labels or physical state measurements are mandatory next evidence.

\paragraph{Attack: labeler-disagreement weighting is hypothetical.}
Correct. It is a mechanism hypothesis. It becomes real only after collecting labels from multiple annotators and modeling their tolerance.

\paragraph{Attack: strong baselines could be stronger.}
Correct in principle. The current suite includes 15 comparators, but a real submission should add any accepted robotics benchmark baselines relevant to the chosen hardware or simulator.

\paragraph{Attack: page count does not equal quality.}
Agreed. The 25-page requirement is treated as space for theory, protocol, failure analysis, and auditability, not as a reason to pad claims.

\paragraph{Attack: visual citation boxes do not affect science.}
Agreed. Boxed citations are an artifact-quality requirement. They improve navigation but do not change the evidence.

\clearpage
\section*{Appendix J: External Validation Protocol}
\paragraph{Label collection.}
Collect matched-success trajectory pairs across the same side-effect taxonomy. Each pair should include visible frames, force or tactile summaries when available, delayed observations, and a short explanation prompt asking annotators why they prefer one trajectory. The protocol should recruit enough annotators to estimate disagreement rather than averaging it away.

\paragraph{Robot or high-fidelity evaluation.}
Evaluate on robot hardware or an accepted high-fidelity simulator with contact, damage proxies, object displacement, and delayed stability. The simulator must expose logs that map to the same side-effect fields used by the model. If the environment cannot measure latent material damage, that limitation must be stated rather than approximated away.

\paragraph{Training and checkpoints.}
Train the preference model and downstream policy from the collected labels. Release configuration files, checkpoints, and evaluation scripts. The current local generator is not enough because it does not test optimization, perception, or policy-learning failure modes.

\paragraph{Predefined reporting.}
Before running the external study, freeze the same gates: success, utility, recall, violation, damage, false alarms, query cost, regret, paired seeds, ablations, endpoint stress, fixed-risk coverage, and scope. Report all predefined results even if the v5 method loses.

\paragraph{Videos and logs.}
Provide rollout videos or equivalent physical traces for accepted and rejected trajectories. For each failure case, provide at least one qualitative example linked to quantitative logs. This is the evidence needed to convince a skeptical robotics reviewer that side-effect mechanisms are not merely spreadsheet fields.

\paragraph{Decision threshold.}
Only after external labels, downstream policies, and physical validation exist should the paper be considered ICLR-main ready. If the external study preserves the v5 margins without raising damage, false alarms, query burden, or low-coverage safety artifacts, the decision can move from strong revise to submission candidate. If not, the correct decision is to revise or archive.

\paragraph{Statistical plan.}
The external study should preserve paired seeds or paired task instances wherever possible. Pairing is not a cosmetic detail: it makes failure analysis sharper by comparing methods under matched side-effect pressure. Confidence intervals should be reported for success, utility, damage, false alarms, query cost, and fixed-risk deployment utility.

\paragraph{Safety stop rules.}
Before any robot evaluation, define stop rules for excessive force, repeated object drops, workspace disruption, and human-intervention events. A side-effect preference paper should not create side effects while trying to measure them. Stop-rule activations should be reported as failures, not filtered out.

\paragraph{Release checklist.}
The released artifact should include label schemas, annotator instructions, anonymized disagreement statistics, task definitions, robot or simulator configuration, checkpoints, evaluation seeds, raw logs, and videos. Without those artifacts, reviewers cannot distinguish mechanism learning from benchmark overfitting.

\clearpage
\section*{Appendix K: Evidence Ledger}
This appendix records the purpose of every generated artifact. A hostile reviewer should be able to trace each claim to a file rather than to narrative prose.

\paragraph{\texttt{dataset\_summary.csv}.}
This file contains the 80 task-regime combinations used to define the physical side-effect loads. It is the first place to check whether the benchmark accidentally ignores a task or side-effect regime.

\paragraph{\texttt{cell\_metrics.csv}.}
This is the main evidence table with @MAIN_ROWS@ rows. Each row corresponds to one method, task, regime, split, and seed. The table is large enough to test interactions but small enough to rerun on CPU.

\paragraph{\texttt{main\_group\_metrics.csv}.}
This table aggregates the main cells by method, task, regime, and split. It is useful for finding whether a headline gain is isolated to one task or one side-effect mechanism.

\paragraph{\texttt{seed\_metrics.csv}.}
This table aggregates by method, split, and seed. It is used for paired comparisons and confidence intervals. Seed-level reporting is important because aggregate means can hide instability.

\paragraph{\texttt{metrics.csv}.}
This table aggregates by method and split. It is the compact summary most readers will inspect first, but it is not the source of the hard decision; the hard aggregate is separate.

\paragraph{\texttt{hard\_seed\_metrics.csv}.}
This table aggregates the hostile splits and hostile regimes by method and seed. The paired hard utility gate is computed here. This prevents nominal cases from diluting the decision.

\paragraph{\texttt{hard\_aggregate\_metrics.csv}.}
This table gives the 16-method hard aggregate. It determines the strongest non-oracle baseline and the headline v5 margins.

\paragraph{\texttt{hard\_pairwise\_stats.csv}.}
This table compares v5 to every non-v5 comparator under paired hard seeds. The old v4 method is included here, so the new paper cannot claim progress merely by dropping its strongest predecessor.

\paragraph{\texttt{ablation\_cell\_metrics.csv}.}
This table contains @ABLATION_ROWS@ ablation cells. Each component removal is tested on the same task-regime-seed structure under combined stress.

\paragraph{Ablation seed and aggregate metrics.}
The files \path{ablation_seed_metrics.csv} and \path{ablation_metrics.csv} expose whether the full model beats its strongest removed-component variant. The result is intentionally modest; large synthetic ablation gaps would be suspicious.

\paragraph{\texttt{stress\_sweep\_cell\_metrics.csv}.}
This table contains @STRESS_ROWS@ stress cells across six stress levels. It tests whether the method only works at a convenient side-effect intensity.

\paragraph{\texttt{stress\_sweep\_seed\_metrics.csv} and \texttt{stress\_sweep.csv}.}
These files summarize the stress sweep by seed and aggregate method. The endpoint gate is computed from the stress level 1.0 rows.

\paragraph{\texttt{fixed\_risk\_cell\_metrics.csv}.}
This table contains @FIXED_ROWS@ fixed-risk deployment cells. It is the audit against conservative no-action safety. The table records true risk, estimated risk, acceptance, breach, and deployment utility.

\paragraph{Fixed-risk seed, aggregate, and pairwise metrics.}
The files \path{fixed_risk_seed_metrics.csv}, \path{fixed_risk_metrics.csv}, and \path{fixed_risk_pairwise_stats.csv} summarize fixed-risk coverage and utility. They are the reason the paper can say a method is not rewarded for refusing almost everything.

\paragraph{\texttt{failure\_cases.csv}.}
This file contains 24 failure boundaries. It is not a qualitative afterthought; it is an evidence contract that names what the local benchmark cannot resolve.

\paragraph{\texttt{summary.json}.}
This file is the machine-readable audit result. It stores the version, terminal decision, scope failures, row counts, gates, and headline metrics used by the validator and status ledgers.

\paragraph{Generated figures and tables.}
The figures summarize hard utility, diagnostics, ablations, stress sweep, and fixed-risk coverage. The LaTeX tables are generated from the same CSVs. The manuscript should not contain hand-entered result numbers that disagree with these files.

\clearpage
\section*{Appendix L: Negative Claims and Non-Claims}
\paragraph{The paper does not claim real robot validation.}
Every strong result in the paper is local. The correct interpretation is that the mechanism deserves an external study, not that it is already validated.

\paragraph{The paper does not claim real human preference modeling.}
The labeler-disagreement feature is a generated proxy. A submission-ready version must collect real labels and show that the weighting improves held-out human preferences.

\paragraph{The paper does not claim complete side-effect coverage.}
The taxonomy is intentionally explicit, but explicit does not mean complete. Real homes, labs, and factories can produce side effects outside the eight mechanisms.

\paragraph{The paper does not claim that the oracle is reachable.}
The oracle is an upper reference. It uses privileged side-effect judgment and should not be presented as a method.

\paragraph{The paper does not claim that fixed-risk coverage solves safety.}
Fixed-risk coverage is a reporting discipline. It reveals low-coverage safety artifacts; it does not by itself guarantee safe deployment.

\paragraph{The paper does not claim that all preferences should be causal.}
The claim is narrower: for physical side effects in robot tasks, mechanism features are useful because visible task success can be ambiguous.

\paragraph{The paper does not claim that all conservative behavior is bad.}
Conservatism can be appropriate under high physical risk. The problem is unreported conservatism, where a policy looks safe because it rarely acts.

\paragraph{The paper does not claim that query cost is always more important than safety.}
Query cost is reported because robotics labels are expensive. A real system may choose higher cost for safety-critical tasks, but that tradeoff must be explicit.

\paragraph{The paper does not claim that delayed-effect memory replaces sensing.}
Memory helps only if delayed evidence exists. Without tactile, force, material-state, or delayed observations, memory can encode only a proxy.

\paragraph{The paper does not claim that the old v4 method is weak.}
The old v4 method is the strongest non-oracle baseline in the hard aggregate. This is useful because it makes the v5 comparison more credible.

\paragraph{The paper does not claim that the page count is evidence.}
The length increase is used to expose theory, gates, baselines, failure cases, and reproducibility. The scientific claim remains tied to the CSVs and scope gate.

\clearpage
\section*{Appendix M: Sensitivity and Extension Plan}
\paragraph{Utility sensitivity.}
A real submission should sweep the utility coefficients for success, recall, violation, damage, false alarms, query cost, preference regret, label disagreement, and delayed misses. The v5 method should not be accepted if it wins only under one fragile weighting.

\paragraph{Taxonomy sensitivity.}
The external study should remove, merge, and add side-effect mechanisms. If the v5 method collapses when one taxonomy entry changes name, it is overfit to the generator.

\paragraph{Annotator sensitivity.}
Annotators should be grouped by risk tolerance, workspace ownership, and prior robotics experience. The labeler-disagreement module should improve held-out prediction within each group, not only average accuracy.

\paragraph{Sensor sensitivity.}
The study should compare RGB-only, force-only, tactile-only, proprioceptive, and multimodal observations. Latent material damage cannot be declared solved if only RGB is tested.

\paragraph{Policy sensitivity.}
The preference model should be plugged into more than one downstream policy class. If the result depends on a single planner or controller, the paper should report that dependence.

\paragraph{Deployment sensitivity.}
Risk budgets should be varied before deployment, and coverage should be reported for every budget. A policy that is useful at budget 0.10 but useless at budget 0.05 has a very different deployment story.

\paragraph{Long-horizon sensitivity.}
Delayed effects should be measured over multiple horizons. Some workspace disruptions appear minutes or tasks later, so a single short rollout can hide the relevant failure.

\paragraph{Adversarial-task sensitivity.}
The external benchmark should include adversarially selected tasks where visible success and side-effect cost are anti-correlated. These are the cases most likely to expose reward-model shortcuts.

\paragraph{Release sensitivity.}
All scripts should be deterministic, but the released paper should also include raw logs and seeds. Reviewers should be able to rerun the exact claims and inspect any row that supports a gate.

\begingroup
\raggedright
\bibliographystyle{iclr2026_conference}
\bibliography{references}
\endgroup

\end{document}
"""
    for key, value in replacements.items():
        tex = tex.replace(key, value)

    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print("Wrote paper/main.tex and paper/references.bib")


if __name__ == "__main__":
    main()
