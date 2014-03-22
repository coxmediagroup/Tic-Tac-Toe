'''
@author: Corey Hutton
'''
from Tkinter import Tk

from tictactoe import TicTacToe

def main():
    root = Tk()
    root.wm_title("Tic-Tac-Toe")

    game = TicTacToe(master=root)

    root.mainloop()

if __name__ == '__main__':
    main()
