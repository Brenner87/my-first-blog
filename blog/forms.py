from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('title', 'text')

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('author', 'text',)