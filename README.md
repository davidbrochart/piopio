Python Input Output
===========

Offload Python code to another Python interpreter - typically PyPy.

piopio sends function code and arguments to a PyPy process, and gets the results back. Its main purpose is execution speed up, but it can also be useful for executing Python2 code into a Python3 program.

General Usage
---------------

It mimics Numba's `@jit` decorator. The function you want to offload to PyPy is decorated with `@pio`.


```python
from piopio import pio

@pio
def foo(x):
    return 'PyPy is saying ' + x + ' !!!'

for i in range(10):
    print(foo(str(i)))
```

The `foo` function will be offloaded to PyPy.

Limitations
-------------
  - It only works on Linux.
  - Nested functions are not automatically offloaded. You need to call `push_code(func)` if `func` is called by the offloaded function.

How it works
-------------

It is done the bad way! Function code and arguments/results are passed using files. Code is clear text, while arguments and results are pickled. The execution of the PyPy subprocess is controlled using Linux signals (SIGSTOP/SIGCONT). When the PyPy process is running, it also controls the execution of the main process using these Linux signals.
