# Function Switcher

A Python decorator that allows switching function calls behavior. When you pass a string argument to a function, it's interpreted as the target function name, while the original function name becomes the argument.

## Installation

```bash
pip install git+https://github.com/krakotay/function-switcher.git
```

## Usage

```python
from function_switcher import switch_call

@switch_call
def main():
    hello('print')  # Prints: hello
    length = mystring('len')  # Gets length of 'mystring'
    print(f"Length of 'mystring' is: {length}")
```
