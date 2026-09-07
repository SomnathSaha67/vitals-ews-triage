"""
Streams patient vital-sign records from CSV, sorted by timestamp for the live simulator.
"""

import csv
from datetime import datetime
from dataclasses import dataclass

@dataclass

class VitalRecord:                      # Strongly-typed snapshot instead of passing raw dict rows around
  patient_id: int
  heart_rate: float
  resp_rate: float
  timestamp: datetime
  temperature: float
  spo2: float
  systolic_bp: float
  diastolic_bp: float
  age: int
  ground_truth_risk: str                # Needed later to validate our scoring

def load_records(path: str) -> list[VitalRecord]:
  records= []
  with open(path, newline="") as f:
    reader= csv.DictReader(f)
    for row in reader:
      records.append(VitalRecord(
        patient_id= int(row["Patient ID"]),
        heart_rate= float(row["Heart Rate"]),
        resp_rate= float(row["Respiratory Rate"]),
        timestamp= datetime.fromisoformat(row["Timestamp"]),
        temperature= float(row["Body Temperature"]),
        spo2= float(row["Oxygen Saturation"]),
        systolic_bp= float(row["Systolic Blood Pressure"]),
        diastolic_bp= float(row["Diastolic Blood Pressure"]),
        age= int(row["Age"]),
        ground_truth_risk= row["Risk Category"]
      ))
  records.sort(key= lambda r: r.timestamp)                   # Simulator must replay events in real arrival order
  return records