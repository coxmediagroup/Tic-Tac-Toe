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
    
    def move(self, square, btn):
        self.board.human_move(square)
        btn.text = self.square_label(square)
    
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