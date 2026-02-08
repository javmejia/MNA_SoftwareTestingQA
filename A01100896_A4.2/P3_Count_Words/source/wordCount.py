#!/usr/bin/env python3
"""Count distinct words in a file and report frequencies."""
# pylint: disable=invalid-name

from __future__ import annotations

import os
import sys
import time
from typing import Dict, List, Tuple


def is_alpha_word(token: str) -> bool:
    """Return True when the token contains only alphabetic characters."""
    if token == "":
        return False
    for ch in token:
        if not ("a" <= ch <= "z" or "A" <= ch <= "Z"):
            return False
    return True


def parse_words(file_path: str) -> List[str]:
    """Read words from file, skipping invalid tokens with console errors."""
    words: List[str] = []
    with open(file_path, "r", encoding="utf-8") as file_handle:
        for line_no, raw_line in enumerate(file_handle, start=1):
            line = raw_line.strip()
            if line == "":
                print(f"Line {line_no}: empty line skipped")
                continue
            for token in line.split():
                if not is_alpha_word(token):
                    print(f"Line {line_no}: invalid value '{token}'")
                    continue
                words.append(token)
    return words


def count_words(words: List[str]) -> Dict[str, int]:
    """Count word occurrences using basic loops."""
    counts: Dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def sort_counts(counts: Dict[str, int]) -> List[Tuple[str, int]]:
    """Return counts sorted by frequency desc then word asc."""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


def render_results(counts: Dict[str, int], label: str, elapsed: float) -> str:
    """Render results table for console and file output."""
    lines = [f"Row Labels\tCount of {label}"]
    for word, count in sort_counts(counts):
        lines.append(f"{word}\t{count}")
    lines.append(f"ELAPSED_SECONDS\t{elapsed:.6f}")
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    """Program entry point."""
    if len(argv) < 2:
        print("Usage: python wordCount.py fileWithData.txt")
        return 1

    file_path = argv[1]
    label = os.path.splitext(os.path.basename(file_path))[0]
    start = time.perf_counter()
    words = parse_words(file_path)
    counts = count_words(words)
    elapsed = time.perf_counter() - start

    output = render_results(counts, label, elapsed)
    print(output)

    with open("WordCountResults.txt", "w", encoding="utf-8") as file_handle:
        file_handle.write(output + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
