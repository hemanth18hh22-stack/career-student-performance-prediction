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
        async with httpx.AsyncClient() as client:
            resp = await client.put("http://127.0.0.1:9222/json/new?http://localhost:8501")
            tab_info = resp.json()
            ws_url = tab_info["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url, max_size=25_000_000) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            await asyncio.sleep(2)

            async def take_screenshot(name):
                msg_id = int(time.time() * 1000) % 1000000
                await ws.send(json.dumps({
                    "id": msg_id,
                    "method": "Page.captureScreenshot",
                    "params": {"format": "png"}
                }))
                while True:
                    m = json.loads(await ws.recv())
                    if m.get("id") == msg_id:
                        data = base64.b64decode(m["result"]["data"])
                        out_p = os.path.join(ARTIFACT_DIR, name)
                        with open(out_p, "wb") as f:
                            f.write(data)
                        print(f"Captured {name} ({len(data)} bytes)")
                        break

            # 1. Login screen
            await take_screenshot("1_login_screen.png")

            # 2. Click Signup link
            print("Clicking Go to Signup...")
            click_signup = {
                "id": 201,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.querySelector('div.st-key-go_to_signup button').click()"}
            }
            await ws.send(json.dumps(click_signup))
            await asyncio.sleep(2.5)
            await take_screenshot("2_signup_screen.png")

            # 3. Fill Signup and submit to get OTP
            print("Filling signup and submitting...")
            fill_signup = """
            (() => {
                const nameInput = document.querySelector('input[aria-label="Full Name"]');
                const emailInput = document.querySelector('input[aria-label="Email Address"]');
                const pwdInputs = document.querySelectorAll('input[type="password"]');
                
                function setNativeValue(element, value) {
                    const valueSetter = Object.getOwnPropertyDescriptor(element.__proto__, 'value').set;
                    valueSetter.call(element, value);
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                }

                if (nameInput) setNativeValue(nameInput, 'Alex Sharma');
                if (emailInput) setNativeValue(emailInput, 'alex@example.com');
                if (pwdInputs.length >= 2) {
                    setNativeValue(pwdInputs[0], 'password123');
                    setNativeValue(pwdInputs[1], 'password123');
                }
            })()
            """
            await ws.send(json.dumps({"id": 202, "method": "Runtime.evaluate", "params": {"expression": fill_signup}}))
            await asyncio.sleep(1)

            # Click create account
            await ws.send(json.dumps({"id": 203, "method": "Runtime.evaluate", "params": {"expression": "document.querySelector('div.st-key-signup_email_submit button').click()"}}))
            await asyncio.sleep(2.5)
            await take_screenshot("3_otp_screen.png")

            # 4. Read demo OTP and verify
            get_otp_code = """
            (() => {
                const badge = document.querySelector('.demo-otp-code');
                return badge ? badge.innerText.trim() : null;
            })()
            """
            await ws.send(json.dumps({"id": 204, "method": "Runtime.evaluate", "params": {"expression": get_otp_code, "returnByValue": True}}))
            while True:
                m = json.loads(await ws.recv())
                if m.get("id") == 204:
                    otp_code = m.get("result", {}).get("result", {}).get("value")
                    break

            print(f"Extracted Demo OTP: {otp_code}")
            if otp_code:
                enter_otp = f"""
                (() => {{
                    const otpInput = document.querySelector('input[aria-label="6-Digit Code"]');
                    if (otpInput) {{
                        const valueSetter = Object.getOwnPropertyDescriptor(otpInput.__proto__, 'value').set;
                        valueSetter.call(otpInput, '{otp_code}');
                        otpInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        otpInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }})()
                """
                await ws.send(json.dumps({"id": 205, "method": "Runtime.evaluate", "params": {"expression": enter_otp}}))
                await asyncio.sleep(1)
                await ws.send(json.dumps({"id": 206, "method": "Runtime.evaluate", "params": {"expression": "document.querySelector('div.st-key-otp_verify_btn button').click()"}}))
                await asyncio.sleep(3)
                await take_screenshot("4_onboarding_screen.png")

                # 5. Click Continue to Analyzer
                await ws.send(json.dumps({"id": 207, "method": "Runtime.evaluate", "params": {"expression": "document.querySelector('div.st-key-onboard_continue_btn button').click()"}}))
                await asyncio.sleep(3)
                await take_screenshot("5_analyzer_screen.png")

    finally:
        chrome_proc.terminate()

if __name__ == "__main__":
    asyncio.run(capture_all())
