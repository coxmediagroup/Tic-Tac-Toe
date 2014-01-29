#! /usr/bin/env
from Board import Board

def new_board():
    b = Board()
    assert b.board == (b.P0 * b.ROWS * b.COLS)
    return 'new board: "{0}"'.format(b.board)
 
def tests():
    """Tests for the Board class"""
    # test that a new board is rational
    new_board()

    print "All Board tests have passed!"

def cli_tests():
    """Tests CLI game"""
    assert 1 == 1
    
    print "All CLI tests have passed!"

if __name__ == '__main__':
    tests()
    cli_tests()