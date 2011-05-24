import itertools

from board import Board
import ai


def get_player_choice_for_human():
    """Ask the human player which letter they want to play as.

    """
    player = None
    print
    while True:
        player = raw_input('What player do you want to be? [Xo]  -> ')
        if not player:
            player = 'x'
        if player.lower() in ['x', 'o']:
            print "You have chosen to play as '%s'" % player.upper()
            break
        print "Invalid player - please choose one of 'x' or 'o'"
    return player.lower()


def human_moves_first():
    """Ask the human whether they want to move first.

    """
    move_first = None
    print
    while True:
        move_first = raw_input('Do you want to go first? [Yn]  -> ')
        if not move_first:
            move_first = 'y'
        if move_first.lower() in ['y', 'n']:
            ordinal = {'y': 'first', 'n': 'second'}[move_first]
            print "You have chosen to go %s." % ordinal
            break
        print "Invalid answer - please choose one of 'y' or 'n'"
    return (move_first == 'y')


get_display_position = lambda x: x + 1


get_internal_position = lambda x: x - 1


def get_move_position_for_computer(board, player):
    print 'Computer is thinking...'
    return ai.get_move_position(board, player)


def get_move_position_for_human(board, player):
    """Ask the human for a valid position for their next move.

    """
    valid_positions = [get_display_position(x) for x in board.valid_moves]
    if len(valid_positions) == 1:
        print 'Only one possible move remains.'
        return get_internal_position(valid_positions[0])
    while True:
        position = raw_input(
            'Where do you want to move? %s  -> ' % valid_positions)
        if position.isdigit():
            position = int(position)
        if position in valid_positions:
            return get_internal_position(position)
        else:
            print 'Invalid move - please choose again.'


def get_instruction_message():
    instructions = """
Make your move by entering a number between %d and %d corresponding to the position you want to move to, as follows:

%s
""".strip()
    positions = [get_display_position(x) for x in Board().valid_moves]
    board_positions = Board.board_template % tuple(positions)
    return instructions % (positions[0], positions[-1], board_positions)


def get_winner_message(winner, player_configs):
    if winner:
        winner_name = dict((x.letter, x.name) for x in player_configs)[winner]
        return '%s won the game!' % winner_name
    else:
        return 'Game ended in a draw.'


class PlayerConfig(object):

    def __init__(self, letter, name, func):
        self.letter = letter
        self.name = name
        self.func = func

    def get_move_position(self, board):
        return self.func(board, self.letter)


def play_game():
    """Play a game of tic-tac-toe, human vs computer.

    """
    print "Let's play tic-tac-toe!"
    human_player = get_player_choice_for_human()
    opponent = Board.get_opponent(human_player)
    player_configs = [
        PlayerConfig(human_player, 'You', get_move_position_for_human),
        PlayerConfig(opponent, 'The computer', get_move_position_for_computer),
        ]
    if not human_moves_first():
        player_configs.reverse()
    print '\n%s\n' % get_instruction_message()
    board = Board()
    for player_config in itertools.cycle(player_configs):
        position = player_config.get_move_position(board)
        board.add_move(player_config.letter, position)
        print '%s moved to position %d\n%s\n' % (
            player_config.name,
            get_display_position(position),
            board.printable_state)
        if board.is_game_over():
            break
    print get_winner_message(board.get_winner(), player_configs)


if __name__ == '__main__':
    play_game()
