"""Build a beginner-friendly starting checklist for inclusive testing."""

import argparse
import dataclasses
import pathlib


DEFAULT_OUTPUT = "inclusive-test-plan.md"


@dataclasses.dataclass
class ProjectAnswers:
    """Answers collected from the project team."""

    project_type: str
    collects_personal_information: bool
    supports_multiple_languages: bool
    expected_users: str


def recommend_tests(answers: ProjectAnswers) -> list[str]:
    """Return practical testing suggestions based on project answers."""
    suggestions = [
        "Screen-reader users: Test headings, labels, focus order, status messages, and image descriptions with a screen reader.",
        "Keyboard-only users: Complete every important task without a mouse and check visible focus, logical tab order, and keyboard-operable controls.",
        "Readable text and color contrast: Check text size, plain-language instructions, zoom to 200%, contrast, color-independent errors, and reduced motion.",
        "Different ages and technical experience: Ask people with different ages and familiarity with technology to try realistic tasks; observe confusing words, steps, and recovery from errors.",
        "Different languages and cultures: Review translations with fluent speakers, test longer translated text, dates, names, numbers, icons, and culturally specific assumptions.",
    ]

    if answers.supports_multiple_languages:
        suggestions.append(
            "Language support: Switch languages during key workflows and verify that every message, validation error, email, and help link is translated."
        )
    else:
        suggestions.append(
            "Language access: Check whether people who are not fluent in the primary language can understand the most important content and find help."
        )

    if answers.collects_personal_information:
        suggestions.append(
            "Privacy and safety: Test consent, data minimization, field explanations, privacy settings, access controls, secure error messages, and account recovery without exposing personal information."
        )
    else:
        suggestions.append(
            "Privacy and safety: Confirm that the product does not request unnecessary personal information and that logs and error messages avoid exposing user data."
        )

    if answers.expected_users.strip():
        suggestions.append(
            f"Expected users: Include people represented by '{answers.expected_users.strip()}' in review sessions, and record whose perspective is still missing."
        )

    suggestions.append(
        f"Project context ({answers.project_type.strip()}): Test the complete journey on the devices, connection speeds, and assistive tools your users are likely to have."
    )
    return suggestions


def build_markdown(answers: ProjectAnswers, suggestions: list[str]) -> str:
    """Format a generated plan as Markdown."""
    personal_data = "Yes" if answers.collects_personal_information else "No"
    multiple_languages = "Yes" if answers.supports_multiple_languages else "No"
    checklist = "\n".join(f"- [ ] {suggestion}" for suggestion in suggestions)
    return f"""# Inclusive Test Plan

## Project snapshot

- **Project type:** {answers.project_type.strip()}
- **Collects personal information:** {personal_data}
- **Supports multiple languages:** {multiple_languages}
- **Expected users:** {answers.expected_users.strip() or "Not specified"}

## Starting checklist

{checklist}

## Human review reminder

This checklist is a starting point for human review. It cannot prove that software is fair or inclusive. Talk with people who have different abilities, languages, ages, backgrounds, and levels of technical experience, then prioritize and document what you learn.
"""


def ask_yes_no(prompt: str, input_func=input) -> bool:
    """Ask a yes/no question until the user enters a recognizable answer."""
    while True:
        answer = input_func(f"{prompt} (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y/yes or n/no.")


def collect_answers(input_func=input) -> ProjectAnswers:
    """Collect project details from an interactive user."""
    print("\nInclusive Test Planner")
    print("Answer a few questions to create a starting checklist.\n")
    project_type = input_func("What type of project is it? ").strip()
    while not project_type:
        print("Please enter a project type.")
        project_type = input_func("What type of project is it? ").strip()
    collects_personal_information = ask_yes_no(
        "Does it collect personal information?", input_func
    )
    supports_multiple_languages = ask_yes_no(
        "Does it support multiple languages?", input_func
    )
    expected_users = input_func("Who are its expected users? ").strip()
    return ProjectAnswers(
        project_type,
        collects_personal_information,
        supports_multiple_languages,
        expected_users,
    )


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Create a human-centered starting checklist for inclusive testing."
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Markdown file to create (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Use the supplied answer options instead of asking questions.",
    )
    parser.add_argument("--project-type", help="Project type for non-interactive use")
    parser.add_argument(
        "--collects-personal-information",
        action="store_true",
        help="Mark the project as collecting personal information.",
    )
    parser.add_argument(
        "--supports-multiple-languages",
        action="store_true",
        help="Mark the project as supporting multiple languages.",
    )
    parser.add_argument("--expected-users", default="", help="Expected users")
    return parser.parse_args(arguments)


def main(arguments: list[str] | None = None) -> int:
    """Run the command-line tool and write the generated plan."""
    args = parse_args(arguments)
    try:
        if args.non_interactive:
            if not args.project_type:
                raise ValueError("--project-type is required with --non-interactive")
            answers = ProjectAnswers(
                args.project_type,
                args.collects_personal_information,
                args.supports_multiple_languages,
                args.expected_users,
            )
        else:
            answers = collect_answers()
        suggestions = recommend_tests(answers)
        output_path = pathlib.Path(args.output)
        output_path.write_text(build_markdown(answers, suggestions), encoding="utf-8")
    except (OSError, ValueError) as error:
        print(f"Error: could not create the inclusive test plan: {error}")
        return 1

    print(
        f"Success: created {output_path} with {len(suggestions)} testing suggestions."
    )
    print(
        "Review the checklist with people who bring perspectives different from your own."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
