# MNA Software Testing & QA - Assignment 5.2

A software testing and quality assurance project focused on sales-cost processing from JSON data, with test validation and code quality checks.

## 📁 Repository Structure

```
MNA_SoftwareTestingQA/
├── README.md
├── .gitignore
└── A01100896_A5.2/
    ├── README.md
    └── P1/
        ├── source/
        │   └── computeSales.py
        ├── data/
        │   └── priceCatalogue.json
        ├── tests/
        │   ├── TC1.salesRecord.json
        │   ├── TC2.salesRecord.json
        │   └── TC3.salesRecord.json
        └── results/
            ├── ExpectedResults.txt
            ├── TC1.ActualSalesResults.txt
            ├── TC2.ActualSalesResults.txt
            ├── TC3.ActualSalesResults.txt
            ├── TC1.InvalidData.txt
            ├── TC2.InvalidData.txt
            ├── TC3.InvalidData.txt
            ├── PEP8_Report.txt
            └── Pylint_Report.txt
```

## 📊 Test Analysis & Results

### P1: Compute Sales
**Input files:**
- Catalogue: `A01100896_A5.2/P1/data/priceCatalogue.json`
- Sales records: `A01100896_A5.2/P1/tests/TC1.salesRecord.json`, `TC2.salesRecord.json`, `TC3.salesRecord.json`

**Output files:**
- `A01100896_A5.2/P1/results/TC1.ActualSalesResults.txt`
- `A01100896_A5.2/P1/results/TC2.ActualSalesResults.txt`
- `A01100896_A5.2/P1/results/TC3.ActualSalesResults.txt`
- Invalid-data reports per test case (`TCx.InvalidData.txt`)

**Key Findings:**
- Totals for TC1, TC2, and TC3 match expected totals from `ExpectedResults.txt`.
- `TOTAL_VS_EXPECTED` is 0.00 (TC2 may display `-0.00`, which is numerically zero).
- The program continues execution when invalid data is found and records those entries in invalid-data reports.
- Negative quantities are treated as valid inputs.

## ✅ Code Quality Checks

- **PEP 8 (pycodestyle):** Pass (no violations)
  - Report: `A01100896_A5.2/P1/results/PEP8_Report.txt`
- **Pylint:** 10.00/10
  - Report: `A01100896_A5.2/P1/results/Pylint_Report.txt`

## ▶️ Program Execution

From `A01100896_A5.2/P1/source/`:

```bash
python3 computeSales.py ../data/priceCatalogue.json ../tests/TC1.salesRecord.json
python3 computeSales.py ../data/priceCatalogue.json ../tests/TC2.salesRecord.json
python3 computeSales.py ../data/priceCatalogue.json ../tests/TC3.salesRecord.json
```
