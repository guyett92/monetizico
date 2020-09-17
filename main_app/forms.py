from django.forms import ModelForm
from .models import User, Profile
from django import forms
from datetime import date

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'birth_date', 'bio')
        widgets = {'birth_date':DateInput(attrs={'type':'date'}),}
