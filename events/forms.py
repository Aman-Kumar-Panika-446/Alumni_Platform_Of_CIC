from django import forms
from .models import Event, EventReport

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ['user']
        
        widgets = {
            "time": forms.TimeInput(format="%H:%M", attrs={'type': 'time'}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

class EventReportForm(forms.ModelForm):
    class Meta:
        model = EventReport
        fields  = ['description']

        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Why do want to report...?',
                'rows': 3,
                'class': 'form-control'
            })
        }