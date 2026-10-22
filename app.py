from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import joblib
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(
    title="MLOps Iris Classifier API",
    description="Production-ready FastAPI service serving Scikit-learn Random Forest model with Prometheus metrics",
    version="0.1.0"
)

# Prometheus metrics definition
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status_code"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency in seconds",
    ["endpoint"]
)
PREDICTION_COUNT = Counter(
    "model_predictions_total",
    "Total Predictions by Class",
    ["predicted_class"]
)

# Load trained model
MODEL_PATH = "model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

# Target class mapping
TARGET_NAMES = {0: "setosa", 1: "versicolor", 2: "virginica"}

class PredictionInput(BaseModel):
    features: list[float] = Field(
        ..., 
        json_schema_extra={"example": [5.1, 3.5, 1.4, 0.2]},
        description="Sepal length, sepal width, petal length, petal width (in cm)"
    )

@app.get("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/", status_code="200").inc()
    return {
        "message": "MLOps prediction API running",
        "model_loaded": model is not None,
        "docs_url": "/docs"
    }

@app.get("/health")
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status_code="200").inc()
    return {
        "status": "healthy" if model is not None else "degraded",
        "service": "iris-prediction-api"
    }

@app.post("/predict")
def predict(data: PredictionInput):
    t0 = time.perf_counter()
    if model is None:
        REQUEST_COUNT.labels(method="POST", endpoint="/predict", status_code="503").inc()
        raise HTTPException(status_code=503, detail="Model artifact model.pkl not loaded")
    
    if len(data.features) != 4:
        REQUEST_COUNT.labels(method="POST", endpoint="/predict", status_code="422").inc()
        raise HTTPException(
            status_code=422, 
            detail=f"Expected 4 features, got {len(data.features)}"
        )

    prediction = model.predict([data.features])
    latency = time.perf_counter() - t0
    
    REQUEST_LATENCY.labels(endpoint="/predict").observe(latency)
    pred_int = int(prediction[0])
    class_name = TARGET_NAMES.get(pred_int, "unknown")
    PREDICTION_COUNT.labels(predicted_class=class_name).inc()
    REQUEST_COUNT.labels(method="POST", endpoint="/predict", status_code="200").inc()

    return {
        "prediction": pred_int,
        "flower_class": class_name,
        "status": "success",
        "latency_ms": round(latency * 1000, 3)
    }

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
