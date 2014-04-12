
class MoveGenerator(object):
   '''Figures out next move based on a dictionary describing the game.
    Dictionary should be in this format: {'box_0':0,'box_1':2}.
    0: empty square
    1: your square
    2: opponents square
    '''
    def __init__(self,moves,*args,**kwargs):
        if not isinstance(moves,dict):
            raise ValueError(u"Pass a dictionary of moves.")

        for x in xrange(0,9):
            setAttr(self,"box_%s" % x,moves.get("box_%s" % x,0))

        