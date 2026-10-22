from datetime import date
import unittest

from src.framework_map import Escalation, Requirement, escalate, run_review


class FrameworkMapTests(unittest.TestCase):
    def test_missing_evidence_escalates_and_reports_objective(self):
        requirements = [
            Requirement("policy", "governance", "POL-01", "present", "policy-v3"),
            Requirement("performance", "management", "PERF-01", "present"),
        ]
        review = run_review(requirements, "AV-204", date(2026, 10, 21))
        self.assertEqual(review.objective, "Every requirement is present with evidence")
        self.assertFalse(review.criteria_met)
        self.assertEqual(review.status, "escalate")
        self.assertEqual(review.open_gaps, ("performance",))
        self.assertEqual(review.evidence_checked, 1)

    def test_complete_evidence_is_ready(self):
        requirements = [
            Requirement("policy", "governance", "POL-01", "present", "policy-v3"),
        ]
        review = run_review(requirements, "AV-204", date(2026, 10, 21))
        self.assertTrue(review.criteria_met)
        self.assertEqual(review.status, "ready")
        self.assertEqual(escalate(review, "governance-ops", date(2026, 11, 20)), ())

    def test_incomplete_escalation_is_rejected(self):
        requirement = Requirement("performance", "management", "PERF-01", "gap")
        review = run_review([requirement], "AV-204", date(2026, 10, 21))
        with self.assertRaises(ValueError):
            escalate(review, "", date(2026, 11, 20))

    def test_evidence_update_returns_ready_on_next_review(self):
        requirements = [
            Requirement("performance", "management", "PERF-01", "present"),
        ]
        first = run_review(requirements, "AV-204", date(2026, 10, 21))
        self.assertEqual(first.open_gaps, ("performance",))
        updated = [
            replace(requirements[0], evidence_ref="evaluation-2026-10"),
        ]
        second = run_review(updated, "AV-204", date(2026, 11, 20))
        self.assertEqual(second.open_gaps, ())
        self.assertEqual(second.status, "ready")


if __name__ == "__main__":
    unittest.main()
