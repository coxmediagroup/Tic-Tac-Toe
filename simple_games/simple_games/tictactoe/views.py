import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Player, TicTacToe

SIGNS = ('X', 'O')


class TicTacToeViewController(TemplateView):

    template_name = 'tictactoe.html'
    game = TicTacToe
    player = Player

    def get(self, request, *args, **kwargs):

        if "move" in kwargs:
            player_move = int(kwargs.get('move'))-1
            player_sign = request.session['player_sign']
            game_board = request.session['board']
            message = ''
            self.player = Player(player_sign)
            self.game = TicTacToe(self.player, game_board)
            status = True
            if not player_move in self.game.possible_moves():
                message = u"Move invalid"
            else:
                self.game.make_move(player_move, self.player.sign)
                if self.game.complete():
                    status = False
                    message = u"Game Over"
                else:
                    self.game.next_move()
                    message = u"Your turn"
                    if self.game.complete():
                        status = False
                        message = u"Game Over"

            request.session['board'] = self.game.squares
            winner = self.game.winner_label()
            variables = {
                'board': self.game.squares,
                'message': message,
                'status': status,
                'winner': winner
            }
            json_output = json.dumps([variables])
            response = HttpResponse(json_output, mimetype="application/json")

        elif 'sign' in kwargs:
            sign = kwargs.get('sign')
            if sign in SIGNS:
                self.player = Player(sign)
            else:
                self.player = Player('O')
            self.game = TicTacToe(self.player)
            request.session['player_sign'] = self.player.sign
            request.session['board'] = self.game.squares

            variables = {
                'board': self.game.squares,
                'message': "Your turn"
            }
            json_output = json.dumps([variables])
            response = HttpResponse(json_output, mimetype="application/json")

        else:
            empty_board = [None for i in range(9)]
            variables = {
                'board': empty_board,
                'message': "Pick your sign"
            }
            response = render(request, self.template_name, variables)

        return response
