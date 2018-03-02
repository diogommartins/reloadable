from functools import wraps
from time import sleep
from typing import Optional, Callable

from reloadable import config


def reloadable(exception_callback: Optional[Callable]=None,
               sleep_time: float=0,
               stop_condition_exception: BaseException=None,
               max_reloads: Optional[int] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            reload_counter = 0

            if not config.ENABLED:
                return func(*args, **kwargs)

            while reload_counter != max_reloads:
                try:
                    func(*args, **kwargs)
                except (stop_condition_exception or config.STOP_CONDITION_EXCEPTION) as e:
                    raise e
                except Exception as e:
                    if exception_callback:
                        exception_callback(e)
                    sleep(sleep_time)
                    reload_counter += 1
        return wrapper
    return decorator
