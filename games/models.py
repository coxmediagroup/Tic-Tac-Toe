import pdb
import ast
import copy
import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from . import GameError


SIZE = 9
EMPTY = ('E', '-')
PLAYER = ('P', 'X')
COMPUTER = ('C', 'O')
DEFAULT_BOARD = [{x: EMPTY} for x in range(0, SIZE)]


class Game(models.Model):
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TicTacToe(Game):
    """
    Tic-Tac-Toe model that includes the logic for running the game.

    To initialize create a new object and then call the move() method
    to advance. You must pass in a valid User Object and position or 
    neither.

    """
    board = models.TextField(max_length=SIZE, default=DEFAULT_BOARD, blank=True)
    player = models.ForeignKey(User, null=True, blank=True)
    last_move = models.IntegerField(null=True, blank=True)

    GameError = GameError

    class Meta(Game.Meta):
        verbose_name = 'Tic Tac Toe'

    def __unicode__(self):
        return '{}'.format(self.board)

    def get_absolute_url(self):
        return reverse('tictactoe-detail', args=[self.pk])

    def move(self, position=None, player=None):
        """
        Object method to initiate a move in the Tic-Tac-Toe game.

        First runs a few sanity checks to make sure it's not a completed game
        and that the method was initialized correctly.

        If position and player are given then the turn must be for the player, if
        neither are given then the turn must be for the computer.

        After each player turn, the computer automatically gets a turn. The computer
        determines it's next move based on the following logic:

        1) Check if player has more than 1 mark, if not, place at center.
        2) If the player has more than one mark, block any attempt at win.
        3) If no attempt at win, place mark in one of the corners.

        """
        # Be sure that the board has been converted to actual list.
        if not isinstance(self.board, list):
            self.board = ast.literal_eval(self.board)

        # Check if the game is still active.
        if self.is_complete:
            return self.GameError('This game is already completed.')

        # Check if player and position were passed signifying player's turn.
        if player and position is not None:
            if position <= len(self.board) and self._is_valid_move(position):
                # The move is valid so go ahead and place the players mark.
                self._place_mark(position, player, save=True)
                
                # Next we initiate a move for the computer by calling move() with no player. 
                self.move()
            else:
                return self.GameError('That move is invalid, please try again.')
        
        # Since no player or position were passed, it's the computers turn.
        else:
            # Make winning move or block the player from his winning move, then check
            # to see if the game was won and if so set is_complete = True.
            if not self._can_win_or_block:
                # Try to capture the center first.
                if self._center_empty:
                    self._place_mark(self._center(), save=True)
                else:
                    # Otherwise just pick an empty space and move there.
                    # TODO: Choose corners or random space.
                    for index, mark in enumerate(self.board):
                        if mark[index] == EMPTY:
                            self._place_mark(index, save=True)
                            break
            
            # Check if the game has been won, if so set the state to complete.
            if self._game_over():
                self.is_complete = True

        # Save the game now that the move is complete.
        self.save()
        return 
            
    def _place_mark(self, position, player=None, save=False):
        """Places a mark down for either a player or computer."""
        if player:
            self.board[position][position] = PLAYER
        else:
            self.board[position][position] = COMPUTER
            self.last_move = position
        if save:
            self.save()
        return

    @property
    def _can_win_or_block(self):
        """Determine if the computer can either win or block in next move."""
        cached = copy.deepcopy(self.board)
        for index, mark in enumerate(self.board):
            if mark[index] == EMPTY:
                self._place_mark(index)
                if self._game_over():
                    return True
            self.board = copy.deepcopy(cached)

        return False

    def _game_over(self, player=False):
        """
        Determine if the game is over or not. First run the function against
        the computer's moves by calling it without player set. The function then
        checks the players moves automatically by calling itself with player.
        """
        won = False

        if not player:
            for path in self._winning_paths:
                if all([path[0].values() == item.values() and item.values()[0] == COMPUTER for item in path]):
                    won = True
                    break

            # Run this function again with player to check player moves.
            if not won:
                self._game_over(player=True)

        elif player:
            for path in self._winning_paths:
                if all([path[0].values() == item.values() and item.values()[0] == PLAYER for item in path]):
                    won = True
                    break

        return won

    @property
    def _winning_paths(self):
        winners = []
        board = [self.board[x:x+3] for x in range(0, len(self.board), 3)]
       
        # Find all horizontal winning paths.
        for row in board:
            winners.append(row)
       
        # Find all vertical winning paths.
        for x in range(0, 3):
            cols = []
            for row in board:
                cols.append(row[x])
            winners.append(cols)

        # Find all diagonal winning paths.
        winners.append([x[i] for i, x in enumerate(board)])
        winners.append([x[-i-1] for i, x in enumerate(board)])

        return winners

    def _is_valid_move(self, position):
        return self.board[position][position] == EMPTY
    
    @property
    def get_board(self):
        """Template helper function to return the board pieces."""
        if not isinstance(self.board, list):
            self.board = ast.literal_eval(self.board)
        return self.board

    @property
    def _corners(self):
        # Could get this programatically but simple enough to just return them.
        return [self.board[i] for i in (0, 2, 6, 8)]

    @property
    def _center_empty(self):
        center = self._center()
        return self.board[center][center] == EMPTY

    @property
    def _size(self):
        return SIZE

    @staticmethod
    def _center():
        return int(((SIZE) - 1) / 2)

