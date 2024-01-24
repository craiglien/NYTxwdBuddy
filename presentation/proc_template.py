import atexit
import inspect
import re
import subprocess
import sys
import tempfile
import os

dir_depth = 2

if len(sys.argv) != 3:
    print("arguments source_template destination_file")
    sys.exit()

parts = os.path.realpath(__file__).split('/')
repo_path='/'.join(parts[:-1*dir_depth])
sys.path.insert(0, repo_path)

import fetch_and_crack

def get_object(src):
    return inspect.getsource(eval(src))

def get_file(src):
    with open(f"{repo_path}/{src}") as f:
        return f.read()

def execute_shell(src):
    result = subprocess.run(f"cd {repo_path}; {src}", stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, text=True, shell=True)
    return result

def value_so(value, arg):
    return value.stdout

def value_re(value, arg):
    match = re.search(eval(arg), value, re.MULTILINE)
    return match.group(0)

def value_l(value, arg):
    lns = value.split('\n')
    rngs = arg[1:].split(',')
    ret = []
    for r in rngs:
        if ":" in r:
            i = r.split(":")
            si = int(i[0]) if i[0] else None
            ei = int(i[1]) if i[1] else None
            ret += lns[si:ei]
        else:
            ret += [lns[int(r)]]
    return '\n'.join(ret)

class DynamicKeys(dict):
    def process_line(self, ln):
        kee, op, src, arg = ln.strip().split(':', 3)
        value = None
        value = {
            "o": get_object,
            "f": get_file,
            "x": execute_shell,
            }[op](src)
        self[kee] = {
            "": value_so,
            "r": value_re,
            "l": value_l,
            }[arg[:1]](value, arg=arg)

dk = DynamicKeys()

tmp_file = tempfile.NamedTemporaryFile(mode="w+", buffering=1, delete=False)
atexit.register(os.remove, tmp_file.name)

with open(sys.argv[1]) as rf:
    for ln in rf.readlines():
        if ln.startswith('__DK:'):
#            tmp_file.write(ln)
            dk.process_line(ln[5:])
        else:
            tmp_file.write(ln)

fetch_and_crack.process_template(tmp_file.name, sys.argv[2], dk)
