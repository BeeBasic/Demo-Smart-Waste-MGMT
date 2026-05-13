"""
Tests for README.md content introduced in this PR.

The PR added a new README.md with the content "Testing CodeRabbit PR review".
These tests verify the file's existence, content, and structure.
"""

import os
import pathlib

import pytest

# Resolve the repository root relative to this test file
REPO_ROOT = pathlib.Path(__file__).parent.parent
README_PATH = REPO_ROOT / "README.md"

EXPECTED_CONTENT = "Testing CodeRabbit PR review"


class TestReadmeExists:
    """Tests that verify the README.md file is present in the repository."""

    def test_readme_file_exists(self):
        """README.md must exist at the repository root."""
        assert README_PATH.exists(), f"README.md not found at {README_PATH}"

    def test_readme_is_a_file(self):
        """README.md must be a regular file, not a directory or symlink."""
        assert README_PATH.is_file(), f"{README_PATH} is not a regular file"

    def test_readme_is_not_empty(self):
        """README.md must not be an empty file."""
        assert README_PATH.stat().st_size > 0, "README.md is empty"


class TestReadmeContent:
    """Tests that verify the exact content added in this PR."""

    @pytest.fixture(autouse=True)
    def read_readme(self):
        """Read the README.md content once for all tests in this class."""
        self.content = README_PATH.read_text(encoding="utf-8")

    def test_readme_contains_expected_text(self):
        """README.md must contain the PR-introduced text."""
        assert EXPECTED_CONTENT in self.content

    def test_readme_content_matches_exactly(self):
        """README.md content must match exactly what was added in the PR (no extra text)."""
        assert self.content == EXPECTED_CONTENT

    def test_readme_starts_with_expected_text(self):
        """README.md must start with the expected content string."""
        assert self.content.startswith(EXPECTED_CONTENT)

    def test_readme_has_no_leading_whitespace(self):
        """README.md content must not have unexpected leading whitespace."""
        assert not self.content.startswith((" ", "\t", "\n")), (
            "README.md content has unexpected leading whitespace"
        )

    def test_readme_has_no_trailing_newline(self):
        """README.md was added without a trailing newline (per the PR diff)."""
        assert not self.content.endswith("\n"), (
            "README.md should not have a trailing newline based on the PR diff"
        )

    def test_readme_encoding_is_valid_utf8(self):
        """README.md must be readable as valid UTF-8 text."""
        raw_bytes = README_PATH.read_bytes()
        decoded = raw_bytes.decode("utf-8")
        assert decoded == self.content

    def test_readme_text_is_not_blank(self):
        """README.md content must not be blank or whitespace-only."""
        assert self.content.strip() != "", "README.md contains only whitespace"


class TestReadmeBoundaryAndRegression:
    """Boundary and regression tests for the README.md content."""

    @pytest.fixture(autouse=True)
    def read_readme(self):
        self.content = README_PATH.read_text(encoding="utf-8")

    def test_readme_does_not_contain_placeholder_text(self):
        """README.md must not contain common placeholder/template text."""
        placeholders = ["TODO", "FIXME", "lorem ipsum", "placeholder"]
        for placeholder in placeholders:
            assert placeholder.lower() not in self.content.lower(), (
                f"README.md contains placeholder text: '{placeholder}'"
            )

    def test_readme_word_count(self):
        """README.md should contain exactly 4 words as introduced in the PR."""
        words = self.content.split()
        assert len(words) == 4, (
            f"Expected 4 words in README.md, found {len(words)}: {words}"
        )

    def test_readme_line_count(self):
        """README.md should contain exactly one line of content."""
        # splitlines() handles the case where there is no trailing newline
        lines = self.content.splitlines()
        assert len(lines) == 1, (
            f"Expected 1 line in README.md, found {len(lines)}"
        )

    def test_readme_first_line_equals_expected(self):
        """The first (and only) line of README.md must equal the expected content."""
        first_line = self.content.splitlines()[0]
        assert first_line == EXPECTED_CONTENT

    def test_readme_path_is_at_repo_root(self):
        """README.md must reside at the repository root, not in a subdirectory."""
        assert README_PATH.parent == REPO_ROOT
