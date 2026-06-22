"""
Utility functions for the Ritten SDK.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

from datetime import datetime, timezone


def to_iso_format(dt: datetime) -> str:
    """Converts a datetime object into a clean ISO 8601 string."""
    if dt.tzinfo == timezone.utc:
        return dt.isoformat(timespec="seconds").replace("+00:00", "Z")
    return dt.isoformat(timespec="seconds")
