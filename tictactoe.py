#from Tkinter import Tk, BOTH
from Tkinter import *
from ttk import Frame, Button, Style

class TicTacToe:
    def __init__(self):
        self.start()
    def play(self, player, x, y):
        self.board[x][y] = player;
    def getxy(self,x,y):
        return self.board[x][y]
    def boardfull(self):
        for ox in self.board:
            for oy in ox:
                if oy==' ':
                    return False
        return True
    def start(self):
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    def win(self):
        result = ' '
        if ((self.board[0][0]!=' ') and (self.board[0][0]==self.board[0][1]) and (self.board[0][0]==self.board[0][2])):
            return self.board[0][0] + "A"
        if ((self.board[1][0]!=' ') and (self.board[1][0]==self.board[1][1]) and (self.board[1][0]==self.board[1][2])):
            return self.board[1][0] + "B"
        if ((self.board[2][0]!=' ') and (self.board[2][0]==self.board[2][1]) and (self.board[2][0]==self.board[2][2])):
            return self.board[2][0] + "C"
        if ((self.board[0][0]!=' ') and (self.board[0][0]==self.board[1][1]) and (self.board[0][0]==self.board[2][2])):
            return self.board[0][0] + "D"
        if ((self.board[0][2]!=' ') and (self.board[0][2]==self.board[1][1]) and (self.board[2][0]==self.board[0][2])):
            return self.board[0][2] + "E"
        if ((self.board[0][1]!=' ') and (self.board[0][1]==self.board[1][1]) and (self.board[0][1]==self.board[2][1])):
            return self.board[0][1] + "F"
        if ((self.board[0][2]!=' ') and (self.board[0][2]==self.board[1][2]) and (self.board[0][2]==self.board[2][2])):
            return self.board[0][2] + "G"
        if ((self.board[0][0]!=' ') and (self.board[0][0]==self.board[1][0]) and (self.board[0][0]==self.board[2][0])):
            return self.board[0][0] + "H"
        return result

    def printx(self):
        result = self.board[0][0]+self.board[0][1]+self.board[0][2]+"\n"
        result = result + self.board[1][0]+self.board[1][1]+self.board[1][2]+"\n"
        result = result + self.board[2][0]+self.board[2][1]+self.board[2][2]+"\n"
        return result
        
class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        self.game = TicTacToe();
        self.player = 'X'
        self.NewX()
    def NewX(self):
        self.player = 'X'
        self.game.start()
        for ox in self.Bboard:
            for oy in ox:
                oy.config(text=' ')
        print "New X\n"
        self.status["text"] = "X Pick a Square"
    def NewO(self):
        self.player = 'O'
        self.game.start()
        for ox in self.Bboard:
            for oy in ox:
                oy.config(text=' ')
        print "New O\n"
        self.status["text"] = "O Pick a Square"
    def Play(self,x,y):
        print 'Play x={0:1d} y={1:1d}\n'.format(x,y)
        self.game.play(self.player,y,x)
        self.Bboard[y][x].config(text=self.game.getxy(y,x))
        print self.game.printx()
        if self.game.win()!=' ':
            self.status["text"] = self.game.win()+" Won the game"
        elif self.game.boardfull():
            self.status["text"] = "Cats Game"
        elif self.player=='X':
            self.player='O'
            self.status["text"] = "O Pick a Square"
        else:
            self.player='X'
            self.status["text"] = "X Pick a Square"
    def initUI(self):
        self.status = Label(self, text = "Status")
        self.status.place(x=0,y=30)
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
        quitButton.place(x=160, y=0)
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
    game.play('X',0,0);
    game.play('X',2,2);
    game.play('X',1,1);
    if game.win()!=' ':
        print game.win()+"Won the game"
    print game.printx();
    root = Tk()
    root.geometry("250x350+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 
