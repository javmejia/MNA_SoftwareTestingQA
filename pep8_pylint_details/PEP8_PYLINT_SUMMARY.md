# PEP 8 and Pylint Quality Checks Summary

**Date:** February 8, 2026

## Overview
This document summarizes all PEP 8 and pylint quality checks performed on the three projects in the MNA_SoftwareTestingQA repository.

---

## Project 1: P1_Compute_Statistics

### File: `computeStatistics.py`

#### Initial PEP 8 Check
- **Rating:** 9.89/10
- **Issue Found:**
  - Line 18: `text == ''` can be simplified to `not text`

#### Fix Applied
- Replaced `if text == "":` with `if not text:`

#### Final PEP 8 Check
- **Rating:** 10.00/10 ✓
- **Status:** PASSED - No style violations

#### Full Pylint Check
- **Rating:** 10.00/10 ✓
- **Status:** PASSED - No issues

---

## Project 2: P2_Converter

### File: `convertNumbers.py`

#### Initial PEP 8 Check
- **Rating:** 9.62/10
- **Issues Found:**
  - Line 18: `text == ''` can be simplified to `not text`
  - Line 33: `value == 0` can be simplified to `not value`
  - Line 45: `value == 0` can be simplified to `not value`

#### Fixes Applied
1. Line 18: Changed `if text == "":` to `if not text:`
2. Line 33: Changed `if value == 0:` to `if not value:`
3. Line 45: Changed `if value == 0:` to `if not value:`

#### Final PEP 8 Check
- **Rating:** 10.00/10 ✓
- **Status:** PASSED - No style violations

#### Full Pylint Check
- **Rating:** 10.00/10 ✓
- **Status:** PASSED - No issues

---

## Project 3: P3_Count_Words

### File: `wordCount.py`

#### Initial PEP 8 Check
- **Rating:** 9.64/10
- **Issues Found:**
  - Line 15: `token == ''` can be simplified to `not token`
  - Line 29: `line == ''` can be simplified to `not line`

#### Fixes Applied
1. Line 15: Changed `if token == "":` to `if not token:`
2. Line 29: Changed `if line == "":` to `if not line:`

#### Final PEP 8 Check
- **Rating:** 10.00/10 ✓
- **Status:** PASSED - No style violations

#### Full Pylint Check
- **Rating:** 10.00/10 ✓
- **Status:** PASSED - No issues

---

## Summary of Changes

### Files Modified
1. `/A01100896_A4.2/P1_Compute_Statistics/source/computeStatistics.py`
2. `/A01100896_A4.2/P2_Converter/source/convertNumbers.py`
3. `/A01100896_A4.2/P3_Count_Words/source/wordCount.py`

### Files Deleted
1. `/A01100896_A4.2/P1_Compute_Statistics/source/StatisticsResults.txt`
2. `/A01100896_A4.2/P2_Converter/source/ConvertionResults.txt`
3. `/A01100896_A4.2/P3_Count_Words/source/WordCountResults.txt`

### Files Created
1. `/A01100896_A4.2/P1_Compute_Statistics/results/PEP8_Report.txt`
2. `/A01100896_A4.2/P2_Converter/results/PEP8_Report.txt`
3. `/A01100896_A4.2/P3_Count_Words/results/PEP8_Report.txt`

---

## Test Execution Results

All programs were successfully executed with TC1 test cases:

### P1: Compute Statistics
- Input: 400 numbers from TC1.txt
- Output: Mean (242.32), Median (239.5), Mode (170,393), SD (145.26), Variance (21099.92)
- Status: ✓ PASSED

### P2: Number Converter
- Input: 200 decimal numbers from TC1.txt
- Output: Binary and hexadecimal conversions
- Status: ✓ PASSED

### P3: Word Counter
- Input: Text file from TC1.txt
- Output: 99 distinct words with frequencies
- Status: ✓ PASSED

---

## Final Status

✅ **ALL QUALITY CHECKS PASSED**

- All source files: 10.00/10 (PEP 8 + Pylint)
- All programs: Functionally verified with TC1
- All changes: Committed and pushed to GitHub

Repository: https://github.com/javmejia/MNA_SoftwareTestingQA
