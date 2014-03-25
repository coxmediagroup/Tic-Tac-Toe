# Matthew Haley, tic-tac-toe game submission
# email: matthew.d.haley@gmail.com
# github: https://github.com/uncertainsound
# Purpose: Make a tic-tac-toe game with an AI that will never lose

from gtnwfunctions import *

# ************** Pre-game business *************************

# player chooses X or O
turn_select = raw_input("Greetings Professor Falken.  Would you like to go first? ")


# check for valid input and assign human player
switch = False
while switch == False:
    turn_select = turn_select.lower()  # yes, YES, Yes, yEs, etc. are all valid inputs for yes
    if turn_select[0] == "y":          # checking the first letter only (y or n)
        print "You will be X."
        human_player = 1
        switch = True                   # switch breaks the loop
    elif turn_select[0] == "n":
        print "You will be O."
        human_player = 0
        switch = True
    else:
        turn_select = raw_input("Would you like to go first? Please enter yes or no. ")    # Not valid input, try again


game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank


# Setting up some variables for the first turn
win_condition = False     # No one has won yet
turn = 0                  # setting turn to 0, will become 1 at beginning of main gameplay
player_turn = "X"         # current player turn, whoever is moving THIS turn (human or AI)
opponent_turn = "O"       # other player turn, whoever isn't moving this turn (human or AI)
previous_move = "none"    # No moves yet, so no previous moves


# ************** Main Gameplay ***********************************

while win_condition == False:    # main gameplay takes place within this loop
    turn += 1                                    # changes turn count
    displayBoard(game_board)                     # displays tic-tac-toe board

    print "************ Player turn = ", player_turn

    # checking to see if it is human or AI turn
    if human_player == (turn % 2):
        move = playerMove(game_board)            # human's turn, gets move
    else:
        move = AIMove(game_board, player_turn, opponent_turn, turn, previous_move)       # AI's turn, gets move

    game_board[move - 1] = player_turn           # puts move into game board
    winner = winCheck(game_board, player_turn, player_turn)         # check for win
    win_condition = winner[0]                    #winCheck returns (True or False, row)
 
    if player_turn == "X":  # switching player and opponent turn
        player_turn = "O"
        opponent_turn = "X"
    else:
        player_turn = "X"
        opponent_turn = "O"

    previous_move = move       # recording last move for AI
    if turn == 9:
       break


# if there is a winner or tie, loop is broken and the following is displayed
print "******* GAME END  *********"
if win_condition == True:
    print "%s wins" % opponent_turn
else:
    print "The only winning move is to not play."

displayBoard(game_board)
