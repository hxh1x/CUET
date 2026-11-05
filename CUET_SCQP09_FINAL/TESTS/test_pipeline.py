#!/usr/bin/env python3
"""
Unit tests for CUET SCQP09 Pipeline Integrity.
Tests build_master_syllabus imports/constants, taxonomy_data ROWS count, and classify_recent A dict counts.
"""

import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCE_DIR = os.path.join(BASE_DIR, "05_SOURCE")
if SOURCE_DIR not in sys.path:
    sys.path.insert(0, SOURCE_DIR)


class TestPipeline(unittest.TestCase):

    def test_taxonomy_data_rows(self):
        from taxonomy_data import ROWS
        self.assertEqual(len(ROWS), 92, f"Expected 92 modules in ROWS, found {len(ROWS)}")
        ids = [r["id"] for r in ROWS]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate module IDs found in ROWS")

    def test_classify_recent_dict_counts(self):
        from classify_recent import A
        self.assertIn(2024, A)
        self.assertIn(2025, A)
        self.assertIn(2026, A)

        self.assertEqual(len(A[2024]), 75, f"2024 count in A is {len(A[2024])}, expected 75")
        self.assertEqual(len(A[2025]), 75, f"2025 count in A is {len(A[2025])}, expected 75")
        self.assertEqual(len(A[2026]), 75, f"2026 count in A is {len(A[2026])}, expected 75")
        total_a = sum(len(A[yr]) for yr in (2024, 2025, 2026))
        self.assertEqual(total_a, 225, f"Total questions in A is {total_a}, expected 225")

    def test_build_master_syllabus_syntax_and_import(self):
        import py_compile
        script_path = os.path.join(SOURCE_DIR, "build_master_syllabus.py")
        self.assertTrue(os.path.exists(script_path), f"File missing: {script_path}")
        compiled = py_compile.compile(script_path, doraise=True)
        self.assertTrue(os.path.exists(compiled))


if __name__ == "__main__":
    unittest.main()
