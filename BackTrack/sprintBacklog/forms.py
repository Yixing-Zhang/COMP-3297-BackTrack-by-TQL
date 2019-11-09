from django import forms
from .models import *


class SprintForm(forms.ModelForm):
    class Meta:
        model = SprintBacklog
        fields = ('capacity', 'ddl')


class TaskAddForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'estimated',)


class TaskModifyForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'estimated', 'effortsDone')
