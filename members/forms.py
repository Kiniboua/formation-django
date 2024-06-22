from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    frist_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    #address = forms.CharField(max_length=200)
    class Meta:
        model = User
        fields = ('username', 'frist_name', 'last_name', 'email', 'password1', 'password2')
