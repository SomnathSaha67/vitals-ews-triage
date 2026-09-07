"""
Replays patient records in timestamp order, scoring each and feeding the triage queue live.
"""

from src.data_loader import load_records
from src.ews_scorer import score_vitals, risk_tier
from src.triage_queue import TriageQueue

def run_simulation(csv_path: str, ward_capacity: int= 5):
  records= load_records(csv_path)
  queue= TriageQueue()
  for record in records:
    score= score_vitals(record.heart_rate, record.resp_rate, record.spo2,
                        record.temperature, record.systolic_bp)
    queue.add(record.patient_id, score)
    print(f"[{record.timestamp}] patient {record.patient_id} -> score= {score} tier= {risk_tier(score)}")
  print("\nMost urgent patients right now:")
  for patient_id, score in queue.most_urgent(ward_capacity):
    print(f"  patient {patient_id}: score= {score}")
if __name__=="__main__":
  import sys
  run_simulation(sys.argv[1])