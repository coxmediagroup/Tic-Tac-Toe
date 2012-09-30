class Gameboard(object):
    def __init__(self):
        self.boardstate = [[0,0,0],[0,0,0],[0,0,0]]
        
    def available_spaces(self):
        spaces = []
        for x in range(3):
            for y in range(3):
                if self.boardstate[x][y] == 0:
                    spaces.append([x,y])
        return spaces
        
    def player_move(self, position):
        x = position[0]
        y = position[1]
        self.boardstate[x][y] = 1
        
    def computer_move(self, position):
        #x = position[0]
        #y = position[1]
        #self.boardstate[x][y] = -1
        pass
