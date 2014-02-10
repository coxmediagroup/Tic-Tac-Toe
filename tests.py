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
    min_dim = Board.MIN_DIM
    max_dim = Board.MIN_DIM

    for x in range(min_dim, max_dim+1):
        for y in range(min_dim, max_dim+1):
            b = Board(rows=x, cols=y)
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

def bad_logical_move():
    """

    """
    # AI should place winning move
    b = Board()

    b.board[0][0].player = b.P1 #1
    b.board[0][1].player = b.P1 #2
    b.board[0][2].player = b.P2 #3
    b.board[1][0].player = b.P0 #4
    b.board[1][1].player = b.P0 #5
    b.board[1][2].player = b.P0 #6
    b.board[2][0].player = b.P0 #7
    b.board[2][1].player = b.P0 #8
    b.board[2][2].player = b.P2 #9

    b.this_player = b.P2
    b.next_player = b.P1
    b.ai()

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
    assert str(b) == board_spots, msg.format(b.P2, board_spots, b)
    print str(b)

def tests():
    """Tests for the Board class"""
    # test that a new board is rational
    new_space()
    new_board()
    board_positions()
    game_winners()
    ai()
    # bad_logical_move()

    print "All tests have passed!"

if __name__ == '__main__':
    tests()