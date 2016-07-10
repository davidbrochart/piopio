import os, signal, pickle

code_file_name = 'pc.py'

def pio(func):
    return func

while True:
    with open(code_file_name, 'rt') as f:
        code = f.read()
        exec(code)
