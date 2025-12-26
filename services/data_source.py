import os
import requests
import dlt
from typing import Iterator

HUBSPOT_DEALS_URL = "https://api.hubapi.com/crm/v3/objects/deals"

@dlt.resource(
    name="hubspot_deals",
    write_disposition="replace"
)
def hubspot_deals_resource() -> Iterator[dict]:
    """
    Fetch deals from HubSpot and yield them for DLT
    """

    access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("HUBSPOT_ACCESS_TOKEN is not set")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "limit": 100
    }

    while True:
        response = requests.get(
            HUBSPOT_DEALS_URL,
            headers=headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        for deal in data.get("results", []):
            yield deal

        paging = data.get("paging")
        if not paging or "next" not in paging:
            break

        params["after"] = paging["next"]["after"]
