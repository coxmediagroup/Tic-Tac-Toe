import unittest
from src.tic_tac_toe import Game, TurnOutOfOrderError, IllegalMoveError

class GameTests(unittest.TestCase):
    def test_valid_plays_are_1_thru_9(self):
        game = Game()
        self.assertRaises(IllegalMoveError, game.do_turn, 1, 10)
        self.assertRaises(IllegalMoveError, game.do_turn, 1, -1)

    def test_turns_must_arrive_in_order(self):
        game = Game()
        game.do_turn(1, 1)
        self.assertRaises(TurnOutOfOrderError, game.do_turn, 3, 1)

    def test_player_cannot_play_in_occupied_squre(self):
        game = Game()
        game.do_turn(1, 1)
        self.assertRaises(IllegalMoveError, game.do_turn, 2, 1)
        

if __name__ == '__main__':
    unittest.main()
