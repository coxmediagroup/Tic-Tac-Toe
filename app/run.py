"""
UI classes for running this app. Logic can be found in ttt.py.
"""
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from ttt import TicTacToeBoard 

HUMAN_NAME = "[color=c60f13]You[/color] "
COMPUTER_NAME = "[color=2ba6cb]Josh[/color] "


class OpeningFrame(BoxLayout):
    pass


class TicTacToeFrame(BoxLayout):
    """ Main container for other elements """
    board = TicTacToeBoard()
    
    def computer_move(self):
        square, game_over, winner = self.board.computer_move()
        self.set_square(square)
        return game_over, winner
    
    def get_me_outta_here(self):
        import pdb; pdb.set_trace()
    
    def player_move(self, square, btn):
        self.set_turn_label("")
        
        square, game_over, winner = self.board.human_move(square)
        self.set_square(square)
        
        if not game_over:
            game_over, winner = self.computer_move()

        if game_over:
            self.update_scores()
            self.set_new_game_button(hide=False)
    
    def player_text(self, player_number):
        if player_number == 1:
            name_text = HUMAN_NAME
        else:
            name_text = COMPUTER_NAME
        return name_text + self.board.player_stats(player_number)
    
    def reset_game(self, btn):
        self.set_new_game_button(hide=True)
        self.board.reset_board()
        self.update_squares()
        
        if self.board.is_computer_turn():
            self.computer_move()
            self.set_turn_label("[color=000000]Now your turn...[/color]")
        else:
            self.set_turn_label("[color=000000]You go first...[/color]")
    
    def set_new_game_button(self, hide):
        ph = self.board_wrapper.placeholder
        
        if hide:
            ph.remove_widget(self.new_game_btn)
            ph.add_widget(ph.placeholder_label)
            self.new_game_btn = None
        else:
            ph.remove_widget(ph.placeholder_label)
            if not getattr(self, 'new_game_btn', None):
                self.new_game_btn = Button(text='[color=000000]Start Another Game[/color]',
                                           background_normal="img/new-game-btn.png",
                                           on_press=self.reset_game,
                                           size_hint=(1, .15))
                ph.add_widget(self.new_game_btn)
    
    def set_square(self, square):
        if square is not None:
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
        for square in range(9):
            self.set_square(square)


class ExitFrame(BoxLayout):
    def exit_text(self):
        try:
            board = self.board
            if not (board.player_wins or board.player_losses or board.ties):
                return "Running away so soon?"
            return "A strange game. The only winning move is not to play."
        except AttributeError:
            # the tic-tac-toe screen hasn't passed control over yet
            return ""
    
    def player1_score(self):
        try:
            return "%s\n%s" % (HUMAN_NAME, self.board.player_wins)
        except AttributeError:
            # the tic-tac-toe screen hasn't passed control over yet
            return ""
    
    def player2_score(self):
        try:
            return "%s\n%s" % (COMPUTER_NAME, self.board.player_losses)
        except AttributeError:
            # the tic-tac-toe screen hasn't passed control over yet
            return ""
    
    def update_text(self):
        self.player1.text = self.player1_score()
        self.player2.text = self.player2_score()
        self.exit.text = self.exit_text()


class TicTacToeApp(App):
    """ Primary class for running the game """
    
    def build(self):
        # the three screens we'll use for this game
        self.root = BoxLayout()
        self.opening = OpeningFrame()
        self.tic_tac_toe = TicTacToeFrame()
        self.exit_screen = ExitFrame()
        
        self.root.add_widget(self.opening)
        return self.root
    
    def load_game(self):
        self.root.remove_widget(self.opening)
        self.root.add_widget(self.tic_tac_toe)
        
    def quit_game(self):
        # we'll hand the logic object over to the exit screen
        self.exit_screen.board = self.tic_tac_toe.board
        self.exit_screen.update_text()
        
        self.root.remove_widget(self.tic_tac_toe)
        self.root.add_widget(self.exit_screen)


if __name__ == '__main__':
    TicTacToeApp().run()