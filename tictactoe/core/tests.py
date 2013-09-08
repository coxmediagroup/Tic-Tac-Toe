from django.test import TestCase
from random import choice

from core.game import Game, COMPUTER, PLAYER, NO_RESULT

NUMBER_OF_GAMES = 100

class GameTest(TestCase):
    def test_game_result(self):
        '''
        This test will simulate n games between a computer and a human where 
        n is determing by the NUMBER_OF_GAMES settings and make sure that the computer never loses
        '''
        for i in xrange(NUMBER_OF_GAMES):
            board = [0] * 9
            game = Game(board)
            while True:
                available_moves = game.get_blank_boxes()
                # Make a random player move
                box = choice(available_moves)
                game.make_move(box, PLAYER)

                result, winning_combination = game.check_game_over()
                if result:
                    break

                # Make computer's move
                box = game.best_next_move(COMPUTER)
                game.make_move(box, COMPUTER)

                result, winning_combination = game.check_game_over()
                if result:
                    break

            self.assertIsNot(result, PLAYER)
        