import subprocess
import sys
import time
import socket
from playwright.sync_api import sync_playwright

proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"])
for _ in range(30):
    time.sleep(0.5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = s.connect_ex(("127.0.0.1", 8000))
    s.close()
    if res == 0:
        break

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("http://127.0.0.1:8000/docs", wait_until="domcontentloaded")
        time.sleep(2)
        try:
            page.locator(".opblock-summary-post").click()
            time.sleep(1)
            try_it = page.locator("button:has-text('Try it out')")
            if try_it.count() > 0:
                try_it.first.click()
                time.sleep(1)
        except Exception as e:
            print("Swagger click note:", e)
        page.screenshot(path="visuals/step3_fastapi_swagger.png")
        print("Updated step3_fastapi_swagger.png successfully!")
        browser.close()
finally:
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except Exception:
        proc.kill()
