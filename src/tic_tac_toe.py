import uuid
from random import choice

class TurnOutOfOrderError(Exception):
    pass

class IllegalMoveError(Exception):
    pass

class Server:
    """Keeps track of multiple games of Tic Tac Toe facilitates communication
    to the various instances."""
    def __init__(self):
        self.games = {}

    def createGame(self):
        game = Game()
        self.games[game.id] = game
        return game

    def getGame(self, gameId):
        return self.games[gameId]


def find_opening_in_path(path_name, game):
    for square in game.winning_paths[path_name]:
        if not game.board[square]:
            return square


def find_path_move(game, player_symbol):
    b = game.board
    for path_name, path in game.winning_paths.iteritems():
        if (b[path[0]] == b[path[1]] == player_symbol) or \
           (b[path[1]] == b[path[2]] == player_symbol) or \
           (b[path[0]] == b[path[2]] == player_symbol):
            open_space = find_opening_in_path(path_name, game)
            if open_space:
                return open_space


def find_corner_move(game):
    open_corners = [c for c in game.corners if not game.board[c]]
    if open_corners: return choice(open_corners)


def get_optimal_move(game):
    if game.turn == 1:
        if game.board[5] == 'x':
            return choice(game.corners)
        else:
            return 5

    if game.turn == 2:
        if game.board[1] == game.board[9] == 'x' or \
           game.board[3] == game.board[7] == 'x':
            return choice(game.edges)            

    # if there is an opportunity for a win, take it
    # iterate thru each winning path
    win_move = find_path_move(game, 'o')
    if win_move: return win_move

    # if there is an opportunity to block X, take it
    block_move = find_path_move(game, 'x')
    if block_move: return block_move

    # if a corner is open, take it
    corner_move = find_corner_move(game)
    if corner_move: return corner_move

    # take whatever
    empty_spaces = [ s for s in game.board.keys() if not game.board[s] ]
    if empty_spaces: return choice(empty_spaces)

    raise IllegalMoveError("no empty spaces remain")
        

class Game:
    """Maintains the state of a single game of Tic Tac Toe."""
    winning_paths = {
        "h1": (1, 2, 3),
        "h2": (4, 5, 6),
        "h3": (7, 8, 9),
        "v1": (1, 4, 7),
        "v2": (2, 5, 8),
        "v3": (3, 6, 9),
        "d1": (1, 5, 9),
        "d2": (3, 5, 7),
    }
    corners = [1,3,7,9]
    edges = [2,4,6,8]

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.turn = 1
        self.status = 'in_progress'
        self.winning_squares = tuple()
        self.board = self._initialize_board()

    def _initialize_board(self):
        return dict.fromkeys(range(1,10), "")

    def do_turn(self, turnNum, squareNum):
        """Plays an X on squareNum and then finds optimal counter-play and 
        puts an O on the right spot."""
        # ensure valid squareNum
        if squareNum < 1 or squareNum > 9:
            raise IllegalMoveError(
                "squares are numbered 1-9 but you have chosen %d" % squareNum)

        # ensure turns arrive in order
        if turnNum > self.turn+1:
            raise TurnOutOfOrderError(
                    "expecting turn %d but got turn %d instead" % (
                    self.turn+1, turnNum))

        # ensure square is open 
        if self.board[squareNum]:
            raise IllegalMoveError(
                    "square %d is already occupied with %s" % (
                    squareNum, self.board[squareNum]))

        self.board[squareNum] = 'x'
        
        self.evaluate_status()
        if self.status == 'we_lose' or self.status == 'tie':
            return self.status

        optimal_move = get_optimal_move(self)
        self.board[optimal_move] = 'o'

        self.evaluate_status()
        if self.status == 'we_win':
            return self.status

        self.turn += 1
        return self.status # in_progress

    def x_wins(self):
        for path_name, path in self.winning_paths.iteritems():
            if self.board[path[0]] == self.board[path[1]] == self.board[path[2]] == 'x':
                self.winning_squares = self.winning_paths[path_name]
                return True
        return False

    def o_wins(self):
        for path_name, path in self.winning_paths.iteritems():
            if self.board[path[0]] == self.board[path[1]] == self.board[path[2]] == 'o':
                self.winning_squares = self.winning_paths[path_name]
                return True
        return False

    def board_full(self):
        for occupied_spot in self.board.values():
            if not occupied_spot: return False
        return True

    def evaluate_status(self):
        """If x wins, return we_lose and winning squares. If o wins, return
        we_win and winning squares. If tie, return tie. Otherwise, return 
        in_progress."""
        if self.x_wins():
            self.status = 'we_lose'
        elif self.o_wins():
            self.status = 'we_win'
        elif self.board_full():
            self.status = 'tie'
        else:
            self.status = 'in_progress'

game_server = Server()
    
