
class View:
    def __init__(self, board):
        self.board = board

    def __displayRow(self, row):
        print " ", row[0], " | ", row[1], " | ", row[2]

    def __displaySeparator(self):
        print "-----+-----+-----"
        
    def displayBoard(self):
        boardData = self.board.fetch()
        self.__displayRow(boardData[0])
        self.__displaySeparator()
        self.__displayRow(boardData[1])
        self.__displaySeparator()
        self.__displayRow(boardData[2])
        print "\n"

    def __displayInvalidMove(self):
        print "Invalid move. Please enter a valid move."
        return 0
    
    def __validateMove(self, validMoves, move):
        try:
            move = int(move)
            if move not in validMoves:
                move = self.__displayInvalidMove()
        except ValueError:                
            move = self.__displayInvalidMove()
        return move

    def inputMove(self):
        validMoves = self.board.validPositions()
        stringValidMoves = ", ".join(str(move) for move in validMoves)
        move = 0
        while move not in validMoves:
            move = raw_input("Enter move: (" + stringValidMoves + "): ")
            print "\n"
            move = self.__validateMove(validMoves, move)
        return move

    def __displayInvalidStartingPlayer(self):
        print "Invalid starting player. Please enter 1 for Human, or 2 for Computer."
        return 0

    def __validateStartingPlayer(self, validOptions, player):
        try:
            player = int(player)
            if player not in validOptions:
                player = self.__displayInvalidStartingPlayer()
        except ValueError:
            player == self.__displayInvalidStartingPlayer()
        return player

    def inputStartPlayer(self):
        validOptions = [1, 2]
        player = 0
        while player not in validOptions:
            player = raw_input("Enter startng player (1 - Human, 2 - Computer): ")
            print "\n"
            player = self.__validateStartingPlayer(validOptions, player)
        return player

    
