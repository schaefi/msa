import sys
from functools import wraps
from typing import Callable
from msa.logger import MSALogger

log = MSALogger.get_logger()


def exception_handler(func: Callable) -> Callable:
    """
    Decorator method to add exception handling
    Methods marked with this decorator are called under

    control of the MSA exceptions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MSAError as issue:
            # known exception, log information and exit
            log.error(f'{type(issue).__name__}: {issue}')
            sys.exit(1)
        except KeyboardInterrupt:
            log.error('Exit on keyboard interrupt')
            sys.exit(1)
        except SystemExit as issue:
            # user exception, program aborted by user
            sys.exit(issue)
        except Exception:
            # exception we did no expect, show python backtrace
            log.error('Unexpected error:')
            raise
    return wrapper


class MSAError(Exception):
    """
    **Base class to handle all known exceptions**

    Specific exceptions are implemented as sub classes of MSAError

    :param str message: Exception message text
    """
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return format(self.message)


class MSAConfigFileNotFoundError(MSAError):
    """
    Exception raised if a config file could not be found
    """
