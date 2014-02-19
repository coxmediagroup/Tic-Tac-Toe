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
    
    def computer_move(self):
        square, game_over, winner = self.board.computer_move()
        getattr(self.get_btn_parent(), "square%s" % square).text = self.square_label(square)
        return game_over, winner
    
    def get_btn_parent(self):
        return self.wrapper.board_wrapper.game_board.game_board_buttons
    
    def player_move(self, square, btn):
        self.wrapper.board_wrapper.board_text.go_first_label.text = ""
        move, game_over, winner = self.board.human_move(square)
        btn.text = self.square_label(square)
        
        if not game_over:
            game_over, winner = self.computer_move()

        if game_over:
            self.update_scores()
    
    def update_scores(self):
        self.wrapper.player1_score.text = self.player_text(1)
        self.wrapper.player2_score.text = self.player_text(2)
    
    def player_text(self, player_number):
        if player_number == 1:
            name_text = "[color=c60f13]You[/color] "
        else:
            name_text = "[color=2ba6cb]Hal[/color] " 
        return name_text + self.board.player_stats(player_number)
    
    def reset_game(self):
        self.board.reset_board()
        if self.board.is_computer_turn():
            self.computer_move()
        else:
            self.wrapper.board_wrapper.board_text.go_first_label.text = "You go first..."
    
    def square_label(self, square):
        return self.board.get_square_label(square)


class TicTacToeApp(App):
    """ Primary class for running the game """
    
    def build(self):
        frame = TicTacToeFrame()
        return frame


if __name__ == '__main__':
    TicTacToeApp().run()