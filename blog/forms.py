from django import forms
from .models import Post, Tag, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['com_author', 'com_content', 'post']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Parollar mos emas!")
        return cleaned

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
