#!/usr/bin/env python3
"""Convert decimal numbers from a file to binary and hexadecimal."""
# pylint: disable=invalid-name

from __future__ import annotations

import sys
import time
from typing import List, Optional, Tuple


def parse_numbers(file_path: str) -> List[Tuple[str, Optional[int]]]:
    """Read integers from a file, keeping invalid entries with None value."""
    numbers: List[Tuple[str, Optional[int]]] = []
    with open(file_path, "r", encoding="utf-8") as file_handle:
        for line_no, raw_line in enumerate(file_handle, start=1):
            text = raw_line.strip()
            if not text:
                print(f"Line {line_no}: empty line skipped")
                continue
            try:
                value = int(text)
            except ValueError:
                print(f"Line {line_no}: invalid value '{text}'")
                numbers.append((text, None))
                continue
            numbers.append((text, value))
    return numbers


def to_binary_positive(value: int) -> str:
    """Convert a non-negative integer to binary using basic division."""
    if not value:
        return "0"
    digits: List[str] = []
    number = value
    while number > 0:
        digits.append(str(number % 2))
        number //= 2
    return "".join(reversed(digits))


def to_hex_positive(value: int) -> str:
    """Convert a non-negative integer to hexadecimal using basic division."""
    if not value:
        return "0"
    digits: List[str] = []
    number = value
    symbols = "0123456789ABCDEF"
    while number > 0:
        digits.append(symbols[number % 16])
        number //= 16
    return "".join(reversed(digits))


def to_binary_twos_complement(value: int, bits: int) -> str:
    """Convert a negative integer to two's complement binary with fixed width."""
    base = 1 << bits
    adjusted = base + value
    return to_binary_positive(adjusted).rjust(bits, "0")


def to_hex_twos_complement(value: int, bits: int) -> str:
    """Convert a negative integer to two's complement hex with fixed width."""
    base = 1 << bits
    adjusted = base + value
    hex_width = bits // 4
    return to_hex_positive(adjusted).rjust(hex_width, "0")


def convert_value(value: int) -> tuple[str, str]:
    """Convert integer to binary and hex strings."""
    if value >= 0:
        return to_binary_positive(value), to_hex_positive(value)

    binary = to_binary_twos_complement(value, 10)
    hexadecimal = to_hex_twos_complement(value, 40)
    return binary, hexadecimal


def render_results(values: List[Tuple[str, Optional[int]]], elapsed: float, label: str) -> str:
    """Render results table for console and file output."""
    lines = [f"ITEM\t{label}\tBIN\tHEX"]
    for index, (raw_text, value) in enumerate(values, start=1):
        if value is None:
            binary, hexadecimal = "#VALUE!", "#VALUE!"
        else:
            binary, hexadecimal = convert_value(value)
        lines.append(f"{index}\t{raw_text}\t{binary}\t{hexadecimal}")
    lines.append(f"ELAPSED_SECONDS\t{elapsed:.6f}")
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    """Program entry point."""
    if len(argv) < 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        return 1

    file_path = argv[1]
    start = time.perf_counter()
    values = parse_numbers(file_path)
    elapsed = time.perf_counter() - start

    output = render_results(values, elapsed, "INPUT")
    print(output)

    with open("ConvertionResults.txt", "w", encoding="utf-8") as file_handle:
        file_handle.write(output + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
