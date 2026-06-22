"""
Ritten SDK.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

from importlib.metadata import version, PackageNotFoundError

from ritten.ritten import Ritten
from ritten.auth import Auth
from ritten.config import Config
from ritten.exceptions import (
    RittenError,
    RittenClientError,
    RittenConnectionError,
    RittenAPIError,
    RittenAuthError,
    RittenUnauthorizedError,
    RittenValidationError,
    RittenNotFoundError,
    RittenRateLimitError,
    RittenServerError,
)
from ritten.resources import (
    Resource,
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
from ritten.storage import TokenStorage, MemoryStorage

__all__ = [
    "Ritten",
    "Auth",
    "Config",
    "TokenStorage",
    "MemoryStorage",
    "RittenError",
    "RittenClientError",
    "RittenConnectionError",
    "RittenAPIError",
    "RittenAuthError",
    "RittenUnauthorizedError",
    "RittenValidationError",
    "RittenNotFoundError",
    "RittenRateLimitError",
    "RittenServerError",
    "Resource",
    "Calendar",
    "Cases",
    "Contacts",
    "Facilities",
    "Forms",
    "Insurance",
    "Organizations",
    "Patients",
    "Programs",
    "Users",
]


try:
    __version__ = version("ritten-python-sdk")
except PackageNotFoundError:
    __version__ = "unknown"
