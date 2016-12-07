#!/usr/bin/env python3  # Let's be current-ish.

# This is an original implementation done without studying any existing code.
# It follows my practice of making things as simple and as clear as possible
# so that code reviews and maintenance don't have to fight through obscure code.
# I have eschewed "premature" optimization, too. :-)

# The board, the rules, and the players are represented by objects.
# The rules object uses Python's first class functions to order the rules.

# Custom exceptions are raised for situations that require human intervention.

# No unit tests, no QA.  Sorry.  There is some input validation.  It would be
# nice to present a formal proof that this algorithm works, but, actually,
# it is ad-hoc.


from __future__ import print_function # for syntax compatibility on Python 2 & Python 3
import sys

class MyException(BaseException):
    "Just some basic required behavior.  Stringify method makes life easier."
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MarkError(MyException): # I dislike multipurpose exceptions.  Hence these subclasses.
    pass
class RuleError(MyException):
    pass
class BoardFull(MyException):
    "Whoops!  There are no free squares."
    pass
class WinHappened(MyException):
    pass
class WinError(MyException):
    pass

class Board():
    """
    Create the traditional 3X3 tic-tac-toe board, populated with empty cells.
    Because performance against a human player is not an issue I can use the
    output format as the native data structure.  This is a luxury but it will
    make the code clearer.  There is partial support for larger boards, but
    I'm not going to enable it.
    """
    def __init__(self, board_size = 3):
        # The optional board_size keyword argument defaults to the standard size.
        self.extent = range(board_size)
        self.extent_max = board_size - 1 # Zero-based
        self.blank = "-"
        self.board = []
        for i in self.extent:
            self.board.append([]) # List that represents a row.
            for j in self.extent:
                self.board[i].append(self.blank)

    def contents_of(self, position):
        return self.board[ position[0] ][ position[1] ]

    def mark(self, position, player):
        if not self.contents_of(position) is self.blank:
            raise MarkError("Position is not blank.  It's already taken.")
        self.board[ position[0] ][ position[1] ] = player
        print("Player {} takes postition {}".format(player, position))
    def __str__(self):
        "Return a text representation of the board."
        string = ""
        for i in self.extent:
            for j in self.extent:
               string += self.board[j][i]
            string += "\n"
        return string

class Player():
    "Simple container for player information."
    def __init__(self, token, board):
        self.token = token
        self.board = board
        self.vectors = Vectors()
        self.rules = Rules(self.token, self.board)
        self.them = "O" if self.token is "X" else "X"
    def move(self):
        "This is where the computer calculates and makes its move."
        for rule in self.rules.list:
            if rule():
                break  # Stop after a rule makes a move
    def human_move(self, position):
        "This is how a human makes a move."
        self.board.mark(position, self.token)
        if self.rules.we_have_a_winner():
            raise WinHappened('You win!')
class Rules():
    """
    Just a place to keep the strategy steps that I'm calling rules.
    Methods listed in @list are the strategy steps to take, in proper order.
    The other methods in this class are just helpers.
    """
    def __init__(self, me, board):
        self.token = me
        self.board = board
        self.blank = "-"
        self.them = "O "if self.token is "X" else "X"
        self.vectors = Vectors()
        self.list = [self.win, self.block_opponent, self.take_center,
                     self.take_corner,self.take_anything, self.board_full] # These are the strategy steps.  Order is critical.

    #### Rule implementations ####

    def win(self):
        print("{} applying rule: win".format(self.token))
        for vector in self.vectors.list:
            if self.i_can_win_in(vector):
                print("Computer ({}) can win in vector: {}".format(self.token, vector))
                target = self.winning_move_in(vector)
                print("Winning move: {}".format(target))
                self.board.mark(target, self.token)
                # print("{} wins".format(self.token))
                raise WinHappened('The computer wins!')
                return True
        print("  Win rule failed to find a move.")
        return False
    def block_opponent(self):
        print("{} applying rule: block".format(self.token))
        for vector in self.vectors.list:
            print('looking at vector: ', vector)
            if self.opponent_can_win_in(vector):
                print("Opponent can win in {}".format(vector))
                target = self.winning_move_in(vector)
                print("Move to block opponent's win: {}".format(target))
                self.board.mark(target, self.token)
                return True
        print("  Block rule failed to find a move.")
        return False
    def take_center(self): # TODO: Add support for other board sizes.
        print("{} applying rule: take_center".format(self.token))
        position = [1,1]
        if self.board.contents_of(position) == self.board.blank:
            self.board.mark(position, self.token)
            return True
        else:
            print("  Take_center rule failed to find a move.")
            return False
    def take_corner(self): # TODO: Add support for other board sizes.
        print("{} applying rule: take_corner".format(self.token))
        for position in [ [0,0], [0,2], [2,0], [2,2] ]:
            # print("pos: #{position}")
            if self.board.contents_of(position) == self.board.blank:
                self.board.mark(position, self.token)
                return True
        print("  Take corner rule failed to find a move.")
        return False
    def take_anything(self):
        print("{} applying rule: take_anything".format(self.token))
        for vector in self.vectors.list:
            for position in vector:
                if self.board.contents_of(position) == self.board.blank:
                    self.board.mark(position, self.token)
                    return True
        print("{} applying rule: take_anything failed to find a blank cell".format(self.token))
        return False # The board is actually full.  We detect that in the next rule."
    def board_full(self):
        raise BoardFull("No rule could find a move to make.  There are no empty cells.")

    #### Helper routines ####
    #
    # Note how the names of these routines lend themselves to code that reads
    # as if it were vernacular English.  The logic can be proofread by non-programmers.
    # I came up with this at Regression Logic when working with a math professor.
    #

    def count_in(vector, mark):
        count = 0
        for position in vector:
            if self.board.contents_of(position) == mark:
                count += 1
        return count
    def i_can_win_in(self, vector):
        return self.can_win_in(self.token, vector)
    def opponent_can_win_in(self, vector):
        return self.can_win_in(self.them, vector)
    def can_win_in(self, player, vector):
        count = 0; has_vacancy = False
        for position in vector:
            if self.belongs_to(position, player):
                count += 1
            if self.is_blank(position):
                has_vacancy = True
        # The below is Guido's sort of ternary assignment syntax.  It's a bit funny-looking but it is standard.
        return True if (count == 2 and has_vacancy) else False
    def belongs_to(self, position, player):
        return True if self.board.contents_of(position) == player else False
    def is_mine(self, position):
        return True if self.board.contents_of(position) == self.token else False
    def is_blank(self, position):
        return True if self.board.contents_of(position) == self.blank else False
        return False
    def winning_move_in(self, vector):
        for position in vector:
            if self.board.contents_of(position) is self.blank: # We have all but one, this is the position of the blank.
                return position
        raise WinError("winning_move_in error")
    def we_have_a_winner(self):
        winner = False
        for vector in self.vectors.list:
            a = [self.board.contents_of(position)for position in vector]
            if not self.board.blank in a: # Must contain no blanks.
                if len(set(a)) == 1:
                    winner = True
        return True if winner else False

class Vectors(): # Todo: A variable-size board version that is as clear as this version is.
    "This is the list of all possible ways to win, defined as lists of x/y coordinates."
    def __init__(self):
        self.list = [
                  # Horizontal.  This is the natural layout and a useful visual map.
                  [ [0,0], [0,1], [0,2] ],
                  [ [1,0], [1,1], [1,2] ],
                  [ [2,0], [2,1], [2,2] ],
                  # Vertical (these rows are actually columns)
                  [ [0,0], [1,0], [2,0] ],
                  [ [0,1], [1,1], [2,1] ],
                  [ [0,2], [1,2], [2,2] ],
                  # Diagonal
                  [ [0,0], [1,1], [2,2] ],
                  [ [2,0], [1,1], [0,2] ]
                ]
    def __str__(self):
        return repr(self.list)

# This is effectively the main loop.
def play_game(board, X, O):
    while True:
        try:
            user_input = input("Your move: ")
            if hasattr(user_input, '__iter__'): # We get a tuple if stdin is a terminal.
                coordinates = user_input
            else: # Running under Emacs, we get a string.
                coordinates = [ int(q) for q in user_input.split(",") ] # List Comprehension
        except (ValueError, IndexError) as e:
            print("Tsk. That input does not appear to resemble two integers separated by a comma.")
            continue # Okay, let the human try again.
        try:
            X.human_move(coordinates)
        except MarkError as e:
            print(e)
            continue
        except WinHappened as e:
            print(board)
            print("You win!")
            sys.exit(0)
        except BoardFull as e:
            draw()
        print("")
        print('After your move, the board is:')
        print(board)
        try:
            O.move()
        except WinHappened as e:
            print("")
            print("After the computer's sublime finishing move, the board is:")
            print(board)
            print(e)
            sys.exit(0)
        except BoardFull as e:
            draw()
        print("")
        print("After the computer's move, the board is now:")
        print(board)


def draw():
    print("")
    print("That's a draw. Nobody wins.  I wouldn't play him; he wins a lot!")
    sys.exit(1) # Let's exit with a bad status just to show we can.

def main():
    "Create board and players; print directions; play the game."
    board = Board()
    X = Player("X", board)
    O = Player( "O", board)

    usage = """Tic Tac Toe: Computer is O, you are X.
    Make your move by specifying a cell as X, Y.
    A valid move is 1,1.
    The upper left cell is 0,0."""

    print(usage)
    play_game(board, X, O)


# The standard idiom for standalone modules
if __name__ == '__main__':
    main()
