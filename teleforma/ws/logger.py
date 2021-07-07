from functools import wraps
from logging import getLogger

from channels.exceptions import AcceptConnection, DenyConnection, StopConsumer
from inspect import iscoroutinefunction

logger = getLogger("websocket")


def log_exceptions(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except (AcceptConnection, DenyConnection, StopConsumer):
            raise
        except Exception as exception:
            if not getattr(exception, "logged_by_wrapper", False):
                logger.error(
                    "Unhandled exception occurred in {}:".format(
                        f.__qualname__),
                    exc_info=exception,
                )
                setattr(exception, "logged_by_wrapper", True)
            raise
    return wrapper


def log_consumer_exceptions(klass):
    for method_name, method in list(klass.__dict__.items()):
        if iscoroutinefunction(method):
            setattr(klass, method_name, log_exceptions(method))

    return klass
