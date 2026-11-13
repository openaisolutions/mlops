import json
import tempfile
import unittest
from pathlib import Path

from measurement import measure, write_report


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).parent / "example.json").read_text())

    def values(self, data):
        return {m["metric_id"]: m for m in measure(data, "test-digest")["metrics"]}

    def test_known_engineering_example(self):
        rows = self.values(self.data)
        for key, expected in {
            "defect_density_per_kesloc": 0.8,
            "productivity_esloc_per_hour": 4.1,
            "test_execution_pct": 75,
            "test_pass_of_executed_pct": 68 / 75 * 100,
            "test_pass_of_planned_pct": 68,
            "line_coverage_pct": 90.2,
            "requirements_volatility_pct": 15.625,
            "rework_hours_share_pct": 12,
        }.items():
            self.assertAlmostEqual(rows[key]["metric_value"], expected)

    def test_missing_fixes_are_not_invented_from_caption(self):
        self.assertEqual(
            self.values(self.data)["rework_fixes_per_hour"]["quality_status"],
            "missing_input",
        )

    def test_zero_denominator_unavailable(self):
        self.data["facts"]["tests"] = dict(planned=0, executed=0, passed=0, failed=0)
        self.assertIsNone(self.values(self.data)["test_execution_pct"]["metric_value"])

    def test_rejects_nonfinite_and_negative(self):
        for value in [-1, float("nan"), float("inf"), True]:
            with self.subTest(value=value):
                self.data["facts"]["size"]["delivered_esloc"] = value
                with self.assertRaises(ValueError):
                    self.values(self.data)

    def test_test_counts_reconcile(self):
        self.data["facts"]["tests"]["passed"] = 200
        with self.assertRaises(ValueError):
            self.values(self.data)

    def test_scope_missing_suppresses_cross_source_rates(self):
        del self.data["metadata"]["release_id"]
        self.assertIsNone(
            self.values(self.data)["productivity_esloc_per_hour"]["metric_value"]
        )

    def test_stock_and_change_denominators_are_distinct(self):
        rows = self.values(self.data)
        self.assertNotEqual(
            rows["defect_density_per_kesloc"]["denominator"],
            rows["change_defect_density_per_kesloc"]["denominator"],
        )

    def test_html_escapes_untrusted_content(self):
        result = measure(self.data, "<script>alert(1)</script>")
        with tempfile.TemporaryDirectory() as tmp:
            write_report(result, Path(tmp))
            text = (Path(tmp) / "dashboard.html").read_text()
            self.assertNotIn("<script>", text)
            self.assertIn("&lt;script&gt;", text)
            self.assertEqual(
                len(json.loads((Path(tmp) / "SHA256SUMS.json").read_text())), 3
            )

    def test_unrecognized_metadata_is_not_exported(self):
        self.data["metadata"]["api_key"] = "example-secret-not-for-reports"
        result = measure(self.data, "digest")
        self.assertNotIn("example-secret-not-for-reports", json.dumps(result))

    def test_conflicting_source_scope_is_rejected(self):
        self.data["facts"]["labor"]["csci_id"] = "OTHER-CSCI"
        with self.assertRaisesRegex(ValueError, "scope mismatch"):
            measure(self.data, "digest")


if __name__ == "__main__":
    unittest.main()
