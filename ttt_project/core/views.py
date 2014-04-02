import random
from django.http import HttpResponse
from annoying.decorators import render_to
from core.models import Game, Move

@render_to('core/core.html')
def main(request):
    new_game = Game.objects.create()
    return {'game_num': new_game.id}


@render_to('core/board.html')
def player_move(request, game_id, space_id):
    current_game = Game.objects.get(id=game_id)
    new_player_move = Move.objects.create(game=current_game, space=space_id)

    calculate_computer_move(request, current_game)

    # Gather all moves to re-populate board
    all_moves = Move.objects.filter(game=current_game)
    vals = {}
    for move in all_moves:
        vals["space%s" % move.space] = move.player_move

    if all_moves.count() == 9:
        vals["end_game"] = True

    return vals


def calculate_computer_move(request, current_game):
    all_spaces = [1,2,3,4,5,6,7,8,9]
    space_for_computer_move = None

    # get all moves for this game
    moves_for_current_game = Move.objects.filter(game=current_game)

    # If it's the first move of the game, just pick a random space
    if moves_for_current_game.count() == 1:
        player_space = moves_for_current_game[0].space
        all_spaces.remove(player_space)

        if player_space != 5:
            space_for_computer_move = 5
        else:
            all_spaces.remove(2)
            all_spaces.remove(4)
            all_spaces.remove(6)
            all_spaces.remove(8)

            # pick one of the remaining spaces
            space_for_computer_move = random.choice(all_spaces)

    elif moves_for_current_game.count() == 9:
        return

    else:
        player_moves = []
        for move in moves_for_current_game:
            if move.player_move:
                player_moves.append(move.space)
                all_spaces.remove(move.space)
            else:
                all_spaces.remove(move.space)

        for space in all_spaces:
            row1 = [1,2,3]
            row2 = [4,5,6]
            row3 = [7,8,9]
            column1 = [1,4,7]
            column2 = [2,5,8]
            column3 = [3,6,9]
            diag1 = [1,5,9]
            diag2 = [3,5,7]

            # Check rows
            if space in row1:
                row1.remove(space)
                if set(row1).issubset(set(player_moves)):
                    space_for_computer_move = space
            elif space in row2:
                row2.remove(space)
                if set(row2).issubset(set(player_moves)):
                    space_for_computer_move = space
            elif space in row3:
                row3.remove(space)
                if set(row3).issubset(set(player_moves)):
                    space_for_computer_move = space

            # Check columns
            if space in column1:
                column1.remove(space)
                if set(column1).issubset(set(player_moves)):
                    space_for_computer_move = space
            elif space in column2:
                column2.remove(space)
                if set(column2).issubset(set(player_moves)):
                    space_for_computer_move = space
            elif space in column3:
                column3.remove(space)
                if set(column3).issubset(set(player_moves)):
                    space_for_computer_move = space

            # Check diagonals
            if space in diag1:
                diag1.remove(space)
                if set(diag1).issubset(set(player_moves)):
                    space_for_computer_move = space
            elif space in diag2:
                diag2.remove(space)
                if set(diag2).issubset(set(player_moves)):
                    space_for_computer_move = space

        if not space_for_computer_move:
            space_for_computer_move = random.choice(all_spaces)

    new_computer_move = Move.objects.create(game=current_game, player_move=False, space=space_for_computer_move)

    return
