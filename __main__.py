"""
The main game play

"""
import sys
import curses
from tic_tac_toe.curses_game_screen import GameScreen

def main(screen):
    """main"""
    # Make new Game
    _game = GameScreen(screen)
    _game.run_game()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        print "Thanks for playing!"
