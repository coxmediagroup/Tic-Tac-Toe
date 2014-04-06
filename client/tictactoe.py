from copy import copy

class TicTacToe:

    def __init__(self, board=None, coordinates=None):
        self.board = {}
        self.opponent = 'O'
        self.player = 'X'

        if board:
            self.board = board
        else:
            for i in range(3):
                for j in range(3):
                    self.board[i,j] = None

        if coordinates:
            self.board[coordinates] = self.player
            (self.player, self.opponent) = (self.opponent, self.player)

    def __str__(self):
        output = ""
        for y in range(3):
            for x in range(3):
                output += self.board[x,y] if self.board[x,y] != None else '-'
            output += '\n'
        return output

    def move(self, coordinates):
        self.board[coordinates] = self.player
        (self.player, self.opponent) = (self.opponent, self.player)

    def minmax(self, player):
        if self._won():
            return {'value' : -1, 'coordinates' : None} if player else {'value': 1, 'coordinates' : None}
        elif self._tied():
            return { 'value' : 0, 'coordinates' : None}
        elif player:
            best_move = {'value' : -2, 'coordinates' : None}
            for x,y in self.board:
                if self.board[x,y] == None:
                    new_board = TicTacToe(copy(self.board), (x,y))
                    value = new_board.minmax(not player)['value']
                    if value > best_move['value']:
                        best_move['value'] = value
                        best_move['coordinates'] = (x,y)
            return best_move
        else:
            best_move = { 'value': 2, 'coordinates': None}
            for x,y in self.board:
                if self.board[x,y] == None:
                    new_board = TicTacToe(copy(self.board), (x,y))
                    value = new_board.minmax(not player)['value']
                    if value < best_move['value']:
                        best_move['value'] = value
                        best_move['coordinates'] = (x,y)
            return best_move

    def _tied(self):
        for x,y in self.board:
            if self.board[x,y] == None:
                return False
        return True

    def _won(self):
        # Horizontal wins
        for y in range(3):
            win = []
            for x in range(3):
                if self.board[x,y] == self.opponent:
                    win.append((x,y))
            if(len(win) == 3):
                return win

        # Vertical wins
        for x in range(3):
            win = []
            for y in range(3):
                if self.board[x,y] == self.opponent:
                    win.append((x,y))
            if(len(win) == 3):
                return win

        # Diagonal wins
        win = []
        for y in range(3):
            x = y
            if self.board[x,y] == self.opponent:
                win.append((x,y))
        if len(win) == 3:
            return win

        win = []
        for y in range(3):
            x = 2 - y
            if self.board[x,y] == self.opponent:
                win.append((x,y))
        if len(win) == 3:
            return win

        return None