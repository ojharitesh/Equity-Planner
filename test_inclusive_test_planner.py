import tempfile
import unittest
from pathlib import Path

from inclusive_test_planner import (
    ProjectAnswers,
    build_markdown,
    main,
    recommend_tests,
)


class RecommendationTests(unittest.TestCase):
    def test_recommends_privacy_and_language_checks_when_relevant(self):
        answers = ProjectAnswers("health app", True, True, "patients and caregivers")

        suggestions = recommend_tests(answers)

        joined = " ".join(suggestions).lower()
        self.assertIn("privacy and safety", joined)
        self.assertIn("switch languages", joined)
        self.assertIn("patients and caregivers", joined)

    def test_recommends_language_access_and_minimal_data_checks_when_not_relevant(self):
        answers = ProjectAnswers("calculator", False, False, "older adults")

        suggestions = recommend_tests(answers)

        joined = " ".join(suggestions).lower()
        self.assertIn("language access", joined)
        self.assertIn("does not request unnecessary personal information", joined)
        self.assertIn("older adults", joined)

    def test_markdown_contains_human_review_limitation(self):
        answers = ProjectAnswers("website", False, False, "students")

        markdown = build_markdown(answers, ["Check the workflow."])

        self.assertIn("# Inclusive Test Plan", markdown)
        self.assertIn("- [ ] Check the workflow.", markdown)
        self.assertIn("cannot prove that software is fair", markdown)

    def test_non_interactive_main_writes_requested_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "plan.md"

            result = main(
                [
                    "--non-interactive",
                    "--project-type",
                    "mobile app",
                    "--supports-multiple-languages",
                    "--output",
                    str(output_path),
                ]
            )

            self.assertEqual(result, 0)
            self.assertTrue(output_path.exists())
            self.assertIn("mobile app", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
