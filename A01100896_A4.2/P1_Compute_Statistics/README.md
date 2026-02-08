# P1 Compute Statistics

Compute descriptive statistics for each test case in `tests/`.

## Program Description

This program reads a list of numeric values from a text file and calculates key statistical measures:
- **Count:** The total number of values
- **Mean:** The average value (sum of all values divided by count)
- **Median:** The middle value when numbers are sorted
- **Mode:** The value(s) that appear most frequently
- **Standard Deviation:** A measure of how spread out the numbers are from the mean
- **Variance:** The square of the standard deviation

The program validates input, skipping empty lines and invalid entries while reporting errors. Results include execution time for performance analysis.

## Folders
- `source/` program source code
- `tests/` input test cases (TC1.txt, TC2.txt, ...)
- `results/` expected, actual, and comparison outputs

## Run one file
```bash
cd /Users/javmejia/Documents/MNA_SoftwareTestingQA/A01100896_A4.2/P1_Compute_Statistics/source
python3 computeStatistics.py ../tests/TC1.txt
```

## Run all tests and comparison
```bash
cd /Users/javmejia/Documents/MNA_SoftwareTestingQA/A01100896_A4.2/P1_Compute_Statistics/tests
python3 run_tests.py
```
