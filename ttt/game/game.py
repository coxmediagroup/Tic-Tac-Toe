
from ttt.board import board
from ttt.player import player


class AbstractGame:
    """
    The nuts and bolts of TTT itself.  Shouldn't be used directly, rather
    used as a base class for <UIType>Game (i.e. TextGame(AbstractGame)
    or GUIGame(AbstractGame)
    """
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.current_player = player1
        self.winner = None
        self.board = board.Board(9)
        self.win_paths = [
            [0, 1, 2],  # row 1
            [3, 4, 5],  # row 2
            [6, 7, 8],  # row 3
            [0, 3, 6],  # col 1
            [1, 4, 7],  # col 2
            [2, 5, 8],  # col 3
            [0, 4, 8],  # diag 1
            [2, 4, 6]   # diag 2
        ]

    def check_for_winner(self):
        """
        Checks the in-play board for a winner based on the rules of TTT.
        returns the winning person or None if no one has won yet.
        """
        if self.winner:
            return self.winner

        for a, b, c in self.win_paths:
            if self.board.squares[a] \
                    and self.board.squares[a] == self.board.squares[b] \
                    and self.board.squares[a] == self.board.squares[c]:
                self.winner = self.board.squares[a]
                return self.winner

        return None

    def play(self):
        """
        Main game loop, only terminates when play results in a lose or a draw
        """
        while True:
            if not isinstance(self.current_player, player.ComputerPlayer):
                self.display_board()

            message = ""
            square = None
            while True:
                try:
                    square = self.current_player.get_square(
                        self.board,
                        message)
                    if not square:
                        return  # no value, doesn't want to continue
                    square = int(square)
                    if self.board.square_free(square):
                        break
                except (ValueError, board.BoardError):
                    pass  # normally wouldn't do this but okay here, they
                          # gave us either not a number or an invalid square
                          # number
                message = "Invalid Square"

            self.board.place(square, self.current_player.marker)
            if self.check_for_winner() or self.board.is_full():
                break

            if self.current_player == self.player1:
                self.current_player = self.player2
            else:
                self.current_player = self.player1

        self.display_board()
        self.display_finale()

    def display_board(self):
        raise NotImplemented

    def display_finale(self):
        raise NotImplemented
