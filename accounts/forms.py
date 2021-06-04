from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput

from .models import PostsModel


class NewPostForm(forms.ModelForm):
    heading = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Subject of the Post'}),
        max_length=150
    )
    message = forms.CharField(required=False,
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    post_image = forms.ImageField(required=False, error_messages={'invalid': ("Image files only")},
                                  widget=forms.FileInput)

    class Meta:
        model = PostsModel
        fields = ['heading', 'message', 'post_image']


class ExtendedRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 help_text="Required. please enter your first name.")
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                help_text="Required. please enter your last name.")
    email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             help_text="Required. please enter your personal email id.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
