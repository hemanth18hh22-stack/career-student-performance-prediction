import asyncio
import base64
import json
import os
import subprocess
import time
import httpx
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARTIFACT_DIR = r"C:\Users\Hemanth\.gemini\antigravity-ide\brain\820e4cde-9705-47c6-a255-1d63b048c451"

screens = [
    ("screen_login.png", "http://localhost:8501/?screen=login"),
    ("screen_signup.png", "http://localhost:8501/?screen=signup"),
    ("screen_otp.png", "http://localhost:8501/?screen=otp"),
    ("screen_onboarding.png", "http://localhost:8501/?screen=onboarding"),
    ("screen_analyzer.png", "http://localhost:8501/?screen=analyzer"),
]

async def capture_all():
    chrome_proc = subprocess.Popen([
        CHROME_PATH,
        "--headless=new",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1400,950"
    ])
    
    time.sleep(2)
    try:
        for fname, url in screens:
            async with httpx.AsyncClient() as client:
                resp = await client.put(f"http://127.0.0.1:9222/json/new?{url}")
                tab_info = resp.json()
                ws_url = tab_info["webSocketDebuggerUrl"]
                tab_id = tab_info["id"]

            async with websockets.connect(ws_url, max_size=25_000_000) as ws:
                await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
                await asyncio.sleep(2.5)

                msg_id = 100
                await ws.send(json.dumps({
                    "id": msg_id,
                    "method": "Page.captureScreenshot",
                    "params": {"format": "png"}
                }))
                while True:
                    m = json.loads(await ws.recv())
                    if m.get("id") == msg_id:
                        data = base64.b64decode(m["result"]["data"])
                        out_p = os.path.join(ARTIFACT_DIR, fname)
                        with open(out_p, "wb") as f:
                            f.write(data)
                        print(f"Captured {fname} ({len(data)} bytes)")
                        break

            # Close tab
            async with httpx.AsyncClient() as client:
                await client.get(f"http://127.0.0.1:9222/json/close/{tab_id}")

    finally:
        chrome_proc.terminate()

if __name__ == "__main__":
    asyncio.run(capture_all())
