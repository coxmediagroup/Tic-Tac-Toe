from unittest import TestCase
from board import Board
from player import AIPlayer

class AIPlayerTests(TestCase):
    ''' Tests for the computer AI player '''

    def _game_over(self, board):
        if(board.draw()):
            return True

        winner = board.winner()
        if(winner is not None):
            self.assertTrue(winner == board.X) # Only the AI should ever win
            return True

        return False

    def _test_all_moves(self, board, player):
        # Try each possible move
        for move in board.open_moves():
            # Try a move, then let the AI go again
            new_board = Board(board.x_first)
            new_board._state = board._state
            new_board.move(move, not player.player)
            if(self._game_over(new_board)):
                continue
            new_player = AIPlayer(player.player, new_board)
            new_player.next_move()
            if(self._game_over(new_board)):
                continue
            self._test_all_moves(new_board, new_player)

    def test_move_first(self):
        ''' Make sure the AI cannot lose when it goes first by testing all
            possible game combinations. '''
        board = Board()
        player = AIPlayer(True, board)
        # Let the AI go first
        player.next_move()
        self._test_all_moves(board, player)

    def test_move_second(self):
        ''' Make sure the AI cannot lose when it goes second by testing all
            possible game combinations. '''
        board = Board(False) # O goes first
        player = AIPlayer(False, board)
        self._test_all_moves(board, player)


