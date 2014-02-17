import random
import unittest

from app.ttt import *


O_MOVES = ((0, 0b000000000000000010), (1, 0b000000000000001000), 
           (2, 0b000000000000100000), (3, 0b000000000010000000), 
           (4, 0b000000001000000000), (5, 0b000000100000000000),
           (6, 0b000010000000000000), (7, 0b001000000000000000), 
           (8, 0b100000000000000000))

X_MOVES = ((0, 0b000000000000000011), (1, 0b000000000000001100), 
           (2, 0b000000000000110000), (3, 0b000000000011000000), 
           (4, 0b000000001100000000), (5, 0b000000110000000000),
           (6, 0b000011000000000000), (7, 0b001100000000000000), 
           (8, 0b110000000000000000))

WINNING_MOVES = (0b010101000000000000, 0b010000000100000001,
                 0b010000000000010100, 0b000100000001000001,
                 0b000001010100000000, 0b000001000000010001,
                 0b000000010000000101, 0b000000000101010000)


class TicTacToeBoardTests(unittest.TestCase):
    # Testing done in binary as a second check to hex calculations in main class
    
    def generate_board(self, empty_squares):
        """
        A helper method to randomly generate a game board.
        
        :param empty_squares: list of squares that should not have an 'X' or 'O'
        """
        board = 0
        for i in range(8, -1, -1):
            match = not (i in empty_squares)
            new_square = (int(match) << 1) + (random.randint(0, 1) 
                                              if match else 0)
            board = (board << 2) + new_square
        return board
    
    def insert_random_moves(self, winning_board, winning_player, pieces=2):
        """
        Helper method to insert random pieces into an existing game board.
        The game board should consist of one of the 'WINNING_MOVES' boards 
        above, and the winning player should be the one that has won the game.
        
        Note: do not include more pieces than there are empty slots on the 
            board.
        
        :param winning_board: an integer from WINNING_MOVES
        :param winning_player: integer representing the player, either 1 or 2
        :param pieces: number of random pieces to insert for the losing. Note 
            that inserting more than 2 pieces may result in a board where the
            losing player actually wins
        :return: integer
        """
        if not pieces:
            return winning_board
        
        # WINNING_MOVES has values for Player 1. We need to update them to
        # Player 2 if that player was specified
        if winning_player == 2:
            for i in range(0, 18, 2):
                mask = 2 << i
                if mask & winning_board:
                    winning_board = winning_board | (1 << i)
            
        # this isn't intended to be a smart algorithm; simply a quick-and-dirty
        # one for testing purposes to get as random as possible
        losing_player = ~winning_player & 0b11
        while pieces:
            for i in range(0, 18, 2):
                mask = 2 << i
                if not mask & winning_board:
                    winning_board = winning_board | (losing_player << i)
                    pieces -= 1
                    if not pieces:
                        return winning_board

    def test__init(self):
        # defaults
        ttt = TicTacToeBoard()
        for attr in ('board', 'turn', 'player_wins', 'player_losses', 'ties'):
            self.assertEquals(0, getattr(ttt, attr))
    
    def test__board_for_player(self):
        self.assertTrue(False, "Not Implemented")
    
    def test__convert_move(self):
        ttt = TicTacToeBoard()
        # testing for O
        for move, expected in O_MOVES:
            self.assertEquals(expected, ttt._convert_move(move))
        
        # testing for X
        ttt.turn = 1
        for move, expected in X_MOVES:
            self.assertEquals(expected, ttt._convert_move(move))
            
        # should return None for integers 0 <= move <= 8
        for move in (-2, -1, 9, 10):
            self.assertIsNone(ttt._convert_move(move))
        
        # should return None for moves that can't be converted to integers
        for move in ('a', None, {}):
            self.assertIsNone(ttt._convert_move(move))
    
    def test__has_won(self):
        ttt = TicTacToeBoard()
        
        # winning circumstances
        for player in (1, 2):
            for board in WINNING_MOVES:
                # winning circumstances
                ttt.board = self.insert_random_moves(board, player)
                self.assertTrue(ttt._has_won(player))
                
                # losing circumstances
                ttt.board = self.insert_random_moves(board, (~player & 0b11))
                self.assertFalse(ttt._has_won(player))
        
        # some tie boards
        for board in (0b101011101111101110, 0b111011111011101010,
                      0b111110111010111010, 0b101110101110111110):
            ttt.board = board
            for player in (1, 2):
                self.assertFalse(ttt._has_won(player))
        
        # incomplete games
        for board in (0b000000000000000000, 0b110010000000111010,
                      0b100000001110110010, 0b000011101100100010):
            ttt.board = board
            for player in (1, 2):
                self.assertFalse(ttt._has_won(player))

    def test__is_board_full(self):
        ttt = TicTacToeBoard()
        
        # a few random tests where board is full
        for i in range(9):
            ttt.board = self.generate_board([])
            self.assertTrue(ttt._is_board_full())
        
        # comprehensive, but not exhaustive non-full tests.
        # we'll run each non-full set of tests twice
        for trial in range(2):
            for empty in range(1, 9):
                open_squares = list(range(empty))
                empty_squares = []
                for sqr in range(empty):
                    square = random.choice(open_squares)
                    empty_squares.append(open_squares.pop(open_squares.index(square)))
                
                ttt.board = self.generate_board(empty_squares)
                self.assertFalse(ttt._is_board_full())
    
    def test__is_valid_move(self):
        ttt = TicTacToeBoard()
        
        # running an exhaustive test
        for empty_square in range(9):
            ttt.board = self.generate_board([empty_square])
            
            for moveset in (O_MOVES, X_MOVES):
                for square, move in moveset:
                    self.assertEquals((square == empty_square), 
                                      ttt._is_valid_move(move))
    
    def test__is_win(self):
        self.assertTrue(False, "Not Implemented")
    
    def test__set_turn(self):
        ttt = TicTacToeBoard()
        self.assertEquals(0, ttt.turn)
        
        # should alternate between 1 and 0
        for turn in (1, 0, 1, 0, 1, 0, 1, 0):
            ttt._set_turn()
            self.assertEquals(turn, ttt.turn)
            
    def test__set_win(self):
        self.assertTrue(False, "Not Implemented")
    
    def test_apply_move(self):
        ttt = TicTacToeBoard()
        self.assertEquals(0, ttt.board)
        self.assertEquals(0, ttt.turn)
        
        # empty board should always apply
        self.assertTrue(ttt.apply_move(3))
        self.assertEquals(0b000000000010000000, ttt.board)
        
        # some intermediate test cases
        ttt.turn = 1
        self.assertTrue(ttt.apply_move(5))
        self.assertEquals(0b000000110010000000, ttt.board)
        
        ttt.turn = 0
        self.assertFalse(ttt.apply_move(5))
        self.assertEquals(0b000000110010000000, ttt.board)
        self.assertTrue(ttt.apply_move(8))
        self.assertEquals(0b100000110010000000, ttt.board)
        
        # full board should never apply
        ttt.board = 0b101011101110101111
        for turn in (0, 1):
            ttt.turn = turn
            for move in range(9):
                self.assertFalse(ttt.apply_move(move))
                self.assertEquals(0b101011101110101111, ttt.board)
    
    def test_game_over_validation(self):
        ttt = TicTacToeBoard()
        
        # player won (shouldn't happen, but we should detect if it does)
        ttt.board = 0b101110111000110010
        self.assertEquals((True, 1), ttt.game_over_validation())
        
        # computer won
        ttt.board = 0b101011101111110010
        self.assertEquals((True, 2), ttt.game_over_validation())
        
        # tie
        ttt.board = 0b101011101111101110
        self.assertEquals((True, None), ttt.game_over_validation())
        
        # game is still going
        ttt.board = 0b111011001000000010
        self.assertEquals((False, None), ttt.game_over_validation())
    
    def test_is_computer_turn(self):
        ttt = TicTacToeBoard()
        for turn in (0, 1):
            ttt.turn = turn
            self.assertEquals(bool(turn), ttt.is_computer_turn())

