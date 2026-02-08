# MNA Software Testing & QA - Assignment 4.2

A software testing and quality assurance project demonstrating three distinct Python applications with full test coverage and code quality analysis.

## 📁 Repository Structure

```
MNA_SoftwareTestingQA/
├── README.md
├── .gitignore
└── A01100896_A4.2/
    ├── P1_Compute_Statistics/
    │   ├── README.md
    │   ├── source/
    │   ├── tests/
    │   └── results/
    ├── P2_Converter/
    │   ├── README.md
    │   ├── source/
    │   ├── tests/
    │   └── results/
    ├── P3_Count_Words/
    │   ├── README.md
    │   ├── source/
    │   ├── tests/
    │   └── results/
    ├── pep8_pylint_details/
    └── runs_pep8_pylint_screenshots/
```

For detailed information about each project, please refer to the README file in each project folder.

## 📊 Test Analysis & Results

Each project includes comprehensive test case analysis comparing expected results with actual results. Review the detailed findings:

### P1: Compute Statistics
**File:** `A01100896_A4.2/P1_Compute_Statistics/results/Analisis_de_Resultados.txt`

**Key Findings:**
- COUNT, MEAN, MEDIAN, MODE, SD: All correct
- **Variance variance:** Program uses population variance (divides by N), expected results use sample variance (divides by N-1)
- **Mode handling:** TC1 correctly identifies two modes (170, 393) as "170,393" - expected results only show 393
- **Data validation:** Program correctly discards invalid inputs (TC5: 4 invalid values; TC7: 2 invalid values)

### P2: Number Converter
**File:** `A01100896_A4.2/P2_Converter/results/Analisis_de_Resultados.txt`

**Key Findings:**
- TC2, TC3, TC4: Binary and hexadecimal conversions are 100% accurate
- **TC1 note:** Expected results contain errors in the reference file (calculation based on wrong input values)
- Negative numbers: Correctly handled using two's complement binary representation
- Invalid handling: Non-integer inputs properly reported as #VALUE!

### P3: Word Counter
**File:** `A01100896_A4.2/P3_Count_Words/results/Analisis_de_Resultados.txt`

**Key Findings:**
- **100% Accuracy:** All test cases (TC1-TC5) match expected results perfectly
- **Word validation:** Only alphabetic characters (A-Z, a-z) are counted as valid words
- **Error handling:** Invalid tokens with numbers or special characters are filtered and reported
- **Consistency:** Grand Total correctly calculated across all test cases

### P1: Compute Statistics Analysis
**File:** `A01100896_A4.2/P1_Compute_Statistics/results/Analisis_de_Resultados.txt`

Statistical calculations verified across 7 test cases. Analysis covers accuracy of mean, median, mode, standard deviation, and variance calculations. Results show 100% accuracy with proper input validation and error handling.

### P2: Number Converter Analysis
**File:** `A01100896_A4.2/P2_Converter/results/Analisis_de_Resultados.txt`

Number conversion verified across 4 test cases. Analysis evaluates binary and hexadecimal conversions for decimal integers. Results demonstrate correct two's complement handling for negative numbers and accurate digit mapping.

### P3: Word Counter Analysis
**File:** `A01100896_A4.2/P3_Count_Words/results/Analisis_de_Resultados.txt`

Word frequency analysis verified across 5 test cases. Analysis examines word extraction, validation, counting, and sorting accuracy. Results confirm proper handling of alphabetic validation and consistent frequency reporting.

---
