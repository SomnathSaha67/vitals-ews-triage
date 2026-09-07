"""
Priority triage queue: uses binary search insertion (bisect) so a new patient is placed into
a severity-sorted queue in O(log n) instead of re-sorting the whole ward each arrival.
In a real ward patients arrive continuously; a full re-sort every time wouldn't scale.
"""

import bisect

class TriageQueue:
  def __init__(self):
    self._scores= []                                 # Kept always sorted so bisect can binary-search it
    self._patients= []                               # Same index as '_scores'; higher original score= more urgent
  
  def add(self, patient_id: int, score: int):
    """
    Negative score keeps the list ascending while urgency stays worst-first.
    """
    idx= bisect.bisect_left(self._scores, -score)
    self._scores.insert(idx, -score)
    self._patients.insert(idx, patient_id)
  
  def most_urgent(self, n:int= 5):
    """
    Front of the queue= highest-severity patients waiting right now.
    """
    return list(zip(self._patients[:n], [-s for s in self._scores[:n]]))