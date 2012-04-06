#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains all the core functions and objects for game mechanics.
"""
from math import sqrt # for diminishing returns

""" Defines a custom exception for easy differentiation between a game error
and a system error. Game errors can be caught and handled by the UI. System
errors will be generic Exceptions.
"""
class TTTError(Exception):

    def __init__(self, value):
        self.value = str(value)
        
    def __str__(self):
        return self.value
        
# Defines a custom exception for indicating a winner.
class TTTEndGame(Exception):
    def __init__(self, value):
        self.value = str(value)
        
    def __str__(self):
        return self.value
        
# The bread n' butter of the whole game. Holdes everything together in a tight
# little package, completely separate from the UI.
class TTTEngine:
    def __init__(self):
        # the board consists of a nine-element mutable list
        self.board = [ '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
        self.moves = 0 # tracks the number of completed moves
                
        # Define all the different kinds of lines.
        self.LINES = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        
    # Check to see if anyone has won, and if so raise the TTTEndGame exception.
    # If a stalemate has occured, raises the TTTStalemate exception.
    def check_state(self):
        # little shortcut
        b = self.board
        
        # Check for a winner.
        for line in self.LINES:
            if b[line[0]] == b[line[1]] == b[line[2]]:
                winner = 'You'
                if self.moves % 2 == 0:
                    winner = 'I'
        
                raise TTTEndGame('%s won!' % winner)
            
        # No winner, so check for stalemate (all X's and O's).
        if len( ''.join(b).replace('X','').replace('O','') ) == 0:
            raise TTTEndGame('Stalemate!')
            
        # No else because there was no winner and no stalemate.
        
    # given a digit that represents the slot to move into
    def apply_move(self, move):
        # check that move is valid before applying it, raising a TTTError if not
        if not move in range(0,9) or not self.board[ move ].isdigit():
            # the specified slot is taken, so invalid move
            raise TTTError('Please choose an open position.')
            
        if self.moves % 2 == 0:
            # this is X's turn
            self.board[ move ] = 'X'
        else:
            # this is O's turn
            self.board[ move ] = 'O'
            
        self.moves += 1
        
        self.check_state()
        
    # returns a list of any open space on the board
    def get_valid_moves(self):
        avail_moves = []
        for i in range(0,9):
            if self.board[i].isdigit():
                avail_moves.append(i)
        
        return avail_moves
        
    def __highest(self, val1, val2):
        if val1 > val2:
            return val1
        else:
            return val2
            
    def __sum(self, board, row):
        return board[row[0]] + board[row[1]] + board[row[2]]
    
    # Internal function to rate the given move with the current board state.
    # It is assumed that the given move is an available move on the board.
    def __rate_move(self, move, player_value, opp_value):
        if not move in self.get_valid_moves():
            raise Exception('A non-available move was given.')

        # Copy the current board state.
        b = self.board[:]

        # Initialize the highest point value for this move as having no value.
        highest = 0
        
        # Determine whose turn it is.
        token = 'O'
        if self.moves % 2 == 0:
            token = 'X'
            
        # Replace player tokens with numerical values so we can read entire lines easily.
        for i in range(0, 9):
            if not b[i].isdigit():
                if b[i] == token:
                    b[i] = player_value
                else:
                    b[i] = opp_value
            else:
                b[i] = 0

        # Determine which lines the current move is in.
        m_lines = []
        
        # Apply the move to the board copy for checking flat out wins or blocks.
        b[move] = player_value
        
        for line in self.LINES:
            if move in line:
                # Weight player moves that would block an opponent who is about to win.
                if self.__sum(b, line) == 2 * opp_value:
                    for cell in line:
                        if b[cell] == opp_value:
                            b[cell] = player_value
                
                # Weight player moves that are about to win.
                if self.__sum(b, line) == 3 * player_value:
                    for cell in line:
                        if b[cell] == player_value:
                            b[cell] = player_value * 100.0
                
                # Slightly weight empty cells so they're more desirable.
                for cell in line:
                    if b[cell] == 0:
                        b[cell] = opp_value / 100.0
                        
                m_lines.append(line)
        
        # Calculate the highest value line this move would produce.
        for line in m_lines:
            line_total = self.__sum(b, line)
            highest = self.__highest(highest, line_total)
            
        return highest
        
    # Back out the specified move (reset the space and decrement the moves
    # counter. Move is the actual index in the board list.
    def __back_out_move(self, move):
        if not self.board[move].isalpha():
            raise Exception('Space given is not occupied.')
            
        self.board[move] = str(move + 1)
        self.moves -= 1
        
    """ Given a move node and the current game state, generates a weighted move
    tree for any available moves and appends them to the given move node's
    children list. Returns the modified move node.
    """
    def __get_move_tree(self, parent_node, player_value, opp_value):
        move_list = self.get_valid_moves()
        
        if len(move_list) == 0:
            # no more moves, board is currently full so just return
            return parent_node

        # rate each move and determine the best course of action
        for move in move_list:
            move_node = TTTMoveNode(move, self.__rate_move(move, player_value, opp_value))
 
            # On predicted player moves, zero out the weight
            if self.moves % 2 == 0:
                move_node.weight = 0
            
            try:
                self.apply_move(move)
                # Note if the apply_move throws an end game, the recursion stops.
                # Apply diminishing returns on events the farther into predection this goes.
                move_node = self.__get_move_tree(move_node, (player_value / 2.0), (opp_value / 2.0))  
            
            except TTTEndGame:
                pass

            self.__back_out_move(move)
            parent_node.weight += move_node.weight
            parent_node.add_child(move_node)
        
        return parent_node
        
        
    # Returns True if the specified move occurs on a corner. Used for when a
    # tie occurs between multiple moves. Corners are preferred if nothing else.
    def __is_corner(self, move):
        return move in (0, 2, 6, 8)
    
    # Runs the AI to determine the best next move for the CPU.
    def get_best_move(self):
        ''' Manual override for first move seems to iron out some very very slow
        decisions the AI makes when it has too many choices or if
        the game is too vague.
        '''
        if self.moves == 1:
            for pos in self.board:
                # Determine where the opponent has gone.
                if not pos.isdigit():
                    p_move = self.board.index(pos)
                    if self.__is_corner(p_move) or p_move in (1, 3, 5, 7):
                        # Opponent moves to corner, you move to center.
                        return 4
                    
                    else:
                        # Opponent moved to center or to a middle spot, so move to position 0,
                        # top-left corner
                        return 0
                    
            
        # Second special-case: P1 - C5 - P9, AI should choose 2, 4, 6, or 8.
        elif self.moves == 3:
            p_moves = []
            for i in range(0, len(self.board)):
                if not self.board[i].isdigit() and self.board[i] == 'X' and self.__is_corner(i):
                    p_moves.append(i)
                    
            if len(p_moves) == 2:
                diag = { 0: 8, 8: 0, 2: 6, 6: 2 }
                # Only enforce this rule if the two corners are opposite of each other.
                if diag[p_moves[0]] == p_moves[1]:
                    return 5
                
        # start the move tree with a root node move of -1
        moves = self.__get_move_tree(TTTMoveNode(-1, 0), 4, 3) # 4 and 6 are arbitrary weights
            
        # sort descending by weight
        moves.children = sorted(moves.children, key=lambda node: -node.weight)
        
        # debug
        '''
        print '\n----\n'
        for child in moves.children:
            print '%s = %s' % (child.move+1, child.weight)
        '''
        
        # Ties don't matter, so just take the first element regardless.
        return moves.children[0].move
        

# Tracks potential moves, their child moves, and their weights. An optimal
# move is indicated by the path with the highest weight.
class TTTMoveNode:
    def __init__(self, move, weight):
        self.children = []
        self.move = move
        self.weight = weight
        
    def add_child(self, child_node):
        self.children.append(child_node)
        
