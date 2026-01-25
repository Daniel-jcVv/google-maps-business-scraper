"""
Sync n8n workflow to local file system
"""

from dotenv import load_dotenv
import os
import sys
import requests
import json
from pathlib import Path

def load_api_token() -> str:
    """
    Read n8n API token from .env file

    Returns:
        token as string
    
    Raises:
        ValueError: If token is not found
    """
    
    # Load environment variables from .env file
    load_dotenv()

    # Read API token from environment variable
    token = os.getenv("N8N_API_TOKEN")

    # Validate token exists
    if not token:
        raise ValueError("N8N_API_TOKEN not found in .env file")

    return token


# read workflow from n8n
def fetch_workflow(workflow_id: str, token: str) -> dict:
    """
    Download workflow from n8n API

    Args:
        workflow_id: ID of the workflow to download
        api_token: token to authenticate
    
    Returns:
        Workflow data as dictionary (JSON parsed)
    
    Raises:
        requests.HTTPError: if request fails
    """

    # build API URL
    base_url = "http://localhost:5678"
    url = f"{base_url}/api/v1/workflows/{workflow_id}"

    # set headers with token authentication
    headers = {
        "X-N8N-API-KEY": token
    }
    
    # make GET request
    print(f"Downloading workflow {workflow_id} from {url}")
    response = requests.get(url, headers=headers, timeout=10)

    # check for HTTP errors
    response.raise_for_status()

    # Parse JSON response and return as dict
    return response.json()


# save workflow to file 
def save_workflow(workflow_data: dict, output_path: Path) -> None:
    """
    Save workflow to JSON file

    Args:
        workflow_data: dict with data of workflow to save
        output_path: Path where to save workflow
    
    Returns:
        None (no return value, only save the file)
    """

    # 1 validate that directory exists
    # if workflows/ doesn't exist, create it
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 2 open file on write mode
    with open(output_path, 'w', encoding='utf-8') as f:
        
        # 3 convert dict to json and write
        json.dump(
            workflow_data, # data to write
            f, # where to write 
            indent=2, # pretty print
            ensure_ascii=False # to handle special characters
        )

    # 4 print the path where the workflow was saved
    print(f" Workflow saved to: {output_path}")
    print(f" Size: {output_path.stat().st_size:,} bytes")


# main execution block
if __name__ == "__main__":

    try:
        # 1 Load API token
        token = load_api_token()
        print(f"Token loaded: {token[:7]}") # print only 7 caracters 
        
        # 2 Download workflow
        print("Downloading workflow...")
        workflow_id = "f8h0TZ4lTu3YDzTX"
        workflow = fetch_workflow(workflow_id, token)
        print(f"Name: {workflow['name']}")
        print(f"Nodes: {len(workflow.get('nodes', []))}\n")
        print(f"ID {workflow.get('id')}\n")
        
        # 3 Save workflow to file
        print("Saving workflow...")
        output_path = Path("workflows/gas_station_analyzer.json")
        save_workflow(workflow, output_path)
        print(f"Workflow downloaded successfully: {workflow_id}")
        
        print("Workflow synced successfully!")
        print("1. Check changes: git diff workflows/gas_station_analyzer.json")
        print("2. Do commit: git add workflows/ && git commit -m 'sync: Update workflow")
        print("3. Push a remote: git push") 

    except ValueError as e:
        # Error configuration (.env without token)
        print(f"Setting Error: {e}")
        sys.exit(1)


    except requests.HTTPError as e:
        # Error HTTP (401, 404, 500, etc) 
        if e.response.status_code == 401:
            print("token invalid or expired. Create a new token in n8n settings")
        elif e.response.status_code == 404:
            print("workflow not found. Check the workflow ID")
        else:
            print(f"HTTP Error: {e}")
        sys.exit(1)
        

    except Exception as e:
        # any other error (network, file system, etc)
        import traceback
        traceback.print_exc()
        sys.exit(1)
      


