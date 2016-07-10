import subprocess, signal, os, inspect, sys, pickle

code_file_name = 'pc.py'
open(code_file_name, 'wt').close()

pypath = 'pypy'
# launch subprocess:
pyprocess = subprocess.Popen([pypath, os.path.dirname(__file__) + '/pe.py'])
# suspend subprocess:
os.kill(pyprocess.pid, signal.SIGSTOP)

main_pid = os.getpid()

pushed_code = []

def pio(func):
    def pyexec(args):
        global pushed_code
        # write subprocess code:
        with open(code_file_name, 'wt') as f:
            code = pushed_code
            pushed_code = []
            # write function:
            code += inspect.getsourcelines(func)[0]
            # suspend main:
            code.append('os.kill(' + str(main_pid) + ', signal.SIGSTOP)\n')
            # load arguments:
            code.append("with open('pi.pkl', 'rb') as f:\n")
            code.append('    args = pickle.load(f)\n')
            # call function:
            code.append('ret = ' + func.__name__ +'(args)\n')
            # dump results:
            code.append("with open('po.pkl', 'wb') as f:\n")
            code.append('    pickle.dump(ret, f)\n')
            # erase code:
            code.append("open('" + code_file_name + "', 'wt').close()\n")
            # resume main:
            code.append('os.kill(' + str(main_pid) + ', signal.SIGCONT)\n')
            f.writelines(code)
        # dump function argument values:
        with open('pi.pkl', 'wb') as f:
            pickle.dump(args, f)
        # erase results:
        open('po.pkl', 'wb').close()
        # resume subprocess:
        os.kill(pyprocess.pid, signal.SIGCONT)
        # wait for subprocess to execute function (not actually polling since main process will be suspended and then resumed by subprocess):
        while os.path.getsize('po.pkl') == 0:
            pass
        # suspend subprocess:
        os.kill(pyprocess.pid, signal.SIGSTOP)
        # load results:
        with open('po.pkl', 'rb') as f:
            ret = pickle.load(f)
        return ret
    return pyexec

def push_code(func):
    global pushed_code
    code = inspect.getsourcelines(func)[0]
    pushed_code += code
