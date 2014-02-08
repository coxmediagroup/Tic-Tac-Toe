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
    assert b.player_win_round(b.P1) == True

    # win by column
    b = Board()
    b.board[0][0].player = b.P1
    b.board[1][0].player = b.P1
    b.board[2][0].player = b.P1
    assert b.player_win_round(b.P1) == True

    # win by diagonal left-to-right
    b = Board()
    b.board[0][0].player = b.P1
    b.board[1][1].player = b.P1
    b.board[2][2].player = b.P1
    assert b.player_win_round(b.P1) == True

    # win by diagonal right-to-left
    b = Board()
    b.board[0][2].player = b.P1
    b.board[1][1].player = b.P1
    b.board[2][0].player = b.P1
    assert b.player_win_round(b.P1) == True

    # Draw
    b = Board()
    assert len(b.remaining_spaces()) == 9
    b.board[0][0].player = b.P1
    assert len(b.remaining_spaces()) == 8
    b.board[0][1].player = b.P1
    assert len(b.remaining_spaces()) == 7
    b.board[0][2].player = b.P1
    assert len(b.remaining_spaces()) == 6
    b.board[1][0].player = b.P1
    assert len(b.remaining_spaces()) == 5
    b.board[1][1].player = b.P1
    assert len(b.remaining_spaces()) == 4
    b.board[1][2].player = b.P1
    assert len(b.remaining_spaces()) == 3
    b.board[2][0].player = b.P1
    assert len(b.remaining_spaces()) == 2
    b.board[2][1].player = b.P1
    assert len(b.remaining_spaces()) == 1
    b.board[2][2].player = b.P1
    assert len(b.remaining_spaces()) == 0

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

def ai():
    
    # AI should place player on board
    b = Board()
    b.this_player = b.P1
    b.next_player = b.P2
    
    # empty board has 9 spaces
    assert len(b.remaining_spaces()) == 9
    
    # first move should have 8 spaces
    b.ai()
    assert len(b.remaining_spaces()) == 8
    
    # AI should place winning move
    b = Board()
    # OO-
    # XX-
    # O-X
    b.board[0][0].player = b.P2 #1
    b.board[0][1].player = b.P2 #2
    b.board[0][2].player = b.P0 #3
    b.board[1][0].player = b.P1 #4
    b.board[1][1].player = b.P1 #5
    b.board[1][2].player = b.P0 #6
    b.board[2][0].player = b.P2 #7
    b.board[2][1].player = b.P0 #8
    b.board[2][2].player = b.P1 #9
    
    b.this_player = b.P1
    b.next_player = b.P2
    b.ai()
    
    board_spots = 'OO-XXXO-X'
    msg = 'Winning Move for "{}" is "{}", not "{}"'
    assert b.__str__() == board_spots, msg.format(b.P1, board_spots, b)
    
    # AI should block winning move
    b = Board()
    # XX-
    # --O
    # --O
    b.board[0][0].player = b.P1 #1
    b.board[0][1].player = b.P1 #2
    b.board[0][2].player = b.P0 #3
    b.board[1][0].player = b.P0 #4
    b.board[1][1].player = b.P0 #5
    b.board[1][2].player = b.P2 #6
    b.board[2][0].player = b.P0 #7
    b.board[2][1].player = b.P0 #8
    b.board[2][2].player = b.P0 #9
    
    b.this_player = b.P2
    b.next_player = b.P1
    b.ai()
    
    board_spots = 'XXO--O---'
    msg = 'Blocking move for P2 is "{}", not "{}"'
    assert str(b) == board_spots, msg.format(board_spots, b)

    # NOT a win by diagonal right-to-left
    b = Board()
    # XOX
    # -X-
    # OXO
    b.board[0][0].player = b.P1 #1
    b.board[0][1].player = b.P2 #2
    b.board[0][2].player = b.P1 #3
    b.board[1][0].player = b.P0 #4
    b.board[1][1].player = b.P1 #5
    b.board[1][2].player = b.P0 #6
    b.board[2][0].player = b.P2 #7
    b.board[2][1].player = b.P1 #8
    b.board[2][2].player = b.P2 #9

    b.this_player = b.P2
    b.next_player = b.P1
    b.ai()
    # assert b.player_win_round(b.P2) == True
    msg = 'Board should be not be winnable: "{}"'
    assert b.winning_space() == False, msg.format(b)

def tests():
    """Tests for the Board class"""
    # test that a new board is rational
    new_space()
    new_board()
    board_positions()
    game_winners()
    ai()

    print "All tests have passed!"

if __name__ == '__main__':
    tests()