#tictactoe program authored by Ronald Braly

import sys
from collections import namedtuple

Coord = namedtuple("Coord", ["row", "column"])

ROWS = [[Coord(0,0),Coord(0,1),Coord(0,2)],
        [Coord(1,0),Coord(1,1),Coord(1,2)],
        [Coord(2,0),Coord(2,1),Coord(2,2)]]
COLUMNS = [[Coord(0,0),Coord(1,0),Coord(2,0)],
        [Coord(0,1),Coord(1,1),Coord(2,1)],
        [Coord(0,2),Coord(1,2),Coord(2,2)]]
DIAGONALS = [[Coord(0,0),Coord(1,1),Coord(2,2)],
        [Coord(0,2),Coord(1,1),Coord(2,0)]]
CORNERS = [Coord(0,0),Coord(0,2),Coord(2,0), Coord(2,2)]
CROSS = [Coord(1,1), Coord(1,0), Coord(1,2), Coord(0,1), Coord(2,1)]

class Board():
    def __init__(self):
        self.board = [[" " for x in range(3)] for y in range(3)]

    def __repr__(self):
        return "\n  0 1 2 \n" \
             + "0 " + "|".join(self.board[0]) + "\n  -----\n" \
             + "1 " + "|".join(self.board[1]) + "\n  -----\n" \
             + "2 " + "|".join(self.board[2]) + "\n"

    def is_open(self, coord):
        return self.board[coord.row][coord.column] == " "

    def make_move(self, coord, player_mark):
        self.board[coord.row][coord.column] = player_mark

    @property
    def moves_left(self):
        return any([" " in row for row in self.board])

    @property
    def winning_player(self):
        for each_row in self.board:
            if len(set(each_row)) == 1 and " " not in each_row:
                return each_row[0]
        for each_column in [
                [self.board[0][x], self.board[1][x], self.board[2][x]]
                for x in range(3)]:
            if len(set(each_column)) == 1 and " " not in each_column:
                return each_column[0]
        for each_diagonal in [
                [self.board[0][0], self.board[1][1], self.board[2][2]],
                [self.board[0][2], self.board[1][1], self.board[2][0]]]:
            if len(set(each_diagonal)) == 1 and " " not in each_diagonal:
                return each_diagonal[0]
        return None

class Player():
    def __init__(self, player_mark, player_type = "H"):
        self.player_mark = player_mark
        self.player_type = player_type

    def get_move(self, board = None):
        result = None
        if self.player_type == "H":
            while True:
	        row_input = ""
	        while row_input not in ["0","1","2"]:
	            row_input = raw_input("Player %s, enter row (0,1, or 2): "
                        %self.player_mark)
	        column_input = ""
	        while column_input not in ["0","1","2"]:           
	            column_input = raw_input("Player %s, enter column (0,1, or 2): "
                        %self.player_mark)
                result = Coord(row = int(row_input),
                               column = int(column_input))
                return result
        else:
            # Else condition is for determining computer moves. Ideally, this
            # would be an implementation of an algorithm using a decision tree
            # or an A* algorithm, but there are deadlines and the perfect is
            # the enemy of the good, so instead some common moves and counter
            # moves are handled since there aren't very many.

            # If there is a winning move, take it
            for entity in [ROWS, COLUMNS, DIAGONALS]:
                for each in entity:
                    triple = [board.board[x.row][x.column] for x in each]
                    if triple.count(' ') == 1:
                        other_marks = set(triple)
                        other_marks.remove(' ')
                        if len(other_marks) == 1 and self.player_mark in other_marks:
                            for square in each:
                                if board.is_open(square):
                                    return square
            # If theopponent can win, block them
            for entity in [ROWS, COLUMNS, DIAGONALS]:
                for each in entity:
                    triple = [board.board[x.row][x.column] for x in each]
                    if triple.count(' ') == 1:
                        other_marks = set(triple)
                        other_marks.remove(' ')
                        if len(other_marks) == 1:
                            for square in each:
                                if board.is_open(square):
                                    return square
            # Special case when non-computer controlled player has moved first
            # and played a corner. Computer should select center square and
            # cross squares as that's the only defensible move.
            all_squares = []
            for row in ROWS:
                for each in row:
                    all_squares.append(board.board[each.row][each.column])
            open_squares = all_squares.count(' ')
            player_squares = all_squares.count(self.player_mark)
            other_player_squares = len(all_squares) - (open_squares + player_squares)
            if other_player_squares > player_squares:
                for square in CROSS:
                    if any(not board.is_open(square) for square in CORNERS):
                        if board.is_open(square):
                            return square
            # Else, play a corner
            for square in CORNERS:
                if board.is_open(square):
                    return square
            # Else, play any move
            for x in range(3):
                for y in range(3):
                    square = Coord(row = x, column = y)
                    if board.is_open(square):
                        return square

def run():

    play_again = True
    play_again_choices = ['Y', 'YES']
    while play_again:
        play_again = False
        player_choice = ""
        player_choices = ["X", "O"]
        while player_choice.upper() not in player_choices:
            player_choice = raw_input("Which player will be controlled by human (X or O)?: ")
    
        player_choice = player_choice.upper()
        human_player = Player(player_choice)
        player_choices.remove(player_choice)
        computer_player = Player(player_choices[0], "C")
    
        players = [computer_player, human_player]
        if human_player.player_mark == "X":
            players = [human_player, computer_player]
    
        board = Board()
        round = 0
        winning_player = None
        print board
        while board.moves_left and not winning_player:
            player = players[round%2]
            while True:
                player_move = player.get_move(board)
                if board.is_open(player_move):
                    break
                print "That square is not open, try again."
            board.make_move(player_move,player.player_mark)
            print board
            winning_player = board.winning_player
            round += 1
    
        if winning_player:
            print "\n -- A winner is player %s -- " %winning_player
        print "\n Game Over \n"
        
        play_again_choice = raw_input('Play again? (Y or y or yes): ')
        if play_again_choice.upper() in play_again_choices:
            play_again = True
            
    print 'Thanks for playing...'
        

if __name__ == "__main__":


    try:
        run()
    except Exception, e:
        print "\nEncountered error, program stopping"
        print str(e)
    sys.exit(0)
