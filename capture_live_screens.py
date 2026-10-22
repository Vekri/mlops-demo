import subprocess
import time
import sys
import os
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_DIR = os.path.abspath("visuals")
os.makedirs(OUT_DIR, exist_ok=True)

print("Starting MLflow server on port 5000...")
mlflow_proc = subprocess.Popen(
    [sys.executable, "-m", "mlflow", "server", "--backend-store-uri", "sqlite:///mlflow.db", "--port", "5000", "--host", "127.0.0.1"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("Starting FastAPI server on port 8000...")
fastapi_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app:app", "--port", "8000", "--host", "127.0.0.1"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(6)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Step 2: MLflow UI Screenshot
        print("Navigating to MLflow UI...")
        try:
            page.goto("http://127.0.0.1:5000", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(3000)
            mlflow_path = os.path.join(OUT_DIR, "step2_mlflow_ui.png")
            page.screenshot(path=mlflow_path)
            print(f"Captured MLflow screenshot: {mlflow_path}")
        except Exception as e:
            print(f"MLflow capture error: {e}")

        # Step 3: FastAPI Swagger Docs Screenshot
        print("Navigating to FastAPI Docs...")
        try:
            page.goto("http://127.0.0.1:8000/docs", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(2000)
            # Expand predict endpoint if available
            try:
                page.click("button.opblock-summary-control")
                page.wait_for_timeout(1000)
            except Exception:
                pass
            fastapi_path = os.path.join(OUT_DIR, "step3_fastapi_swagger.png")
            page.screenshot(path=fastapi_path)
            print(f"Captured FastAPI screenshot: {fastapi_path}")
        except Exception as e:
            print(f"FastAPI capture error: {e}")

        browser.close()

finally:
    print("Terminating background servers...")
    mlflow_proc.terminate()
    fastapi_proc.terminate()
    mlflow_proc.wait()
    fastapi_proc.wait()
    print("Servers terminated cleanly.")
