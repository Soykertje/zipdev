"""Form to score candidades based on a defined criteria."""
from django import forms


class ScoringForm(forms.Form):
    query = forms.CharField(label='Criteria to search candidates', max_length=200, min_length=10, widget=forms.Textarea)
