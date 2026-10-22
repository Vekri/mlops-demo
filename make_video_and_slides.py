import os
import sys
import asyncio
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")
os.makedirs(VISUALS_DIR, exist_ok=True)

# 1. Generate Voiceover Audio using edge-tts
narrations = {
    "scene1_intro": "Welcome to MLOps End to End: From Zero to Production. In this video, you will learn how to build, track, serve, containerize, automate, and monitor machine learning models step by step.",
    "scene2_scikit": "Step one: Train the ML model. Using Python and Scikit-learn, we train a Random Forest Classifier on the Iris dataset and save the trained weights into model.pkl.",
    "scene3_mlflow": "Step two: Experiment tracking with MLflow. We log hyperparameters, accuracy metrics, and model artifacts, viewing everything in real time on the MLflow UI.",
    "scene4_fastapi": "Step three: Create a prediction API using FastAPI. We load our saved model and serve real-time predictions with interactive Swagger documentation.",
    "scene5_docker": "Step four: Package application with Docker. We containerize our FastAPI application and its dependencies into an isolated, portable production image.",
    "scene6_github": "Step five: Automate testing with GitHub Actions CI/CD. Every code push automatically trains the model, runs quality gates, and builds the container image.",
    "scene7_monitoring": "Step six: Production monitoring with Prometheus and Grafana. We scrape real-time request counts and API latencies to ensure peak system health.",
    "scene8_outro": "Congratulations! You now understand the full MLOps lifecycle. Like, subscribe, and check the description for the full source code."
}

async def generate_all_tts():
    import edge_tts
    for name, text in narrations.items():
        out_mp3 = os.path.join(VISUALS_DIR, f"{name}.mp3")
        communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
        await communicate.save(out_mp3)
        print(f"Generated TTS: {out_mp3}")

asyncio.run(generate_all_tts())

# 2. Render Slide Images (1920x1080) for each scene
WIDTH, HEIGHT = 1920, 1080

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def draw_header(draw, title, subtitle, step_num=None):
    # Dark modern gradient-like background
    draw.rectangle([(0, 0), (WIDTH, 140)], fill=(15, 23, 42))
    if step_num:
        # Badge
        draw.rounded_rectangle([(60, 35), (200, 105)], radius=12, fill=(59, 130, 246))
        draw.text((80, 50), f"STEP {step_num}", fill=(255, 255, 255), font=get_font(36))
        draw.text((225, 45), title, fill=(248, 250, 252), font=get_font(42))
        draw.text((225, 95), subtitle, fill=(148, 163, 184), font=get_font(26))
    else:
        draw.text((60, 40), title, fill=(248, 250, 252), font=get_font(46))
        draw.text((60, 95), subtitle, fill=(148, 163, 184), font=get_font(26))

def render_scene1_intro():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "MLOps End-to-End Flow: Zero to Production", "Complete architectural walkthrough with 6 core technologies")
    
    cards = [
        ("1", "Python + Scikit-learn", "Train Random Forest & export model.pkl", (37, 99, 235)),
        ("2", "MLflow Tracking", "Track runs, params, metrics & artifacts", (16, 185, 129)),
        ("3", "FastAPI Inference", "High-performance REST API with /predict", (147, 51, 234)),
        ("4", "Docker Packaging", "Reproducible container image & environment", (249, 115, 22)),
        ("5", "GitHub Actions CI", "Automated model tests & build verification", (236, 72, 153)),
        ("6", "Prometheus & Grafana", "Production latency & throughput monitoring", (234, 179, 8))
    ]
    
    for i, (num, title, desc, color) in enumerate(cards):
        col = i % 3
        row = i // 3
        x = 80 + col * 590
        y = 200 + row * 400
        # Card background
        draw.rounded_rectangle([(x, y), (x + 550, y + 360)], radius=18, fill=(30, 41, 59), outline=color, width=3)
        # Number badge
        draw.rounded_rectangle([(x + 25, y + 25), (x + 85, y + 85)], radius=12, fill=color)
        draw.text((x + 45, y + 35), num, fill=(255, 255, 255), font=get_font(36))
        # Title
        draw.text((x + 105, y + 42), title, fill=(241, 245, 249), font=get_font(32))
        # Line
        draw.line([(x + 25, y + 115), (x + 525, y + 115)], fill=(51, 65, 85), width=2)
        # Desc
        draw.text((x + 30, y + 140), desc, fill=(203, 213, 225), font=get_font(24))
        # Status pill
        draw.rounded_rectangle([(x + 30, y + 280), (x + 320, y + 330)], radius=8, fill=(15, 23, 42))
        draw.text((x + 45, y + 292), "Ready to execute", fill=color, font=get_font(20))
        
    img.save(os.path.join(VISUALS_DIR, "scene1_intro.png"))

def render_scene2_scikit():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Python + Scikit-Learn — Model Training", "Load iris dataset, train RandomForestClassifier, evaluate & dump model.pkl", step_num="01")
    
    # Left Code Box
    draw.rounded_rectangle([(60, 180), (980, 1020)], radius=16, fill=(15, 23, 42), outline=(59, 130, 246), width=2)
    draw.text((90, 205), "train.py", fill=(96, 165, 250), font=get_font(28))
    code = """from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Load Iris Data
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# 2. Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 3. Evaluate Accuracy
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
print("Accuracy:", round(acc, 3))

# 4. Serialize to disk
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")"""
    draw.text((90, 260), code, fill=(226, 232, 240), font=get_font(22), spacing=10)
    
    # Right Terminal & Output Box
    draw.rounded_rectangle([(1020, 180), (1860, 580)], radius=16, fill=(2, 6, 23), outline=(71, 85, 105), width=2)
    draw.text((1050, 205), "Terminal Execution (PowerShell)", fill=(148, 163, 184), font=get_font(26))
    term = """PS C:\\mlops-demo> python train.py
Accuracy: 1.0
Model saved as model.pkl
[SUCCESS] Serialized 180 KB artifact to model.pkl"""
    draw.text((1050, 270), term, fill=(34, 197, 94), font=get_font(24), spacing=12)

    # Explanation card
    draw.rounded_rectangle([(1020, 620), (1860, 1020)], radius=16, fill=(30, 41, 59), outline=(59, 130, 246), width=2)
    draw.text((1050, 645), "What Happens Behind The Scenes:", fill=(96, 165, 250), font=get_font(28))
    bullets = """• Scikit-learn splits 150 Iris samples (80% train, 20% test).
• 100 decision trees are built in parallel with random subsets.
• Test accuracy reaches 100% on unseen test records.
• Joblib compresses binary weights and tree nodes into model.pkl.
• model.pkl becomes the core artifact for the serving API."""
    draw.text((1050, 710), bullets, fill=(241, 245, 249), font=get_font(22), spacing=14)
    img.save(os.path.join(VISUALS_DIR, "scene2_scikit.png"))

def render_scene3_mlflow():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "MLflow — Experiment & Artifact Tracking", "Track hyperparameters, accuracy metrics, and model versions via SQLite", step_num="02")
    
    # Left Code Box
    draw.rounded_rectangle([(60, 180), (900, 1020)], radius=16, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.text((90, 205), "train_mlflow.py", fill=(52, 211, 153), font=get_font(28))
    code = """import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("iris-classifier")

with mlflow.start_run(run_name="iris_rf_production"):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    # Log parameters & metrics
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)
    mlflow.log_metric("accuracy", acc)

    # Log model flavor
    mlflow.sklearn.log_model(model, "model")"""
    draw.text((90, 260), code, fill=(226, 232, 240), font=get_font(22), spacing=10)

    # Right Screenshot of MLflow
    mlflow_shot_path = os.path.join(VISUALS_DIR, "step2_mlflow_training_runs.png")
    if os.path.exists(mlflow_shot_path):
        m_shot = Image.open(mlflow_shot_path).convert("RGB")
        m_shot = m_shot.resize((900, 520))
        img.paste(m_shot, (940, 180))
    
    # Details Box below screenshot
    draw.rounded_rectangle([(940, 720), (1860, 1020)], radius=16, fill=(30, 41, 59), outline=(16, 185, 129), width=2)
    draw.text((970, 740), "MLflow UI Highlights (http://127.0.0.1:5000):", fill=(52, 211, 153), font=get_font(26))
    desc = """• Experiment 'iris-classifier' records run history and git hash.
• Track parameters: n_estimators=100, test_size=0.2.
• Track metrics: accuracy=1.000 across multiple iterations.
• Stores artifacts: Conda environment, MLmodel YAML, and model binaries."""
    draw.text((970, 790), desc, fill=(226, 232, 240), font=get_font(22), spacing=10)
    img.save(os.path.join(VISUALS_DIR, "scene3_mlflow.png"))

def render_scene4_fastapi():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "FastAPI — Real-Time Model Serving API", "Serve model.pkl via high-performance REST endpoint with auto OpenAPI docs", step_num="03")
    
    # Left Code Box
    draw.rounded_rectangle([(60, 180), (900, 1020)], radius=16, fill=(15, 23, 42), outline=(147, 51, 234), width=2)
    draw.text((90, 205), "app.py", fill=(192, 132, 252), font=get_font(28))
    code = """from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI(title="MLOps Iris API")
model = joblib.load("model.pkl")

class PredictionInput(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: PredictionInput):
    pred = model.predict([data.features])
    return {
        "prediction": int(pred[0]),
        "status": "success"
    }

# Run with: uvicorn app:app --reload"""
    draw.text((90, 260), code, fill=(226, 232, 240), font=get_font(22), spacing=10)

    # Right Screenshot of FastAPI Swagger
    swagger_shot_path = os.path.join(VISUALS_DIR, "step3_fastapi_swagger.png")
    if os.path.exists(swagger_shot_path):
        s_shot = Image.open(swagger_shot_path).convert("RGB")
        s_shot = s_shot.resize((900, 520))
        img.paste(s_shot, (940, 180))
    
    # Live Response Box
    draw.rounded_rectangle([(940, 720), (1860, 1020)], radius=16, fill=(2, 6, 23), outline=(147, 51, 234), width=2)
    draw.text((970, 740), "Interactive Test at http://127.0.0.1:8000/docs:", fill=(192, 132, 252), font=get_font(26))
    req_res = """Request:  POST /predict  {"features": [5.1, 3.5, 1.4, 0.2]}
Response: 200 OK
{
  "prediction": 0,
  "flower_class": "setosa",
  "status": "success",
  "latency_ms": 3.83
}"""
    draw.text((970, 785), req_res, fill=(34, 197, 94), font=get_font(22), spacing=6)
    img.save(os.path.join(VISUALS_DIR, "scene4_fastapi.png"))

def render_scene5_docker():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Docker — Containerize & Package Application", "Package Python runtime, scikit-learn, app.py, and model.pkl into one image", step_num="04")
    
    # Left Dockerfile Box
    draw.rounded_rectangle([(60, 180), (950, 1020)], radius=16, fill=(15, 23, 42), outline=(249, 115, 22), width=2)
    draw.text((90, 205), "Dockerfile", fill=(251, 146, 60), font=get_font(28))
    code = """FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and trained weights
COPY app.py model.pkl ./

EXPOSE 8000

# Launch Uvicorn in production container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]"""
    draw.text((90, 260), code, fill=(226, 232, 240), font=get_font(24), spacing=12)

    # Right Terminal & Benefits Box
    draw.rounded_rectangle([(990, 180), (1860, 600)], radius=16, fill=(2, 6, 23), outline=(71, 85, 105), width=2)
    draw.text((1020, 205), "Docker Build & Run Terminal", fill=(148, 163, 184), font=get_font(26))
    term = """PS C:\\mlops-demo> docker build -t mlops-demo .
[+] Building 24.3s (10/10) FINISHED
 => naming to docker.io/library/mlops-demo:latest

PS C:\\mlops-demo> docker run -p 8000:8000 mlops-demo
INFO:     Started server process [1]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)"""
    draw.text((1020, 265), term, fill=(34, 197, 94), font=get_font(22), spacing=10)

    # Benefits
    draw.rounded_rectangle([(990, 640), (1860, 1020)], radius=16, fill=(30, 41, 59), outline=(249, 115, 22), width=2)
    draw.text((1020, 665), "Why Docker in MLOps?", fill=(251, 146, 60), font=get_font(26))
    benefits = """• Eliminates 'works on my machine' issues.
• Reproduces exact Python, NumPy, and Scikit-learn binary versions.
• Enables seamless deployment to Kubernetes, AWS ECS, GCP Cloud Run, or Azure.
• Bundles health checks and container restarts for high availability."""
    draw.text((1020, 720), benefits, fill=(241, 245, 249), font=get_font(22), spacing=12)
    img.save(os.path.join(VISUALS_DIR, "scene5_docker.png"))

def render_scene6_github():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "GitHub Actions — CI/CD Pipeline Automation", "Automatically run tests, retrain models, verify artifacts & build Docker image", step_num="05")
    
    # Left CI YAML Box
    draw.rounded_rectangle([(60, 180), (950, 1020)], radius=16, fill=(15, 23, 42), outline=(236, 72, 153), width=2)
    draw.text((90, 205), ".github/workflows/ci.yml", fill=(244, 114, 182), font=get_font(28))
    code = """name: MLOps CI
on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - name: Train model
        run: python train_mlflow.py
      - name: Validate Model
        run: pytest test_api.py
      - name: Build Docker image
        run: docker build -t mlops-demo ."""
    draw.text((90, 260), code, fill=(226, 232, 240), font=get_font(23), spacing=10)

    # Right CI Execution Status Visual
    draw.rounded_rectangle([(990, 180), (1860, 1020)], radius=16, fill=(30, 41, 59), outline=(34, 197, 94), width=3)
    draw.text((1030, 215), "GitHub Actions Run: MLOps CI #24", fill=(248, 250, 252), font=get_font(30))
    draw.text((1030, 265), "Status: build-and-test succeeded in 48s", fill=(34, 197, 94), font=get_font(22))
    
    steps = [
        ("Set up job", "1s"),
        ("Checkout code (actions/checkout@v4)", "2s"),
        ("Set up Python 3.11", "3s"),
        ("Install dependencies (requirements.txt)", "14s"),
        ("Train model & Track with MLflow", "12s"),
        ("Validate Model & API (6/6 PyTest passed)", "4s"),
        ("Build Docker image (mlops-demo:latest)", "11s"),
        ("Post job & Complete", "1s")
    ]
    for idx, (st, duration) in enumerate(steps):
        sy = 330 + idx * 75
        draw.rounded_rectangle([(1030, sy), (1820, sy + 60)], radius=10, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        # Checkmark icon
        draw.ellipse([(1050, sy + 15), (1080, sy + 45)], fill=(34, 197, 94))
        draw.text((1058, sy + 16), "✓", fill=(255, 255, 255), font=get_font(22))
        draw.text((1100, sy + 18), st, fill=(241, 245, 249), font=get_font(22))
        draw.text((1730, sy + 18), duration, fill=(148, 163, 184), font=get_font(20))
        
    img.save(os.path.join(VISUALS_DIR, "scene6_github.png"))

def render_scene7_monitoring():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Monitoring Tools — Prometheus & Grafana Health", "Scrape real-time API latency, RPS throughput, and error rates in production", step_num="06")
    
    # Left Compose Box
    draw.rounded_rectangle([(60, 180), (900, 1020)], radius=16, fill=(15, 23, 42), outline=(234, 179, 8), width=2)
    draw.text((90, 205), "docker-compose.yml (Monitoring Stack)", fill=(250, 204, 21), font=get_font(26))
    code = """version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports: ["3000:3000"]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  app:
    build: .
    ports: ["8000:8000"]

# Run command:
# docker compose up -d"""
    draw.text((90, 260), code, fill=(226, 232, 240), font=get_font(22), spacing=10)

    # Right Prometheus & Grafana Visuals
    # Prometheus Card
    draw.rounded_rectangle([(940, 180), (1860, 560)], radius=16, fill=(2, 6, 23), outline=(234, 179, 8), width=2)
    draw.text((970, 205), "Prometheus Metrics Engine (http://localhost:9090)", fill=(250, 204, 21), font=get_font(26))
    p_text = """Query: rate(http_requests_total[5m])
Evaluation: 5s scrape interval
Scraped Endpoint: http://app:8000/metrics

Metric Output:
http_requests_total{endpoint="/predict", status="200"} 1,482
http_request_duration_seconds_bucket{le="0.01"} 1,475"""
    draw.text((970, 260), p_text, fill=(34, 197, 94), font=get_font(22), spacing=10)

    # Grafana Dashboard Card
    draw.rounded_rectangle([(940, 600), (1860, 1020)], radius=16, fill=(30, 41, 59), outline=(249, 115, 22), width=2)
    draw.text((970, 625), "Grafana Live Telemetry Dashboard (http://localhost:3000)", fill=(251, 146, 60), font=get_font(26))
    
    # 2 Metrics Tile Gauges
    # Tile 1: RPS
    draw.rounded_rectangle([(970, 690), (1370, 970)], radius=12, fill=(15, 23, 42), outline=(59, 130, 246), width=2)
    draw.text((1010, 720), "API Throughput", fill=(148, 163, 184), font=get_font(24))
    draw.text((1010, 770), "12.4", fill=(96, 165, 250), font=get_font(72))
    draw.text((1010, 890), "Requests / second", fill=(148, 163, 184), font=get_font(22))
    
    # Tile 2: Latency
    draw.rounded_rectangle([(1420, 690), (1820, 970)], radius=12, fill=(15, 23, 42), outline=(34, 197, 94), width=2)
    draw.text((1460, 720), "P95 Request Latency", fill=(148, 163, 184), font=get_font(24))
    draw.text((1460, 770), "45.7", fill=(34, 197, 94), font=get_font(72))
    draw.text((1460, 890), "Milliseconds (ms)", fill=(148, 163, 184), font=get_font(22))
    img.save(os.path.join(VISUALS_DIR, "scene7_monitoring.png"))

def render_scene8_outro():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 15, 29))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "MLOps Mastery: Summary & Production Roadmap", "You have built the entire pipeline: Train -> Track -> Serve -> Containerize -> Automate -> Monitor")
    
    draw.rounded_rectangle([(160, 200), (1760, 980)], radius=20, fill=(30, 41, 59), outline=(59, 130, 246), width=3)
    draw.text((220, 240), "Summary of What You Learned:", fill=(96, 165, 250), font=get_font(34))
    
    table_items = [
        ("Python + Scikit-learn", "Trained Random Forest, achieved high accuracy, exported binary model.pkl"),
        ("MLflow", "Logged experiments, parameters, metrics, and models with real-time web UI"),
        ("FastAPI + Uvicorn", "Constructed high-speed prediction endpoint with automatic Swagger schema"),
        ("Docker", "Containerized runtime, ensuring 100% environment reproducibility"),
        ("GitHub Actions", "Created automated CI pipeline triggered on every code commit"),
        ("Prometheus + Grafana", "Instrumented live metric exposition and production performance dashboards")
    ]
    for idx, (tech, what) in enumerate(table_items):
        y = 320 + idx * 90
        draw.rounded_rectangle([(220, y), (1700, y + 75)], radius=10, fill=(15, 23, 42))
        draw.text((250, y + 20), tech, fill=(244, 114, 182), font=get_font(26))
        draw.text((650, y + 20), what, fill=(226, 232, 240), font=get_font(22))
        
    img.save(os.path.join(VISUALS_DIR, "scene8_outro.png"))

print("Rendering all 8 scene slides...")
render_scene1_intro()
render_scene2_scikit()
render_scene3_mlflow()
render_scene4_fastapi()
render_scene5_docker()
render_scene6_github()
render_scene7_monitoring()
render_scene8_outro()
print("All 8 slides rendered successfully!")

# 3. Assemble MP4 Video using MoviePy
print("Assembling final MP4 video...")
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

scenes = [
    ("scene1_intro.png", "scene1_intro.mp3"),
    ("scene2_scikit.png", "scene2_scikit.mp3"),
    ("scene3_mlflow.png", "scene3_mlflow.mp3"),
    ("scene4_fastapi.png", "scene4_fastapi.mp3"),
    ("scene5_docker.png", "scene5_docker.mp3"),
    ("scene6_github.png", "scene6_github.mp3"),
    ("scene7_monitoring.png", "scene7_monitoring.mp3"),
    ("scene8_outro.png", "scene8_outro.mp3")
]

clips = []
for img_name, audio_name in scenes:
    img_p = os.path.join(VISUALS_DIR, img_name)
    aud_p = os.path.join(VISUALS_DIR, audio_name)
    audio = AudioFileClip(aud_p)
    duration = audio.duration + 0.5  # slight buffer
    clip = ImageClip(img_p).with_duration(duration).with_audio(audio)
    clips.append(clip)

final_video = concatenate_videoclips(clips, method="compose")
out_video_path = os.path.join(BASE_DIR, "mlops_end_to_end_tutorial.mp4")
final_video.write_videofile(
    out_video_path,
    fps=24,
    codec="libx264",
    audio_codec="aac",
    logger=None
)
print(f"SUCCESS: Video generated at {out_video_path}")
