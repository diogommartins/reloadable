from typing import Optional, Callable


def reloadable(exception_callback: Optional[Callable]=None,
               sleep_time: float=0,
               stop_condition_exception: BaseException=None,
               max_reloads: Optional[int]=None,
               return_on_sucess: bool=False) -> Callable:
    pass

def retry_on_error(exception_callback: Optional[Callable]=None,
                   sleep_time: float=0,
                   stop_condition_exception: BaseException=None,
                   max_reloads: Optional[int]=None) -> Callable:
    """ Convenience function to use reloadable with return_on_sucess=True """
    pass
