

# ************** Game Mechanics Functions *********************

def playerMove(game_board):
    '''
    Prompts for move, checks for valid input, checks if the move is in an empty space, returns the move.
    Args: 
        game_board - list containing current gameboard
    Returns:
        move_input - integer between 1 and 9
    Raises: 
        ValueError - if input is not an integer
    '''

    move_input = raw_input("Enter Move: ")    # input the move
    switch = "off"

    # check for a valid move
    while switch == "off":
        try:
            move_input = int(move_input)    # Checking for valid input
        except ValueError:
            move_input = raw_input("Not a number.  Please enter a number 1-9:")    # Try again
        else:
            if 0 < move_input < 10 and game_board[move_input - 1] == " " :    # Checking against game_board
                switch = "on" 
            else:
                move_input = raw_input("Input a valid move:  ")    # Try again
    return move_input


def winCheck(game_board, a, b):
    '''
    Defines rows to check, checks for multiple conditions: winner, win now, block now, searches for empty spot (AI)
    Args:
        game_board - list containing current gameboard
        a - primary search item in gameboard, typically current player
        b - secondary search item in gameboard, can be the same as a
    Returns:
        winner - returns [boolean, row or move]
    '''

    winning_rows = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (6, 4, 2)]    # Rows to check
    winner = [False, "none"]    # Setting switch to False, none

    if a == b:   
        condition = 3    # if a == b, check for a winner now
    else:        
        condition = 2    # otherwise, check for other conditions (AI move to win, move to block, etc.)

    for row in winning_rows:    # looping through each winning row
        row_check_dict = {"X":0, "O":0, " ":0}    # blanking out row check dictionary
        for each in row:
            slot = game_board[each]
            row_check_dict[slot] = row_check_dict[slot] + 1         # counting number of X, O, and blank spots
            if row_check_dict[a] == condition and row_check_dict[b] >= 1 and condition == 2:   # if row satisfies condition (AI)
                for each in row:              # this section only applies to the AI search
                    winner = game_board[each]
                    if winner == " ":           # AI is searching for an empty spot to move
                        move = each + 1
                        break
                    else:                     # no empty spot found
                        move = "none"        
                winner = [True, move]
            if row_check_dict[a] == condition and row_check_dict[b] >= 1 and condition == 3:   # we have a winner (either player)
                winner = [True, row]
            if winner == True:    # found our answer (either AI move or there is a winner), no need to keep searching
                break

    return winner


# ************** Game AI Functions ***************************

def AIMove(game_board, player_turn, opponent_turn, turn, previous_move):
    '''
    Searches for best AI_Move based on the following rules and exceptions: 
    Win, block, center, block double moves, corner, anywhere
    Args: 
        game_board - list containing current gameboard
        player_turn - current player turn (AI)
        opponent_turn - other player turn (human)
        turn - turn number
        previous_move - last move by human player
    Returns:
        AI_Move - number to be sent to playerMove
    '''

    # AI Rules: 1. Win, 2. Block, 3. Take Center, 4. Block corner double move, 
    # 5. Block t double move, 6. Take the corner, 7. Go anywhere

    win = winCheck(game_board, player_turn, " ")      # check to see if AI can win (Rule 1, win)
    block = winCheck(game_board, opponent_turn, " ")  # check to see if human can win (Rule 2, block)
    AI_Move = 'unfilled'


    if win[0] == True:           # if AI can win, move to win (Rule 1, win)
        AI_Move = win[1]
    elif block[0] == True:       # if human can win next move, block (Rule 2, block)
        AI_Move = block[1]
    elif game_board[4] == " ":   # if center is empty, take it (Rule 3, center)
        AI_Move = 5

        # the following elif statements check for the threat of a 
        # double move to start the game (Rule 4, corner double move)
    elif (turn / 2 <= 2) and (game_board[0] == opponent_turn and game_board[8] == opponent_turn):    # checking each diagonal
        if game_board[1] == " ":
            AI_Move = 2
        elif game_board[3] == " ":
            AI_Move = 4
        elif game_board[5] == " ":
            AI_Move = 6
    elif (turn / 2 <= 2) and (game_board[2] == opponent_turn and game_board[6] == opponent_turn):    
        AI_Move = 2
    elif (turn / 2 <= 2) and (game_board[1] == opponent_turn and game_board[6] == opponent_turn):    
        AI_Move = 1
    elif (turn / 2 <= 2) and (game_board[3] == opponent_turn and game_board[8] == opponent_turn):
        AI_Move = 1
    elif (turn / 2 <= 2) and (game_board[3] == opponent_turn and game_board[2] == opponent_turn):
        AI_Move = 1

        # the following two elif statements check to see if the 
        # human moved in one of the 't' positions (Rule 5, t double move)
    elif previous_move == 4 or previous_move == 6:
        potential_move = [previous_move - 3, previous_move + 3]
        for each in potential_move:
            if game_board[each - 1] == " ":
                AI_Move = each
    elif previous_move == 2 or previous_move == 8:
        potential_move = [previous_move - 1, previous_move + 1]
        for each in potential_move:
            if game_board[each - 1 ] == " ":
                AI_Move = each

        # if none of the above are met, try to move in the corner (Rule 6, corner), 
        # otherwise just move anywhere (Rule 7, anywhere)
    if AI_Move == 'unfilled':
        potential_move = [0, 2, 6, 8, 1, 3, 5, 7, 4]
        for each in potential_move:
            if game_board[each - 1] == " ":
                AI_Move = each
                break

    return AI_Move




# ************** Game Display Functions *********************

def displayBoard(game_board):
    '''
    Simple text display of game board. Empty squares are numbers, filled squares display their owner.
    Args:
        game_board - list containing current gameboard
    Returns:
        none
    '''

    bars = "__________"    # horizontal line
    counter = 1
    for each in game_board:
        if each != " ":    # Filled spots show their owner
            print each,
        else:
            print counter,    # Empty spots are numbered for ease of play
        if counter % 3 != 0:    # Vertical lines only on the inside
            print "|",
        else:
            print ""
            if counter < 7:
                print bars            
        counter +=1

