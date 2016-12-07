
class MoveGenerator(object):
    '''Figures out next move based on a dictionary describing the game.
    Dictionary should be in this format: {'box_0':0,'box_1':2}.
    0: empty square
    1: your square
    2: opponents square
    '''

    my_moves = 0
    opp_moves = 0

    def __init__(self,moves,*args,**kwargs):
        if not isinstance(moves,dict):
            raise ValueError(u"Pass a dictionary of moves.")

        self.possible_moves = []
        self.winner = None

        for x in xrange(0,9):
            box = 'box_%s' % x
            setattr(self,box,moves.get(box,'0'))
            if moves.get(box,'0') == '1':
                self.my_moves += 1
            elif moves.get(box,'0') == '2':
                self.opp_moves += 1
            else:
                self.possible_moves.append(box)

        self.total_moves = self.my_moves + self.opp_moves
        self.set_first()

        self.win_cont = [['box_0','box_1','box_2'],
                         ['box_3','box_4','box_5'],
                         ['box_6','box_7','box_8'],
                         ['box_0','box_3','box_6'],
                         ['box_1','box_4','box_7'],
                         ['box_2','box_5','box_8'],
                         ['box_0','box_4','box_8'],
                         ['box_2','box_4','box_6'],
                         ]
    def get_possible_moves(self):
        move_list = []
        for x in xrange(0,9):
            box = 'box_%s' % x
            if getattr(self,box) == '0':
                move_list.append(box)
        return move_list


    def make_move(self):
        move, score = self.max_move()
        if move:
            setattr(self,move,'1')
        self.is_gameover()

    def max_move(self):
        best_score = None
        best_move = None
        for move in self.get_possible_moves():
            setattr(self,move,'1')

            if self.is_gameover():
                score = self.get_score()
            else:
                min_move, score = self.min_move()

            setattr(self,move,'0')
            self.winner = None

            if best_score == None or score > best_score:
                best_score = score
                best_move = move

        return best_move, best_score

    
    def min_move(self):
        best_score = None
        best_move = None
        for move in self.get_possible_moves():
            setattr(self,move,'2')

            if self.is_gameover():
                score = self.get_score()
            else:
                min_move, score = self.max_move()

            setattr(self,move,'0')
            self.winner = None

            if best_score == None or score < best_score:
                best_score = score
                best_move = move

        return best_move, best_score


    def is_gameover(self):
        for x,y,z in self.win_cont:
            if getattr(self,x) == getattr(self,y) == getattr(self,z) and not getattr(self,x) == '0':
                self.winning_three = [int(x.split('_')[1]),int(y.split('_')[1]),int(z.split('_')[1])]
                if getattr(self,x) == '1':
                    self.winner = '1'
                    return True
                elif getattr(self,x) == '2':
                    self.winner = '2'
                    self.winning_three = [x,y,x]
                    return True
        
        if not self.get_possible_moves():
            self.winning_three = ['','','']
            self.winner = '0'
            return True

        return False

    def get_score(self):
        if self.winner == '0': #draw
            return 0
        elif self.winner == '1': #computer win
            return 1
        elif self.winner == '2': #opponent win
            return -1


    def set_first(self):
        if self.total_moves % 2 == 0:
            self.first = '1'
            self.second = '2'
        else:
            self.first = '2'
            self.second = '1'

    def box_dict(self):
        d = {}
        for x in xrange(0,9):
            d['box_%s' % x] = getattr(self,'box_%s' % x)
        return d





