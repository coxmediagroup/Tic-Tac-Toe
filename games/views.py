from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from braces.views import JSONResponseMixin

from .models import TicTacToe


class TicTacToeList(ListView):
    model = TicTacToe

    def post(self, request, *args, **kwargs):
        """If this page was posted to, create a new game and go to it."""
        game = TicTacToe.objects.create()
        return redirect(game)


class TicTacToeDetail(DetailView):
    model = TicTacToe


class TicTacToeNextMove(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        """Check if the request was made using ajax and if so process it."""
        if request.is_ajax():
            mark = request.GET.get('mark', None)
            obj = request.GET.get('obj', None)
            
            if mark and obj:
                try:
                    obj = TicTacToe.objects.get(pk=obj)
                except DoesNotExist:
                    raise Http404
                
                # Initiate a move with the given mark.
                move = obj.move(int(mark), request.user)

                # Create json data to send back for page update.
                context = {
                    'pMark': [
                        int(mark), obj.board[int(mark)]],
                    'cMark': [
                        obj.last_move, obj.board[obj.last_move]]
                }

                if obj.is_complete:
                    context.update({'message': 'Game Over'})
            
            return self.render_json_response(context, *args, **kwargs)

        return Http404
