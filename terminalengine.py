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
                  "help": print_help}
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
    global game_running
    start_player = random.choice(("You", "The computer"))
    print("{} will go first.".format(start_player))
    player_turn = True if start_player == "You" else False
    strategy.self_flag = model.O if start_player == "You" else model.X
    strategy.player_flag = model.X if start_player == "You" else model.O
    while game_running:
        print("""[{0}][{1}][{2}]
[{3}][{4}][{5}]
[{6}][{7}][{8}]""".format(*current_board()))
        if player_turn:
            game_control()
            player_turn = not player_turn
        else:
            model.update_square(strategy.self_flag, strategy.pick_move())
            player_turn = not player_turn


def program_stop():
    global script_running
    script_running = False


def game_quit():
    global game_running
    game_running = False


def print_help():
    print("Current commands:\n"
          "start: Start new game.\n"
          "exit: Exit program.\n"
          "help: Print this help text.")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def current_board():
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
    global spaces
    commands = {"quit": game_quit}
    while True:
        command = raw_input(">")
        try:
            model.update_square(strategy.player_flag,spaces[int(command) - 1])
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