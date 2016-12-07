
import random
from ttt.board import board


class AbstractPlayer:
    """
    Base representation of a player.  Should not be used directly, but as part
    of TextPlayer(AbstractPlayer), GUIPlayer(AbstractPlayer), etc.

    Also gives us a good place to contain the Computer Player logic
    """
    def __init__(self, marker):
        self.marker = marker

    def get_square(self, current_board, previous_move, message):
        """
        Ask the player what square they would like to claim.
            current_board is the current board in play, only being passed here
                for sake of ComputerPlayer
            message will be a string contain any warnings or errors from the
                game engine (i.e. bad input)

            You are expected to return a number corresponding to the square
                the player wishes to claim.  If you return a NoneType, you
                are signalling to end the game
        """
        raise NotImplemented


class ComputerPlayer(AbstractPlayer):
    def __init__(self, marker):
        self.count = 0
        self.style = None
        self.opp_moves = ""
        self.corners = [0, 2, 6, 8]
        self.edges = [1, 3, 5, 7]
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
        self.first_player_responses = {
            "3": 8,  # If their first move after us is an edge, it's game over
            "1": 8,  # pick an appropriate corner response.  They will have to
            "5": 0,  # block us, which will cause us to have to block them.
            "7": 0,  # However, that "block" end up giving us a 2-way win

            "0": 8,  # If their first move after us is a corner, it'll take a
            "2": 6,  # little longer, possibly end in a draw.  Complete the
            "6": 2,  # diagonal and wait to see what their 2nd move is.
            "8": 0,  #

            "61": 8,  # If their second move after a corner is an edge, it's
            "65": 0,  # game over.  Either they have 2-in-a-row which our
            "81": 6,  # other code will block and lead us to a win, or they
            "83": 2,  # did an odd-ball edge which the list here will
            "23": 8,  # respond with the proper corner response that sets us
            "27": 0,  # up for a 2-way win
            "05": 6,  #
            "07": 2   #
        }
        self.second_player_diagonal_check = [
            "08",  # If they are not playing the first_player() strategy, then
            "80",  # we check to see if they did a diagonal play off our center
            "26",  # square.  If so, we just stick to either edges or blocking
            "62",  # them and the game will end in draw
        ]
        AbstractPlayer.__init__(self, marker)

    def check_for(self, current_board, check_func):
        for path in self.win_paths:
            cnt = 0
            blank = 0
            for sq in path:
                if current_board.squares[sq] is None:
                    blank += 1
                elif check_func(current_board.squares[sq]):
                    cnt += 1

            if cnt == 2 and blank == 1:
                for sq in path:
                    if current_board.squares[sq] is None:
                        return sq

        return None

    def check_for_block(self, current_board):
        def is_not_me(marker):
            return marker != self.marker

        return self.check_for(current_board, is_not_me)

    def check_for_win(self, current_board):
        def is_me(marker):
            return marker == self.marker

        return self.check_for(current_board, is_me)

    def first_player(self, current_board, previous_move):
        """
        If we have first square, they we are playing to win but might get a
        draw
        """

        # If we have first square, center is the most versatile place to be
        if self.count == 1:
            return 4

        self.opp_moves += str(previous_move)

        # Like chess, we have pre-programmed responses to their opening moves.
        # No need for us to work too hard, see __init__ for description
        if self.opp_moves in self.first_player_responses:
            return self.first_player_responses[self.opp_moves]

        # After the pre-programmed moves, keep checking to see if we can
        # complete a 2-way win which they could only block 1 leg
        rtn = self.check_for_win(current_board)
        if rtn:
            return rtn

        # A couple of the pre-programmed moves will end with them w/ 2 squares
        # but still be good for us, just throw a block.
        rtn = self.check_for_block(current_board)
        if rtn:
            return rtn

        # If we're down here, the game is definitely going to a draw.  Just
        # pick randomly until the board is full
        i = None
        while True:
            i = random.randint(0, current_board.size-1)
            if current_board.square_free(i):
                return i

    def second_player(self, current_board, previous_move):
        """
        If we have second square, the only good strategy is to play to a
        draw
        """
        self.opp_moves += str(previous_move)

        # If they took the center at the start, take a corner and see what they
        # do.  Otherwise, we need to take the center ourselves.
        if self.count == 1:
            if previous_move == 4:
                return 6
            else:
                return 4

        # If they responded to our corner by completing the diagonal, they are
        # using the same strategy as we have in first_player().  Place in an
        # open corner and keep blocking until draw.
        if self.opp_moves == "42":
            return 0

        # When we are second player, we should always be playing to a draw, but
        # doesn't hurt to see if they did something dumb
        rtn = self.check_for_win(current_board)
        if rtn:
            return rtn

        # This is what we're constantly doing as second player
        rtn = self.check_for_block(current_board)
        if rtn:
            return rtn

        # If we're down here, means they aren't playing the same strategy as
        # first_player.  Pick only available edges and keep blocking to a draw
        if self.opp_moves[0:2] in self.second_player_diagonal_check:
            for e in self.edges:
                if current_board.square_free(e):
                    return e

        # This should never happen as second_player but just in case we somehow
        # fall through all of the above
        i = None
        while True:
            i = random.randint(0, current_board.size-1)
            if current_board.square_free(i):
                return i

    def get_square(self, current_board, previous_move, message):
        """
        Unbeatable NPC with strategy taken from
            http://www.wikihow.com/Win-at-Tic-Tac-Toe
        """
        self.count += 1

        # first move we get to make, are we first or second player?
        if not self.style:
            if previous_move is None:
                self.style = self.first_player
            else:
                self.style = self.second_player

        rtn = self.style(current_board, previous_move)
        return rtn
