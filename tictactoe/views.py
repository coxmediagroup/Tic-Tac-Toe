from django.template import Context, loader
from django.http import HttpResponse
from django.core.cache import cache
from random import choice

class Computer:
    MAX = 'MAX'
    MIN = 'MIN'
    
    def make_move(self, board_instance):
        # logic for counter to opening move, hard-coded to save CPU
        user_moves = 0
        
        for i in range(9):
            if board_instance.board[i] == Board.USER:
                user_moves += 1

        if user_moves == 1:
            # special strategy to counter opening move
            if board_instance.board[0] == Board.USER \
                or board_instance.board[2] == Board.USER \
                or board_instance.board[6] == Board.USER  \
                or board_instance.board[8] == Board.USER: 
                # opening move was a corner
                board_instance.set_mark(4, Board.COMPUTER)
            elif board_instance.board[4] == Board.USER:
                # opening move was the center
                board_instance.set_mark(choice([0, 2, 6, 8]), Board.COMPUTER)
            else: # it was an edge opening
                if board_instance.board[1] == Board.USER:
                    board_instance.set_mark(choice([4, 2, 0, 7]), Board.COMPUTER)
                elif board_instance.board[3] == Board.USER:
                    board_instance.set_mark(choice([4, 6, 0, 5]), Board.COMPUTER)
                elif board_instance.board[5] == Board.USER:
                    board_instance.set_mark(choice([4, 8, 2, 3]), Board.COMPUTER)
                else: # board[7]
                    board_instance.set_mark(choice([4, 8, 6, 1]), Board.COMPUTER)
        else:
            # the remaining logic is for a non-opening move counter... (i.e. the
            # user has made at least two moves)
            move_pos, result = self.max_move(board_instance)
            board_instance.set_mark(move_pos, Board.COMPUTER)

    def max_move(self, board_instance):
        best_result = None
        best_move = None
        
        for m in board_instance.get_open_spaces():
            board_instance.set_mark(m, Board.COMPUTER)
                
            if board_instance.is_game_over():
                result = self.get_result(board_instance)
            else:
                move_pos, result = self.min_move(board_instance)

            board_instance.revert_last_move()
            
            if best_result == None or result > best_result:
                best_result = result
                best_move = m

        return best_move, best_result
        
    def min_move(self, board_instance):
        best_result = None
        best_move = None
        
        for m in board_instance.get_open_spaces():
            board_instance.set_mark(m, Board.USER)
                
            if board_instance.is_game_over():
                result = self.get_result(board_instance)
            else:
                move_pos, result = self.max_move(board_instance)

            board_instance.revert_last_move()
            
            if best_result == None or result < best_result:
                best_result = result
                best_move = m

        return best_move, best_result
        
    def get_result(self, board_instance):
        if board_instance.is_game_over():
            if board_instance.winner == Board.COMPUTER:
                return 1
            elif board_instance.winner == Board.USER:
                return -1
        
        return 0
        
class Board:
    EMPTY = 'not-selected'
    USER = 'user-selected'
    COMPUTER = 'computer-selected'
    
    WINNER_USER = 'winner-user'
    WINNER_COMPUTER = 'winner-computer'
    WINNER_DRAW = 'winner-draw'
    
    EMPTY_BOARD = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]    

    def __init__(self, board = None):
        if board:
            self.board = board
        else:
            self.board = Board.EMPTY_BOARD
            
        self.moves = []
        self.winner = None

    def set_mark(self, position, user):
        self.board[position] = user
        self.moves.append(position)
        
        b = self.board
        
        if (b[0] == b[1] == b[2] and not b[0] == self.EMPTY):
            self.winner = b[0]
        elif (b[3] == b[4] == b[5] and not b[3] == self.EMPTY):
            self.winner = b[3]
        elif (b[6] == b[7] == b[8] and not b[6] == self.EMPTY):
            self.winner = b[6]            
        elif (b[0] == b[3] == b[6] and not b[0] == self.EMPTY):
             self.winner = b[0]            
        elif (b[1] == b[4] == b[7] and not b[1] == self.EMPTY):
             self.winner = b[1]            
        elif (b[2] == b[5] == b[8] and not b[2] == self.EMPTY):
             self.winner = b[2]            
        elif (b[0] == b[4] == b[8] and not b[0] == self.EMPTY):
             self.winner = b[0]            
        elif (b[2] == b[4] == b[6] and not b[2] == self.EMPTY):
             self.winner = b[2]                        
        
    def revert_last_move(self):
        self.board[self.moves.pop()] = Board.EMPTY
        self.winner = None
    
    def get_open_spaces(self):
        open_spaces = []
        
        for i in range(9):
            if self.board[i] == Board.EMPTY:
                open_spaces.append(i)
        
        return open_spaces
        
    def is_game_over(self):
        if self.winner:
            return True
        else:
            for i in range(9):
                if self.board[i] == Board.EMPTY:
                    return False
        
        return True     

def start(request):
    computer = Computer()
    selected_cell = request.GET.get('selected_cell', None)
    current_board = cache.get('board')
    winner = ''
    
    if current_board and selected_cell:
        board_instance = Board(current_board)
    else:
        board_instance = Board()        

    if request.method == 'GET' and selected_cell:
        # ensure the value is not already set (e.g. refresh button was pressed
        # with the GET value in the URL)        
        if not board_instance.board[int(selected_cell)] in (Board.USER, Board.COMPUTER):
            # update the current board with the user's move
            board_instance.set_mark(int(selected_cell), Board.USER)
            
            # check for victory
            if board_instance.is_game_over():
                if board_instance.winner == Board.USER:
                    winner = Board.WINNER_USER
                elif board_instance.winner == Board.COMPUTER:
                    winner = Board.WINNER_COMPUTER
                else:
                    winner = Board.WINNER_DRAW
            else:    
                # follow-up with a move from the computer
                computer.make_move(board_instance)
                
                # check for victory
                if board_instance.is_game_over():
                    if board_instance.winner == Board.USER:
                        winner = Board.WINNER_USER
                    elif board_instance.winner == Board.COMPUTER:
                        winner = Board.WINNER_COMPUTER
                    else:
                        winner = Board.DRAW                
      
    # store the board in cache
    cache.set('board', board_instance.board)
    
    t = loader.get_template('home.html')
    c = Context({
        'board': board_instance.board,
        'winner': winner,
    })
    
    return HttpResponse(t.render(c))