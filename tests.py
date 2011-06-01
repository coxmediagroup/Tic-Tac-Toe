import doctest
import xsos

if __name__ == '__main__':
    res = doctest.testmod(m=xsos)
    print "%d/%d tests passed" % (res.attempted - res.failed, res.attempted)
    
