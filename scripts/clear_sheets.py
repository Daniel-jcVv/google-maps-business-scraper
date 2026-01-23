#!/usr/bin/env python3
"""
Clear Google Sheets Bad Data
Clears the problematic rows from Google Sheets Data tab
"""

import sys

def main():
    print("=" * 60)
    print("MANUAL CLEANUP REQUIRED")
    print("=" * 60)
    print()
    print("The Google Sheets 'Data' tab contains incorrect data.")
    print()
    print("Steps to fix:")
    print("1. Open Google Sheets:")
    print("   https://docs.google.com/spreadsheets/d/1PWbrLBshcW_lb0L04C4vnlMStwU6t5X6DNRgY5OTgCo/edit")
    print()
    print("2. Go to the 'Data' tab")
    print()
    print("3. Delete ALL rows with data (keep the header row)")
    print("   - Select row 2 to the last row with data")
    print("   - Right-click → Delete rows")
    print()
    print("4. Go back to n8n and execute the workflow again")
    print()
    print("5. Check that new data appears correctly")
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()

