import random
import copy

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def three_in_a_row(positions):
    for i in range(3):
        if positions[i][0] == positions[i][1] == positions[i][2] != "-":
            return True
        if positions[0][i] == positions[1][i] == positions[2][i] != "-":
            return True

    if positions[0][0] == positions[1][1] == positions[2][2] != "-" or \
            positions[0][2] == positions[1][1] == positions[2][0] != "-":
        return True

    return False


def get_available_moves(positions):
    available_moves = []
    for i in range(3):
        for j in range(3):
            if positions[i][j] == "-":
                available_moves.append([i, j])
    return available_moves


def best_move(positions):
    available_moves = get_available_moves(positions)

    # If user didn't use the middel cell in first move, then take the middle cell.
    if len(available_moves) == 8:
        if [1, 1] in available_moves:
            return [1, 1]
        else:
            return [0, 0]

    for i in available_moves:
        temp_positions = copy.deepcopy(positions)
        temp_positions[i[0]][i[1]] = "X"
        if three_in_a_row(temp_positions):
            return i

    for i in available_moves:
        temp_positions = copy.deepcopy(positions)
        temp_positions[i[0]][i[1]] = "O"
        if three_in_a_row(temp_positions):
            return i

    for i in range(3):
        for j in range(3):
            if positions[i][j] == "O":
                try:
                    if positions[i+1][j] == "-":
                        return [i+1, j]
                except:
                    pass
                try:
                    if positions[i-1][j] == "-":
                        return [i-1, j]
                except:
                    pass
                try:
                    if positions[i][j+1] == "-":
                        return [i, j+1]
                except:
                    pass
                try:
                    if positions[i][j-1] == "-":
                        return [i, j-1]
                except:
                    pass

    return random.choice(available_moves)


def game(request):
    positions_string = request.GET.get("positions", "")
    if not positions_string:
        return HttpResponse("")

    positions_array = positions_string.split(",")
    positions = [positions_array[:3], positions_array[3:6], positions_array[6:]]

    if three_in_a_row(positions):
        return HttpResponse(simplejson.dumps({"move": "", "win": "user"}))

    available_moves = get_available_moves(positions)
    if not available_moves:
        return HttpResponse(simplejson.dumps({"move": "", "win": "draw"}))

    move = best_move(positions)
    positions[move[0]][move[1]] = "X"
    win = ""
    if three_in_a_row(positions):
        win = "ai"

    return HttpResponse(simplejson.dumps({"move": move, "win": win}))
