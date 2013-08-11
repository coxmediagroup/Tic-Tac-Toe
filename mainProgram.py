#Adriel Velazquez 8/10/2013
from methods import *
import random 

#Adriel Velazquez 8/10/2013

# Creating Board from regular print statements; however, from a little research
# Pygame module would make this process drastically easier (Visually)

board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
board2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
aiBoard = [8, 1, 6, 3, 5, 7, 4, 9, 2]
winningSets = [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [6, 4, 2]
winningSets2 = [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [6, 4, 2]
playerSelections = []
aiSelections = []

#Board utilizing just print statements

print board[0], '|', board[1], '|', board[2]
print '----------'
print board[3], '|', board[4], '|', board[5]
print '----------'
print board[6], '|', board[7], '|', board[8]

start = random.randint(1, 100)
print 'Deciding who goes first'

if start%2:
    print 'player goes first'
    while True:
        selectSpace()
        ai()
else:
    print 'computer goes first'
    while True:
        ai()
        selectSpace()




        


    


    
