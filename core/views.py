from core.utils import CBVBaseView

class HomeView(CBVBaseView):
	def get(self, request):
		return self.to_template()


