# generic game class and utilities


class Game(object):
    """Generic game class"""
	
    initial = None

    def make_move(self, state, move):
        raise NotImplementedError()

    def legal_moves(self, state):
        raise NotImplementedError()

    def player_MIN(self, state):
        return state['player_MIN']

    def player_MAX(self, state):
        return state['player_MAX']

    def utility(self, state):
        raise NotImplementedError()

    def terminal_state(self, state):
        return not self.legal_moves(state)

    def turn(self, state):
        return state['turn']

    def display(self, state):
        raise NotImplementedError()

    def successors(self, state):
        """returns a list of legal (move, state) pairs"""
        return [(move, self.make_move(state, move))
            for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


def play_game(game, *players):
    state = game.initial
    while True:
        for player in players:
            previous_turn = state['turn']
            while state['turn'] == previous_turn:
                move = player(game, state)
                print move
                state = game.make_move(state, move)
            if game.terminal_state(state):
                game.display(state)
                print 'Player %s wins' % previous_turn
                return
