#! /usr/bin/env python
""" ----------------------------------------------------------------
" TIC-TAC-TOE W. BRUTE FORCE MINIMAX ALGORITHM
" **Code adapted from:
 " http://en.literateprograms.org/Tic_Tac_Toe_(Python)**
" author:   Bryan Bennet <bryanabennett.com>
" modified: March 23, 2011
" vim:nu:ai:si:et:ts=4:sw=4:ft=python:
"TODO:
"        -implement this with A/B Pruning Optimizations
"        -add better error checking (particularly in set_owner)
----------------------------------------------------------------"""

def are_equal(list):
    """Utility function from
    http://en.literateprograms.org/Tic_Tac_Toe_(Python)"""
    return not list or list == [list[0]] * len(list)

class Board:
    def __init__(self):
        self.cells = []
        for i in range(9):
            self.cells.append('_')
        self.cell_names = "789456123"

    def get_winner(self):
        """determine if we have a winner and who it is -
        returns [True|False,0|1]"""
        winning_rows = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]]
        for row in winning_rows:
            return [self.cells[0] != '_' and
                are_equal([self.cells[i] for i in row]), self.cells[0]]

    def get_legal_moves(self):
        x =  [pos for pos in range(9) if self.cells[pos] == "_"]
        return [self.cell_names[i] for i in x]

    def get_game_over(self):
            return self.get_winner()[0] or not self.get_legal_moves()

    def judge_game(self, winner):
        if winner == "X":
            return -1
        elif winner == "O":
            return +1
        else:
             return 0

    def judge_move(self, move, player="O"):
        try:
            self.set_owner(move, player)
            if self.get_game_over():
                return self.judge_game(self.get_winner()[1])
            outcomes = (self.judge_move(next_move, player)
                for next_move in self.get_legal_moves())
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
        finally:
            self.undo_move(move)
    def set_owner(self, cell, owner):
        self.cells[self.cell_names.index(cell)] = owner
        return True

    def start_game(self):
        """Starts a game. Human is X, Computer is 0."""
        while True:
            #PLAYER'S TURN
            print("Legal move are:", end=" ")
            for entry in self.get_legal_moves():
                print(entry, end=",  ")
            print()
            print(self.__str__())
            move = input("Enter a move: ")
            if move not in self.get_legal_moves():
                print("Not a valid move!; try again")
            else:
                self.set_owner(move, "X")
            if self.get_winner()[0]:
                break
            #COMPUTER'S TURN
            avail_moves = [(self.judge_move(move), move)
                for move in self.get_legal_moves()]
            avail_moves.sort()
            print(avail_moves)
            if self.get_winner()[0]:
                break

        if self.get_winner()[0] and self.get_winner()[1] == "X":
            print("You Win!")
        elif self.get_winner()[0] and self.get_winner()[1] == "O":
            print("Sorry, but you lose!")
        else:
            print("No more moves! Game over!")

    def undo_move(self, move):
        print(move)
        self.cells[int(move)] = "_"

    def __repr__(self):
        for x in [self.cells[0:3],self.cells[3:6],self.cells[6:9]]:
            print(' '.join(x))
        return " "

    def __str__(self):
        for x in [self.cells[0:3],self.cells[3:6],self.cells[6:9]]:
            print(' '.join(x))
        return " "

if __name__ == "__main__":
    x = Board()
    x.start_game()
