#!/usr/bin/env python3
"""
OAuth2 Credential Fix Tool
Opens n8n credentials page for re-authentication
"""

import os
import sys
import webbrowser
import urllib.request
import json
from pathlib import Path

def load_env():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'

def check_n8n_running(url: str) -> bool:
    """Check if n8n is running"""
    try:
        req = urllib.request.Request(f"{url}/healthz")
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except:
        return False

def main():
    """Main entry point"""
    n8n_url = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
    
    print("OAuth2 Credential Fix Tool")
    print("="*60)
    print()
    
    # Check n8n status
    print("Checking n8n status...")
    if not check_n8n_running(n8n_url):
        print(f"{Colors.RED}[ERROR]{Colors.NC} n8n is not running at {n8n_url}")
        print()
        print("Start n8n first:")
        print("  npm: n8n start")
        print("  docker: docker start n8n")
        sys.exit(1)
    
    print(f"{Colors.GREEN}[OK]{Colors.NC} n8n is running")
    print()
    
    # Open credentials page
    credentials_url = f"{n8n_url}/credentials"
    print(f"Opening credentials page: {credentials_url}")
    
    try:
        webbrowser.open(credentials_url)
        print(f"{Colors.GREEN}[OK]{Colors.NC} Browser opened")
    except:
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} Could not open browser automatically")
        print(f"Please open manually: {credentials_url}")
    
    print()
    print("Next Steps:")
    print("="*60)
    print("1. Find credential: 'Google Sheets account'")
    print("2. Click 'Connect my account' or 'Reconnect'")
    print("3. Authorize access in Google popup")
    print("4. Select account: daniel.sh.be@gmail.com")
    print("5. Click 'Save'")
    print()

if __name__ == "__main__":
    main()
