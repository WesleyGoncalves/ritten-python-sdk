"""
Ritten SDK Programs Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Programs(Resource):
    """
    Handles all interactions with the Ritten API `/programs` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/programs"

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        programType: str | None = None,
        facility_id: str | None = None,
    ) -> Dict[str, Any]:
        """Lists active programs configured in the clinic."""
        params = {"limit": limit, "offset": offset}
        if search is not None:
            params["search"] = search
        if programType is not None:
            params["programType"] = programType
        if facility_id is not None:
            params["facility_id"] = facility_id
        return self._client.get(self._base_path, params=params).json()

    def get(self, id: str) -> Dict[str, Any]:
        """Retrieves an active program by its ID."""
        return self._client.get(f"{self._base_path}/{id}").json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new program."""
        return self._client.post(self._base_path, json=payload).json()

    def update(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an active program's configurations by ID."""
        return self._client.patch(f"{self._base_path}/{id}", json=payload).json()
