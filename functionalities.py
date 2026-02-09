from functools import wraps
from datetime import datetime

def log_operacao(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} - {datetime.now()}")
        return func(*args, **kwargs)
    return wrapper
