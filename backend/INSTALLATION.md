# 🚀 Complete Installation & Setup Guide

## Table of Contents
1. [Windows Installation](#windows-installation)
2. [macOS Installation](#macos-installation)
3. [Linux Installation](#linux-installation)
4. [Cloudflare Tunnel Setup](#cloudflare-tunnel-setup)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Windows Installation

### Method 1: Automated Setup (Recommended)

1. **Open Command Prompt** (or PowerShell)
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to project directory:**
   ```bash
   cd path\to\edge-device-controller
   ```

3. **Run the setup script:**
   ```bash
   python setup.py
   ```

   This will automatically:
   - ✅ Check Python installation
   - ✅ Install all Python packages
   - ✅ Download and install Cloudflared

### Method 2: Manual Setup

#### Step 1: Install Python

1. Download from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

#### Step 2: Install Python Packages

```bash
cd path\to\edge-device-controller
pip install -r requirements.txt
```

**What gets installed:**
- `fastapi` - Web framework
- `uvicorn` - Server
- `qrcode` - QR generation
- `pillow` - Image support
- `websockets` - Real-time connection

#### Step 3: Install Cloudflared

**Option A: Download & Manual Install (Best for Beginners)**

1. Go to: https://github.com/cloudflare/cloudflared/releases
2. Download **cloudflared-windows-amd64.exe** (for 64-bit Windows)
3. Right-click the file → Rename to `cloudflared.exe`
4. Move to: `C:\Windows\System32\` (requires admin)
5. Verify:
   ```bash
   cloudflared --version
   ```

**Option B: Using Chocolatey (If installed)**

```bash
choco install cloudflare-warp
```

**Option C: Using Scoop (If installed)**

```bash
scoop install cloudflared
```

---

## macOS Installation

### Step 1: Install Python

If you don't have Python 3.8+:

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Verify
python3 --version
```

### Step 2: Install Dependencies

```bash
cd path/to/edge-device-controller
pip3 install -r requirements.txt
```

### Step 3: Install Cloudflared

```bash
brew install cloudflare/cloudflare/cloudflared
```

Verify:
```bash
cloudflared --version
```

---

## Linux Installation

### Ubuntu/Debian

#### Step 1: Install Python

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

#### Step 2: Install Dependencies

```bash
cd path/to/edge-device-controller
pip3 install -r requirements.txt
```

#### Step 3: Install Cloudflared

**Option A: Using APT (Debian/Ubuntu)**

```bash
sudo -i
# Add Cloudflare repository
echo "deb http://deb.debian.org/debian bullseye-backports main" | tee /etc/apt/sources.list.d/bullseye-backports.list
apt update
apt install -t bullseye-backports cloudflared

# Verify
cloudflared --version
```

**Option B: Download Binary**

```bash
# Download
cd /tmp
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz

# Extract & Install
tar xzf cloudflared-linux-amd64.tgz
sudo cp cloudflared /usr/bin/
sudo chmod +x /usr/bin/cloudflared

# Verify
cloudflared --version
```

### Fedora/RHEL

```bash
# Install Cloudflared directly
sudo dnf install cloudflared

# Or from binary
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz | tar xz
sudo cp cloudflared /usr/bin/
```

---

## Cloudflare Tunnel Setup

### Quick Start (Ephemeral Tunnel)

The main.py script automatically uses an ephemeral tunnel:

```bash
python main.py
```

Output will show:
```
🌍 Public URL: https://xxxxxx.trycloudflare.com
🔌 WebSocket URL: wss://xxxxxx.trycloudflare.com/ws
```

### Production Setup (Named Tunnel)

For persistent URLs and better control:

#### Step 1: Authenticate

```bash
cloudflared tunnel login
```

- Opens browser
- Select your Cloudflare domain
- Downloads certificate

#### Step 2: Create Tunnel

```bash
cloudflared tunnel create my-edge-device
```

Note the **TUNNEL_ID** shown in output

#### Step 3: Create Configuration

**Windows**: Create `%USERPROFILE%\.cloudflared\config.yml`

**macOS/Linux**: Create `~/.cloudflared/config.yml`

```yaml
tunnel: my-edge-device
credentials-file: ~/.cloudflared/UUID.json

ingress:
  - hostname: device.yourdomain.com
    service: http://localhost:8000
    websocket: true
  - service: http_status:404
```

#### Step 4: Add DNS Record

1. Go to: https://dash.cloudflare.com/
2. Select your domain
3. DNS → Add Record
4. Create CNAME:
   - Name: `device`
   - Target: `UUID.cfargotunnel.com`

#### Step 5: Run Named Tunnel

```bash
cloudflared tunnel run my-edge-device
```

---

## Running the Application

### Option 1: Cloudflare Tunnel (Internet Access)

```bash
python main.py
```

**Access:**
- HTTP: `https://xxxxxx.trycloudflare.com`
- WebSocket: `wss://xxxxxx.trycloudflare.com/ws`

### Option 2: Local Server (LAN Access)

```bash
python other-scripts/server.py
```

Or use the menu:

```bash
python start.py
```

**Access:**
- HTTP: `http://192.168.x.x:8000`
- WebSocket: `ws://192.168.x.x:8000/ws`

### Option 3: Using Uvicorn Directly

**With auto-reload:**
```bash
uvicorn main:app --reload
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Troubleshooting

### ❌ "Python command not found"

**Windows:**
- Download Python from https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**
- Restart command prompt

**macOS/Linux:**
```bash
# Use python3 instead
python3 main.py

# Or create alias
alias python=python3
```

### ❌ "cloudflared command not found"

**Windows:**
1. Download from: https://github.com/cloudflare/cloudflared/releases
2. Place in: `C:\Windows\System32\`
3. Restart terminal

**macOS:**
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Linux:**
```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz | tar xz
sudo cp cloudflared /usr/bin/
sudo chmod +x /usr/bin/cloudflared
```

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install fastapi uvicorn websockets qrcode pillow
```

### ❌ "Port 8000 already in use"

**Windows:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number)
taskkill /PID <PID> /F

# Or use different port
python main.py --port 8001
```

**macOS/Linux:**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### ❌ "Tunnel won't start"

1. Check internet connection
2. Verify cloudflared is installed:
   ```bash
   cloudflared --version
   ```
3. Check firewall isn't blocking
4. Restart the application

### ❌ "WebSocket connection refused"

- Verify the tunnel URL is correct
- Check port 8000 is accessible
- Ensure the server is running
- Check browser console for full error message

---

## Quick Command Reference

| Command | Purpose |
|---------|---------|
| `python setup.py` | Automated setup (Windows/Mac/Linux) |
| `python main.py` | Run with Cloudflare tunnel |
| `python other-scripts/server.py` | Run local server |
| `python start.py` | Interactive menu |
| `cloudflared --version` | Check Cloudflared version |
| `cloudflared tunnel login` | Authenticate with Cloudflare |
| `cloudflared tunnel create NAME` | Create named tunnel |
| `cloudflared tunnel run NAME` | Run named tunnel |

---

## Useful Links

| Resource | URL |
|----------|-----|
| Python | https://www.python.org/downloads/ |
| FastAPI Docs | https://fastapi.tiangolo.com/ |
| Cloudflared Releases | https://github.com/cloudflare/cloudflared/releases |
| Cloudflare Tunnel Docs | https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/ |
| Cloudflare Dashboard | https://dash.cloudflare.com/ |

---

**Last Updated**: February 2026
**Compatibility**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
