import unittest
import logic
import copy
import random

class TestGame(unittest.TestCase):
    """
    This test tests the game object to ensure that win checking works and 
    row values are working.
    """
    def test_row_ranges(self):
        p = lambda *args, **kwargs: None
        g = logic.Game(None, p, p)
        assert(g.ranges == {0: [(0, 0), (1, 0), (2, 0)],
                                       1: [(0, 1), (1, 1), (2, 1)], 
                                       2: [(0, 2), (1, 2), (2, 2)], 
                                       3: [(0, 0), (0, 1), (0, 2)], 
                                       4: [(1, 0), (1, 1), (1, 2)], 
                                       5: [(2, 0), (2, 1), (2, 2)], 
                                       6: [(0, 0), (1, 1), (2, 2)], 
                                       7: [(2, 0), (1, 1), (0, 2)]})
    def test_win_check(self):
        b = logic.Board()
        cells = [['X', 'X', 'X'],
                   ['O', 'O', None],
                   ['O', None, None]
                ]
        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                b.set_val(x, y, cell)

        p = lambda *args, **kwargs: None
        g = logic.Game(b, p, p)
        assert(g.check_for_win() == (0, 'X'))

        b.set_val(1, 0, None)
        assert(g.check_for_win() == False)

        #vertical row
        b.set_val(0, 0, 'O')
        assert(g.check_for_win() == (3, 'O'))

        #diagonal
        b.set_val(2, 2, 'O')
        b.set_val(0, 2, None)
        assert(g.check_for_win() == (6, 'O'))

        #no win again
        b.set_val(1, 1, None)
        assert(g.check_for_win() == False)

class TransformTest(unittest.TestCase):
    """
    This test tests rotating a board and ensures that all cells end up as they should.
    """
    def test_board_transform(self):
        board = logic.Board(cells = [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        new_board = logic.rotate(board)
        assert(new_board._cells == [[7, 4, 1], [8, 5, 2], [9, 6, 3]])

    def test_cell_transform(self):
        assert(logic.rotate_cell((0, 0)) == (2, 0))
        assert(logic.rotate_cell((1, 1)) == (1, 1))
        assert(logic.rotate_cell((0, 2)) == (0, 0))


class ComputerTest(unittest.TestCase):
    """
    This test tests all permutations of any possible games based on the computer's move to ensure
    that the computer never loses.
    """
    def game_permutation(self, game, move):
        newgame = copy.deepcopy(game)
        newgame.board.set_val(*move)
        return newgame

    def test_computer_us_first(self):
        #for random_seed in range(1, 60):
            count = 0
            random_seed = 1
            games_to_test = []
            board = logic.Board()
            g = logic.Game(board, logic.Player, logic.Computer)

            for move in board.get_valid_moves():
                games_to_test.append(self.game_permutation(g, (move[0], move[1], 'X')))
            while games_to_test:
                g = games_to_test.pop()
                #check for us winning

                if not g.board.get_valid_moves():
                    #tie
                    continue

                assert(g.check_for_win() != 'X')
                #set the same seed so the computer will always choose the same random.choice moves
                random.seed(random_seed)
                cm = g.p2.get_move()
                g.board.set_val(cm[0], cm[1], 'O')
                win = g.check_for_win()
                assert(win != 'X')
                if win: continue
                for move in g.board.get_valid_moves():
                    games_to_test.append(self.game_permutation(g, (move[0], move[1], 'X')))

    def test_computer_first(self):
        #for random_seed in range(1,60):
            random_seed = 1
            board = logic.Board()
            g = logic.Game(board, logic.Computer, logic.Player)
            random.seed(1)
            cm = g.p1.get_move()
            g.board.set_val(cm[0], cm[1], 'X')
            games_to_test = []
            for move in g.board.get_valid_moves():
                games_to_test.append(self.game_permutation(g, (move[0], move[1], 'O')))

            while games_to_test:
                g = games_to_test.pop()
                if not g.board.get_valid_moves():
                    #tie
                    continue
                assert(g.check_for_win() != 'O')
                #set the same seed so the computer will always choose the same random.choice moves
                random.seed(random_seed)
                cm = g.p1.get_move()
                g.board.set_val(cm[0], cm[1], 'X')
                win = g.check_for_win()
                assert(win != 'O')
                if win: 
                    continue
                for move in g.board.get_valid_moves():
                    games_to_test.append(self.game_permutation(g, (move[0], move[1], 'O')))
        
if __name__ == '__main__':
        unittest.main()
