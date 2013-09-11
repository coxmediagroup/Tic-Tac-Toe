#from Tkinter import Tk, BOTH
from Tkinter import *
from ttk import Frame, Button, Style

class TicTacToe:
    def __init__(self):
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    def play(self, player, x, y):
        self.board[x-1][y-1] = player;
    def getxy(self,x,y):
        return self.board[x-1][y-1]
    def win(self):
        result = ' '
        if ((self.board[0][0]==self.board[0][1]) and (self.board[0][0]==self.board[0][2])):
            return self.board[0][0]
        if ((self.board[1][0]==self.board[1][1]) and (self.board[1][0]==self.board[1][2])):
            return self.board[1][0]
        if ((self.board[2][0]==self.board[0][1]) and (self.board[0][0]==self.board[0][2])):
            return self.board[0][0]
        if ((self.board[0][0]==self.board[1][1]) and (self.board[0][0]==self.board[2][2])):
            return self.board[0][0]
        if ((self.board[0][2]==self.board[1][1]) and (self.board[2][0]==self.board[0][2])):
            return self.board[0][0]
        if ((self.board[0][1]==self.board[1][1]) and (self.board[0][1]==self.board[2][1])):
            return self.board[0][1]
        if ((self.board[0][2]==self.board[1][2]) and (self.board[0][2]==self.board[2][2])):
            return self.board[0][2]
        if ((self.board[0][0]==self.board[1][0]) and (self.board[0][0]==self.board[2][0])):
            return self.board[0][0]
        return result

    def printx(self):
        result = self.board[0][0]+self.board[0][1]+self.board[0][2]+"\n"
        result = result + self.board[1][0]+self.board[1][1]+self.board[1][2]+"\n"
        result = result + self.board[2][0]+self.board[2][1]+self.board[2][2]+"\n"
        return result
        
class Example(Frame):
    def __init__(self, parent):
        self.game = TicTacToe();
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    def NewX(self):
        print "New X\n"
    def NewO(self):
        print "New O\n"
    def Play(self,x,y):
        print 'Play x={0:1d} y={1:1d}\n'.format(x,y)
        self.Bboard[y][x].config(text="P")
    def initUI(self):
        newgamex = Button(self, text = "New game X", command=self.NewX)
        newgamex.place(x=0,y=0)
        newgamey = Button(self, text = "New game O", command=self.NewO)
        newgamey.place(x=80,y=0)
        self.game = TicTacToe()
        self.parent.title("Tic Tac Toe")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit",
            command=self.quit)
        quitButton.place(x=150, y=150)
        #fred = Button(self)
        #fred["text"] = "hello"
        #fred.place(x=0,y=0)
        #print fred
        self.Bboard = [[Button(self,command=lambda: self.Play(0,0),width=1,text=" "),
                        Button(self,command=lambda: self.Play(1,0),width=1,text=" "),
                        Button(self,command=lambda: self.Play(2,0),width=1,text=" ")],
                       [Button(self,command=lambda: self.Play(0,1),width=1,text=" "),
                        Button(self,command=lambda: self.Play(1,1),width=1,text=" "),
                        Button(self,command=lambda: self.Play(2,1),width=1,text=" ")],
                       [Button(self,command=lambda: self.Play(0,2),width=1,text=" "),
                        Button(self,command=lambda: self.Play(1,2),width=1,text=" "),
                        Button(self,command=lambda: self.Play(2,2),width=1,text=" ")]]
        x = 0
        for ox in self.Bboard:
            y=0
            for oy in ox:
                oy.place(y=30*x+50,x=30*y)
                y = y + 1
            x = x + 1


def main():
    game = TicTacToe()
    game.play('X',1,1);
    game.play('X',2,2);
    game.play('X',3,3);
    if game.win()!=' ':
        print game.win()+"Won the game"
    print game.printx();
    root = Tk()
    root.geometry("250x350+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 
