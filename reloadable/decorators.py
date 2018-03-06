from functools import wraps, partial
from time import sleep

from reloadable import config


def reloadable(exception_callback=None,
               sleep_time=0,
               stop_condition_exception=None,
               max_reloads=None,
               return_on_sucess=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            reload_counter = 0

            if not config.ENABLED:
                return func(*args, **kwargs)

            while reload_counter != max_reloads:
                try:
                    result = func(*args, **kwargs)
                    if return_on_sucess:
                        return result
                except (stop_condition_exception or config.STOP_CONDITION_EXCEPTION) as e:
                    raise e
                except Exception as e:
                    if exception_callback:
                        exception_callback(e)
                    sleep(sleep_time)
                    reload_counter += 1
        return wrapper
    return decorator


retry_on_error = partial(reloadable, return_on_sucess=True)
