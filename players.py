import random

CORNERS = [0, 2, 6, 8]
CADDY_CORNERS = [[0, 8], [2, 6]]
WALLS = [1, 3, 5, 7]
CENTER = 4
WINNING_MOVES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


class ComputerPlayerO(object):
    """A computer player for the game TicTacToe
    Plays only the O round.
    """
    def __init__(self, board, round):
        self.board = board
        self.round = round

    rounds = [
        'round_one',
        'round_two',
        'round_three',
        'round_four',
    ]

    def round_one(self, last_play):
        """Strategy:
        If X plays anything other than center, take center.
        If X plays center, pick a random corner.
        """
        if last_play is not CENTER:
            return CENTER
        return random.choice(CORNERS)

    def round_two(self, last_play):
        """Strategy:
        If X threatens a win, block it
        If the X's are in opposite corners, play 3, 5 or 7 to force a tie
        Else, pick a remaining corner
        """
        needs_blocked, play = self.block_win()
        if needs_blocked:
            return play
        if self.caddy_corner_xes():
            # tie game
            return random.choice([3, 5, 7])
        return random.choice(self.remaining_corners)

    def round_three(self, last_play):
        """Strategy:
        If O can win, take the win
        If X threatens a win, block it
        Else, pick a wall space
        """
        play_found, play = self.block_or_win()
        if play_found:
            return play
        return random.choice(self.remaining_walls)

    def round_four(self, last_play):
        """Strategy:
        If O can win, take the win
        If X threatens a win, block it
        Else, pick a remaining space
        """
        play_found, play = self.block_or_win()
        if play_found:
            return play
        return random.choice(self.remaining_spaces)

    def play(self, last_play):
        # find the function to call for the specified round in self.rounds
        # and call it to get the next move
        play_round = getattr(self, self.rounds[self.round - 1])
        next_play = play_round(last_play)
        self.board[next_play]["has_o"] = True
        return next_play

    @property
    def xes(self):
        return [x for x, square in enumerate(self.board) if square['has_x']]

    @property
    def oes(self):
        return [o for o, square in enumerate(self.board) if square['has_o']]

    @property
    def xes_and_oes(self):
        return self.xes + self.oes

    @property
    def remaining_spaces(self):
        spaces = CORNERS + WALLS + [CENTER]
        return [space for space in spaces if space not in self.xes_and_oes]

    @property
    def remaining_corners(self):
        return [i for i in CORNERS if i not in self.xes_and_oes]

    @property
    def remaining_walls(self):
        return [i for i in WALLS if i not in self.xes_and_oes]

    @property
    def best_spaces(self):
        """returns a list of spaces that best setup the computer
        for a winning game
        """
        spaces = []
        for win in WINNING_MOVES:
            oes_in_win = [o for o in self.oes if o in win]
            if oes_in_win:
                spaces += win
        return [space for space in spaces if space in self.remaining_spaces]

    def block_win(self):
        for win in WINNING_MOVES:
            xes_in_win = [x for x in self.xes if x in win]
            if len(xes_in_win) is 2:
                oes_in_win = [o for o in self.oes if o in win]
                if not oes_in_win:
                    return True, [x for x in win if x not in xes_in_win][0]
        return False, False

    def winning_move(self):
        for win in WINNING_MOVES:
            oes_in_win = [o for o in self.oes if o in win]
            if len(oes_in_win) is 2:
                xes_in_win = [x for x in self.xes if x in win]
                if not xes_in_win:
                    return True, [o for o in win if o not in oes_in_win][0]
        return False, False

    def block_or_win(self):
        can_win, play = self.winning_move()
        if can_win:
            return True, play
        needs_blocked, play = self.block_win()
        if needs_blocked:
            return True, play
        return False, False

    def caddy_corner_xes(self):
        return self.xes in CADDY_CORNERS

    def is_game_over(self):
        """Returns True of False if the game is over and the winning
        combiniation if there was one.
        """
        game_over = self.round is 5
        for win in WINNING_MOVES:
            oes_in_win = [o for o in self.oes if o in win]
            if len(oes_in_win) is 3:
                return True, win
        return game_over, False
