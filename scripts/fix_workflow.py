#!/usr/bin/env python3
"""
Workflow Fixer Script
Fixes data mapping issues in the gas_station_analyzer workflow
"""

import json
import sys
from pathlib import Path

def fix_workflow():
    """Fix the workflow JSON file"""
    
    # Get the correct path (script is in scripts/, workflow is in workflows/)
    workflow_path = Path(__file__).parent.parent / 'workflows' / 'gas_station_analyzer.json'
    
    if not workflow_path.exists():
        print(f"Error: Workflow file not found at {workflow_path}")
        return False
    
    print(f"Loading workflow from: {workflow_path}")
    
    # Load workflow
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    # Find the "Save Business Data" node
    save_node = None
    for node in workflow.get('nodes', []):
        if node.get('name') == 'Save Business Data':
            save_node = node
            break
    
    if not save_node:
        print("Error: 'Save Business Data' node not found")
        return False
    
    print("Found 'Save Business Data' node")
    
    # Get current mappings
    columns = save_node.get('parameters', {}).get('columns', {})
    current_mappings = columns.get('value', {})
    
    print("\nCurrent mappings:")
    for key, value in current_mappings.items():
        print(f"  {key}: {value}")
    
    # Fix the mappings
    fixed_mappings = {
        "Station_ID": "={{ $json.Station_ID }}",
        "Station_Name": "={{ $json.Station_Name }}",  # Remove extra }
        "address": "={{ $json.Address }}",
        "Latitude": "={{ $json.Latitude }}",
        "Longitude": "={{ $json.Longitude }}",
        "Rating_Average": "={{ $json.Rating_Average }}",  # Add missing field
        "Total_Reviews": "={{ $json.Total_Reviews }}",
        "Open_24_Hours": "={{ $json.Open_24_Hours }}",
        "Google_Maps_URL": "={{ $json.Google_Maps_URL }}",
        "Decision_Score": "={{ $json.Decision_Score }}"
        # Remove searchString - it's not needed
    }
    
    # Update the node
    columns['value'] = fixed_mappings
    save_node['parameters']['columns'] = columns
    
    print("\nFixed mappings:")
    for key, value in fixed_mappings.items():
        print(f"  {key}: {value}")
    
    # Create backup
    backup_path = workflow_path.with_suffix('.json.backup')
    print(f"\nCreating backup at: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)
    
    # Save fixed workflow
    print(f"Saving fixed workflow to: {workflow_path}")
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)
    
    print("\n✅ Workflow fixed successfully!")
    print("\nChanges made:")
    print("1. Fixed Station_Name mapping (removed extra })")
    print("2. Added Rating_Average field")
    print("3. Removed searchString field (not needed)")
    print("\nNext steps:")
    print("1. Reload the workflow in n8n")
    print("2. Execute the workflow")
    print("3. Check Google Sheets for correct data")
    
    return True

if __name__ == '__main__':
    try:
        success = fix_workflow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
