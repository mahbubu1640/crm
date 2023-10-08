# crm_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Role, CustomField

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), empty_label=None)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = ('label', 'field_type')

    # Add custom validation or additional form fields as needed
