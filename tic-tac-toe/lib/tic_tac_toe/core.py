import itertools


class TicTacToeGame(object):
    
    PLAYER = 'X'
    OPPONENT_PLAYER = 'O'
    WIN_POSITIONS = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # vertical
        (0, 4, 8), (2, 4, 6) # diagonal
    )
    
    def __init__(self, board=None):
        """Game initializer"""
        if board is None:
            self._board = [None for _ in range(9)]
        else:
            assert len(board) == 9
            assert set(board).issubset(set([self.PLAYER,
                                            self.OPPONENT_PLAYER,
                                            None]))
            self._board = list(board)
    
    def __str__(self):
        lns = []
        for i in (0, 3, 6):
            lns.append(self._board[i:i+3])
        return '\n'.join(('|'.join((e or '-') for e in ln)) for ln in lns)
    
    @classmethod
    def from_game(cls, other_game):
        if isinstance(other_game, cls):
            board = other_game.board[:]
        else:
            board = other_game
        return cls(board=board)
    
    @property
    def board(self):
        return tuple(self._board)
    
    @property
    def status(self):
        """Return the status for this game. Possible values are:
        
        'WIN', 'DRAW', 'ACTIVE'
        """
        is_over, winner = self._game_result()
        if is_over:
            if winner is None:
                return GAME_STATUS.DRAW
            return GAME_STATUS.WIN
        return GAME_STATUS.ACTIVE
        
    @property
    def winner(self):
        """Return the game winner if the game is over and is not
        
        a draw; otherwise None.
        """
        is_over, winner = self._game_result()
        if is_over and winner is not None:
            return winner
        return None
    
    @property
    def is_over(self):
        """Return whether this game is over; i.e. there's a winner
        
        or this game is a tie/draw.
        """
        return self._game_result()[0]
    
    def mark(self, symbol, pos):
        """
        
        Raises:
            InvalidSymbol
            InvalidMove
        """
        symbol = symbol.upper()
        if symbol not in (self.PLAYER, self.OPPONENT_PLAYER):
            raise InvalidSymbol()
        if pos not in range(9):
            raise InvalidMove()
        
        self._board[pos] = symbol
    
    def available_positions(self):
        """Return list containing available move positions"""
        return [pos for pos, val in enumerate(self._board) if val is None]
    
    def _game_result(self):
        """Return a tuple indicating the status of this game:
            
            Possible outputs:
                (True, 'X') => game over and player 'X' won
                (True, 'O') => game over and player 'O' won 
                (True, None) => game over and is a draw
                (False, None) => game is active
        """
        def win_cond(win_perm):
            if len(set(map(lambda pos: self._board[pos], win_perm))) == 1:
                return self._board[win_perm[0]]
            return None
        
        winner = next(
            itertools.ifilter(
                None,
                itertools.imap(win_cond, self.WIN_POSITIONS)
            ),
            None
        )
        if winner is not None:
            return True, winner
        elif None not in self._board:
            return True, None
        else:
            return False, None
        

class Player(object):
    
    def do_move(self):
        pass


class ComputerPlayer(object):
    """A smarty unbeatable player"""
    
    def __init__(self):
        self._symbol = TicTacToeGame.PLAYER
        self._next_active_turn = itertools.cycle(
            (TicTacToeGame.PLAYER, TicTacToeGame.OPPONENT_PLAYER)
        )
    
    def do_move(self, game):
        """Perform best possible move on `game`'s board.
        
        Args:
            game: A TicTacToeGame instance
        Returns:
            None
        """
        best_move, _ = self._mini_max(game, self._next_active_turn.next())
        game.mark(self._symbol, best_move)
        
    def _mini_max(self, game, active_turn):
        """Minimax algorithm implementation"""    
        best_score = None
        best_move = None
        
        if game.is_over:
            return None, self._score(game)

        for pos in game.available_positions():
            game = TicTacToeGame.from_game(game)
            game.mark(active_turn, pos)
            _, score = self._mini_max(game, self._next_active_turn.next())
            
            # computer's turn
            if active_turn == self._symbol:
                if best_score is None or score > best_score:
                    best_score = score
                    best_move = pos
            else: # opponent's turn
                if best_score is None or score < best_score:
                    best_score = score
                    best_move = pos
        
        return best_move, best_score
    
    def _score(self, game):
        assert game.is_over
        winner = game.winner
        # it's a draw
        if winner is None:
            score = 0
        # computer won
        if winner == self._symbol:
            score = 1
        # opponent won
        else:
            score = -1
        return score


class InvalidSymbol(Exception):
    pass


class InvalidMove(Exception):
    pass


class attrdict(dict):
    
    def __getattr__(self, name):
        if self.has_key(name):
            return self[name]
        raise AttributeError("'%s' object has no attribute '%s'" %
                             (self.__class__.name, name))



GAME_STATUS = attrdict(
    WIN='WIN',
    DRAW='DRAW',
    ACTIVE='ACTIVE'
)
