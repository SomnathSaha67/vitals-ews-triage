from src.ews_scorer import score_vitals, risk_tier

def test_normal_vitals_score_zero():
  assert score_vitals(hr= 70, resp= 16, spo2= 98, temp= 37.0, sbp= 120)==0

def test_critical_vitals_flag_high_risl():
  score= score_vitals(hr= 145, resp= 39, spo2= 88, temp= 39.5, sbp= 85)
  assert risk_tier(score)== "High Risk"

def test_scores_use_declared_band_points():
  assert score_vitals(hr= 45, resp= 10, spo2= 93, temp= 35.5, sbp= 95)== 7