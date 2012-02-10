from Tkinter import *
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
    print number

if __name__ == '__main__':
    app = App(root)
    root.title("Tic-Tac-Toe")
    root.mainloop()
