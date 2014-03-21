import model
import os
import random
import strategy


script_running = True
game_running = True
spaces = [model.BOT_LEFT, model.BOT_MID, model.BOT_RIGHT,
          model.MID_LEFT, model.CENTER, model.MID_RIGHT,
          model.TOP_LEFT, model.TOP_MID, model.TOP_RIGHT]


def main_loop():
    """No return. Outer loop to allow program to continue running."""
    global script_running
    controller = {"start": game_loop, "exit": program_stop,
                  "help": print_help, "quit": program_stop}
    print("This is Tic-Tac-Toe.\n"
          "Type start to begin\n"
          "Use your number pad to select squares.\n"
          "Type help for other commands.")
    while script_running:
        command = raw_input(">")
        try:
            controller[command]()
        except KeyError:
            print("Command not recognized.")


def game_loop():
    """No return. Primary game loop."""
    global game_running
    game_running = True
    model.clear_board()
    start_player = random.choice(("You", "The computer"))
    print("{} will go first.".format(start_player))
    player_turn = True if start_player == "You" else False
    strategy.computer_flag = model.O if start_player == "You" else model.X
    strategy.player_flag = model.X if start_player == "You" else model.O
    while game_running:
        print("""[{0}][{1}][{2}]
[{3}][{4}][{5}]
[{6}][{7}][{8}]""".format(*current_board()))
        if " " not in current_board():
            print("Draw game.")
            break
        if player_turn:
            game_control()
            if model.did_player_win(strategy.player_flag):
                print("You won.")
                game_quit()
            else:
                player_turn = not player_turn
        else:
            model.update_square(strategy.computer_flag, strategy.pick_move())
            if model.did_player_win(strategy.computer_flag):
                print("The computer won.")
                game_quit()
            else:
                player_turn = not player_turn
        clear()


def program_stop():
    """Breaks main_loop. Allows program to exit."""
    global script_running
    script_running = False


def game_quit():
    """Breaks game_loop."""
    global game_running
    game_running = False


def print_help():
    """Output help text to standard output."""
    print("Current commands:\n"
          "start: Start new game.\n"
          "exit: Exit program.\n"
          "quit: Exit program.\n"
          "help: Print this help text.")


def clear():
    """Clears standard output."""
    os.system('cls' if os.name == 'nt' else 'clear')


def current_board():
    """Return list representing the current board as strings."""
    board = []
    for row in model.board:
        for space in row:
            if space == model.X:
                board.append("X")
            elif space == model.O:
                board.append("O")
            else:
                board.append(" ")
    return board


def game_control():
    """No return. Simple loop to accept user input and validate it."""
    global spaces
    commands = {"quit": game_quit, "exit": game_quit}
    while True:
        command = raw_input(">")
        try:
            model.update_square(strategy.player_flag, spaces[int(command) - 1])
            return
        except ValueError:
            try:
                commands[command]()
                return
            except IndexError:
                print("Unrecognized command. Try again.")
        except IndexError:
            print("Value out of range. Please use the number pad.")


if __name__ == '__main__':
    main_loop()