from django import forms

class GameForm(forms.Form):
    game_choices = [(0,0),(1,1),(2,2)]

    def __init__(self,*args,**kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for x in xrange(0,9):
            self.fields["box_%s" % x] = forms.ChoiceField(choices=game_choices, default=0)
