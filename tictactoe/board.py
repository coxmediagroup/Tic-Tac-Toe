
class BadMoveError(Exception):
    pass

class Board:
    """ a board for playing tictactoe on """
    def  __init__(self):
        self.board = [[0 for j in range(3)] for i in range(3)]
        self.next_move = 1
        self.moves = []
    
    def move(self,x, y):
        """ make a move x,y
            raises BadMoveError if the move is bad """
        if x >= 3 or y >= 3 or self.board[x][y] != 0:
            raise BadMoveError()
        self.board[x][y] = self.next_move
        self.moves.append((x,y))
        self.next_move *= -1
        
    def unmove(self):
        """ undo the last move on the stack """
        self.next_move *= -1
        move = self.moves.pop()
        self.board[move[0]][move[1]] = 0

    def legal_moves(self):
        """ return a list of legal moves on the current board """
        move_list = []
        for i, row in enumerate(self.board):
            for j, place in enumerate(row):
                if place == 0:
                    move_list.append([i,j])

        return move_list

    def win_check(self):
        """ Check to see if the game is over """
        tie = True
        #check horizontal
        for row in self.board:
            win = list_check(row)
            if win:
                return win
            if win is None:
                tie = False
        #check vertical
        for i in range(3):
            win = list_check([row[i] for row in self.board])
            if win:
                return win
            if win is None:
                tie = False

       #check diagonal
        win = list_check([self.board[i][i] for i in range(3)])
        if win:
            return win
        if win is None:
            tie = False
        win = list_check([self.board[i][2-i] for i in range(3)])
        if win:
            return win
        if tie or win is None:
            return None
        return 0
        
    def key(self):
        """ return a dictionary key to to find this board """
        fsboard = ''
        for row in self.board:
            for pos in row:
                if pos == -1:
                    fsboard += 'O'
                elif pos == 0:
                    fsboard += '_'
                else:
                    fsboard += 'X'
        return fsboard
    
    def __str__(self):
        output = ''
        line  = ''
        for i in range(3):
            line  += '--'
        line += '-'
        output += line + '\n'
        for row in self.board:
            output += '|'
            for pos in row:
                if pos == 1:
                    output += 'X|'
                elif pos == 0:
                    output += ' |'
                elif pos == -1:
                    output += 'O|'
            output += '\n' + line + '\n'
        return output

def list_check(l):
    """ if the game isn't over return None
        otherwise return the winner or 0 if it is a tie """
    fm = None
    open_move = False
    for n in l:
        if fm is None:
            if n == 0:
                open_move = True
            else:
                fm = n
        else:
            if n == 0:
                open_move = True
            elif n != fm:
                return 0

    if open_move:
        return None
    return fm


