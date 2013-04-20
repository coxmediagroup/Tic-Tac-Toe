class GameBoard(object):
    def __init__(self, symbol):
        self._symbol = symbol
        self._spaces = [1, 2, 4, 
                        8, 16, 32, 
                        64, 128, 256]

        self._corners = [1, 4, 64, 256]

        self._best_corners = [[256], [64, 256], 64,
                              [4, 256], [], [1, 64],
                              [4], [1, 4], [1]]
        wins = [[1, 2, 4],
              [8, 16, 32],
              [64, 128, 256],
              [1, 8, 64],
              [2, 16, 128],
              [4, 32, 256],
              [1, 16, 256],
              [4, 16, 64]]
        self._wins = dict([(sum(x), x) for x in wins])

        self._moves = []
        self._snapshots = {'X': 0, 'O': 0}
        self._critical_move = None

    @property
    def moves_available(self):
        '''
        Whether or not there are any spaces available that 
        would lead any player closer to a win.
        
        :returns:
        :rtype: bool

        '''
        return bool(self._wins) and not self.winner

    @property
    def winner(self):
        '''
        Whether or not there is a current winner
        
        .. note:: This property assumes the gameboard cannot lose

        :returns:
        :rtype: bool
        
        '''
        snapshot = self._snapshots[self._symbol]
        return any([snapshot & win == win for win in self._wins.iterkeys()])

    @property
    def display(self):
        '''
        Builds a visual representation of the 
        current state of the game board.
        
        :returns:
        :rtype: string
        
        '''
        display =  '-' * 25 +'\n'
        i = 0
        for y in xrange(3):
            idx_row = '|'
            symbol_row = '|'
            for x in xrange(3):
                idx_row += '  ({0})  |'.format(i)
                space_value = self._spaces[i]
                symbol = ' '
                if self._space_taken(space_value, 'X'):
                    symbol = 'X'
                elif self._space_taken(space_value, 'O'):
                    symbol = 'O'
                symbol_row += '   {0}   |'.format(symbol)
                i += 1

            display += '|       ' * 3 + '|\n'
            display += '{0}\n{1}\n'.format(idx_row, symbol_row)
            display += '|       ' * 3 + '|\n'
            display += '-' * 25 + '\n'

        return display

    def make_move_by_index(self, index, symbol):
        '''
        Places a symbol on a space on the board
        
        :param index: space index
        :type index: int
        :param symbol: symbol to use
        :type symbol: string ('X' or 'O')
        
        :returns: Whether or not the action was successful
        :rtype: bool

        '''
        value = self._spaces[index]
        return self._make_move_by_value(value, symbol)

    def move(self):
        '''
        Triggers the game board to make a move on it's own behalf
        
        :returns: Whether or not the action was successful
        :rtype: bool 

        '''
        if self._critical_move:
            return self._make_move_by_value(self._critical_move, self._symbol)
        else:
            move = self._find_best_move()
            return self._make_move_by_value(move, self._symbol)
    
    def _make_move_by_value(self, value, symbol):
        '''
        Places a symbol on a space on the board
        
        :param value: the value of the space to use
        :type value: int
        :param symbol: symbol to use
        :type symbol: string ('X' or 'O')
        
        :returns: Whether or not the action was successful
        :rtype: bool

        '''
        if value in self._moves:
            return False
        
        self._snapshots[symbol] += value
        self._moves.append(value)
        
        self._clean_up()
        return True
    
    def _find_best_move(self):
        '''
        Loops through spaces on the board until it finds an unused space.
        Spaces are prioritized based on the following (in order):
        
        1. The center of the board
        2. The corner space(s) farthest from the human player's last move
        3. Any other corner space
        4. Any edge space
        
        :returns: value of the best space available
        :rtype: int

        '''
        if 16 not in self._moves:
            return 16
        
        last_move_idx = self._spaces.index(self._moves[-1])
        best_corners = self._best_corners[last_move_idx]
        for corner in best_corners:
            if corner not in self._moves:
                return corner

        for corner in self._corners:
            if corner not in self._moves:
                return corner

        for space in self._spaces:
            if space not in self._moves:
                return space

        return None
    
    def _space_taken(self, space, symbol):
        '''
        Determines whether or not one or more spaces 
        are occupied by a player.
        
        :param space: the numerical value associated with 1 or more spaces
        :type space: int
        :param symbol: the player's symbol
        :type symbol: string ('X' or 'O')
        
        example::

            # Determine whether player 'X' owns space 4
            print self._space_taken(4, 'X')
            # Determine whether player 'X' owns spaces 8 and 16
            print self._space_taken(24, 'X')
        
        :returns: Whether or not the space(s) is/are taken by the player
        :rtype: bool

        '''
        snapshot = self._snapshots[symbol]
        return snapshot & space == space
    
    def _clean_up(self):
        '''
        Loops through the previously possible win combinations (self._wins)
        and if any are no longer possible outcomes of the game, they are 
        removed from consideration in future calls to various methods on this
        class, including this one.
        
        If a near-win situation is found (1 player has 2 of the 3 spots on a
        win scenario and the third spot is not taken, this function also makes
        note of it so that the next call to self.move() can pick up on it.
        
        '''
        self._critical_move = None

        moves_left = len(self._spaces) - len(self._moves)

        for snapshot, spaces in self._wins.items():
            spots_owned_by_x = 0
            spots_owned_by_o = 0
            spots_not_owned = []
            for space in spaces:
                if self._space_taken(space, 'X'):
                    spots_owned_by_x += 1
                elif self._space_taken(space, 'O'):
                    spots_owned_by_o += 1
                else:
                    spots_not_owned.append(space)

            if ((spots_owned_by_x and spots_owned_by_o) or
                (len(spots_not_owned) >= moves_left)):
                self._wins.pop(snapshot)
            
            if (not self._critical_move and 
                (spots_owned_by_x == 2 or spots_owned_by_o == 2) 
                and spots_not_owned):
                self._critical_move = spots_not_owned[0]
