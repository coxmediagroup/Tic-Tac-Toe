
class TicTacToe(object):

    def __init__(self):
        self.moves = []
        self.board = [None for x in range(0, 9)]
        self.turn = 0

    def run(self, human, computer):

        print_game_state(t3)

        pass

class Player(object):
    def __init__(self, mark, *args, **kwargs):
        self.mark = mark

    def move(self, game):
        pass

class Human(Player):
    def __init__(self, *args, **kwargs):
        super(Human, self).__init__('O', *args, **kwargs)

class Computer(Player):
    def __init__(self, *args, **kwargs):
        super(Computer, self).__init__('X', *args, **kwargs)

def print_game_state(game):
    board = game.board

    print "\n"
    print "+----------------+"
    print "|---- TURN {0} ----|".format(game.turn)
    print "+----------------+"

    print "  +-----------+"
    for i in range(0, 9, 3): # 0-9 by 3s
        print '  |',
        for j in range(3):
            if not board[j + i]:
                print "{0} |".format(j+i),
            else:
                print "%s |" % board[j+i],
        print "\n",
    print "  +-----------+"


if __name__ == '__main__':
    t3 = TicTacToe()
    human = Human()
    computer = Computer()
    t3.run(human, computer)

