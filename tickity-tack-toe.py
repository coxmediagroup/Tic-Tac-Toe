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


def killcomp_map_check_done():
    global comp_map
    for i in range(0, 3):
        if comp_map[i][0] == comp_map[i][1] == comp_map[i][2] == computer != " " \
        or comp_map[0][i] == comp_map[1][i] == comp_map[2][i] == computer != " ":
            return True

    if comp_map[0][0] == comp_map[1][1] == comp_map[2][2] == computer != " " \
    or comp_map[0][2] == comp_map[1][1] == comp_map[2][0] == computer != " ":
        return True

    if " " not in comp_map[0] and " " not in comp_map[1] and " " not in comp_map[2]:
        print "It is a tie."
        return True

    return False


def which_corner():
    counter = 0
    corner = [1, 3, 7, 9]
    for i in range(0, 3):
        comp_pos = corner[i]
        if comp_pos <= 9 and comp_pos >= 1:
            Y = comp_pos / 3
            X = comp_pos % 3
            if X != 0:
                X -= 1
            else:
                X = 2
                Y -= 1
        if map[Y][X] == " ":
            counter = counter + 1

    return counter


def random_corner():
    global map
    corner = [1, 3, 7, 9]
    a = random.randint(0, 3)
    comp_pos = corner[a]
    if comp_pos <= 9 and comp_pos >= 1:
        Y = comp_pos / 3
        X = comp_pos % 3
        if X != 0:
            X -= 1
        else:
            X = 2
            Y -= 1
    if map[Y][X] == " ":
        map[Y][X] = computer


def place_corner():
    global map
    m = 0
    corner = [1, 3, 7, 9]
    for i in range(0, 3):
        if m is not 1:
            comp_pos = corner[i]
            if comp_pos <= 9 and comp_pos >= 1:
                Y = comp_pos / 3
                X = comp_pos % 3
                if X != 0:
                    X -= 1
                else:
                    X = 2
                    Y -= 1
            if map[Y][X] == " ":
                map[Y][X] = computer
                m = 1


def comp_kill():
    m = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if m != 1:
                if comp_map[2-i][j] == " ":
                    comp_map[2-i][j] = computer
                    comp_done = killcomp_map_check_done()
                    comp_map[2-i][j] = " "
                    if comp_done == True:
                        map[2-i][j] = computer
                        m = 1
                        comp_done = False
                        break
                    comp_done = False
    return m


def computer_moves():
    count = 0
    m = 0
    comp_count = 0
    corner = [1, 3, 7, 9]
    global map
    global comp_map
    comp_done = False
    for i in range(0, 3):
        for j in range(0, 3):
            comp_map[2-i][j] = map[2-i][j]
            if map[2-i][j] == " ":
                count = count + 1

    m = 0

    if count == 9:
        random_corner()
        m = 1

    for i in range(0, 3):
        for j in range(0, 3):
            if m is not 1:
                if comp_map[2-i][j] == " ":
                    comp_map[2-i][j] = player
                    comp_done = comp_map_check_done()
                    m = comp_kill()
                    comp_map[2-i][j] = " "
                    if comp_done is True and m is not 1:
                        map[2-i][j] = computer
                        m = 1
                        comp_done = False
                        break
                    comp_done = False

    if m is not 1:
        m = comp_kill()
        comp_count = which_corner()
        if comp_count >= 0 and m is not 1:
            place_corner()
            m = 1

    if m is not 1:
        if map[1][1] == " ":
            map[1][1] = computer
            m = 1


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
    print "View of the board."
    print_board()
    print
    print turn, "'s turn"
    print

    moved = False

    if computer == turn:
        computer_moves()
        moved = True
        done = check_done()
        if done is not False:
            if turn == "X":
                turn = "O"
            else:
                turn = "X"

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
