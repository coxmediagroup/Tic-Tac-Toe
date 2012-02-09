
import tictactoe


def test_board_creation():
    board = tictactoe.Board()


def test_add_move():
    board = tictactoe.Board()
    board.add_move(pos=(1,1), player=tictactoe.PLAYER_X)

    try:
        board.add_move(pos=(1,1), player=tictactoe.PLAYER_O)
    except tictactoe.MoveNotAvailable:
        pass
    else:
        assert False, 'Board allowed 2 moves at the same position'

    try:
        board.add_move(pos=(0,0), player='Unknown')
    except tictactoe.InvalidPlayerError:
        pass
    else:
        assert False, 'Board allowed a move by an unknown player'
        
        
def test_winner_detection():
    board = tictactoe.Board()

    assert board.get_winner() == None

    board.add_move(pos=(0,0), player= tictactoe.PLAYER_X)
    assert board.get_winner() == None

    board.add_move(pos=(1,1), player= tictactoe.PLAYER_X)
    assert board.get_winner() == None

    board.add_move(pos=(2,2), player= tictactoe.PLAYER_X)
    assert board.get_winner() == tictactoe.PLAYER_X
