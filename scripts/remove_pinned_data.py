#!/usr/bin/env python3
"""
Remove Pinned Data from Workflow
Removes test data that's preventing the workflow from executing correctly
"""

import json
import sys
from pathlib import Path

def remove_pinned_data():
    """Remove pinned data from workflow"""
    
    workflow_path = Path(__file__).parent.parent / 'workflows' / 'gas_station_analyzer.json'
    
    if not workflow_path.exists():
        print(f"Error: Workflow file not found at {workflow_path}")
        return False
    
    print(f"Loading workflow from: {workflow_path}")
    
    # Load workflow
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    # Check if pinData exists
    if 'pinData' not in workflow:
        print("No pinned data found in workflow")
        return True
    
    print(f"\nFound pinned data for {len(workflow['pinData'])} nodes:")
    for node_name in workflow['pinData'].keys():
        print(f"  - {node_name}")
    
    # Create backup
    backup_path = workflow_path.with_suffix('.json.backup2')
    print(f"\nCreating backup at: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)
    
    # Remove pinData
    del workflow['pinData']
    
    # Save fixed workflow
    print(f"Saving workflow without pinned data to: {workflow_path}")
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)
    
    print("\n✅ Pinned data removed successfully!")
    print("\nWhat this fixes:")
    print("- Workflow will now use LIVE data from Apify")
    print("- Code node will process actual scraped results")
    print("- Google Sheets will receive correct transformed data")
    print("\nNext steps:")
    print("1. Reload the workflow in n8n (F5)")
    print("2. Clear old data from Google Sheets 'Data' tab")
    print("3. Execute the workflow")
    print("4. Verify correct data in Google Sheets")
    
    return True

if __name__ == '__main__':
    try:
        success = remove_pinned_data()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
