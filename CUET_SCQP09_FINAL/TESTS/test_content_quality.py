#!/usr/bin/env python3
"""
Unit tests for CUET SCQP09 Pilot Content Quality.
Validates M1 module file exists, has all 19 required sections, no empty sections,
and includes official PYQ source references and category tags.
"""

import os
import re
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
M1_PATH = os.path.join(BASE_DIR, "CURRICULUM", "modules", "M1_Sets_Venn_Inclusion_Exclusion.md")

REQUIRED_SECTIONS = [
    "1. Module Identity & Overview",
    "2. Prerequisites",
    "3. Learning Objectives",
    "4. Required Prior Knowledge",
    "5. Detailed Concept Explanations",
    "6. Terminology & Formal Definitions",
    "7. Mathematical Foundations & Term-by-Term Formulas",
    "8. Visual Explanations (ASCII Venn Diagrams)",
    "9. Worked Examples (Step-by-Step with Full Computations)",
    "10. Common Misconceptions",
    "11. Common Mistakes & Exam Pitfalls",
    "12. Progressive Exercises (12 Structured Drills)",
    "13. Practical Assignment: University Course Enrollment Survey",
    "14. Knowledge-Check Questions (5 MCQs with Explanations)",
    "15. Independent Mastery Assessment (10 Exam-Level Questions)",
    "16. Assessment Rubric & Mastery Criteria",
    "17. Revision Material: Quick-Reference Formula Card",
    "18. Source References",
    "19. Source Category Labels"
]

EXPECTED_PYQS = ["2024 Q26", "2025 Q17", "2025 Q19", "2026 Q21", "2026 Q39"]
EXPECTED_TAGS = ["[SOURCE]", "[DERIVED]", "[SUPPLEMENTARY]"]


class TestContentQuality(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.exists(M1_PATH), f"Pilot module file not found at: {M1_PATH}")
        with open(M1_PATH, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_all_19_sections_present(self):
        for sec in REQUIRED_SECTIONS:
            # Check for header
            prefix = sec.split()[0] # e.g. '1.'
            title_word = sec.split()[1] # e.g. 'Module'
            pattern = rf"##\s+{re.escape(prefix)}\s+.*{re.escape(title_word)}"
            self.assertTrue(re.search(pattern, self.content, re.I),
                            f"Missing required section: {sec}")

    def test_no_empty_sections(self):
        sections = re.split(r"\n##\s+", self.content)
        for sec in sections[1:]: # Skip title block
            lines = [line.strip() for line in sec.split("\n") if line.strip()]
            self.assertGreaterEqual(len(lines), 3,
                                    f"Section appears empty or too brief: {lines[0] if lines else 'UNKNOWN'}")

    def test_source_references_present(self):
        for pyq in EXPECTED_PYQS:
            self.assertIn(pyq, self.content, f"Expected PYQ reference not found: {pyq}")

    def test_source_category_tags_present(self):
        for tag in EXPECTED_TAGS:
            self.assertIn(tag, self.content, f"Expected classification tag not found: {tag}")


if __name__ == "__main__":
    unittest.main()
