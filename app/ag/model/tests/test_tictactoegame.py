from mock import Mock, MagicMock, patch

from app.ag.model.tictactoegame import TicTacToeGame


###########################
# TEST TIC TAC TOE GAME   #
###########################

class test_tic_tac_toe(object):

    def setup(self):
        self.game = TicTacToeGame()

    def test_take_a_turn_results_in_tie(self):
        board = [' ', 'X', 'X', 'O', 'O', 'X', 'X', 'X ', 'O', 'O']
        turn = self.game.take_a_turn(board)

        print 'turn: {0}'.format(turn)

        assert turn.get('outcome_code') == TicTacToeGame.CODE_YOU_TIE

    def test_take_a_turn_results_in_win(self):
        board = [' ', 'X', 'X', 'O', 'O', 'X', 'X', 'O ', 'X', 'O']
        turn = self.game.take_a_turn(board)

        print 'turn: {0}'.format(turn)

        assert turn.get('outcome_code') == TicTacToeGame.CODE_YOU_WIN

    def test_take_a_turn_results_in_loss(self):
        board = [' ', 'X', 'X', 'O', ' ', ' ', ' ', 'O', ' ', ' ']
        turn = self.game.take_a_turn(board)

        print 'turn: {0}'.format(turn)

        assert turn.get('outcome_code') == TicTacToeGame.CODE_YOU_LOSE
