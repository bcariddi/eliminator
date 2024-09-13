from django import forms
from .models import League


class LeagueCreateForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name', 'password']
        labels = {
            'name': 'League Name',
            'password': 'League Password'
        }
