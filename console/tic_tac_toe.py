#! /usr/bin/env python
#import pdb
import re

class BoardError(Exception): pass
class Board(object):

    BOARD_SIZE = 9

    def __init__(self):
        self.clear()

    def size(self):
        return len(self.__board)

    @property
    def winner(self):
        return self.__winner

    @property
    def last_cell(self):
        return self.__last_cell

    @property
    def grid(self):
        return self.__board

    def take_cell(self, index, claim):
        if index < self.BOARD_SIZE:
            if self.__board[index] == None:
                self.__board[index] = claim
                self.__last_cell = index
            else:
                raise BoardError, "{0} already taken".format(index)
        else:
            raise BoardError, "{0} off board".format(index)

    def get_cell(self, index):
        if index < self.BOARD_SIZE:
            return self.__board[index]
        else:
            raise BoardError, "{0} off board".format(index)

    def declare_cat(self):
        self.__winner = "cat"

    def clear(self):
        self.__board = []
        self.__winner = None
        self.__last_cell = None
        for i in range(Board.BOARD_SIZE):
            self.__board.append(None)

    def __check_cells(self, index1, index2, index3):
        a,b,c = self.get_cell(index1), self.get_cell(index2), self.get_cell(index3)
        if a == None and b == None and c == None:
            return False
        result = (a == b and a == c)
        if result:
            self.__winner = a
        return result



    def __check_rows(self):
        result = False
        result = self.__check_cells(0,1,2)
        if result == False:
            result = self.__check_cells(3,4,5)
        if result == False:
            result = self.__check_cells(6,7,8)
        return result

    def __check_columns(self):
        result = False
        result = self.__check_cells(0,3,6)
        if result == False:
            result = self.__check_cells(1,4,7)
        if result == False:
            result = self.__check_cells(2,5,8)
        return result

    def __check_diagonals(self):
        result = False
        result = self.__check_cells(0,4,8)
        if result == False:
            result = self.__check_cells(2,4,6)
        return result

    def check_board(self):
        result = False
        result = self.__check_rows()
        if result == False:
            result = self.__check_columns()
        if result == False:
            result = self.__check_diagonals()
        return result

class Player(object):

    def __init__(self, marker = None, board = None, name = None):
        self.__marker = marker
        self.__board = board
        self.__name = name

    @property
    def marker(self):
        return self.__marker

    @marker.setter
    def marker(self, value):
        self.__marker = value

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self,value):
        self.__board = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def place_marker(self, cell_index):
        self.__board.take_cell(cell_index, self.__marker)
        self.__board.check_board()



class ComputerPlayer(Player):
    PATTERNS = (
        (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (2,4,6),
        (0,4,8),
        )
    def __init__(self, marker = None, board = None, name = "Computer"):
        Player.__init__(self, marker, board, name)

    def __check_probability_pattern(self, pattern):
        prob_count = 0
        for index in pattern:
            if self.board.get_cell(index) == None:
                prob_count += 1
            if self.board.get_cell(index) == self.marker:
                return 0
        return prob_count

    def __investigate_board(self):
        current_pattern = None
        current_probability = 3
        for pattern in self.PATTERNS:
            if self.board.last_cell in pattern:
                prob = self.__check_probability_pattern(pattern)
                if prob > 0 and prob < current_probability:
                    current_pattern = pattern
                    current_probability = prob
        if current_probability == 3:
            self.board.declare_cat()
            return -1
        for index in current_pattern:
            if self.board.get_cell(index) == None:
                return index

    def place_marker(self, cell_index = -1):
        index = self.__investigate_board()
        if index == -1:
            self.board.declare_cat()
        else:
            Player.place_marker(self, index)


class Game(object):

    def __init__(self):
        pass

    def setup(self):
        self.board = Board()
        print "Welcome to Tic-Tac-Toe"
        name = raw_input("What is your Name: ")
        marker = raw_input("which marker do you want X or O: ")
        while marker not in ["X", "O"]:
            marker = raw_input("Come on pick one of the two X or O: ")
        if marker.upper() == "X":
            computer_marker = "O"
        else:
            computer_marker = "X"
        self.player = Player(marker, self.board, name)
        self.computer = ComputerPlayer(computer_marker, self.board)

    def draw(self):
        str = "+---+---+---+\n"
        counter = 0
        for ele in self.board.grid:
            body = ele
            if body == None:
                body = "{0}".format(counter +1)
            str += "| {0} ".format(body)
            counter += 1
            if counter % 3 == 0:
                str +="|\n+---+---+---+\n"
        print str


    def update(self):
        choice = raw_input("Selet where you want to place your marker(1-9) or Q to quit the game:")
        while re.match("[1-9qQ]", choice) == None:
            choice = raw_input("Please enter a valid option(1-9 or Q): ")
        if choice.isdigit():
            self.player.place_marker(int(choice)-1)
            if self.board.winner == None:
                self.computer.place_marker()
        else:
            self.board.declare_cat()


    def game_loop(self):
        print "Please Go First\n"
        while self.board.winner == None:
            self.draw()
            self.update()
        self.draw()
        print "The winner is {0}".format(self.board.winner)
        if re.match("[yY]", raw_input("Do you wish to play again(y/n):")) != None:
            self.board.clear()
            self.game_loop()

    def start_game(self):
        self.setup()
        self.game_loop()

if __name__ == "__main__":
    Game().start_game()
