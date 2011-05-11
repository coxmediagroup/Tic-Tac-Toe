from django.template import RequestContext
from django.shortcuts import render_to_response


def cell_list():
    """ assemble a list of cell lables for a tic-tac-toe board"""
    cell_list = []
    for row in ['top','middle','bottom']:
        for col in ['left','center','right']:
            cell_list.append(col + ' ' + row)
    return cell_list


def board(request):
    # board_list = [str(val) for val in range(1,10)]
    board_list = ['X','-','-','-','O','-','-','-','-']
    cells = cell_list()
    my_board = [zip(cells[:3], board_list[:3]),
                zip(cells[3:6], board_list[3:6]),
                zip(cells[6:], board_list[6:])]
    return render_to_response('board.html',
                              {'board': my_board},
                              context_instance=RequestContext(request))