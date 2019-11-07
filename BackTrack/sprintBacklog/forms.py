from django import forms
from .models import *


class SprintForm(forms.ModelForm):
    class Meta:
        model = SprintBacklog
        fields = ('sprintNumber', 'capacity', 'ddl')
