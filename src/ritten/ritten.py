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
)


class Ritten:
    """
    A client for interacting with the Ritten API.

    Features:
    - Connection pooling with configurable limits to optimize performance and resource usage.
    - Timeout to prevent hanging requests.
    """

    @exception_handler
    def __init__(self, config: Config):
        """Initialize the RittenClient with authentication and connection settings."""
        self.config = config

        try:
            # Configure limits explicitly based on user inputs
            limits = httpx.Limits(
                max_connections=config.max_connections,
                max_keepalive_connections=config.max_keepalive_connections,
                keepalive_expiry=config.keepalive_expiry,
            )

            self.client = httpx.Client(
                base_url=config.base_url,
                headers=self._get_default_headers(),
                auth=self.auth,
                limits=limits,
                timeout=config.timeout,
                event_hooks={"response": [self._raise_on_error_hook]},
            )
        except Exception as e:
            raise RittenClientError(
                f"Failed to initialize HTTP client: {str(e)}"
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

    @exception_handler
    def close(self):
        """Close the HTTP client and release resources."""
        self.client.close()

    @cached_property
    def auth(self):
        """Access the Auth service."""
        return Auth(self.config)

    # --- Resource Accessors ---

    @cached_property
    def calendar(self):
        """Access the Calendar resource."""
        return Calendar(self.client)

    @cached_property
    def cases(self):
        """Access the Cases resource."""
        return Cases(self.client)
