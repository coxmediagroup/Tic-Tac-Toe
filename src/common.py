'''
Created on May 9, 2011

@author: pmtemp
'''
EMPTY   = 0
NOUGHT  = 1
CROSS   = 2
DRAW    = 3
DEBUG   = True
shape_map = {0: " ", 1 : 0, 2 : "x"}

def singleton(cls):
    """ Enforce single instance of decorated class """
    instances = {}
    def getInstance():
        if not cls in instances.keys():
            instances[cls] = cls()
        return instances[cls]
    return getInstance

def debug(f):
    """ Print a basic debug statement """
    def wrapper(*args, **kwargs):
        print "executing: ",f.func_name
        f(*args, **kwargs)
    return wrapper

@singleton
class Storage:
    def __init__(self):
        self._game_board = None
        self._player_one = None
        self._player_two = None
        self._game_instance = None

def indexes(lst, val):
    """ return all indexes value occupies in a list """
    return [ind for ind, item in enumerate(lst) if item == val] 
