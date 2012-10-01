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
        
    def save_move(self, position, player):
        """
        Save any player's move
        """
        x = position[0]
        y = position[1]
        self.boardstate[x][y] = player
        
    def computer_move(self):
        """
        Calculate computer's move
        """
        snapshot = Gameboard()
        snapshot.boardstate = self.boardstate
        best_move = snapshot._minimax(5, -1)
        self.save_move(best_move[1], -1)
        
    def _minimax(self, level, player):
        """
        Minimax algorithm to determine best move
        """
        best_score = -1000 * player
        best_position = []
        children = self.available_spaces()
        if not children or level == 0 or self.check_status(-1) or self.check_status(1):
            best_score = self._calc_score()
        else:
            for child in children:
                position = [child[0], child[1]]
                self.save_move(position, player)
                if player == 1: # maximize
                    score = self._minimax(level - 1, -1)[0]
                    if score > best_score:
                        best_score = score
                        best_position = position
                else: # minimize
                    score = self._minimax(level - 1, 1)[0]
                    if score < best_score:
                        best_score = score
                        best_position = position
                self.save_move(position, 0)
        return [best_score, best_position]
            
    def _calc_score(self):
        """
        Heuristic evaluation function for minimax
        """
        all_rows = [row for row in self.boardstate] + \
                   [[row[i] for row in self.boardstate] for i in range(3)] + \
                   [[self.boardstate[i][i]] for i in range(3)] + \
                   [[self.boardstate[i][2-i]] for i in range(3)]
        score = 0
        for row in all_rows:
            score += self._sum_rows(row)
        return score
        
    def _sum_rows(self, row):
        score = reduce(lambda x, y: x + y, row)
        if score == 2 or score == -2:
            score = 10 * (score / 2)
        if score == 3 or score == -3:
            score = 100 * (score / 3)
        return score
