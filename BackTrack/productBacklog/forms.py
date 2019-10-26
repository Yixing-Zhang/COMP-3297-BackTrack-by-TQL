from django import forms

from .models import PBI

class PBIForm(forms.ModelForm):

    class Meta:
        model = PBI
        fields = ('name', 'description', 'estimated', 'priority', 'status')