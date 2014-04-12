
class MoveGenerator(object):
   '''Figures out next move based on a dictionary describing the game.
    Dictionary should be in this format: {'box_0':0,'box_1':2}.
    0: empty square
    1: your square
    2: opponents square
    '''

    your_moves = 0
    opp_moves = 0

    def __init__(self,moves,*args,**kwargs):
        if not isinstance(moves,dict):
            raise ValueError(u"Pass a dictionary of moves.")

        for x in xrange(0,9):
            box = 'box_%s' % x
            setAttr(self,box,moves.get(box,0))
            if moves.get(box,0) == 1:
                self.your_moves += 1
            elif moves.get(box,0) == 2:
                self.opp_moves += 1

        self.total_moves = your_moves + opp_moves
        self.first = self.is_even(self.total_moves)

    

    @staticmethod
    def is_even(num):
        return num % 2 == 0
