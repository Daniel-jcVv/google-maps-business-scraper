import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

def deploy_workflow(file_path: str):
    """
    Deploy a local JSON workflow to n8n via API.
    """
    load_dotenv()
    
    token = os.getenv("N8N_API_TOKEN")
    if not token or token == "tu_token_aqui":
        print("❌ Error: N8N_API_TOKEN not set in .env")
        print("Obtén tu token en: n8n Settings > Personal Setup > API Keys")
        return

    # Load local file
    path = Path(file_path)
    if not path.exists():
        print(f"❌ Error: File {file_path} not found")
        return

    with open(path, 'r') as f:
        workflow_data = json.load(f)

    workflow_id = workflow_data.get('id')
    if not workflow_id:
        print("❌ Error: Workflow ID not found in JSON")
        return

    # n8n API URL
    base_url = os.getenv("N8N_URL", "http://localhost:5678").rstrip('/')
    url = f"{base_url}/api/v1/workflows/{workflow_id}"
    
    # Try different authentication schemes
    auth_methods = [
        {"X-N8N-API-KEY": token},
        {"Authorization": f"Bearer {token}"}
    ]

    print(f"🚀 Deploying workflow '{workflow_data.get('name')}' (ID: {workflow_id}) to {url}...")

    payload = {
        "name": workflow_data.get('name'),
        "nodes": workflow_data.get('nodes'),
        "connections": workflow_data.get('connections'),
        "settings": workflow_data.get('settings', {}),
        "staticData": workflow_data.get('staticData')
    }

    last_error = ""
    for headers in auth_methods:
        try:
            headers["Content-Type"] = "application/json"
            response = requests.put(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Deploy Successful using {list(headers.keys())[0]}!")
                return
            last_error = f"{response.status_code}: {response.text}"
        except Exception as e:
            last_error = str(e)

    print(f"❌ Error during deploy: {last_error}")
    print("\n💡 Sugerencia Proactiva:")
    print("1. El token actual parece ser un JWT o está expirado.")
    print("2. Ve a n8n > Settings > Personal Setup > API Keys.")
    print("3. Crea una 'Personal API Key' (debe empezar con 'n8n_api_').")
    print("4. Actualiza N8N_API_TOKEN en tu .env con esa nueva llave.")

if __name__ == "__main__":
    target_file = "workflows/gas_station_analyzer.json"
    deploy_workflow(target_file)
