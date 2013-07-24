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
        selection = ''
        choices = ['O','X']
        while not (selection == 'X' or selection == 'O'):
            selection = raw_input('Choose X OR O').upper()
        self.board = board.board(human=selection, computer= choices.remove(selection))
    
    
    def toss(self):
        # coin flip
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'computer' #change this to human, to make fair game.
    
    def available_moves(self):
        """
        available moves
        """
        print self.possible_moves
    
    def choose_move(self):
        """
        pick a move from possible moves
        """
        valid_move = False
        next_move = ""        
        while not valid_move:
            next_move = raw_input("your turn buddy!")
            if next_move in self.possible_moves:
                self.board.is_space_available(next_move)
                valid_move = True
                self.possible_moves.remove(next_move)
            else:
                self.available_moves()
        return next_move
        
    def get_computer_move(self):
        """
        pick computer's next move
        """
        #check if computer can win in next move, pick that move
        secret_board = deepcopy(self.board)
        for move in self.available_moves():
            secret_board.move(move)
            if secret_board.is_winner():
                return move
        #check if human can win in next move, if pick that move so to block him
        secret_board2 = deepcopy(self.board)
        for move2 in self.available_moves():
            secret_board2.move(move2)
            if secret_board2.is_winner():
                return move2
        #take center box if available
        if self.board.is_space_available(self.center):
            return self.center
        #take one of the corner box
        for crn in self.corners:
            if self.board.is_space_available(crn):
                return crn
        #just pick random available
        for poss_mv in self.possible_moves:
            if self.board.is_space_available(poss_mv):
                return poss_mv
        
    
    def play(self):
        """
        play the game
        """
        print "Let's play Tic Tac Toe" 
        gm.select_letters()       
        while(True):
            #set the next turn by a coin toss
            turn = gm.toss()
            print "{0} will go first".format(turn)            
            if turn == 'human':
                print self.available_moves()
                #move for human
                mv = self.choose_move()
                if self.board.is_space_available(mv):
                    self.board.move("human", mv)                    
                
                #if human won : break
                turn = 'computer'        
            else:
                #move for computer
                #if computer won : break
                turn = 'human'
            
if __name__== "__main__":
    gm =  game()
    gm.play()