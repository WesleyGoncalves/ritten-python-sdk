"""
Ritten SDK Client.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

from calendar import Calendar
from functools import cached_property

import httpx
from ritten.auth import Auth
from ritten.config import Config
from ritten.decorators import exception_handler
from ritten.exceptions import RittenClientError, RittenAPIError, ERROR_MAP
from ritten.resources import (
    Calendar,
    Cases,
    Contacts,
    Facilities,
    Forms,
    Insurance,
    Organizations,
    Patients,
    Programs,
    Users,
)
from ritten.storage import TokenStorage


class Ritten:
    """A client for interacting with the Ritten API."""

    @exception_handler
    def __init__(
        self,
        tenant_id: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        storage: TokenStorage | None = None,
        *,
        config: Config | None = None,
    ):
        """Initialize the RittenClient with authentication and connection settings."""

        self.config: Config
        if config:
            self.config = config
        elif tenant_id and client_id and client_secret:
            self.config = Config(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret,
                storage=storage,
            )
        else:
            raise RittenClientError(
                "Either a Config object or tenant_id, client_id, and client_secret must be provided."
            )

        self.auth = Auth(self.config)

        try:
            self._build_http_client()
        except Exception as e:
            raise RittenClientError(
                f"Failed to initialize HTTP client: {str(e)}."
            ) from e

    def _get_default_headers(self) -> dict:
        """Generate default headers for API requests, including authentication."""

        return {
            "Content-Type": "application/json",
            "X-Ritten-Tenant": self.config.tenant_id,
        }

    def _raise_on_error_hook(self, response: httpx.Response):
        """Hook to raise exceptions on HTTP error responses."""

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code

            # Yield to the Auth class for expiration retries
            if status_code == 401:
                return

            response.read()
            error_message = f"Ritten API Error [{status_code}]: {e.response.text}"

            # Raise specific exception or default to base
            ExceptionClass = ERROR_MAP.get(status_code, RittenAPIError)
            raise ExceptionClass(error_message, status_code) from e

    def _build_http_client(self) -> None:
        """Build an HTTP client with the specified configuration."""

        # Configure limits explicitly based on user inputs
        limits = httpx.Limits(
            max_connections=self.config.max_connections,
            max_keepalive_connections=self.config.max_keepalive_connections,
            keepalive_expiry=self.config.keepalive_expiry,
        )

        self.client = httpx.Client(
            base_url=self.config.base_url,
            headers=self._get_default_headers(),
            auth=self.auth,
            limits=limits,
            timeout=self.config.timeout,
            event_hooks={"response": [self._raise_on_error_hook]},
        )

    @exception_handler
    def close(self):
        """Close the HTTP client and release resources."""
        self.client.close()

    # --- Resource Accessors ---

    @cached_property
    def calendar(self):
        """Access the Calendar resource."""
        return Calendar(self.client)

    @cached_property
    def cases(self):
        """Access the Cases resource."""
        return Cases(self.client)

    @cached_property
    def contacts(self):
        """Access the Contacts resource."""
        return Contacts(self.client)

    @cached_property
    def forms(self):
        """Access the Forms resource."""
        return Forms(self.client)

    @cached_property
    def facilities(self):
        """Access the Facilities resource."""
        return Facilities(self.client)

    @cached_property
    def insurance(self):
        """Access the Insurance resource."""
        return Insurance(self.client)

    @cached_property
    def organizations(self):
        """Access the Organizations resource."""
        return Organizations(self.client)

    @cached_property
    def patients(self):
        """Access the Patients resource."""
        return Patients(self.client)

    @cached_property
    def programs(self):
        """Access the Programs resource."""
        return Programs(self.client)

    @cached_property
    def users(self):
        """Access the Users resource."""
        return Users(self.client)
