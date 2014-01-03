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


def get_optimal_move(board):
    # for now just find an open space
    empty_spaces = [ s for s in board.keys() if not board[s] ]
    return choice(empty_spaces)

class Game:
    """Maintains the state of a single game of Tic Tac Toe."""
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.turn = 0
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
        
        optimal_move = get_optimal_move(self.board)
        self.board[optimal_move] = 'o'
        self.turn += 1
        
        #consider returning updated board?
        

game_server = Server()
    
