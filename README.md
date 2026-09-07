# Vitals Early Warning and Triage Queue

## Overview
A rule-based patient vital-sign scoring and triage-reporting system built with Python. It reads
vital signs from a CSV file, assigns points to abnormal measurements, automatically selects a
risk threshold when labels are available, and creates separate sorted files for high-risk and
low-risk records.

## Project Structure
```text
vitals-ews-triage/
├── data/
│   └── human_vital_signs_dataset_2024.csv
├── src/
│   ├── data_loader.py
│   ├── ews_scorer.py
│   ├── export_risk_csv.py
│   ├── export_triage.py
│   ├── simulator.py
│   ├── threshold_selector.py
│   ├── triage_queue.py
│   └── validate.py
├── tests/
│   ├── test_ews_scorer.py
│   ├── test_export_triage.py
│   └── test_triage_queue.py
├── .gitignore
└── README.md
```

## Purpose
This project processes a complete patient-vital-sign CSV file instead of calculating only one
score. It assigns a simple score to each record, separates records into high-risk and low-risk
groups, and sorts each group for review.

The score uses heart rate, respiratory rate, oxygen saturation, body temperature, and systolic
blood pressure. Each measurement is compared with defined ranges and receives between 0 and 3
points. The points are added to produce one total score.

The dataset also contains age, gender, BMI, and other derived measurements. The current scoring
rules do not use those additional fields.

## How It Works
1. Load the patient records from the CSV file.
2. Convert numeric values and timestamps into usable Python values.
3. Compare five vital signs with their predefined ranges.
4. Add the points to create one total score.
5. If the CSV has a `Risk Category` column, test possible thresholds automatically.
6. Select the threshold with the highest agreement with the dataset labels.
7. If the CSV has no labels, use the default threshold of `1`.
8. Assign each record as `High Risk` or `Low Risk`.
9. Sort records by score, timestamp, and patient ID.
10. Write `output/high_risk.csv` and `output/low_risk.csv`.

When labels are available, `src/threshold_selector.py` tests possible threshold values. A
threshold is the boundary that converts a score into a risk label:

```text
score >= threshold -> High Risk
score < threshold  -> Low Risk
```

The agreement percentage is calculated as:

```text
(correct High Risk predictions + correct Low Risk predictions)
/ total records * 100
```

For the current dataset, the program currently reports a selected threshold of `1` and an
agreement of `65.05%`. This means the calculated labels match the dataset labels for about 65 out
of every 100 records. It does not prove medical accuracy. Threshold selection uses Python loops,
lists, comparisons, and counting.

If a CSV does not contain `Risk Category`, the exporter cannot learn a threshold from that file.
It uses `DEFAULT_RISK_THRESHOLD`, currently `1`, and still creates the reports. The validation
command requires labeled data.

## Technology Stack and Libraries
- **Python 3.10+**: Application language and runtime.
- **csv** (Python standard library): Reads input data and writes output reports.
- **datetime** (Python standard library): Parses timestamps and supports sorting.
- **dataclasses** (Python standard library): Defines the `VitalRecord` object.
- **bisect** (Python standard library): Finds insertion positions in the triage queue.
- **pathlib** (Python standard library): Creates output directories and handles file paths.
- **sys** (Python standard library): Reads command-line arguments.
- **argparse** (Python standard library): Used by the alternate exporter.
- **pytest**: Runs the automated test suite.

The application uses only Python's standard library at runtime. A `requirements.txt` file and a
`config.py` file are not required. `pytest` must be installed separately for testing if it is not
already available. The dataset contains 200,020 records and 17 columns.

## File Roles
| Path | Role |
| --- | --- |
| `data/human_vital_signs_dataset_2024.csv` | Input dataset containing vital-sign records and risk labels. |
| `src/data_loader.py` | Reads CSV rows, converts values, creates `VitalRecord` objects, and sorts records by timestamp. |
| `src/ews_scorer.py` | Defines vital-sign ranges, calculates scores, and converts scores into risk labels. |
| `src/threshold_selector.py` | Tests possible thresholds and returns the one with the highest label agreement. |
| `src/validate.py` | Selects a threshold and reports agreement with the dataset labels. |
| `src/export_triage.py` | Main exporter that creates `output/high_risk.csv` and `output/low_risk.csv`. |
| `src/export_risk_csv.py` | Alternate exporter with a different output format and directory name. |
| `src/triage_queue.py` | Maintains patients in score order using binary-search insertion. |
| `src/simulator.py` | Replays timestamped records and demonstrates the priority queue. |
| `tests/test_ews_scorer.py` | Tests normal scores, critical scores, and point totals. |
| `tests/test_export_triage.py` | Tests report creation, calculated labels, and sorting. |
| `tests/test_triage_queue.py` | Tests highest-score-first queue ordering. |
| `.gitignore` | Excludes caches, virtual environments, logs, and generated reports. |

## Use Cases
Demonstrates transparent rule-based scoring, automatic threshold evaluation, CSV processing,
deterministic sorting, priority-queue design, and automated testing with Python's standard
library. It is not a replacement for clinical assessment, medical professionals, hospital
software, or validated patient-monitoring systems.

## Advantages
- Easy to understand: every score comes from visible value ranges.
- Automatically selects a threshold when labeled data is available.
- Preserves the original CSV fields in the exported reports.
- Produces deterministic sorting using score, timestamp, and patient ID.
- Uses only the Python standard library for application code.
- Includes automated tests for scoring, exporting, and queue behavior.

## Limitations
- The scoring rules use only five vital signs.
- The threshold is selected and evaluated on the same labeled dataset, which can make agreement
  look better than performance on new data.
- Different datasets may use different column names, units, labels, or scoring rules.
- The system does not handle every possible missing-value or data-quality problem.
- The dataset's risk label is not a disease diagnosis.
- The simulator prints one line per record and is not practical for normal full-dataset use.
- The project does not connect to hospital systems, send alerts, recommend treatment, or replace
  clinical judgment.

## Setup
```bash
python -m pip install pytest
```

## Run
Run the automated tests:

```bash
python -m pytest tests/
```

Validate the labeled dataset and select the threshold automatically:

```bash
python -m src.validate data/human_vital_signs_dataset_2024.csv
```

Create the sorted high-risk and low-risk reports:

```bash
python -m src.export_triage data/human_vital_signs_dataset_2024.csv
```

The exporter creates:

```text
output/high_risk.csv
output/low_risk.csv
```

The simulator is optional. It prints one line for every record and is mainly useful for learning
or debugging:

```bash
python -m src.simulator data/human_vital_signs_dataset_2024.csv
```

## Tests
```bash
python -m pytest tests/
```

The tests cover the scorer, automatic report export, and priority queue ordering.

## Safety and Scope
The dataset's `Risk Category` is a supplied label, not a disease diagnosis. Vital signs alone
should not be used to assign a disease. Before any real patient-care use, the data, scoring rules,
labels, threshold-selection method, wording, and results would require clinical review and formal
validation. A future machine-learning project should also separate training, validation, and test
data.