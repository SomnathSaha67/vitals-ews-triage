from src.triage_queue import TriageQueue


def test_most_urgent_returns_highest_scores_first():
  queue = TriageQueue()
  queue.add(patient_id=1, score=2)
  queue.add(patient_id=2, score=9)
  queue.add(patient_id=3, score=5)

  assert queue.most_urgent() == [(2, 9), (3, 5), (1, 2)]