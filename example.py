from piopio import pio

@pio
def foo(x):
    import time
    time.sleep(1)
    return 'PyPy is saying ' + x + ' !!!'

i = 0
while True:
    print(foo(str(i)))
    i += 1
