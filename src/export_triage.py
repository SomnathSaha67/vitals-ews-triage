"""Create sorted high-risk and low-risk CSV reports from a vital-sign dataset."""
from src.threshold_selector import choose_best_threshold
import csv
import sys
from datetime import datetime
from pathlib import Path

from src.ews_scorer import DEFAULT_RISK_THRESHOLD, score_vitals


def _score_row(row: dict[str, str], threshold: int) -> dict[str, str | int]:
    """
    Calculate one row's score and risk label.
    """
    score = score_vitals(
        hr=float(row["Heart Rate"]),
        resp=float(row["Respiratory Rate"]),
        spo2=float(row["Oxygen Saturation"]),
        temp=float(row["Body Temperature"]),
        sbp=float(row["Systolic Blood Pressure"]),
    )

    scored_row = dict(row)
    scored_row["Calculated Score"] = score
    scored_row["Calculated Risk"] = "High Risk" if score >= threshold else "Low Risk"

    return scored_row


def _sort_key(row: dict[str, str | int]) -> tuple[int, datetime, int]:
  """Sort high scores first, then use stable timestamp and patient-ID tie-breakers."""
  return (
    -int(row["Calculated Score"]),
    datetime.fromisoformat(str(row["Timestamp"])),
    int(row["Patient ID"]),
  )


def _write_rows(path: Path, rows: list[dict[str, str | int]], fieldnames: list[str]) -> None:
  """Write a collection of scored rows with a header to one CSV file."""
  with path.open("w", newline="", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def export_by_risk(csv_path: str, output_dir: str = "output") -> tuple[Path, Path]:
    """
    Automatically choose a threshold and create two sorted reports.
    """
    rows = []

    with open(csv_path, newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)

        if reader.fieldnames is None:
            raise ValueError("Input CSV must contain a header row")

        fieldnames = [
            *reader.fieldnames,
            "Calculated Score",
            "Calculated Risk",
        ]

        for row in reader:
            score = score_vitals(
                hr=float(row["Heart Rate"]),
                resp=float(row["Respiratory Rate"]),
                spo2=float(row["Oxygen Saturation"]),
                temp=float(row["Body Temperature"]),
                sbp=float(row["Systolic Blood Pressure"]),
            )

            rows.append((row, score))

    scores = [score for row, score in rows]
    if all("Risk Category" in row for row, score in rows):
        actual_labels = [row["Risk Category"] for row, score in rows]
        best_threshold = choose_best_threshold(scores, actual_labels)
    else:
        # Unlabeled datasets cannot teach us a threshold, so use the documented default.
        best_threshold = DEFAULT_RISK_THRESHOLD

    high_risk_rows = []
    low_risk_rows = []

    for row, score in rows:
        scored_row = _score_row(row, best_threshold)

        if scored_row["Calculated Risk"] == "High Risk":
            high_risk_rows.append(scored_row)
        else:
            low_risk_rows.append(scored_row)

    high_risk_rows.sort(key=_sort_key)
    low_risk_rows.sort(key=_sort_key)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    high_path = output_path / "high_risk.csv"
    low_path = output_path / "low_risk.csv"

    _write_rows(high_path, high_risk_rows, fieldnames)
    _write_rows(low_path, low_risk_rows, fieldnames)

    print(f"Automatically selected threshold: {best_threshold}")
    print(f"High-risk records: {len(high_risk_rows)}")
    print(f"Low-risk records: {len(low_risk_rows)}")

    return high_path, low_path


if __name__ == "__main__":
  input_path = sys.argv[1]
  output_directory = sys.argv[2] if len(sys.argv) > 2 else "output"
  high_path, low_path = export_by_risk(input_path, output_directory)
  print(f"Wrote {high_path}")
  print(f"Wrote {low_path}")