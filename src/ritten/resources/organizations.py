"""
Ritten SDK Organizations Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Organizations(Resource):
    """
    Handles all interactions with the Ritten API `/organizations` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/organizations"

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        sort_by: str | None = None,
        organization_type_ids: list[str] | None = None,
        assigned_user_ids: list[str] | None = None,
    ) -> Dict[str, Any]:
        """Lists active organizations."""
        params = {"limit": limit, "offset": offset}
        if search:
            params["search"] = search
        if sort_by:
            params["sortBy"] = sort_by
        if organization_type_ids:
            params["organizationTypeIds"] = str(organization_type_ids)
        if assigned_user_ids:
            params["assignedUserIds"] = str(assigned_user_ids)
        return self._client.get(self._base_path, params=params).json()

    def get(self, id: str) -> Dict[str, Any]:
        """Retrieves a single active organization by its ID."""
        return self._client.get(f"{self._base_path}/{id}").json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new organization."""
        return self._client.post(self._base_path, json=payload).json()

    def update(self, id: str, payload: Dict[str, Any]) -> None | Dict[str, Any]:
        """Updates an active organization by ID."""
        return self._client.patch(f"{self._base_path}/{id}", json=payload).json()

    def members(
        self,
        organization_id: str,
        limit: int = 20,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Lists members of an active organization."""
        params = {"limit": limit, "offset": offset}
        return self._client.get(
            f"{self._base_path}/{organization_id}/members", params=params
        ).json()
