"""Alternate report exporter with an explicit output-directory option."""

import argparse
import csv
from datetime import datetime
from pathlib import Path

from src.ews_scorer import risk_tier, score_vitals

OUTPUT_COLUMNS = [
    "Patient ID",
    "Heart Rate",
    "Respiratory Rate",
    "Timestamp",
    "Body Temperature",
    "Oxygen Saturation",
    "Systolic Blood Pressure",
    "Diastolic Blood Pressure",
    "Age",
    "Gender",
    "Weight (kg)",
    "Height (m)",
    "Derived_HRV",
    "Derived_Pulse_Pressure",
    "Derived_BMI",
    "Derived_MAP",
    "Risk Category",
    "Calculated EWS Score",
    "Calculated Risk Tier",
]

def calculate_record(row: dict) -> dict:
  """Calculate the project score and attach fields used for report sorting."""
  score= score_vitals(
    hr= float(row["Heart Rate"]),
    resp=float(row["Respiratory Rate"]),
    spo2=float(row["Oxygen Saturation"]),
    temp=float(row["Body Temperature"]),
    sbp=float(row["Systolic Blood Pressure"])
  )

  result = dict(row)
  result["Calculated EWS Score"] = str(score)
  result["Calculated Risk Tier"] = risk_tier(score)
  result["_sort_score"] = score
  result["_sort_timestamp"] = datetime.fromisoformat(row["Timestamp"])
  result["_sort_patient_id"] = int(row["Patient ID"])
  return result

def sort_key(row: dict) -> tuple:
  """Put the most severe records first with deterministic tie-breakers."""
  return (
    -row["_sort_score"],
    row["_sort_timestamp"],
    row["_sort_patient_id"]
  )

def export_risk_files(input_path: str, output_dir: str) -> None:
  """Split scored rows into two sorted CSV reports."""
  output_path= Path(output_dir)
  output_path.mkdir(parents= True, exist_ok= True)

  high_risk= []
  low_risk= []

  with open(input_path, newline= "", encoding= "utf-8") as input_file:
    reader= csv.DictReader(input_file)

    for row in reader:
      # Preserve the input row so the exported report remains traceable.
      scored_row= calculate_record(row)

      if scored_row["Calculated Risk Tier"]=="High Risk":
        high_risk.append(scored_row)
      else:
        low_risk.append(scored_row)
  write_csv(output_path/"high_risk_patients.csv", high_risk)
  write_csv(output_path/"low_risk_patients.csv", low_risk)

  print(f"High-risk records: {len(high_risk)}")
  print(f"Low-risk records: {len(low_risk)}")
  print(f"Files written to: {output_path}")

def write_csv(path: Path, rows: list[dict]) -> None:
  """Write rows using the report columns and discard internal sort fields."""
  with open(path, 'w', newline= "", encoding= "utf-8") as output_file:
    writer= csv.DictWriter(
      output_file,
      fieldnames= OUTPUT_COLUMNS,
      extrasaction= "ignore"
    )
    writer.writeheader()
    writer.writerows(rows)

def main() -> None:
  parser= argparse.ArgumentParser(
    description= "Split patient records into sorted high and low risk CSV files."
  )
  parser.add_argument("input_csv")
  parser.add_argument(
    "--output-dir",
    default= "outputs",
    help= "Directory for generated CSV files."
  )
  args= parser.parse_args()
  
  export_risk_files(args.input_csv, args.output_dir)

if __name__=="__main__":
  main()