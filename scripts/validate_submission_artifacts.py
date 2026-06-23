import csv
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS_PDF = Path.home() / "Downloads" / "112.pdf"
EXPECTED_HASH = "43EB404BF1B1B34E7642EB0D3D6BC2561E2962103A69054AB991DA226D199C10"
EXPECTED_ROWS = {
    "dataset_summary.csv": ("dataset_summary", 80),
    "cell_metrics.csv": ("main_cell", 102400),
    "main_group_metrics.csv": ("main_group", 10240),
    "seed_metrics.csv": ("seed_metric", 1280),
    "metrics.csv": ("metric", 128),
    "hard_seed_metrics.csv": ("hard_seed", 160),
    "hard_aggregate_metrics.csv": ("hard_metric", 16),
    "hard_pairwise_stats.csv": ("hard_pairwise", 15),
    "ablation_cell_metrics.csv": ("ablation_cell", 8000),
    "ablation_seed_metrics.csv": ("ablation_seed", 100),
    "ablation_metrics.csv": ("ablation_metric", 10),
    "stress_sweep_cell_metrics.csv": ("stress_cell", 48000),
    "stress_sweep_seed_metrics.csv": ("stress_seed", 600),
    "stress_sweep.csv": ("stress_metric", 60),
    "fixed_risk_cell_metrics.csv": ("fixed_risk_cell", 51200),
    "fixed_risk_seed_metrics.csv": ("fixed_risk_seed", 640),
    "fixed_risk_metrics.csv": ("fixed_risk_metric", 64),
    "fixed_risk_pairwise_stats.csv": ("fixed_risk_pairwise", 60),
    "failure_cases.csv": ("failure_cases", 24),
}
NUMERIC_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def fail(message):
    raise AssertionError(message)


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def pdf_pages(path):
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    for line in output.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    fail(f"Could not read page count from {path}")


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_finite_numeric(rows, path):
    for row_idx, row in enumerate(rows, start=2):
        for key, value in row.items():
            value = value.strip()
            if value and NUMERIC_RE.match(value):
                number = float(value)
                if not math.isfinite(number):
                    fail(f"Non-finite value in {path}:{row_idx} column {key}")


def check_summary():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    if summary["paper"] != 112:
        fail("summary paper id is not 112")
    if summary["version"] != "v5_expanded":
        fail("summary version is not v5_expanded")
    if summary["terminal_decision"] != "STRONG_REVISE":
        fail("terminal decision is not STRONG_REVISE")
    if summary["iclr_main_ready"] is not False:
        fail("iclr_main_ready must be false")
    if summary["local_gates_pass"] is not True:
        fail("local gates must pass")
    if summary["scope_gate_pass"] is not False:
        fail("scope gate must fail honestly")
    if not all(summary["gates"].values()):
        fail("at least one frozen local gate failed")
    metrics = summary["metrics"]
    if metrics["paired_hard_utility_wins"] < 8:
        fail("paired hard utility wins below gate")
    if metrics["strict_fixed_risk_coverage"] < 0.30:
        fail("strict fixed-risk coverage below lower bound")
    if metrics["strict_fixed_risk_coverage"] >= 0.95:
        fail("strict fixed-risk coverage is suspiciously perfect")
    if metrics["strict_fixed_risk_utility_margin"] <= 0:
        fail("strict fixed-risk utility margin is not positive")
    return summary


def check_rows(summary):
    for filename, (summary_key, expected_count) in EXPECTED_ROWS.items():
        path = RESULTS / filename
        if not path.exists():
            fail(f"Missing expected CSV {path}")
        rows = read_csv_rows(path)
        if len(rows) != expected_count:
            fail(f"{filename} has {len(rows)} rows, expected {expected_count}")
        if summary["row_counts"][summary_key] != expected_count:
            fail(f"summary row count {summary_key} is wrong")
        check_finite_numeric(rows, path)


def check_pdf():
    repo_pdf = PAPER / "main.pdf"
    if not repo_pdf.exists():
        fail("paper/main.pdf is missing")
    if not DOWNLOADS_PDF.exists():
        fail("Downloads/112.pdf is missing")
    if pdf_pages(repo_pdf) < 25:
        fail("paper/main.pdf has fewer than 25 pages")
    if pdf_pages(DOWNLOADS_PDF) < 25:
        fail("Downloads/112.pdf has fewer than 25 pages")
    if file_hash(DOWNLOADS_PDF) != EXPECTED_HASH:
        fail("Downloads/112.pdf hash mismatch")
    if file_hash(repo_pdf) != EXPECTED_HASH:
        fail("paper/main.pdf hash does not match Downloads copy")


def check_artifact_locations():
    forbidden = [
        Path.home() / "Desktop" / "112.pdf",
        ROOT.parent / "112.pdf",
        ROOT / "112.pdf",
    ]
    for path in forbidden:
        if path.exists():
            fail(f"Forbidden PDF copy exists at {path}")


def check_latex_log():
    log = (PAPER / "main.log").read_text(encoding="utf-8", errors="replace")
    bad_patterns = [
        "Undefined control sequence",
        "Citation `",
        "There were undefined citations",
        "Overfull \\hbox",
        "Underfull \\hbox",
        "Rerun to get cross-references right",
        "Label(s) may have changed",
        "! LaTeX Error",
    ]
    for pattern in bad_patterns:
        if pattern in log:
            fail(f"LaTeX log contains recoverable issue: {pattern}")
    blg = (PAPER / "main.blg").read_text(encoding="utf-8", errors="replace")
    if "Warning--" in blg:
        fail("BibTeX warning found")


def check_manuscript_settings():
    tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    table = (PAPER / "generated_gate_table.tex").read_text(encoding="utf-8")
    if "citebordercolor={0 0.82 0}" not in tex:
        fail("bright boxed citation settings missing")
    if ">=" in table or "<=" in table:
        fail("raw comparison operators leaked into generated gate table")
    if r"\geq" not in table or r"\leq" not in table:
        fail("math comparison symbols missing from generated gate table")


def main():
    summary = check_summary()
    check_rows(summary)
    check_pdf()
    check_artifact_locations()
    check_latex_log()
    check_manuscript_settings()
    print("Paper 112 validation passed.")


if __name__ == "__main__":
    main()
