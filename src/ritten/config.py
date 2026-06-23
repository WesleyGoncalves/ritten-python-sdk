"""
Ritten SDK Configuration.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

from typing import Any
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    ConfigDict,
)
from ritten.storage import TokenStorage, MemoryStorage
from ritten.exceptions import RittenError


class Config(BaseModel):
    """Configuration for the Ritten SDK client."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    base_url: str = Field(
        default="https://api.ritten.io/v1",
        description="Base URL for the Ritten API.",
    )

    audience: str = Field(
        default="https://external-api.ritten.io",
        description="Audience for OAuth token requests.",
    )

    # Authentication
    tenant_id: str | None = Field(
        default="ritclinic",
        description="Tenant ID for the Ritten API.",
    )

    client_id: str | None = Field(
        default=None,
        description="Client ID for authentication.",
    )
    client_secret: str | None = Field(
        default=None,
        description="Client secret for authentication.",
    )

    storage: TokenStorage = Field(
        default=MemoryStorage(),
        description="Token storage mechanism. Defaults to in-memory storage.",
    )

    @field_validator("storage", mode="after")
    @classmethod
    def validate_storage_interface(cls, value: Any) -> Any:
        """Validates that the provided storage object implements the `TokenStorage` protocol if it is not None."""
        if value is None:
            return value

        if not isinstance(value, TokenStorage):
            raise RittenError(
                "The provided storage object must implement the `TokenStorage` protocol."
            )

        return value

    # Connection pooling and timeout settings
    timeout: float = Field(
        default=30.0,
        description="The timeout in seconds for the HTTP client.",
    )
    max_connections: int = Field(
        default=10,
        description="Maximum number of concurrent connections in the pool.",
    )
    max_keepalive_connections: int = Field(
        default=5,
        description="Maximum number of keep-alive connections to maintain.",
    )

    keepalive_expiry: float = Field(
        default=5.0,
        description="Time in seconds before a keep-alive connection is closed. Keep this low for serverless.",
    )
