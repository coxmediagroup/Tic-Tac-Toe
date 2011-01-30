"""
User interface for Tic-Tac-Toe game.
"""

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

class GUI:
    # Seems gross to have 9 identical functions, but exec() doesn't
    # love me anymore.
    def on_tbtn_00_toggled(self, widget, data=None):
        self.tbtn_toggled(0, 0, player="human")
    def on_tbtn_01_toggled(self, widget, data=None):
        self.tbtn_toggled(0, 1, player="human")
    def on_tbtn_02_toggled(self, widget, data=None):
        self.tbtn_toggled(0, 2, player="human")
    def on_tbtn_10_toggled(self, widget, data=None):
        self.tbtn_toggled(1, 0, player="human")
    def on_tbtn_11_toggled(self, widget, data=None):
        self.tbtn_toggled(1, 1, player="human")
    def on_tbtn_12_toggled(self, widget, data=None):
        self.tbtn_toggled(1, 2, player="human")
    def on_tbtn_20_toggled(self, widget, data=None):
        self.tbtn_toggled(2, 0, player="human")
    def on_tbtn_21_toggled(self, widget, data=None):
        self.tbtn_toggled(2, 1, player="human")
    def on_tbtn_22_toggled(self, widget, data=None):
        self.tbtn_toggled(2, 2, player="human")

    def tbtn_toggled(self, x, y, player=None):
        """
        Player has toggled one of the buttons.

        """
        if not player or not self.game.turn:
            return

        if self.game.winner:
            return
        self.game.move(player, x, y)
        

    def on_menu_new_activate(self, widget, data=None):
        print("MENU")
        self.game.initialize()

    def list_buttons(self):
        """
        Toggle buttons are labeled by coordinate.  Return a list of them.

        """
        buttons = []
        for x in range(0, 3):
            for y in range(0, 3):
                buttons.append("tbtn_%s%s" % (x, y))
        return buttons

    def update_board(self, *args):
        """
        Update the GUI game board to match the game module's board.

        *args: unused, must be present for game module's update.

        """
        print("update_board")
        board = self.game.get_board()
        for row in range(0, 3):
            for col in range(0, 3):
                if board[row][col] == " ":
                    self.unset("self.tbtn_%s%s" % (row, col))
                else:
                    self.set("self.tbtn_%s%s" % (row, col), board[row][col])
    
    def set(self, string, what):
        """
        Deactivate, press, and set button label.

        string: input string containing widget name.
        what: what do we set the label to?

        """
        exec(string + """.set_active(True)""")
        exec(string + """.set_sensitive(False)""")
        exec(string + """.set_label("%s")""" % what)

    def unset(self, string):
        """
        Activate, depress, and clear button label.

        string: input string containing widget name.

        """
        exec(string + """.set_active(False)""")
        exec(string + """.set_sensitive(True)""")
        exec(string + """.set_label("")""")

    def __init__(self, game):
        self.glade = "tictactoe.glade"
        self.win_main = gtk.glade.XML(self.glade, "win_main")
        self.win_main.signal_autoconnect(self)

        widgets = []
        widgets += self.list_buttons()

        # give us a reference to glade widgets
        for e in widgets:
            widget = e.replace('"', '')
            string = "self.%s =\
                    self.win_main.get_widget(%s)" % (widget, '"'+widget+'"')
            exec(string)

        self.game = game
        game.register_main_loop(gtk.main)
        game.register_update(self.update_board, self)

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def delete_event(self, widget, data=None):
        self.destroy(widget)
