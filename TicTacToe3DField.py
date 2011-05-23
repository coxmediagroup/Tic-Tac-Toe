### Tic Tac Toe strategy module by James Robey

#This module offers a class to represent a 3d tic-tac-toe field.
#A "field" is the complete grid, while a "board" is a given 2D
#tic-tac-toe game inside of the field.

class TicTacToe3DField:
    """ I store a "field" (three tic tac toe boards) that along with
        tables indicating all possible winning moves will be 
        used to determine the move the computer should make next.
    """
    
    #set up for a default game
    default_game = [
        [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ],
        [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ],
        [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ],
    ]
    
    #a list of all possible winning vectors through the 3x3x3 cube, in specific order! (diagonals first)
    vectors_to_check = (
        #2D vectors diagonals ------------
        
        #diagonals_board_0_2d
        ((0, 0, 0), (1, 1, 0), (2, 2, 0)),
        ((0, 2, 0), (1, 1, 0), (2, 0, 0)),

        #diagonals_board_1_2d
        ((0, 0, 1), (1, 1, 1), (2, 2, 1)),
        ((0, 2, 1), (1, 1, 1), (2, 0, 1)),

        #diagonals_board_2_2d
        ((0, 0, 2), (1, 1, 2), (2, 2, 2)),
        ((0, 2, 2), (1, 1, 2), (2, 0, 2)),
        
        #3D Vectors diagonal ------------
        
        #up_to_down_diagonal_top_to_bottom_3d
        ((0, 0, 0), (0, 1, 1), (0, 2, 2)),
        ((1, 0, 0), (1, 1, 1), (1, 2, 2)),
        ((2, 0, 0), (2, 1, 1), (2, 2, 2)),

        #up_to_down_diagonal_bottom_to_top_3d
        ((0, 2, 0), (0, 2, 1), (0, 0, 2)),
        ((1, 2, 0), (1, 1, 1), (1, 0, 2)),
        ((2, 2, 0), (2, 1, 1), (2, 0, 2)),

        #up_to_down_diagonal_left_to_right_3d
        ((0, 0, 0), (1, 0, 1), (2, 0, 2)),
        ((0, 1, 0), (1, 1, 1), (2, 1, 2)),
        ((0, 2, 0), (1, 2, 1), (2, 2, 2)),

        #up_to_down_diagonal_right_to_left_3d
        ((2, 0, 0), (1, 0, 1), (0, 0, 2)),
        ((2, 1, 0), (1, 1, 1), (0, 1, 2)),
        ((2, 2, 0), (1, 2, 1), (0, 2, 2)),

        #up_to_down_diagonal_cross_center_3d
        ((0, 0, 0), (1, 1, 1), (2, 2, 2)),
        ((0, 2, 2), (1, 1, 1), (2, 0, 2)),
        
        #2D vectors flat ------------

        #left_to_right_board_0_2d
        ((0, 0, 0), (1, 0, 0), (2, 0, 0)),
        ((0, 1, 0), (1, 1, 0), (2, 1, 0)),
        ((0, 2, 0), (1, 2, 0), (2, 2, 0)),

        #left_to_right_board_1_2d
        ((0, 0, 1), (1, 0, 1), (2, 0, 1)),
        ((0, 1, 1), (1, 1, 1), (2, 1, 1)),
        ((0, 2, 1), (1, 2, 1), (2, 2, 1)),

        #left_to_right_board_2_2d
        ((0, 0, 2), (1, 0, 2), (2, 0, 2)),
        ((0, 1, 2), (1, 1, 2), (2, 1, 2)),
        ((0, 2, 2), (1, 2, 2), (2, 2, 2)),

        #top_to_bottom_board_0_2d
        ((0, 0, 0), (0, 1, 0), (0, 2, 0)),
        ((1, 0, 0), (1, 1, 0), (1, 2, 0)),
        ((2, 0, 0), (2, 1, 0), (2, 2, 0)),

        #top_to_bottom_board_1_2d
        ((0, 0, 1), (0, 1, 1), (0, 2, 1)),
        ((1, 0, 1), (1, 1, 1), (1, 2, 1)),
        ((2, 0, 1), (2, 1, 1), (2, 2, 1)),

        #top_to_bottom_board_2_2d
        ((0, 0, 2), (0, 1, 2), (0, 2, 2)),
        ((1, 0, 2), (1, 1, 2), (1, 2, 2)),
        ((2, 0, 2), (2, 1, 2), (2, 2, 2)),

        #3D Vectors flat ------------

        #up_to_down_left_to_right_top_3d
        ((0, 0, 0), (0, 0, 1), (0, 0, 2)),
        ((1, 0, 0), (1, 0, 1), (1, 0, 2)),
        ((2, 0, 0), (2, 0, 1), (2, 0, 2)),

        #up_to_down_left_to_right_middle_3d
        ((0, 1, 0), (0, 1, 1), (0, 1, 2)),
        ((1, 1, 0), (1, 1, 1), (1, 1, 2)),
        ((2, 1, 0), (2, 1, 1), (2, 1, 2)),

        #up_to_down_left_to_right_bottom_3d
        ((0, 2, 0), (0, 2, 1), (0, 2, 2)),
        ((1, 2, 0), (1, 2, 1), (1, 2, 2)),
        ((2, 2, 0), (2, 2, 1), (2, 2, 2)),
    )
    
    def __init__(self, game=None):
        """ initialize from the incoming structure, or use a default """
        if game:
            self.game = game
        else:
            self.game = self.default_game
            
    def determineMove(self):
        """ This implements the decision method to enact a computer player at 
            3D Tic Tac Toe. Using the vectors_to_check list of lists, iterate 
            through each vector, comparing it to the existing values at that vector
            looking first for vectors that add up to either 2 or -2 (indicative of 
            wins or almost losing situations). If we find those we have our move.
            If we don't find them, make a move the first place we can make a 
            two, or a2 one if there are no ones.
        """
        
        #arrays to hold the vector that might be a good move
        score_of_neg_twos = []
        score_of_twos = []
        score_of_neg_ones = []
        score_of_ones = []
        
        for vector in self.vectors_to_check:
            #note that the array is [board, y, x] while vectors are x, y, board
            
            #if the row is filled (with 1 or -1, i.e. are no zeros) then skip the row
            if not [1 for point in vector if self.game[point[2]][point[1]][point[0]] == 0]:
                continue
           
            #if the row is not filled, (has an open zero) then determine it's score
            score = sum([self.game[point[2]][point[1]][point[0]] for point in vector])
            
            #if we have a winnning move
            if score == 2:    
                score_of_twos.append(vector)
                
            #if we find they can make a winning move next
            elif score == -2:   
                score_of_neg_twos.append(vector)
                
            #if we find somewhere beneficial for us to block opponent
            elif score == -1:    
                score_of_neg_ones.append(vector)
            
            #if we find somewhere beneficial for us to go
            elif score == 1:    
                score_of_ones.append(vector)        

        #analyze the scores of each vector evaluated, looking for the best match
        vector_to_evaluate = None
        
        #any wins?
        if score_of_twos:
            vector_to_evaluate = score_of_twos[0]
            
        #are they about to win?
        elif score_of_neg_twos:
            vector_to_evaluate = score_of_neg_twos[0]
            
        #can we help our selves?
        elif score_of_ones:
            vector_to_evaluate = score_of_ones[0]
                
        #can we stop them?
        elif score_of_neg_ones:
            vector_to_evaluate = score_of_neg_ones[0]

        #if we have detected a good move
        for point in vector_to_evaluate:
            if self.game[point[2]][point[1]][point[0]] == 0:
                moveToMake = point     
                            
        #make the move decided upon
        self.game[moveToMake[2]][moveToMake[1]][moveToMake[0]] = 1
                
        return self.game

if __name__ == "__main__":
    ttt = TicTacToe3DField()
    print ttt.determineMove()
    
    
    