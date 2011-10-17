pyumpf
======

Python Unified Multiprocessing Parallel Functions

This is a small library that aims to bring together the standard library map/reduce functions
with both the multiprocessing module in the standard library and the PP module (www.parallelpython.com).

Each has their own niche, and there own advantages and disadvantages. The map/reduce functions
in the standard library are good for implementing a functional paradigm, but are limited by the GIL
to only run one task at a time. The multiprocessing module is good for single machines with multiple
CPUs, but can be awkward to debug and use. The PP module is great for clusters, but is even more
awkward to debug and use. Plus all of these have different APIs, and so cannot be drop-in replacements.

pyumpf gets around this by providing a unified interface via umpf.map and umpf.reduce that can easily be 
expanded to use multiprocessing or PP when needed, but also collapsed to the built-in map/reduce for
simpler debugging.

To install: python setup.py install

For an example, see umpf_test.py Note that this example gives PP a poor performance. This is because 
it is running on a single machine, and this example is too small to make best use of the parallelism.
Ideally, tasks should run for several seconds each and have easily pickleable arguments and returned
values.

By default, umpf defaults to pythons built-in map/reduce. These are single-threaded.

To use multiprocessing, do the following:

    import umpf
    import multiprocessing as mp
    umpf.Hub.pool = mp.Pool()
    
To use Parallel Python, do the following:

    import umpy
    import pp
    umpy.Hub.pool = pp.Server()
