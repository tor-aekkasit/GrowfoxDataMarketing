from django import forms
from .models import PageGroup

class PageURLForm(forms.Form):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
    ]
    platform = forms.ChoiceField(
        choices=PLATFORM_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-lg',
        }),
        required=True,  # บังคับเลือก platform
        label="Platform"
    )
    url = forms.URLField(
        label="Page URL",
        widget=forms.URLInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Input URL Page'
        })
    )

class PageGroupForm(forms.ModelForm):
    class Meta:
        model = PageGroup
        fields = ['group_name']
        widgets = {
            'group_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',  # เพิ่ม form-control-lg เพื่อให้ input ใหญ่เหมือน add_page
                'placeholder': 'Input Group Name'
            }),
        }
