import asyncio
import json
import subprocess
import time
import httpx
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def check():
    chrome_proc = subprocess.Popen([
        CHROME_PATH, "--headless=new", "--remote-debugging-port=9222",
        "--disable-gpu", "--no-first-run", "--window-size=1400,900"
    ])
    time.sleep(2)
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.put("http://127.0.0.1:9222/json/new?http://localhost:8501")
            ws_url = resp.json()["webSocketDebuggerUrl"]
        async with websockets.connect(ws_url) as ws:
            await asyncio.sleep(2)
            js = """
            (() => {
                const m = document.querySelector('.google-btn-marker');
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Google'));
                return {
                    m_exists: !!m,
                    btn_exists: !!btn,
                    m_parent: m ? m.parentElement.outerHTML.substring(0, 150) : null,
                    m_grandparent: m && m.parentElement ? m.parentElement.parentElement.outerHTML.substring(0, 150) : null,
                    btn_parent: btn ? btn.parentElement.outerHTML.substring(0, 150) : null,
                    btn_grandparent: btn && btn.parentElement ? btn.parentElement.parentElement.outerHTML.substring(0, 150) : null,
                    areSiblings: m && btn ? m.parentElement.parentElement.nextElementSibling === btn.parentElement.parentElement : null,
                    grandparentTag: m && m.parentElement ? m.parentElement.parentElement.tagName : null,
                    grandparentClass: m && m.parentElement ? m.parentElement.parentElement.className : null
                };
            })()
            """
            cmd = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {"expression": js, "returnByValue": True}
            }
            await ws.send(json.dumps(cmd))
            res = json.loads(await ws.recv())
            print(json.dumps(res["result"]["result"]["value"], indent=2))
    finally:
        chrome_proc.terminate()

if __name__ == "__main__":
    asyncio.run(check())
