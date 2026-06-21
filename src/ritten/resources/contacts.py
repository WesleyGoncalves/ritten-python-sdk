"""
Ritten SDK Contacts Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Contacts(Resource):
    """
    Handles all interactions with the Ritten API `/contacts` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/contacts"

    def list(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Lists contacts in a clinic."""
        params = {"limit": limit, "offset": offset}
        return self._client.get(self._base_path, params=params).json()

    def get(self, id: str) -> Dict[str, Any]:
        """Retrieves a single contact by their ID."""
        return self._client.get(f"{self._base_path}/{id}").json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new contact."""
        return self._client.post(self._base_path, json=payload).json()

    def update(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing contact by ID."""
        return self._client.patch(
            f"{self._base_path}/{id}",
            json=payload,
        ).json()

    def list_relationships(self, id: str) -> Dict[str, Any]:
        """Lists a contact's relationships."""
        return self._client.get(f"{self._base_path}/{id}/relationships").json()

    def create_relationship(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new relationship for a contact."""
        return self._client.post(
            f"{self._base_path}/{id}/relationships",
            json=payload,
        ).json()
