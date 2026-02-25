#!/usr/bin/env python3
"""
Edge Device Controller - Quick Start Script
Choose between local server or Cloudflare tunnel
"""

import subprocess
import sys
import os

def main():
    print("\n" + "="*60)
    print("  Edge Device Controller - Start Menu")
    print("="*60 + "\n")
    
    print("Choose an option:\n")
    print("1️⃣  Run with Cloudflare Tunnel (Internet Access)")
    print("     - Public access via HTTPS")
    print("     - WebSocket via WSS (Secure)")
    print("     - Perfect for remote access\n")
    
    print("2️⃣  Run Local Server Only (LAN Access)")
    print("     - Local network access only")
    print("     - WebSocket via WS (No encryption)")
    print("     - Lower latency\n")
    
    print("3️⃣  Exit\n")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting with Cloudflare Tunnel...\n")
        print("Make sure cloudflared is installed!")
        print("(Run setup.py if you haven't installed it yet)\n")
        
        try:
            subprocess.run([sys.executable, "main.py"], check=True)
        except KeyboardInterrupt:
            print("\n\n⛔ Server stopped\n")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error: {e}\n")
            return 1
    
    elif choice == "2":
        print("\n🚀 Starting Local Server...\n")
        
        try:
            subprocess.run(
                [sys.executable, "-m", "uvicorn", 
                 "other-scripts.server:app", "--host", "0.0.0.0", "--port", "8000"],
                check=True
            )
        except KeyboardInterrupt:
            print("\n\n⛔ Server stopped\n")
            return 0
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error: {e}\n")
            return 1
    
    elif choice == "3":
        print("Goodbye!\n")
        return 0
    
    else:
        print("❌ Invalid choice. Please try again.\n")
        return main()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⛔ Operation cancelled\n")
        sys.exit(0)
