import time
from functools import wraps


def timer_decorator(func):
    """Декоратор для измерения времени выполнения функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # в миллисекундах
        print(f"Время выполнения {func.__name__}: {execution_time:.5f} мс")
        return result

    return wrapper
