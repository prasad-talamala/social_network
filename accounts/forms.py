from django import forms
from django.forms import TextInput

from .models import PostsModel


class NewPostForm(forms.ModelForm):
    heading = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Subject of the Post'}),
        max_length=150
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = PostsModel
        fields = ['heading', 'message']
