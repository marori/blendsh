#!/usr/bin/env python3
try:
    import bpy, code
except:
    import os, sys
    os.system("%s/blendipse.py -u %s"%(os.path.dirname(__file__), __file__))
    sys.exit(0)
code.interact()
