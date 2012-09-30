class Gameboard(object):
    def __init__(self):
        self.boardstate = [[0,0,0],[0,0,0],[0,0,0]]
        
    def change(self):
        self.boardstate = [[1,0,0],[0,0,0],[0,0,0]]
