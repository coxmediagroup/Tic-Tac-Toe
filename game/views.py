from django.views.generic import TemplateView

class GameView(TemplateView):
	def get_template_names(self):
		return ["game/game" + self.kwargs['version'] + ".html"]

