import board
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
    from board import X ,O, STALEMATE, EMPTY as E
    b = board.Board()
    b._spaces = [[E,E,E],
                 [E,E,E],
                 [E,E,E]]
    assert b.check_win() is None

    b._spaces = [[X,E,E],
                 [X,E,E],
                 [X,E,E]]
    assert b.check_win() is X

    b._spaces = [[O,O,O],
                 [E,E,E],
                 [E,E,E]]
    assert b.check_win() is O

    b._spaces = [[O,E,O],
                 [E,O,E],
                 [E,E,O]]
    assert b.check_win() is O

    b._spaces = [[O,X,O],
                 [X,X,O],
                 [O,O,X]]
    assert b.check_win() is STALEMATE




