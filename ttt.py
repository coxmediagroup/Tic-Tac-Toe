from random import randrange

DEBUG=False
winning_rows = [[1,2,3],[4,5,6],[7,8,9],
                        [7,4,1],[8,5,2],[9,6,3],
                        [1,5,9],[3,5,7]]

def are_equal(list):
    return not list or list == [list[0]]*len(list)

class Board:
    def __init__(self):
        self.cells = {}
        for i in range(1,10):
            self.cells[str(i)] = "_"

    def computer_player(self):
        # 1) if a winning move exists, take it
        # 2) if an opponent is going to win, block them
        # 3) if the center square is available, take it
        # 4) if a corner square is available, take it
        # 5) if a side square (8,4,6,2) is available and you've
        #     already got center, take it.
        # 6) else...pick randomly?
        # Also: Good god is this ugly and makes a case for
        # switch statements in python -_-

        moves = self.get_legal_moves()
        move = None
        for row in winning_rows:
            x = self.cells[str(row[0])]
            y = self.cells[str(row[1])]
            z = self.cells[str(row[2])]

            # check for #1
            if move == None and ( x == "O" or y == "O" or z == "O"):
                if x == "O" and y == "O" and z == "_":
                    move = row[2]
                elif y== "O" and z == "O" and x == "_":
                    move = row[0]
                elif x == "O" and z == "O" and y == "_":
                    move = row[1]
                if DEBUG == True:
                    print("Method #1 - " + str(move))

            # check for #2
            if move == None and (x == "X"  or y == "X" or z == "X"):
                if x == "X" and y == "X" and z == "_":
                    move = row[2]
                elif y == "X" and z == "X" and x == "_":
                    move = row[0]
                elif x == "X" and z == "X" and y == "_":
                    move = row[1]
                if DEBUG == True:
                    print("Method #2 - " + str(move))

        #check for #3
        if move == None and self.cells['5'] == "_":
            if DEBUG == True:
                print("Using #3")
            move  = '5'

        #check for #4
        if move == None:
            if DEBUG == True:
                print("Using #4")
            if self.cells['7'] == "_":
                move = '7'
            elif self.cells['9'] == "_":
                move = '9'
            elif self.cells['1'] == "_":
                move = '1'
            elif self.cells['3'] == "_":
                move = '3'

        #check for #5
        if move == None and self.cells['5'] == "O":
            if DEBUG == True:
                print("Using #5")
            if self.cells['8'] == "_":
                move = '8'
            elif self.cells['6'] == "_":
                move = '6'
            elif self.cells['4'] == "_":
                move = '4'
            elif self.cells['2'] == "_":
                move = '2'
        if move == None:
            if DEBUG == True:
                print("Nothing worked...Picking Randomly")
            move = int(randrange(0, len(self.get_legal_moves()),1))
        if DEBUG == True:
           print(move)
        self.set_cell(move, "O")

    def get_legal_moves(self):
        return [str(pos) for pos in range(1,10) if self.cells[str(pos)] == "_"]

    def get_game_over(self):
        return self.get_winner()[0]  or not self.get_legal_moves()

    def get_status(self):
        """returns the board in a human readable form"""
        for i in [7,8,9,4,5,6,1,2,3]:
            if i%3 == 0:
                print(self.cells[str(i)])
            else:
                print(self.cells[str(i)], end=" ")

    def get_winner(self):
        """determine if we have a winner and who it is"""
        """returns [True|False, "O"|"X"|"_"]"""

        for row in winning_rows:
            if self.cells[str(row[0])] != "_" and are_equal([self.cells[str(i)] for i in row]):
                return [True, self.cells[str(row[0])]]
        return [False, "_"]

    def human_player(self):
        self.get_status()
        print("Legal moves are:", end=" ")
        legal_moves = self.get_legal_moves()
        print(legal_moves)
        move = input("Please enter a move:")
        while move not in legal_moves:
            print("{move} is not a legal move! Try again!".format(move=move))
            move = input("Please enter a move:")
        self.set_cell(move, "X")

    def set_cell(self, cell, owner):
        if owner in ["X","O", "_"]:
            self.cells[str(cell)] = owner
            return True
        else:
            return False

    def start_game(self):
        coin_flip = randrange(0,2,1)
        if coin_flip == 0:
            print("You go first this time.")
            while True:
                if self.get_game_over():
                  break
                self.human_player()
                if self.get_game_over():
                  break
                self.computer_player()
                if self.get_game_over():
                    break
        elif coin_flip == 1:
            print("I'll go first this time.")
            while True:
                if self.get_game_over():
                  break
                self.computer_player()
                if self.get_game_over():
                  break
                self.human_player()
                if self.get_game_over():
                    break
        if self.get_winner()[0]:
            self.get_status()
            print(self.get_winner()[1] + " wins!")
        else:
            print("No one wins! Try again!")
if __name__ == "__main__":
    x = Board()
    x.start_game()
