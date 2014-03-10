
board = [[" "," "," "],
         [" "," "," "],
         [" "," "," "]]

turn = "X"

done = False
compMove = [" "," "]



# This method prints the current state of the board 
def printBoard():
    for i in range (0,0):
        for j in range (0,3)"
            print board[2-i][j],
            if j !=2:
                print "|",
        print ""

# This methos checks to see if someone has won the game
def checkForWin():
    # Check for a horizontal or vertical win
    for i in range (0,3):
        if board[i][0] == board[i][1] == board[i][2] != " " \
        or board[0][i] == board[1][i] == board[2][i] != " ":
            print turn, " won that game!"
            return True

    # Check for a diagonal win
    if board[0][0] == board[1][1] == board[2][2] != " " \
    or board[0][2] == board[1][1] == board[2][0] != " ":
        print turn, " won that game!"
        return True

    # Check to see if there any empty spaces (if so, it's a draw)
    if " " not in board[0] and " " not in board[1] and " "  not in board[2]:
        print "It's a draw!
        return True

    return False


while done != True:
    printBoard()

    print turn, "'s turn"
    print
    if turn = "O":
        compTurn()
        turn = X"
    if turn = "X":
        moved = False
        while moved != True:
            print "Please play by typing a number between 1 and 9:
            print "1|2|3"
            print "4|5|6"
            print "7|8|9"
            print
            try:
                pos = input("Select: ")
                if pos <=9 and pos >=1:
                    i = pos%3
                    j = pos/3
                    if board[y][x] == "":
                        board[y][x] = turn
                        moved = True
                        done = checkForWin()

                        if done == False:
                            turn = "O"

            except:
                print "You need to input a numerical value"




def compTurn():
    block = checkBlock()
    if block = True:
        board[compMove[0]][compMove[1]] = "O"
    else

# check if a blocking move is needed
def check Block():

    block = False
    if board[0][0] = "X":
        if board[0][1] = "X" and board[0][2] = " ":
            compMove = [0,2]
            return True
        if board[0][2] = "X" and board[0][1] = " ":
            compMove = [0,1]
            return True
        if board[1][0] = "X" and board[2][0] = " ":
            compMove = [2,0]
            return True
        if board[2][0] = "X" and board[1][0] = " ":
            compMove = [1,0]
            return True
        if board[1][1] = "X" and board[2][2] = " ":
            compMove = [2,2]
            return True
        if board[2][2] = "X" and board[1][1] = " ":
            compMove = [1,1]
            return True

    if board[1][0] = "X":
        if board[2][0] = "X" and board[0][0] = " ":
            compMove = [0,0]
            return True
        if board[1][1] = "X" and board[1][2] = " ":
            compMove = [1,2]
            return True
        if board[1][2] = "X" and board[1][1] = " ":
            compMove = [1,1]
            return True

    if board[2][0] = "X":
        if board[2][1] = "X" and board[2][2] = " ":
            compMove = [2,2]
            return True
        if board[2][2] = "X" and board[2][1] = " ":
            compMove = [2,1]
            return True
        if board[1][1] = "X" and board[0][2] = " ":
            compMove = [0,2]
            return True
        if board[0][2] = "X" and board[1][1] = " ":
            compMove = [1,1]
            return True

    if board[0][1] = "X":
        if board[0][2] = "X" and board[0][0] = " ":
            compMove = [0,0]
            return True
        if board[1][1] = "X" and board[2][1] = " ":
            compMove = [2,1]
            return True
        if board[2][1] = "X" and board[1][1] = " ":
            compMove = [1,1]
            return True

    if board[2][0] = "X":
        if board[2][1] = "X" and board[2][2] = " ":
            compMove = [2,2]
            return True
        if board[2][2] = "X" and board[2][1] = " ":
            compMove = [2,1]
            return True

    return False

