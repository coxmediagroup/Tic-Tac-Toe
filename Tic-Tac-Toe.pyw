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
        if checkPopulate('XXX'):
            tkMessageBox.showinfo('Tic-Tac-Toe', 'You Win!')
    else:
        tkMessageBox.showerror('Error','Space is already taken')

def checkPopulate(value):
    for i in range(3):
        # check rows
        if app.bb[i*3].text.get() + app.bb[1+i*3].text.get() + app.bb[2+i*3].text.get() == value:
            return 1
        # check columns
        if app.bb[i].text.get() + app.bb[3+i].text.get() + app.bb[6+i].text.get() == value:
            return 1
    # check first diagonal
    if app.bb[0].text.get() + app.bb[4].text.get() + app.bb[8].text.get() == value:
        return 1
    # check second diagonal
    if app.bb[2].text.get() + app.bb[4].text.get() + app.bb[6].text.get() == value:
        return 1

if __name__ == '__main__':
    app = App(root)
    root.title("Tic-Tac-Toe")
    root.mainloop()
