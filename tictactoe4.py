#!/usr/bin/env python

class Game:
    def __init__(self):
        # initialize default game setups
        self.board = [ '-' for i in range(0,9) ]
        self.lastmoves = []
        self.winner = None

    def print_board(self):
        # show current board
        print ""
        for j in range(0,9,3):
            for i in range(3):
                if i == 0:
                    print "",
                if self.board[j+i] == '-':
                    print "%s" % ((j+i)+1),
                else:
                    print "%s" % self.board[j+i],
                if i != 2:
                    print "|",
            if j < 6:
                print "\n-----------",
            print "\n",
        print ""

    def get_avail_positions(self):
        # get available positions
        moves = []
        for i,v in enumerate(self.board):
            if v == '-':
                moves.append(i)
        return moves

    def mark(self, marker, pos):
        # change board to reflect move
        self.board[pos] = marker
        self.lastmoves.append(pos)

    def undo_last_move(self):
        # undo last move
        self.board[self.lastmoves.pop()] = '-'
        self.winner = None

    def is_gameover(self):
        # check if game is over
        win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for i,j,k in win_positions:
            if self.board[i] == self.board[j] == self.board[k] and self.board[i] != '-':
                self.winner = self.board[i]
                return True
        if '-' not in self.board:
            self.winner = '-'
            return True
        return False

    def play(self, player1, player2):
        # main game loop
        self.p1 = player1
        self.p2 = player2
        for i in range(9):
            self.print_board()
            if i%2==0:
                if self.p1.type == 'H':
                    print "[Human's Move]"
                else:
                    print "[Computer's Move]"
                self.p1.move(self)
            else:
                if self.p2.type == 'H':
                    print "[Human's Move]"
                else:
                    print "[Computer's Move]"
                self.p2.move(self)
            if self.is_gameover():
                self.print_board()
                if self.winner == '-':
                    print "\nGame ends in Draw"
                else:
                    print "\nWinner: %s\n" % self.winner
                return

class HumanPlayer:
    # human player class
    def __init__(self, marker):
        self.marker = marker
        self.type = 'H'
   
    def move(self, gameins):
        while True:
            m = raw_input("\tInput the numbered position you want to play: ")
            try:
                m = int(m) - 1
            except:
                m = -1
            if m not in gameins.get_avail_positions():
                print "Invalid move. Retry"
            else:
                break
        gameins.mark(self.marker, m)

class ComputerPlayer:
    # computer player class
    def __init__(self, marker):
        self.marker = marker
        self.type = 'C'
        if self.marker == 'X':
            self.oppmarker = 'O'
        else:
            self.oppmarker = 'X'

    def move(self, gameins):
        move_position,score = self.move_max(gameins)
        gameins.mark(self.marker, move_position)

    def move_max(self, gameins):
        # Find maximized move
        bscore = None
        bmove = None
        for m in gameins.get_avail_positions():
            gameins.mark(self.marker, m)
            gameins.print_board()
            if gameins.is_gameover():
                score = self.get_score(gameins)
            else:
                move_position,score = self.move_min(gameins)
            gameins.undo_last_move()
            if bscore == None or score > bscore:
                bscore = score
                bmove = m
        return bmove, bscore

    def move_min(self, gameins):
        # Find the minimized move
        bscore = None
        bmove = None
        for m in gameins.get_avail_positions():
            gameins.mark(self.oppmarker, m)
            if gameins.is_gameover():
                score = self.get_score(gameins)
            else:
                move_position,score = self.move_max(gameins)
            gameins.undo_last_move()
            if bscore == None or score < bscore:
                bscore = score
                bmove = m
        return bmove, bscore

    def get_score(self, gameins):
        # eval moves and quality of move
        if gameins.is_gameover():
            if gameins.winner == self.marker:
                return 1 # Won
            elif gameins.winner == self.oppmarker:
                return -1 # Opponent won
        return 0 # Draw

if __name__ == '__main__':
    game=Game()    
    player1 = HumanPlayer("X")
    player2 = ComputerPlayer("O")
    game.play(player1, player2)

