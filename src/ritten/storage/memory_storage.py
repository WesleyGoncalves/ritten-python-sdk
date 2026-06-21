"""
In-memory token storage implementation.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""


class MemoryStorage:
    """
    In-memory token storage implementation.
    This is a simple storage mechanism that keeps the token in memory.
    """

    def __init__(self, initial_token: str | None = None):
        self._token = initial_token

    def get_token(self) -> str | None:
        return self._token

    def set_token(self, token: str) -> None:
        self._token = token
