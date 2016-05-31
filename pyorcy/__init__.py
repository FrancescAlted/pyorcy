from __future__ import print_function
from __future__ import absolute_import

import sys
import re
import os
import importlib
import inspect
import pyximport
from .version import __version__

pyximport.install()


# Operation defaults
USE_CYTHON = True
VERBOSE = False


def parse_cython_module(path_in, force=False, verbose=True):
    """Extract cython code from the .py file and create a _cy.pyx file.

    The script is called by the cythonize decorator.
    """
    p_pattern = re.compile(r"\{\{\s*(.*?)\s*\|\s*p\s*\}\}")
    c_pattern = re.compile(r"(\{\{\s*(.*?)\s*\|\s*c\s*\}\})")
    if not path_in.endswith('.py'):
        raise ValueError("%s is not a python file" % path_in)

    path_out = path_in.replace('.py', '_cy.pyx')
    if (not force and os.path.exists(path_out) and
        os.path.getmtime(path_out) >= os.path.getmtime(path_in)):
        if verbose:
            print("File %s already exists" % path_out)
        return

    if verbose:
        print("Creating %s" % path_out)
    with open(path_out, 'w') as fobj:
        for line in open(path_in):
            line = line.rstrip()
            if mode == "cython":
                m = re.match(r'( *)(.*)#p *$', line)
                if m:
                    line = m.group(1) + '#p ' + m.group(2)
                else:
                    line = re.sub(r'#c ', '', line)
            # Now remove all python markers
            line = re.sub(p_pattern, '', line)
            # And extract cython ones
            line = re.sub(c_pattern, lambda m: m.group(2), line)
            fobj.write(line + '\n')


def parse_python_module(path_in, force=False, verbose=True):
    """Extract python code from the .py file and create a _py.pyx file.

    The script is called by the cythonize decorator.
    """
    p_pattern = re.compile(r"\{\{\s*(.*?)\s*\|\s*p\s*\}\}")
    c_pattern = re.compile(r"(\{\{\s*(.*?)\s*\|\s*c\s*\}\})")
    if not path_in.endswith('.py'):
        raise ValueError("%s is not a python file" % path_in)

    path_out = path_in.replace('.py', '_py.py')
    if (not force and os.path.exists(path_out) and
        os.path.getmtime(path_out) >= os.path.getmtime(path_in)):
        if verbose:
            print("File %s already exists" % path_out)
        return

    if verbose:
        print("Creating %s" % path_out)
    with open(path_out, 'w') as fobj:
        for line in open(path_in):
            line = line.rstrip()
            if not line:
                fobj.write(line + '\n')
            if "cythonize" in line and line.startswith('@'):
                # Do not include the @cythonize decorator so as to not call
                # it recursively
                continue
            # Now extract all python markers
            line = re.sub(p_pattern, lambda m: m.group(2), line)
            # And remove cython ones
            line = re.sub(c_pattern, '', line)
            if line:
                fobj.write(line + '\n')


def import_module(name):
    """Import a Cython module via pyximport machinery."""
    path = name.split('.')
    package = '.'.join(path[:-1])
    name_last = path[-1]
    if package:
        # when there is a package, let's add a preceding dot (absolute_import)
        name_last = '.' + name_last
    print("importing:", package, name_last)
    return importlib.import_module(name_last, package)


def cythonize(func):
    "Function decorator for triggering the pyorcy mechanism."
    # inspect usage found in http://stackoverflow.com/a/7151403
    func_filepath = inspect.getframeinfo(inspect.getouterframes(
        inspect.currentframe())[1][0])[0]
    print("filepath:", func_filepath)
    if USE_CYTHON:
        parse_cython_module(func_filepath, verbose=VERBOSE)
        module_name = func.__module__ + '_cy'
    else:
        parse_python_module(func_filepath, verbose=VERBOSE)
        module_name = func.__module__ + '_py'
    print("module_name:", module_name)
    module = import_module(module_name)
    parsed_func = getattr(module, func.__name__)

    def wrapper(*arg, **kw):
        if USE_CYTHON:
            if VERBOSE:
                print("Running via Cython mode")
        else:
            if VERBOSE:
                print("Running via Python mode")
        return parsed_func(*arg, **kw)

    return wrapper


def test():
    "Programatically run tests."
    import pytest
    sys.exit(pytest.main())


if __name__ == '__main__':
    extract_cython(sys.argv[1])
