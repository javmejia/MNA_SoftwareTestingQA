#!/usr/bin/env python3
"""Compute total sales cost from a price catalogue and sales record JSON files."""
# pylint: disable=invalid-name

from __future__ import annotations

import json
import os
import sys
import time
from typing import Dict, List, Optional, Tuple


def read_json_file(file_path: str) -> Optional[object]:
    """Read JSON content from a file and return None on error."""
    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except FileNotFoundError:
        print(f"Error: file not found '{file_path}'")
    except json.JSONDecodeError as error:
        print(f"Error: invalid JSON in '{file_path}': {error}")
    return None


def load_price_catalogue(file_path: str) -> Tuple[Dict[str, float], List[str]]:
    """Load catalogue as product->price and collect invalid catalogue entries."""
    content = read_json_file(file_path)
    prices: Dict[str, float] = {}
    invalid_entries: List[str] = []

    if not isinstance(content, list):
        invalid_entries.append("Catalogue root must be a JSON array.")
        return prices, invalid_entries

    for index, entry in enumerate(content, start=1):
        if not isinstance(entry, dict):
            message = f"Catalogue item {index}: expected object, got {type(entry).__name__}"
            invalid_entries.append(message)
            print(f"Error: {message}")
            continue

        title = entry.get("title")
        price = entry.get("price")

        if not isinstance(title, str) or not title.strip():
            message = f"Catalogue item {index}: invalid title '{title}'"
            invalid_entries.append(message)
            print(f"Error: {message}")
            continue

        if not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0:
            message = f"Catalogue item {index}: invalid price '{price}' for '{title}'"
            invalid_entries.append(message)
            print(f"Error: {message}")
            continue

        clean_title = title.strip()
        if clean_title in prices:
            message = f"Catalogue item {index}: duplicate title '{clean_title}', last value kept"
            invalid_entries.append(message)
            print(f"Error: {message}")
        prices[clean_title] = float(price)

    return prices, invalid_entries


def compute_total_sales(
    sales_file: str, prices: Dict[str, float]
) -> Tuple[float, int, int, List[str]]:
    """Compute total cost from sales file and keep invalid sales messages."""
    content = read_json_file(sales_file)
    if not isinstance(content, list):
        return 0.0, 0, 0, ["Sales record root must be a JSON array."]

    total_cost = 0.0
    valid_count = 0
    invalid_count = 0
    invalid_entries: List[str] = []

    for index, entry in enumerate(content, start=1):
        if not isinstance(entry, dict):
            message = f"Sale item {index}: expected object, got {type(entry).__name__}"
            invalid_entries.append(message)
            print(f"Error: {message}")
            invalid_count += 1
            continue

        product = entry.get("Product")
        quantity = entry.get("Quantity")

        if not isinstance(product, str) or not product.strip():
            message = f"Sale item {index}: invalid product '{product}'"
            invalid_entries.append(message)
            print(f"Error: {message}")
            invalid_count += 1
            continue

        if not isinstance(quantity, (int, float)) or isinstance(quantity, bool):
            message = f"Sale item {index}: invalid quantity '{quantity}' for '{product}'"
            invalid_entries.append(message)
            print(f"Error: {message}")
            invalid_count += 1
            continue

        clean_product = product.strip()
        if clean_product not in prices:
            message = f"Sale item {index}: product not found in catalogue '{clean_product}'"
            invalid_entries.append(message)
            print(f"Error: {message}")
            invalid_count += 1
            continue

        total_cost += prices[clean_product] * float(quantity)
        valid_count += 1

    return total_cost, valid_count, invalid_count, invalid_entries


def get_test_case_label(file_path: str) -> str:
    """Infer test case label from sales file name, defaulting to the file stem."""
    base_name = os.path.basename(file_path)
    parts = base_name.split(".")
    if parts and parts[0]:
        return parts[0]
    return os.path.splitext(base_name)[0]


def load_expected_costs(file_path: str) -> Dict[str, float]:
    """Load expected totals from a tab/space-separated file."""
    expected_costs: Dict[str, float] = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file_handle:
            for raw_line in file_handle:
                line = raw_line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 2:
                    continue
                label = parts[0].strip()
                value_text = parts[1].strip()
                if label.upper() == "TOTAL":
                    continue
                try:
                    expected_costs[label] = float(value_text)
                except ValueError:
                    print(f"Error: invalid expected value '{value_text}' for '{label}'")
    except FileNotFoundError:
        print(f"Error: expected results file not found '{file_path}'")
    return expected_costs


def render_sales_results(
    price_file: str,
    sales_file: str,
    total_cost: float,
    valid_count: int,
    invalid_count: int,
    expected_cost: Optional[float],
    elapsed: float,
) -> str:
    """Build human-readable sales output."""
    if expected_cost is None:
        expected_text = "#N/A"
        delta_text = "#N/A"
    else:
        expected_text = f"{expected_cost:.2f}"
        delta_text = f"{(total_cost - expected_cost):.2f}"

    lines = [
        "Sales Processing Results",
        "========================",
        f"Price catalogue file : {price_file}",
        f"Sales record file    : {sales_file}",
        f"Valid sale rows      : {valid_count}",
        f"Invalid sale rows    : {invalid_count}",
        f"TOTAL_COST           : {total_cost:.2f}",
        f"EXPECTED_COST        : {expected_text}",
        f"TOTAL_VS_EXPECTED    : {delta_text}",
        f"ELAPSED_SECONDS      : {elapsed:.6f}",
    ]
    return "\n".join(lines)


def render_invalid_results(messages: List[str], elapsed: float) -> str:
    """Build invalid-data report output."""
    lines = [
        "Invalid Data Report",
        "===================",
        f"Invalid rows: {len(messages)}",
    ]
    if messages:
        lines.append("")
        lines.append("Details:")
        for message in messages:
            lines.append(f"- {message}")
    lines.append("")
    lines.append(f"ELAPSED_SECONDS: {elapsed:.6f}")
    return "\n".join(lines)


def write_file(file_path: str, content: str) -> None:
    """Write UTF-8 text to file."""
    with open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(content + "\n")


def main(argv: List[str]) -> int:
    """Program entry point."""
    if len(argv) < 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        return 1

    price_file = argv[1]
    sales_file = argv[2]

    start = time.perf_counter()
    prices, invalid_catalogue = load_price_catalogue(price_file)
    total_cost, valid_count, invalid_count, invalid_sales = compute_total_sales(sales_file, prices)
    elapsed = time.perf_counter() - start

    all_invalid = invalid_catalogue + invalid_sales
    invalid_output = render_invalid_results(all_invalid, elapsed)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.normpath(os.path.join(script_dir, "..", "results"))
    os.makedirs(results_dir, exist_ok=True)
    expected_file = os.path.join(results_dir, "ExpectedResults.txt")
    expected_costs = load_expected_costs(expected_file)

    test_case = get_test_case_label(sales_file)
    expected_cost = expected_costs.get(test_case)
    output = render_sales_results(
        price_file,
        sales_file,
        total_cost,
        valid_count,
        invalid_count + len(invalid_catalogue),
        expected_cost,
        elapsed,
    )
    actual_file = os.path.join(results_dir, f"{test_case}.ActualSalesResults.txt")
    invalid_file = os.path.join(results_dir, f"{test_case}.InvalidData.txt")

    print(output)
    if all_invalid:
        print("\nInvalid records were found. Review the invalid report file.")

    write_file("SalesResults.txt", output)
    write_file(actual_file, output)
    write_file(invalid_file, invalid_output)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
