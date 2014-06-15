from django import forms

from authoring.models import Course, Client, Author


class CourseForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        Client.objects.get_query_set(),
        empty_label=None
    )
    author = forms.ModelChoiceField(Author.objects.all(), empty_label=None)
    class Meta:
        model = Course
        fields = ( 'code', 'title', 'description', 'client', 'author')
