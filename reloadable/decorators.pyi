from typing import Optional, Callable


def reloadable(exception_callback: Optional[Callable]=None,
               sleep_time: float=0,
               stop_condition_exception: BaseException=None,
               max_reloads: Optional[int]=None) -> Callable:
    pass
