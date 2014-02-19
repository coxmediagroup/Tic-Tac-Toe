"""
UI classes for running this app. Logic can be found in ttt.py.
"""
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from ttt import TicTacToeBoard 


class TicTacToeFrame(BoxLayout):
    """ Main container for other elements """
    board = TicTacToeBoard()
    
    def computer_move(self):
        square, game_over, winner = self.board.computer_move()
        self.set_square(square)
        return game_over, winner
    
    def player_move(self, square, btn):
        self.set_turn_label("")
        
        square, game_over, winner = self.board.human_move(square)
        btn.text = self.square_label(square)
        
        if not game_over:
            game_over, winner = self.computer_move()

        if game_over:
            self.update_scores()
            self.set_next_game_button(hide=False)
    
    def player_text(self, player_number):
        if player_number == 1:
            name_text = "[color=c60f13]You[/color] "
        else:
            name_text = "[color=2ba6cb]Hal[/color] " 
        return name_text + self.board.player_stats(player_number)
    
    def reset_game(self, btn):
        self.set_next_game_button(hide=True)
        self.board.reset_board()
        self.update_squares()
        
        if self.board.is_computer_turn():
            self.computer_move()
            self.set_turn_label("Your turn...")
        else:
            self.set_turn_label("You go first...")
    
    def set_next_game_button(self, hide=False):
        ph = self.board_wrapper.placeholder
        
        if hide:
            ph.remove_widget(self.new_game_btn)
            ph.add_widget(ph.placeholder_label)
        else:
            ph.remove_widget(ph.placeholder_label)
            self.new_game_btn = Button(text='[color=000000]Start Another Game[/color]',
                                       background_normal="img/new-game-btn.png",
                                       on_press=self.reset_game,
                                       size_hint=(1, .15))
            ph.add_widget(self.new_game_btn)
    
    def set_square(self, square):
        btn_grid = self.board_wrapper.game_board.game_board_buttons
        getattr(btn_grid, "square%s" % square).text = self.square_label(square)
    
    def set_turn_label(self, text):
        self.board_wrapper.board_text.go_first_label.text = text
    
    def square_label(self, square):
        return self.board.get_square_label(square)
    
    def update_scores(self):
        self.player1_score.text = self.player_text(1)
        self.player2_score.text = self.player_text(2)
        
    def update_squares(self):
        for square in range(8):
            self.set_square(square)


class TicTacToeApp(App):
    """ Primary class for running the game """
    
    def build(self):
        frame = TicTacToeFrame()
        return frame


if __name__ == '__main__':
    TicTacToeApp().run()