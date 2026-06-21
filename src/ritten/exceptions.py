"""
Ritten SDK Exceptions.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""


class RittenError(Exception):
    """The base exception for all Ritten SDK errors."""

    pass


class RittenClientError(RittenError):
    """Client is misconfigured or used incorrectly."""

    pass


class RittenConnectionError(RittenError):
    """SDK cannot reach the API."""

    pass


class RittenValueError(RittenError):
    """Invalid value provided to a method."""

    pass


class RittenParseError(RittenError):
    """Failed to parse API response."""

    pass


class RittenAuthError(RittenError):
    """Authentication error."""

    pass


# HTTP Response Errors
class RittenAPIError(RittenError):
    """Base class for errors returned by the Ritten API (HTTP 4xx and 5xx)."""

    def __init__(self, message: str, status_code: int, payload: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}


class RittenUnauthorizedError(RittenAPIError):
    """401 Unauthorized or 403 Forbidden."""

    pass


class RittenValidationError(RittenAPIError):
    """400 Bad Request or 422 Unprocessable Entity."""

    pass


class RittenNotFoundError(RittenAPIError):
    """404 Not Found."""

    pass


class RittenRateLimitError(RittenAPIError):
    """429 Too Many Requests."""

    pass


class RittenServerError(RittenAPIError):
    """5xx Server Errors (e.g., 500, 502, 503)."""

    pass


ERROR_MAP = {
    400: RittenValidationError,
    403: RittenUnauthorizedError,
    404: RittenNotFoundError,
    422: RittenValidationError,
    429: RittenRateLimitError,
    500: RittenServerError,
    502: RittenServerError,
    503: RittenServerError,
}
"""Mapping of HTTP status codes to specific error classes for structured error handling."""
