import unittest

from src.testing_strategy import RISKS, matrix_rows, prioritize


class TestingStrategyTests(unittest.TestCase):
    def test_priority_is_impact_times_likelihood(self):
        first = RISKS[0]
        self.assertEqual(first.priority, 20)

    def test_priority_and_tie_break_are_deterministic(self):
        names = [risk.name for risk in prioritize(RISKS)]
        self.assertEqual(
            names,
            [
                "exclude watched titles",
                "protect history",
                "compare director coverage",
                "survive repeated requests",
                "stay responsive under load",
            ],
        )

    def test_matrix_contains_observable_evidence(self):
        rows = matrix_rows(RISKS)
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(row["evidence"] for row in rows))


if __name__ == "__main__":
    unittest.main()
