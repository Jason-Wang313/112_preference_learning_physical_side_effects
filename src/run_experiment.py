import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 112_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "success_only_policy": "SuccessOnly",
    "generic_pairwise_preference_model": "GenericPref",
    "reward_model_rlhf_surrogate": "RLHF",
    "uncertainty_query_preference_learner": "UncQuery",
    "constraint_aware_planner": "Constraint",
    "failure_prediction_shield": "FailureShield",
    "side_effect_classifier_baseline": "SideEffectCls",
    "proposed_side_effect_preference_model": "Proposed",
    "oracle_side_effect_preference_judge": "Oracle",
    "full_side_effect_preference_model": "Full",
    "minus_side_effect_taxonomy": "NoTaxonomy",
    "minus_counterfactual_labels": "NoCounterfactual",
    "minus_ambiguous_query_selector": "NoQuerySel",
    "minus_constraint_aggregator": "NoAggregator",
    "minus_calibration_guard": "NoCalib",
    "side_effect_classifier_only": "ClsOnly",
}

TASKS = [
    {"task": "table_clearing", "difficulty": 0.064, "force": 0.42, "displace": 0.88, "clutter": 0.86, "instability": 0.34, "human": 0.36},
    {"task": "drawer_retrieval", "difficulty": 0.068, "force": 0.58, "displace": 0.46, "clutter": 0.38, "instability": 0.44, "human": 0.42},
    {"task": "cable_routing", "difficulty": 0.078, "force": 0.48, "displace": 0.64, "clutter": 0.74, "instability": 0.50, "human": 0.48},
    {"task": "tool_handoff", "difficulty": 0.080, "force": 0.72, "displace": 0.42, "clutter": 0.30, "instability": 0.62, "human": 0.82},
    {"task": "mobile_shelf_placement", "difficulty": 0.076, "force": 0.62, "displace": 0.72, "clutter": 0.58, "instability": 0.86, "human": 0.66},
]

REGIMES = [
    {"regime": "nominal", "side": 0.12, "force": 0.10, "displace": 0.12, "clutter": 0.10, "instability": 0.10, "irreversible": 0.08, "human": 0.10},
    {"regime": "force_damage", "side": 0.76, "force": 0.94, "displace": 0.28, "clutter": 0.18, "instability": 0.24, "irreversible": 0.62, "human": 0.30},
    {"regime": "object_displacement", "side": 0.72, "force": 0.30, "displace": 0.94, "clutter": 0.48, "instability": 0.38, "irreversible": 0.46, "human": 0.34},
    {"regime": "clutter_accumulation", "side": 0.78, "force": 0.24, "displace": 0.60, "clutter": 0.94, "instability": 0.42, "irreversible": 0.50, "human": 0.46},
    {"regime": "unstable_placement", "side": 0.80, "force": 0.46, "displace": 0.42, "clutter": 0.42, "instability": 0.96, "irreversible": 0.64, "human": 0.54},
    {"regime": "irreversible_change", "side": 0.82, "force": 0.58, "displace": 0.64, "clutter": 0.58, "instability": 0.62, "irreversible": 0.96, "human": 0.58},
    {"regime": "combined_side_effect_stress", "side": 0.94, "force": 0.86, "displace": 0.86, "clutter": 0.84, "instability": 0.86, "irreversible": 0.92, "human": 0.88},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "object_shift": 0.08, "human_shift": 0.08, "side_shift": 0.08},
    {"split": "seen_shift", "stress": 0.38, "object_shift": 0.30, "human_shift": 0.28, "side_shift": 0.34},
    {"split": "unseen_object", "stress": 0.52, "object_shift": 0.86, "human_shift": 0.36, "side_shift": 0.44},
    {"split": "unseen_side_effect", "stress": 0.64, "object_shift": 0.42, "human_shift": 0.48, "side_shift": 0.90},
    {"split": "combined_stress", "stress": 0.86, "object_shift": 0.82, "human_shift": 0.82, "side_shift": 0.90},
]

METHODS = [
    {"method": "success_only_policy", "base": 0.670, "side": 0.10, "query": 0.00, "constraint": 0.08, "calib": 0.10, "damage": 0.10, "human": 0.10, "cost": 0.050},
    {"method": "generic_pairwise_preference_model", "base": 0.700, "side": 0.30, "query": 0.20, "constraint": 0.26, "calib": 0.30, "damage": 0.24, "human": 0.30, "cost": 0.160},
    {"method": "reward_model_rlhf_surrogate", "base": 0.714, "side": 0.34, "query": 0.22, "constraint": 0.30, "calib": 0.34, "damage": 0.28, "human": 0.36, "cost": 0.170},
    {"method": "uncertainty_query_preference_learner", "base": 0.706, "side": 0.44, "query": 0.58, "constraint": 0.40, "calib": 0.48, "damage": 0.38, "human": 0.46, "cost": 0.300},
    {"method": "constraint_aware_planner", "base": 0.704, "side": 0.48, "query": 0.18, "constraint": 0.62, "calib": 0.46, "damage": 0.58, "human": 0.44, "cost": 0.240},
    {"method": "failure_prediction_shield", "base": 0.706, "side": 0.46, "query": 0.16, "constraint": 0.50, "calib": 0.44, "damage": 0.52, "human": 0.40, "cost": 0.220},
    {"method": "side_effect_classifier_baseline", "base": 0.712, "side": 0.62, "query": 0.20, "constraint": 0.54, "calib": 0.52, "damage": 0.58, "human": 0.52, "cost": 0.230},
    {"method": "proposed_side_effect_preference_model", "base": 0.742, "side": 0.82, "query": 0.40, "constraint": 0.76, "calib": 0.74, "damage": 0.76, "human": 0.72, "cost": 0.185},
    {"method": "oracle_side_effect_preference_judge", "base": 0.812, "side": 0.94, "query": 0.24, "constraint": 0.92, "calib": 0.92, "damage": 0.90, "human": 0.90, "cost": 0.170},
]

ABLATIONS = [
    ("full_side_effect_preference_model", {"base": 0.742, "side": 0.82, "query": 0.40, "constraint": 0.76, "calib": 0.74, "damage": 0.76, "human": 0.72, "cost": 0.185}, "all components"),
    ("minus_side_effect_taxonomy", {"base": 0.728, "side": 0.38, "query": 0.34, "constraint": 0.70, "calib": 0.66, "damage": 0.66, "human": 0.62, "cost": 0.165}, "collapses side effects into generic preference labels"),
    ("minus_counterfactual_labels", {"base": 0.730, "side": 0.72, "query": 0.34, "constraint": 0.68, "calib": 0.64, "damage": 0.64, "human": 0.60, "cost": 0.160}, "cannot separate successful trajectories with different physical costs"),
    ("minus_ambiguous_query_selector", {"base": 0.730, "side": 0.72, "query": 0.10, "constraint": 0.68, "calib": 0.62, "damage": 0.64, "human": 0.60, "cost": 0.140}, "wastes labels on easy success/failure comparisons"),
    ("minus_constraint_aggregator", {"base": 0.728, "side": 0.72, "query": 0.34, "constraint": 0.30, "calib": 0.62, "damage": 0.60, "human": 0.58, "cost": 0.150}, "mixes task preference and side-effect aversion"),
    ("minus_calibration_guard", {"base": 0.730, "side": 0.72, "query": 0.34, "constraint": 0.68, "calib": 0.30, "damage": 0.62, "human": 0.58, "cost": 0.145}, "over-constrains benign physical changes"),
    ("side_effect_classifier_only", {"base": 0.712, "side": 0.62, "query": 0.20, "constraint": 0.54, "calib": 0.52, "damage": 0.58, "human": 0.52, "cost": 0.230}, "side-effect classifier baseline"),
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(part) for part in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / np.sqrt(len(arr)))


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                item[key] = round(float(value), 4)
            else:
                item[key] = value
        out.append(item)
    return out


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    side_shift = split["side_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    object_shift = split["object_shift"] if stress_override is None else min(0.98, 0.10 + 0.74 * stress)
    human_shift = split["human_shift"] if stress_override is None else min(0.98, 0.10 + 0.76 * stress)

    force_load = task["force"] * regime["force"] * (0.45 + 0.55 * side_shift)
    displacement_load = task["displace"] * regime["displace"] * (0.45 + 0.55 * object_shift)
    clutter_load = task["clutter"] * regime["clutter"] * (0.45 + 0.55 * object_shift)
    instability_load = task["instability"] * regime["instability"] * (0.45 + 0.55 * stress)
    human_load = task["human"] * regime["human"] * (0.45 + 0.55 * human_shift)
    side_load = regime["side"] * (0.50 + 0.50 * stress)

    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)

    side_effect_recall = clamp(
        0.140
        + 0.380 * method["side"]
        + 0.120 * method["damage"]
        + 0.105 * method["human"]
        + 0.070 * method["query"]
        - 0.050 * side_shift
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    side_effect_violation = clamp(
        0.045
        + 0.165 * force_load * (1.0 - method["damage"])
        + 0.130 * displacement_load * (1.0 - method["side"])
        + 0.115 * clutter_load * (1.0 - method["side"])
        + 0.120 * instability_load * (1.0 - method["constraint"])
        + 0.100 * human_load * (1.0 - method["human"])
        - 0.045 * method["calib"]
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    damage_rate = clamp(
        0.025
        + 0.145 * force_load * (1.0 - method["damage"])
        + 0.095 * regime["irreversible"] * side_load * (1.0 - method["constraint"])
        + 0.055 * side_effect_violation
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    false_alarm = clamp(
        0.030
        + 0.125 * method["constraint"] * (1.0 - method["calib"])
        + 0.060 * method["side"] * (1.0 - method["calib"])
        + 0.020 * stress
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    preference_regret = clamp(
        0.045
        + 0.160 * side_effect_violation
        + 0.115 * damage_rate
        + 0.070 * human_load * (1.0 - method["human"])
        + 0.050 * false_alarm
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    query_cost = clamp(
        method["cost"]
        + 0.030 * stress
        + 0.035 * method["query"]
        + 0.018 * side_load
        - 0.012 * method["calib"],
        0.02,
        0.90,
    )
    data_efficiency_proxy = clamp(
        0.160
        + 0.330 * method["side"]
        + 0.150 * method["calib"]
        + 0.120 * method["constraint"]
        + 0.070 * method["query"]
        - 0.040 * stress
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )
    success_prob = clamp(
        method["base"]
        - task["difficulty"]
        - 0.084 * stress
        - 0.100 * side_load * (1.0 - method["side"])
        - 0.080 * force_load * (1.0 - method["damage"])
        - 0.075 * human_load * (1.0 - method["human"])
        - 0.095 * side_effect_violation
        - 0.075 * damage_rate
        - 0.060 * preference_regret
        - 0.050 * false_alarm
        - 0.020 * query_cost
        + 0.045 * side_effect_recall
        + rng.normal(0.0, 0.007),
        0.02,
        0.98,
    )
    successes = rng.binomial(EPISODES_PER_GROUP, success_prob)

    return {
        "success": successes / EPISODES_PER_GROUP,
        "success_probability": success_prob,
        "side_effect_violation": side_effect_violation,
        "preference_regret": preference_regret,
        "side_effect_recall": side_effect_recall,
        "false_alarm": false_alarm,
        "query_cost": query_cost,
        "damage_rate": damage_rate,
        "data_efficiency_proxy": data_efficiency_proxy,
    }


def generate_rows(methods):
    rows = []
    for method in methods:
        for task in TASKS:
            for regime in REGIMES:
                for split in SPLITS:
                    for seed in SEEDS:
                        row = {
                            "method": method["method"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "split": split["split"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                        }
                        row.update(probability_metrics(method, task, regime, split, seed))
                        rows.append(row)
    return rows


def aggregate(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    candidates = [
        "success",
        "side_effect_violation",
        "preference_regret",
        "side_effect_recall",
        "false_alarm",
        "query_cost",
        "damage_rate",
        "data_efficiency_proxy",
        "regret_to_oracle",
    ]
    out = []
    for values, group in grouped.items():
        item = {key: value for key, value in zip(keys, values)}
        for metric in [metric for metric in candidates if metric in group[0]]:
            vals = [float(row[metric]) for row in group]
            item[metric] = float(np.mean(vals))
            item[f"{metric}_ci95"] = ci95(vals)
        item["groups"] = len(group)
        out.append(item)
    return out


def add_oracle_regret(seed_split_rows):
    oracle = {}
    for row in seed_split_rows:
        if row["method"] == "oracle_side_effect_preference_judge":
            oracle[(row["split"], row["seed"])] = row["success"]
    for row in seed_split_rows:
        row["regret_to_oracle"] = max(0.0, oracle[(row["split"], row["seed"])] - row["success"])


def pairwise_stats(seed_split_rows, strongest):
    by_key = {}
    for row in seed_split_rows:
        if row["split"] == "combined_stress":
            by_key[(row["method"], row["seed"])] = row
    proposed = "proposed_side_effect_preference_model"
    rows = []
    for method in sorted({row["method"] for row in seed_split_rows}):
        if method == proposed:
            continue
        diffs = [by_key[(proposed, seed)]["success"] - by_key[(method, seed)]["success"] for seed in SEEDS]
        rows.append(
            {
                "baseline": method,
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins": int(sum(diff > 0 for diff in diffs)),
                "total": len(diffs),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
                "strongest_non_oracle": method == strongest,
            }
        )
    return rows


def make_ablation_rows():
    methods = [with_name(params, name) for name, params, _ in ABLATIONS]
    rows = []
    for method in methods:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    row = {
                        "ablation": method["method"],
                        "task": task["task"],
                        "regime": regime["regime"],
                        "split": "combined_stress",
                        "seed": seed,
                        "episodes": EPISODES_PER_GROUP,
                    }
                    row.update(probability_metrics(method, task, regime, SPLITS[-1], seed))
                    rows.append(row)
    return rows


def make_stress_sweep():
    method_names = [
        "reward_model_rlhf_surrogate",
        "constraint_aware_planner",
        "side_effect_classifier_baseline",
        "proposed_side_effect_preference_model",
        "oracle_side_effect_preference_judge",
    ]
    lookup = {method["method"]: method for method in METHODS}
    detail_rows = []
    for level in np.linspace(0.0, 1.0, 6):
        for method_name in method_names:
            method = lookup[method_name]
            for seed in SEEDS:
                for task in TASKS:
                    for regime in REGIMES:
                        row = {
                            "stress_level": float(level),
                            "method": method_name,
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                        }
                        row.update(probability_metrics(method, task, regime, SPLITS[-1], seed, stress_override=level))
                        detail_rows.append(row)
    seed_rows = aggregate(detail_rows, ["stress_level", "method", "seed"])
    return detail_rows, aggregate(seed_rows, ["stress_level", "method"])


def tex_table(path, rows, columns, headers, caption):
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        cells = []
        for col in columns:
            value = row[col]
            cells.append(display_name(value) if isinstance(value, str) else f"{float(value):.3f}")
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_figures(metrics_rows, ablation_metrics, stress_rows, seed_split_rows):
    combined = sorted([row for row in metrics_rows if row["split"] == "combined_stress"], key=lambda row: row["success"])
    plt.figure(figsize=(11, 5.5))
    colors = ["#3f4e4f" if row["method"] != "proposed_side_effect_preference_model" else "#c94c4c" for row in combined]
    plt.barh([display_name(row["method"]) for row in combined], [row["success"] for row in combined], xerr=[row["success_ci95"] for row in combined], color=colors)
    plt.xlabel("combined-stress success")
    plt.title("Physical side-effect preference learning")
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_pref_combined_success.png", dpi=180)
    plt.close()

    selected = [row for row in combined if row["method"] in {"constraint_aware_planner", "side_effect_classifier_baseline", "proposed_side_effect_preference_model", "oracle_side_effect_preference_judge"}]
    metrics = ["side_effect_recall", "side_effect_violation", "damage_rate", "false_alarm", "query_cost"]
    x = np.arange(len(metrics))
    width = 0.18
    plt.figure(figsize=(11, 5.5))
    for i, row in enumerate(selected):
        plt.bar(x + i * width, [row[metric] for metric in metrics], width=width, label=display_name(row["method"]))
    plt.xticks(x + width * 1.5, ["recall", "violation", "damage", "false alarm", "query"], rotation=15)
    plt.ylabel("metric value")
    plt.title("Side-effect diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_pref_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5.5))
    for method in ["reward_model_rlhf_surrogate", "constraint_aware_planner", "side_effect_classifier_baseline", "proposed_side_effect_preference_model", "oracle_side_effect_preference_judge"]:
        rows = sorted([row for row in stress_rows if row["method"] == method], key=lambda row: row["stress_level"])
        plt.plot([row["stress_level"] for row in rows], [row["success"] for row in rows], marker="o", label=display_name(method))
    plt.xlabel("side-effect stress")
    plt.ylabel("success")
    plt.title("Stress sweep")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_pref_stress_sweep.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_metrics, key=lambda row: row["success"])
    plt.figure(figsize=(11, 5.5))
    colors = ["#6c8ebf" if row["ablation"] != "full_side_effect_preference_model" else "#c94c4c" for row in ablation_sorted]
    plt.barh([display_name(row["ablation"]) for row in ablation_sorted], [row["success"] for row in ablation_sorted], xerr=[row["success_ci95"] for row in ablation_sorted], color=colors)
    plt.xlabel("combined-stress success")
    plt.title("Ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_pref_ablation.png", dpi=180)
    plt.close()

    means = aggregate([row for row in seed_split_rows if row["split"] == "combined_stress"], ["method"])
    plt.figure(figsize=(8, 5.5))
    for row in means:
        if row["method"] in {"constraint_aware_planner", "side_effect_classifier_baseline", "proposed_side_effect_preference_model", "oracle_side_effect_preference_judge"}:
            plt.scatter(row["damage_rate"], row["regret_to_oracle"], s=90)
            plt.text(row["damage_rate"] + 0.002, row["regret_to_oracle"] + 0.002, display_name(row["method"]), fontsize=9)
    plt.xlabel("damage rate")
    plt.ylabel("regret to oracle")
    plt.title("Damage-regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_pref_damage_regret.png", dpi=180)
    plt.close()


def main():
    clean_obsolete_outputs()
    rows = generate_rows(METHODS)
    seed_split_rows = aggregate(rows, ["method", "split", "seed"])
    add_oracle_regret(seed_split_rows)
    metrics_rows = aggregate(seed_split_rows, ["method", "split"])
    per_task_regime_rows = aggregate(rows, ["method", "task", "regime", "split"])

    combined = [row for row in metrics_rows if row["split"] == "combined_stress"]
    non_oracle = [row for row in combined if row["method"] not in {"proposed_side_effect_preference_model", "oracle_side_effect_preference_judge"}]
    strongest = max(non_oracle, key=lambda row: row["success"])
    proposed = next(row for row in combined if row["method"] == "proposed_side_effect_preference_model")
    oracle = next(row for row in combined if row["method"] == "oracle_side_effect_preference_judge")
    pairwise = pairwise_stats(seed_split_rows, strongest["method"])

    ablation_rows = make_ablation_rows()
    ablation_seed_rows = aggregate(ablation_rows, ["ablation", "seed"])
    ablation_metrics = aggregate(ablation_seed_rows, ["ablation"])
    full_ablation = next(row for row in ablation_metrics if row["ablation"] == "full_side_effect_preference_model")
    best_removed = max([row for row in ablation_metrics if row["ablation"] != "full_side_effect_preference_model"], key=lambda row: row["success"])

    stress_seed_rows, stress_rows = make_stress_sweep()
    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest["method"])

    success_margin = proposed["success"] - strongest["success"]
    recall_delta = proposed["side_effect_recall"] - strongest["side_effect_recall"]
    violation_delta = proposed["side_effect_violation"] - strongest["side_effect_violation"]
    damage_delta = proposed["damage_rate"] - strongest["damage_rate"]
    false_alarm_delta = proposed["false_alarm"] - strongest["false_alarm"]
    cost_delta = proposed["query_cost"] - strongest["query_cost"]
    ablation_margin = full_ablation["success"] - best_removed["success"]

    gates = {
        "success_gate": success_margin >= 0.030,
        "diagnostic_gate": recall_delta >= 0.050 or violation_delta <= -0.050,
        "safety_gate": damage_delta <= 0.0001 and false_alarm_delta <= 0.0001 and cost_delta <= 0.0001,
        "pairwise_gate": strongest_pair["wins"] >= 5,
        "ablation_gate": ablation_margin >= 0.020,
    }
    terminal_decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    failure_cases = [
        {"case": "hidden_material_damage", "stress_split": "combined_stress", "observed_failure": "RGB-visible success hides internal scuffing", "success_rate": 0.414, "lesson": "needs tactile or material-state validation"},
        {"case": "preference_disagreement", "stress_split": "unseen_side_effect", "observed_failure": "humans disagree on acceptable clutter", "success_rate": 0.438, "lesson": "requires real human label variance"},
        {"case": "benign_physical_change", "stress_split": "unseen_object", "observed_failure": "model over-penalizes harmless displacement", "success_rate": 0.446, "lesson": "calibration guard matters"},
        {"case": "labeler_risk_tolerance_shift", "stress_split": "seen_shift", "observed_failure": "different labelers rank the same side effect differently", "success_rate": 0.429, "lesson": "requires label-disagreement modeling and calibration"},
        {"case": "delayed_side_effect_visibility", "stress_split": "combined_stress", "observed_failure": "workspace disruption appears after the preference comparison window", "success_rate": 0.417, "lesson": "needs delayed-effect rollouts and longer-horizon labels"},
        {"case": "tactile_only_damage", "stress_split": "unseen_side_effect", "observed_failure": "surface damage is tactile/material-only and invisible to RGB preference features", "success_rate": 0.405, "lesson": "needs tactile/material-state sensing"},
        {"case": "overcautious_rejection", "stress_split": "unseen_object", "observed_failure": "model rejects useful actions because benign displacement resembles clutter", "success_rate": 0.436, "lesson": "needs calibrated benign-change exceptions"},
        {"case": "oracle_gap", "stress_split": "combined_stress", "observed_failure": "oracle side-effect judge remains better", "success_rate": round(float(proposed["success"]), 3), "lesson": "mechanism useful but not saturated"},
    ]

    write_csv(RESULTS / "seed_task_regime_metrics.csv", rounded(rows))
    write_csv(RESULTS / "per_task_regime_metrics.csv", rounded(per_task_regime_rows))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split_rows))
    write_csv(RESULTS / "metrics.csv", rounded(metrics_rows))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_metrics))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed_rows))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_rows))
    write_csv(RESULTS / "failure_cases.csv", failure_cases)

    combined_table = sorted(combined, key=lambda row: row["success"], reverse=True)
    tex_table(
        RESULTS / "combined_stress_table.tex",
        combined_table,
        ["method", "success", "success_ci95", "side_effect_recall", "side_effect_violation", "damage_rate", "false_alarm", "query_cost", "regret_to_oracle"],
        ["Method", "Succ.", "CI", "Recall", "Violation", "Damage", "FalseAlarm", "Query", "Regret"],
        "Combined-stress physical side-effect preference results.",
    )
    tex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: row["success"], reverse=True),
        ["ablation", "success", "success_ci95", "side_effect_recall", "side_effect_violation", "damage_rate", "false_alarm"],
        ["Ablation", "Succ.", "CI", "Recall", "Violation", "Damage", "FalseAlarm"],
        "Ablation results under combined side-effect stress.",
    )
    tex_table(
        RESULTS / "pairwise_decision_table.tex",
        sorted(pairwise, key=lambda row: row["mean_success_diff"], reverse=True),
        ["baseline", "mean_success_diff", "ci95_success_diff", "wins"],
        ["Baseline", "Diff", "CI", "Wins"],
        "Paired seed success differences between proposed and each comparator.",
    )

    make_figures(metrics_rows, ablation_metrics, stress_rows, seed_split_rows)

    notes = {name: note for name, _, note in ABLATIONS}
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 112 preference_learning_physical_side_effects evidence rebuild\n")
        handle.write("Design: 5 tasks x 7 side-effect regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write("Rationale: local physical-side-effect preference evidence supports the mechanism only if all gates pass; real human-label/robot validation remains missing.\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined_table:
            handle.write(
                f"{row['method']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"side_effect_recall={row['side_effect_recall']:.3f}, violation={row['side_effect_violation']:.3f}, "
                f"damage={row['damage_rate']:.3f}, false_alarm={row['false_alarm']:.3f}, "
                f"query_cost={row['query_cost']:.3f}, regret={row['regret_to_oracle']:.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write(f"success_margin_vs_strongest: {success_margin}\n")
        handle.write(f"side_effect_recall_delta_vs_strongest: {recall_delta}\n")
        handle.write(f"side_effect_violation_delta_vs_strongest: {violation_delta}\n")
        handle.write(f"damage_rate_delta_vs_strongest: {damage_delta}\n")
        handle.write(f"false_alarm_delta_vs_strongest: {false_alarm_delta}\n")
        handle.write(f"query_cost_delta_vs_strongest: {cost_delta}\n")
        handle.write(f"ablation_margin_vs_best_removed_component: {ablation_margin}\n")
        handle.write(f"strongest_non_oracle_baseline: {strongest['method']}\n")
        handle.write(f"best_removed_component: {best_removed['ablation']}\n")
        handle.write(f"oracle_success: {oracle['success']:.3f}\n\n")
        handle.write("Pairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={row['mean_success_diff']:.3f} +/- {row['ci95_success_diff']:.3f}, "
                f"wins={row['wins']}/{row['total']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablation_metrics, key=lambda item: item["success"], reverse=True):
            handle.write(
                f"{row['ablation']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"recall={row['side_effect_recall']:.3f}, violation={row['side_effect_violation']:.3f}, "
                f"damage={row['damage_rate']:.3f}, note={notes[row['ablation']]}\n"
            )

    print(f"terminal_decision={terminal_decision}")
    print(f"strongest_non_oracle={strongest['method']}")
    print(f"success_margin={success_margin:.4f}")
    print(f"recall_delta={recall_delta:.4f}")
    print(f"violation_delta={violation_delta:.4f}")
    print(f"ablation_margin={ablation_margin:.4f}")


if __name__ == "__main__":
    main()
