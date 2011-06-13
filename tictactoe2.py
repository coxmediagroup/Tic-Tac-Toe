import operator, sys, random, time

def checkwinner(wincombos,check):
    # Set the array element variables
    a,b,c=0,1,2

    #Loop through wincombos to check winner
    while a<=21:
        combo = [wincombos[a],wincombos[b],wincombos[c]]

        # If we have three 'X' or 'O' we have a winner
        if combo.count(check) == 3:
            status =1
            break
        else:
            status =0

        # Iterate to the next combo
        a+=3
        b+=3
        c+=3

    # Return status of the game
    return status

def make_play(board,spaces,wincombos,player,n):
    # set X for player one, or O for player 2
    if player==1:
        check="X"
    else:  
        check="O"
    # Check if block is used.
    while spaces.count(n)==0:
        print "\nInvalid Space"
        n=playerinput(player)

    # Remove block from spaces array
    spaces=spaces.remove(n)

    # Replace block with check mark in board
    board=board.replace(str(n),check)

    # Replace space with check mark in wincombos array
    for c in range(len(wincombos)):
        if wincombos[c]==n:
            wincombos[c]=check

    # Run the checkwinner function
    status = checkwinner(wincombos,check)
    return board,status

def playerinput(player):
    try:
        key = int(raw_input('\n\nPlayer ' + str(player) + ': Please select a space '))
    except ValueError:
        print "Invalid Space"
        key = playerinput(player)
    return key

def playttt():
    """main game play function"""
    print "NOTE: Numbers correspond to board play positions, left to right, top to bottom."
    board = " 1 | 2 | 3\n-----------\n 4 | 5 | 6\n-----------\n 7 | 8 | 9"
    wincombos=[1,2,3,4,5,6,7,8,9,1,4,7,2,5,8,3,6,9,1,5,9,3,5,7]
    spaces=range(1,10)
    print "\n"+board

    while True:
        player = len(spaces)%2 +1
        print "player %s" % player
        if player == 1:
            player = 2
        else:
            player = 1

        print "player %s" % player
        key = playerinput(player)

        board,status = make_play(board,spaces,wincombos,player,key)

        if status == 1:
            print '\n\nPlayer ' + str(player) + ' is the winner!!!'
            print board
            break
        elif len(spaces)==0:
            print "No more spaces left. Game ends in a TIE!!!"
            print board
            break
        else:
            print board
            continue

if __name__ == "__main__":
    playttt()

