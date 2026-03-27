"""Scrape details for all stations in the XLSX by placeId via Apify."""

import json
import os
import sys
import time

import openpyxl
import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_API_KEY = os.getenv("APIFY_API_KEY")
ACTOR_ID = "compass~crawler-google-places"
BASE_URL = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
XLSX_PATH = "sheets/Google Maps Scraper - local.xlsx"
OUTPUT_PATH = "sheets/apify_full_details.json"


def get_unique_place_ids() -> list[str]:
    """Extract unique placeIds from the Data sheet."""
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True)
    ws = wb["Data"]
    ids = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:
            ids.add(str(row[0]))
    wb.close()
    return list(ids)


def scrape_by_place_ids(place_ids: list[str]) -> None:
    """Send all placeIds to Apify in one run and save results."""

    # Build startUrls from placeIds
    start_urls = [
        {"url": f"https://www.google.com/maps/place/?q=place_id:{pid}"}
        for pid in place_ids
    ]

    body = {
        "startUrls": start_urls,
        "maxCrawledPlacesPerSearch": len(place_ids),
    }

    # 1. Start scraping job
    print(f"Sending {len(place_ids)} placeIds to Apify...")
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
        if state in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"Error: scrape termino con status {state}")
            return
        time.sleep(10)

    # 3. Download results
    dataset_id = status["data"]["defaultDatasetId"]
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    items = requests.get(
        items_url, params={"token": APIFY_API_KEY}
    ).json()

    # 4. Save raw JSON
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"\nGuardado {len(items)} estaciones en {OUTPUT_PATH}")
    print("Ahora corre: python3 scripts/populate_details.py sheets/apify_full_details.json")


if __name__ == "__main__":
    place_ids = get_unique_place_ids()
    print(f"Found {len(place_ids)} unique placeIds in XLSX")
    scrape_by_place_ids(place_ids)
