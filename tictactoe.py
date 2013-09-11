"""tictactoe.py: A one player tic tac toe game with the computer.  The computer never loses."""

__author__      = "Art McGee"
__copyright__   = "Copyright 2013, USA"

from Tkinter import *
from ttk import Frame, Button, Style

class TicTacToeComputer:
    def __init__(self):
        self.x=0
        self.y=0

    def location(self, x, y):
        self.x = x
        self.y = y
        print 'location x={0:1d} y={1:1d}\n'.format(self.x,self.y)

    def play(self,game,player):
        if player=='X':
            aponent = 'O'
        else:
            aponent = 'X'
        x = 0
        while x<3:
            y = 0
            while y <3:
                if game.getxy(x,y)==' ':
                    if game.check(player,x,y)==player:
                        self.location(x,y)
                        return
                    elif game.check(aponent,x,y)==aponent:
                        self.location(x,y)
                        return
                y = y + 1
            x = x + 1
        if game.board[1][1]==' ':
            self.location(1,1)
        elif game.board[0][0]==' ':
            self.location(0,0)
        elif game.board[2][2]==' ':
            self.location(2,2)
        elif game.board[0][2]==' ':
            self.location(0,2)
        elif game.board[2][0]==' ':
            self.location(2,0)
        elif game.board[0][1]==' ':
            self.location(0,1)
        elif game.board[1][0]==' ':
            self.location(1,0)
        elif game.board[2][1]==' ':
            self.location(2,1)
        elif game.board[1][2]==' ':
            self.location(1,2)
        
class TicTacToe:
    def __init__(self):
        self.start()

    def play(self, player, x, y):
        if self.board[x][y]==' ':
            self.board[x][y] = player;
        else:
            print "Play Error Space Taken {0:s} {1:d} {2:d}".format(player,x,y)
        
    def check(self, player, x, y):
        before = self.board[x][y]
        self.board[x][y] = player;
        result = self.win()
        self.board[x][y] = before;
        if result==player:
            print 'check:player {0:s} at {1:d} {2:d}\n'.format(player,x,y)
        return result;

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
            return self.board[0][0]
        if ((self.board[1][0]!=' ') and (self.board[1][0]==self.board[1][1]) and (self.board[1][0]==self.board[1][2])):
            return self.board[1][0]
        if ((self.board[2][0]!=' ') and (self.board[2][0]==self.board[2][1]) and (self.board[2][0]==self.board[2][2])):
            return self.board[2][0]
        if ((self.board[0][0]!=' ') and (self.board[0][0]==self.board[1][1]) and (self.board[0][0]==self.board[2][2])):
            return self.board[0][0]
        if ((self.board[0][2]!=' ') and (self.board[0][2]==self.board[1][1]) and (self.board[2][0]==self.board[0][2])):
            return self.board[0][2]
        if ((self.board[0][1]!=' ') and (self.board[0][1]==self.board[1][1]) and (self.board[0][1]==self.board[2][1])):
            return self.board[0][1]
        if ((self.board[0][2]!=' ') and (self.board[0][2]==self.board[1][2]) and (self.board[0][2]==self.board[2][2])):
            return self.board[0][2]
        if ((self.board[0][0]!=' ') and (self.board[0][0]==self.board[1][0]) and (self.board[0][0]==self.board[2][0])):
            return self.board[0][0]
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
        self.computer = TicTacToeComputer()
        self.player = 'X'
        self.NewX()

    def NewX(self):
        self.player = 'X'
        self.game.start()
        print self.game.printx()
        for ox in self.Bboard:
            for oy in ox:
                oy.config(text=' ')
        print "New X\n"
        self.status["text"] = "X Pick a Square"

    def NewO(self):
        self.player = 'O'
        self.game.start()
        print self.game.printx()
        for ox in self.Bboard:
            for oy in ox:
                oy.config(text=' ')
        print "New O\n"
        self.status["text"] = "O Pick a Square"
        self.computer.play(self.game,'X')
        print 'Computer X Plays x={0:1d} y={1:1d}\n'.format(self.computer.x,self.computer.y)
        self.game.play('X',self.computer.y,self.computer.x)
        self.Bboard[self.computer.y][self.computer.x].config(text=self.game.getxy(self.computer.y,self.computer.x))
        print self.game.printx()

    def Play(self,x,y):
        print 'Play {2:s} x={0:1d} y={1:1d}\n'.format(x,y,self.player)
        self.game.play(self.player,x,y)
        self.Bboard[x][y].config(text=self.game.getxy(x,y))
        print self.game.printx()
        if self.game.win()!=' ':
            self.status["text"] = self.game.win()+" Won the game"
        elif self.game.boardfull():
            self.status["text"] = "Cats Game"
        elif self.player=='X':
            self.computer.play(self.game,'O')
            print 'Computer O Plays x={0:1d} y={1:1d}\n'.format(self.computer.x,self.computer.y)
            self.game.play('O',self.computer.x,self.computer.y)
            self.Bboard[self.computer.x][self.computer.y].config(text=self.game.getxy(self.computer.x,self.computer.y))
            print self.game.printx()
        else:
            self.computer.play(self.game,'X')
            print 'Computer X Plays x={0:1d} y={1:1d}\n'.format(self.computer.x,self.computer.y)
            self.game.play('X',self.computer.x,self.computer.y)
            self.Bboard[self.computer.x][self.computer.y].config(text=self.game.getxy(self.computer.x,self.computer.y))
            print self.game.printx()
        if self.game.win()!=' ':
            self.status["text"] = self.game.win()+" Won the game"
        elif self.game.boardfull():
            self.status["text"] = "Cats Game"

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
                        Button(self,command=lambda: self.Play(0,1),width=1,text=" "),
                        Button(self,command=lambda: self.Play(0,2),width=1,text=" ")],
                       [Button(self,command=lambda: self.Play(1,0),width=1,text=" "),
                        Button(self,command=lambda: self.Play(1,1),width=1,text=" "),
                        Button(self,command=lambda: self.Play(1,2),width=1,text=" ")],
                       [Button(self,command=lambda: self.Play(2,0),width=1,text=" "),
                        Button(self,command=lambda: self.Play(2,1),width=1,text=" "),
                        Button(self,command=lambda: self.Play(2,2),width=1,text=" ")]]
        x = 0
        while x<3:
            y = 0
            while y<3:
                self.Bboard[x][y].place(y=30*y+50,x=30*x)
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
