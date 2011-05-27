import unittest
import logic


class TestGame(unittest.TestCase):
    def test_row_ranges(self):
        g = logic.Game(None, None, None)
        assert(g._ranges == {0: [(0, 0), (1, 0), (2, 0)],
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

        g = logic.Game(b, None, None)
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

if __name__ == '__main__':
        unittest.main()
