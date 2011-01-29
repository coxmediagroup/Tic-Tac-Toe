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

    #FIXME: This function is getting kludgey.  Move moves to game.py
    #FIXME: and make an update function that updates using data from there.
    def tbtn_toggled(self, x, y, player=None):
        if not player:
            return

        if self.game.winner:
            return
        self.game.move(player, x, y)
        
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
        print("update board")
        board = self.game.get_board()
        print(board)
        for row in range(0, 3):
            for col in range(0, 3):
                print("update_board: %s" % board[row][col])
                if board[row][col] == " ":
                    self.unset("self.tbtn_%s%s" % (row, col))
                else:
                    self.set("self.tbtn_%s%s" % (row, col), board[row][col])
    
    def set(self, string, what):
        exec(string + """.set_active(True)""")
        exec(string + """.set_sensitive(False)""")
        exec(string + """.set_label("%s")""" % what)

    def unset(self, string):
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
