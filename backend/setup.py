#!/usr/bin/env python3
"""
Edge Device Controller - Automated Setup Script
Supports Windows, macOS, and Linux
"""

import subprocess
import sys
import os
import platform

def print_banner():
    print("\n" + "="*60)
    print("  Edge Device Controller - Automated Setup")
    print("="*60 + "\n")

def check_python():
    print("✅ Python detected:")
    print(f"   Version: {sys.version}")
    print()

def install_requirements():
    print("📦 Installing Python dependencies...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", "pip"
        ])
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ])
        
        print("\n✅ Python packages installed successfully!\n")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install Python packages\n")
        return False

def check_cloudflared():
    print("🔍 Checking Cloudflared...")
    
    try:
        result = subprocess.run(
            ["cloudflared", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Cloudflared is already installed:")
            print(f"   {result.stdout.strip()}\n")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Cloudflared is not installed\n")
    return False

def install_cloudflared():
    print("📥 Installing Cloudflared...\n")
    
    system = platform.system()
    
    if system == "Windows":
        print("Windows detected - Downloading cloudflared.exe...\n")
        
        import urllib.request
        
        # Download based on architecture
        is_64bit = sys.maxsize > 2**32
        url = (
            "https://github.com/cloudflare/cloudflared/releases/latest/"
            "download/cloudflared-windows-amd64.exe"
            if is_64bit else
            "https://github.com/cloudflare/cloudflared/releases/latest/"
            "download/cloudflared-windows-386.exe"
        )
        
        try:
            print("Downloading from: " + url)
            urllib.request.urlretrieve(url, "cloudflared.exe")
            
            # Try to move to System32
            system32 = os.path.join(os.environ["WINDIR"], "System32")
            print(f"Moving cloudflared.exe to {system32}...")
            
            subprocess.run([
                "powershell", "-Command",
                f"Move-Item -Path cloudflared.exe -Destination '{system32}' -Force"
            ], check=True)
            
            print("✅ Cloudflared installed to System32\n")
            return True
        except Exception as e:
            print(f"❌ Failed to install Cloudflared: {e}\n")
            print("Manual installation:")
            print("1. Download from: https://github.com/cloudflare/cloudflared/releases")
            print("2. Extract to: C:\\Windows\\System32\\")
            return False
    
    elif system == "Darwin":  # macOS
        print("macOS detected - Using Homebrew...\n")
        
        try:
            subprocess.run(
                ["brew", "install", "cloudflare/cloudflare/cloudflared"],
                check=True
            )
            print("✅ Cloudflared installed via Homebrew\n")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Cloudflared\n")
            return False
    
    elif system == "Linux":
        print("Linux detected - Installing cloudflared...\n")
        
        try:
            subprocess.run([
                "sh", "-c",
                "curl -L https://github.com/cloudflare/cloudflared/releases/latest/"
                "download/cloudflared-linux-amd64.tgz | tar xz"
            ], check=True)
            
            subprocess.run(["sudo", "cp", "./cloudflared", "/usr/bin/"], check=True)
            subprocess.run(["sudo", "chmod", "+x", "/usr/bin/cloudflared"], check=True)
            
            print("✅ Cloudflared installed to /usr/bin/\n")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Cloudflared\n")
            return False
    
    return False

def print_next_steps():
    print("="*60)
    print("✅ Setup Complete!")
    print("="*60 + "\n")
    
    print("📖 NEXT STEPS:\n")
    
    print("Option 1 - Run with Cloudflare Tunnel (Internet Access):")
    print("  python main.py\n")
    
    print("Option 2 - Run Local Server Only (LAN Access):")
    print("  python other-scripts/server.py\n")
    
    print("🌐 For more information, see README.md\n")

def main():
    print_banner()
    check_python()
    
    # Install Python packages
    if not install_requirements():
        sys.exit(1)
    
    # Check and install Cloudflared
    if not check_cloudflared():
        if not install_cloudflared():
            print("⚠️  Please install Cloudflared manually from:")
            print("   https://github.com/cloudflare/cloudflared/releases\n")
    
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)
