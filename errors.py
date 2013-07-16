"""
General exception raised when errors occur throughout the Tic-Tac-Toe console program.
"""


class TicTacToeError(Exception):
    """
    General exception raised when errors occur throughout the Tic-Tac-Toe console program.
    """
    def __init__(self, error_msg, error_code):
        Exception.__init__(self, error_msg)
        self.error_msg = error_msg
        self.error_code = error_code

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "[{0}] {1}".format(self.error_code, self.error_msg)
