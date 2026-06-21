"""
Ritten SDK Calendar Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Calendar(Resource):
    """
    Handles all interactions with the Ritten API `/calendar/events` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/calendar/events"

    def list(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Queries calendar events based on specific criteria.
        The POST body is the query object.
        """
        return self._client.post(f"{self._base_path}/list", json=payload).json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new calendar event."""
        return self._client.post(f"{self._base_path}", json=payload).json()
