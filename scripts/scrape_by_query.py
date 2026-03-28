import argparse
import json
import os
import time 

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_API_KEY = os.getenv("APIFY_API_KEY")
ACTOR_ID = "compass~crawler-google-places"
BASE_URL = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"


def scrape_by_query(query: str, max_results: int = 50) -> None:
    """Scrape Google Maps by search query via Apify."""

    body = {
        "searchStringsArray": [query], # busca esto en Google Maps
        "maxCrawledPlacesPerSearch": max_results,
    }

    # 1. Start scraping job
    print(f"Searching: '{query}' ({max_results} results)")
    resp = requests.post(
        BASE_URL,
        params={"token": APIFY_API_KEY},
        json=body,
        headers={"Content-Type": "application/json"},
    )
    resp.raise_for_status()
    run_id = resp.json()["data"]["id"]
    print(f"Run ID: {run_id}")

    # 2. Poll until complete
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
    while True:
        status = requests.get(
            status_url, params={"token": APIFY_API_KEY}
            ).json()
        state = status["data"]["status"]
        print(f"  Status: {state}")
        if state == "SUCCEEDED":
            break
        if state in ["FAILED", "ABORTED", "TIMED-OUT"]:
            print(f"Error: scrape ended with status {state}")
            return
        time.sleep(10)

    # 3. Download results
    dataset_id = status["data"]["defaultDatasetId"]
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    items = requests.get(
        items_url, params={"token": APIFY_API_KEY}
        ).json() # datos crudos en JSON nombre, direccion, raiting, etc

    output_path = "sheets/apify_restaurants.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False) # para acentos y otros caracteres se guarden bien (datos en espanol)

    print(f"\nSaved {len(items)} results to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Google Maps by query")
    parser.add_argument("query", help="Search query, e.g. 'restaurants in Querétaro Mexico'")
    parser.add_argument(
        "--max",
        type=int,
        default=50,
        help="Max results (default: 50)")
        
    args = parser.parse_args()

    scrape_by_query(args.query, args.max)


