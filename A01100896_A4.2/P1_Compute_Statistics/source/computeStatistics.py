#!/usr/bin/env python3
"""Compute descriptive statistics for a list of numbers in a file."""
# pylint: disable=invalid-name

from __future__ import annotations

import sys
import time
from typing import Dict, List, Optional, Sequence


def parse_numbers(file_path: str) -> List[float]:
    """Read numbers from file, skipping invalid lines with console errors."""
    numbers: List[float] = []
    with open(file_path, "r", encoding="utf-8") as file_handle:
        for line_no, raw_line in enumerate(file_handle, start=1):
            text = raw_line.strip()
            if text == "":
                print(f"Line {line_no}: empty line skipped")
                continue
            try:
                value = float(text)
            except ValueError:
                print(f"Line {line_no}: invalid value '{text}'")
                continue
            numbers.append(value)
    return numbers


def compute_mean(values: List[float]) -> float:
    """Compute arithmetic mean using a basic loop."""
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def compute_median(sorted_values: List[float]) -> float:
    """Compute median from a pre-sorted list."""
    count = len(sorted_values)
    mid = count // 2
    if count % 2 == 1:
        return sorted_values[mid]
    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0


def compute_mode(values: List[float]) -> Optional[List[float]]:
    """Compute mode; return all modes, or None if no repeated values exist."""
    counts: Dict[float, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    max_count = 0
    for count in counts.values():
        max_count = max(max_count, count)
    if max_count <= 1:
        return None
    modes = [value for value, count in counts.items() if count == max_count]
    return sorted(modes)


def compute_variance(values: List[float], mean: float) -> float:
    """Compute population variance."""
    total = 0.0
    for value in values:
        diff = value - mean
        total += diff * diff
    return total / len(values)


def compute_statistics(values: List[float]) -> Dict[str, Optional[object]]:
    """Compute statistics using basic algorithms."""
    if not values:
        return {
            "count": 0.0,
            "mean": None,
            "median": None,
            "mode": None,
            "variance": None,
            "sd": None,
        }

    sorted_values = sorted(values)
    mean = compute_mean(values)
    median = compute_median(sorted_values)
    mode = compute_mode(values)
    variance = compute_variance(values, mean)
    sd = variance ** 0.5

    return {
        "count": float(len(values)),
        "mean": mean,
        "median": median,
        "mode": mode,
        "variance": variance,
        "sd": sd,
    }


def format_number(value: Optional[float]) -> str:
    """Format numeric values to match expected output style."""
    if value is None:
        return "#N/A"
    rounded = round(value)
    if abs(value - rounded) < 1e-9:
        return str(int(rounded))
    text = f"{value:.10f}"
    text = text.rstrip("0").rstrip(".")
    return text


def format_mode(values: Optional[Sequence[float]]) -> str:
    """Format mode list as a comma-separated string."""
    if values is None:
        return "#N/A"
    return ",".join(format_number(value) for value in values)


def render_results(stats: Dict[str, Optional[object]], elapsed: float) -> str:
    """Render statistics lines for console and file output."""
    lines = [
        f"COUNT\t{format_number(stats['count'])}",
        f"MEAN\t{format_number(stats['mean'])}",
        f"MEDIAN\t{format_number(stats['median'])}",
        f"MODE\t{format_mode(stats['mode'])}",
        f"SD\t{format_number(stats['sd'])}",
        f"VARIANCE\t{format_number(stats['variance'])}",
        f"ELAPSED_SECONDS\t{elapsed:.6f}",
    ]
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    """Program entry point."""
    if len(argv) < 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return 1

    file_path = argv[1]
    start = time.perf_counter()
    values = parse_numbers(file_path)
    stats = compute_statistics(values)
    elapsed = time.perf_counter() - start

    output = render_results(stats, elapsed)
    print(output)

    with open("StatisticsResults.txt", "w", encoding="utf-8") as file_handle:
        file_handle.write(output + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
