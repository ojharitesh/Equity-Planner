# Inclusive Test Planner

Inclusive Test Planner is a small Python command-line tool for software teams. It asks a few simple questions about a project and creates an `inclusive-test-plan.md` checklist with practical ideas for testing with people who have different abilities, languages, ages, backgrounds, and levels of technical experience.

## Why it matters

Teams can easily test only with people who share their own experiences. This tool creates a prompt to consider perspectives that may otherwise be missed. It is connected to **Building Multicultural Capacity** because it encourages developers to learn from people whose abilities, languages, cultures, and life experiences differ from their own.

It is also connected to **Making Diversity Actionable**. Instead of leaving equity as a broad goal, the tool turns it into concrete activities: try the product with a screen reader, complete tasks by keyboard, review translations, check contrast, and examine privacy and safety decisions.

The generated plan is a starting checklist for human review. It cannot prove that software is fair or inclusive. Meaningful review still requires listening to and working with people who represent the product's users.

## Installation

1. Install Python 3.10 or newer.
2. Clone or download this repository.
3. Open a terminal in the project directory.

The tool uses only Python's standard library, so no package installation is required.

## Usage

Run the interactive planner:

```bash
python3 inclusive_test_planner.py
```

It asks:

- **What type of project is it?** You can enter a website, mobile app, student portal, health app, game, or another project type.
- **Does it collect personal information?** Answer `y` for yes or `n` for no.
- **Does it support multiple languages?** Answer `y` for yes or `n` for no.
- **Who are its expected users?** Describe the audience, such as students and families, older adults new to smartphones, patients and caregivers, or people who use screen readers.

These are suggestions, not a fixed menu. You can type a project type and user group that better match your project.

The answers are saved to `inclusive-test-plan.md`. For a repeatable command, use non-interactive options:

```bash
python inclusive_test_planner.py --non-interactive \
	--project-type "student portal" \
	--supports-multiple-languages \
	--expected-users "students, families, and staff"
```

Example output:

```text
Success: created inclusive-test-plan.md with 8 testing suggestions.
Review the checklist with people who bring perspectives different from your own.
```

The Markdown file includes checks for screen-reader users, keyboard-only users, readable text and color contrast, languages and cultures, ages and technical experience, and privacy and safety.

## Project structure

```text
inclusive_test_planner.py       # CLI, recommendation logic, and Markdown generation
test_inclusive_test_planner.py  # Tests for recommendations and file output
inclusive-test-plan.md          # Generated result; created after running the tool
README.md                       # Project documentation
```

## Run the tests

```bash
python3 -m unittest -v
```

## Limitations and future improvements

- The suggestions are general prompts, not a complete accessibility audit or a guarantee of fairness.
- The tool does not replace usability research with people who use assistive technology or speak the supported languages.
- Future versions could add more project-specific questions, export formats, localization guidance, and links to accessibility standards.
- A future version could let teams record findings, owners, priorities, and follow-up dates in the generated plan.