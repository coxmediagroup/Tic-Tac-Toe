#!/usr/bin/env python
import wx

import tictactoe


class TicTacToeFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Tic-Tac-Toe', size=(400, 400))

        self.board = tictactoe.Board()
        self.human = tictactoe.PLAYER_X
        self.computer = tictactoe.AIPlayer(tictactoe.PLAYER_O)

        self.turn = tictactoe.PLAYER_X
        self.turn_messages = {
                tictactoe.PLAYER_X: "Your turn",
                tictactoe.PLAYER_O: "Computer's turn",
            }

        self.turn_label = wx.StaticText(self, label=self.turn_messages[self.turn])

        gridbag = wx.GridBagSizer(5, 5)
        gridbag.Add(self.turn_label, (0, 0), (1, 3), wx.ALIGN_CENTER_HORIZONTAL)

        self.button_map = {}

        for column in range(self.board.size):
            for row in range(self.board.size):
                button = wx.Button(self, id=wx.NewId(), label='?')
                self.button_map[button.GetId()] = ((column, row), button)

                gridbag.Add(button, (row+1, column), (1, 1), wx.EXPAND)


        gridbag.AddGrowableCol(0)
        gridbag.AddGrowableCol(1)
        gridbag.AddGrowableCol(2)

        gridbag.AddGrowableRow(1)
        gridbag.AddGrowableRow(2)
        gridbag.AddGrowableRow(3)

        self.SetSizerAndFit(gridbag)
        self.Bind(wx.EVT_BUTTON, self.on_button_press)

    def _replace_button_with_label(self, pos, label_text):
        gbpos = (pos[1]+1, pos[0])

        button = self.GetSizer().FindItemAtPosition(gbpos).GetWindow()
        button.Hide()

        self.GetSizer().Detach(button)
        self.GetSizer().Add(wx.StaticText(self, label=label_text), gbpos, (1, 1), wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL)
        self.Layout()

    def _new_game(self):
        for pos, button in self.button_map.itervalues():
            gbpos = (pos[1]+1, pos[0])

            label = self.GetSizer().FindItemAtPosition(gbpos).GetWindow()
            self.GetSizer().Detach(label)

            if label.GetClassName() == 'wxStaticText':
                label.Destroy()

            button.Show()

            self.GetSizer().Add(button, gbpos, (1, 1), wx.EXPAND)

        self.board = tictactoe.Board()
        self.turn = self.human
        self.Layout()

    def on_button_press(self, evt):
        # Not your turn, cheater
        if self.turn != self.human:
            return

        position, button = self.button_map[evt.GetId()]
        print 'Position: %s' % (position,)

        try:
            self.board.add_move(position, self.human)
        except tictactoe.MoveNotAvailable:
            wx.MessageBox("That is not a legal move", "Error", wx.OK, self)
        except IndexError:
            wx.MessageBox("That is not a legal move", "Error", wx.OK, self)

        self._replace_button_with_label(position, "X")

        if self.board.get_winner():
            result = wx.MessageBox("You win.\nNew game?", "New Game?", wx.YES|wx.NO)

            if result == wx.YES:
                self._new_game()

            return

        if len(self.board.get_available_moves()) == 0:
            result = wx.MessageBox("Draw.\nNew game?", "New Game?", wx.YES|wx.NO)

            if result == wx.YES:
                self._new_game()

            return

        self.turn = self.computer.player
        self.turn_label.SetLabel(self.turn_messages[self.turn])

        computers_move = self.computer.get_next_move(self.board)
        print 'Computers move = %s' % (computers_move,)
        self._replace_button_with_label(computers_move, "O")

        self.board.add_move(computers_move, self.computer.player)

        if self.board.get_winner():
            result = wx.MessageBox("Computer wins.\nNew game?", "New Game?", wx.YES|wx.NO)

            if result == wx.YES:
                self._new_game()

            return

        self.turn = self.human
        self.turn_label.SetLabel(self.turn_messages[self.turn])


if __name__ == '__main__':
    app = wx.App(redirect=False, useBestVisual=True)
    frame = TicTacToeFrame()
    frame.Show()
    app.MainLoop()
