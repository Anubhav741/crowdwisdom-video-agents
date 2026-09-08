import os
import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

ACTOR_ID = "igolaizola~facebook-ad-library-scraper"


def get_ads():
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs/last"

    response = requests.get(
        url,
        params={
            "token": APIFY_TOKEN
        }
    )

    response.raise_for_status()

    run = response.json()["data"]

    dataset_id = run["defaultDatasetId"]

    print("Dataset ID:", dataset_id)

    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"

    ads_response = requests.get(
        dataset_url,
        params={
            "token": APIFY_TOKEN,
            "format": "json"
        }
    )

    ads_response.raise_for_status()

    ads = ads_response.json()

    print("Ads received:", len(ads))

    return ads


if __name__ == "__main__":
    ads = get_ads()

    with open("ads_raw.json", "w") as f:
        import json
        json.dump(ads, f, indent=2)

    print("Saved → ads_raw.json")
