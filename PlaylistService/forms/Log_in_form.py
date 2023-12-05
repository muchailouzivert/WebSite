from django import forms
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.exceptions import ValidationError


# Create your forms here.
class NewUserForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Add your custom validation logic here
        if len(password1) < 8 or len(password2) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Add your custom validation logic here
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        return password2

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


