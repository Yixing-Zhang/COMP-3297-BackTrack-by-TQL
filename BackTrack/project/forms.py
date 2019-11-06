from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BackTrackUser


class BackTrackUserCreationForm(UserCreationForm):
    class Meta:
        model = BackTrackUser
        fields = ('username', 'email')


class BackTrackUserChangeForm(UserChangeForm):
    class Meta:
        model = BackTrackUser
        fields = ('username', 'email')
