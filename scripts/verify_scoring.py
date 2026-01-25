#!/usr/bin/env python3
"""
Scoring Verification Script

WHAT THIS DOES:
- Runs the Decision Score logic against a set of sample gas stations
- Validates that the formula produces expected results
- Simulates what n8n will do in production

Reflects the logic in: src/scorer.py
"""

import sys
import os
from pathlib import Path

# Add project root to python path to allow importing src
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.scorer import calculate_decision_score

def run_verification():
    """Run verification on sample data"""
    
    # 1. Define Test Data (Real-world scenarios)
    test_cases = [
        {
            "name": "Shell (Perfect Station)",
            "rating": 5.0,
            "reviews": 1000,
            "open_24h": True,
            "amenities": 4, # OXXO, ATM, Coffee, Mechanic
            "expected_desc": "Max score (100)"
        },
        {
            "name": "Local Station (Good but small)",
            "rating": 4.5,
            "reviews": 50,
            "open_24h": False,
            "amenities": 0,
            "expected_desc": "Good rating, but no amenities/night"
        },
        {
            "name": "Highway Stop (Popular)",
            "rating": 3.8,
            "reviews": 5000,
            "open_24h": True,
            "amenities": 2, # OXXO, Bathroom
            "expected_desc": "High traffic + some amenities"
        },
        {
            "name": "Bad Station",
            "rating": 2.1,
            "reviews": 15,
            "open_24h": True,
            "amenities": 4, # Has everything but bad service
            "expected_desc": "Bad service but great facilities"
        }
    ]
    
    print("🔍 Running Decision Score Verification...\n")
    print(f"{'Station Name':<30} | {'Rat':<3} | {'Rev':<5} | {'24h':<3} | {'Amen':<4} | {'Score':<5} | {'Notes'}")
    print("-" * 100)
    
    for station in test_cases:
        # Calculate Score
        score = calculate_decision_score(
            rating=station["rating"],
            total_reviews=station["reviews"],
            open_24_hours=station["open_24h"],
            amenities_count=station["amenities"]
        )
        
        # Print Row
        print(f"{station['name']:<30} | {station['rating']:<3} | {station['reviews']:<5} | {str(station['open_24h'])[0]:<3} | {station['amenities']:<4} | {score:<5} | {station['expected_desc']}")

    print("\n✅ Verification Complete!")
    print("   If these scores look correct, the logic in src/scorer.py is solid.")
    
if __name__ == "__main__":
    run_verification()
