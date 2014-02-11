#!/usr/bin/env python
import sys


class BoardError(Exception):
    pass


class Board:
    """
    A very basic board class that could be used for any  game
    """
    
    def __init__(self, size):
        self.squares = [None] * size
        self.size = size

    def _is_valid_square(self, square):
        """
        Is the user square a valid value for the size of the board?
        """
        if 0 <= square <= (self.size - 1):
            return

        raise BoardError("Invalid Square")

    def is_full(self):
        """
        Are there available squares left on the board?
        """
        return not(None in self.squares)

    def square_free(self, square):
        """
        Has a player already used the requested square?
        """
        self._is_valid_square(square)
        return self.squares[square] is None

    def place(self, square, marker):
        """
        Try to place a player marker on a square.  Will error out if the
        square is not available
        """
        if self.is_full():
            raise BoardError("Board is Full")
        if not self.square_free(square):
            raise BoardError("Square is Taken")

        self.squares[square] = marker

    def clear(self, square):
        """
        Remove a player marker from a square.  Can be called on an already
        empty square
        """
        self.squares[square] = None


def main():
    return -1

if __name__ == "__main__":
    sys.exit(main())
