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
        print "\nInvalid position"
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

def get_computer_input(board, spaces, wincombos):
    for s in spaces:
        board = board.replace(str(s), "X")
        test_wc = []
        for e in wincombos:
            if e != s:
                test_wc.append(e)
            else:
                test_wc.append("X")
        print test_wc
        status = checkwinner(test_wc, "X")
        if status == 1:
            return s
    #import pdb; pdb.set_trace()
    if 5 in spaces:
        return 5
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
    #print "NOTE: Numbers correspond to board play positions, left to right, top to bottom."
    board = " 1 | 2 | 3\n-----------\n 4 | 5 | 6\n-----------\n 7 | 8 | 9"
    wincombos=[1,2,3,4,5,6,7,8,9,1,4,7,2,5,8,3,6,9,1,5,9,3,5,7]
    spaces=range(1,10)
    print "\n"+board

    while True:
        player = len(spaces)%2 +1
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

