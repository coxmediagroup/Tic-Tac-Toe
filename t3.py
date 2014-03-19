"""
Tic Tac Toe

Implements the minmax algorithm to solve the tic tac toe problem.
"""

class TicTacToe(object):

    def __init__(self, human, computer):
        self.moves = []
        self.board = [None for x in range(0, 9)]
        self.turn = 0

        self.human = human
        self.computer = computer
        self.winner = None

    def run(self):

        # Play through 9 turns or until a win is found
        for turn in range(9):
            self.turn = turn
            print_game_state(self)

            # Take a turn
            if not turn % 2:
                human.move(self)
            else:
                computer.move(self)

            if self.game_was_won():
                print_game_state(self)
                if not self.winner:
                    print "\nIt's a tie!"
                else:
                    print "\nThe {0} won".format(self.winner.name)
                return

    def set_owner(self, player, cell):
        self.board[cell] = player
        self.moves.append(cell)

    def game_was_won(self):
        #                  ROWS     COLS     DIAGS
        winning_combos = [(0,1,2), (0,3,6), (0,4,8),
                          (3,4,5), (1,4,7), (2,4,6),
                          (6,7,8), (2,5,8),]
        board = self.board
        for i, j, k in winning_combos:
            if board[i] == board[j] == board[k] and board[i]:
                self.winner = board[i]
                return True
            if None not in self.board:
                self.winner = None
                return True
        return False

    def set_winner(self, winner):
        self.winner = winner

    def get_empty_cells(self):
        return [i for i, v in enumerate(self.board) if not v]

    def reset_one(self):
        self.board[self.moves.pop()] = None
        self.winner = None

class Player(object):
    name = ""

    def __init__(self, mark, *args, **kwargs):
        self.mark = mark

    def __str__(self):
        return self.name

    def move(self, game):
        pass

class Human(Player):
    name = "human"

    def __init__(self, *args, **kwargs):
        super(Human, self).__init__('O', *args, **kwargs)

    def move(self, game):
        print "Human is moving..."
        cell = int(raw_input("Choose a cell (0-8):"))
        game.set_owner(self, cell)

class Computer(Player):
    name = "computer"

    def __init__(self, *args, **kwargs):
        super(Computer, self).__init__('X', *args, **kwargs)

    def move(self, game):
        print "Computer is moving..."

        # Apply the minmax algorithm
        cell, score = self._maximize(game)
        game.set_owner(self, cell)

    def _maximize(self, game):
        maxscore = None
        maxmove = None

        for cell in game.get_empty_cells():
            game.set_owner(self, cell)

            if game.game_was_won():
                score = self._get_score(game)
            else:
                move, score = self._minimize(game)

            game.reset_one()

            if maxscore == None or score > maxscore:
                maxscore = score
                maxmove = cell

        return maxmove, maxscore

    def _minimize(self, game):
        minscore = None
        minmove = None

        for cell in game.get_empty_cells():
            game.set_owner(game.human, cell)

            if game.game_was_won():
                score = self._get_score(game)
            else:
                move, score = self._maximize(game)

            game.reset_one()

            if minscore == None or score < minscore:
                minscore = score
                minmove = cell

        return minmove, minscore

    def _get_score(self, game):
        """ Return 1 if win, -1 if lost, and 0 for no change """
        if game.game_was_won():
            if game.winner == self:
                return 1
            elif isinstance(game.winner, Human):
                return -1
        return 0



def print_game_state(game):
    board = game.board

    print "\n"
    print "+----------------+"
    print "|---- TURN {0} ----|".format(game.turn + 1)
    print "+----------------+"

    print "  +-----------+"
    for i in range(0, 9, 3): # 0-9 by 3s
        print '  |',
        for j in range(3):
            if not board[j + i]:
                print "{0} |".format(j+i),
            else:
                print "%s |" % board[j+i].mark,
        print "\n",
    print "  +-----------+"


if __name__ == '__main__':
    human = Human()
    computer = Computer()
    t3 = TicTacToe(human, computer)
    t3.run()

