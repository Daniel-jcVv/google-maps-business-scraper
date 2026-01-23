#!/usr/bin/env python3
"""
Add Amenities Nodes to Workflow
Completes the amenities enrichment functionality
"""

import json
import sys
from pathlib import Path

def add_amenities_nodes():
    """Add amenities search nodes to the workflow"""
    
    workflow_path = Path(__file__).parent.parent / 'workflows' / 'gas_station_analyzer.json'
    
    if not workflow_path.exists():
        print(f"Error: Workflow file not found at {workflow_path}")
        return False
    
    print(f"Loading workflow from: {workflow_path}")
    
    # Load workflow
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    # Find the Code in JavaScript node
    code_node_id = None
    for node in workflow.get('nodes', []):
        if node.get('name') == 'Code in JavaScript':
            code_node_id = node.get('id')
            break
    
    if not code_node_id:
        print("Error: 'Code in JavaScript' node not found")
        return False
    
    print(f"Found 'Code in JavaScript' node with ID: {code_node_id}")
    
    # Create new nodes
    new_nodes = [
        # Split In Batches node
        {
            "parameters": {
                "batchSize": 1,
                "options": {
                    "reset": True
                }
            },
            "id": "split-batches-amenities",
            "name": "Process Each Station",
            "type": "n8n-nodes-base.splitInBatches",
            "typeVersion": 3,
            "position": [-400, 608]
        },
        # HTTP Request for Google Places API
        {
            "parameters": {
                "method": "POST",
                "url": "https://places.googleapis.com/v1/places:searchNearby",
                "authentication": "genericCredentialType",
                "genericAuthType": "httpHeaderAuth",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "X-Goog-Api-Key",
                            "value": "={{ $env.GOOGLE_PLACES_API }}"
                        },
                        {
                            "name": "X-Goog-FieldMask",
                            "value": "places.displayName,places.types"
                        },
                        {
                            "name": "Content-Type",
                            "value": "application/json"
                        }
                    ]
                },
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={\n  \"locationRestriction\": {\n    \"circle\": {\n      \"center\": {\n        \"latitude\": {{ $json.Latitude }},\n        \"longitude\": {{ $json.Longitude }}\n      },\n      \"radius\": 300\n    }\n  },\n  \"includedTypes\": [\"convenience_store\", \"cafe\", \"atm\", \"car_repair\"],\n  \"maxResultCount\": 10\n}",
                "options": {}
            },
            "id": "http-places-api",
            "name": "Search Nearby Amenities",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [-200, 608]
        },
        # Code node to process amenities
        {
            "parameters": {
                "jsCode": "const station = $('Process Each Station').first().json;\nconst response = $input.first().json;\n\n// Extract amenities from Google Places API response\nconst places = response.places || [];\n\nlet nearbyOxxo = false;\nlet nearbyCoffee = false;\nlet nearbyMechanic = false;\nlet nearbyATM = false;\n\n// Analyze found places\nfor (const place of places) {\n  const types = place.types || [];\n  \n  if (types.includes('convenience_store')) nearbyOxxo = true;\n  if (types.includes('cafe')) nearbyCoffee = true;\n  if (types.includes('car_repair')) nearbyMechanic = true;\n  if (types.includes('atm')) nearbyATM = true;\n}\n\n// Calculate amenities score\nlet amenitiesScore = 0;\nif (nearbyOxxo) amenitiesScore += 5;\nif (nearbyCoffee) amenitiesScore += 5;\nif (nearbyMechanic) amenitiesScore += 5;\nif (nearbyATM) amenitiesScore += 5;\n\n// Recalculate Decision Score with amenities\nconst rating = station.Rating_Average || 0;\nconst reviews = station.Total_Reviews || 0;\nconst is24hrs = station.Open_24_Hours || false;\n\nconst ratingScore = (rating / 5) * 40;\nconst reviewScore = Math.min(Math.log(reviews + 1) * 10, 30);\nconst availabilityScore = is24hrs ? 10 : 0;\n\nconst decisionScore = Math.round((\n  ratingScore + \n  reviewScore + \n  availabilityScore + \n  amenitiesScore\n) * 10) / 10;\n\nreturn [{\n  json: {\n    ...station,\n    Nearby_OXXO: nearbyOxxo,\n    Nearby_Coffee: nearbyCoffee,\n    Nearby_Mechanic: nearbyMechanic,\n    Nearby_ATM: nearbyATM,\n    Amenities_Score: amenitiesScore,\n    Decision_Score: decisionScore\n  }\n}];"
            },
            "id": "code-calculate-amenities",
            "name": "Calculate Amenities Score",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [0, 608]
        }
    ]
    
    # Add new nodes to workflow
    workflow['nodes'].extend(new_nodes)
    
    # Update connections
    connections = workflow.get('connections', {})
    
    # Connect Code in JavaScript -> Process Each Station
    connections['Code in JavaScript'] = {
        "main": [[{
            "node": "Process Each Station",
            "type": "main",
            "index": 0
        }]]
    }
    
    # Connect Process Each Station -> Search Nearby Amenities
    connections['Process Each Station'] = {
        "main": [[{
            "node": "Search Nearby Amenities",
            "type": "main",
            "index": 0
        }]]
    }
    
    # Connect Search Nearby Amenities -> Calculate Amenities Score
    connections['Search Nearby Amenities'] = {
        "main": [[{
            "node": "Calculate Amenities Score",
            "type": "main",
            "index": 0
        }]]
    }
    
    # Connect Calculate Amenities Score -> Save Business Data
    connections['Calculate Amenities Score'] = {
        "main": [[{
            "node": "Save Business Data",
            "type": "main",
            "index": 0
        }]]
    }
    
    workflow['connections'] = connections
    
    # Update Save Business Data node to include new columns
    for node in workflow['nodes']:
        if node.get('name') == 'Save Business Data':
            columns = node['parameters']['columns']['value']
            # Add new amenities columns
            columns['Nearby_OXXO'] = '={{ $json.Nearby_OXXO }}'
            columns['Nearby_Coffee'] = '={{ $json.Nearby_Coffee }}'
            columns['Nearby_Mechanic'] = '={{ $json.Nearby_Mechanic }}'
            columns['Nearby_ATM'] = '={{ $json.Nearby_ATM }}'
            columns['Amenities_Score'] = '={{ $json.Amenities_Score }}'
            break
    
    # Create backup
    backup_path = workflow_path.with_suffix('.json.backup_amenities')
    print(f"\nCreating backup at: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)
    
    # Save updated workflow
    print(f"Saving updated workflow to: {workflow_path}")
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)
    
    print("\n✅ Amenities nodes added successfully!")
    print("\nNew nodes created:")
    print("1. Process Each Station (Split In Batches)")
    print("2. Search Nearby Amenities (HTTP Request to Google Places API)")
    print("3. Calculate Amenities Score (Code node)")
    print("\nNew data fields:")
    print("- Nearby_OXXO (Boolean)")
    print("- Nearby_Coffee (Boolean)")
    print("- Nearby_Mechanic (Boolean)")
    print("- Nearby_ATM (Boolean)")
    print("- Amenities_Score (0-20 points)")
    print("- Decision_Score (updated formula)")
    print("\nNext steps:")
    print("1. Reload the workflow in n8n (F5)")
    print("2. Execute the workflow to test")
    print("3. Check Google Sheets for new columns")
    
    return True

if __name__ == '__main__':
    try:
        success = add_amenities_nodes()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
