#!/usr/bin/env python2

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
        self.tbtn_toggled(0, 0)
    def on_tbtn_01_toggled(self, widget, data=None):
        self.tbtn_toggled(0, 1)
    def on_tbtn_02_toggled(self, widget, data=None):
        self.tbtn_toggled(0, 2)
    def on_tbtn_10_toggled(self, widget, data=None):
        self.tbtn_toggled(1, 0)
    def on_tbtn_11_toggled(self, widget, data=None):
        self.tbtn_toggled(1, 1)
    def on_tbtn_12_toggled(self, widget, data=None):
        self.tbtn_toggled(1, 2)
    def on_tbtn_20_toggled(self, widget, data=None):
        self.tbtn_toggled(2, 0)
    def on_tbtn_21_toggled(self, widget, data=None):
        self.tbtn_toggled(2, 1)
    def on_tbtn_22_toggled(self, widget, data=None):
        self.tbtn_toggled(2, 2)

    def tbtn_toggled(self, x, y, player="X"):
        #This splits x and y for the gameboard alter.
        exec("""self.tbtn_%s%s.set_sensitive(False)""" % (x, y))
        exec("""self.tbtn_%s%s.set_label("%s")""" % (x, y, player))
        if player == "X":
            import ai
            (x, y) = ai.move()
            exec("""self.tbtn_toggled(%s, %s, player="O")""" % (x, y))

    def list_buttons(self):
        """
        Toggle buttons are labeled by coordinate.  Return a list of them.
        """
        buttons = []
        for x in range(0, 3):
            for y in range(0, 3):
                buttons.append("tbtn_%s%s" % (x, y))
        return buttons

    def __init__(self):
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

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def delete_event(self, widget, data=None):
        self.destroy(widget)

if __name__ == "__main__":
    gui = GUI()
    gtk.main()
