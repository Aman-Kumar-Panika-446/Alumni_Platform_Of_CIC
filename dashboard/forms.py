from django import forms
from authentication.models import Experience, Skill

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = "__all__"
        exclude = ['user']
        widgets = {
            "organization_name":forms.TextInput(attrs={
                "pattern":"(?=(?:.*[A-Za-z]){3,})[A-Za-z0-9 .,&()-]+",
                "title": "Use at least 3 alphabets. Letters, numbers, spaces, . , & ( ) - allowed."
            }),
            "designation": forms.TextInput(attrs={
                "pattern": "(?=(?:.*[A-Za-z]){3,}).+",
                "title": "Use at least 3 alphabets. Letters, numbers, spaces, . , & ( ) - allowed."
            }),
            "location":forms.TextInput(attrs={
                "pattern": "(?=(?:.*[A-Za-z]){2,})[A-Za-z .,&()-]+",
                "title": "Use at least 2 alphabets. Letters, spaces, . , & ( ) - allowed."
            }),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={
                "rows": 3, 
                "pattern": "(?=(?:.*[A-Za-z]){3,})[A-Za-z0-9 .,&()\-!?:;\n]+",
                "title": "Use at least 3 alphabets. Common punctuation allowed."
            }),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill

        fields = "__all__"
        exclude = ['user']

        widgets = {
            'skill_name': forms.TextInput(attrs={
                'pattern': '[A-Za-z ]+',
                'title': 'Only alphabets allowed'
            }),
        }

