Python Input Output
===========

Offload Python code to another Python interpreter - typically PyPy.

piopio sends function code and arguments to a PyPy process, and gets the results back. Its main purpose is execution speed up, but it can also be useful for executing Python2 code inside a Python3 program.

General Usage
---------------

It mimics Numba's `@jit` decorator. The function you want to offload to PyPy is decorated with `@pio`.

```python
from piopio import pio

@pio
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

print(fib(40))
```

With the `@pio` decorator, the `fib` function will be offloaded to PyPy and computed quite quickly. Try commenting out the decorator!

Limitations
-------------
  - It only works on Linux.
  - Nested functions are not automatically offloaded. You need to call `push_code(func)` if `func` is called by the offloaded function.

How it works
-------------

It is done the bad way! Function code and arguments/results are passed using files. Code is clear text, while arguments and results are pickled. The execution of the PyPy subprocess is controlled using Linux signals (SIGSTOP/SIGCONT). When the PyPy process is running, it also controls the execution of the main process using these Linux signals.
