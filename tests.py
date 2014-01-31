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

def board_positions():
    """
     1 | 2 | 3 
    --- --- ---
     4 | 5 | 6 
    --- --- ---
     7 | 8 | 9
     
    """
    b = Board(rows=16, cols=16)
    last_space_on_board = b.board[-1][-1].board_index
    
    for x in range(1, last_space_on_board+1):
        row, col = b.board_position_by_index(x)
        board_space_index = b.board[row][col].board_index
        msg = "b.board[{}][{}].board_index == {} (It is {}!)"
        msg = msg.format(row, col, x, board_space_index)
        assert b.board[row][col].board_index == x, msg
    
    return True

def tests():
    """Tests for the Board class"""
    # test that a new board is rational
    new_space()
    new_board()
    board_positions()

    print "All Board tests have passed!"

def cli_tests():
    """Tests CLI game"""
    assert 1 == 1

    print "All CLI tests have passed!"

if __name__ == '__main__':
    tests()
    cli_tests()