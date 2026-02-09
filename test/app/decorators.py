from functools import wraps
from datetime import datetime

def log_operacao(func):
    """Decorador que registra operações com timestamp"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        return func(*args, **kwargs)
    return wrapper
