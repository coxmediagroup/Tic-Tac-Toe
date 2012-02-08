from random import random
from copy import deepcopy

class TicTacToe:
    """An unbeatable Tic Tac Toe game.  Human always starts. """
    def __init__(self):
        self.board = [list(range(3)), list(range(3, 6)), list(range(6, 9))]
        self.human = 'x'
        self.computer = 'o'
        self.board_string = (
                 " {0[0][0]} | {0[0][1]} | {0[0][2]}\n"
                 "-----------\n"
                 " {0[1][0]} | {0[1][1]} | {0[1][2]}\n"
                 "-----------\n"
                 " {0[2][0]} | {0[2][1]} | {0[2][2]}\n")    

    def human_move(self):
        """Accepts / validates the input for a human move.
             
             Returns True on a valid move.
             Otherwise False."""
        move = raw_input("Your turn: ")
        if len(move) == 1 and ord(move) >= ord('0') and ord(move) < ord('9'):
            move = int(move) 
            if isinstance(self.board[move // 3][move % 3], int):
                self.board[move // 3][move % 3] = self.human
                return True
            else:
                print("This position has already been played. Try again!")
        else:
            print("Input must be between 1 and 9 inclusive!")
        return False
    
    def computer_move(self):
        """The logic for the computer move. From wikipedia:

             Attempt to move in this order
             1. Win
             2. Block win
             3. Fork
             4. Block Fork
             5. Center
             6. Opposite corner
             7. Empty corner
             8. Empty side
        """
        (row, col) = (self.win(self.board, self.computer) or
                                    self.win(self.board, self.human) or
                                    self.fork(self.board, self.computer) or
                                    self.block_fork() or
                                    self.center() or
                                    self.opposite_corner() or
                                    self.empty_corner() or
                                    self.empty_side())
        self.board[row][col] = self.computer

    def win(self, board, mark):
        """Finds a position that will win the game for a given 
           board with a given mark.

           Returns the row, col of or None
        """
        scratch_board = deepcopy(board)
        for row in range(3):
            for col in range(3):
                if isinstance(scratch_board[row][col], int):
                    scratch_board[row][col] = mark
                    if self.tic_tac_toe(scratch_board):
                        return row, col
                    scratch_board[row][col] = 3 * row + col

    
    def fork(self, board, mark):
        """Finds a position that will fork (a move that creates two 
           possible following winning moves).
             
           Returns the position or None
        """
        scratch_board = deepcopy(board)
        for row in range(3):
            for col in range(3):
                if isinstance(scratch_board[row][col], int):
                    scratch_board[row][col] = mark
                    if self.forked(scratch_board, mark):
                        return row, col
                    scratch_board[row][col] = row * 3 + col

    def forked(self, board, mark):
        """
        For a given board and mark, determine if a fork exists.
        """
        win = self.win(board, mark)
        if win:
            board[win[0]][win[1]] = 'i'
            second_win = self.win(board, mark)
            if second_win:
                return True
            board[win[0]][win[1]] = win[0] * 3 + win[1]

    def block_fork(self):
        """Blocks an impending fork.
             If the oponent can fork next move,
                 try to threaten a win or
                 block the fork
             Returns the position or None.
        """
        if self.fork(self.board, self.human):
            for row in range(3):
                for col in range(3):
                    if isinstance(self.board[row][col], int):
                        board = deepcopy(self.board)
                        board[row][col] = self.computer
                        win_pos = self.win(board, self.computer)
                        if win_pos:
                            board[win_pos[0]][win_pos[1]] = self.human
                            if ((self.tic_tac_toe(board) != self.human) and 
                                not self.forked(board, self.human)):
                                return row, col
            return self.fork(self.board, self.human)

    def center(self):
        """Checkes if the center position is empty.
             
           Returns the position or None
        """
        if isinstance(self.board[1][1], int):
            return 1, 1

    def opposite_corner(self):
        """Detects if the opponent has selected a corner and if  
           the opposite corner is available.

           Returns the position or None
        """
        def get_pos(board, pos):
            """
            Returns the value in baord at the givent position
            """
            return board[pos[0]][pos[1]]
        corners = (((0, 0),(2, 2)), ((0, 2),(2, 0)))
        for pair in corners:
            if (get_pos(self.board, pair[0]) == self.human and 
                    isinstance(get_pos(self.board, pair[1]), int)):
                return pair[1]
            if (get_pos(self.board, pair[1]) == self.human and 
                    isinstance(get_pos(self.board, pair[0]), int)):
                return pair[0]

    def empty_pos(self, positions): 
        """
        Returns the first empty position found on the board
        """
        for row, col in positions:
            if isinstance(self.board[row][col], int):
                return row, col

    def empty_corner(self):
        """Detects if any corners are empty.    
             
           Returns the position or None
        """
        return self.empty_pos(((0, 0), (0, 2), (2, 0), (2, 2)))

    def empty_side(self):
        """Detects if any of the side positions are empty.
             
           Returns the position or None"""
        return self.empty_pos(((0, 1), (1, 0), (1, 2), (2, 1)))
            
    def tic_tac_toe(self, board):
        """Examines the board to determine if a tic tac toe
             has occured.
            
             Returns the character that won ('x' or 'o')
                 or None
        """
        def the_winner(combinations):
            """Check if all members of the list are the same value, 
                 if so, return that value"""
            for combo in combinations:
                if len(set(combo)) == 1:
                    return combo[0]
        if len(set((v for row in self.board for v in row))) == 2:
            return "cat"
        winner = the_winner(self.win_combinations(board))
        return winner
        
    def win_combinations(self, board):
        """
        Returns the values for each of the possible 
        3 in a row combinations.
        """
        return (board[0], board[1], board[2],  # Horizontal
                tuple(row[0] for row in board),    # Verticals
                tuple(row[1] for row in board),
                tuple(row[2] for row in board),
                (board[0][0], board[1][1], board[2][2]),  # Diagonals
                (board[0][2], board[1][1], board[2][0]))

    def __str__(self):
        """Represents the board as a string."""
        return self.board_string.format(self.board)
 
    def main(self):
        """This function drives the game."""
        moves = 0
        winner = None
        if random() < 0.5:
            print("You go first!")
        else:
            print("I went first!")
            moves += 1

        while not winner:
            if moves % 2 == 0:
                print(self)
                while not self.human_move():
                    pass
            else:
                self.computer_move()
            moves += 1
            winner = self.tic_tac_toe(self.board)
        
        print(self)
        print("And the winner is............... {0}!!!".format(winner))
            

if __name__ == '__main__':
    Game = TicTacToe()
    Game.main()
