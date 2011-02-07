'''
Created on Jan 29, 2011

@author: Krzysztof Tarnowski (krzysztof.tarnowski@ymail.com)
'''

import numpy

P1 = 1
P2 = -1
EMPTY = 0

NOT_STARTED = -2
IN_PROGRESS = 2
P1_WON = 1
P2_WON = -1
DRAW = 0

class Engine(object):
    ''' Provides helper methods for Tic-Tac-Toe game and interface for AI-like
        algorithms.
    
    Class attributes:
        _COMP_MATRIX: A 3x3 Numpy array filled with the powers of 2. Used for
                      calculating the game state.
        _WIN_VALUES: A list of values that represent a win condition.
        _TOTAL: A sum of values in _COMP_MATRIX.
    '''

    #Can be computed with 2**to_flat_index((i, j)) as well
    _COMP_MATRIX = numpy.array([
                                    [1, 2, 4],
                                    [8, 16, 32],
                                    [64, 128, 256],
                                ])

    _WIN_VALUES = (7, 56, 73, 84, 146, 273, 292, 448)
    
    _TOTAL = 511
        
    def next_move(self, board, player):
        ''' Calculates the best possible _move. 
        
        Args:
            board: As defined in the game.Game class.
            player: As defined in the game.Game class.
            
        Returns:
            A tuple (x, y) representing the best _move from the current player's
            perspective.
        '''
        pass
    
    def get_state(self, board):
        ''' Evaluates the board for win and draw.
        
        The algorithm is based on binary and sum properties of the 2**n
        sequence. For example if the board is given as follows:
        
                0   1   2
              +---+---+---+
            0 | X | O |   |
              +---+---+---+
            1 | X | X | O |
              +---+---+---+
            2 | X | O |   |
              +---+---+---+,
              
        then the scores for P1 and P2 are are calculated by adding together
        all the fields in _COMP_MATRIX that are marked X and Y on the board,
        respectively. Here the score value for X is 89 and for Y is 162.
        
        Total is the sum of scores for P1 and P2 (here: 251).
        
        To check whether a player has won it is necessary to check whether
        specific bits, given as integers in _WIN_VALUES, are set for player's
        score value.        
        
        Args:
            board: As defined in the game.Game class.
            
        Returns:
            The state (as defined in game.Game) of the game for the given board.
        '''
        #TODO: Something faster; possibly use Magic Square

        total, scores = self._compute_scores(board)
                    
        for win_value in self._WIN_VALUES:
            if (scores[P1] & win_value) == win_value: return P1_WON
            if (scores[P2] & win_value) == win_value: return P2_WON
        
        # All fields are taken and no one has won
        if total == self._TOTAL:
            return DRAW
            
        return IN_PROGRESS
    
    def get_opponent(self, player):
        ''' Gets opponent to the given player.
        
        Args:
            player: P1 or P2.
            
        Returns:
            Opponent to the player.
        '''
        
        return (player == P1) and P2 or P1

    def get_legal_moves(self, board):
        ''' Gets valid moves for the given board.
        
        Args:
            board: As defined in the game.Game class.
            
        Returns:
            A list of tuples (x, y) representing valid _move for the given board
            (game state).
        '''
        
        return [(i, j) for i in xrange(0, 3) for j in xrange(0, 3) 
                if board[i, j] == EMPTY]
        
    def _compute_scores(self, board):
        ''' Calculates scores (index values) for the game board evaluation.
        
        Args:
            board: As defined in the game.Game class.
            
        Returns:
            A tuple of integers (total, p1_score, p2_score).
        '''

        total = 0 
        scores = { P1: 0, P2: 0 }
                
        for i in xrange(0, 3):
            for j in xrange(0, 3):
                if board[i, j] != EMPTY:
                    value = self._COMP_MATRIX[i, j]
                    scores[board[i, j]] += value
                    
        total = scores[P1] + scores[P2]
                    
        return total, scores
        

class NegamaxEngine(Engine):
    ''' Tic-Tac-Toe game engine that uses Negamax algorithm to calculate
        the best possible move.
        
        See http://www.hamedahmadi.com/gametree/#negamax for more details.
    
    Attributes:
        max_depth: An integer greater than 0, which represent the maximum depth
                   that the algorithm can descend into the game tree. Defaults
                   to +Infinity.
        _move: The best possible move (x, y) calculated by the algorithm.
    '''
    
    def __init__(self, max_depth=float('Infinity')):
        Engine.__init__(self)
        self.max_depth = max_depth
        self._move = None
        
    def next_move(self, board, player):
        # P1 = 1, P2 = -1
        self._negamax(board, 0, player)
        
        return self._move
            
    def _negamax(self, board, depth, player):
        ''' Traverses the game tree to determine the best possible move.
        
        Args:
            board: As defined in game.Game.
            depth: The current depth in the game tree.
            player: P1 or P2. Determines whether the algorithm should maximize
                    or minimize the game value.
                    
        Returns:
            Maximum value for the game node (state).
        '''
        
        state = self.get_state(board)
        if state != IN_PROGRESS or depth > self.max_depth:
            return player*self._evaluate_board(board, state)
        
        maximum = float('-Infinity')
        
        for move in self.get_legal_moves(board):
            next_board = board.copy()
            next_board[move[0], move[1]] = player
            
            x = -self._negamax(next_board, depth + 1, self.get_opponent(player))
            
            if x > maximum:
                maximum = x
                self._move = move
                
        return maximum
    
    def _evaluate_board(self, board, state):
        ''' Evaluates game tree node given as (board, state) pair.
        
        Args:
            board: As defined in game.Game.
            state: As defined in game.Game.
            
        Returns:
            Value for the given game tree node (state).
        '''
        #TODO: Heuristic board evaluation when depth > max_depth
        
        return state
    
class RulesBasedEngine(Engine):
    ''' Tic-Tac-Toe game engine that uses rules to calculate
        the best possible move.
    
        See http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy for more details.
        
        Attributes:
            _strategies:
            
        Class attributes:
            _CORNERS:
            _OPPOSITE_CORNERS:
            _SIDES:
    '''
    #TODO: Use decorators to mark strategies
    
    _CORNERS = [(0, 0), (0, 2), (2, 0), (2, 2)]
    
    _OPPOSITE_CORNERS = {   
                            (0, 0): (2, 2),
                            (0, 2): (2, 0),
                            (2, 0): (0, 2),
                            (2, 2): (0, 0),
                        }
    
    _SIDES = [(0, 1), (1, 0), (1, 2), (2, 1)]
    
    def __init__(self):
        ''' Initializes a list of available strategies. '''
        
        self._strategies = [
                                '_play_win', '_play_block',
                                '_play_fork', '_play_block_fork',
                                '_play_center', '_play_opposite_corner',
                                '_play_empty_corner', '_play_empty_side',
                                '_play_anywhere',
                            ]
    
    def next_move(self, board, player):
        total, scores = self._compute_scores(board)        
        
        # Try available strategies in the specific order. Stop if a strategy
        # produces valid move(s).
        for strategy in self._strategies:
            fn = getattr(RulesBasedEngine, strategy)
            moves = fn(self, board, player, total, scores)
            if moves: break
            
        return moves[0]

    def _play_win(self, board, player, total, scores):
        ''' Strategy. AI attempts to make a winning move.
        
            The algorithm checks if the win value can be obtained by making
            a move on the given board.
        '''
        
        moves = []
        
        for win_value in self._WIN_VALUES:
            move = numpy.where(self._COMP_MATRIX == win_value - (scores[player] & win_value))
            if board[move] == EMPTY: moves.append(move)
            
        return moves
    
    def _play_block(self, board, player, total, scores):
        ''' Strategy. AI attempts to block opponent's winning move.
        
            It is the same as trying to play a winning move from opponent's
            perspective.
        '''
        
        return self._play_win(board, self.get_opponent(player), total, scores)
    
    def _play_fork(self, board, player, total, scores):
        ''' Strategy. AI attempts to create a fork, i.e. two possible winning
            moves.
            
            The algorithm tries all possible moves to create a new board, which
            is then evaluated according to the 'Play win' strategy.
        '''
        
        moves = []
        
        # Check whether any of the legal moves creates two possible win moves
        for legal_move in self.get_legal_moves(board):
            board[legal_move[0], legal_move[1]] = player
            # Recalculate scores
            new_total, new_scores = self._compute_scores(board)
            next_moves = self._play_win(board, player, new_total, new_scores)
            # Revert
            board[legal_move[0], legal_move[1]] = EMPTY
            # Did the _move create a fork?
            if len(next_moves) > 1: moves.append(legal_move)
            
        return moves
    
    def _play_block_fork(self, board, player, total, scores):
        ''' Strategy. AI attempts to force the opponent into defending.
        
            The algorithm attempts to play two in row as long as it does not
            result in the opponent creating a fork or winning.
        '''
        moves = []
        opponent = self.get_opponent(player)
        
        for move in self.get_legal_moves(board):
            board[move[0], move[1]] = player
            new_total, new_scores = self._compute_scores(board)
            
            # Get winning moves for the player on the new board
            winning_moves = self._play_win(board, player, new_total, new_scores)
            # Get fork moves for the opponent on the new board
            fork_moves = self._play_fork(board, opponent, new_total, new_scores)
            # The move is valid only if it does not create a fork
            for winning_move in winning_moves:
                if not winning_move in fork_moves: moves.append(move)
            # Revert the board
            board[move[0], move[1]] = EMPTY
            
        return moves
    
    def _play_center(self, board, player, total, scores):
        ''' Strategy. AI attempts to play center. '''
        
        if board[1][1] == EMPTY: return [(1, 1)]
    
    def _play_opposite_corner(self, board, player, total, scores):
        ''' Strategy. AI attempts to play opposite corner. '''
        
        moves = []
        opponent = self.get_opponent(player)
        
        for corner in self._CORNERS:
            if board[corner[0], corner[1]] == opponent:
                opp_corner = self._OPPOSITE_CORNERS[corner]
                if board[opp_corner[0], opp_corner[1]] == EMPTY: moves.append(opp_corner)
                
        return moves 
    
    def _play_empty_corner(self, board, player, total, scores):
        ''' Strategy. AI attempts to play empty corner. '''
        
        moves = []
        
        for corner in self._CORNERS:
            if board[corner[0], corner[1]] == EMPTY: moves.append(corner)

        return moves
    
    def _play_empty_side(self, board, player, total, scores):
        ''' Strategy. AI attempts to play empty side. '''
        
        moves = []
        
        for side in self._SIDES:
            if board[side[0], side[1]] == EMPTY: moves.append(side)
            
        return moves

    def _play_anywhere(self, board, player, total, scores):
        ''' Strategy. AI plays any of the available moves. '''
        
        return self.get_legal_moves(board)
