#! /usr/bin/python
# This game was written by Wes Cannon, http://www.linkedin.com/in/wescannon
# It was originally written for the code challenge requested by Cox Media for
# the job application of Python Developer.
# First iteration completed May 31, 2011
import string
import random
import sys
# game_initialize sets the initial variables, the markers for players and the order of play
def game_initialize():
    global MARKERS, WINNING_COMBINATIONS, FORKS, CORNER_MOVES
    # MARKERS stores all of the moves for the game
    MARKERS = {
        'A1': ' ',
        'A2': ' ',
        'A3': ' ',
        'B1': ' ',
        'B2': ' ',
        'B3': ' ',
        'C1': ' ',
        'C2': ' ',
        'C3': ' ',
    }
    # WINNING_COMBINATIONS is used by check_for_win at the beginning of a turn
    # to see if a player won during last turn
    WINNING_COMBINATIONS = [
        ('A1','B1','C1'),
        ('A2','B2','C2'),
        ('A3','B3','C3'),
        ('A1','A2','A3'),
        ('B1','B2','B3'),
        ('C1','C2','C3'),
        ('A1','B2','C3'),
        ('C1','B2','A3'),
    ]
    # FORKS is used by check_forks to see if the human  has the first two
    # moves of a fork and blocks it by taking the third move
    FORKS = [
        ('A1','C3','B1'),
        ('A1','C3','B3'),
        ('A3','C1','A2'),
        ('A3','C1','C2'),
        ('B1','C3','C1'),
        ('B1','A3','A1'),
        ('C2','A3','C3'),
        ('C2','A1','C1'),
        ('B3','A1','A3'),
        ('B3','C1','C3'),
        ('A2','C3','A3'),
        ('A2','C1','A1'),
        ('B1','C2','C1'),
        ('C2','B3','C3'),
        ('B3','A2','A3'),
        ('A2','B1','A1'),
        ('B2','C1','C3'),
        ('B2','C3','C1'),
        ('B2','A3','C3'),
        ('B2','C3','A3'),
        ('B2','A1','A3'),
        ('B2','A3','A1'),
        ('B2','A1','C1'),
        ('B2','C1','A1'),
        ('B2','C1','C2'),
        ('B2','C3','C2'),
        ('B2','A3','B3'),
        ('B2','C3','B3'),
        ('B2','A1','A2'),
        ('B2','A3','A2'),
        ('B2','A1','B1'),
        ('B2','C1','B2'),
    ]
    # CORNER_MOVES is used by the computer in the early game to take a corner
    CORNER_MOVES = ('A1','A3','C1','C3')
    # set_mark is used to store the marker (X or O) the human chooses
    def set_mark():
        global MARK1, MARK2, MESSAGE1
        mark = raw_input("Would you like be Xs or Os (enter X or O)? ")
        selection = string.upper(mark)
        if selection == 'X' or selection == 'O':
            MARK1 = selection
            MESSAGE1 = 'You selected ' + MARK1 + 's'
            if MARK1 == 'X':
                MARK2 = 'O'
            else:
                MARK2 = 'X'
        else:
            print 'You have entered an invalid response.  Please try again.'
            print
            set_mark()
    # set_order sets the order of the first move chosen by the human
    def set_order():
        global ORDER, MESSAGE2
        order = raw_input("Would you move 1st or 2nd (enter 1 or 2)? ")
        if order == '1':
            ORDER = order
            MESSAGE2 = 'You chose to go 1st'
        elif order == '2':
            ORDER = order
            MESSAGE2 = 'You chose to go 2nd'
        else:
            print 'You have entered an invalid response.  Please try again.'
            print
            set_order()
    # The following calls the functions to set initial variables and provides
    # feedback for the human
    print
    print 'Welcome to Tic Tac Toe by Wes Cannon'
    print
    set_mark()
    set_order()
    print
    print MESSAGE1
    print MESSAGE2
# set_marker sets the marker selected by each player during a turn
def set_marker(m,n):
    if n == 1:
        MARKERS[m] = MARK1
    else:
        MARKERS[m] = MARK2
    draw_board()
# draw_board is called by set_marker redraws the game board after each turn
def draw_board():
    print
    print '     A     B     C'
    print
    print '1    ' + MARKERS['A1'] + '  |  ' + MARKERS['B1'] + '  |  ' + MARKERS['C1']
    print '   ================='
    print '2    ' + MARKERS['A2'] + '  |  ' + MARKERS['B2'] + '  |  ' + MARKERS['C2']
    print '   ================='
    print '3    ' + MARKERS['A3'] + '  |  ' + MARKERS['B3'] + '  |  ' + MARKERS['C3']
    print
# check_for_win is called at the beginning of each player's turn to see if the
# other player won during last turn and if so, display a message
def check_for_win():
    mark = ' '
    for combo in WINNING_COMBINATIONS:
        if MARKERS[combo[0]] == MARKERS[combo[1]] == MARKERS[combo[2]]:
            mark = MARKERS[combo[0]]
    if mark <> ' ':
        if mark == MARK1:
            print 'You win!  That is not supposed to happen.'
        else:
            print 'I win.  Do not feel bad.  The best you can do is a draw.'
        play_again()
# check_available_moves is called during each turn to determine which turns are
# valid and count the number of possible moves used in computer_turn logic
def check_available_moves():
    global AVAILABLE_MOVES, POSSIBLE_MOVES
    AVAILABLE_MOVES = []
    for mark in MARKERS:
        if MARKERS[mark] == ' ':
            AVAILABLE_MOVES.append(mark)
    POSSIBLE_MOVES = len(AVAILABLE_MOVES)
    if POSSIBLE_MOVES == 0:
        print 'There are no more moves. The game is a draw.'
        play_again()
# play_again is called whenever a player wins or there is a draw to either
# restart the game or exit
def play_again():
    a = raw_input("Would you like to play again (Y or N)? ")
    answer = string.upper(a)
    if answer == 'Y':
        game_initialize()
        if ORDER == '1':
            draw_board()
            player_turn()
        else:
            computer_turn()
    elif answer == 'N':
        sys.exit()
    else:
        print 'You have entered an invalid response.  Please try again.'
        play_again()
# player_turn gets human input and stores the move in MARKERS if valid, then
# calls computer_turn
def player_turn():
    check_for_win()
    check_available_moves()
    print 'Enter the grid coordinates to place your marker (like A1 or a1):'
    move = raw_input("? ")
    print
    m = string.upper(move)
    if m in MARKERS:
        if MARKERS[m] == ' ':
            set_marker(m,1)
            print 'You chose square ' + m
            computer_turn()
        else:
            print 'You can not move there.  That sqare is taken.'
            player_turn()
    else:
        print 'You have entered an invalid response.  Please try again.'
        player_turn()
# computer_turn executes the game logic for determining the computer move and if
# game is not won, calls player_turn
def computer_turn():
    # look_for_win checks to see if there is a winning move and if so execute it
    def look_for_win():
        for combo in WINNING_COMBINATIONS:
            if MARK2 == MARKERS[combo[0]] == MARKERS[combo[1]] and MARKERS[combo[2]] == ' ':
                m = combo[2]
            elif MARK2 == MARKERS[combo[1]] == MARKERS[combo[2]] and MARKERS[combo[0]] == ' ':
                m = combo[0]
            elif MARK2 == MARKERS[combo[0]] == MARKERS[combo[2]] and MARKERS[combo[1]] == ' ':
                m = combo[1]
            else:
                m = ' '
            if m <> ' ':
                set_marker(m,2)
                print 'I chose square ' + m
                print
                check_for_win()
    # look_for_block checks to see if the human has two markers in any row and
    # if so blocks it by selecting the third
    def look_for_block():
        for combo in WINNING_COMBINATIONS:
            if MARK1 == MARKERS[combo[0]] == MARKERS[combo[1]] and MARKERS[combo[2]] == ' ':
                m = combo[2]
            elif MARK1 == MARKERS[combo[1]] == MARKERS[combo[2]] and MARKERS[combo[0]] == ' ':
                m = combo[0]
            elif MARK1 == MARKERS[combo[2]] == MARKERS[combo[0]] and MARKERS[combo[1]] == ' ':
                m = combo[1]
            else:
                m = ' '
            if m <> ' ':
                set_marker(m,2)
                print 'I chose square ' + m
                print
                check_for_win()
                player_turn()
    # check_available_corners is used in the early moves to select a corner
    def check_available_corners():
        global AVAILABLE_CORNERS, POSSIBLE_CORNERS
        AVAILABLE_CORNERS = []
        for mark in CORNER_MOVES:
            if MARKERS[mark] == ' ':
                AVAILABLE_CORNERS.append(mark)
        POSSIBLE_CORNERS = len(AVAILABLE_CORNERS)
    # check_forks uses FORKS to see if the human has the first two markers in an
    # eminent fork and if so blocks it
    def check_forks():
        for fork in FORKS:
            if MARK1 == MARKERS[fork[0]] == MARKERS[fork[1]] and MARKERS[fork[2]] == ' ':
                m = fork[2]
                set_marker(m,2)
                print 'I chose square ' + m
                print
                check_for_win()
                player_turn()
    # The main logic in selecting the computer's marker during a turn
    check_available_moves()
    check_available_corners()
    if POSSIBLE_MOVES == 9:
        s = random.randrange(0, POSSIBLE_MOVES-1)
        m = AVAILABLE_MOVES[s]
    elif POSSIBLE_MOVES == 8 and 'B2' in AVAILABLE_MOVES:
        m = 'B2'
    elif POSSIBLE_MOVES == 8 and not 'B2' in AVAILABLE_MOVES:
        s = random.randrange(0, POSSIBLE_CORNERS-1)
        m = AVAILABLE_CORNERS[s]
    elif POSSIBLE_MOVES == 7 and 'B2' in AVAILABLE_MOVES:
        check_forks()
        m = 'B2'
    elif POSSIBLE_MOVES == 7 and not 'B2' in AVAILABLE_MOVES:
        check_forks()
        s = random.randrange(0, POSSIBLE_CORNERS-1)
        m = AVAILABLE_CORNERS[s]
    elif POSSIBLE_MOVES == 1:
        m = AVAILABLE_MOVES[0]
    else:
        check_for_win()
        look_for_win()
        look_for_block()
        check_forks()
        s = random.randrange(0, POSSIBLE_MOVES-1)
        m = AVAILABLE_MOVES[s]
    # After a marker is selected set the marker, provide feedback, check for a
    # win and if needed call player_turn
    set_marker(m,2)
    print 'I chose square ' + m
    check_for_win()
    player_turn()
# Initialize the game and call first player's turn
game_initialize()
if ORDER == '1':
    draw_board()
    player_turn()
else:
    computer_turn()