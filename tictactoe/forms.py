from django import forms

class SelectionForm(forms.Form):
    """
    This Form simply validates that the selected choice submitted by a User is
    a valid possible choice. This validation is *not* tied to whether or not
    the given selection is available on the current Game Board or not.
    """
    SELECTION_CHOICES = (
        ('top_left', 'Top Left'),
        ('top_center', 'Top Center'),
        ('top_right', 'Top Right'),
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
        ('bottom_left', 'Bottom Left'),
        ('bottom_center', 'Bottom Center'),
        ('bottom_right', 'Bottom Right')
    )
    selection = forms.ChoiceField(choices=SELECTION_CHOICES)
