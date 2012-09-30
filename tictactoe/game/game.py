class Gameboard(object):
    def __init__(self):
        self.boardstate = [[0,0,0],[0,0,0],[0,0,0]]
        self.status = None
        
    def available_spaces(self):
        spaces = []
        for x in range(3):
            for y in range(3):
                if self.boardstate[x][y] == 0:
                    spaces.append([x,y])
        return spaces
        
    def check_status(self, value):
        """
        Check for finished gamestate
        """
        winner = 0
        if all(self.boardstate[0][i] == value for i in range(3)) or \
                all(self.boardstate[1][i] == value for i in range(3)) or \
                all(self.boardstate[2][i] == value for i in range(3)) or \
                all(self.boardstate[i][0] == value for i in range(3)) or \
                all(self.boardstate[i][1] == value for i in range(3)) or \
                all(self.boardstate[i][2] == value for i in range(3)) or \
                all(self.boardstate[i][i] == value for i in range(3)) or \
                all(self.boardstate[i][2-i] == value for i in range(3)):
            winner = value
        if winner:
            if value == 1:
                self.status = 'Player wins!'
            if value == -1:
                self.status = 'Computer wins!'
            return True
        elif not self.available_spaces():
            self.status = 'Game ends in a draw!'
            return True
        return False
        
    def player_move(self, position):
        x = position[0]
        y = position[1]
        self.boardstate[x][y] = 1
        
    def computer_move(self):
        #x = position[0]
        #y = position[1]
        #self.boardstate[x][y] = -1
        pass
