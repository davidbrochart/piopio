import pickle, os, signal

def pio(func):
    return func

while True:
    with open('code.py', 'rt') as f:
        code = f.read()
        exec(code)
