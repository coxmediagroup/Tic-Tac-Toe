import doctest
import xsos
import sim

if __name__ == '__main__':
    res = doctest.testmod(m=xsos)
    print "%d/%d tests passed in xsos.py" % (res.attempted - res.failed, res.attempted)
    res = doctest.testmod(m=sim)
    print "%d/%d tests passed in sim.py" % (res.attempted - res.failed, res.attempted)
    
