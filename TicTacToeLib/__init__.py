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
CORNERS = [UPPER_LEFT_CORNER,UPPER_RIGHT_CORNER,LOWER_LEFT_CORNER,LOWER_RIGHT_CORNER]
OPPOSITE_CORNERS = [[UPPER_LEFT_CORNER,LOWER_RIGHT_CORNER],[UPPER_RIGHT_CORNER,LOWER_LEFT_CORNER]]
EDGES = [UPPER_EDGE,LEFT_EDGE,RIGHT_EDGE,LOWER_EDGE]


class Board(object):
    def __init__(self):
        # Create an empty board        
        self.__gameboard = [BLANK] * (GAME_BOARD_SQUARE_SIZE)
        
    def getGameBoard(self):
        return list(self.__gameboard)
    
    def isValidMove(self,pos):
        return self.__gameboard[pos] == BLANK
    
    def validMoveList(self):
        _valid_moves = []
        for i in xrange(GAME_BOARD_SQUARE_SIZE):
            if self.isValidMove(i): _valid_moves.append(i)
        return _valid_moves
    
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
            
# Base class that doesn't do much but will be used for the human player            
class Player(object):
    def __init__(self, piece):
        self.piece = piece
        
# Class for the AI controlled player 
class AIPlayer(Player):
    def __init__(self, piece):
        super(AIPlayer, self).__init__(piece)
        self.__hasMadeInitialMove = False
        
    def move(self, board):
        # using the wikipedia algorithm
        # 1. Play for win
        # 2. Play for block
        # 3. Play for fork
        # 4. Play for block of potential opponent fork
        # 5. Play center
        # 6. Play opposite corner from opponent
        # 7. Play empty corner
        # 8. Play empty edge
        _board = copy.deepcopy(board)
        # move = INVALID_MOVE
        
        # 1. check for win
        move = self.__checkForWin(_board)
        if move != NO_MOVE: return move
        
        # 2. check for block
        move = self.__checkForBlock(_board)
        if move != NO_MOVE: return move
        
        # 3. check for fork
        move = self.__checkForFork(_board)
        if move != NO_MOVE: return move
        
        # 4. check for fork block
        move = self.__blockFork(_board)
        if move != NO_MOVE: return move
        
        # 5. check for center
        move = self.__checkForCenter(_board)
        if move != NO_MOVE: return move
        
        # 6. check for opposite corner
        move = self.__checkForOppositeCorner(_board)
        if move != NO_MOVE: return move
        
        # 7. Play empty corner
        move = self.__checkForEmptyCorner(_board)
        if move != NO_MOVE: return move
        
        # 8. Play empty edge
        move = self.__checkForEmptyEdge(_board)        
        return move
            
    def __opponentPiece(self):
        return PIECE_O if (self.piece == PIECE_X) else PIECE_X

    # return the first move that creates a win for the specified player
    def __findFirstWinningMove(self, board, player):
        _move = NO_MOVE
            
        for future_move in board.validMoveList():
            _board = copy.deepcopy(board)
            _board.move(player, future_move)
            if _board.isWinner(player):
                return future_move
        
        return _move
    
    def __checkForWin(self, board):
        return self.__findFirstWinningMove(board, self) 
    
    def __checkForBlock(self, board):
        return self.__findFirstWinningMove(board, Player( self.__opponentPiece()))
    
    #TODO is there a better algorithm for this? 
    def __findFork(self,board,player):
        _move = NO_MOVE

        for future_move in board.validMoveList():
            _board = copy.deepcopy(board)
            _board.move(player, future_move)
            # now count possible winning moves
            possible_wins = 0
            for future_move_plus in _board.validMoveList():
                _winning_board = copy.deepcopy(_board)
                _winning_board.move(player,future_move_plus)
                if _winning_board.isWinner(player):
                    possible_wins += 1
                    
            # two possible winning moves makes a fork
            if possible_wins > 1:
                return future_move
        
        return _move
    
    def __checkForFork(self,board):
        return self.__findFork(board, self)

    def __checkForCenter(self,board):
        return CENTER if board.isValidMove(CENTER) else NO_MOVE
    
    def __checkForEmptyCorner(self,board):
        _emptyCornerList = [i for i in CORNERS if i in board.validMoveList()]
        return NO_MOVE if len(_emptyCornerList) == 0 else _emptyCornerList[0]

    def __checkForEmptyEdge(self,board):
        _emptyEdgeList = [i for i in EDGES if i in board.validMoveList()]
        return NO_MOVE if len(_emptyEdgeList) == 0 else _emptyEdgeList[0]
    
    # check to see if a an opponent occupies a corner and if so choose a caddy corner move
    def __checkForOppositeCorner(self, board):
        gameBoard = board.getGameBoard()
        validMoves = board.validMoveList()
        for corners in OPPOSITE_CORNERS:
            if ((corners[0] not in validMoves) 
            and (gameBoard[corners[0]]==self.__opponentPiece()) 
            and (corners[1] in validMoves)):
                return corners[1]
            
            if ((corners[1] not in validMoves) 
            and (gameBoard[corners[1]]==self.__opponentPiece()) 
            and (corners[0] in validMoves)):
                return corners[0]
            
        return NO_MOVE
    
    # look ahead logic for forcing a block
    def __blockFork(self,board):
        opponent = Player(self.__opponentPiece())
        if self.__findFork(board, opponent) == NO_MOVE:
            return NO_MOVE
        
        # try to force opponent to block
        # create list of moves that will force block
        for future_move in board.validMoveList():
            _board = copy.deepcopy(board)
            _board.move(self, future_move)
            opponent_block = self.__checkForWin(_board) 
            if  opponent_block != NO_MOVE: 
                _board.move(opponent,opponent_block)
                
                # if we created a fork we can move on
                if self.__checkForWin(_board) != NO_MOVE:
                    return future_move
                
                # another possible look ahead
                ai_block = self.__checkForBlock(_board)
                
                # no forks and nothing to block == good move
                if ai_block == NO_MOVE and self.__findFork(_board, opponent)==NO_MOVE:
                    return future_move
                    
                # do the next look ahead    
                if ai_block != NO_MOVE:
                    _board.move(self, ai_block)
                    # redundant?
                    if ((self.__checkForBlock(_board) == NO_MOVE) and 
                        (self.__findFork(_board, opponent)==NO_MOVE)):
                        return future_move
                    
            # No way to force opponent into block
            # Let's see if we broke the fork and didn't set up a win
            elif ((self.__checkForBlock(_board) == NO_MOVE) and 
                  (self.__findFork(_board, opponent)==NO_MOVE)):
                return future_move
                            
        return NO_MOVE



            
                
                
                
            
        
        
