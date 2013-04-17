from django.test import TestCase
from gamelogic import isWin, nextMove

class SimpleTest(TestCase):
    def TestIsWin(self):
        assert isWin(list("XXX---OOO"))==True
        assert isWin(list('X---OO--X'))==False
        assert isWin(list('X--X--X--'))==True
        assert isWin(list('X-O-OO--X'))==False
        assert isWin(list('X-OOX--OX'))==True
        assert isWin(list('X-OOO-O-X'))==True

    def TestNextMove(self):
        assert nextMove(list('X----O-XO'),'X')==(1,2)
        assert nextMove(list('OXX---XOO'),'X')==(1,4)
        assert nextMove(list('XX---OO-O'),'X') == (1,2)
        assert nextMove(list('---------'),'X') == (0,4)
        assert nextMove(list('XXOOO-XO-'),'X') == (0,5)
        assert nextMove(list('OO-XXO-XO'),'X') == (0,2)
        assert nextMove(list('XX-OO-XO-'),'O') ==(-1,5)
        assert nextMove(list('XX--O-XOO'),'O') ==(1,2)
