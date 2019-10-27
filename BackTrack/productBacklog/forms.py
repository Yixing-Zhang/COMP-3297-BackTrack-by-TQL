from django import forms

from .models import PBI


class PBIAddForm(forms.ModelForm):
    class Meta:
        model = PBI
        fields = ('name', 'description', 'estimated', 'priority')


class PBIModifyForm(forms.ModelForm):
    class Meta:
        model = PBI
        fields = ('name', 'description', 'estimated', 'priority', 'status', 'sprintNumber')
