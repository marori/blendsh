#!/usr/bin/env python3
import sys
import os

argv = sys.argv

blender_default = "/opt/blender/blender"

path = os.environ['PATH'] + ':' + blender_default

for p in path.split(os.pathsep):
    p = os.path.join(p, 'blender')
    if os.path.isfile(p) and os.access(p, os.X_OK):
        blender = p

if not blender:
    print("Blender executable not found")
    sys.exit(1)    

tmpfile = "/tmp/blendips.args"

class UnbufferedStream(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, *args, **kwargs):
        self.stream.write(*args, **kwargs)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)
sys.stdout = UnbufferedStream(sys.stdout)

mode = 'PYTHON3'
for arg in argv[1:]:
    if os.path.isfile(arg):
        mode = 'DEBUG' if arg.endswith("pydevd.py") else 'BLENDER'
        argv = argv[2:]
        break    
try:
    import bpy
except:
    if mode == 'PYTHON3':
        cmd = '/usr/bin/env python3 %s'%(" ".join(sys.argv[1:]))
        os.system(cmd)
    else:
        bg = "-b" if mode == 'BLENDER' else ''
        with open(tmpfile, 'w') as args:
            args.write(" ".join(argv))
        cmd = "%s %s -P $(readlink -f %s)"%(blender, bg, __file__)
        os.system(cmd)
    sys.exit()

pypredef_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "python_api", "pypredef")
sys.path.append(pypredef_path)

with open(tmpfile, 'r') as args:
    sys.argv = args.read().split()

filename = sys.argv[0]
path = os.path.dirname(filename)
sys.path.append(path)
__file__ = os.path.realpath(filename)
print(__file__)
with open(filename, 'r') as fh:
    exec(fh.read())
