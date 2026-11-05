#!/usr/bin/env python3
"""
Unit tests for CUET SCQP09 Data Integrity.
Tests 225 questions, 75 per year, unique year/qno pairs, 92 modules, no duplicates.
"""

import csv
import json
import os
import sys
import unittest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH = os.path.join(BASE_DIR, "02_QUESTION_BANK", "SCQP09_Question_Bank_2024-2026.csv")
JSON_V2_PATH = os.path.join(BASE_DIR, "DATA", "question_bank_v2.json")
TAX_CSV_PATH = os.path.join(BASE_DIR, "01_MASTER_SYLLABUS", "SCQP09_Master_Taxonomy.csv")


class TestDataIntegrity(unittest.TestCase):

    def test_csv_total_count(self):
        self.assertTrue(os.path.exists(CSV_PATH), f"CSV not found: {CSV_PATH}")
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        self.assertEqual(len(reader), 225, f"Expected 225 questions, got {len(reader)}")

    def test_csv_yearly_distribution(self):
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        year_counts = {}
        for r in reader:
            y = r["year"]
            year_counts[y] = year_counts.get(y, 0) + 1

        self.assertEqual(year_counts.get("2024"), 75, "2024 should have 75 questions")
        self.assertEqual(year_counts.get("2025"), 75, "2025 should have 75 questions")
        self.assertEqual(year_counts.get("2026"), 75, "2026 should have 75 questions")

    def test_unique_year_qno_pairs(self):
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        seen = set()
        for r in reader:
            pair = (r["year"], int(r["qno"]))
            self.assertNotIn(pair, seen, f"Duplicate pair found: {pair}")
            seen.add(pair)
        self.assertEqual(len(seen), 225)

    def test_json_v2_integrity_and_english_clean(self):
        self.assertTrue(os.path.exists(JSON_V2_PATH), f"JSON v2 not found: {JSON_V2_PATH}")
        with open(JSON_V2_PATH, "r", encoding="utf-8") as f:
            items = json.load(f)
        self.assertEqual(len(items), 225)

        for item in items:
            self.assertIn("question_id", item)
            self.assertIn("question_text_clean", item)
            clean_text = item["question_text_clean"]
            # Assert zero Devanagari / Hindi characters
            for ch in clean_text:
                self.assertFalse(0x0900 <= ord(ch) <= 0x097F,
                                 f"Devanagari character found in {item['question_id']}")

    def test_taxonomy_module_count_and_uniqueness(self):
        self.assertTrue(os.path.exists(TAX_CSV_PATH), f"Taxonomy CSV not found: {TAX_CSV_PATH}")
        with open(TAX_CSV_PATH, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 92, f"Expected 92 taxonomy modules, got {len(rows)}")

        ids = [r["id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate module IDs found in taxonomy")


if __name__ == "__main__":
    unittest.main()
