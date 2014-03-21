import model


def can_win():
    """Return tuple representing space"""
    return None or can_opponent_win()


def can_opponent_win():
    """Return tuple (boolean, tuple(integer, integer)"""
    return None or can_fork()


def can_fork():
    """Return tuple (boolean, tuple(integer, integer)"""
    return None or can_opponent_fork()


def can_opponent_fork():
    """Return tuple (boolean, tuple(integer, integer)"""
    return None or square()


def is_board_empty():
    """Return boolean"""
    return None


def is_center_empty():
    """Return boolean"""
    return None


def is_corner_empty():
    """Return boolean"""
    return None


def corner():
    """Return integer"""
    return None


def side():
    """Return integer"""
    return None


def square():
    """Return int."""
    if is_board_empty():
        return corner()
    if is_center_empty():
        return CENTER
    if is_corner_empty():
        return corner()
    return side()

def pick_move():
    """Return tuple representing space

    Public facing call to allow modification to strategy logic without changing other parts of the program."""
    return can_win()