import sys
import curses
from curses_game_screen import GameScreen

def main(screen):

    # Make new Game
    s = GameScreen(screen)
    s.run_game()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        print "Thanks for playing!"