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
CADDY_CORNER_MAP = {
    0: 8,
    8: 0,
    2: 6,
    6: 2,
}
CORNER_BORDERS_MAP = {
    (1, 3): 0,
    (1, 5): 2,
    (3, 7): 6,
    (5, 7): 8,
}


class ComputerPlayerO(object):
    """A computer player for the game TicTacToe
    Plays only the O round.
    """
    def __init__(self, board):
        self.board = board

    rounds = [
        'round_one',
        'round_two',
        'round_three',
        'round_four',
    ]

    def round_one(self):
        """Strategy:
        If X plays anything other than center, take center.
        If X plays center, pick a random corner.
        """
        if self.xes[0] is not CENTER:
            return CENTER
        return random.choice(CORNERS)

    def round_two(self):
        """Strategy:
        If X threatens a win, block it
        If the X's are caddy corner, play 3, 5 or 7 to force a tie
        If X on edge and corner, play the corner square caddy-corner
            to the corner X
        If X's border a corner, play in that corner
        Else, pick a remaining corner
        """
        needs_blocked, play = self.block_win()
        if needs_blocked:
            return play
        edge_and_corner, corner_x = self.xes_on_edge_and_corner()
        if edge_and_corner:
            return CADDY_CORNER_MAP[corner_x]
        if self.caddy_corner_xes():
            return random.choice([3, 5, 7])
        if self.xes_border_a_corner():
            return CORNER_BORDERS_MAP[tuple(self.xes)]
        return random.choice(self.remaining_corners)

    def round_three(self):
        """Strategy:
        If O can win, take the win
        If X threatens a win, block it
        Else, pick a wall space
        """
        play_found, play = self.win_or_block()
        if play_found:
            return play
        return random.choice(self.remaining_walls)

    def round_four(self):
        """Strategy:
        If O can win, take the win
        If X threatens a win, block it
        Else, pick a remaining space
        """
        play_found, play = self.win_or_block()
        if play_found:
            return play
        return random.choice(self.remaining_spaces)

    def play(self):
        # find the function to call for the specified round in self.rounds
        # and call it to get the next move
        next_play = None
        if self.current_round < 5:
            play_round = getattr(self, self.rounds[self.current_round - 1])
            next_play = play_round()
            self.board[next_play]["has_o"] = True
        return next_play

    @property
    def xes(self):
        return [x for x, square in enumerate(self.board)
                if square['has_x']]

    @property
    def oes(self):
        return [o for o, square in enumerate(self.board)
                if square['has_o']]

    @property
    def xes_and_oes(self):
        return self.xes + self.oes

    @property
    def remaining_spaces(self):
        spaces = CORNERS + WALLS + [CENTER]
        return [space for space in spaces
                if space not in self.xes_and_oes]

    @property
    def remaining_corners(self):
        return [i for i in CORNERS
                if i not in self.xes_and_oes]

    @property
    def remaining_walls(self):
        return [i for i in WALLS
                if i not in self.xes_and_oes]

    @property
    def current_round(self):
        return len(self.xes)

    def block_win(self):
        for win in WINNING_MOVES:
            xes_in_win = [x for x in self.xes
                          if x in win]
            oes_in_win = [o for o in self.oes
                          if o in win]
            if oes_in_win:
                # already blocked
                continue
            if len(xes_in_win) is 2:
                return True, [x for x in win
                              if x not in xes_in_win][0]
        return False, False

    def winning_move(self):
        for win in WINNING_MOVES:
            oes_in_win = [o for o in self.oes
                          if o in win]
            xes_in_win = [x for x in self.xes
                          if x in win]
            if xes_in_win:
                # already blocked
                continue
            if len(oes_in_win) is 2:
                return True, [o for o in win
                              if o not in oes_in_win][0]
        return False, False

    def win_or_block(self):
        can_win, play = self.winning_move()
        if can_win:
            return True, play
        needs_blocked, play = self.block_win()
        if needs_blocked:
            return True, play
        return False, False

    def caddy_corner_xes(self):
        return self.xes in CADDY_CORNERS

    def xes_on_edge_and_corner(self):
        on_edge = [x for x in self.xes
                   if x in WALLS]
        on_corner = [x for x in self.xes
                     if x in CORNERS]
        try:
            corner_x = on_corner[0]
        except IndexError:
            corner_x = None
        return all([on_edge, on_corner]), corner_x

    def xes_border_a_corner(self):
        return tuple(self.xes) in CORNER_BORDERS_MAP

    def is_game_over(self):
        """Returns True of False if the game is over and the winning
        combination if there is one.
        """
        game_over = self.current_round is 5
        for win in WINNING_MOVES:
            oes_in_win = [o for o in self.oes
                          if o in win]
            if len(oes_in_win) is 3:
                return True, win
        return game_over, False
