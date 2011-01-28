#!/usr/bin/env python2

"""
User interface for Tic-Tac-Toe game.
"""

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

class GUI:
    def __init__(self):
        self.glade = "tictactoe.glade"
        self.win_main = gtk.glade.XML(self.glade, "win_main")
        self.win_main.signal_autoconnect(self)

        widgets = []

        # toggle buttons labeled by coordinate
        for x in range(0, 3):
            for y in range(0, 3):
                widgets.append("tbtn_%s%s" % (x, y))

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
