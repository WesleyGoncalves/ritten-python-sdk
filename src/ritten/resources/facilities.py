"""
Ritten SDK Facilities Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any
from datetime import datetime

from ritten.resources.resource import Resource
from ritten.utils import to_iso_format


class Facilities(Resource):
    """
    Handles all interactions with the Ritten API `/facilities` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/facilities"

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        created_after: datetime | None = None,
    ) -> Dict[str, Any]:
        """Lists active clinic facilities.

        Arguments:
            limit: Number of facilities to return (default: 20).
            offset: Number of facilities to skip for pagination (default: 0).
            search: Optional case-insensitive search to filter facilities by name.
            created_after: Optional datetime to filter facilities created after this date.
        """
        params = {"limit": limit, "offset": offset}
        if search:
            params["search"] = search
        if created_after:
            params["createdAfter"] = to_iso_format(created_after)
        return self._client.get(self._base_path, params=params).json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new facility."""
        return self._client.post(self._base_path, json=payload).json()

    def update(self, id: str, name: str) -> None | Dict[str, Any]:
        """Updates an existing facility by ID."""
        payload = {"name": name}
        return self._client.patch(f"{self._base_path}/{id}", json=payload).json()
