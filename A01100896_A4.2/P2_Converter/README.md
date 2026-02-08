# P2 Converter

Convert decimal numbers to binary and hexadecimal for each test case in `tests/`.

## Program Description

This program reads decimal integer values from a text file and converts each number to two alternative number systems:
- **Binary (Base 2):** Represents numbers using only digits 0 and 1
- **Hexadecimal (Base 16):** Represents numbers using digits 0-9 and letters A-F

The program handles both positive and negative numbers, using two's complement representation for negative values in binary. It validates input, reporting errors for non-integer values while tracking successful conversions. Each conversion is displayed in a formatted table with the original decimal value and its binary and hexadecimal equivalents. Results include execution time for performance measurement.

## Folders
- `source/` program source code
- `tests/` input test cases (TC1.txt, TC2.txt, ...)
- `results/` expected, actual, and comparison outputs

## Run one file
```bash
cd /Users/javmejia/Documents/MNA_SoftwareTestingQA/A01100896_A4.2/P2_Converter/source
python3 convertNumbers.py ../tests/TC1.txt
```

## Run all tests and comparison
```bash
cd /Users/javmejia/Documents/MNA_SoftwareTestingQA/A01100896_A4.2/P2_Converter/tests
python3 run_tests.py
```
