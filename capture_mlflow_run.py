import subprocess
import sys
import time
import socket
from playwright.sync_api import sync_playwright

proc = subprocess.Popen([sys.executable, "-m", "mlflow", "ui", "--backend-store-uri", "sqlite:///mlflow.db", "--host", "127.0.0.1", "--port", "5000"])
for _ in range(30):
    time.sleep(0.5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = s.connect_ex(("127.0.0.1", 5000))
    s.close()
    if res == 0:
        break

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 850})
        # Go to experiments directly
        page.goto("http://127.0.0.1:5000/#/experiments/1", wait_until="domcontentloaded")
        time.sleep(3)
        page.screenshot(path="visuals/step2_mlflow_run_details.png")
        print("Captured MLflow run details screenshot!")
        browser.close()
finally:
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except Exception:
        proc.kill()
