import subprocess, signal, os, inspect, pickle, sys

open('code.py', 'wt').close()

pypath = 'pypy'
# launch subprocess:
pyprocess = subprocess.Popen([pypath, os.path.dirname(__file__) + '/py.py'])
# suspend subprocess:
os.kill(pyprocess.pid, signal.SIGSTOP)

main_pid = os.getpid()

def pio(func):
    def pyexec(args):
        # write subprocess code:
        with open('code.py', 'wt') as f:
            # write function:
            code = inspect.getsourcelines(func)[0]
            # suspend main:
            code.append('os.kill(' + str(main_pid) + ', signal.SIGSTOP)\n')
            # load arguments:
            code.append("with open('data_in.pkl', 'rb') as f:\n")
            code.append('    args = pickle.load(f)\n')
            # call function:
            code.append('ret = ' + func.__name__ + '(args)\n')
            # dump results:
            code.append("with open('data_out.pkl', 'wb') as f:\n")
            code.append('    pickle.dump(ret, f)\n')
            # erase code:
            code.append("open('code.py', 'wt').close()\n")
            # resume main:
            code.append('os.kill(' + str(main_pid) + ', signal.SIGCONT)\n')
            f.writelines(code)
        # dump function argument values:
        with open('data_in.pkl', 'wb') as f:
            pickle.dump(args, f)
        # erase results:
        open('data_out.pkl', 'wb').close()
        # resume subprocess:
        os.kill(pyprocess.pid, signal.SIGCONT)
        # wait for subprocess to execute function (not actually polling since main process will be suspended and then resumed by subprocess):
        while os.path.getsize('data_out.pkl') == 0:
            pass
        # suspend subprocess:
        os.kill(pyprocess.pid, signal.SIGSTOP)
        # load results:
        with open('data_out.pkl', 'rb') as f:
            ret = pickle.load(f)
        return ret
    return pyexec
