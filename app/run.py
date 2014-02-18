"""
UI classes for running this app. Logic can be found in ttt.py.
"""
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from ttt import TicTacToeBoard


class TicTacToeFrame(FloatLayout):
    """ Main container for other elements """
    board = TicTacToeBoard()
    
    def player_text(self, player_number):
        return self.board.player_stats(player_number)
    pass


class TicTacToeApp(App):
    """ Primary class for running the game """
    
    def build(self):
        frame = TicTacToeFrame(size=(300, 300))
        return frame


if __name__ == '__main__':
    TicTacToeApp().run()