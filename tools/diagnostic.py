"""
N8N Workflow Diagnostic Tool
Checks connectivity and credentials for the Google Maps Scraper workflow
"""

import os
import sys
import json
import socket
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Tuple


def load_env():
    """Load environment variables from .env file"""
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
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class WorkflowDiagnostic:
    """Diagnostic tool for n8n workflow"""
    
    def __init__(self):
        self.n8n_url = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
        self.apify_key = os.getenv('APIFY_API_KEY')
        self.google_sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.results = []
        
    def print_header(self, text: str):
        """Print section header"""
        print(f"\n{'='*60}")
        print(f"{text}")
        print(f"{'='*60}\n")
    
    def check_status(self, name: str, status: bool, details: str = "") -> bool:
        """Print and record check status"""
        symbol = f"{Colors.GREEN}[PASS]{Colors.NC}" if status else f"{Colors.RED}[FAIL]{Colors.NC}"
        print(f"{symbol} {name}")
        if details:
            print(f"      {details}")
        self.results.append((name, status, details))
        return status
    
    def check_n8n_status(self) -> bool:
        """Check if n8n is running"""
        try:
            req = urllib.request.Request(f"{self.n8n_url}/healthz")
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                return self.check_status(
                    "n8n Server Status",
                    data.get('status') == 'ok',
                    f"Running at {self.n8n_url}"
                )
        except Exception as e:
            return self.check_status("n8n Server Status", False, f"Error: {str(e)}")
    
    def check_apify_connectivity(self) -> bool:
        """Check Apify API connectivity"""
        # Test DNS resolution first
        try:
            socket.gethostbyname('api.apify.com')
        except socket.gaierror:
            return self.check_status(
                "Apify DNS Resolution",
                False,
                "Cannot resolve api.apify.com - Check network/DNS settings"
            )
        
        # Test API endpoint
        try:
            req = urllib.request.Request(
                'https://api.apify.com/v2/acts',
                headers={'Authorization': f'Bearer {self.apify_key}'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    return self.check_status(
                        "Apify API Connectivity",
                        True,
                        "API responding correctly"
                    )
        except urllib.error.HTTPError as e:
            if e.code == 401:
                return self.check_status(
                    "Apify API Connectivity",
                    False,
                    "Invalid API key"
                )
            return self.check_status(
                "Apify API Connectivity",
                False,
                f"HTTP {e.code}"
            )
        except Exception as e:
            return self.check_status(
                "Apify API Connectivity",
                False,
                f"Connection error: {str(e)}"
            )
    
    def check_credentials(self) -> bool:
        """Check if required credentials are set"""
        checks = [
            ("APIFY_API_KEY", self.apify_key),
            ("GOOGLE_SHEET_ID", self.google_sheet_id),
        ]
        
        all_ok = True
        for name, value in checks:
            status = bool(value and value.strip())
            self.check_status(
                f"Environment Variable: {name}",
                status,
                "Set" if status else "Missing or empty"
            )
            all_ok = all_ok and status
        
        return all_ok
    
    def check_google_sheets_url(self) -> bool:
        """Verify Google Sheets URL is accessible"""
        if not self.google_sheet_id:
            return self.check_status(
                "Google Sheets URL",
                False,
                "Sheet ID not configured"
            )
        
        url = f"https://docs.google.com/spreadsheets/d/{self.google_sheet_id}"
        return self.check_status(
            "Google Sheets URL",
            True,
            url
        )
    
    def run_diagnostics(self) -> bool:
        """Run all diagnostic checks"""
        self.print_header("N8N Workflow Diagnostic Report")
        
        print("Checking system status...\n")
        
        # Run all checks
        n8n_ok = self.check_n8n_status()
        creds_ok = self.check_credentials()
        apify_ok = self.check_apify_connectivity()
        sheets_ok = self.check_google_sheets_url()
        
        # Summary
        self.print_header("Summary")
        
        total = len(self.results)
        passed = sum(1 for _, status, _ in self.results if status)
        failed = total - passed
        
        print(f"Total Checks: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.NC}")
        print(f"{Colors.RED}Failed: {failed}{Colors.NC}")
        
        if failed > 0:
            print(f"\n{Colors.YELLOW}Action Required:{Colors.NC}")
            print("Review failed checks above and fix configuration issues.")
            return False
        else:
            print(f"\n{Colors.GREEN}All checks passed. Workflow should be operational.{Colors.NC}")
            return True
    
    def get_recommendations(self) -> list:
        """Get recommendations based on failed checks"""
        recommendations = []
        
        for name, status, details in self.results:
            if not status:
                if "DNS" in name:
                    recommendations.append(
                        "DNS Resolution Failed: Check your network connection and DNS settings. "
                        "Try: sudo systemctl restart systemd-resolved"
                    )
                elif "APIFY_API_KEY" in name:
                    recommendations.append(
                        "Apify API Key Missing: Get your key from https://console.apify.com/account/integrations"
                    )
                elif "API key" in details:
                    recommendations.append(
                        "Invalid Apify API Key: Verify your key in .env file"
                    )
                elif "n8n" in name:
                    recommendations.append(
                        "n8n Not Running: Start with 'n8n start' or check Docker container"
                    )
        
        return recommendations

def main():
    """Main entry point"""
    diagnostic = WorkflowDiagnostic()
    success = diagnostic.run_diagnostics()
    
    if not success:
        recommendations = diagnostic.get_recommendations()
        if recommendations:
            print(f"\n{Colors.YELLOW}Recommendations:{Colors.NC}")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
