"""
Ritten SDK Token Storage Protocol.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class TokenStorage(Protocol):
    """
    Contract for token storage.

    This allows for flexible implementations, such as in-memory, file-based, or database storage.
    """

    def get_token(self) -> str | None:
        """Retrieve the current access token, if it exists."""
        ...

    def set_token(self, token: str) -> None:
        """Store a new access token."""
        ...
