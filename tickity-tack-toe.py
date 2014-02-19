# One Player Python Tic-Tac-Toe Game that the computer can not lose


def print_board():
    for i in range(0, 3):
        for j in range(0, 3):
            print map[2-i][j],
            if j != 2:
                print "|",
        print ""


def check_done():
    for i in range(0, 3):
        if map[i][0] == map[i][1] == map[i][2] != " " \
        or map[0][i] == map[1][i] == map[2][i] != " ":
            print turn, "Winner!"
            return True

    if map[0][0] == map[1][1] == map[2][2] != " " \
    or map[0][2] == map[1][1] == map[2][0] != " ":
        print turn, "Winner!"
        return True

    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        print "It is a tie."
        return True

    return False


# Checking the computer map
def comp_map_check_done():
    global comp_map
    for i in range(0, 3):
        if comp_map[i][0] == comp_map[i][1] == comp_map[i][2] == player!= " " \
        or comp_map[0][i] == comp_map[1][i] == comp_map[2][i] == player != " ":
            return True

    if comp_map[0][0] == comp_map[1][1] == comp_map[2][2] == comp_map != " " \
    or comp_map[0][2] == comp_map[1][1] == comp_map[2][0] == player != " ":
        return True

    if " " not in comp_map[0] and " " not in comp_map[1] and " " not in comp_map[2]:
        print "It is a tie."
        return True

    return False


computer = ""
correct_input = False

while correct_input is not True:
    player = raw_input("Please select X or O \n").upper()
    if player == "X":
        computer = "O"
        correct_input = True
    elif player == "O":
        computer = "X"
        correct_input = True
    else:
        print "Wrong input please try again"
        correct_input = False


import random
turn = "X"
map = [[" ", " ", " "],
       [" ", " ", " "],
       [" ", " ", " "]]
done = False
# This is the computers map
comp_map = [[" ", " ", " "],
           [" ", " ", " "],
           [" ", " ", " "]]


while done is not True:
    print_board()

    print turn, "'s turn"
    print

    moved = False
    while moved is not True:
        print "Select a position by picking a number between 1 and 9, see below..."
        print "7|8|9"
        print "4|5|6"
        print "1|2|3"
        print

        try:
            pos = input("Select: ")
            if pos <= 9 and pos >= 1:
                Y = pos / 3
                X = pos % 3
                if X != 0:
                    X -= 1
                else:
                    X = 2
                    Y -= 1

                if map[Y][X] == " ":
                    map[Y][X] = turn
                    moved = True
                    done = check_done()

                    if done is not False:
                        if turn == "X":
                            turn = "O"
                        else:
                            turn = "X"

        except:
            print "You need to add a numeric value"
