from core.utils import CBVBase

class HomeView(CBVBase):
	def get(self, request):
		return self.to_template('home.html')


