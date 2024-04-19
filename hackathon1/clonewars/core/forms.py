from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Email')
