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

def game_winners():

    # Win by row
    b = Board()
    b.board[0][0].player = b.P1
    b.board[0][1].player = b.P1
    b.board[0][2].player = b.P1
    assert b.player_won(b.P1) == True

    # win by column
    b = Board()
    b.board[0][0].player = b.P1
    b.board[1][0].player = b.P1
    b.board[2][0].player = b.P1
    assert b.player_won(b.P1) == True

    # win by diagonal left-to-right
    b = Board()
    b.board[0][0].player = b.P1
    b.board[1][1].player = b.P1
    b.board[2][2].player = b.P1
    assert b.player_won(b.P1) == True

    # win by diagonal right-to-left
    b = Board()
    b.board[0][2].player = b.P1
    b.board[1][1].player = b.P1
    b.board[2][0].player = b.P1
    assert b.player_won(b.P1) == True

    # Player 0 (Draw) Score board
    assert b.score_board[b.P0] == 0
    b.score_board[b.P0] += 1
    assert b.score_board[b.P0] == 1

    # Player 1 Score board
    assert b.score_board[b.P1] == 0
    b.score_board[b.P1] += 1
    assert b.score_board[b.P1] == 1

    # Player 2 Score board
    assert b.score_board[b.P2] == 0
    b.score_board[b.P2] += 1
    assert b.score_board[b.P2] == 1

def tests():
    """Tests for the Board class"""
    # test that a new board is rational
    new_space()
    new_board()
    board_positions()
    game_winners()

    print "All Board tests have passed!"

if __name__ == '__main__':
    tests()