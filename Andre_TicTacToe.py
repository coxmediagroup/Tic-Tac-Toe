
board = [[" "," "," "],
         [" "," "," "],
         [" "," "," "]]

turn = "O"

done = False


# This method prints the current state of the board 
def printBoard():
    print (board[0][0] + "|" + board[0][1] + "|" + board[0][2])
    print (board[1][0] + "|" + board[1][1] + "|" + board[1][2])
    print (board[2][0] + "|" + board[2][1] + "|" + board[2][2])

# This methos checks to see if someone has won the game
def checkForWin():
    # Check for a horizontal or vertical win
    for i in range (0,3):
        if board[i][0] == board[i][1] == board[i][2] != " " \
        or board[0][i] == board[1][i] == board[2][i] != " ":
            print (turn, " won that game!")
            return True

    # Check for a diagonal win
    if board[0][0] == board[1][1] == board[2][2] != " " \
    or board[0][2] == board[1][1] == board[2][0] != " ":
        print (turn, " won that game!")
        return True

    # Check to see if there any empty spaces (if so, it's a draw)
    draw = True
    for i in range (0,3):
        for j in range (0,3):
            if board[i][j] == " ":
                return False
    print ("It's a draw!")
    return True

    
def compTurn():
    # Priority 1: check to see if computer has a winning move available
    win = checkBlock("O","O")
    if win == True:
        return

    # priority 2: check to see if computer has a blocking play to make
    block = checkBlock("X","O")
    if block == True:
        return

    # Priority 3: check for a fork
    if board == [["X"," ", " "], [" ", "O", " "], [" "," "," "]]:
        board[2][2] = "O"
        return
    if board == [["X"," ", " "], [" ", "O", " "], [" "," ","X"]]:
        board[0][1] = "O"
        return
    if board == [[" "," ", "X"], [" ", "O", " "], ["X"," "," "]]:
        board[0][1] = "O"
        return

    # Priority 4: Play in the center
    elif board[1][1] == " ":
        board[1][1] = "O"
        return
    
    # Priority 5: Play in an open corner
    elif board[0][0] == " ":
        board[0][0] = "O"
        return
    elif board[2][0] == " ":
        board[2][0] = "O"
        return
    elif board[2][2] == " ":
        board[2][2] = "O"
        return
    elif board[0][2] == " ":
        board[0][2] = "O"
        return
    
    # Last priority: Play in an open side
    elif board[0][1] == " ":
        board[0][1] = "O"
        return
    elif board[1][0] == " ":
        board[1][0] = "O"
        return
    elif board[2][1] == " ":
        board[2][1] = "O"
        return
    elif board[1][2] == " ":
        board[1][2] = "O"
        return

# check if a blocking move is needed
# also called to check whether the computer has a winning play available
def checkBlock(xo,xo2):

    if board[0][0] == xo:
        if board[0][1] == xo and board[0][2] == " ":
            board[0][2] = xo2
            print("xx_")
            return True
        if board[0][2] == xo and board[0][1] == " ":
            board[0][1] = xo2
            print("x x")
            return True
        if board[1][0] == xo and board[2][0] == " ":
            compMove = [2,0]
            board[2][0] = xo2
            print("x|x|_")
            return True
        if board[2][0] == xo and board[1][0] == " ":
            board[1][0] = xo2
            print("x|_|x")
            return True
        if board[1][1] == xo and board[2][2] == " ":
            board[2][2] = xo2
            return True
        if board[2][2] == xo and board[1][1] == " ":
            board[1][1] = xo2
            return True

    if board[1][0] == xo:
        if board[2][0] == xo and board[0][0] == " ":
            board[0][0] = xo2
            return True
        if board[1][1] == xo and board[1][2] == " ":
            board[1][2] = xo2
            return True
        if board[1][2] == xo and board[1][1] == " ":
            board[1][1] = xo2
            return True

    if board[2][0] == xo:
        if board[2][1] == xo and board[2][2] == " ":
            board[2][2] = xo2
            return True
        if board[2][2] == xo and board[2][1] == " ":
            board[2][1] = xo2
            return True
        if board[1][1] == xo and board[0][2] == " ":
            board[0][2] = xo2
            return True
        if board[0][2] == xo and board[1][1] == " ":
            board[1][1] = xo2
            return True

    if board[0][1] == xo:
        if board[0][2] == xo and board[0][0] == " ":
            board[0][0] = xo2
            return True
        if board[1][1] == xo and board[2][1] == " ":
            board[2][1] = xo2
            return True
        if board[2][1] == xo and board[1][1] == " ":
            board[1][1] = xo2
            return True

    if board[0][2] == xo:
        if board[1][2] == xo and board[2][2] == " ":
            board[2][2] = xo2
            return True
        if board[2][2] == xo and board[1][2] == " ":
            board[1][2] = xo2
            return True

    return False




# Main

print("You will be X, I (the computer) will be O.")
first = input("Do you want to go first? Type Y or y for yes, anything else to go second:  ")
if first == "Y" or first == "y":
    turn = "X"

while done != True:
    print (turn, "'s turn")
    print (" ")

    if turn == "O":
        compTurn()
        turn = "X"
    printBoard()

    if turn == "X":
        moved = False
        while moved != True:
            print ("Please play by typing a number between 1 and 9:")
            print ("1|2|3")
            print ("4|5|6")
            print ("7|8|9")
            print ("")
            pos = input("Select: ")
            print("{0}\n".format(pos))
            try:
                pos = int(pos)
                j = int(pos%3)
                i = int((pos-1)/3)
                if board[i][j-1] == " ":
                    board[i][j-1] = turn
                    moved = True
                    printBoard()
                    done = checkForWin()

                    if done == False:
                        turn = "O"

            except:
                print ("You need to input a numerical value")






