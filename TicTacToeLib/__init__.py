#TODO Is TicTacToeEngine a better name?
import copy

'''        
    Going to prematurely optimize here by turning a 2D structure into 1D.
    Our board will map 1D positions to 2D like this:
     0 | 1 | 2
     __+___+__
     3 | 4 | 5
     __+___+__
     6 | 7 | 8
     
     For AI: 
     corners = [0,2,6,8]
     edges = [1,3,5,7]
     center = [4]
     winning lines horizontal = [0,1,2], [3,4,5], [6,7,8] 
     winning lines vertical = [0,3,6], [1,4,7], [2,5,8]
     winning lines diagonal = [0,4,8], [2,4,6] 
     
     the winning lines map out to slices:
     horizontal=[0:3:1],[3:6:1],[6:9:1]
     vertical=[0:7:3],[1:8:3],[2:9:3]
     diagonal=[0:9:4],[2:7:2]
'''
GAME_BOARD_WIDTH = 3
GAME_BOARD_SQUARE_SIZE = GAME_BOARD_WIDTH*GAME_BOARD_WIDTH
BLANK = ''
WINNING_LINE_SLICES = [[0,3,1],[3,6,1],[6,9,1],[0,7,3],[1,8,3],[2,9,3],[0,9,4],[2,7,2]]
PIECE_X = 'X'
PIECE_O = 'O'
UPPER_LEFT_CORNER = 0
UPPER_EDGE = 1
UPPER_RIGHT_CORNER = 2
LEFT_EDGE = 3
CENTER = 4
RIGHT_EDGE = 5
LOWER_LEFT_CORNER = 6
LOWER_EDGE = 7
LOWER_RIGHT_CORNER = 8
NO_MOVE = INVALID_MOVE = -1

# TODO Is naming clear?
class Board(object):
    def __init__(self):
        # Create an empty board        
        self.__gameboard = [BLANK] * (GAME_BOARD_SQUARE_SIZE)
        
    def getGameBoard(self):
        return list(self.__gameboard)
    
    def isValidMove(self,pos):
        return self.__gameboard[pos] == BLANK
    
    def move(self,player,pos):
        valid = self.isValidMove(pos)
        if valid: self.__gameboard[pos] = player.piece
        return valid
    
    def isBoardFull(self):
        return BLANK not in self.__gameboard
    
    def isWinner(self, player):
        # get the sliced list and see if count matches
        for first,last,step in WINNING_LINE_SLICES:
            line = self.__gameboard[first:last:step]
            if line.count(player.piece) == GAME_BOARD_WIDTH:
                return True
            
        return False
    

    def getTotalMovesMade(self):
        return (GAME_BOARD_SQUARE_SIZE-self.__gameboard.count(BLANK))            
            
class Player(object):
    def __init__(self, piece):
        self.piece = piece
        
class AIPlayer(Player):
    def __init__(self, piece):
        super(AIPlayer, self).__init__(piece)
        #self.__gameboard = []
        self.__hasMadeInitialMove = False
        
    #def setGameBoard(self, gameboard):
    #    self.__gameboard = gameboard
        
    def move(self, board):
        # this should probably require a gameboard?
        _board = copy.deepcopy(board)
        move = INVALID_MOVE
        if not self.__hasMadeInitialMove:
            move = self.__initialMove(_board)    
            if move != INVALID_MOVE:
                self.__hasMadeInitialMove = True
        return move
    
    def __initialMove(self, board):
        _move = -1
        if board.getTotalMovesMade() == 0:
            _move = UPPER_LEFT_CORNER # Always Upper Left for 1st move
        elif board.getTotalMovesMade() == 1:
            # if center is available take it else take first corner
            if board.isValidMove(CENTER): 
                _move = CENTER
            elif board.isValidMove(UPPER_LEFT_CORNER):
                _move = UPPER_LEFT_CORNER
        return _move
    
    def __opponentPiece(self):
        return PIECE_O if (self.piece == PIECE_X) else PIECE_X

    def __findFirstWinningMove(self, board, player):
        _move = NO_MOVE
        _valid_moves = []
        for i in xrange(GAME_BOARD_SQUARE_SIZE):
            if board.isValidMove(i): _valid_moves.append(i)
            
        for future_move in _valid_moves:
            _board = copy.deepcopy(board)
            _board.move(player, future_move)
            if _board.isWinner(player):
                return future_move
        
        return _move
    
    def __checkForWin(self, board):
        return self.__findFirstWinningMove(board, self) 
    
    def __checkForBlock(self, board):
        return self.__findFirstWinningMove(board, Player( self.__opponentPiece()))
    
    def __findFork(self,board,player):
        _move = NO_MOVE
        for future_move in xrange(GAME_BOARD_SQUARE_SIZE):
            if board.isValidMove(future_move):
                _board = copy.deepcopy(board)
                _board.move(player, future_move)
                # now count possible winning moves
                possible_wins = 0
                for x in xrange(GAME_BOARD_SQUARE_SIZE):
                    if _board.isValidMove(x):
                        _winboard = copy.deepcopy(_board)
                        _winboard.move(player,x)
                        if _winboard.isWinner(player):
                            possible_wins += 1
                
                print possible_wins
                if possible_wins > 1:
                    return future_move
        
        return _move
    
    def __checkForFork(self,board):
        return self.__findFork(board, self)
    
