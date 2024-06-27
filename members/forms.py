from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 

# Django Registration Forms and Bootstrap
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget= forms.EmailInput(attrs={'class':'form-control'}))
    frist_name = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class':'form-control'}))
    #address = forms.CharField(max_length=200)
    class Meta:
        model = User
        fields = ('username', 'frist_name', 'last_name', 'email', 'password1', 'password2')
    # A customized user registration form class
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegisterUserForm, self).__init__(*args, **kwargs)
    
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
