# P3 Count Words

Count distinct words and their frequency for each test case in `tests/`.

## Program Description

This program reads text from a file and analyzes word patterns by:
- **Extracting words:** Reading the file line by line and splitting each line into individual tokens
- **Validating words:** Ensuring tokens contain only alphabetic characters (A-Z, a-z)
- **Counting frequency:** Tracking how many times each distinct word appears in the text
- **Sorting and reporting:** Displaying words alphabetically with their occurrence counts in a formatted table

The program reports errors for invalid tokens (containing numbers or special characters) while counting only valid alphabetic words. Results are presented in a clear tabular format showing word frequencies and include execution time for performance tracking.

## Folders
- `source/` program source code
- `tests/` input test cases (TC1.txt, TC2.txt, ...)
- `results/` expected, actual, and comparison outputs

## Run one file
```bash
cd /Users/javmejia/Documents/MNA_SoftwareTestingQA/A01100896_A4.2/P3_Count_Words/source
python3 wordCount.py ../tests/TC1.txt
```

## Run all tests and consolidated comparison
```bash
cd /Users/javmejia/Documents/MNA_SoftwareTestingQA/A01100896_A4.2/P3_Count_Words/tests
python3 run_tests.py
```
