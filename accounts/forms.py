from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']