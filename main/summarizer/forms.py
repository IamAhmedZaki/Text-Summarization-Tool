# summarizer/forms.py
from django import forms

class SummaryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "placeholder": "Paste your article here..."}))
    method = forms.ChoiceField(choices=[('extractive', 'Extractive'), ('abstractive', 'Abstractive')])
