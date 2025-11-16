from django import forms
from .models import Event, EventReport

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ['user']
        
        widgets = {
            "title":forms.TextInput(attrs={"pattern":"(?=(?:.*[A-Za-z]){3,}).+", "title":"Use atleast 3 alphabets or valid name"}),
            "venue":forms.TextInput(attrs={"pattern":"(?=(?:.*[A-Za-z]){3,}).+", "title":"Use atleast 3 alphabets or valid name"}),
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
            'description': forms.TextInput(attrs={
                'rows': 3,
                'placeholder': 'Why do want to report...?',
                'pattern':"(?=(?:.*[A-Za-z]){10,}).+", 
                'title':"Use atleast 10 alphabets or valid description",
                'class': 'form-control'
            })
        }