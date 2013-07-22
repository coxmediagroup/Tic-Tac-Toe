import board
from board import X ,O, STALEMATE
def test_rows_cols_diags():
    b = board.Board()
    b._spaces = [[1,2,3],
                 [4,5,6],
                 [7,8,9]]

    l = list(b.rows_cols_diags())
    assert l == [(1, 2, 3), (4, 5, 6), (7, 8, 9),
                 (1, 4, 7), (2, 5, 8), (3, 6, 9),
                      (1, 5, 9), (7, 5, 3)], str(l)

def test_win():
    b = board.Board()
    assert b.check_win() is None

    b._spaces = [[X,2,3],
                 [X,5,6],
                 [X,8,9]]
    assert b.check_win() is X

    b._spaces = [[O,O,O],
                 [4,5,6],
                 [7,8,9]]
    assert b.check_win() is O

    b._spaces = [[O,2,X],
                 [4,O,6],
                 [X,8,O]]
    assert b.check_win() is O

    b._spaces = [[O,X,O],
                 [X,X,O],
                 [O,O,X]]
    assert b.check_win() is STALEMATE

def test_str():
    b = board.Board()
    b._spaces = [[O,X,O],
                 [X,5,O],
                 [O,O,X]]
    assert str(b) == '\n  0   1   2\n0 O | X | O\n -----------\n1 X | 5 | O\n-----------\n2 O | O | X\n'

    print repr(b)

def test_move():
    b = board.Board()
    b.move(X, 0, 0)
    assert b._spaces == [[X,2,3],
                         [4,5,6],
                         [7,8,9]], str(b._spaces)






