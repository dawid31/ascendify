from django import forms
from .models import Profile, Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    # Custom fields for climbing stats
    experience_level = forms.ChoiceField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], required=False)
    completed_routes = forms.IntegerField(min_value=0, required=False)
    highest_grade = forms.CharField(max_length=50, required=False)
    
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        climbing_stats = self.instance.climbing_stats if self.instance.climbing_stats else {}
        self.fields['experience_level'].initial = climbing_stats.get('experience_level', 'beginner')
        self.fields['completed_routes'].initial = climbing_stats.get('completed_routes', 0)
        self.fields['highest_grade'].initial = climbing_stats.get('highest_grade', '')

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        # Update climbing_stats JSONField
        climbing_stats = profile.climbing_stats or {}
        climbing_stats['experience_level'] = self.cleaned_data['experience_level']
        climbing_stats['completed_routes'] = self.cleaned_data['completed_routes']
        climbing_stats['highest_grade'] = self.cleaned_data['highest_grade']
        profile.climbing_stats = climbing_stats
        if commit:
            profile.save()
        return profile
    
class LocationForm(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input text-black', 'placeholder': 'Enter city name'}))


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date']