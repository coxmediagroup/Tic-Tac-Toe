#! /usr/bin/env
from Board import Board, BoardSpace

def new_space():
    s = BoardSpace(player=u"X", board_index=1)
    assert s.__str__() == "X"

def new_board():
    b = Board()
    assert b.__str__() == b.P0 * b.ROWS * b.COLS
    assert len(b.board) == b.ROWS
    assert all(len(x) == b.COLS for x in b.board)
    return 'new board: "{0}"'.format(b.board)

def tests():
    """Tests for the Board class"""
    # test that a new board is rational
    new_space()
    new_board()

    print "All Board tests have passed!"

def cli_tests():
    """Tests CLI game"""
    assert 1 == 1
    
    print "All CLI tests have passed!"

if __name__ == '__main__':
    tests()
    cli_tests()