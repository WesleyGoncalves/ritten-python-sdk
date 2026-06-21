"""
Ritten SDK Insurance Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Insurance(Resource):
    """
    Handles all interactions with the Ritten API `/insurance/payers` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/insurance/payers"

    def list(self) -> Dict[str, Any]:
        """List all insurance payers."""
        return self._client.get(f"{self._base_path}").json()

    def get(self, id: str) -> Dict[str, Any]:
        """Retrieves a single insurance payer by their ID."""
        return self._client.get(f"{self._base_path}/{id}").json()
