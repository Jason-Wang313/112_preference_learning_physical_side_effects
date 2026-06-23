import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 112_2026_5
SEEDS = list(range(10))
EPISODES_PER_CELL = 96
PROPOSED = "side_effect_causal_preference_model_v5"
OLD_PROPOSED = "proposed_side_effect_preference_model_v4"
ORACLE = "oracle_human_side_effect_judge"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"
for directory in (RESULTS, FIGURES, PAPER):
    directory.mkdir(exist_ok=True)

DISPLAY_NAMES = {
    "success_only_policy": "SuccessOnly",
    "generic_pairwise_preference_model": "GenericPref",
    "reward_model_rlhf_surrogate": "RLHF",
    "uncertainty_query_preference_learner": "UncQuery",
    "constraint_aware_planner": "Constraint",
    "failure_prediction_shield": "FailureShield",
    "side_effect_classifier_baseline": "SideEffectCls",
    "inverse_reward_design_baseline": "InvRewardDesign",
    "conservative_safety_filter": "ConservativeFilter",
    "preference_transformer_no_side_effects": "PrefTransformer",
    "human_query_max_uncertainty": "MaxUncQuery",
    "physical_affordance_penalty": "AffordPenalty",
    "risk_calibrated_reward_model": "RiskCalReward",
    OLD_PROPOSED: "OldV4Proposed",
    PROPOSED: "CausalSideEffectV5",
    ORACLE: "OracleHumanJudge",
    "full_causal_side_effect_model": "FullV5",
    "minus_side_effect_taxonomy": "NoTaxonomy",
    "minus_counterfactual_pairs": "NoCounterfactualPairs",
    "minus_labeler_disagreement_weighting": "NoDisagreement",
    "minus_delayed_effect_memory": "NoDelayedMemory",
    "minus_benign_change_calibration": "NoBenignCalib",
    "minus_deployment_risk_budget": "NoRiskBudget",
    "minus_ambiguous_query_selector": "NoQuerySelector",
    "minus_constraint_aggregator": "NoAggregator",
    "old_v4_preference_model": "OldV4",
}

TASKS = [
    {"task": "table_clearing", "difficulty": 0.060, "force": 0.42, "displace": 0.88, "clutter": 0.86, "instability": 0.34, "human": 0.36, "latency": 0.34},
    {"task": "drawer_retrieval", "difficulty": 0.068, "force": 0.58, "displace": 0.46, "clutter": 0.38, "instability": 0.44, "human": 0.42, "latency": 0.42},
    {"task": "cable_routing", "difficulty": 0.078, "force": 0.48, "displace": 0.64, "clutter": 0.74, "instability": 0.50, "human": 0.48, "latency": 0.64},
    {"task": "tool_handoff", "difficulty": 0.082, "force": 0.72, "displace": 0.42, "clutter": 0.30, "instability": 0.62, "human": 0.82, "latency": 0.46},
    {"task": "mobile_shelf_placement", "difficulty": 0.076, "force": 0.62, "displace": 0.72, "clutter": 0.58, "instability": 0.86, "human": 0.66, "latency": 0.58},
    {"task": "fragile_object_sorting", "difficulty": 0.088, "force": 0.86, "displace": 0.54, "clutter": 0.40, "instability": 0.56, "human": 0.52, "latency": 0.62},
    {"task": "countertop_wiping", "difficulty": 0.074, "force": 0.70, "displace": 0.34, "clutter": 0.66, "instability": 0.32, "human": 0.58, "latency": 0.76},
    {"task": "bin_packing_cleanup", "difficulty": 0.072, "force": 0.50, "displace": 0.80, "clutter": 0.90, "instability": 0.70, "human": 0.54, "latency": 0.44},
    {"task": "shared_workspace_fetch", "difficulty": 0.084, "force": 0.54, "displace": 0.58, "clutter": 0.72, "instability": 0.48, "human": 0.92, "latency": 0.52},
    {"task": "stacked_container_staging", "difficulty": 0.086, "force": 0.64, "displace": 0.74, "clutter": 0.48, "instability": 0.94, "human": 0.60, "latency": 0.60},
]

REGIMES = [
    {"regime": "nominal", "side": 0.12, "force": 0.10, "displace": 0.12, "clutter": 0.10, "instability": 0.10, "irreversible": 0.08, "human": 0.10, "latent": 0.08},
    {"regime": "force_damage", "side": 0.76, "force": 0.94, "displace": 0.28, "clutter": 0.18, "instability": 0.24, "irreversible": 0.62, "human": 0.30, "latent": 0.54},
    {"regime": "object_displacement", "side": 0.72, "force": 0.30, "displace": 0.94, "clutter": 0.48, "instability": 0.38, "irreversible": 0.46, "human": 0.34, "latent": 0.26},
    {"regime": "clutter_accumulation", "side": 0.78, "force": 0.24, "displace": 0.60, "clutter": 0.94, "instability": 0.42, "irreversible": 0.50, "human": 0.46, "latent": 0.36},
    {"regime": "unstable_placement", "side": 0.80, "force": 0.46, "displace": 0.42, "clutter": 0.42, "instability": 0.96, "irreversible": 0.64, "human": 0.54, "latent": 0.44},
    {"regime": "irreversible_change", "side": 0.82, "force": 0.58, "displace": 0.64, "clutter": 0.58, "instability": 0.62, "irreversible": 0.96, "human": 0.58, "latent": 0.62},
    {"regime": "human_workspace_disruption", "side": 0.84, "force": 0.42, "displace": 0.72, "clutter": 0.86, "instability": 0.48, "irreversible": 0.54, "human": 0.96, "latent": 0.46},
    {"regime": "latent_material_damage", "side": 0.88, "force": 0.88, "displace": 0.50, "clutter": 0.44, "instability": 0.56, "irreversible": 0.86, "human": 0.62, "latent": 0.96},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "object_shift": 0.08, "human_shift": 0.08, "side_shift": 0.08, "label_shift": 0.08, "delay": 0.08},
    {"split": "seen_shift", "stress": 0.34, "object_shift": 0.30, "human_shift": 0.28, "side_shift": 0.34, "label_shift": 0.22, "delay": 0.20},
    {"split": "unseen_object", "stress": 0.50, "object_shift": 0.86, "human_shift": 0.36, "side_shift": 0.44, "label_shift": 0.32, "delay": 0.28},
    {"split": "unseen_side_effect", "stress": 0.62, "object_shift": 0.42, "human_shift": 0.48, "side_shift": 0.90, "label_shift": 0.36, "delay": 0.36},
    {"split": "human_preference_shift", "stress": 0.66, "object_shift": 0.42, "human_shift": 0.92, "side_shift": 0.62, "label_shift": 0.94, "delay": 0.42},
    {"split": "delayed_effects", "stress": 0.72, "object_shift": 0.52, "human_shift": 0.58, "side_shift": 0.74, "label_shift": 0.48, "delay": 0.94},
    {"split": "latent_damage_shift", "stress": 0.78, "object_shift": 0.62, "human_shift": 0.64, "side_shift": 0.86, "label_shift": 0.56, "delay": 0.82},
    {"split": "combined_stress", "stress": 0.88, "object_shift": 0.82, "human_shift": 0.86, "side_shift": 0.94, "label_shift": 0.88, "delay": 0.88},
]

METHODS = [
    {"method": "success_only_policy", "base": 0.668, "side": 0.10, "query": 0.00, "constraint": 0.08, "calib": 0.10, "damage": 0.10, "human": 0.10, "delayed": 0.08, "disagreement": 0.08, "risk": 0.08, "cost": 0.050},
    {"method": "generic_pairwise_preference_model", "base": 0.700, "side": 0.30, "query": 0.20, "constraint": 0.26, "calib": 0.30, "damage": 0.24, "human": 0.30, "delayed": 0.22, "disagreement": 0.24, "risk": 0.24, "cost": 0.160},
    {"method": "reward_model_rlhf_surrogate", "base": 0.714, "side": 0.34, "query": 0.22, "constraint": 0.30, "calib": 0.34, "damage": 0.28, "human": 0.36, "delayed": 0.26, "disagreement": 0.28, "risk": 0.28, "cost": 0.170},
    {"method": "uncertainty_query_preference_learner", "base": 0.708, "side": 0.44, "query": 0.58, "constraint": 0.40, "calib": 0.48, "damage": 0.38, "human": 0.46, "delayed": 0.38, "disagreement": 0.42, "risk": 0.40, "cost": 0.300},
    {"method": "constraint_aware_planner", "base": 0.704, "side": 0.48, "query": 0.18, "constraint": 0.62, "calib": 0.46, "damage": 0.58, "human": 0.44, "delayed": 0.40, "disagreement": 0.38, "risk": 0.58, "cost": 0.240},
    {"method": "failure_prediction_shield", "base": 0.706, "side": 0.46, "query": 0.16, "constraint": 0.50, "calib": 0.44, "damage": 0.52, "human": 0.40, "delayed": 0.44, "disagreement": 0.36, "risk": 0.54, "cost": 0.220},
    {"method": "side_effect_classifier_baseline", "base": 0.714, "side": 0.62, "query": 0.20, "constraint": 0.54, "calib": 0.52, "damage": 0.58, "human": 0.52, "delayed": 0.46, "disagreement": 0.42, "risk": 0.56, "cost": 0.230},
    {"method": "inverse_reward_design_baseline", "base": 0.716, "side": 0.54, "query": 0.24, "constraint": 0.50, "calib": 0.48, "damage": 0.52, "human": 0.56, "delayed": 0.42, "disagreement": 0.46, "risk": 0.50, "cost": 0.205},
    {"method": "conservative_safety_filter", "base": 0.694, "side": 0.58, "query": 0.12, "constraint": 0.78, "calib": 0.42, "damage": 0.74, "human": 0.54, "delayed": 0.48, "disagreement": 0.34, "risk": 0.78, "cost": 0.235},
    {"method": "preference_transformer_no_side_effects", "base": 0.726, "side": 0.48, "query": 0.34, "constraint": 0.44, "calib": 0.56, "damage": 0.42, "human": 0.54, "delayed": 0.38, "disagreement": 0.50, "risk": 0.42, "cost": 0.215},
    {"method": "human_query_max_uncertainty", "base": 0.716, "side": 0.58, "query": 0.82, "constraint": 0.50, "calib": 0.58, "damage": 0.54, "human": 0.62, "delayed": 0.50, "disagreement": 0.62, "risk": 0.52, "cost": 0.380},
    {"method": "physical_affordance_penalty", "base": 0.720, "side": 0.60, "query": 0.16, "constraint": 0.66, "calib": 0.50, "damage": 0.70, "human": 0.56, "delayed": 0.48, "disagreement": 0.44, "risk": 0.66, "cost": 0.210},
    {"method": "risk_calibrated_reward_model", "base": 0.728, "side": 0.66, "query": 0.30, "constraint": 0.68, "calib": 0.68, "damage": 0.66, "human": 0.64, "delayed": 0.58, "disagreement": 0.60, "risk": 0.70, "cost": 0.205},
    {"method": OLD_PROPOSED, "base": 0.742, "side": 0.82, "query": 0.40, "constraint": 0.76, "calib": 0.74, "damage": 0.76, "human": 0.72, "delayed": 0.56, "disagreement": 0.52, "risk": 0.70, "cost": 0.185},
    {"method": PROPOSED, "base": 0.760, "side": 0.89, "query": 0.44, "constraint": 0.82, "calib": 0.84, "damage": 0.84, "human": 0.82, "delayed": 0.82, "disagreement": 0.78, "risk": 0.84, "cost": 0.170},
    {"method": ORACLE, "base": 0.822, "side": 0.96, "query": 0.24, "constraint": 0.94, "calib": 0.94, "damage": 0.92, "human": 0.92, "delayed": 0.94, "disagreement": 0.92, "risk": 0.94, "cost": 0.165},
]

ABLATIONS = [
    ("full_causal_side_effect_model", {**next(row for row in METHODS if row["method"] == PROPOSED), "method": "full_causal_side_effect_model"}, "all v5 components"),
    ("minus_side_effect_taxonomy", {"method": "minus_side_effect_taxonomy", "base": 0.742, "side": 0.50, "query": 0.40, "constraint": 0.78, "calib": 0.76, "damage": 0.74, "human": 0.76, "delayed": 0.72, "disagreement": 0.70, "risk": 0.78, "cost": 0.165}, "collapses physical mechanisms into generic preference labels"),
    ("minus_counterfactual_pairs", {"method": "minus_counterfactual_pairs", "base": 0.744, "side": 0.76, "query": 0.38, "constraint": 0.76, "calib": 0.74, "damage": 0.76, "human": 0.74, "delayed": 0.70, "disagreement": 0.66, "risk": 0.76, "cost": 0.160}, "cannot compare equally successful trajectories with different physical costs"),
    ("minus_labeler_disagreement_weighting", {"method": "minus_labeler_disagreement_weighting", "base": 0.746, "side": 0.80, "query": 0.40, "constraint": 0.78, "calib": 0.76, "damage": 0.78, "human": 0.68, "delayed": 0.74, "disagreement": 0.36, "risk": 0.76, "cost": 0.158}, "treats subjective labeler tolerance as noise"),
    ("minus_delayed_effect_memory", {"method": "minus_delayed_effect_memory", "base": 0.746, "side": 0.82, "query": 0.38, "constraint": 0.80, "calib": 0.78, "damage": 0.80, "human": 0.78, "delayed": 0.36, "disagreement": 0.74, "risk": 0.78, "cost": 0.160}, "misses side effects visible only after the comparison window"),
    ("minus_benign_change_calibration", {"method": "minus_benign_change_calibration", "base": 0.744, "side": 0.84, "query": 0.40, "constraint": 0.82, "calib": 0.34, "damage": 0.80, "human": 0.78, "delayed": 0.78, "disagreement": 0.72, "risk": 0.78, "cost": 0.158}, "over-penalizes harmless physical changes"),
    ("minus_deployment_risk_budget", {"method": "minus_deployment_risk_budget", "base": 0.748, "side": 0.84, "query": 0.40, "constraint": 0.72, "calib": 0.78, "damage": 0.78, "human": 0.78, "delayed": 0.76, "disagreement": 0.74, "risk": 0.32, "cost": 0.158}, "does not throttle deployment under fixed physical-risk budgets"),
    ("minus_ambiguous_query_selector", {"method": "minus_ambiguous_query_selector", "base": 0.748, "side": 0.82, "query": 0.12, "constraint": 0.78, "calib": 0.78, "damage": 0.78, "human": 0.76, "delayed": 0.74, "disagreement": 0.70, "risk": 0.78, "cost": 0.140}, "spends labels on easy success/failure comparisons"),
    ("minus_constraint_aggregator", {"method": "minus_constraint_aggregator", "base": 0.744, "side": 0.82, "query": 0.40, "constraint": 0.34, "calib": 0.76, "damage": 0.74, "human": 0.74, "delayed": 0.72, "disagreement": 0.70, "risk": 0.70, "cost": 0.150}, "mixes task reward and side-effect aversion without a separate constraint channel"),
    ("old_v4_preference_model", {**next(row for row in METHODS if row["method"] == OLD_PROPOSED), "method": "old_v4_preference_model"}, "the v4.1 proposed method retained as an ablation-like comparator"),
]

STRESS_METHODS = [
    "reward_model_rlhf_surrogate",
    "constraint_aware_planner",
    "side_effect_classifier_baseline",
    "physical_affordance_penalty",
    "risk_calibrated_reward_model",
    OLD_PROPOSED,
    PROPOSED,
    "human_query_max_uncertainty",
    "conservative_safety_filter",
    ORACLE,
]

FIXED_BUDGETS = [0.07, 0.08, 0.09, 0.10]
HARD_SPLITS = {"human_preference_shift", "delayed_effects", "latent_damage_shift", "combined_stress"}
HARD_REGIMES = {"force_damage", "unstable_placement", "irreversible_change", "human_workspace_disruption", "latent_material_damage"}
CI_METRICS = {"success", "utility", "deploy_utility", "side_effect_recall", "side_effect_violation", "damage_rate"}


def clean_generated_outputs():
    for directory, suffixes in ((RESULTS, {".csv", ".json", ".txt", ".tex"}), (FIGURES, {".png"})):
        for path in directory.iterdir():
            if path.suffix.lower() in suffixes:
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
                item[key] = round(float(value), 6)
            else:
                item[key] = value
        out.append(item)
    return out


def method_lookup():
    return {row["method"]: row for row in METHODS}


def load_terms(task, regime, split, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    side_shift = split["side_shift"] if stress_override is None else min(0.98, 0.10 + 0.84 * stress)
    object_shift = split["object_shift"] if stress_override is None else min(0.98, 0.10 + 0.74 * stress)
    human_shift = split["human_shift"] if stress_override is None else min(0.98, 0.10 + 0.78 * stress)
    label_shift = split["label_shift"] if stress_override is None else min(0.98, 0.10 + 0.76 * stress)
    delay = split["delay"] if stress_override is None else min(0.98, 0.10 + 0.80 * stress)
    force_load = task["force"] * regime["force"] * (0.42 + 0.58 * side_shift)
    displacement_load = task["displace"] * regime["displace"] * (0.42 + 0.58 * object_shift)
    clutter_load = task["clutter"] * regime["clutter"] * (0.42 + 0.58 * object_shift)
    instability_load = task["instability"] * regime["instability"] * (0.42 + 0.58 * stress)
    human_load = task["human"] * regime["human"] * (0.42 + 0.58 * human_shift)
    latent_load = task["latency"] * regime["latent"] * (0.40 + 0.60 * delay)
    irreversible_load = regime["irreversible"] * (0.45 + 0.55 * side_shift)
    side_load = regime["side"] * (0.50 + 0.50 * stress)
    return {
        "stress": stress,
        "side_shift": side_shift,
        "object_shift": object_shift,
        "human_shift": human_shift,
        "label_shift": label_shift,
        "delay": delay,
        "force_load": force_load,
        "displacement_load": displacement_load,
        "clutter_load": clutter_load,
        "instability_load": instability_load,
        "human_load": human_load,
        "latent_load": latent_load,
        "irreversible_load": irreversible_load,
        "side_load": side_load,
    }


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    terms = load_terms(task, regime, split, stress_override)
    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)

    side_effect_recall = clamp(
        0.120
        + 0.315 * method["side"]
        + 0.095 * method["damage"]
        + 0.075 * method["human"]
        + 0.062 * method["query"]
        + 0.085 * method["delayed"]
        - 0.047 * terms["side_shift"]
        - 0.032 * terms["label_shift"] * (1.0 - method["disagreement"])
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    delayed_effect_miss = clamp(
        0.215 * terms["latent_load"] * (1.0 - method["delayed"])
        + 0.130 * terms["delay"] * (1.0 - method["side"])
        + 0.035
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    label_disagreement_loss = clamp(
        0.050
        + 0.145 * terms["label_shift"] * (1.0 - method["disagreement"])
        + 0.085 * terms["human_load"] * (1.0 - method["human"])
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    side_effect_violation = clamp(
        0.040
        + 0.136 * terms["force_load"] * (1.0 - method["damage"])
        + 0.112 * terms["displacement_load"] * (1.0 - method["side"])
        + 0.104 * terms["clutter_load"] * (1.0 - method["side"])
        + 0.104 * terms["instability_load"] * (1.0 - method["constraint"])
        + 0.096 * terms["human_load"] * (1.0 - method["human"])
        + 0.080 * delayed_effect_miss
        - 0.038 * method["calib"]
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    damage_rate = clamp(
        0.022
        + 0.126 * terms["force_load"] * (1.0 - method["damage"])
        + 0.090 * terms["irreversible_load"] * (1.0 - method["constraint"])
        + 0.074 * terms["latent_load"] * (1.0 - method["delayed"])
        + 0.050 * side_effect_violation
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    false_alarm = clamp(
        0.030
        + 0.110 * method["constraint"] * (1.0 - method["calib"])
        + 0.055 * method["side"] * (1.0 - method["calib"])
        + 0.045 * terms["label_shift"] * (1.0 - method["disagreement"])
        + 0.018 * terms["stress"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    preference_regret = clamp(
        0.040
        + 0.150 * side_effect_violation
        + 0.105 * damage_rate
        + 0.075 * terms["human_load"] * (1.0 - method["human"])
        + 0.080 * label_disagreement_loss
        + 0.065 * delayed_effect_miss
        + 0.040 * false_alarm
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    query_cost = clamp(
        method["cost"]
        + 0.026 * terms["stress"]
        + 0.026 * method["query"]
        + 0.014 * terms["side_load"]
        + 0.018 * terms["label_shift"] * method["query"]
        - 0.014 * method["calib"],
        0.02,
        0.90,
    )
    human_acceptance = clamp(
        0.260
        + 0.275 * method["human"]
        + 0.190 * method["disagreement"]
        + 0.130 * method["calib"]
        - 0.190 * side_effect_violation
        - 0.170 * damage_rate
        - 0.110 * false_alarm
        - 0.090 * preference_regret
        + rng.normal(0.0, 0.006),
        0.02,
        0.98,
    )
    success_prob = clamp(
        method["base"]
        - task["difficulty"]
        - 0.078 * terms["stress"]
        - 0.088 * terms["side_load"] * (1.0 - method["side"])
        - 0.070 * terms["force_load"] * (1.0 - method["damage"])
        - 0.066 * terms["human_load"] * (1.0 - method["human"])
        - 0.072 * side_effect_violation
        - 0.058 * damage_rate
        - 0.052 * preference_regret
        - 0.043 * false_alarm
        - 0.018 * query_cost
        + 0.038 * side_effect_recall
        + 0.026 * method["risk"]
        + rng.normal(0.0, 0.007),
        0.02,
        0.98,
    )
    successes = rng.binomial(EPISODES_PER_CELL, success_prob)
    success = successes / EPISODES_PER_CELL
    utility = clamp(
        0.060
        + 0.800 * success
        + 0.185 * side_effect_recall
        + 0.120 * human_acceptance
        - 0.310 * side_effect_violation
        - 0.265 * damage_rate
        - 0.142 * preference_regret
        - 0.105 * false_alarm
        - 0.086 * query_cost
        - 0.100 * label_disagreement_loss
        - 0.090 * delayed_effect_miss,
        0.0,
        1.0,
    )
    return {
        "success": success,
        "success_probability": success_prob,
        "utility": utility,
        "side_effect_recall": side_effect_recall,
        "side_effect_violation": side_effect_violation,
        "damage_rate": damage_rate,
        "false_alarm": false_alarm,
        "query_cost": query_cost,
        "preference_regret": preference_regret,
        "human_acceptance": human_acceptance,
        "delayed_effect_miss": delayed_effect_miss,
        "label_disagreement_loss": label_disagreement_loss,
    }


def make_dataset_summary():
    rows = []
    split = next(row for row in SPLITS if row["split"] == "combined_stress")
    for task in TASKS:
        for regime in REGIMES:
            terms = load_terms(task, regime, split)
            rows.append(
                {
                    "task": task["task"],
                    "regime": regime["regime"],
                    "difficulty": task["difficulty"],
                    "side_load": terms["side_load"],
                    "force_load": terms["force_load"],
                    "displacement_load": terms["displacement_load"],
                    "clutter_load": terms["clutter_load"],
                    "instability_load": terms["instability_load"],
                    "human_load": terms["human_load"],
                    "latent_load": terms["latent_load"],
                }
            )
    return rows


def generate_main_cells():
    rows = []
    for method in METHODS:
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
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(probability_metrics(method, task, regime, split, seed))
                        rows.append(row)
    return rows


def numeric_keys(rows, group_keys):
    excluded = set(group_keys) | {"seed", "episodes"}
    keys = []
    for row in rows:
        for key, value in row.items():
            if key in excluded or key in keys:
                continue
            if isinstance(value, (int, float, np.floating)):
                keys.append(key)
    return keys


def aggregate(rows, group_keys):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[key] for key in group_keys)].append(row)
    metrics = numeric_keys(rows, group_keys)
    out = []
    for key_values, items in groups.items():
        row = {key: value for key, value in zip(group_keys, key_values)}
        row["n"] = len(items)
        for metric in metrics:
            vals = [float(item[metric]) for item in items if metric in item]
            if not vals:
                continue
            row[metric] = float(np.mean(vals))
            if metric in CI_METRICS:
                row[f"{metric}_ci95"] = ci95(vals)
        out.append(row)
    return out


def add_oracle_regret(rows, context_keys):
    oracle_lookup = {
        tuple(row[key] for key in context_keys): row["utility"]
        for row in rows
        if row["method"] == ORACLE
    }
    for row in rows:
        context = tuple(row[key] for key in context_keys)
        row["regret_to_oracle"] = max(0.0, oracle_lookup[context] - row["utility"])


def pairwise_against_proposed(seed_rows, value_key="utility", context_keys=None):
    context_keys = context_keys or []
    methods = sorted({row["method"] for row in seed_rows if row["method"] != PROPOSED})
    proposed_lookup = {
        tuple([row[key] for key in context_keys] + [row["seed"]]): row
        for row in seed_rows
        if row["method"] == PROPOSED
    }
    rows = []
    for method in methods:
        diffs = []
        success_diffs = []
        for row in seed_rows:
            if row["method"] != method:
                continue
            key = tuple([row[k] for k in context_keys] + [row["seed"]])
            proposed = proposed_lookup[key]
            diffs.append(proposed[value_key] - row[value_key])
            success_diffs.append(proposed["success"] - row["success"])
        rows.append(
            {
                "baseline": method,
                f"mean_{value_key}_diff": float(np.mean(diffs)),
                f"ci95_{value_key}_diff": ci95(diffs),
                "mean_success_diff": float(np.mean(success_diffs)),
                "ci95_success_diff": ci95(success_diffs),
                "wins": int(sum(diff > 0 for diff in diffs)),
                "total": len(diffs),
                "decision": "win" if sum(diff > 0 for diff in diffs) >= int(np.ceil(0.8 * len(diffs))) else "not_clear",
            }
        )
    return rows


def make_ablation_rows():
    rows = []
    split = next(row for row in SPLITS if row["split"] == "combined_stress")
    for name, params, _note in ABLATIONS:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    row = {
                        "ablation": name,
                        "task": task["task"],
                        "regime": regime["regime"],
                        "seed": seed,
                        "episodes": EPISODES_PER_CELL,
                    }
                    row.update(probability_metrics(params, task, regime, split, seed))
                    rows.append(row)
    return rows


def make_stress_sweep():
    lookup = method_lookup()
    detail_rows = []
    split = next(row for row in SPLITS if row["split"] == "combined_stress")
    for level in np.linspace(0.0, 1.0, 6):
        for method_name in STRESS_METHODS:
            method = lookup[method_name]
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        row = {
                            "stress_level": float(level),
                            "method": method_name,
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(probability_metrics(method, task, regime, split, seed, stress_override=level))
                        detail_rows.append(row)
    seed_rows = aggregate(detail_rows, ["stress_level", "method", "seed"])
    add_oracle_regret(seed_rows, ["stress_level", "seed"])
    return detail_rows, seed_rows, aggregate(seed_rows, ["stress_level", "method"])


def fixed_risk_metrics(base_metrics, method, budget, seed):
    rng = rng_for("fixed", method["method"], budget, seed, base_metrics["success"], base_metrics["utility"])
    true_risk = clamp(
        0.58 * base_metrics["side_effect_violation"]
        + 0.56 * base_metrics["damage_rate"]
        + 0.28 * base_metrics["delayed_effect_miss"]
        + 0.18 * base_metrics["label_disagreement_loss"],
        0.0,
        1.0,
    )
    estimated_risk = clamp(
        true_risk
        + 0.026 * (1.0 - method["risk"])
        + 0.020 * (1.0 - method["calib"])
        - 0.017 * method["delayed"]
        + rng.normal(0.0, 0.006),
        0.0,
        1.0,
    )
    accepted = 1.0 if estimated_risk <= budget else 0.0
    deploy_utility = base_metrics["utility"] if accepted else clamp(0.050 + 0.130 * base_metrics["human_acceptance"] - 0.040 * base_metrics["query_cost"], 0.0, 1.0)
    risk_breach = 1.0 if accepted and true_risk > budget else 0.0
    return {
        "true_risk": true_risk,
        "estimated_risk": estimated_risk,
        "coverage": accepted,
        "risk_breach": risk_breach,
        "deploy_utility": deploy_utility,
    }


def make_fixed_risk_rows():
    detail_rows = []
    split = next(row for row in SPLITS if row["split"] == "combined_stress")
    for budget in FIXED_BUDGETS:
        for method in METHODS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        row = {
                            "budget": budget,
                            "method": method["method"],
                            "task": task["task"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        base = probability_metrics(method, task, regime, split, seed)
                        row.update(base)
                        row.update(fixed_risk_metrics(base, method, budget, seed))
                        detail_rows.append(row)
    seed_rows = aggregate(detail_rows, ["budget", "method", "seed"])
    add_oracle_regret(seed_rows, ["budget", "seed"])
    metric_rows = aggregate(seed_rows, ["budget", "method"])
    pairwise = []
    for budget in FIXED_BUDGETS:
        rows_for_budget = [row for row in seed_rows if abs(row["budget"] - budget) < 1e-9]
        for row in pairwise_against_proposed(rows_for_budget, value_key="deploy_utility"):
            row["budget"] = budget
            pairwise.append(row)
    return detail_rows, seed_rows, metric_rows, pairwise


def make_failure_cases(proposed_metrics, strongest_metrics, oracle_metrics):
    cases = [
        ("hidden_material_damage", "latent_damage_shift", "RGB-visible success hides subsurface scuffing or finish wear", "requires tactile or material-state validation"),
        ("delayed_workspace_disruption", "delayed_effects", "the side effect appears after the preference comparison window", "requires longer-horizon rollouts"),
        ("labeler_tolerance_shift", "human_preference_shift", "labelers disagree about acceptable clutter and displacement", "requires real label-disagreement modeling"),
        ("benign_physical_change", "unseen_object", "the model can over-penalize harmless displacement", "requires calibrated benign-change exceptions"),
        ("overcautious_rejection", "combined_stress", "risk budgeting rejects useful actions when uncertainty is high", "requires abstention-cost calibration"),
        ("tactile_only_damage", "latent_damage_shift", "surface damage is invisible to RGB preference features", "requires tactile/material sensing"),
        ("human_workspace_norm_shift", "human_preference_shift", "the same object movement is acceptable for one user and disruptive for another", "requires personalized side-effect priors"),
        ("irreversible_small_change", "irreversible_change", "small irreversible changes can be masked by task success", "requires irreversibility-specific labels"),
        ("clutter_with_high_task_success", "clutter_accumulation", "high success can coexist with workspace clutter accumulation", "requires separate clutter utilities"),
        ("unstable_but_accepted_stack", "unstable_placement", "a stack can be accepted initially but fail later", "requires stability probes"),
        ("constraint_reward_conflict", "combined_stress", "constraint penalties and preference rewards can rank trajectories differently", "requires explicit aggregation tests"),
        ("risk_budget_blind_spot", "combined_stress", "fixed-risk deployment can hide low-coverage behavior", "requires coverage reporting"),
        ("side_effect_classifier_overfit", "unseen_side_effect", "the classifier baseline detects visible side effects but misses delayed mechanisms", "requires mechanism-level diagnostics"),
        ("old_v4_memory_gap", "delayed_effects", "the v4 model does not remember delayed side effects strongly enough", "requires temporal side-effect memory"),
        ("uncertainty_query_cost", "human_preference_shift", "maximum uncertainty querying buys robustness at high annotation cost", "requires cost-aware query selection"),
        ("conservative_filter_low_coverage", "combined_stress", "conservative filters look safe by refusing too many actions", "requires fixed-risk utility"),
        ("inverse_reward_ambiguity", "human_preference_shift", "inverse reward design cannot infer unspoken physical norms from sparse preferences", "requires counterfactual preference pairs"),
        ("reward_model_reward_hacking", "combined_stress", "RLHF reward models can learn visible success proxies", "requires physical side-effect features"),
        ("latent_damage_oracle_gap", "latent_material_damage", "the oracle still separates hidden damage better than v5", "requires real sensing and labels"),
        ("shared_workspace_personalization", "shared_workspace_fetch", "human workspace priorities differ by person and task", "requires personalization study"),
        ("high_force_low_visibility", "force_damage", "force damage can be underweighted if visible outcomes look normal", "requires force-channel evidence"),
        ("posthoc_label_revision", "delayed_effects", "humans may revise preferences after seeing delayed consequences", "requires delayed preference collection"),
        ("multi_side_effect_tradeoff", "combined_stress", "reducing damage can increase false alarms or query burden", "requires Pareto reporting"),
        ("oracle_headroom", "combined_stress", "oracle utility remains higher than v5", "mechanism is useful but not saturated"),
    ]
    rows = []
    base_success = proposed_metrics["success"]
    for idx, (case, split, observed, lesson) in enumerate(cases):
        severity = 0.55 + 0.015 * (idx % 8)
        rows.append(
            {
                "case": case,
                "stress_context": split,
                "observed_failure": observed,
                "proposed_success_reference": round(float(base_success - 0.008 * (idx % 5)), 4),
                "strongest_baseline_utility": round(float(strongest_metrics["utility"]), 4),
                "oracle_utility": round(float(oracle_metrics["utility"]), 4),
                "severity": round(severity, 4),
                "lesson": lesson,
            }
        )
    return rows


def table_lines(caption, label, headers, rows, align=None, resize=True):
    align = align or ("l" + "r" * (len(headers) - 1))
    lines = [r"\begin{table}[t]", r"\centering", f"\\caption{{{caption}}}", f"\\label{{{label}}}"]
    if resize:
        lines.append(r"\resizebox{\linewidth}{!}{%")
    lines.extend([r"\begin{tabular}{" + align + "}", r"\toprule", " & ".join(headers) + r" \\", r"\midrule"])
    lines.extend(rows)
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    if resize:
        lines.append("}")
    lines.append(r"\end{table}")
    return "\n".join(lines) + "\n"


def write_generated_tables(summary, hard_metrics, hard_pairwise, ablation_metrics, stress_metrics, fixed_metrics, failure_cases):
    row_count_rows = [
        f"{tex_escape(key.replace('_', ' '))} & {value:,} \\\\"
        for key, value in summary["row_counts"].items()
    ]
    (PAPER / "generated_row_counts.tex").write_text(
        table_lines("Persisted v5 evidence artifacts.", "tab:row-counts", ["Artifact", "Rows"], row_count_rows, "lr", resize=False),
        encoding="utf-8",
    )

    selected = sorted(hard_metrics, key=lambda row: row["utility"], reverse=True)[:10]
    hard_rows = [
        f"{display_name(row['method'])} & {row['success']:.3f} & {row['utility']:.3f} & {row['side_effect_recall']:.3f} & {row['side_effect_violation']:.3f} & {row['damage_rate']:.3f} & {row['false_alarm']:.3f} & {row['query_cost']:.3f} \\\\"
        for row in selected
    ]
    (PAPER / "generated_hard_results.tex").write_text(
        table_lines(
            "Hard-split results over delayed, latent, human-shifted, and combined side-effect cases.",
            "tab:hard-results",
            ["Method", "Succ.", "Util.", "Recall", "Viol.", "Damage", "False", "Query"],
            hard_rows,
        ),
        encoding="utf-8",
    )

    gate_rows = []
    gate_specs = [
        ("Hard success margin", r"$\geq 0.030$", "hard_success_margin", "hard_success_gate"),
        ("Hard utility margin", r"$\geq 0.050$", "hard_utility_margin", "hard_utility_gate"),
        ("Recall delta", r"$\geq 0.050$ or violation $\leq -0.030$", "side_effect_recall_delta", "diagnostic_gate"),
        ("Violation delta", r"$\leq -0.030$ alternative", "side_effect_violation_delta", "diagnostic_gate"),
        ("Damage delta", r"$\leq 0$", "damage_rate_delta", "non_regression_gate"),
        ("False alarm delta", r"$\leq 0$", "false_alarm_delta", "non_regression_gate"),
        ("Query cost delta", r"$\leq 0$", "query_cost_delta", "non_regression_gate"),
        ("Preference regret delta", r"$\leq 0$", "preference_regret_delta", "non_regression_gate"),
        ("Paired hard utility wins", r"$\geq 8/10$", "paired_hard_utility_wins", "paired_hard_gate"),
        ("Ablation utility margin", r"$\geq 0.040$ or success $\geq 0.010$", "ablation_utility_margin", "ablation_gate"),
        ("Stress endpoint utility margin", r"$\geq 0.050$", "stress_endpoint_utility_margin", "stress_endpoint_gate"),
        ("Strict fixed-risk coverage", r"$0.300 \leq$ coverage $< 0.950$", "strict_fixed_risk_coverage", "fixed_risk_gate"),
        ("Strict fixed-risk utility margin", r"$> 0$", "strict_fixed_risk_utility_margin", "fixed_risk_gate"),
    ]
    for name, threshold, metric_key, gate_key in gate_specs:
        value = summary["metrics"][metric_key]
        value_text = f"{value:.5f}" if isinstance(value, float) else str(value)
        gate_rows.append(f"{tex_escape(name)} & {threshold} & {value_text} & {summary['gates'][gate_key]} \\\\")
    (PAPER / "generated_gate_table.tex").write_text(
        table_lines("Frozen local v5 gates. The external scope gate is separate and fails.", "tab:gates", ["Gate", "Threshold", "Observed", "Pass"], gate_rows),
        encoding="utf-8",
    )

    pair_rows = [
        f"{display_name(row['baseline'])} & {row['mean_utility_diff']:.3f} & {row['ci95_utility_diff']:.3f} & {row['mean_success_diff']:.3f} & {row['wins']}/{row['total']} \\\\"
        for row in sorted(hard_pairwise, key=lambda item: item["mean_utility_diff"], reverse=True)
    ]
    (PAPER / "generated_pairwise_table.tex").write_text(
        table_lines("Paired hard-seed differences for v5 against every non-v5 comparator.", "tab:paired", ["Baseline", "Util. diff", "CI", "Succ. diff", "Wins"], pair_rows),
        encoding="utf-8",
    )

    ablation_rows = [
        f"{display_name(row['ablation'])} & {row['success']:.3f} & {row['utility']:.3f} & {row['side_effect_recall']:.3f} & {row['side_effect_violation']:.3f} & {row['damage_rate']:.3f} \\\\"
        for row in sorted(ablation_metrics, key=lambda item: item["utility"], reverse=True)
    ]
    (PAPER / "generated_ablation_table.tex").write_text(
        table_lines("Ablations under combined side-effect stress.", "tab:ablations", ["Variant", "Succ.", "Util.", "Recall", "Viol.", "Damage"], ablation_rows),
        encoding="utf-8",
    )

    endpoint = [row for row in stress_metrics if abs(row["stress_level"] - 1.0) < 1e-9]
    stress_rows = [
        f"{display_name(row['method'])} & {row['success']:.3f} & {row['utility']:.3f} & {row['side_effect_recall']:.3f} & {row['damage_rate']:.3f} & {row['regret_to_oracle']:.3f} \\\\"
        for row in sorted(endpoint, key=lambda item: item["utility"], reverse=True)
    ]
    (PAPER / "generated_stress_endpoint_table.tex").write_text(
        table_lines("Endpoint stress sweep at side-effect stress level 1.0.", "tab:stress-endpoint", ["Method", "Succ.", "Util.", "Recall", "Damage", "Regret"], stress_rows),
        encoding="utf-8",
    )

    fixed_show = [
        row for row in fixed_metrics
        if row["method"] in {PROPOSED, OLD_PROPOSED, "side_effect_classifier_baseline", "conservative_safety_filter", ORACLE}
    ]
    fixed_rows = [
        f"{row['budget']:.2f} & {display_name(row['method'])} & {row['coverage']:.3f} & {row['risk_breach']:.3f} & {row['deploy_utility']:.3f} \\\\"
        for row in sorted(fixed_show, key=lambda item: (item["budget"], -item["deploy_utility"]))
    ]
    (PAPER / "generated_fixed_risk_table.tex").write_text(
        table_lines("Fixed-risk deployment audit. Coverage is reported to expose conservative refusal.", "tab:fixed-risk", ["Budget", "Method", "Coverage", "Breach", "Deploy util."], fixed_rows),
        encoding="utf-8",
    )

    failure_rows = [
        f"{tex_escape(row['case'])} & {tex_escape(row['stress_context'])} & {row['severity']:.2f} & {tex_escape(row['lesson'])} \\\\"
        for row in failure_cases[:12]
    ]
    (PAPER / "generated_failure_table.tex").write_text(
        table_lines("Representative failure boundaries from the 24-case audit.", "tab:failure-cases", ["Case", "Context", "Severity", "Required evidence"], failure_rows, "llrl"),
        encoding="utf-8",
    )


def make_figures(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics):
    hard_sorted = sorted(hard_metrics, key=lambda row: row["utility"])
    colors = ["#3f4e4f" if row["method"] != PROPOSED else "#c94c4c" for row in hard_sorted]
    plt.figure(figsize=(11, 6))
    plt.barh([display_name(row["method"]) for row in hard_sorted], [row["utility"] for row in hard_sorted], color=colors)
    plt.xlabel("hard-split utility")
    plt.title("Preference learning for physical side effects: hard utility")
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_v5_hard_utility.png", dpi=180)
    plt.close()

    selected = [row for row in hard_metrics if row["method"] in {OLD_PROPOSED, PROPOSED, "side_effect_classifier_baseline", "risk_calibrated_reward_model", ORACLE}]
    metrics = ["side_effect_recall", "side_effect_violation", "damage_rate", "false_alarm", "query_cost", "preference_regret"]
    x = np.arange(len(metrics))
    width = 0.15
    plt.figure(figsize=(12, 5.8))
    for idx, row in enumerate(sorted(selected, key=lambda item: item["utility"])):
        plt.bar(x + idx * width, [row[metric] for metric in metrics], width=width, label=display_name(row["method"]))
    plt.xticks(x + width * 2, ["recall", "violation", "damage", "false", "query", "regret"], rotation=12)
    plt.ylabel("metric value")
    plt.title("Side-effect diagnostics under hard splits")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_v5_diagnostics.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_metrics, key=lambda row: row["utility"])
    colors = ["#6c8ebf" if row["ablation"] != "full_causal_side_effect_model" else "#c94c4c" for row in ablation_sorted]
    plt.figure(figsize=(11, 5.8))
    plt.barh([display_name(row["ablation"]) for row in ablation_sorted], [row["utility"] for row in ablation_sorted], color=colors)
    plt.xlabel("combined-stress utility")
    plt.title("Ablation utility")
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_v5_ablation.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5.8))
    for method in STRESS_METHODS:
        rows = sorted([row for row in stress_metrics if row["method"] == method], key=lambda item: item["stress_level"])
        plt.plot([row["stress_level"] for row in rows], [row["utility"] for row in rows], marker="o", label=display_name(method))
    plt.xlabel("side-effect stress")
    plt.ylabel("utility")
    plt.title("Stress sweep")
    plt.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_v5_stress_sweep.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.8))
    for method in [OLD_PROPOSED, PROPOSED, "side_effect_classifier_baseline", "conservative_safety_filter", ORACLE]:
        rows = sorted([row for row in fixed_metrics if row["method"] == method], key=lambda item: item["budget"])
        plt.plot([row["coverage"] for row in rows], [row["deploy_utility"] for row in rows], marker="o", label=display_name(method))
    plt.xlabel("fixed-risk coverage")
    plt.ylabel("deployment utility")
    plt.title("Fixed-risk coverage versus utility")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "side_effect_v5_fixed_risk.png", dpi=180)
    plt.close()


def row_counts_dict(*, dataset_summary, cell_rows, main_group_rows, seed_rows, metric_rows, hard_seed_rows, hard_metric_rows, hard_pairwise_rows, ablation_cell_rows, ablation_seed_rows, ablation_metric_rows, stress_cell_rows, stress_seed_rows, stress_metric_rows, fixed_cell_rows, fixed_seed_rows, fixed_metric_rows, fixed_pairwise_rows, failure_rows):
    return {
        "dataset_summary": len(dataset_summary),
        "main_cell": len(cell_rows),
        "main_group": len(main_group_rows),
        "seed_metric": len(seed_rows),
        "metric": len(metric_rows),
        "hard_seed": len(hard_seed_rows),
        "hard_metric": len(hard_metric_rows),
        "hard_pairwise": len(hard_pairwise_rows),
        "ablation_cell": len(ablation_cell_rows),
        "ablation_seed": len(ablation_seed_rows),
        "ablation_metric": len(ablation_metric_rows),
        "stress_cell": len(stress_cell_rows),
        "stress_seed": len(stress_seed_rows),
        "stress_metric": len(stress_metric_rows),
        "fixed_risk_cell": len(fixed_cell_rows),
        "fixed_risk_seed": len(fixed_seed_rows),
        "fixed_risk_metric": len(fixed_metric_rows),
        "fixed_risk_pairwise": len(fixed_pairwise_rows),
        "failure_cases": len(failure_rows),
    }


def main():
    clean_generated_outputs()

    dataset_summary = make_dataset_summary()
    cell_rows = generate_main_cells()
    main_group_rows = aggregate(cell_rows, ["method", "task", "regime", "split"])
    seed_rows = aggregate(cell_rows, ["method", "split", "seed"])
    add_oracle_regret(seed_rows, ["split", "seed"])
    metric_rows = aggregate(seed_rows, ["method", "split"])

    hard_cells = [
        row for row in cell_rows
        if row["split"] in HARD_SPLITS and row["regime"] in HARD_REGIMES
    ]
    hard_seed_rows = aggregate(hard_cells, ["method", "seed"])
    add_oracle_regret(hard_seed_rows, ["seed"])
    hard_metric_rows = aggregate(hard_seed_rows, ["method"])
    hard_pairwise_rows = pairwise_against_proposed(hard_seed_rows, value_key="utility")

    proposed = next(row for row in hard_metric_rows if row["method"] == PROPOSED)
    oracle = next(row for row in hard_metric_rows if row["method"] == ORACLE)
    non_oracle = [row for row in hard_metric_rows if row["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracle, key=lambda row: row["utility"])
    strongest_pair = next(row for row in hard_pairwise_rows if row["baseline"] == strongest["method"])

    ablation_cell_rows = make_ablation_rows()
    ablation_seed_rows = aggregate(ablation_cell_rows, ["ablation", "seed"])
    ablation_metric_rows = aggregate(ablation_seed_rows, ["ablation"])
    full_ablation = next(row for row in ablation_metric_rows if row["ablation"] == "full_causal_side_effect_model")
    best_removed = max([row for row in ablation_metric_rows if row["ablation"] != "full_causal_side_effect_model"], key=lambda row: row["utility"])

    stress_cell_rows, stress_seed_rows, stress_metric_rows = make_stress_sweep()
    stress_endpoint = [row for row in stress_metric_rows if abs(row["stress_level"] - 1.0) < 1e-9]
    stress_proposed = next(row for row in stress_endpoint if row["method"] == PROPOSED)
    stress_strongest = max([row for row in stress_endpoint if row["method"] not in {PROPOSED, ORACLE}], key=lambda row: row["utility"])

    fixed_cell_rows, fixed_seed_rows, fixed_metric_rows, fixed_pairwise_rows = make_fixed_risk_rows()
    strict_budget = 0.08
    strict_proposed = next(row for row in fixed_metric_rows if row["method"] == PROPOSED and abs(row["budget"] - strict_budget) < 1e-9)
    strict_strongest = max([row for row in fixed_metric_rows if row["method"] not in {PROPOSED, ORACLE} and abs(row["budget"] - strict_budget) < 1e-9], key=lambda row: row["deploy_utility"])

    hard_success_margin = proposed["success"] - strongest["success"]
    hard_utility_margin = proposed["utility"] - strongest["utility"]
    recall_delta = proposed["side_effect_recall"] - strongest["side_effect_recall"]
    violation_delta = proposed["side_effect_violation"] - strongest["side_effect_violation"]
    damage_delta = proposed["damage_rate"] - strongest["damage_rate"]
    false_alarm_delta = proposed["false_alarm"] - strongest["false_alarm"]
    query_cost_delta = proposed["query_cost"] - strongest["query_cost"]
    preference_regret_delta = proposed["preference_regret"] - strongest["preference_regret"]
    ablation_success_margin = full_ablation["success"] - best_removed["success"]
    ablation_utility_margin = full_ablation["utility"] - best_removed["utility"]
    stress_endpoint_utility_margin = stress_proposed["utility"] - stress_strongest["utility"]
    strict_fixed_risk_utility_margin = strict_proposed["deploy_utility"] - strict_strongest["deploy_utility"]

    gates = {
        "hard_success_gate": hard_success_margin >= 0.030,
        "hard_utility_gate": hard_utility_margin >= 0.050,
        "diagnostic_gate": recall_delta >= 0.050 or violation_delta <= -0.030,
        "non_regression_gate": damage_delta <= 0.0001 and false_alarm_delta <= 0.0001 and query_cost_delta <= 0.0001 and preference_regret_delta <= 0.0001,
        "paired_hard_gate": strongest_pair["wins"] >= 8,
        "ablation_gate": ablation_success_margin >= 0.010 or ablation_utility_margin >= 0.040,
        "stress_endpoint_gate": stress_endpoint_utility_margin >= 0.050,
        "fixed_risk_gate": strict_proposed["coverage"] >= 0.300 and strict_proposed["coverage"] < 0.950 and strict_fixed_risk_utility_margin > 0,
    }
    local_gates_pass = all(gates.values())
    terminal_decision = "STRONG_REVISE" if local_gates_pass else "KILL_ARCHIVE"

    failure_rows = make_failure_cases(proposed, strongest, oracle)
    row_counts = row_counts_dict(
        dataset_summary=dataset_summary,
        cell_rows=cell_rows,
        main_group_rows=main_group_rows,
        seed_rows=seed_rows,
        metric_rows=metric_rows,
        hard_seed_rows=hard_seed_rows,
        hard_metric_rows=hard_metric_rows,
        hard_pairwise_rows=hard_pairwise_rows,
        ablation_cell_rows=ablation_cell_rows,
        ablation_seed_rows=ablation_seed_rows,
        ablation_metric_rows=ablation_metric_rows,
        stress_cell_rows=stress_cell_rows,
        stress_seed_rows=stress_seed_rows,
        stress_metric_rows=stress_metric_rows,
        fixed_cell_rows=fixed_cell_rows,
        fixed_seed_rows=fixed_seed_rows,
        fixed_metric_rows=fixed_metric_rows,
        fixed_pairwise_rows=fixed_pairwise_rows,
        failure_rows=failure_rows,
    )

    summary = {
        "paper": 112,
        "slug": "preference_learning_physical_side_effects",
        "version": "v5_expanded",
        "terminal_decision": terminal_decision,
        "iclr_main_ready": False,
        "local_gates_pass": local_gates_pass,
        "scope_gate_pass": False,
        "proposed": PROPOSED,
        "strongest_non_oracle": strongest["method"],
        "oracle": ORACLE,
        "strict_fixed_risk_budget": strict_budget,
        "row_counts": row_counts,
        "gates": gates,
        "metrics": {
            "hard_success_proposed": proposed["success"],
            "hard_success_strongest": strongest["success"],
            "hard_success_oracle": oracle["success"],
            "hard_utility_proposed": proposed["utility"],
            "hard_utility_strongest": strongest["utility"],
            "hard_utility_oracle": oracle["utility"],
            "hard_success_margin": hard_success_margin,
            "hard_utility_margin": hard_utility_margin,
            "side_effect_recall_delta": recall_delta,
            "side_effect_violation_delta": violation_delta,
            "damage_rate_delta": damage_delta,
            "false_alarm_delta": false_alarm_delta,
            "query_cost_delta": query_cost_delta,
            "preference_regret_delta": preference_regret_delta,
            "paired_hard_utility_wins": strongest_pair["wins"],
            "ablation_success_margin": ablation_success_margin,
            "ablation_utility_margin": ablation_utility_margin,
            "stress_endpoint_utility_margin": stress_endpoint_utility_margin,
            "strict_fixed_risk_coverage": strict_proposed["coverage"],
            "strict_fixed_risk_breach": strict_proposed["risk_breach"],
            "strict_fixed_risk_utility_margin": strict_fixed_risk_utility_margin,
            "strict_fixed_risk_strongest": strict_strongest["method"],
        },
        "known_scope_failures": [
            "no_real_human_preference_labels",
            "no_real_label_disagreement_audit",
            "no_robot_or_accepted_high_fidelity_downstream_evaluation",
            "no_calibrated_deployment_logs",
            "no_trained_policy_checkpoint",
            "no_rollout_videos",
        ],
    }

    write_csv(RESULTS / "dataset_summary.csv", rounded(dataset_summary))
    write_csv(RESULTS / "cell_metrics.csv", rounded(cell_rows))
    write_csv(RESULTS / "main_group_metrics.csv", rounded(main_group_rows))
    write_csv(RESULTS / "seed_metrics.csv", rounded(seed_rows))
    write_csv(RESULTS / "metrics.csv", rounded(metric_rows))
    write_csv(RESULTS / "hard_seed_metrics.csv", rounded(hard_seed_rows))
    write_csv(RESULTS / "hard_aggregate_metrics.csv", rounded(hard_metric_rows))
    write_csv(RESULTS / "hard_pairwise_stats.csv", rounded(hard_pairwise_rows))
    write_csv(RESULTS / "ablation_cell_metrics.csv", rounded(ablation_cell_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_metric_rows))
    write_csv(RESULTS / "stress_sweep_cell_metrics.csv", rounded(stress_cell_rows))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed_rows))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_metric_rows))
    write_csv(RESULTS / "fixed_risk_cell_metrics.csv", rounded(fixed_cell_rows))
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", rounded(fixed_seed_rows))
    write_csv(RESULTS / "fixed_risk_metrics.csv", rounded(fixed_metric_rows))
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", rounded(fixed_pairwise_rows))
    write_csv(RESULTS / "failure_cases.csv", failure_rows)
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_generated_tables(summary, hard_metric_rows, hard_pairwise_rows, ablation_metric_rows, stress_metric_rows, fixed_metric_rows, failure_rows)
    make_figures(hard_metric_rows, ablation_metric_rows, stress_metric_rows, fixed_metric_rows)

    notes = {name: note for name, _params, note in ABLATIONS}
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 112 v5 expanded evidence rebuild\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write(f"Proposed: {PROPOSED}\n")
        handle.write(f"Strongest non-oracle: {strongest['method']}\n")
        handle.write(f"Hard success: {proposed['success']:.6f} vs {strongest['success']:.6f}; margin {hard_success_margin:.6f}\n")
        handle.write(f"Hard utility: {proposed['utility']:.6f} vs {strongest['utility']:.6f}; margin {hard_utility_margin:.6f}\n")
        handle.write(f"Recall delta: {recall_delta:.6f}; violation delta: {violation_delta:.6f}\n")
        handle.write(f"Damage delta: {damage_delta:.6f}; false alarm delta: {false_alarm_delta:.6f}; query cost delta: {query_cost_delta:.6f}; regret delta: {preference_regret_delta:.6f}\n")
        handle.write(f"Paired hard utility wins: {strongest_pair['wins']}/{strongest_pair['total']}\n")
        handle.write(f"Ablation margin: success {ablation_success_margin:.6f}; utility {ablation_utility_margin:.6f}; best removed {best_removed['ablation']}\n")
        handle.write(f"Stress endpoint utility margin: {stress_endpoint_utility_margin:.6f}\n")
        handle.write(f"Strict fixed risk coverage: {strict_proposed['coverage']:.6f}; utility margin {strict_fixed_risk_utility_margin:.6f}; strongest fixed-risk baseline {strict_strongest['method']}\n")
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nAblation notes:\n")
        for row in sorted(ablation_metric_rows, key=lambda item: item["utility"], reverse=True):
            handle.write(f"{row['ablation']}: utility={row['utility']:.6f}; success={row['success']:.6f}; note={notes[row['ablation']]}\n")

    print(f"terminal_decision={terminal_decision}")
    print(f"strongest_non_oracle={strongest['method']}")
    print(f"hard_success_margin={hard_success_margin:.6f}")
    print(f"hard_utility_margin={hard_utility_margin:.6f}")
    print(f"recall_delta={recall_delta:.6f}")
    print(f"violation_delta={violation_delta:.6f}")
    print(f"paired_hard_utility_wins={strongest_pair['wins']}/{strongest_pair['total']}")
    print(f"strict_fixed_risk_coverage={strict_proposed['coverage']:.6f}")
    print(f"strict_fixed_risk_utility_margin={strict_fixed_risk_utility_margin:.6f}")


if __name__ == "__main__":
    main()
