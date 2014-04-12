from django import forms

class GameForm(forms.Form):
    '''0: empty square
    1: your square
    2: opponents square
    '''

    def __init__(self,*args,**kwargs):
        first = kwargs.pop('first',False)
        super(GameForm, self).__init__(*args, **kwargs)
        game_choices = [(0, ''),(1, 'X' if first else 'O'),(2, 'O' if first else 'X')]

        for x in xrange(0,9):
            self.fields["box_%s" % x] = forms.ChoiceField(choices=game_choices, initial=0, widget=forms.HiddenInput())
