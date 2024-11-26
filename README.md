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
    (hello + world)('print')  # helloworld
    
    leng = 10
    (engt)('print')  # engt
    (l + f'{leng}' + th)('print') # l10th 
    
    a = " 10 "
    num = 42
    (hello + a + world)('print') # hello 10 world
    (hello + f'{num}' + world)('print') # hello42world
    
    length = mystring('len')  
    (mystring + ' length == ' + f'{length}')('print') #mystring length == 8

main()
```
