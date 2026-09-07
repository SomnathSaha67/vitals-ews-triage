import csv

from src.export_triage import export_by_risk


def test_export_creates_sorted_risk_files(tmp_path):
  input_path = tmp_path / "vitals.csv"
  input_path.write_text(
    "Patient ID,Heart Rate,Respiratory Rate,Timestamp,Body Temperature,Oxygen Saturation,Systolic Blood Pressure\n"
    "1,70,16,2024-01-01T00:00:02,37,98,120\n"
    "2,145,39,2024-01-01T00:00:01,39.5,88,85\n",
    encoding="utf-8",
  )

  high_path, low_path = export_by_risk(str(input_path), str(tmp_path / "output"))

  with high_path.open(newline="", encoding="utf-8") as high_file:
    high_rows = list(csv.DictReader(high_file))
  with low_path.open(newline="", encoding="utf-8") as low_file:
    low_rows = list(csv.DictReader(low_file))

  assert [row["Patient ID"] for row in high_rows] == ["2"]
  assert high_rows[0]["Calculated Risk"] == "High Risk"
  assert [row["Patient ID"] for row in low_rows] == ["1"]
  assert low_rows[0]["Calculated Risk"] == "Low Risk"