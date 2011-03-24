#! /usr/bin/env python
# vim:nu:ai:si:et:ts=4:sw=4:ft=python:
DEBUG=False

def are_equal(list):
    return not list or list == [list[0]]*len(list)

class Board:
    def __init__(self):
        self.cells = {}
        for i in range(1,10):
            self.cells[str(i)] = "_"

    def computer_player(self):
        moves = [(self.judge_move(move), move) for move in self.get_legal_moves()]
        moves.sort()
        self.set_cell(moves[-1][1],"O")

    def get_legal_moves(self):
        return [str(pos) for pos in range(1,10) if self.cells[str(pos)] == "_"]

    def get_game_over(self):
        return self.get_winner()[0] or not self.get_legal_moves()

    def get_status(self):
        """returns the board in a human readable form"""
        for i in [7,8,9,4,5,6,1,2,3]:
            if i%3 == 0:
                print(self.cells[str(i)])
            else:
                print(self.cells[str(i)], end=" ")

    def get_winner(self):
        """determine if we have a winner and who it is"""
        """returns [True|False, "O"|"X"]"""
        winning_rows = [
            [1,2,3],[4,5,6],[7,8,9],
            [7,4,1],[8,5,2],[9,6,3],
            [1,5,9],[3,5,7]]
        for row in winning_rows:
            return [self.cells[str(row[0])] != "_" and
                are_equal([self.cells[str(i)] for i in row]),
                self.cells[str(row[0])]]

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

    def judge_game(self, winner):
        if winner == "X":
            return +1
        elif winner == "O":
            return -1
        return 0

    def judge_move(self, move, player="O"):
        try:
            #This recursively calculates 'outcomes'
            self.set_cell(move, player)
            if self.get_game_over():
                return self.judge_game(self.get_winner()[1])
            outcomes = (self.judge_move(next_move, player)
                for next_move in self.get_legal_moves())

            #Calculate the weight of the move in 'outcomes'
            if player == "O":
                min_element = 1
                for outcome in outcomes:
                    if outcome == -1:
                        return outcome
                    min_element = min(outcome, min_element)
                return min_element
            elif player == "X":
                max_element = -1
                for outcome in outcomes:
                    if outcome == 1:
                        return outcome
                    max_element = max(outcome, max_element)
                return max_element

        #undo everything we've done to the board, so we
        #can use the same instance throughout the program
        finally:
            self.set_cell(move, "_")

    def set_cell(self, cell, owner):
        if owner in ["X","O", "_"]:
            self.cells[str(cell)] = owner
            return True
        else:
            return False

    def start_game(self):
        while True:
            self.human_player()
            if self.get_winner()[0]:
                break
            self.computer_player()
            if self.get_winner()[0]:
                break
if __name__ == "__main__":
    x = Board()

    if DEBUG == True:
        for i in [0,4,8]:
            x.set_cell(i,"X")
        x.get_legal_moves()
        x.get_status()

    x.start_game()
