import Board
import Brain




class Game(object):

    def __init__(self):

        self.board = Board.Board()
        self.current_player = self.board.firstMove()

    def main(self):
        """Run the game"""

        self._print_message('Welcome to Tic Tac Toe!')
        while True:
            self.board.inputPlayerLetter()
            self._print_message('The %s will go first.' % self.current_player)
            self.play()
            self._print_message("Ok, I'll go play a nice game of global thermonuclear war.")
            return

    def _toggle_turn(self):
        """switch the player"""
        if self.current_player == 'computer':
            self.current_player = 'player'
        else:
            self.current_player = 'computer'

    def _player_move(self):
        """Do the player move"""
        self.board.getPlayerMove()
        self._print_message(self.board.drawBoard())
        outcome = self.board.isWinner()
        if outcome == 'win':
        #We will never get here BUT just in case
            self._print_message('Hooray! You have won the game!')
            return True
        elif outcome == 'draw':
            self._print_message('The game is a tie!')
            return True
        return False

    def _computer_move(self):
        """do the computer move"""
        brain = Brain.Brain(Board.Board(), self.board.computer_token)
        self.board.makeComputerMove(brain)

        outcome = self.board.isWinner()
        self._print_message(self.board.drawBoard())
        if outcome == 'win':
            self._print_message('The computer has beaten you! You lose.')
            return True
        elif outcome == 'draw':
            self._print_message('The game is a tie!')
            return True
        return False


    def play(self):
        """Here is where we play the game"""

        turn = self.board.firstMove()
        while True:
            if self.current_player == 'player':
                # Player's turn.
                game_over = self._player_move()
            else:
                # Computer's turn. Give it Tabla Rasa
                game_over = self._computer_move()
            if not self.board.playAgain() and game_over is True:
                return
            self._toggle_turn()




    def _print_message(self, arg):
        print arg
#
#while True:
#    self.board = Board.Board()
#    self.board.inputPlayerLetter()
#    turn = self.board.firstMove()
#    print 'The %s will go first.' % turn
#    if turn == 'player':
#        print self.board.drawBoard()
#
#    playing = True
#
#    while playing:
#        if turn == 'player':
#            # Player's turn.
#            self.board.getPlayerMove()
#
#            outcome = self.board.isWinner()
#            if outcome == 'win':
#                print self.board.drawBoard()
#                print('Hooray! You have won the game!')
#                playing = False
#                break
#            elif outcome == 'draw':
#
#                print self.board.drawBoard()
#                print('The game is a tie!')
#                playing = False
#                break
#            else:
#                turn = 'computer'
#
#        else:
#            # Computer's turn. Give it Tabla Rasa
#            brain = Brain.Brain(Board.Board(), self.board.computer_token)
#            self.board.makeComputerMove(brain)
#
#            outcome = self.board.isWinner()
#            if outcome == 'win':
#                print self.board.drawBoard()
#                print('The computer has beaten you! You lose.')
#                playing = False
#                break
#            elif outcome == 'draw':
#                print self.board.drawBoard()
#                print('The game is a tie!')
#                playing = False
#                break
#            else:
#                turn = 'player'
#
#    if not self.board.playAgain():
#        print "Ok, I'll go play a nice game of global thermonuclear war."
#        break
