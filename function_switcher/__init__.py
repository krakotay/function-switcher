import functools
import builtins
from typing import Any, Callable

class ProxyString:
    """
    A string that can act as a function, with support for string interpolation
    """
    def __init__(self, value: Any):
        self.value = str(value)
        
    def __call__(self, func_name: str | Callable, *args, **kwargs):
        if isinstance(func_name, str):
            target_func = getattr(builtins, func_name, None)
            if target_func is not None and callable(target_func):
                return target_func(self.value, *args, **kwargs)
            raise ValueError(f"Function '{func_name}' not found")
        elif callable(func_name):
            return func_name(self.value, *args, **kwargs)
        return NotImplemented
    
    def __add__(self, other):
        return ProxyString(self.value + str(other))
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"ProxyString('{self.value}')"


class ProxyFunction:
    def __init__(self, name: Any):
        self.name = name
        
    def __call__(self, func_name: str | Any, *args, **kwargs):
        if isinstance(func_name, str):
            target_func = getattr(builtins, func_name, None)
            if target_func is not None and callable(target_func):
                result = target_func(str(self.name), *args, **kwargs)
                return result
            raise ValueError(f"Function '{func_name}' not found")
        return NotImplemented
    
    def __add__(self, other):
        return ProxyString(str(self.name) + str(other))
    
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return f"ProxyFunction('{self.name}')"


class Namespace(dict):
    def __missing__(self, key):
        if isinstance(key, (set, dict)):  # Обрабатываем и множества, и словари
            # Получаем значение из множества или словаря
            try:
                if isinstance(key, set):
                    value = next(iter(key))
                else:
                    value = next(iter(key.values()))
                return ProxyFunction(value)
            except StopIteration:
                return ProxyFunction("")
        return ProxyFunction(key)
        
    def __getitem__(self, key):
        return super().__getitem__(key)

def switch_call(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        original_globals = func.__globals__.copy()
        
        try:
            return eval(
                func.__code__,
                Namespace(original_globals),
                {}
            )
        finally:
            func.__globals__.clear()
            func.__globals__.update(original_globals)
    
    return wrapper