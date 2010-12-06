import random

COMPUTER = 'x'
HUMAN = 'o'

class Board(object):
    def __init__(self):
        self.b = range(9)
        self.pairs = [
            (0, 1), (3, 1), (6, 1), # rows
            (0, 3), (1, 3), (2, 3), # columns
            (0, 4), (2, 2)]         # diagonals

    def draw_board(self):
        for i in range(9):
            if i % 3 == 0: print
            print self.b[i],
        print

    def winner(self):
        for start, incr in self.pairs:
            if self.b[start] == self.b[start+incr] == self.b[start+2*incr]:
                return self.b[start]
        return None

    def valid_moves(self):
        return [x for x in self.b if type(x) == int]

    def make_move(self, move, player):
        self.b[move] = player

    def undo_move(self, move):
        self.b[move] = move

    def game_over(self):
        return self.winner() or not self.valid_moves()


class TicTacToe(object):
    def __init__(self):
        self.players = [(self.computer, 'Computer'), (self.human, 'Human')]
        self.b = Board()

    def __judge(self, winner):
        if winner == COMPUTER:
            return 1
        if winner == None:
            return 0
        return -1

    def __evaluate_move(self, move, p):
        opponents = {HUMAN: COMPUTER, COMPUTER: HUMAN}
        try:
            self.b.make_move(move, p)
            if self.b.game_over():
                return self.__judge(self.b.winner())
            outcomes = (self.__evaluate_move(move, opponents[p]) for move in self.b.valid_moves())

            if p == COMPUTER:
                min_element = 1
                for o in outcomes:
                    if o == -1:
                        return o
                    min_element = min(o, min_element)
                return min_element
            else:
                max_element = -1
                for o in outcomes:
                    if o == 1:
                        return o
                    max_element = max(o, max_element)
                return max_element
        finally:
            self.b.undo_move(move)

    def human(self):
        while 1:
            print 'Enter your move %r:' % self.b.valid_moves(),
            inp = raw_input()
            choice = int(inp)
            if choice in self.b.valid_moves():
                break
        self.b.make_move(choice, HUMAN)

    def computer(self):
        moves = [(move, self.__evaluate_move(move, COMPUTER)) for move in self.b.valid_moves()]
        print moves
        random.shuffle(moves)   # don't want the computer to play the same game everytime
        moves.sort(key=lambda (move, winner): winner)
        print "Computer's move:", moves[-1][0]
        self.b.make_move(moves[-1][0], COMPUTER)

    def run(self):
        # current player
        player = 1  # 0 for computer and 1 for human
        self.b.draw_board()
        while 1:
            self.players[player][0]()
            self.b.draw_board()
            if self.b.winner():
                print '%s player wins!' % self.players[player][1]
                break
            if self.b.game_over():
                print "Game over."
                break
            player = (player+1) % 2


if __name__ == '__main__':
    ttt = TicTacToe()
    ttt.run()
