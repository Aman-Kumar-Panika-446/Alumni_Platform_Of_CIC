from django import forms
from authentication.models import StatusDocuments

class StatusDocumentForm(forms.ModelForm):
    class Meta:
        model = StatusDocuments
        field = ['document']
        exclude = ['alumni']

