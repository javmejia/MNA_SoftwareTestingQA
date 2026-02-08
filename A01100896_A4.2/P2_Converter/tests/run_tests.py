#!/usr/bin/env python3
"""Run convertNumbers against all test cases and compare results."""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(ROOT_DIR, "source")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
EXPECTED_FILE = os.path.join(RESULTS_DIR, "A4.2.P2.ExpectedResults.txt")
ACTUAL_FILE = os.path.join(RESULTS_DIR, "A4.2.P2.ActualResults.txt")
COMPARISON_FILE = os.path.join(RESULTS_DIR, "A4.2.P2.Comparison.txt")

sys.path.insert(0, SOURCE_DIR)

# pylint: disable=wrong-import-position
from convertNumbers import convert_value, parse_numbers  # noqa: E402


def list_test_cases() -> List[str]:
    """List test case files in the tests folder."""
    files = [
        name
        for name in os.listdir(SCRIPT_DIR)
        if name.startswith("TC") and name.endswith(".txt")
    ]
    files.sort()
    return files


def build_row(raw_text: str, value: int | None) -> Tuple[str, str, str]:
    """Build output row values for binary and hex."""
    if value is None:
        return raw_text, "#VALUE!", "#VALUE!"
    binary, hexadecimal = convert_value(value)
    return raw_text, binary, hexadecimal


def write_actual_file(test_files: List[str], output_path: str) -> None:
    """Write actual conversion results for every test case."""
    lines: List[str] = []
    for test_file in test_files:
        tc_name = os.path.splitext(test_file)[0]
        file_path = os.path.join(SCRIPT_DIR, test_file)
        values = parse_numbers(file_path)

        lines.append(f"ITEM\t{tc_name}\tBIN\tHEX")
        for index, (raw_text, value) in enumerate(values, start=1):
            text_value, binary, hexadecimal = build_row(raw_text, value)
            lines.append(f"{index}\t{text_value}\t{binary}\t{hexadecimal}")
        lines.append("")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(lines).rstrip() + "\n")


def parse_expected_sections(path: str) -> Dict[str, List[List[str]]]:
    """Parse expected/actual file into a dict of tc -> rows."""
    sections: Dict[str, List[List[str]]] = {}
    current_tc = ""
    with open(path, "r", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("ITEM"):
                header_parts = [part for part in line.split("\t") if part != ""]
                current_tc = header_parts[1] if len(header_parts) > 1 else ""
                sections[current_tc] = []
                continue
            parts = line.split("\t")
            sections[current_tc].append(parts)
    return sections


def normalize_row(parts: List[str]) -> Tuple[str, str, str, str]:
    """Normalize row values to item, value, bin, hex."""
    if len(parts) >= 4:
        if len(parts) == 5:
            # Handle TC1 extra column case in expected file.
            parts = [parts[0]] + parts[2:]
        return parts[0], parts[1], parts[2], parts[3]
    if len(parts) == 3:
        return parts[0], parts[1], parts[2], ""
    return "", "", "", ""


def write_comparison(expected_path: str, actual_path: str, output_path: str) -> None:
    """Write a comparison report between expected and actual files."""
    # pylint: disable=too-many-locals
    expected = parse_expected_sections(expected_path)
    actual = parse_expected_sections(actual_path)

    lines = ["TC\tITEM\tEXP_VAL\tACT_VAL\tEXP_BIN\tACT_BIN\tEXP_HEX\tACT_HEX\tMATCH"]
    mismatch_count = 0

    for tc_name in sorted(expected.keys()):
        exp_rows = expected.get(tc_name, [])
        act_rows = actual.get(tc_name, [])
        max_len = max(len(exp_rows), len(act_rows))
        for index in range(max_len):
            exp_parts = exp_rows[index] if index < len(exp_rows) else []
            act_parts = act_rows[index] if index < len(act_rows) else []
            exp_item, exp_val, exp_bin, exp_hex = normalize_row(exp_parts)
            act_item, act_val, act_bin, act_hex = normalize_row(act_parts)

            match = (
                exp_val == act_val
                and exp_bin == act_bin
                and exp_hex == act_hex
                and exp_item == act_item
            )
            if not match:
                mismatch_count += 1

            item = exp_item or act_item
            lines.append(
                f"{tc_name}\t{item}\t{exp_val}\t{act_val}\t"
                f"{exp_bin}\t{act_bin}\t{exp_hex}\t{act_hex}\t{str(match)}"
            )

    lines.append(f"MISMATCHES\t{mismatch_count}")
    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(lines) + "\n")


def main() -> int:
    """Run all test cases and generate comparison files."""
    test_files = list_test_cases()
    if not test_files:
        print("No test cases found in tests folder.")
        return 1

    write_actual_file(test_files, ACTUAL_FILE)

    if not os.path.exists(EXPECTED_FILE):
        print("Expected results file not found.")
        return 1

    write_comparison(EXPECTED_FILE, ACTUAL_FILE, COMPARISON_FILE)
    print(f"Wrote: {ACTUAL_FILE}")
    print(f"Wrote: {COMPARISON_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
