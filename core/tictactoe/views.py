from core.utils import CBVBase

class TicTacToeView(CBVBase):
	def get(self, request):
		return self.to_template()


