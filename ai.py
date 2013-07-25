from board import empty, X, O

def first_free_space(spaces):
    return (c for c in spaces if empty(c)).next()

def index_of_max_value(iterable):
    return iterable.index(max(iterable))

class Player(object):
    """docstring for Player"""
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol

    def move(self, board):
        s = self.select_move(board)
        print "Player %s is playing at (%s)" %(self.player_symbol, s)
        board[s] = self.player_symbol

class ComputerPlayer(Player):

    def _find_win(self, board, me, you):
        """Find a line that is a possible one move win for 'me'"""
        for rcd in board.rows_cols_diags():
            if rcd.count(me) == 2 and rcd.count(you)==0:
                return first_free_space(rcd) #Get first free spot
        return None

    def _find_fork(self, board, me, you):
        """
        Find lines with one of my marks and no others
        select a space with the maximum overlap of said lines
        """
        count = [None, 0,0,0, 0,0,0, 0,0,0]
        for rcd in board.rows_cols_diags():
            if rcd.count(me) == 1 and rcd.count(you)==0:
                for c in rcd:
                    if c not in (X,O):
                        count[c] += 1
        max_index = index_of_max_value(count)
        if count[max_index] > 1:
            return max_index
        else:
            return None

    def _setup_win(self, board, me, you):
        """Make 2 in a row"""
        for rcd in board.rows_cols_diags():
            if rcd.count(me) == 1 and rcd.count(you)==0:
                return first_free_space(rcd) #Get first free spot

    def _opposite_corner(self, board, me, you):
        if board[1] is you and empty(board[9]):
            return 9
        if board[9] is you and empty(board[1]):
            return 1
        if board[3] is you and empty(board[7]):
            return 7
        if board[7] is you and empty(board[3]):
            return 3
        return None


    def select_move(self, board):
        """
        Implements http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy

        """

        print "%s is pondering...." % self.player_symbol

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

        #Block Opponents Fork
        print "Considering blocking a fork..."
        move = self._find_fork(board, you, me)
        if move:
            print "moving at %s" % move
            return move

        #Setup Win
        print "Considering setting up a Win..."
        move = self._setup_win(board, me, you)
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














