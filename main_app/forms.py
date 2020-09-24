from django.forms import ModelForm
from .models import User, Profile
from django import forms
from datetime import date

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'bio']
        widgets = {'birth_date':forms.DateInput(attrs={'type':'date'}),}


    