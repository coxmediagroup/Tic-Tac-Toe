"""
UI classes for running this app. Logic can be found in ttt.py.
"""
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from ttt import TicTacToeBoard


class TicTacToeFrame(BoxLayout):
    """ Main container for other elements """
    board = TicTacToeBoard()
    
    def player_move(self, square, btn, btn_parent):
        move, game_over, winner = self.board.human_move(square)
        btn.text = self.square_label(square)
        
        if not game_over:
            square, game_over, winner = self.board.computer_move()
            getattr(btn_parent, "square%s" % square).text = self.square_label(square)

        if game_over:
            pass
    
    def player_text(self, player_number):
        return self.board.player_stats(player_number)
    
    def square_label(self, square):
        return self.board.get_square_label(square)


class TicTacToeApp(App):
    """ Primary class for running the game """
    
    def build(self):
        frame = TicTacToeFrame()
        return frame


if __name__ == '__main__':
    TicTacToeApp().run()