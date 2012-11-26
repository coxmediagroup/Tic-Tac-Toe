from django import forms


class GridFormField(forms.Field):
    """
    A form field that displays a grid's value as rows of text.

    The purpose of this challenge is to write a program which cannot lose,
    which I have done. In the interest of making it easier to interact with
    said program, I have made this form field. And more complex MultiValueField
    would be more suitable if I had more time.
    """
    widget = forms.widgets.Textarea

    def __init__(self, *args, **kwargs):
        super(GridFormField, self).__init__(*args, **kwargs)
        self.help_text = u'Replace an underscore with an "o" and submit to play.'

    def prepare_value(self, value):
        # Split the grid into three rows so line breaks can be added. In the
        # interest of time we do this hack-of-a-grid instead of building an
        # actual table with different form fields for each position.
        rows = [''.join(row) for row in value[:3], value[3:6], value[6:]]
        return u'{0}\r\n{1}\r\n{2}'.format(*rows)

    def clean(self, value):
        # Remove the linebreaks that were previously added.
        value = value.replace('\r\n', '').lower()
        return super(GridFormField, self).clean(value)
