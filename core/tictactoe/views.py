from core.utils import CBVBaseView

class TicTacToeView(CBVBaseView):
	def get(self, request):
		return self.to_template()


class MoveView(CBVBaseView):
	def get(self, request):
		return self.to_json()


