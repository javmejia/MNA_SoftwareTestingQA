# A01100896_A6.2 - Hotel Reservation System

## Overview
This assignment implements a file-based hotel reservation system in Python with:
- Core abstractions: `Hotel`, `Customer`, `Reservation`
- Persistent behaviors for hotel/customer/reservation CRUD and reservation lifecycle
- Unit tests, coverage, and static analysis reports

## Folder Structure
- `src/`: application source code
  - `models/`: domain classes
  - `repositories/`: JSON file persistence
  - `services/`: business operations facade
- `data/`: persistent runtime data (`hotels.json`, `customers.json`, `reservations.json`)
- `test_data/`: scenario inputs split by validity
  - `valid_*.json`
  - `invalid_*.json`
- `tests/`: `unittest` test suite
- `scripts/`: execution utilities
  - `run_test_data_scenarios.py`
- `results/`: reports and execution outputs

## Main Artifacts
### Design
- `design/design_document.md`

### Quality Reports
- `results/PEP8_Report.txt`
- `results/Pylint_Report.txt`
- `results/Flake8_Report.txt`

### Unit Testing
- `results/Unit_Test_Results.txt`: verbose test execution results (per test case)
- `results/Unit_Test_Coverage_Report.txt`: coverage summary (target >= 85%, current >= 95%)

### Scenario Execution Results
- `results/execution_runs/valid_run_results.txt`
- `results/execution_runs/invalid_run_results.txt`

These files include:
- operation name
- expected outcome (`EXPECTED=PASS/FAIL`)
- whether result matched expectation (`MATCH=YES/NO`)
- explicit outcome details (for example: `Hotel does not exist`)

## How to Run
From repository root (`/Users/javmejia/Documents/MNA_SoftwareTestingQA`):

### 1. Unit tests
```bash
.venv/bin/python -m unittest discover -s A01100896_A6.2/tests -p "test_*.py" -v
```

### 2. Coverage
```bash
.venv/bin/python -m coverage run --source=A01100896_A6.2/src -m unittest discover -s A01100896_A6.2/tests -p "test_*.py"
.venv/bin/python -m coverage report > A01100896_A6.2/results/Unit_Test_Coverage_Report.txt
```

### 3. Static analysis
Official assignment scope:
- `A01100896_A6.2/src`
- `A01100896_A6.2/tests`

Optional engineering scope:
- `A01100896_A6.2/scripts`

```bash
pycodestyle A01100896_A6.2/src A01100896_A6.2/tests
pylint A01100896_A6.2/src A01100896_A6.2/tests
.venv/bin/flake8 A01100896_A6.2/src A01100896_A6.2/tests
```

Optional linting for scripts:
```bash
pycodestyle A01100896_A6.2/scripts
pylint A01100896_A6.2/scripts
.venv/bin/flake8 A01100896_A6.2/scripts
```

### 4. Scenario runner (valid + invalid data)
```bash
.venv/bin/python A01100896_A6.2/scripts/run_test_data_scenarios.py
```

## Notes
- The scenario runner resets `data/*.json` at start, runs valid then invalid scenarios, and writes execution logs under `results/execution_runs`.
- In invalid scenarios, non-existing entity lookups are explicitly logged as valid behavior (for example: `Display Hotel H404 | Hotel does not exist`).
- In invalid scenario results, the persistence snapshot is shown only if data changed; otherwise it is omitted to avoid confusion.
