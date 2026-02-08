#!/usr/bin/env python3
"""Run computeStatistics against all test cases and compare results."""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(ROOT_DIR, "source")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
EXPECTED_FILE = os.path.join(RESULTS_DIR, "A4.2.P1.ExpectedResults.txt")
ACTUAL_FILE = os.path.join(RESULTS_DIR, "A4.2.P1.ActualResults.txt")
COMPARISON_FILE = os.path.join(RESULTS_DIR, "A4.2.P1.Comparison.txt")

sys.path.insert(0, SOURCE_DIR)

# pylint: disable=wrong-import-position
from computeStatistics import (  # noqa: E402
    compute_statistics,
    format_mode,
    format_number,
    parse_numbers,
)

METRIC_ORDER = ["COUNT", "MEAN", "MEDIAN", "MODE", "SD", "VARIANCE"]


def list_test_cases() -> List[str]:
    """List test case files in the tests folder."""
    files = [
        name
        for name in os.listdir(SCRIPT_DIR)
        if name.startswith("TC") and name.endswith(".txt")
    ]
    files.sort()
    return files


def build_actual_table(test_files: List[str]) -> Dict[str, Dict[str, str]]:
    """Build actual results table for each metric and test case."""
    table: Dict[str, Dict[str, str]] = {metric: {} for metric in METRIC_ORDER}
    for test_file in test_files:
        tc_name = os.path.splitext(test_file)[0]
        file_path = os.path.join(SCRIPT_DIR, test_file)
        values = parse_numbers(file_path)
        stats = compute_statistics(values)
        table["COUNT"][tc_name] = format_number(stats["count"])
        table["MEAN"][tc_name] = format_number(stats["mean"])
        table["MEDIAN"][tc_name] = format_number(stats["median"])
        table["MODE"][tc_name] = format_mode(stats["mode"])
        table["SD"][tc_name] = format_number(stats["sd"])
        table["VARIANCE"][tc_name] = format_number(stats["variance"])
    return table


def write_results_table(
    test_files: List[str],
    table: Dict[str, Dict[str, str]],
    output_path: str,
) -> None:
    """Write a tab-separated results table to disk."""
    tcs = [os.path.splitext(name)[0] for name in test_files]
    header = ["TC"] + tcs
    lines = ["\t".join(header)]
    for metric in METRIC_ORDER:
        row = [metric] + [table[metric].get(tc, "") for tc in tcs]
        lines.append("\t".join(row))
    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(lines) + "\n")


def parse_expected(path: str) -> Tuple[List[str], Dict[str, Dict[str, str]]]:
    """Parse expected/actual tab-separated file into a table."""
    with open(path, "r", encoding="utf-8") as file_handle:
        lines = [line.strip() for line in file_handle if line.strip()]
    header = lines[0].split("\t")
    tcs = header[1:]
    table: Dict[str, Dict[str, str]] = {}
    for line in lines[1:]:
        parts = line.split("\t")
        metric = parts[0]
        values = parts[1:]
        table[metric] = dict(zip(tcs, values))
    return tcs, table


def is_numeric(value: str) -> bool:
    """Return True when the string can be parsed as float."""
    try:
        float(value)
    except ValueError:
        return False
    return True


def compare_values(expected: str, actual: str, tol: float = 1e-6) -> bool:
    """Compare expected vs actual with tolerance for numeric values."""
    if expected == "#N/A":
        return actual == "#N/A"
    if is_numeric(expected) and is_numeric(actual):
        expected_val = float(expected)
        actual_val = float(actual)
        diff = abs(expected_val - actual_val)
        scale = max(1.0, abs(expected_val))
        return diff <= tol * scale
    return expected == actual


def write_comparison(expected_path: str, actual_path: str, output_path: str) -> None:
    """Write comparison file ordered by test case then metric."""
    # pylint: disable=too-many-locals
    tcs, exp_table = parse_expected(expected_path)
    _, act_table = parse_expected(actual_path)

    lines = ["TC\tMETRIC\tEXPECTED\tACTUAL\tMATCH"]
    mismatch_count = 0

    for tc in tcs:
        for metric in METRIC_ORDER:
            expected = exp_table.get(metric, {}).get(tc, "")
            actual = act_table.get(metric, {}).get(tc, "")
            match = compare_values(expected, actual)
            if not match:
                mismatch_count += 1
            lines.append(f"{tc}\t{metric}\t{expected}\t{actual}\t{str(match)}")

    lines.append(f"MISMATCHES\t{mismatch_count}")
    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(lines) + "\n")


def main() -> int:
    """Run all test cases and generate comparison files."""
    test_files = list_test_cases()
    if not test_files:
        print("No test cases found in tests folder.")
        return 1

    actual_table = build_actual_table(test_files)
    write_results_table(test_files, actual_table, ACTUAL_FILE)

    if not os.path.exists(EXPECTED_FILE):
        print("Expected results file not found.")
        return 1

    write_comparison(EXPECTED_FILE, ACTUAL_FILE, COMPARISON_FILE)
    print(f"Wrote: {ACTUAL_FILE}")
    print(f"Wrote: {COMPARISON_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
