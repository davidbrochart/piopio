from piopio import pio, push_code

def bar(x):
    return 'PyPy is saying ' + x + ' !!!'

@pio
def foo(x):
    return bar(x)

push_code(bar)
for i in range(10):
    print(foo(str(i)))
