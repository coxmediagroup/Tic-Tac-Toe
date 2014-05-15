__author__ = 'marc'
__author__ = 'marc'

from board.views import BoardView

from player.models import Player, AIPlayer

from board.models import PositionAlreadyTakenError
from  game.lib import check_for_win
import sys
class GameView():
    board_view = BoardView()

    def play_game(self):
        """The main game loop/logic"""

        playing = True
        while playing:
            print self.board_view.draw()

            if None not in self.board_view.board.tttboard:
                print 'No more moves left.'
                break

            aichoice = self.board_view.game.deep_blue.take_turn(self.board_view.board,
                                                                self.board_view.game.opponent)
            self.board_view.board.select_position(aichoice, self.board_view.game.deep_blue)

            print self.board_view.draw()
            if check_for_win(self.board_view.board, self.board_view.game.deep_blue):
                print "Computer Wins!"
                break

            if None not in self.board_view.board.tttboard:
                print 'No more moves left.'
                break

            # player selection
            while True:
                selection = raw_input('Pick a spot: ')
                if selection.lower() == 'q':
                    playing = False
                    break

                try:
                    self.board_view.board.select_position(int(selection), self.board_view.game.opponent)
                except PositionAlreadyTakenError:
                    print 'That position is already taken.'
                else:
                    if check_for_win(self.board_view.board, self.board_view.game.opponent):
                        # Well, this isn't supposed to happen.
                        print "You Win!"
                        playing = False
                    break
