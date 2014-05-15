from board import Board

class KeyboardInputPlayer(object):
    ''' Tic-Tac-Toe player that accepts human input from a keyboard. '''

    def __init__(self, player, board):
        self.player = player
        self.board = board

    def next_move(self):
        ''' Take the next move from standard input.  Continue until a move
            has been successfully made. '''
        moved = False
        while not moved:
            value = raw_input('Your move: ')

            if((value == '?') or (value.lower() == 'help')):
                print(self.board.get_layout())
                continue

            try:
                pos = int(value) - 1
            except ValueError:
                print('Invalid move.  Please try again')
            else:
                try:
                    self.board.move(pos, self.player)
                except Board.InvalidMove as e:
                    print(str(e))
                else:
                    moved = True


SIGN = (-1, 1)

class AIPlayer(object):
    ''' Tic-Tac-Toe computer AI player. '''

    def __init__(self, player, board):
        self.player = player
        self.board = board

    def next_move(self):
        ''' Make the next move '''
        move, score = self._find_move(self.player)
        self.board.move(move, self.player)

    def _find_move(self, player):
        ''' A simple negamax implementation for finding a reasonable next move.
        '''
        score = None
        move = None
        me = (player == self.player)
        
        for test_move in self.board.open_moves():
            self.board.move(test_move, player)

            winner = self.board.winner()
            if((winner is not None) or self.board.draw()):
                test_score = self._calc_score(winner) * SIGN[me]
            else:
                unused, test_score = self._find_move(not player)

            self.board.undo()

            # Save off the move associated with the best (or worst) score
            if((score is None) or ((cmp(test_score, score) * SIGN[me]) > 0)):
                score = test_score
                move = test_move

        return move, score

    def _calc_score(self, winner):
        ''' Very crude move scoring.  Adequate for the AI to not lose, but if
            a smarter AI is desired this is where the improvement is needed. '''
        if(winner is not None):
            return 10
        return 0

