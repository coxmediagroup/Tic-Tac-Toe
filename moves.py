### Tic Tac Toe strategy module by James Robey

#This module offers a class to represent a 3d tic-tac-toe field.
#A "field" is the complete grid, while a "board" is a given 2D
#tic-tac-toe game inside of the field.

#vectors_to_check is an exhaustive list of the 
#vector which may be a part of 
# The format of the below is (x, y, z (board #))



class Field:
    """ I store a "field" (three tic tac toe boards) that along with
        tables indicating all possible winning moves will be 
        used to determine the move the computer should make next.
    """
    
    vectors_to_check = (
        #2D vectors ------------

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

        #diagonals_board_0_2d
        ((0, 0, 0), (1, 1, 0), (2, 2, 0)),
        ((0, 2, 0), (1, 1, 0), (2, 0, 0)),

        #diagonals_board_1_2d
        ((0, 0, 1), (1, 1, 1), (2, 2, 1)),
        ((0, 2, 1), (1, 1, 1), (2, 0, 1)),

        #diagonals_board_2_2d
        ((0, 0, 2), (1, 1, 2), (2, 2, 2)),
        ((0, 2, 2), (1, 1, 2), (2, 0, 2)),

        #3d Vectors ------------

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
    )
    
    def __init__(self, field):
        #self.field = field
        
        self.field = [
                        [
                            [1,1,0],
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
                     
    def determineMove(self):
        """ This implements the decision method to enact a computer player at 
            3D Tic Tac Toe. Using the vectors_to_check list of lists, iterate 
            through each vector, comparing it to the existing values at that vector
            looking first for vectors that add up to either 2 or -2 (indicative of 
            wins or almost losing situations). If we find those we have our move.
            If we don't find them, make a move the first place we can make a 
            two, or a2 one if there are no ones.
        """
        
        score_of_ones = []
        score_of_twos = []
        score_of_neg_twos = []
        score_of_neg_ones = []
        for vector in self.vectors_to_check:
            score = sum([self.field[point[0]][point[1]][point[2]] for point in vector])
            
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
            elif score == -1:    
                score_of_neg_ones.append(vector)        
                

        #finally, analyze result of search and make move based on it.
        print "score_of_ones"
        print score_of_ones
        print
        print "score_of_neg_ones"
        print score_of_neg_ones
        print
        print "score_of_twos"
        print score_of_twos
        print
        print "score_of_neg_twos"
        print score_of_neg_twos
        print
        
        return moveToMake

if __name__ == "__main__":
    f = Field()
    f.determineMove()
    
    
    