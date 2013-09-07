WINNING_COMBINATIONS = ( (0, 1, 2), (3, 4, 5), (6, 7, 8), 
                         (0, 3, 6), (1, 4, 7), (2, 5, 8),
                         (0, 4, 8), (2, 4, 6)
                       )

BLANK = 0
PLAYER = 1
COMPUTER = 2
NO_RESULT = 3

class Game(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def check_game_over(self):
        '''
        None - Not over, 1 - 0 wins, 2 - X wins, 3 - tie game
        '''
        if not self.get_blank_boxes():
            return NO_RESULT, None

        result, winning_combination = self.check_win()
        if result:
            return result, winning_combination
        else:
            return None, None

    def check_win(self):
        '''
        Check all the winning combination to see if any one is true.
        If yes, return winner (1 for PLAYER or 2 for COMPUTER) otherwise return None
        '''

        result = None
        winning_combination = None
        for combination in WINNING_COMBINATIONS:
            if self.board[combination[0]] and self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]]:
                result = self.board[combination[0]]
                winning_combination = combination
                break
        return result, winning_combination

    def get_blank_boxes(self):
        '''
        Return all the possible moves
        ''' 
        return [x for x in xrange(9) if self.board[x] == BLANK]

    def check_move_for_win(self, box, value):
        '''
        Virtually make a move and see if the player wins
        '''
        self.make_move(box, value)
        result, winning_combination = self.check_win()
        result = result == value
        self.reset_move(box)
        return result

    def toggle_marker(self, value):
        '''
        Returns O for X and vice versa 
        '''
        if value == PLAYER:
            return COMPUTER
        elif value == COMPUTER:
            return PLAYER
        return None

    def best_next_move(self, value):
        """
        Return the next best move for the current board
        """

        valid_boxes = self.get_blank_boxes()

        # Check if any one of the valid moves makes you the winner
        for box in valid_boxes:
            if self.check_move_for_win(box, value):
                return box

        # Check if the opponent is about to win. Then block him
        for box in valid_boxes:
            if self.check_move_for_win(box, self.toggle_marker(value)):
                return box

        # save a copy of the board since it will get modifed during evaluate move
        board_copy = list(self.board)

        # Evalute each valid move and find the one with the highest score
        selected_box = valid_boxes[0]
        max_score = -1
        for box in valid_boxes:
            score = self.evaluate_move(box, value, value)
            if score >= max_score:
                max_score = score
                selected_box = box

        #change the board back
        self.board = board_copy

        return selected_box


    def evaluate_move(self, box, original_value, current_value):
        self.make_move(box, current_value)

        # Check if this move finished the game
        result, winning_combination = self.check_win()
        if result:
            if result == current_value:
                return 1 # Player won
            else:
                return -1 # Opponent won
        
        # Game drawn
        if not self.get_blank_boxes():
            return 0

        opponent_results = [self.evaluate_move(box, original_value, self.toggle_marker(current_value)) for box in self.get_blank_boxes()]

        if original_value == current_value:
            # Computer is playing. Opponent is human so choose the worst possible outcome for the computer
            return max(opponent_results)
        else:
            # human is playing. Again choose the worst possible outcome for computer
            return min(opponent_results)


    def make_move(self, box, value):
        ''' 
        Box is the board box number (0-9). Value is 1 for PLAYER or 2 for COMPUTER
        '''
        self.board[box] = value

    def reset_move(self, box):
        ''' Box is the board box number (0-9)
        '''
        self.board[box] = 0


