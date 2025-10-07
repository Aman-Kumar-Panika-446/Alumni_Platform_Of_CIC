from django import forms
from authentication.models import Experience, Skill

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = "__all__"
        exclude = ['user']
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill

        fields = "__all__"
        exclude = ['user']