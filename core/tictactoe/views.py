from core.utils import CBVBaseView
from django.views.decorators.csrf import csrf_exempt

class TicTacToeView(CBVBaseView):
    def get(self, request):
        return self.to_template()


    def post(self, request):
        board = {
            'm1': '',
            'm2': 'O',
            'm3': 'X',
            'm4': '',
            'm5': 'X',
            'm6': '',
            'm7': '',
            'm8': 'O',
            'm9': '',
        }
        return self.to_json(board)


