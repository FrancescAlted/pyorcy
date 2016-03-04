======
pyorcy
======

Pyorcy has 2 purposes:

#. Allow the mix of python and cython code in a single file. This can also
   be done with cython pure python mode, but unlike pyorcy this approach does
   not offer you all the cython capabilities.

#. Launch the automatic compilation, triggered by a function decorator.

Check the examples: ``test.py`` and ``compute.py`` for a quick understanding
the mechanism.

Note that pyorcy provides a decorator mechanism which is similar to what numba
offers.

Mechanism
---------

The user writes a python file which is the module. The function which
is to have a speedup is decorated with the @cythonize decorator.

A cython (.pyx) file is extracted from the python file (cf. function
extract_cython in the pyorcy.py).

This file will differ from the corresponding .py file is two ways;

- the comments starting with '#c ' are uncommented.

- the lines ending with '#p' are commented out.

Getting started
---------------

In a command prompt, change into the pyorcy directory and type::

 python test.py 5000

Type the command once again to see what happens when the cython code is
already compiled.

Installation
------------

Put pyorcy.py somewhere in your PYTHONPATH.

Troubleshooting
---------------

If you get::

 ImportError: Building module compute_cy failed: ['DistutilsPlatformError: Unable to find vcvarsall.bat\n']

like me, contact me. I have found a workaround.

My use case
-----------

Here is why is pyorcy is important for my work.

I work in a team of developers (engineers, mathematicians). They have
learn python but not cython. Recently I have proposed a library with
some cython code. This added dependency has created resistance to the
acceptance of my code. Firstly, we met problems with compatibility
with Cython, Anaconda and virtual environments. Secondly, when my
collegues find bugs, they are not happy to depend on my help. They
want to do the debugging themselves. As they don't know Cython and are
uncomfortable with the compilation issues, I decided to provide two
versions of my code, one in pure python and another in Cython. Of
course maintaining two versions of my functions is not an advisable
approach. Using cython pure python mode is not an option since the
code needs advanced cython capabilities.

With pyorcy the user can then add a ``pyorcy.USE_CYTHON = False``
before the function call that they want to debug and proceed the
debugging in the pure python version, being able to add prints and
pbd without having to recompile, nor having to learn cython.