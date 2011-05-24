# tictactoe game

from game import Game, play_game
from player import human, computer


class TicTacToe(Game):

    def __init__(self):
        """Tictactoe game in which first player is X"""
        self.size = 3
        moves = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]
        self.initial = dict(turn='X', player_MIN=False, player_MAX=True,
            utility=0, board={}, moves=moves)

    def make_move(self, state, move):
        if move not in state['moves']:
            return state

        board = state['board'].copy()
        board[move] = state['turn']

        moves = state['moves'][:]
        moves.remove(move)

        return dict(turn=('O' if state['turn'] == 'X' else 'X'),
            player_MIN=not state['player_MIN'],
            player_MAX=not state['player_MAX'],
            utility=self.utility_for_state(board, move, state['turn']),
            board=board, moves=moves)

    def legal_moves(self, state):
        return state['moves']

    def utility_for_state(self, board, move, player):
        def in_line(board, move, player, (dx, dy), k):
            n = 0
            x, y = move
            while board.get((x,y)) == player:
                n += 1
                x, y = x + dx, y + dy

            x, y = move
            while board.get((x,y)) == player:
                n += 1
                x, y = x - dx, y - dy

            return (n-1) >= k

        horizontal = in_line(board, move, player, (1, 0), 3)
        vertical = in_line(board, move, player, (0, 1), 3)
        diagonal_down = in_line(board, move, player, (1, 1), 3)
        diagonal_up = in_line(board, move, player, (1, -1), 3)

        if any([horizontal, vertical, diagonal_down, diagonal_up]):
            return (1 if player == 'X' else -1)
        else:
            return 0

    def utility(self, state):
        """returns utility for player: -1 for loss, 1 for win, default is 0"""
        return state['utility']

    def terminal_state(self, state):
        return state['utility'] != 0 or len(state['moves']) == 0

    def display(self, state):
        board = state['board']
        for x in range(1, self.size+1):
            for y in range(1, self.size+1):
                print board.get((x,y), '.'),
            print


if __name__ == '__main__':
    print 'Simple TicTacToe Game.'
    print 'You are player X, you play against the computer.'
    play_game(TicTacToe(), human, computer)
