from fastapi import FastAPI
from pydantic import BaseModel
import random
from datetime import datetime, timezone


app = FastAPI(title="Mock ML Engine")


class PredictRequest(BaseModel):
    request_id: str
    timestamp: str
    window_size: int
    records: list


@app.post('/api/predict')
def predict(request: PredictRequest):
    risk_score = round(random.uniform(0.3, 0.9), 2)

    if risk_score < 0.33:
        risk_level = 'low'
    elif risk_score < 0.66:
        risk_level = 'medium'
    else:
        risk_level = 'high'

    return {
        'request_id': request.request_id,
        'processed_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "forecast": {
                    "param1_next_1h": round(random.uniform(200, 300), 1),
                    "param1_next_6h": [round(random.uniform(200, 300), 1) for _ in range(6)],
                    "confidence": round(random.uniform(0.7, 0.95), 2),
                    "mape": round(random.uniform(2, 5), 1),
                },
                "anomalies": [
                    {
                        "type": "param_anomaly",
                        "param": f'param{random.randint(1, 5)}',
                        "severity": random.choice(['low', 'high', 'medium']),
                        "unit_id": f"unit-{random.randint(1, 20)}",
                        "description": "Abnormal behavior detected",
                        "score": round(random.uniform(0.5, 0.95), 2),
                    }
                ],
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_breakdown": {
                    "load_risk": round(random.uniform(0.3, 0.8), 2),
                    "anomaly_risk": round(random.uniform(0.3, 0.8), 2),
                    "forecast_risk": round(random.uniform(0.3, 0.8), 2),
                },
                "decisions": [
                    {
                        "priority": 1,
                        "action": "Check unit A status",
                        "reason": "Sudden increase in param1",
                        "urgency": "high",
                    }
                ],
            }
        
        

