from django import forms
from .models import Domain

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500',
                'placeholder': 'e.g. Kitchen, Travel, Medical'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 h-32',
                'placeholder': 'Optional description of this domain...'
            })
        }