from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture']
