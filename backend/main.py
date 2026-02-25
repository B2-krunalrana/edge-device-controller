import subprocess
import threading
import time
import requests
import re
import uvicorn
import qrcode
import base64
from io import BytesIO
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

tunnel_url = None
ws_url = None


# 🔥 Start Cloudflare Tunnel Automatically
def start_tunnel():
    global tunnel_url, ws_url

    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        print(line.strip())

        # Capture trycloudflare URL
        match = re.search(r"https://.*?trycloudflare.com", line)
        if match:
            tunnel_url = match.group(0)
            ws_url = tunnel_url.replace("https", "wss") + "/ws"
            print(f"\n🌍 Public URL: {tunnel_url}")
            print(f"🔌 WebSocket URL: {ws_url}\n")
            break


# 🔥 Run tunnel in background thread
threading.Thread(target=start_tunnel, daemon=True).start()


@app.get("/")
async def root():
    if not ws_url:
        return HTMLResponse("<h3>Starting tunnel... please refresh</h3>")

    # Generate QR dynamically
    qr = qrcode.make(ws_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edge Device Controller</title>
    </head>
    <body style="font-family:Arial;background:#ffffff;text-align:center;padding-top:50px;">
        <h2>Scan QR to Connect</h2>
        <p>{ws_url}</p>
        <img src="data:image/png;base64,{qr_base64}" width="250"/>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("📱 Phone Connected")

    try:
        while True:
            data = await websocket.receive_text()
            print("📩 Command Received:", data)
            await websocket.send_text("Command received by laptop")
    except:
        print("❌ Phone Disconnected")


if __name__ == "__main__":
    print("🚀 Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)