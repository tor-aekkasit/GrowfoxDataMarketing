from django import forms
from .models import PageGroup

class PageURLForm(forms.Form):
    url = forms.URLField(label="Page URL", required=True)

class PageGroupForm(forms.ModelForm):
    class Meta:
        model = PageGroup
        fields = ['group_name']
        widgets = {
            'page_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Group Name'
            }),
        }
