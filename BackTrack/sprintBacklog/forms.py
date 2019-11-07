from django import forms
from project.models import Project
from .models import *


class BasicForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('activeSprint',)
