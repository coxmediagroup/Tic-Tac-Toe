import tictactoe


def test_win_condition_checking():
    human = tictactoe.PLAYER_X
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    board = tictactoe.Board()
    board.add_move((0,0), human)
    board.add_move((0,1), human)
    board.add_move((1,0), tictactoe.PLAYER_O)

    assert (0,2) == computer.get_next_move(board)

    board = tictactoe.Board()
    board.add_move((2,2), human)
    board.add_move((2,1), human)
    board.add_move((1,0), tictactoe.PLAYER_O)
    board.add_move((2,0), tictactoe.PLAYER_O)

    assert (0,0) == computer.get_next_move(board)


def test_optimal_opening_moves():
    human = tictactoe.PLAYER_X
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    board = tictactoe.Board()
    assert computer.get_next_move(board) in ((0,0), (2,0), (0,2), (2,2))
