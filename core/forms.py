from django import forms
from .models import Domain, Item, Translation
from allauth.account.forms import LoginForm, SignupForm

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ['name', 'description','image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500',
                'placeholder': 'e.g. Kitchen, Travel, Medical'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 h-32',
                'placeholder': 'Optional description of this domain...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            })
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            })
        }

class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ['language_code', 'word', 'description', 'example_sentence', 'is_primary']
        widgets = {
            'language_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl',
                'placeholder': 'en, hi, fr, es etc.'
            }),
            'word': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl',
                'placeholder': 'Word in this language'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl h-24',
                'placeholder': 'Meaning or description...'
            }),
            'example_sentence': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl h-20',
                'placeholder': 'Example sentence (optional)'
            }),
            'is_primary': forms.CheckboxInput(attrs={'class': 'w-5 h-5'})
        }
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['login'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1',
            'placeholder': 'Enter your username or email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1',
            'placeholder': 'Enter your password'
        })


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1',
            'placeholder': 'Enter your email'
        })
        
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1',
                'placeholder': 'Choose a username'
            })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1',
            'placeholder': 'Confirm password'
        })