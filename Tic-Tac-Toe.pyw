from Tkinter import *
import tkMessageBox
import tkFont

root = Tk()
buttonFont = tkFont.Font(family='Arial', size=50, weight='bold')

class App():
    def __init__(self, master):
        self.bb = range(9)
        for i in range(9):
            self.bb[i] = Square(i)

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
            end_game('You Win!')
    else:
        tkMessageBox.showerror('Error','Space is already taken')

def checkPopulate(value):
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

def end_game(message):
    tkMessageBox.showinfo('Tic-Tac-Toe', message)

if __name__ == '__main__':
    app = App(root)
    root.title("Tic-Tac-Toe")
    root.mainloop()
