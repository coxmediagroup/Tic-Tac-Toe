"""
Tests checking against the Board class

"""
from tic_tac_toe.board import Board, BoardSpace, MIN_DIM, MAX_DIM

def new_space():
    """Testing for a new space on board with player X"""
    board_space = BoardSpace(player=u"X", board_index=1)
    assert board_space.__str__() == "X"

def new_board():
    """Test making a new board"""
    board = Board()
    assert board.__str__() == board.player0 * board.rows * board.cols
    assert len(board.board) == board.rows
    assert all(len(x) == board.cols for x in board.board)
    return 'new board: "{0}"'.format(board.board)

def board_positions():
    """
    smallest board:

     1 | 2 | 3
    --- --- ---
     4 | 5 | 6
    --- --- ---
     7 | 8 | 9

    biggest board:

     1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13| 14| 15| 16
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
     17| 18| 19| 20| 21| 22| 23| 24| 25| 26| 27| 28| 29| 30| 31| 32
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
     33| 34| 35| 36| 37| 38| 39| 40| 41| 42| 43| 44| 45| 46| 47| 48
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
     49| 50| 51| 52| 53| 54| 55| 56| 57| 58| 59| 60| 61| 62| 63| 64
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
     65| 66| 67| 68| 69| 70| 71| 72| 73| 74| 75| 76| 77| 78| 79| 80
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
     81| 82| 83| 84| 85| 86| 87| 88| 89| 90| 91| 92| 93| 94| 95| 96
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
     97| 98| 99|100|101|102|103|104|105|106|107|108|109|110|111|112
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    113|114|115|116|117|118|119|120|121|122|123|124|125|126|127|128
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    129|130|131|132|133|134|135|136|137|138|139|140|141|142|143|144
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    145|146|147|148|149|150|151|152|153|154|155|156|157|158|159|160
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    161|162|163|164|165|166|167|168|169|170|171|172|173|174|175|176
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    177|178|179|180|181|182|183|184|185|186|187|188|189|190|191|192
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    193|194|195|196|197|198|199|200|201|202|203|204|205|206|207|208
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    209|210|211|212|213|214|215|216|217|218|219|220|221|222|223|224
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    225|226|227|228|229|230|231|232|233|234|235|236|237|238|239|240
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    241|242|243|244|245|246|247|248|249|250|251|252|253|254|255|256

    """

    for row_count in range(MIN_DIM, MAX_DIM+1):
        for col_count in range(MIN_DIM, MAX_DIM+1):
            board = Board(rows=row_count, cols=col_count)
            last_space_on_board = board.board[-1][-1].board_index

            for x_pos in range(1, last_space_on_board+1):
                row, col = board.board_position_by_index(x_pos)
                board_space_index = board.board[row][col].board_index
                msg = "board.board[{}][{}].board_index == {} (It is {}!)"
                msg = msg.format(row, col, x_pos, board_space_index)
                assert board.board[row][col].board_index == x_pos, msg

    return True

def game_winners():
    """Test game winners"""

    # Win by row
    board = Board()
    board.board[0][0].player = board.player1
    board.board[0][1].player = board.player1
    board.board[0][2].player = board.player1
    assert board.player_win_round(board.player1) == True

    # win by column
    board = Board()
    board.board[0][0].player = board.player1
    board.board[1][0].player = board.player1
    board.board[2][0].player = board.player1
    assert board.player_win_round(board.player1) == True

    # win by diagonal left-to-right
    board = Board()
    board.board[0][0].player = board.player1
    board.board[1][1].player = board.player1
    board.board[2][2].player = board.player1
    assert board.player_win_round(board.player1) == True

    # win by diagonal right-to-left
    board = Board()
    board.board[0][2].player = board.player1
    board.board[1][1].player = board.player1
    board.board[2][0].player = board.player1
    assert board.player_win_round(board.player1) == True

    # Draw
    board = Board()
    assert len(board.remaining_spaces()) == 9
    board.board[0][0].player = board.player1
    assert len(board.remaining_spaces()) == 8
    board.board[0][1].player = board.player1
    assert len(board.remaining_spaces()) == 7
    board.board[0][2].player = board.player1
    assert len(board.remaining_spaces()) == 6
    board.board[1][0].player = board.player1
    assert len(board.remaining_spaces()) == 5
    board.board[1][1].player = board.player1
    assert len(board.remaining_spaces()) == 4
    board.board[1][2].player = board.player1
    assert len(board.remaining_spaces()) == 3
    board.board[2][0].player = board.player1
    assert len(board.remaining_spaces()) == 2
    board.board[2][1].player = board.player1
    assert len(board.remaining_spaces()) == 1
    board.board[2][2].player = board.player1
    assert len(board.remaining_spaces()) == 0

    # Player 0 (Draw) Score board
    assert board.score_board[board.player0] == 0
    board.score_board[board.player0] += 1
    assert board.score_board[board.player0] == 1

    # Player 1 Score board
    assert board.score_board[board.player1] == 0
    board.score_board[board.player1] += 1
    assert board.score_board[board.player1] == 1

    # Player 2 Score board
    assert board.score_board[board.player2] == 0
    board.score_board[board.player2] += 1
    assert board.score_board[board.player2] == 1

def test_ai():
    """Testing basic ai moves"""

    # AI should place player on board
    board = Board()
    board.this_player = board.player1
    board.next_player = board.player2

    # empty board has 9 spaces
    assert len(board.remaining_spaces()) == 9

    # first move should have 8 spaces
    board.ai_move()
    assert len(board.remaining_spaces()) == 8

    # AI should place winning move
    board = Board()
    # OO-
    # XX-
    # O-X
    board.board[0][0].player = board.player2 #1
    board.board[0][1].player = board.player2 #2
    board.board[0][2].player = board.player0 #3
    board.board[1][0].player = board.player1 #4
    board.board[1][1].player = board.player1 #5
    board.board[1][2].player = board.player0 #6
    board.board[2][0].player = board.player2 #7
    board.board[2][1].player = board.player0 #8
    board.board[2][2].player = board.player1 #9

    board.this_player = board.player1
    board.next_player = board.player2
    board.ai_move()

    board_spots = 'OO-XXXO-X'
    msg = 'Winning Move for "{}" is "{}", not "{}"'
    assert str(board) == board_spots, msg.format(board.player1, board_spots,
                                                 board)

    # AI should block winning move
    board = Board()
    # XX-
    # --O
    # --O
    board.board[0][0].player = board.player1 #1
    board.board[0][1].player = board.player1 #2
    board.board[0][2].player = board.player0 #3
    board.board[1][0].player = board.player0 #4
    board.board[1][1].player = board.player0 #5
    board.board[1][2].player = board.player2 #6
    board.board[2][0].player = board.player0 #7
    board.board[2][1].player = board.player0 #8
    board.board[2][2].player = board.player0 #9

    board.this_player = board.player2
    board.next_player = board.player1
    board.ai_move()

    board_spots = 'XXO--O---'
    msg = 'Blocking move for.player2 is "{}", not "{}"'
    assert str(board) == board_spots, msg.format(board_spots, board)

    # NOT a win by diagonal right-to-left
    board = Board()
    # XOX
    # -X-
    # OXO
    board.board[0][0].player = board.player1 #1
    board.board[0][1].player = board.player2 #2
    board.board[0][2].player = board.player1 #3
    board.board[1][0].player = board.player0 #4
    board.board[1][1].player = board.player1 #5
    board.board[1][2].player = board.player0 #6
    board.board[2][0].player = board.player2 #7
    board.board[2][1].player = board.player1 #8
    board.board[2][2].player = board.player2 #9

    board.this_player = board.player2
    board.next_player = board.player1
    board.ai_move()
    # assert board.player_win_round(board.player2) == True
    msg = 'Board should be not be winnable: "{}"'
    assert board.winning_space() == False, msg.format(board)

def bad_logical_move():
    """
    Testing ai_move for preference of obvious winning move

    """
    # AI should place winning move
    board = Board()

    board.board.ard[0][0].player = board.player1 #1
    board.board.ard[0][1].player = board.player1 #2
    board.board.ard[0][2].player = board.player2 #3
    board.board.ard[1][0].player = board.player0 #4
    board.board.ard[1][1].player = board.player0 #5
    board.board.ard[1][2].player = board.player0 #6
    board.board.ard[2][0].player = board.player0 #7
    board.board.ard[2][1].player = board.player0 #8
    board.board.ard[2][2].player = board.player2 #9

    board.this_player = board.player2
    board.next_player = board.player1
    board.ai_move()

    # with this board
    # XXO
    # ---
    # --O

    # ai: "O" should win
    # XXO
    # --O
    # --O

    # but it does not
    # XXO
    # O--
    # --O

    board_spots = 'XXO--O--O'
    msg = 'Winning Move for "{}" is "{}", not "{}"'
    assert str(board) == board_spots, msg.format(board.player2, board_spots,
                                                 board)
    print str(board)

def tests():
    """Tests for the Board class"""
    # test that a new board is rational
    new_space()
    new_board()
    board_positions()
    game_winners()
    test_ai()
    # bad_logical_move()

    print "All tests have passed!"

if __name__ == '__main__':
    tests()
