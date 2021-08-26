from django import forms
from .models import DealsModel


class DealsForm(forms.ModelForm):
    class Meta:
        model = DealsModel
        fields = ('upload_deal',)
