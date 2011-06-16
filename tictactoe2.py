import operator, sys, random, time
from random import choice

def checkwinner(wincombos, check):
    # Set the array element variables
    a,b,c = 0,1,2

    #Loop through wincombos to check winner
    while a <= 21:
        combo = [wincombos[a], wincombos[b], wincombos[c]]

        # If we have three 'X' or 'O' we have a winner
        if combo.count(check) == 3:
            status = 1
            break
        elif combo.count(check) == 2 and check == "X":
            if combo.count("O") > 0:
                status = 2
        else:
            status = 0

        # Iterate to the next combo
        a+=3
        b+=3
        c+=3

    # Return status of the game
    return status

def is_valid_move(spaces, n):
    if spaces.count(n) == 0:
        return False
    return True

def make_play(board, spaces, wincombos, player, n):
    # set X for human, or O for computer
    if player == 1:
        symbol = "X"
    else:  
        symbol = "O"
    # Check if block is used.
    while not is_valid_move(spaces, n):
        print "\n%s: Invalid position" % player
        n = get_player_input()

    # Remove block from spaces array
    spaces = spaces.remove(n)

    # Replace block with check mark in board
    board = board.replace(str(n), symbol)

    # Replace space with player symbol in wincombos array
    for c in range(len(wincombos)):
        if wincombos[c] == n:
            wincombos[c] = symbol

    # Run the checkwinner function
    status = checkwinner(wincombos, symbol)
    return board, status

def evalPossibleMoves(spaces, wincombos, player):
    outcomes = [[], [], []]
    test_spaces = spaces[:]
    for s in spaces:
        test_spaces.remove(s)
        test_wc = []
        for e in wincombos:
            if e != s:
                test_wc.append(e)
            else:
                test_wc.append(player)
        status = checkwinner(test_wc, player)
        outcomes[status].append(s)
        recheck = evalPossibleMoves(test_spaces, test_wc, player)
        if recheck[1]:
            outcomes[2].append(s)
    outcomes_cleaned = []
    for o in outcomes:
        outcomes_cleaned.append(list(set(o)))
    return outcomes_cleaned

def get_computer_input(board, spaces, wincombos):
    human_can_win = evalPossibleMoves(spaces, wincombos, "X")
    computer_can_win = evalPossibleMoves(spaces, wincombos, "O")
    #print "hcw: %s" % human_can_win
    #print "ccw: %s" % computer_can_win
    if computer_can_win[1]:
        # make winning move for computer
        return choice(computer_can_win[1])
    if human_can_win[1]:
        # block winning move of human
        return choice(human_can_win[1])
    if computer_can_win[2]:
        selection = find_elev_space(spaces, computer_can_win[2])
    elif human_can_win[2]:
        selection = find_elev_space(spaces, human_can_win[2])
    else:
        selection = find_elev_space(spaces, [])
    return selection

def find_elev_space(spaces, choices):
    corners = [s for s in spaces if s in [1, 3, 7, 9]]
    if 5 in spaces:
        return 5
    elif len(corners) == 2:
        return choice([s for s in spaces if s in [2,4,6,8]])
    elif corners:
        for e in corners:
            if e in choices:
                return e
        return choice(corners)
    else:
        return choice(spaces)

def get_player_input():
    try:
        position = int(raw_input('\nHuman player: which numbered position do you want to play? '))
    except ValueError:
        print "Invalid input"
        position = get_player_input()
    return position

def playttt():
    """main game play function"""
    board = " 1 | 2 | 3\n-----------\n 4 | 5 | 6\n-----------\n 7 | 8 | 9"
    wincombos=[1,2,3,4,5,6,7,8,9,1,4,7,2,5,8,3,6,9,1,5,9,3,5,7]
    spaces=range(1,10)

    while True:
        player = len(spaces)%2
        if player == 1:
            player = 2
            position = get_computer_input(board, spaces, wincombos)
        else:
            player = 1
            position = get_player_input()

        board,status = make_play(board, spaces, wincombos, player, position)

        if status == 1:
            print '\n\nPlayer ' + str(player) + ' is the winner!!!'
            print board
            break
        elif len(spaces) == 0:
            print "No more spaces left. Game ends in a TIE!!!"
            print board
            break
        else:
            if player == 2:
                print board
            continue

if __name__ == "__main__":
    playttt()

