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


def test_first_move():
    human = tictactoe.PLAYER_X
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    board = tictactoe.Board()
    assert computer.get_next_move(board) in ((0,0), (2,0), (0,2), (2,2))


def test_response_to_center():
    human = tictactoe.PLAYER_X
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    board = tictactoe.Board()
    board.add_move((1, 1), human)
    assert computer.get_next_move(board) in ((0,0), (2,0), (0,2), (2,2))


def test_response_to_corners():
    human = tictactoe.PLAYER_X
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    for corner in ((0,0), (2,0), (0,2), (2,2)):
        board = tictactoe.Board()
        board.add_move(corner, human)
        assert (1, 1) == computer.get_next_move(board)


def test_response_to_edge():
    human = tictactoe.PLAYER_X
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    board = tictactoe.Board()
    board.add_move((1, 0), human)
    
    good_moves = [
            # center
            (1, 1),

            # adjacent corner
            (0, 0), (2, 0),

            # opposite edge
            (1, 2),
        ]

    for i in range(100):
        assert computer.get_next_move(board) in good_moves


def test_get_adjacent_corners():
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    corners = computer._get_corners_adjacent_to_edge((0, 1))
    assert 2 == len(corners)
    assert (0, 0) in corners
    assert (0, 2) in corners
    
    corners = computer._get_corners_adjacent_to_edge((2, 1))
    assert 2 == len(corners)
    assert (2, 0) in corners
    assert (2, 2) in corners
    
    corners = computer._get_corners_adjacent_to_edge((1, 0))
    assert 2 == len(corners)
    assert (0, 0) in corners
    assert (2, 0) in corners
    
    corners = computer._get_corners_adjacent_to_edge((1, 2))
    assert 2 == len(corners)
    assert (0, 2) in corners
    assert (2, 2) in corners

def test_get_opposite_edge():
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    assert (2, 1) == computer._get_opposite_edge((0, 1))
    assert (0, 1) == computer._get_opposite_edge((2, 1))
    assert (1, 2) == computer._get_opposite_edge((1, 0))
    assert (1, 0) == computer._get_opposite_edge((1, 2))

def test_get_opposite_corner():
    computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

    assert (2, 2) == computer._get_opposite_corner((0, 0))
    assert (0, 0) == computer._get_opposite_corner((2, 2))
    assert (0, 2) == computer._get_opposite_corner((2, 0))
    assert (2, 0) == computer._get_opposite_corner((0, 2))


