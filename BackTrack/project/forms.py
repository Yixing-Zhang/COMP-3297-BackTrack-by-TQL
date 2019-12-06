from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class BackTrackUserCreationForm(UserCreationForm):
    class Meta:
        model = BackTrackUser
        fields = ('username', 'email')


class BackTrackUserChangeForm(UserChangeForm):
    class Meta:
        model = BackTrackUser
        fields = ('username', 'email')


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description')