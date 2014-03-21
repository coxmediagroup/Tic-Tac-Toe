'''
@author: Corey Hutton
'''
import Tkinter

from tictactoe import TicTacToe

def main():
    root = Tkinter.Tk()

    game = TicTacToe(master=root)

    root.mainloop()

if __name__ == '__main__':
    main()
