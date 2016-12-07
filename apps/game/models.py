from django.db import models

class Game(models.Model):
    '''Models a tic-tac-toe game with a human and AI player. Keeps track of Django's session id so a game in progress can be restarted.
    '''
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    session_id = models.CharField(max_length=32)
    board_str = models.CharField(max_length=54, default=[None]*9) # max length: [None, None, None, None, None, None, None, None, None]
    player_human = models.CharField(max_length=1, default='X') # X, O
    player_AI = models.CharField(max_length=1, default='O') # X, O
    winner = models.CharField(max_length=4, null=True, default=None) # X, O, cat

    def get_board(self):
        '''Returns the tic-tac-toe board as a Python list object.
        '''
        return eval(self.board_str)

    def get_winner(self, board=None):
        '''Returns winner of game. Returns None if no winner.
        '''
        if board == None:
            board = self.get_board()

        if (((board[3] == board[4] == board[5])
          or (board[1] == board[4] == board[7])
          or (board[0] == board[4] == board[8])
          or (board[2] == board[4] == board[6]))
          and board[4] is not None):
            return board[4] # center

        elif (((board[0] == board[1] == board[2])
            or (board[0] == board[3] == board[6]))
            and board[0] is not None):
            return board[0] # top left

        elif (((board[6] == board[7] == board[8])
            or (board[2] == board[5] == board[8]))
            and board[8] is not None):
            return board[8] # bottom right

    def is_tie(self):
        '''Returns True if the game has ended in a tie.
        '''
        if not self.get_winner():
            return None not in self.get_board()

    def get_possible_moves(self, board=None):
        '''Returns a list of all open spaces on the board.
        '''
        if board == None:
            board = self.get_board()
        return [i for i, space in enumerate(board) if space==None]

    def get_winning_moves(self, board=None):
        '''Returns a dictionary of lists with players as keys and lists of winning moves as values.
        '''
        if board == None:
            board = self.get_board()
        player_human_moves = list()
        player_AI_moves = list()
        for space in self.get_possible_moves(board=board):
            board_copy = board[:]
            board_copy[space] = self.player_human
            if self.get_winner(board=board_copy) == self.player_human:
                player_human_moves.append(space)
            board_copy[space] = self.player_AI
            if self.get_winner(board=board_copy) == self.player_AI:
                player_AI_moves.append(space)
        return {self.player_human: player_human_moves,
                self.player_AI: player_AI_moves}

    def get_fork_moves(self):
        '''Returns a dictionary of lists with players as keys and lists of fork moves as values. Fork moves are those which can force a win on the following turn.
        '''
        player_human_moves = list()
        player_AI_moves = list()
        for space in self.get_possible_moves():
            board = self.get_board()
            board[space] = self.player_human
            winning_dict = self.get_winning_moves(board=board)
            if len(winning_dict[self.player_human]) > 1:
                player_human_moves.append(space)
            board[space] = self.player_AI
            winning_dict = self.get_winning_moves(board=board)
            if len(winning_dict[self.player_AI]) > 1:
                player_AI_moves.append(space)
        return {self.player_human: player_human_moves, self.player_AI: player_AI_moves}

    def make_move(self, player, space):
        '''Makes a move by adding player's letter to board and updating database.
        '''
        board = self.get_board()
        board[space] = player
        self.board_str = str(board)
        self.save()

    def __unicode__(self):
        '''Shows a string representation of the board.
        '''
        return self.board_str