from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Profile, LiveEvent, UserEventStatus

class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User  # Use the built-in User model
        fields = ('username', 'email', 'password1', 'password2')  # Include 'name' in the fields

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'second_name']


class LiveEventForm(forms.ModelForm):
    class Meta:
        model = LiveEvent
        fields = ['name', 'venue', 'year']

class UserEventStatusForm(forms.ModelForm):
    class Meta:
        model = UserEventStatus
        fields = ['status']

class SelectLiveEventForm(forms.Form):
    event = forms.ModelChoiceField(queryset=LiveEvent.objects.all())
