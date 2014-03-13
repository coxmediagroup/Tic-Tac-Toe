import re

class TicTacToe():
    def __init__(self):
        #what stage of the game we are in. 
        self.numTurn = 1 

        #layout of basic info we may need to keep in mind. 
        self.squares = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.availSquares = self.squares
        self.xSquares = set()
        self.oSquares = set()
        self.corners = {1, 3, 7, 9}
        self.center = {5}
        self.edges = {2, 4, 6, 8}

        #Winning combos I am calling RDCs(Rows, Diagonals, Columns)
        self.RDCs = {'R1': [1, 2, 3],
                'R2': [4, 5, 6],
                'R3': [7, 8, 9],
                'C1': [1, 4, 7],
                'C2': [2, 5, 8],
                'C3': [3, 6, 9],
                'D1': [1, 5, 9],
                'D2': [3, 5, 7]}

        self.board="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
1    |    2    |    3\
\n     |         |\n     |         |\n---------------------\n     |         |\n     |         |\n\
4    |    5    |    6\
\n     |         |\n     |         |\n---------------------\n     |         |\n     |         |\n\
7    |    8    |    9"

game=TicTacToe()
players=['X', 'O']

if __name__ == '__main__':
    while True:
        print re.sub('[0-9]', '-', game.board)
        #print game.board
        move = raw_input("Pick a spot: ")
        game.availSquares.discard(int(move))
        
        
        
    







