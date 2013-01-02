"""
A simple tic tac toe game where the computer always wins or at least ties.
"""

class PositionAlreadyTakenError(Exception):
    pass

class Board(object):
    """A tic tac toe board"""

    wins = ((0,1,2), # rows
            (3,4,5),
            (6,7,8),
            (0,3,6), # columns
            (1,4,7),
            (2,5,8),
            (0,4,8), # diagonals
            (2,4,6))

    def __init__(self, *args, **kwargs):
        self.tttboard = [None, None, None,
                         None, None, None,
                         None, None, None]

    def select_position(self, position, player):
        """Sets a position on the board as owned by a player"""

        if self.tttboard[position] is not None:
            raise PositionAlreadyTakenError()

        self.tttboard[position] = player.board_value

    def check_for_win(self, player):
        winner = False
        for group in Board.wins:
            if self.tttboard[group[0]] == player.board_value \
                    and self.tttboard[group[1]] == player.board_value \
                    and self.tttboard[group[2]] == player.board_value:
                winner = True
                break

        return winner

class Player(object):
    """A tic tact toe player"""

    def __init__(self, board_value, *args, **kwargs):
        """
        board_value should be a single character to display such as X or O.
        """

        self.board_value = board_value  # the value which will represent the player behind the scenes

class AIPlayer(Player):
    """An AI tic tac toe player"""

    # High priority board positions in order that they should be selected
    # if the position is open and there are no higher priorities such as
    # a winning opening or blocking a win.
    # This is the middle and then the 4 corners, the positions with the most
    # opportunity for leading to a win.
    POSITION_PRIORITY = (4, 0, 2, 6, 8)

    def look_for_win(self, board, player=None):
        """Find a space which allows a win for the given player"""

        win_spot = None
        if player is None:
            player = self

        for group in board.wins:
            # creates a list of just the elements of the board which are
            # part of a specific win group and and not already owned by the player
            # and creates a list of tuples of the element and its value.
            not_mine = [(i, val) for i, val in enumerate(board.tttboard)
                        if i in group
                        and val != player.board_value]

            # If there's only one not owned by the ai player and not owned by
            # the other player then select it and we've won
            if len(not_mine) == 1 and not_mine[0][1] is None:
                # Maybe this should return the selection rather than
                # modifying the board in here.  Decide later.
                win_spot=not_mine[0][0]
                break

        return win_spot

    def pick_open_position(self, board):
        """
        Select any open spot on the board.

        This is a fallback to be used when there are no wins or win blockers.
        """

        open_positions = [i for i, value in enumerate(board.tttboard) if value is None]

        # default no priority position
        selected_position = open_positions[0]

        for position in AIPlayer.POSITION_PRIORITY:
            if position in open_positions:
                selected_position = position
                break


        return selected_position


# A singleton object could be used for the game, but it does't really
# add anything other than some extra complication with the given requirements.
def play_game(board, player1, player2):
    """The main game loop/logic"""
    import sys

    def draw(board):
        print chr(27) + "[2J"
        for position, value in enumerate(board.tttboard):
            if value is None:
                sys.stdout.write(str(position))
            else:
                sys.stdout.write(str(value))

            if (position + 1) % 3 != 0:
                sys.stdout.write('|')
            else:
                print ''

            if position == 2 or position == 5:
                print '-' * 5

    while True:
        draw(board)

        if None not in board.tttboard:
            print 'No more moves left.'
            break

        # ai player logic
        aichoice = player1.look_for_win(board)
        if aichoice is None:
            aichoice = player1.look_for_win(board, player2)

        if aichoice is None:
            aichoice = player1.pick_open_position(board)

        board.select_position(aichoice, player1)
        draw(board)
        if board.check_for_win(player1):
            print "Computer Wins!"
            break

        if None not in board.tttboard:
            print 'No more moves left.'
            break

        # player selection
        selection = raw_input('Pick a spot: ')
        if selection.lower() == 'q':
            break

        board.select_position(int(selection), player2)
        if board.check_for_win(player2):
            # Well, this isn't supposed to happen.
            print "You Win!"
            break


if __name__ == '__main__':
    player1 = AIPlayer('X')
    player2 = Player('Y')
    board = Board()

    play_game(board, player1, player2)
