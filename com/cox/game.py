import random
from copy import deepcopy
from com.cox import board

class game(object):
    """
    game class that drives players
    """
    def __init__(self, *args, **kwargs):
        self.board = None
        self.possible_moves = ['00','01','02','10','11','12','20','21','22']
        self.corners = ['00','02','20','22']
        self.center = '11'
    
    def select_letters(self):
        """
        prompt human player to pick a letter
        """        
        choices = ['O','X']
        while(True):
        #while not (selection == 'X' or selection == 'O'):
            selection = raw_input('Choose X OR O\n').upper()
            if selection in choices:
                choices.remove(selection)
                self.board = board.board(human=selection, computer= choices[0])
                break
    
    
    def toss(self):
        """
        toss by virtual coin flip
        to decide who goes first
        """
        # coin flip
        if random.randint(0, 1):
            return 'computer'
        else:
            return 'computer' #change this to human, to make fair game.
    
    def available_moves(self):
        """
        return available moves as list
        """
        return self.possible_moves
    
    def choose_move(self):
        """
        pick a move from possible moves
        """
        valid_move = False
        next_move = ""        
        while not valid_move:
            self.board.print_board()
            next_move = raw_input("your turn buddy!")
            if self.board.is_space_available(next_move):
                valid_move = True
                self.possible_moves.remove(next_move)
            #else:
            #    self.available_moves()
        return next_move
        
    def get_computer_move(self):
        """
        pick computer's next move
        by virtually playing next move for computer
        and human.
        """
        #check if computer can win in next move, pick that move        
        for move in self.possible_moves:
            secret_board = deepcopy(self.board)
            if secret_board.is_space_available(move):
                secret_board.move("computer", move)
            if secret_board.is_winner("computer"):
                return move
        #check if human can win in next move, if pick that move so to block him                
        for move2 in self.possible_moves:
            secret_board2 = deepcopy(self.board)
            if secret_board2.is_space_available(move2):
                secret_board2.move("human", move2)
            if secret_board2.is_winner("human"):
                return move2
        #take one of the corner box
        for crn in self.corners:
            if self.board.is_space_available(crn):
                return crn
        #take center box if available
        if self.board.is_space_available(self.center):
            return self.center
        
        #just pick random available
        for poss_mv in self.possible_moves:
            if self.board.is_space_available(poss_mv):
                return poss_mv
        
    
    def play(self):
        """
        play the game
        """
        print ("Let's play Tic Tac Toe") 
        gm.select_letters()
        #set the next turn by a coin toss
        turn = gm.toss()
        print "{0} will go first".format(turn)       
        while(True):
            if turn == 'human':
                print self.available_moves()
                #move for human
                mv = self.choose_move()
                if self.board.is_space_available(mv):
                    self.board.move(turn, mv)
                #if human won : break
                if self.board.is_winner(turn):
                    self.board.print_board()
                    print "congratulations You have won."
                    break
                if self.board.is_board_full():
                    self.board.print_board()
                    print "It's a tie."
                    break
                turn = 'computer'        
            else:
                #move for computer
                mv = self.get_computer_move()
                if self.board.is_space_available(mv):
                    self.board.move(turn, mv)
                #if computer won : break
                if self.board.is_winner(turn):
                    self.board.print_board()
                    print "Computer has won."
                    break
                if self.board.is_board_full():
                    self.board.print_board()
                    print "It's a tie."                    
                    break
                turn = 'human'
            
if __name__== "__main__":
    gm =  game()
    gm.play()