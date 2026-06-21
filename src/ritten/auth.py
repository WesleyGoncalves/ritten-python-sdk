"""
Ritten SDK Authentication Handler.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import httpx
from ritten.config import Config
from ritten.exceptions import RittenAuthError, RittenUnauthorizedError


class Auth(httpx.Auth):
    """Authentication handler for the Ritten API."""

    def __init__(self, config: Config):
        self.config = config

    @property
    def access_token(self) -> str | None:
        """Fetch the access token."""
        token = self.config.storage.get_token()
        return token

    @access_token.setter
    def access_token(self, value: str) -> Auth:
        """Set a new access token."""
        self.config.storage.set_token(value)

        return self

    @property
    def client_id(self) -> str | None:
        """Fetch the client ID for authentication."""
        return self.config.client_id

    @property
    def client_secret(self) -> str | None:
        """Fetch the client secret for authentication."""
        return self.config.client_secret

    def _fetch_new_token(self) -> None:
        """Fetch a new access token using client credentials."""
        if not self.config.client_id or not self.config.client_secret:
            raise RittenAuthError(
                "Client ID and Client Secret are required to fetch a new access token."
            )

        response = httpx.post(
            f"{self.config.base_url}/oauth/token",
            json={
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "audience": self.config.audience,
            },
        )

        if response.status_code == 200:
            self.access_token = response.json()["access_token"]

    def add_bearer_token(self, request: httpx.Request) -> httpx.Request:
        """Add the Bearer token to the request headers."""
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request

    def auth_flow(self, request: httpx.Request):
        """Controls the entire authentication workflow."""

        if not self.access_token:
            self._fetch_new_token()
        self.add_bearer_token(request)

        response = yield request

        # Handle Expiration (401 Unauthorized)
        if response.status_code == 401:
            self._fetch_new_token()
            self.add_bearer_token(request)

            # replays the API call
            retry_request = yield request

            # if still fails
            if retry_request.status_code == 401:
                retry_request.read()
                response = retry_request.json()
                raise RittenUnauthorizedError(
                    message=response.get("message", "Unauthorized request."),
                    status_code=retry_request.status_code,
                )
