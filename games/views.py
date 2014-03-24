from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from braces.views import JSONResponseMixin

from .models import TicTacToe


class TicTacToeList(ListView):
    model = TicTacToe

    def post(self, request, *args, **kwargs):
        game = TicTacToe.objects.create()
        return redirect(game)

class TicTacToeDetail(DetailView):
    model = TicTacToe


class TicTacToeNextMove(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        # Check if the request is async and if so process it.        
        if request.is_ajax():
            mark = request.GET.get('mark', None)
            obj = request.GET.get('obj', None)
            
            if mark and obj:
                try:
                    obj = TicTacToe.objects.get(pk=obj)
                except DoesNotExist:
                    return

                move = obj.move(int(mark), request.user)
                obj.save()

            context = {
                'player_mark': [
                    int(mark), obj.get_board[int(mark)]
                ],
            }

            try:
                context.update({'computer_mark': [move[0], move[1]]})
            except IndexError:
                pass

            if obj.is_complete:
                context.update({'message': 'Game Over'})
            
            return self.render_json_response(context, *args, **kwargs)
