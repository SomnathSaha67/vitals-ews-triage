"""
NEWS@-inspired Early Warning Score- rule-based, nt learnd from data
"""

def _band_score(value: float, bands: list[tuple[float, float, int]]) -> int:
  """
  Bands= (low, high, score): returns the score of the first matching range. 
  """
  for low, high, score in bands:
    if low<=value<high:
      return score
  return 3                          # Outside every defined band is itself a worst-case signal

def score_vitals(hr, resp, spo2, temp, sbp) -> int:
  """
  Sums independent per-vital scores into one aggregate severity number.
  """
  hr_score= _band_score(hr, [(0, 41, 3), (41, 51, 1), (51, 91, 0), (91, 111, 1), (111, 131, 2), (131, 999, 3)])
  resp_score= _band_score(resp, [(0, 9, 3), (9, 12, 1), (12, 21, 0), (21, 25, 2), (25, 999, 3)])
  spo2_score= _band_score(spo2, [(0, 92, 3), (92, 94, 2), (94, 96, 1), (96, 101, 0)])
  temp_score = _band_score(temp, [(0, 35.1, 3), (35.1, 36.1, 1), (36.1, 38.1, 0), (38.1, 39.1, 1), (39.1, 99, 2)])
  sbp_score = _band_score(sbp, [(0, 91, 3), (91, 101, 2), (101, 111, 1), (111, 220, 0), (220, 999, 3)])
  return hr_score + resp_score + spo2_score + temp_score + sbp_score

DEFAULT_RISK_THRESHOLD = 1


def risk_tier(total_score: int, threshold: int = DEFAULT_RISK_THRESHOLD) -> str:
  """
  Convert a score into a risk label using the supplied threshold.

  Callers that have labeled data can provide a threshold selected for that dataset.
  The default keeps standalone scoring and simulation usable without labels.
  """
  return "High Risk" if total_score >= threshold else "Low Risk"