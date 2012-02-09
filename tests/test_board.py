
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


def test_available_moves():
    board = tictactoe.Board()

    available_moves = board.get_available_moves()
    assert len(available_moves) == 9
    assert (0,2) in available_moves
    assert (1,2) in available_moves
    assert (2,2) in available_moves
    assert (2,1) in available_moves
    assert (2,0) in available_moves
    assert (1,0) in available_moves
    assert (0,1) in available_moves
    assert (1,1) in available_moves
    assert (0,0) in available_moves

    board.add_move((0,0), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 8
    assert (0,2) in available_moves
    assert (1,2) in available_moves
    assert (2,2) in available_moves
    assert (2,1) in available_moves
    assert (2,0) in available_moves
    assert (1,0) in available_moves
    assert (0,1) in available_moves
    assert (1,1) in available_moves

    board.add_move((1,1), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 7
    assert (0,2) in available_moves
    assert (1,2) in available_moves
    assert (2,2) in available_moves
    assert (2,1) in available_moves
    assert (2,0) in available_moves
    assert (1,0) in available_moves
    assert (0,1) in available_moves

    board.add_move((0,1), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 6
    assert (0,2) in available_moves
    assert (1,2) in available_moves
    assert (2,2) in available_moves
    assert (2,1) in available_moves
    assert (2,0) in available_moves
    assert (1,0) in available_moves

    board.add_move((1,0), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 5
    assert (0,2) in available_moves
    assert (1,2) in available_moves
    assert (2,2) in available_moves
    assert (2,1) in available_moves
    assert (2,0) in available_moves

    board.add_move((2,0), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 4
    assert (0,2) in available_moves
    assert (1,2) in available_moves
    assert (2,2) in available_moves
    assert (2,1) in available_moves

    board.add_move((2,1), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 3
    assert (0,2) in available_moves
    assert (1,2) in available_moves
    assert (2,2) in available_moves

    board.add_move((2,2), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 2
    assert (0,2) in available_moves
    assert (1,2) in available_moves

    board.add_move((0,2), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 1
    assert (1,2) in available_moves

    board.add_move((1,2), tictactoe.PLAYER_X)
    available_moves = board.get_available_moves()
    assert len(available_moves) == 0
