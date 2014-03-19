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
        threats = row_scores(self.board, 'x')
        opportunities = row_scores(self.board, 'o')
        
        # Test for potential winning moves
        for idx, score in enumerate(opportunities):
            if score == 2:
                # Test for an open space
                if first_available_cell(idx) is not None:
                    return first_available_cell(idx)
                
        # Search for greatest potential threat
        for idx, score in enumerate(threats):
            pass

    # Return the first available cell in a given row.
    def first_available_cell(self, row):
        for cell in Strategy.ROWS[row]:
            if self.board[cell] == " ":
                return cell
        return None
    
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
            scores[index] = score
            index = index + 1
        return scores
        
