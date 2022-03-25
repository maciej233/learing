# we use wraps to print fibonacci fun from trace
from functools import wraps
import pickle
def trace(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        result = fun(*args, **kwargs)
        print(f"{fun.__name__}({args!r})_({kwargs!r}) --> ({result!r})")
        return result
    return wrapper

@trace
def fibonacci(n):
    """This is fibonacci function"""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

fibonacci = trace(fibonacci)

print(pickle.dumps(fibonacci))