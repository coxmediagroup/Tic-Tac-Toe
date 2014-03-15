
class KeyboardInputPlayer(object):
    def __init__(self, player, board):
        self.player = player
        self.board = board

    def next_move(self):
        ''' Take the next move from standard input.  Continue until a move
            has been successfully made. '''
        while True:
            value = raw_input('Your move: ')

            if((value == '?') or (value.lower() == 'help')):
                # TODO: Display move grid
                pass

            try:
                pos = int(value)
            except ValueError:
                print('Invalid move.  Please try again')
            else:
                try:
                    self.board.move(pos, self.player)
                except Board.InvalidMove as e:
                    print(str(e))
                else:
                    break


class AIPlayer(object):
    def __init__(self, player, board):
        self.player = player
        self.board = board

    def next_move(self):
        return self._find_move(self.player)

    def _find_move(self, player):
        ''' A simple negamax implementation for finding a reasonable next move.
        '''
        score = None
        move = None
        
        for test_move in self.board.open_moves():
            self.board.move(test_move, player)
            
            if(self.board.winner() is not None):
                test_score = self._calc_score() # TODO: Negatives
            else:
                test_move, test_score = self._find_move(not player)

            self.board.undo()
            
            if((score == None) or (test_score > score)): # TODO: Sign
                score = test_score
                move = test_move

        return move, score

    def _calc_score(self):
        ''' Very crude move scoring.  Adequate for the AI to not lose, but if
            a smarter AI is desired this is where the improvement is needed. '''
        if(self.board.winner()):
            return 10
        return 0

