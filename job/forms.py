from django import forms
from .models import Interview

class SetInterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['date', 'time', 'location', 'notes'] 