#!/usr/bin/env python3
"""
Workflow Test Tool
Opens n8n workflow for testing
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

def main():
    """Main entry point"""
    n8n_url = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    
    print("Workflow Test Tool")
    print("="*60)
    print()
    
    # Check n8n
    try:
        req = urllib.request.Request(f"{n8n_url}/healthz")
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status != 200:
                print(f"{Colors.RED}[ERROR]{Colors.NC} n8n is not responding")
                sys.exit(1)
        print(f"{Colors.GREEN}[OK]{Colors.NC} n8n is running")
    except:
        print(f"{Colors.RED}[ERROR]{Colors.NC} Cannot connect to n8n")
        sys.exit(1)
    
    print()
    print("Test Instructions:")
    print("="*60)
    print()
    print("1. Open n8n workflow:")
    print(f"   {n8n_url}")
    print()
    print("2. Click 'Execute Workflow' button (play icon)")
    print()
    print("3. Monitor these nodes:")
    print("   - Read Pending Queries")
    print("   - Start Apify Scraping Job")
    print("   - Wait for Job Succeed")
    print("   - Check Scraping Status")
    print("   - Fetch Scraped Results")
    print("   - Save Business Data (previously failing)")
    print()
    print("4. Verify data in Google Sheets:")
    if sheet_id:
        print(f"   https://docs.google.com/spreadsheets/d/{sheet_id}")
    print()
    print("5. Check 'Data' tab for new records")
    print()
    
    # Open browser
    try:
        webbrowser.open(n8n_url)
        print(f"{Colors.GREEN}[OK]{Colors.NC} Browser opened")
    except:
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} Could not open browser")
    
    print()

if __name__ == "__main__":
    main()
