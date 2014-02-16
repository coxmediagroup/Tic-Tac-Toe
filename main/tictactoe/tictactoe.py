__author__ = 'henryadam'

import random



def drawBoard(board):
    """
        This function will draw a bootstrap html table based on a sequence received in the argument board
        so that a board (0,1,2,3,4,5,6,7,8,9)    """


    the_board = """
        <div class="row-fluid">
            <div class="offset1 span3 well">
                <h1 class="text-center">%s</h1>
            </div>
            <div class="span3 well">
               <h1 class="text-center">%s</h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center">%s</h1>
            </div>
        </div>
        <div class="row-fluid">
            <div class="offset1 span3 well">
                <h1 class="text-center">%s</h1>
            </div>
            <div class="span3 well">
               <h1 class="text-center">%s</h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center">%s</h1>
            </div>
        </div>
        <div class="row-fluid">
            <div class="offset1 span3 well">
               <h1 class="text-center">%s</h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center">%s</h1>
            </div>
            <div class="span3 well">
                <h1 class="text-center">%s</h1>
            </div>
        </div>

    """ % (board[6],board[7],board[8],board[3],board[4],board[5],board[0],board[1],board[2])

    return(the_board)

