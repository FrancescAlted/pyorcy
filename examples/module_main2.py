from __future__ import print_function
import sys
from time import time

# This module directory will be automatically added to sys.path so
# it is possible to import more modules in the same directory
#from compute_function2 import f
## Here we should implement this instead...
f = pyorcy.import("compute_function2.f")


def main():
    if "__args__" in globals():
        # Run through pyorcy.  Get parameters from __args__.
        n = int(__args__[0])
    else:
        # Run via regular python interpreter.
        n = int(sys.argv[1])
    t1 = timef(1000)

def timef(n):
    t1 = time()
    v = f(n, n)
    delta = time() - t1
    print("n = %d f = %.1f time: %.3fs" % (n, v, delta))
    return delta

if __name__ == "__main__":
    main()
