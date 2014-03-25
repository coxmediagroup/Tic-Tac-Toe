from gtnwfunctions import *
import datetime
from random import randint

is_now = datetime.datetime.now()
print "\n\n\n\n\n"
print "Begin testing...", is_now

functionTest = "passed"


print "======Testing winCheck function======"
# test if blank board returns false, none
print "Testing blank gameboard..."

winCheckTest = "passed"
internalTest = "passed"

game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
test = winCheck(game_board, 'X', 'X')    # blank board should result in [False, 'none']
if test[0] != False or test[1]!= 'none':
    functionTest = "failed"
    internalTest = "failed"
    winCheckTest = "failed"
print "Result for X (should be [False, \'none\']) =",test
test = winCheck(game_board, 'O', 'O')
if test[0] != False or test[1]!= 'none':
    functionTest = "failed"
    internalTest = "failed"
    winCheckTest = "failed"
print "Result for O (should be [False, \'none\']) =",test
if internalTest == "passed":
    print "Blank board test passed..."
else:
    print "******Blank board test FAILED******"


winning_rows = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (6, 4, 2)]   

# test for wins
print "Testing winning rows (X)..."    # Testing X
internalTest = "passed"
for row in winning_rows:    # Testing each set of winning rows
    for each in row:
        game_board[each] = 'X'
    test = winCheck(game_board, 'X', 'X')    # Sending each to winCheck and testing for an X win
    if test[0] != True or test[1] != row:    # Should be True and return the winning row
        functionTest = "failed"
        internalTest = "failed"
        winCheckTest = "failed"
    row = str(row)
    print "Result (should be [True, %s]) =" % row,
    print test
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank for next row
if internalTest == "passed":
    print "Winning rows for X passed..."
else:
    print "******Winning rows for X FAILED******"


print "Testing winning rows (O)..."    # same as above, but for O
internalTest = "passed"
for row in winning_rows:
    for each in row:
        game_board[each] = 'O'
    test = winCheck(game_board, 'O', 'O')
    if test[0] != True or test[1] != row:
        functionTest = "failed"
        internalTest = "failed"
        winCheckTest = "failed"
    row = str(row)
    print "Result (should be [True, %s]) =" % row,
    print test
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
if internalTest == "passed":
    print "Winning rows for O passed..."
else:
    print "******Winning rows for O FAILED******"

if functionTest == "failed":
    winFunTest = "failed"
    print "******Winning rows test FAILED******"
else:
    winFunTest = "passed"
    print "Winning rows test passed"


print "Testing non-winning rows (X)..."    # Testing non-winning rows that could be interpreted as winning for X
internalTest = "passed"
nonWinFunTest = "passed"
print "Checking targeted cases first..."
non_winning_rows = [(1, 2, 3), (4, 5, 6), (7, 8, 0)] 
for row in non_winning_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "X"
    test = winCheck(game_board, 'X', 'X')
    if test[0] == True or test[1] == row:    # Should return False, none
        functionTest = "failed"
        internalTest = "failed"
        nonWinFunTest = "failed"
        winCheckTest = "failed"
    row = str(row)
    print "Result (should be [False, \'none\']) =", test
if internalTest == "passed":
    print "Targeted non-winning rows for X passed..."
else:
    print "******Targeted non-winning rows for X FAILED******"

print "Testing non-winning rows (O)..."    # Same as above, for O
internalTest = "passed"
print "Checking targeted cases first..."
non_winning_rows = [(1, 2, 3), (4, 5, 6), (7, 8, 0)] 
for row in non_winning_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "O"
    test = winCheck(game_board, 'O', 'O')
    if test[0] == True or test[1] == row:    # Should be False, none
        functionTest = "failed"
        internalTest = "failed"
        nonWinFunTest = "failed"
        winCheckTest = "failed"
    row = str(row)
    print "Result (should be [False, \'none\']) =", test
if internalTest == "passed":
    print "Targeted non-winning rows for O passed..."
else:
    print "******Targeted non-winning rows for O FAILED******"

internalTest = "passed"
print "Checking secondary targeted cases for X..."    # Same as above, but for less likely cases (X first)
non_winning_rows = [(1, 5, 0), (4, 8, 3), (7, 2, 6), (1, 3, 0), (4, 6, 3), (7, 0, 6), (3, 7, 2), (6, 1, 5)] 
for row in non_winning_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "X"
    test = winCheck(game_board, 'X', 'X')
    if test[0] == True or test[1] == row:
        functionTest = "failed"
        internalTest = "failed"
        nonWinFunTest = "failed"
        winCheckTest = "failed"
    row = str(row)
    print "Result (should be [False, \'none\']) =", test
if internalTest == "passed":
    print "Secondary targeted non-winning rows for X passed..."
else:
    print "******Secondary targeted non-winning rows for X FAILED******"

internalTest = "passed"
print "Checking secondary targeted cases for O..."    # Now for O
non_winning_rows = [(1, 5, 0), (4, 8, 3), (7, 2, 6), (1, 3, 0), (4, 6, 3), (7, 0, 6), (3, 7, 2), (6, 1, 5)] 
for row in non_winning_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "O"
    test = winCheck(game_board, 'O', 'O')
    if test[0] == True or test[1] == row:
        functionTest = "failed"
        internalTest = "failed"
        nonWinFunTest = "failed"
        winCheckTest = "failed"
    row = str(row)
    print "Result (should be [False, \'none\']) =", test
if internalTest == "passed":
    print "Secondary targeted non-winning rows for O passed..."
else:
    print "******Secondary targeted non-winning rows for O FAILED******"
    


print "======Testing AI function======"    # Testing to make sure the AI functions as designed

AI_Test = "passed"

AI_X_Win = "passed"
AI_O_Win = "passed"
AI_Win = "passed"

horizontal_AI_rows = [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8)]  # Used to check win and block for AI
vertical_AI_rows = [(0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)]
diagonal_AI_rows = [(0, 4), (4, 8), (2, 4), (4, 6)]

print "Checking AI moving to win or block..."
print "Checking AI as X..."
AI_X_Win = "passed"

print "...Horizontal Rows..."

AI_Horizontal_Win = "passed"    # Horizontal first
for row in horizontal_AI_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "X"
    AI_win = AIMove(game_board, "X", "O", randint(1, 9), randint(1, 9))    # Checking for win or block
    game_board[AI_win - 1] = "X"
    AI_check = winCheck(game_board, "X", "X")
    print AI_check
    if AI_check[0] != True:    # Should return True
        AI_Horizontal_Win = "failed"
        AI_X_Win = "failed"
        AI_Win = "failed"
        AI_Test = "failed"
        functionTest = "failed"
print "AI_Horizontal_Win:", AI_Horizontal_Win

print "... as vertical rows..."    # Same as above, for vertical now
AI_Vertical_Win = "passed"
for row in vertical_AI_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "X"
    AI_win = AIMove(game_board, "X", "O", randint(1, 9), randint(1, 9))
    #checking that AI_move will win...
    game_board[AI_win - 1] = "X"
    AI_check = winCheck(game_board, "X", "X")
    print AI_check
    if AI_check[0] != True:
        AI_Vertical_Win = "failed"
        AI_X_Win = "failed"
        AI_Win = "failed"
        AI_Test = "failed"
        functionTest = "failed"
print "AI_Vertical_Win:", AI_Vertical_Win

print "... as diagonal rows..."    # Same as above, now diagonal
AI_Diagonal_Win = "passed"
for row in diagonal_AI_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "X"
    AI_win = AIMove(game_board, "X", "O", randint(1, 9), randint(1, 9))
    #checking that AI_move will win...
    game_board[AI_win - 1] = "X"
    AI_check = winCheck(game_board, "X", "X")
    print AI_check
    if AI_check[0] != True:
        AI_Diagonal_Win = "failed"
        AI_X_Win = "failed"
        AI_Win = "failed"
        AI_Test = "failed"
        functionTest = "failed"
print "AI_Diagonal_Win:", AI_Diagonal_Win

print "AIMove to win as X:", AI_X_Win    # If all work, will pass

print "Checking AI as O..."    # Same as above AI win, now for O
AI_O_Win = "passed"

print "...Horizontal Rows..."
AI_Horizontal_Win = "passed"
for row in horizontal_AI_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "O"
    AI_win = AIMove(game_board, "O", "X", randint(1, 9), randint(1, 9))
    #checking that AI_move will win...
    game_board[AI_win - 1] = "O"
    AI_check = winCheck(game_board, "O", "O")
    print AI_check
    if AI_check[0] != True:
        AI_Horizontal_Win = "failed"
        AI_O_Win = "failed"
        AI_Win = "failed"
        AI_Test = "failed"
        functionTest = "failed"
print "AI_Horizontal_Win:", AI_Horizontal_Win

print "... as vertical rows..."    # Vertical O
AI_Vertical_Win = "passed"
for row in vertical_AI_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "O"
    AI_win = AIMove(game_board, "O", "X", randint(1, 9), randint(1, 9))
    #checking that AI_move will win...
    game_board[AI_win - 1] = "O"
    AI_check = winCheck(game_board, "O", "O")
    print AI_check
    if AI_check[0] != True:
        AI_Vertical_Win = "failed"
        AI_O_Win = "failed"
        AI_Win = "failed"
        AI_Test = "failed"
        functionTest = "failed"
print "AI_Vertical_Win:", AI_Vertical_Win

print "... as diagonal rows..."    # Diagonal O
AI_Diagonal_Win = "passed"
for row in diagonal_AI_rows:
    game_board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]    # defining the game board as blank
    for each in row:
        game_board[each] = "O"
    AI_win = AIMove(game_board, "O", "X", randint(1, 9), randint(1, 9))
    #checking that AI_move will win...
    game_board[AI_win - 1] = "O"
    AI_check = winCheck(game_board, "O", "O")
    print AI_check
    if AI_check[0] != True:
        AI_Diagonal_Win = "failed"
        AI_Win = "failed"
        AI_O_Win = "failed"
        AI_Test = "failed"
        functionTest = "failed"
print "AI_Diagonal_Win:", AI_Diagonal_Win
print "AIMove to win or block as X:", AI_X_Win
print "AIMove to win or block as O:", AI_O_Win
print "AIMove to win or block, both X and O:", AI_Win


AI_Double_Move = "passed"    # Now checking to see if AI will block double moves
AI_Diagonal_Double = "passed"
game_board = ["X", " ", " ", " ", "O", " ", " ", " ", "X"]    # setting up a possible double move
Double_Check = AIMove(game_board, "O", "X", 4, 0) 
if (Double_Check == 2 or Double_Check == 4 or Double_Check == 6) and game_board[Double_Check - 1] == " ":
    print "Diagonal Double move: passed (should be 2, 4, or 6):", Double_Check
else:
    print "Diagonal Double move: failed (should be 2, 4, or 6):", Double_Check
    AI_Diagonal_Double = "failed"
    AI_Double_Move = "failed"
    AI_Test = "failed"
    functionTest = "failed"


game_board = [" ", " ", "X", " ", "O", " ", "X", " ", " "]    # setting up a possible double move
Double_Check = AIMove(game_board, "O", "X", 4, 0) 
if (Double_Check == 2 or Double_Check == 4 or Double_Check == 6) and game_board[Double_Check - 1] == " ":
    print "Diagonal Double move: passed (should be 2, 4, or 6):", Double_Check
else:
    print "Diagonal Double move: failed (should be 2, 4, or 6):", Double_Check
    AI_Diagonal_Double = "failed"
    AI_Double_Move = "failed"
    AI_Test = "failed"
    functionTest = "failed"

game_board = [" ", " ", " ", "X", "O", " ", " ", " ", "X"]    # setting up a possible double move
Double_Check = AIMove(game_board, "O", "X", 4, 0) 
if (Double_Check == 1) and game_board[Double_Check - 1] == " ":
    print "Diagonal Double move: passed (should be 1):", Double_Check
else:
    print "Diagonal Double move: failed (should be 1):", Double_Check
    AI_Diagonal_Double = "failed"
    AI_Double_Move = "failed"
    AI_Test = "failed"
    functionTest = "failed"

game_board = [" ", " ", "X", "X", "O", " ", " ", " ", " "]    # setting up a possible double move
Double_Check = AIMove(game_board, "O", "X", 4, 0) 
if (Double_Check == 1) and game_board[Double_Check - 1] == " ":
    print "Diagonal Double move: passed (should be 1):", Double_Check
else:
    print "Diagonal Double move: failed (should be 1):", Double_Check
    AI_Diagonal_Double = "failed"
    AI_Double_Move = "failed"
    AI_Test = "failed"
    functionTest = "failed"

print "AI Diagonal Double Move:", AI_Diagonal_Double  # if all is good, passed

print "Checking t double move..."    # checking for a double move in the t portion of the board
double_T_test = "passed"
previous_moves = [4, 6, 2, 8]    # moves in the t
game_board = [" ", "O", " ", " ", "X", " ", " ", " ", " "]  
for each in previous_moves:
    T_Test = AIMove(game_board, "X", "O", 3, each)    # checking each possible t move
    if 3 < each < 7 and (each + 3 == T_Test or each - 3 == T_Test):
        print "T test (+ or -3):", double_T_test
    elif each + 1 == T_Test or each - 1 == T_Test:
        print "T test (+ or -1):", double_T_test
    else:
        double_T_test = "failed"
        AI_Double_Move = "failed"
        AI_Test = "failed"
        functionTest = "failed"
        print "T_Test:", double_T_test
print "AI_Double_Move:", AI_Double_Move
print "AI_Test:", AI_Test


print "******************************"
print "FINAL RESULTS for", is_now    # is_now displays date and time of test

print "--------------------------------"
print "winCheck function test results..."    # displaying summarized results
print "Winning rows test:", winFunTest
print "Non-winning rows test:", nonWinFunTest
print "winCheck function:", winCheckTest
print "--------------------------------"
print "AIMove function test results..."
print "AIMove to win or block:", AI_Win
print "AIMove to block double move:", AI_Double_Move
print "AIMove function:", AI_Test

print "================================================"
print "Entire Function Test:", functionTest    # final result of test
print "\n\n\n\n\n"



