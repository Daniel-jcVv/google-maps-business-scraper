"""Test script: scrape 3 gas stations with full details from Apify."""

import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_API_KEY = os.getenv("APIFY_API_KEY")
ACTOR_ID = "compass~crawler-google-places"
BASE_URL = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"


def run_test_scrape():
    """Scrape 3 stations and save raw JSON to inspect available fields."""

    # TODO: Daniel escribe el body del POST aqui
    # Necesitas 3 campos:
    #   - searchStringsArray: lista con "gas stations"
    #   - locationQuery: string con la ciudad
    #   - maxCrawledPlacesPerSearch: numero (3 para el test)
    body = {
        "searchStringsArray": ["gas stations"],
        "locationQuery": "Queretaro Queretaro",
        "maxCrawledPlacesPerSearch": 3,
    }

    # --- De aqui para abajo no toques todavia ---

    # 1. Start the scraping job
    print("Iniciando scrape de prueba (3 estaciones)...")
    resp = requests.post(
        BASE_URL,
        params={"token": APIFY_API_KEY},
        json=body,
        headers={"Content-Type": "application/json"},
    )
    resp.raise_for_status()
    run_data = resp.json()["data"]
    run_id = run_data["id"]
    print(f"Run ID: {run_id}")

    # 2. Poll until complete
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    while True:
        status = requests.get(status_url, params={"token": APIFY_API_KEY}).json()
        state = status["data"]["status"]
        print(f"  Status: {state}")
        if state == "SUCCEEDED":
            break
        if state in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"Error: scrape termino con status {state}")
            return
        time.sleep(5)

    # 3. Download results
    dataset_id = status["data"]["defaultDatasetId"]
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    items = requests.get(items_url, params={"token": APIFY_API_KEY}).json()

    # 4. Save raw JSON
    output_path = "sheets/apify_sample.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"\nGuardado {len(items)} estaciones en {output_path}")
    print("Revisa el archivo para ver que campos de amenities trae Apify.")


if __name__ == "__main__":
    run_test_scrape()
