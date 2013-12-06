from core.utils import CBVBaseView
from django.views.decorators.csrf import csrf_exempt

class TicTacToeView(CBVBaseView):
    def get(self, request):
        return self.to_template()


    def post(self, request):
        return self.to_json()


