from random import randrange
from tictactoe.board import Board

class AI(object):
    '''
    The AI class for tic-tac-toe. Take a move function on initialize indication
    if it is a random ai or semi-intelligent non-losing ai. Also takes markType
    indicating if it is a 'x' or an 'o'
    '''
    def __init__(self, markType, moveFunction):
        self.markType = markType
        self.enemyType = 'o' if markType == 'x' else 'x'
        self.moveFunction = moveFunction
    
    def turn(self, b):
        b.mark(self.moveFunction(self, b), self.markType)
    
    def moveAI(self, b):
        if b.board[4] == '':
            return 4
        if all(b.board[i] == '' for i in (0,1,2,3,5,6,7,8)):
            return 0
        
        #could have "return detectX or \" to be cleaner, but since it returns 0, can't - meh 
        m=self.detectWin(b, self.markType)
        if m is not None:
            return m
        m=self.detectWin(b, self.enemyType)
        if m is not None:
            return m
        m=self.detectCornerManeuver(b)
        if m is not None:
            return m
        m=self.detectLineManeuver(b)
        if m is not None:
            return m
        m=self.detectTightTriangleManeuver(b)
        if m is not None:
            return m
        m=self.detectLManeuver(b)
        if m is not None:
            return m
        return self.moveRandom(b)
    
    def moveRandom(self, b):
        location=-1
        while not b.isFilled() and (location == -1 or b.isMarked(location)):
            location=randrange(9)
        return location

    def detectWin(self, b, markType):
        for case in Board.WIN:
            for empty in range(0,3):
                owned=range(0,3)
                owned.remove(empty)
                if b.board[case[empty]] == '' and all(markType==b.board[case[i]] for i in owned):
                    return case[empty]
        return None

    def detectCornerManeuver(self, b):
        #4 will never be empty
        for l,t in ((0,1),(2,5),(8,7),(6,3)):
            if(b.isEmptyExcept((l,4)) and b.board[l] == self.enemyType):
                return t
        for l1,l2 in ((0,8),(2,6)):
            if(b.isEmptyExcept((l1,l2,4)) and all(b.board[i] == self.enemyType for i in (l1,l2))):
                return 1
        return None
    
    def detectLineManeuver(self, b):
        if b.board[4] == self.enemyType:
            for items,cases in ( ((0,4,8),((0,2),(8,6)) ), ((2,4,6),((2,0),(6,8))) ):
                if b.isEmptyExcept(items):
                    for enemy,desired in cases:
                        if b.board[enemy] == self.enemyType:
                            return desired
        return None
    
    def detectTightTriangleManeuver(self, b):
        '''Detect tight triangle maneuvers, where the player puts their mark
        on two caddy-corner middle spots like top middle and left middle'''
        for enemy,me,move in ( ((1,3),(2,6),0), ((1,5),(0,8),2), ((3,7),(0,8),6), ((7,5),(2,6),8) ):
            if all(b.board[i]==self.enemyType for i in enemy) and \
               all(b.board[i]!=self.markType for i in me) and b.board[move]=='':
              return move
        return None
    
    def detectLManeuver(self, b):
        for enemy,me,move in ( ((1,6),(0,2,3),0), ((1,8),(0,2,5),2), ((3,2),(0,1,6),0), \
                             ((3,8),(6,7,0),6), ((0,5),(1,2,8),2), ((6,5),(7,2,8),8), \
                             ((0,7),(3,6,8),6), ((2,7),(5,6,8),8) ):
            if all(b.board[i]==self.enemyType for i in enemy) and \
               all(b.board[i]!=self.markType for i in me) and b.board[move]=='':
              return move
        return None