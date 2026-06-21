"""
Ritten SDK Resource Base Class.

:copyright: (c) 2026 by Wesley Gonçalves.
:license: MIT, see LICENSE for more details.
"""

import inspect
from typing import Any

from ritten.decorators import exception_handler


class Resource:
    """
    A base class for all SDK resources.
    It automatically wraps all public methods with an exception handler.
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        for attr_name, attr_value in cls.__dict__.items():
            if inspect.isfunction(attr_value) and not attr_name.startswith("_"):
                setattr(cls, attr_name, exception_handler(attr_value))
