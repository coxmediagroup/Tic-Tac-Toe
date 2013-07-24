from board import X, O

def first_free_space(spaces):
    return (c for c in spaces if (c not in (X,O))).next()

def index_of_max_value(iterable):
    return iterable.index(max(iterable))

class Player(object):
    """docstring for Player"""
    input_map = {
                    "1":(0,0), "2":(0,1), "3":(0,2),
                    "4":(1,0), "5":(1,1), "6":(1,2),
                    "7":(2,0), "8":(2,1), "9":(2,2),
                }
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol

    def move(self, board):
        s = self.select_move(board)
        r,c = self.input_map[str(s)]
        print "Player %s is playing at (%s,%s)" %(self.player_symbol, r, c)
        board.move(self.player_symbol, r, c)

class ComputerPlayer(Player):

    opposing_corners= {1:9, 3:7, 7:3, 9:1}

    def _find_win(self, board, me, you):
        """Find a line that is a possible one move win for 'me'"""
        for rcd in board.rows_cols_diags():
            if rcd.count(me) == 2 and rcd.count(you)==0:
                return first_free_space(rcd) #Get first free spot
        return None

    def _find_fork(self, board, me, you):
        count = [None, 0,0,0, 0,0,0, 0,0,0]
        for rcd in board.rows_cols_diags():
            if rcd.count(me) == 1 and rcd.count(you)==0:
                for c in rcd:
                    if c not in (X,O):
                        count[c] += 1
        max_index = index_of_max_value(count)
        if max_index > 1:
            return max_index
        else:
            return None

    def _setup_win(self, board, me, you):
        for rcd in board.rows_cols_diags():
            if rcd.count(me) == 1 and rcd.count(you)==0:
                return first_free_space(rcd) #Get first free spot

    def _opposite_corner(self, board, me, you):
        if board._spaces[0][0] is you and board._spaces[2][2] not in (X,O):
            return 9
        if board._spaces[2][2] is you and board._spaces[0][0] not in (X,O):
            return 1
        if board._spaces[0][2] is you and board._spaces[2][0] not in (X,O):
            return 7
        if board._spaces[2][0] is you and board._spaces[0][2] not in (X,O):
            return 3
        return None


    def select_move(self, board):
        """
        Implements http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy

        """

        print "pondering...."

        me = self.player_symbol
        you = X if self.player_symbol is O else O

        #Find Win for me
        print "Considering winning..."
        move = self._find_win(board, me, you)
        if move:
            print "moving at %s" % move
            return move

        #Block Win For You
        print "Considering blocking..."
        move = self._find_win(board, you, me)
        if move:
            print "moving at %s" % move
            return move

        #Make fork
        print "Considering forking..."
        move = self._find_fork(board, me, you)
        if move:
            print "moving at %s" % move
            return move

        #Setup Win
        print "Considering setting up a Win..."
        move = self._setup_win(board, me, you)
        if move:
            print "moving at %s" % move
            return move

        #Block Opponents Fork
        print "Considering blocking a fork..."
        move = self._find_fork(board, you, me)
        if move:
            print "moving at %s" % move
            return move

        #Take Center
        print "Considering taking the center..."
        if board._spaces[1][1] == 5:
            print "moving at 5"
            return 5

        #Take Opposite Corner
        print "Considering taking opposite corner..."
        move = self._opposite_corner(board, me, you)
        if move:
            print "moving at %s" % move
            return move

        #Take ANY corner
        print "Considering taking any corner..."
        available_corners = [c for c in board.cells() if c in (1,3,7,9)]
        if available_corners:
            move = available_corners[0]
            print "moving at %s" % move
            return move

        #Take an edge
        print "Considering taking an edge corner..."
        available_edge = [c for c in board.cells() if c in (2,4,6,8)]
        if available_edge:
            move = available_edge[0]
            print "moving at %s" % move
            return move














