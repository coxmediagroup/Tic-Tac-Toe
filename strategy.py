import model
import random


self_flag = None
player_flag = None


def can_win():
    """Return tuple representing space"""
    global self_flag
    return model.can_player_win(self_flag) or can_opponent_win()


def can_opponent_win():
    """Return tuple (boolean, tuple(integer, integer)"""
    global player_flag
    return model.can_player_win(player_flag) or can_fork()


def can_fork():
    """Return tuple (boolean, tuple(integer, integer)"""
    global self_flag
    return break_opponent_fork()


def break_opponent_fork():
    """Return tuple (row_index, column_index)"""
    global player_flag
    if model.can_player_fork(player_flag):
        return side()
    else:
        return square()


def corner(empty_corners):
    """Return tuple (row_index, column_index)"""
    return random.choice(empty_corners)


def side():
    """Return integer"""
    try:
        return random.choice(model.empty_sides())
    except IndexError:
        return None

def square():
    """Return integer"""
    if model.is_board_empty():
        return corner(model.is_corner_empty())
    if model.is_center_empty():
        return 1, 1
    corners = model.is_corner_empty()
    if corners:
        return corner(corners)
    return side()

def pick_move():
    """Return tuple representing space

    Public facing call to allow modification to strategy logic without changing other parts of the program."""
    return can_win()