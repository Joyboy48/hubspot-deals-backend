import time
import requests
from typing import Dict, List, Optional


class HubSpotAPIService:
    """
    Service responsible for interacting with HubSpot CRM API.
    """

    def __init__(self, base_url: str, access_token: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

    def get_deals(
        self,
        limit: int = 100,
        properties: Optional[List[str]] = None,
        archived: bool = False
    ) -> List[Dict]:
        """
        Fetch all deals from HubSpot using cursor-based pagination.
        """
        all_deals = []
        after = None

        while True:
            params = {
                "limit": limit,
                "archived": archived
            }

            if after:
                params["after"] = after

            if properties:
                params["properties"] = ",".join(properties)

            response = self._make_request(
                method="GET",
                endpoint="/crm/v3/objects/deals",
                params=params
            )

            deals = response.get("results", [])
            all_deals.extend(deals)

            paging = response.get("paging")
            if not paging or "next" not in paging:
                break

            after = paging["next"]["after"]

        return all_deals

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        retries: int = 3
    ) -> Dict:
        """
        Internal helper to make API requests with retry and rate limit handling.
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(retries):
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()

            # Handle HubSpot rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2))
                time.sleep(retry_after)
                continue

            # Retry on server errors
            if response.status_code >= 500:
                time.sleep(2 ** attempt)
                continue

            # Other errors are fatal
            response.raise_for_status()

        raise Exception("Failed to fetch data from HubSpot API after retries")
