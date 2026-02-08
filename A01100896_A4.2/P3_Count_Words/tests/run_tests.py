#!/usr/bin/env python3
"""Run wordCount against all test cases and compare results."""

from __future__ import annotations

import os
import sys
from typing import Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(ROOT_DIR, "source")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
CONSOLIDATED_COMPARISON = os.path.join(RESULTS_DIR, "P3.Comparison.txt")

sys.path.insert(0, SOURCE_DIR)

# pylint: disable=wrong-import-position
from wordCount import count_words, parse_words  # noqa: E402


def list_test_cases() -> List[str]:
    """List test case files in the tests folder."""
    files = [
        name
        for name in os.listdir(SCRIPT_DIR)
        if name.startswith("TC") and name.endswith(".txt")
    ]
    files.sort()
    return files


def is_header_line(parts: List[str]) -> bool:
    """Return True when the line is a header."""
    return len(parts) >= 2 and parts[0] == "Row Labels"


def load_expected_order(expected_path: str) -> List[str]:
    """Load expected word order from an expected results file."""
    order: List[str] = []
    with open(expected_path, "r", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            line = raw_line.strip()
            if line == "":
                continue
            parts = line.split("\t")
            if is_header_line(parts):
                continue
            if parts[0] == "Grand Total":
                continue
            order.append(parts[0])
    return order


def write_actual_file(
    tc_name: str,
    counts: Dict[str, int],
    expected_order: List[str],
    output_path: str,
) -> None:
    """Write actual results in the same order as expected file."""
    lines = [f"Row Labels\tCount of {tc_name}"]
    seen = set()

    for word in expected_order:
        seen.add(word)
        count = counts.get(word, 0)
        lines.append(f"{word}\t{count}")

    for word, count in counts.items():
        if word in seen:
            continue
        lines.append(f"{word}\t{count}")

    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(lines) + "\n")


def load_expected_counts(expected_path: str) -> Dict[str, int]:
    """Load expected counts from file."""
    counts: Dict[str, int] = {}
    with open(expected_path, "r", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            line = raw_line.strip()
            if line == "":
                continue
            parts = line.split("\t")
            if is_header_line(parts):
                continue
            if len(parts) >= 2:
                if parts[0] == "Grand Total":
                    continue
                counts[parts[0]] = int(parts[1])
    return counts


def build_comparison_rows(
    tc_name: str,
    expected_counts: Dict[str, int],
    actual_counts: Dict[str, int],
) -> List[str]:
    """Build comparison lines ordered alphabetically for a test case."""
    lines: List[str] = []
    lines.append(f"{tc_name}\t---\t---\t---\t---")

    all_words = set(expected_counts.keys()) | set(actual_counts.keys())
    for word in sorted(all_words):
        exp = expected_counts.get(word)
        act = actual_counts.get(word)
        match = exp == act
        lines.append(f"{tc_name}\t{word}\t{exp}\t{act}\t{str(match)}")

    return lines


def write_consolidated_comparison(rows: List[str]) -> None:
    """Write consolidated comparison file for all test cases."""
    header = "TC\tWORD\tEXP_COUNT\tACT_COUNT\tMATCH"
    with open(CONSOLIDATED_COMPARISON, "w", encoding="utf-8") as file_handle:
        file_handle.write(header + "\n")
        file_handle.write("\n".join(rows) + "\n")


def main() -> int:
    """Run all test cases and generate actual/comparison files."""
    test_files = list_test_cases()
    if not test_files:
        print("No test cases found in tests folder.")
        return 1

    consolidated_rows: List[str] = []

    for test_file in test_files:
        tc_name = os.path.splitext(test_file)[0]
        test_path = os.path.join(SCRIPT_DIR, test_file)
        expected_path = os.path.join(RESULTS_DIR, f"{tc_name}.ExpectedResults.txt")
        actual_path = os.path.join(RESULTS_DIR, f"{tc_name}.ActualResults.txt")

        words = parse_words(test_path)
        counts = count_words(words)

        if os.path.exists(expected_path):
            expected_order = load_expected_order(expected_path)
            write_actual_file(tc_name, counts, expected_order, actual_path)
            expected_counts = load_expected_counts(expected_path)
            consolidated_rows.extend(
                build_comparison_rows(tc_name, expected_counts, counts)
            )
            print(f"Wrote: {actual_path}")
        else:
            print(f"Expected results file not found for {tc_name}.")

    write_consolidated_comparison(consolidated_rows)
    print(f"Wrote: {CONSOLIDATED_COMPARISON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
