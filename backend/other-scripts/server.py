from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import socket
import qrcode
import base64
from io import BytesIO

app = FastAPI()

# Get local IP
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

LOCAL_IP = get_local_ip()
WS_URL = f"ws://{LOCAL_IP}:8000/ws"

# Generate QR code as base64
def generate_qr_base64(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

QR_BASE64 = generate_qr_base64(WS_URL)

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        <head>
            <title>Device QR</title>
        </head>
        <body style="text-align:center;font-family:Arial;">
            <h2>Scan This QR To Connect</h2>
            <p><b>WebSocket URL:</b> {WS_URL}</p>
            <img src="data:image/png;base64,{QR_BASE64}" width="300"/>
        </body>
    </html>
    """

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Device Connected")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received: {data}")

            if data == "run_command":
                print("🚀 Running command on laptop...")
                await websocket.send_text("Command executed successfully!")

    except:
        print("❌ Connection closed")

if __name__ == "__main__":
    print(f"\n🌐 Open this in laptop browser: http://{LOCAL_IP}:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)