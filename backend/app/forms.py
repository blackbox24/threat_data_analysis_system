from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class ThreatForm(forms.ModelForm):
    class Meta:
        model = Threat
        fields = ['source_ip', 'attack_type', 'details']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email',"role"]



#