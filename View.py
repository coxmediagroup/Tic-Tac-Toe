'''
Created on Oct 16, 2012

@author: Josh
'''
from Tkinter import *
from Game import Game

class View(Frame):
    def __init__(self, root, game):
        Frame.__init__(self, root)
        
        self.game = game
        self.create_buttons()
        
        
        self.pack()
        
    def create_buttons(self):
        self.buttons = []
        for x in xrange(3):
            self.buttons.append([])
            for y in xrange(3):
                button = Button(self, width = 16, height = 10)
                button.config(text = self.toNoughts(self.game.get(x, y)))
                button.config(command = self.make_a_choice(x, y))
                button.grid(column = x, row = y)
                
                self.buttons[x].append(button)
                
    def toNoughts(self, i):
        if i == 0: return " "
        elif i == 1: return "O"
        elif i == 2: return "X"
                        
    def make_a_choice(self, column, row):
        def command():
            if self.game.get(column, row) == 0:
                self.game.make_choice(column, row, 1)
                
                over, winner = self.game.game_over()
                
                if not over: self.game.make_ai_choice(2)
            
            over, winner = self.game.game_over()
            for x in xrange(3):
                for y in xrange(3):
                    self.buttons[x][y].config(text = self.toNoughts(self.game.get(x, y)))
                    if over: 
                        self.buttons[x][y].config(state = DISABLED)
        return command
        
if __name__ == '__main__':
    root = Tk()
    View(root, Game())
    root.mainloop()