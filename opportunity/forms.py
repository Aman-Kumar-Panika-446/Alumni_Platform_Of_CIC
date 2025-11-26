from django import forms
from .models import *
from datetime import date
class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = "__all__"
        exclude = ['user']
        
        widgets = {
            "organization_name": forms.TextInput(attrs= {"pattern": "[a-zA-Z,. ]{3,}", "title":"Only alphabets are allowed & provide atleast 3 aphabets in name.."}),
            "role": forms.TextInput(attrs= {"pattern": "(?=(?:.*[A-Za-z,.]){3,}).+", "title":"Use atleast 3 aphabets."}),
            "last_date": forms.DateInput(attrs={"type": "date",'min': date.today().strftime('%Y-%m-%d')}),
            "description": forms.Textarea(attrs={"rows": 3}),

        }

        help_texts = {
            'duration': 'eg. 2 months, 1 week etc..',
        }

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = "__all__"
        exclude = ['opportunity', 'user']


class OpportunityReportForm(forms.ModelForm):
    class Meta:
        model = OpportunityReport
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