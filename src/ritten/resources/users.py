"""
Ritten SDK Users Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any, Optional

from ritten.resources.resource import Resource


class Users(Resource):
    """
    Handles all interactions with the Ritten API `/staff`, `/users`, and `/teams` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/users"

    def list(self) -> Dict[str, Any]:
        """Lists users in a clinic."""
        return self._client.get("staff").json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new user and triggers an invitation email."""
        return self._client.post(self._base_path, json=payload).json()

    def delete(self, id: str) -> None:
        """Deletes a user account."""
        self._client.delete(f"{self._base_path}/{id}")

    # --- Roles ---

    def assign_role(self, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Assigns a role to a user."""
        return self._client.post(
            f"{self._base_path}/{user_id}/roles", json=payload
        ).json()

    def remove_role(self, user_id: str, role_id: str) -> None:
        """Removes a role from a user."""
        self._client.delete(f"{self._base_path}/{user_id}/roles/{role_id}")

    # --- Clinic Teams ---

    def list_clinic_teams(self) -> Dict[str, Any]:
        """Lists all clinic teams and their users."""
        return self._client.get("teams").json()
