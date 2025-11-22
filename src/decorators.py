import datetime
import functools
import sys
from typing import Callable, Optional, ParamSpec, TextIO, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор, логирующий начало и конец выполнения функции,
    результаты или ошибки в файл или консоль.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = datetime.datetime.now()

            log_output: TextIO
            if filename:
                log_output = open(filename, "a", encoding="utf-8")
            else:
                log_output = sys.stdout  # type: ignore[assignment]

            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now()
                duration = end_time - start_time
                log_message = (
                    f"{func.__name__} ok\n"
                    f"  Start: {start_time}, End: {end_time}, Duration: {duration}\n"
                    f"  Result: {result!r}\n"
                )
                log_output.write(log_message)
                return result

            except Exception as e:
                end_time = datetime.datetime.now()
                duration = end_time - start_time
                error_message = (
                    f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                    f"  Start: {start_time}, End: {end_time}, Duration: {duration}\n"
                    f"  Error details: {e}\n"
                )
                log_output.write(error_message)
                raise e

            finally:
                if filename:
                    log_output.close()

        return wrapper

    return decorator
