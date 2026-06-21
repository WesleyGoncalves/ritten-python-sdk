from functools import wraps
import httpx
from pydantic import ValidationError
import json
from ritten.exceptions import (
    RittenError,
    RittenConnectionError,
    RittenValueError,
    RittenParseError,
)


def exception_handler(func):
    """
    Decorator that translates third-party exceptions into native SDK exceptions.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        # If it's a RittenError exception, reraise it.
        except RittenError:
            raise

        # Network-level failures
        except httpx.RequestError as e:
            raise RittenConnectionError(f"A network error occurred: {str(e)}") from e

        # Validation errors
        except ValidationError as e:
            raise RittenValueError(f"Data validation failed: {str(e)}") from e

        # JSON parsing errors
        except json.JSONDecodeError as e:
            raise RittenParseError(
                f"Failed to parse API response as JSON: {str(e)}"
            ) from e

        # The Ultimate Catch-All for anything else
        except Exception as e:
            raise RittenError(f"An unexpected SDK error occurred: {str(e)}") from e

    return wrapper
