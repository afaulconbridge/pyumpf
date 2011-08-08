import multiprocessing as mp
import itertools as it
import inspect
import time

#import pp

#this is this file
import umpf

oldmap = map
oldreduce = reduce

p = None 

def _reduce(things):
    f, data = things
    if len(data) == 1:
        return data[0]
    else:
        return f(*data)
        
def minlength(iterable, minlength):
    i = 0
    for x in iterable:
        i += 1
        if i >= minlength:
            return True
    return False
        
    
    
def _mypool_bound_method(passed):
    ((name, self, cls), (args, kwargs)) = passed
    return cls.__dict__[name](self, *args, **kwargs)

def _mypool_function(passed):
    (f, (args, kwargs)) = passed
    return f(*args, **kwargs)
    

class Hub(object):
    server = None
    pool = None

    @classmethod
    def map(cls, f, *args, **kwargs):
        """
        Wrapper of pythons built-in multiprocessing library that is more like the map
        function.
        
        Handles instance methods, as long as they are the same as the class method and 
        do not modify the object as a side-effect. 
        
        Takes parameters as iterables and uses them in lock-step until the shortest is terminated. 
        
        If you have AttributeError problems passing functions, use a fully-qualified imported path.
        
        Does not work with @classmethod or @static method.
        
        Does not modify default parameters as a side effect, or use use modified default parameters.
        """
            
        #need to turn args and kwargs into a single itterable
        #each item in that itterable is a tuple of one set of args and the kwargs
        newargs = it.izip(*args)
        newargskwargs = it.izip(newargs, it.repeat(kwargs))

        #now we need a function that will deal with it approriately
        #at a minimum, the function must unpack the args and kwargs
        #if we were given an instancemethod, we need to handle it too
        
        if inspect.ismethod(f):
            #this is an instance method
            #pickle cant handle this, so hack it apart
            
            #TODO find a way to tell if a function is different from its class method
                        
            if inspect.isclass(f.im_self):
                #this was a class method
                #cant handle this at the moment
                raise ValueError, "classmethod is not usable"
            else:
                assert f.im_func.__name__ in f.im_class.__dict__
                realargs = it.izip(it.repeat((f.im_func.__name__, f.im_self, f.im_class)), newargskwargs)
                tocall = umpf._mypool_bound_method
        else:
            #this is a function, or a function-like object
            #pickle can handle this
            #or pickle cant handle it, but then there is nothing I can do about it anyway!
            
            #TODO maybe raise some warnings if its not pickleable or other pitfalls?
            
            realargs = it.izip(it.repeat(f), newargskwargs)
            tocall = umpf._mypool_function
            
        if cls.server is not None:
            globe = globals()
            for job in (cls.server.submit(tocall, (x,), globals=globe) for x in realargs):
                yield job()
        elif cls.pool is not None:
            for i in cls.pool.imap(tocall, realargs):
                yield i
        else:
            for i in oldmap(tocall, realargs):
                yield i

    @classmethod
    def reduce(cls, f, iterable):
        """
        Wrapper of pythons built-in multiprocessing library that is more like a 
        drop-in replacement for map.
        
        Also handles using instance methods, assuming that they are the same as the class
        method.
        
        Takes parameters as itterables and uses them in lock-step.    
        """
        results = iterable
        a, b = it.tee(results, 2)
        while minlength(a, 2):
            results = b
            steps = pairs(results)
            results = cls.map(_reduce, it.izip(it.repeat(f), steps))
            a, b = it.tee(results, 2)
        results = tuple(b)
        if len(results) == 0:
            return None
        else:
            return results[0]

map = Hub.map
reduce = Hub.reduce

#umpf.Hub.pool = mp.Pool()
#umpf.Hub.server = pp.Server()

def pairs(iterable):
    a = None
    for x in iterable:
        if a is None:
            a = x
        else:
            yield (a,x)
            a = None
    if a is not None:
        yield (a,)
    
