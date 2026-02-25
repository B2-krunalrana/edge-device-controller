# ⚡ Quick Start Guide

## 🎯 TL;DR (Too Long; Didn't Read)

### Windows Users
```bash
# First time only - Automated setup
python setup.py

# Then just run:
python main.py
```

### macOS/Linux Users
```bash
# First time only
python3 setup.py

# Then just run:
python3 main.py
```

---

## 📋 What You Get

✅ **Public HTTPS URL** - Access from anywhere  
✅ **Secure WebSocket** - Real-time communication  
✅ **QR Code** - Easy device connection  
✅ **Free Tunnel** - No credit card needed  

---

## 🚀 Running the App

### Method 1: Interactive Menu (EASIEST)
```bash
python start.py
```
Then choose option 1 or 2

### Method 2: With Cloudflare Tunnel
```bash
python main.py
```
- ✅ Internet access
- ✅ HTTPS + WSS
- ✅ Best for remote sites

### Method 3: Local Network Only
```bash
python other-scripts/server.py
```
- ✅ Lower latency
- ✅ No internet needed
- ✅ Works on same network

---

## 🔗 Access URLs

### With Cloudflare Tunnel:
```
HTTP: https://xxxxxx.trycloudflare.com
WebSocket: wss://xxxxxx.trycloudflare.com/ws
```
(URL shown when main.py runs)

### Local Network:
```
HTTP: http://192.168.x.x:8000
WebSocket: ws://192.168.x.x:8000/ws
```
(Replace x.x with your local IP)

---

## 📦 Installation Commands

### All Platforms (First Time):
```bash
# Install Python packages
pip install -r requirements.txt

# Install Cloudflared
cloudflared --version  # Check if installed
```

### Windows (If cloudflared missing):
1. Download: https://github.com/cloudflare/cloudflared/releases
2. Get: `cloudflared-windows-amd64.exe`
3. Move to: `C:\Windows\System32\`
4. Restart terminal

### macOS:
```bash
brew install cloudflare/cloudflare/cloudflared
```

### Linux (Ubuntu/Debian):
```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz | tar xz
sudo cp cloudflared /usr/bin/
sudo chmod +x /usr/bin/cloudflared
```

---

## 🧪 Test Connection

### Python:
```python
import asyncio
import websockets
import json

async def test():
    async with websockets.connect("wss://your-url/ws") as ws:
        await ws.send(json.dumps({"msg": "Hello"}))
        print(await ws.recv())

asyncio.run(test())
```

### Browser Console:
```javascript
const ws = new WebSocket("wss://your-url/ws");
ws.onmessage = e => console.log(e.data);
ws.send(JSON.stringify({msg: "Hello"}));
```

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| `python not found` | Add to PATH during install |
| `cloudflared not found` | Download from releases, move to System32 |
| `Port 8000 in use` | Close other apps or use `--port 8001` |
| `No internet access` | Use local server mode instead |
| `WebSocket won't connect` | Check URL, ensure server running |

---

## 📚 Documentation

- **Full Setup**: See `INSTALLATION.md`
- **Project Details**: See `README.md`
- **API Docs**: Run server → Visit `http://localhost:8000/docs`

---

## 🔑 Key Files

```
edge-device-controller/
├── main.py                  ← Run this for Cloudflare tunnel
├── other-scripts/server.py  ← Run this for local only
├── start.py                 ← Interactive menu
├── setup.py                 ← Automatic setup
├── requirements.txt         ← Python packages
├── README.md               ← Full documentation
├── INSTALLATION.md         ← Detailed setup guide
└── QUICKSTART.md           ← This file
```

---

## 💡 Tips

- 🎯 Use `start.py` for easy menu
- 🌐 Use `main.py` for internet access
- 🏠 Use `server.py` for fast local access
- 📱 Scan QR code to connect devices
- 🔐 Always use HTTPS URLs in production
- 🔌 Keep terminal running while app is active

---

## 📞 Need Help?

1. Check `INSTALLATION.md` for detailed steps
2. Review `README.md` for full documentation
3. Visit: https://developers.cloudflare.com/cloudflare-one/

---

**Ready?** Run: `python start.py` or `python main.py`

Good luck! 🚀
