"""
Ritten SDK Patients Resource.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from typing import Dict, Any

from ritten.resources.resource import Resource


class Patients(Resource):
    """
    Handles all interactions with the Ritten API `/patients` endpoints.
    """

    def __init__(self, client: httpx.Client):
        self._client = client
        self._base_path = "/patients"

    def list(
        self,
        program_status: str,
        limit: int = 20,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Lists patients in a clinic."""

        params = {
            "programStatus": program_status,
            "limit": limit,
            "offset": offset,
        }

        return self._client.get(self._base_path, params=params).json()

    def get(self, id: str) -> Dict[str, Any]:
        """Retrieves a single patient by their Ritten ID."""
        return self._client.get(f"{self._base_path}/{id}").json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new patient record."""
        return self._client.post(self._base_path, json=payload).json()

    def update(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a patient by ID."""
        return self._client.patch(
            f"{self._base_path}/{id}",
            json=payload,
        ).json()

    def get_by_external_id(self, external_id: str) -> Dict[str, Any]:
        """Retrieves a patient using an external system ID."""
        return self._client.get(f"{self._base_path}/external/{external_id}").json()

    # --- Clinical Data ---

    def record_vitals(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Records a single vital observation for the patient.
        Units are fixed by observation and measurement type; do not include units in the request body.
        """
        return self._client.post(
            f"{self._base_path}/{id}/vitals",
            json=payload,
        ).json()

    # --- Relationships ---

    def list_relationships(self, id: str) -> Dict[str, Any]:
        """Lists a patient's relationships."""
        return self._client.get(f"{self._base_path}/{id}/relationships").json()

    def create_relationship(self, id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new patient relationship."""
        return self._client.post(
            f"{self._base_path}/{id}/relationships",
            json=payload,
        ).json()

    def update_relationship(
        self, patient_id: str, relationship_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates a specific patient relationship."""
        return self._client.patch(
            f"{self._base_path}/{patient_id}/relationships/{relationship_id}",
            json=payload,
        ).json()

    def delete_relationship(self, patient_id: str, relationship_id: str) -> None:
        """Deletes a patient relationship."""
        self._client.delete(
            f"{self._base_path}/{patient_id}/relationships/{relationship_id}",
        )

    # --- Chart Documents ---

    def attach_document(
        self, patient_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Attaches a document to a patient chart."""
        return self._client.post(
            f"{self._base_path}/{patient_id}/attachments",
            json=payload,
        ).json()

    def update_document(
        self, patient_id: str, attachment_id: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Updates the title or type of a document on a patient chart. Omitting a field will leave it unchanged."""

        return self._client.patch(
            f"{self._base_path}/{patient_id}/attachments/{attachment_id}", json=payload
        ).json()
