"""Reproducible measurement evidence; standard library only."""
import argparse
import csv
import hashlib
import html
import json
import math
from pathlib import Path

METHOD = "measurement-companion-1.0"

def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite nonnegative number")
    return value

def measure(document, digest):
    metadata = document.get("metadata", {})
    facts = document.get("facts", {})
    rows = []
    def metric(identifier, section, numerator_key, denominator_key, scale=1, unit="ratio"):
        source = facts.get(section, {})
        n, d = source.get(numerator_key), source.get(denominator_key)
        if n is None or d is None:
            status, value = "missing_input", None
        else:
            n, d = number(n, numerator_key), number(d, denominator_key)
            status, value = ("zero_denominator", None) if d == 0 else ("valid", n / d * scale)
        rows.append(dict(metric_id=identifier, numerator=n, denominator=d, scale=scale,
                         metric_value=value, unit=unit, quality_status=status,
                         method_version=METHOD, evidence_digest=digest,
                         csci_id=metadata.get("csci_id"), release_id=metadata.get("release_id")))
    tests = facts.get("tests", {})
    if all(k in tests for k in ("planned", "executed", "passed", "failed")):
        for k, v in tests.items():
            number(v, k)
        if tests["executed"] > tests["planned"] or tests["passed"] + tests["failed"] != tests["executed"]:
            raise ValueError("Tests require executed <= planned and passed + failed = executed")
    size, defects, labor = facts.get("size", {}), facts.get("defects", {}), facts.get("labor", {})
    combined = {**size, **defects, **labor}
    facts = {**facts, "joined": combined}
    requirements = facts.get("requirements", {})
    changed = [requirements.get(k) for k in ("added", "removed", "materially_modified")]
    facts["requirements"] = {**requirements, "changed": sum(number(v, "requirement change") for v in changed) if all(v is not None for v in changed) else None}
    metric("defect_density_per_kesloc", "joined", "verified_eligible", "delivered_esloc", 1000, "defects/kESLOC")
    metric("change_defect_density_per_kesloc", "joined", "verified_eligible", "incremental_esloc", 1000, "defects/kESLOC changed")
    metric("productivity_esloc_per_hour", "joined", "incremental_esloc", "actual_engineering_hours", 1, "eSLOC/hour")
    metric("test_execution_pct", "tests", "executed", "planned", 100, "%")
    metric("test_pass_of_executed_pct", "tests", "passed", "executed", 100, "%")
    metric("test_pass_of_planned_pct", "tests", "passed", "planned", 100, "%")
    metric("line_coverage_pct", "coverage", "covered_lines", "lines_to_cover", 100, "%")
    metric("requirements_volatility_pct", "requirements", "changed", "opening", 100, "%")
    metric("rework_fixes_per_hour", "joined", "verified_fixes", "corrective_hours", 1, "fixes/hour")
    metric("rework_hours_share_pct", "joined", "corrective_hours", "actual_engineering_hours", 100, "%")
    for section, low, high in (("coverage", "covered_lines", "lines_to_cover"), ("labor", "corrective_hours", "actual_engineering_hours")):
        s = facts.get(section, {})
        if low in s and high in s and number(s[low], low) > number(s[high], high):
            raise ValueError(f"{low} cannot exceed {high}")
    # Cross-source figures may only be joined when the input declares a common scope.
    if not metadata.get("csci_id") or not metadata.get("release_id"):
        for row in rows:
            if row["metric_id"] in {"defect_density_per_kesloc", "change_defect_density_per_kesloc", "productivity_esloc_per_hour", "rework_fixes_per_hour"}:
                row.update(metric_value=None, quality_status="missing_scope")
    return {"method_version": METHOD, "synthetic": metadata.get("synthetic", False),
            "metadata": metadata, "input_sha256": digest, "metrics": rows,
            "limitations": ["Scope and source authorization must be verified by the reporting owner.",
              "Provided eSLOC is not inferred from Git additions/deletions.",
              "A valid calculation does not establish acceptance, compliance, or release authorization."]}

def write_report(result, output):
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (output / "metric_result.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result["metrics"][0]))
        writer.writeheader()
        writer.writerows(result["metrics"])
    body = "".join("<tr>" + "".join("<td>" + html.escape(str(row[k])) + "</td>" for k in
        ("metric_id", "metric_value", "unit", "quality_status", "numerator", "denominator")) + "</tr>" for row in result["metrics"])
    banner = "SYNTHETIC TEACHING DATA" if result["synthetic"] else "SOURCE-SUPPLIED MEASUREMENTS - owner verification required"
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Measurement evidence</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;color:#14243b}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd6e0;padding:10px;text-align:left}h1{color:#073c68}.banner{background:#fff0bb;padding:16px}code{overflow-wrap:anywhere}</style><h1>Measurement evidence</h1><p class="banner">' + banner + '</p><p>Input SHA-256: <code>' + html.escape(result["input_sha256"]) + '</code></p><table><tr><th>Metric</th><th>Value</th><th>Unit</th><th>Quality</th><th>Numerator</th><th>Denominator</th></tr>' + body + '</table><p>Missing data is unavailable, not zero. Review scope, acceptance and source evidence before use.</p></html>'
    (output / "dashboard.html").write_text(page, encoding="utf-8")
    evidence = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir()) if p.name != "SHA256SUMS.json" and p.is_file()}
    (output / "SHA256SUMS.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    if len(raw) > 4 * 1024 * 1024:
        raise ValueError("Measurement input exceeds 4 MiB")
    result = measure(json.loads(raw), hashlib.sha256(raw).hexdigest())
    write_report(result, args.output)

if __name__ == "__main__":
    main()

