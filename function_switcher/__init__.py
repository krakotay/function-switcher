# function_switcher.py

import functools
import builtins
from typing import Any, Callable

def switch_call(func: Callable) -> Callable:
    """
    A decorator that switches function calls behavior:
    If a string argument is passed to a function, it's interpreted as the target function name,
    while the original function name becomes the argument.
    
    Example:
        @switch_call
        def main():
            hello('print')  # Equivalent to: print('hello')
            length = mystring('len')  # Get length of 'mystring'
            print(f"Length is: {length}")
    
    Args:
        func (Callable): The function to be decorated
        
    Returns:
        Callable: The wrapped function with switched behavior
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Save original global variables
        original_globals = func.__globals__.copy()
        
        # Create proxy for non-existent functions
        class ProxyFunction:
            def __init__(self, name):
                self.name = name
                
            def __call__(self, func_name: str, *args, **kwargs):
                if isinstance(func_name, str):
                    target_func = getattr(builtins, func_name, None)
                    if target_func is not None and callable(target_func):
                        result = target_func(self.name, *args, **kwargs)
                        return result
                    raise ValueError(f"Function '{func_name}' not found")
                return NotImplemented
        
        # Create new namespace with proxy
        class Namespace(dict):
            def __missing__(self, key):
                if key == 'print':
                    return builtins.print
                return ProxyFunction(key)
            
            def __getitem__(self, key):
                if key == 'print':
                    return builtins.print
                return super().__getitem__(key)
        
        # Execute function with modified global variables
        try:
            return eval(
                func.__code__,
                Namespace(original_globals),
                {}
            )
        finally:
            # Restore original global variables
            func.__globals__.clear()
            func.__globals__.update(original_globals)
    
    return wrapper
