from Tkinter import *
import tkMessageBox
import tkFont

root = Tk()
buttonFont = tkFont.Font(family='Arial', size=50, weight='bold')
labelFont  = tkFont.Font(family="Arial", size=14)
countFont  = tkFont.Font(family="Arial", size=16, weight='bold')

win = IntVar()
lose= IntVar()
tie = IntVar()

class App():
    def __init__(self, master):
        self.bb = range(9)
        for i in range(9):
            self.bb[i] = Square(i)
        self.score = Score(3)

class Score():
    def __init__(self, row):
        win.set(0)
        lose.set(0)
        tie.set(0)
        
        self.winLbl  = Label(text="Wins", font=labelFont).grid(row=row,column=0)
        self.loseLbl = Label(text="Losses", font=labelFont).grid(row=row,column=1)
        self.tieLbl  = Label(text="Ties", font=labelFont).grid(row=row,column=2)

        self.winCnt  = Label(textvariable=win, font=countFont).grid(row=row+1,column=0)
        self.loseCnt = Label(textvariable=lose, font=countFont).grid(row=row+1,column=1)
        self.tieCnt  = Label(textvariable=tie, font=countFont).grid(row=row+1,column=2)     

class Square():
    def __init__(self, i, master=None):
        self.number = i
        self.text = StringVar()
        self.text.set("")

        self.btn = Button(master, textvariable=self.text, command=lambda:btn_click(self.number), bg='white', width=3, font=buttonFont).grid(row=i/3,column=i%3)

def btn_click(number):
    if app.bb[number].text.get() == "":
        app.bb[number].text.set('X')
        if checkPopulate('XXX') == 'Win':
            win.set(win.get()+1)
            end_game('You Win!')
        else:
            ai_play()
    else:
        tkMessageBox.showerror('Error','Space is already taken')

def checkPopulate(value):
    #check for any empty cell when value = ''
    if value == '':
        for i in range(9):
            if app.bb[i].text.get() == value:
                return i

    for i in range(3):
        # check rows
        if app.bb[i*3].text.get() + app.bb[1+i*3].text.get() + app.bb[2+i*3].text.get() == value:
            if   app.bb[i*3].text.get()   == '': return i*3
            elif app.bb[2+i*3].text.get() == '': return 2+i*3
            elif app.bb[1+i*3].text.get() == '': return 1+i*3
            else: return 'Win'
        # check columns
        if app.bb[i].text.get() + app.bb[3+i].text.get() + app.bb[6+i].text.get() == value:
            if   app.bb[i].text.get()   == '': return i
            elif app.bb[6+i].text.get() == '': return 6+i
            elif app.bb[3+i].text.get() == '': return 3+i
            else: return 'Win'
    # check first diagonal
    if app.bb[0].text.get() + app.bb[4].text.get() + app.bb[8].text.get() == value:
        if   app.bb[0].text.get() == '': return 0
        elif app.bb[8].text.get() == '': return 8
        elif app.bb[4].text.get() == '': return 4
        else: return 'Win'
    # check second diagonal
    if app.bb[2].text.get() + app.bb[4].text.get() + app.bb[6].text.get() == value:
        if   app.bb[2].text.get() == '': return 2
        elif app.bb[6].text.get() == '': return 6
        elif app.bb[4].text.get() == '': return 4
        else: return 'Win'

def ai_play():
    # win game
    if checkPopulate('OO') != None:
        app.bb[checkPopulate('OO')].text.set('O')
        lose.set(lose.get()+1)
        end_game('You Lose!')
    # block player from winning
    elif checkPopulate('XX') != None:
        app.bb[checkPopulate('XX')].text.set('O')
    # take middle square if available
    elif app.bb[4].text.get() == '':
        app.bb[4].text.set('O')
    # check if AI can setup win on next move
    elif checkPopulate('O') != None:
        app.bb[checkPopulate('O')].text.set('O')
    # take any open space
    elif checkPopulate('') != None:
        app.bb[checkPopulate('')].text.set('O')

    # check if board is full
    if checkPopulate('') == None:
        tie.set(tie.get()+1)
        end_game('Tie Game!')

def end_game(message):
    if tkMessageBox.askyesno('Tic-Tac-Toe', message+'\nDo you want to play again?'):
        playAgain()
    else:
        root.destroy()
        root.quit()

def playAgain():
    for i in range(9):
        app.bb[i].text.set('')
    goFirst()

def goFirst():
    if tkMessageBox.askyesno('Tic-Tac-Toe', 'Do you want to go first?') == False:
        ai_play()

if __name__ == '__main__':
    app = App(root)
    root.title("Tic-Tac-Toe")
    goFirst()
    root.mainloop()
