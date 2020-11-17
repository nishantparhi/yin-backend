from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import BlogPost, Author


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

# Blog model form


class PostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['blog_title', 'blog_content', 'coverPic']

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['description', 'facebook_URL', 'youtube_URL', 'pinterest_URL', 'twitter_URL', 'flicker_URL', 'instagram_URL', 'personal_URL']