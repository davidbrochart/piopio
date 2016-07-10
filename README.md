Python Input Output
===========

Offload Python code to another Python interpreter - typically PyPy.
piopio sends function code and arguments to a PyPy process, and gets the results back. It's main purpose is execution speed up, but it can also be useful for executing Python2 code into a Python3 program.

General Usage
---------------

It mimics Numba's `@jit` decorator.
The function you want to offload to PyPy is decorated with `@pio`.


```python
from piopio import pio

@pio
def foo(x):
    return 'PyPy is saying ' + x + ' !!!'

for i in range(10):
    print(foo(str(i)))
```

The `foo` function will be offloaded to PyPy.
