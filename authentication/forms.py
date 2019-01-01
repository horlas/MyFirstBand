from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields =['email',]


class CustomLoginForm(AuthenticationForm):
     '''form to log an user using the django User model, this form is passed to the login view'''

     class Meta:
         model = User
         fields = ['email', 'password']



