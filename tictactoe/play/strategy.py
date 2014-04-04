import random

class Strategy:
    ROWS = (
        # rows
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        
        # columns
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        
        # diagonals
        (0, 4, 8),
        (2, 4, 6),
    )
    board = "   \n   \n   "
    
    def __init__(self, board = "   \n   \n   "):
        self.board = board.replace("\n", "")

    # Returns the index of the next cell the computer will move to.
    # 
    # Logic: First, make a winning move if possible.  Otherwise,
    # address the greatest threat on the board.  Make a random move
    # from amongst those we're considering.
    def next_move(self):
        threats = self.row_scores('x')
        opportunities = self.row_scores('o')
        
        # Test for potential winning moves
        for idx, score in enumerate(opportunities):
            if score == 2:
                # Test for an open space
                if self.first_available_cell(idx) is not None:
                    result = self.first_available_cell(idx)
                    self.move('o', result)
                    return result
        
        # Search for greatest potential threat
        highest_threat = -1
        threat_indexes = []
        for idx, score in enumerate(threats):
            if self.first_available_cell(idx) is None:
                continue
            if score > highest_threat:
                highest_threat = score
                threat_indexes = [idx]
            elif score == highest_threat:
                threat_indexes = threat_indexes + [idx]
        # Randomize next move.
        random.shuffle(threat_indexes)
        if len(threat_indexes):
            result = self.random_available_cell(threat_indexes[0])
            self.move('o', result)
            return result
        return None

    # Return the first available cell in a given row.
    def first_available_cell(self, row):
        for cell in Strategy.ROWS[row]:
            if self.board[cell] == " ":
                return cell
        return None
    
    def cell_available(self, cell):
        if self.board[cell] == ' ':
            return True
        return False
    
    # Return a random available cell in a given row.
    def random_available_cell(self, row):
        cells = []
        for cell in Strategy.ROWS[row]:
            if self.board[cell] == " ":
                cells = cells + [cell]
        if cells == []:
            return None
        return random.choice(cells)

    # Determine the "score" for all possible rows.
    # Calculate scores for all rows, columns and diagonals.  (Referred
    # to as "rows" here.)
    # 
    # Example:
    # +---+
    # |x x|
    # |xo |
    # |o  |
    # +---+
    # 
    # For this board, the rows have the following scores for x and o
    # Row:  x       o
    # 0     2       0
    # 1     1       1
    # 2     0       1
    # (Columns and diagonals omitted for brevity.)
    # 
    # By calculating the scores of each row and column, we can determine
    # both the greatest threat from an opponent and the greatest
    # opportunity for the player.
    def row_scores(self, player):
        scores = [0] * 8    # create an empty list of scores
        index = 0           # index into our scores list
        for cells in Strategy.ROWS:
            score = 0
            for cell in cells:
                if self.board[cell] == player:
                    score = score + 1
                elif self.board[cell] != ' ':
                    score = 0
                    break
            scores[index] = score
            index = index + 1
        return scores
    
    def game_state(self):
        scores = self.row_scores("o")
        for score in scores:
            if score == 3:
                return "win"
        for i in xrange(0, 9):
            if self.board[i] == " ":
                return "in-play"
        return "draw"
    
    def move(self, player, cell):
        tmp = list(self.board)
        tmp[cell] = player
        self.board = ''.join(tmp)
