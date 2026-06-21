"""
Ritten SDK Forms Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Forms(Resource):
    """
    Handles all interactions with the Ritten API `/forms/definitions` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/forms/definitions"

    def list(
        self, show_archived: bool, is_tx_plan: bool, field_definition_ids: list[str]
    ) -> Dict[str, Any]:
        """List all form definitions configured for the clinic, including section definitions and signature requirements."""
        params = {
            "showArchived": show_archived,
            "isTxPlan": is_tx_plan,
            "fieldDefinitionIds": field_definition_ids,
        }
        return self._client.get(f"{self._base_path}", params=params).json()
