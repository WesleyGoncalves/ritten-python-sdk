"""
Ritten SDK Cases Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Cases(Resource):
    """
    Handles all interactions with the Ritten API `/cases` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/cases"

    def list(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Lists cases in a clinic."""
        params = {
            "limit": limit,
            "offset": offset,
        }
        return self._client.get(self._base_path, params=params).json()

    def get(self, id: str) -> Dict[str, Any]:
        """Retrieves a single case by its ID."""
        return self._client.get(f"{self._base_path}/{id}").json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new case."""
        return self._client.post(self._base_path, json=payload).json()

    def update(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing case by ID."""
        return self._client.patch(
            f"{self._base_path}/{id}",
            json=payload,
        ).json()

    def create_note(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a note for a specific case."""
        return self._client.post(
            f"{self._base_path}/{id}/notes",
            json=payload,
        ).json()
