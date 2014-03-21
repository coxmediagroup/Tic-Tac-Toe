import model
import random


computer_flag = None
player_flag = None


def can_win():
    """Return tuple representing space"""
    global computer_flag
    return model.can_player_win(computer_flag) or can_opponent_win()


def can_opponent_win():
    """Return tuple representing space"""
    global player_flag
    return model.can_player_win(player_flag) or can_fork()


def can_fork():
    """Return tuple representing space"""
    global computer_flag
    return break_opponent_fork()


def break_opponent_fork():
    """Return tuple representing space"""
    global player_flag
    if model.can_player_fork(player_flag):
        return side()
    else:
        return square()


def corner(empty_corners):
    """Return tuple representing space"""
    return random.choice(empty_corners)


def side():
    """Return tuple representing space"""
    try:
        return random.choice(model.empty_sides())
    except IndexError:
        return None


def square():
    """Return tuple representing space"""
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