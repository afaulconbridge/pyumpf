import multiprocessing as mp
import pp
import timeit

import umpf
import umpf_test

def f(x,y):
    for j in xrange(1000):
        i = x * y * x * y * j
        i = x * y * x * y * j
        i = x * y * x * y * j
    return (x,y)
    
    
class Boris(object):
    def g(self, x, y):
        return f(x,y)
        
    def __call__(self, x, y):
        return f(x,y)
        
def run():

    count = 500
    
    for i in umpf.map(umpf_test.f, xrange(count), xrange(count+2)):
        i
    
    boris = umpf_test.Boris()   
        
    for i in umpf.map(boris.g, xrange(count), xrange(count+2)):
        i
        
    for i in umpf.map(boris, xrange(count), xrange(count+2)):
        i

if __name__ == "__main__":

    repeats = 10
    duplicates = 3

    t = timeit.Timer(run)
    print "map times", t.repeat(duplicates, repeats)
    
    umpf.Hub.pool = mp.Pool()
    t = timeit.Timer(run)
    print "multiprocessing times", t.repeat(duplicates, repeats)
    del umpf.Hub.pool
    
    
    umpf.Hub.server = pp.Server()
    t = timeit.Timer(run)
    print "PP times", t.repeat(duplicates, repeats)
    del umpf.Hub.server
