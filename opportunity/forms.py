from django import forms
from .models import *

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = "__all__"
        exclude = ['user']
        
        widgets = {
            "last_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
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
            'description': forms.Textarea(attrs={
                'placeholder': 'Why do want to report...?',
                'rows': 3,
                'class': 'form-control'
            })
        }