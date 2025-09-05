import requests
import logging
from typing import Optional, Dict
from config import CLEARBIT_API_KEY, CLEARBIT_ENDPOINT


class CompanyAPI:
    """Fetch additional company information using Clearbit (optional)."""

    def __init__(self, api_key: str = CLEARBIT_API_KEY):
        self.api_key = api_key

    def enrich(self, company_name: str) -> Optional[Dict]:
        """Return company enrichment dict or None if unavailable."""
        if not company_name:
            return None
        if not self.api_key:
            logging.debug("No API key configured for enrichment; skipping.")
            return None

        url = CLEARBIT_ENDPOINT.format(name=company_name)
        try:
            logging.debug("Calling enrichment API for: %s", company_name)
            resp = requests.get(url, auth=(self.api_key, ""), timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "domain": data.get("domain"),
                    "logo": data.get("logo"),
                    "description": data.get("description"),
                    "linkedin": data.get("linkedin", {}).get("handle"),
                }
            logging.warning("Enrichment API returned status %s for %s", resp.status_code, company_name)
        except Exception:
            logging.exception("Error calling enrichment API.")
        return None
