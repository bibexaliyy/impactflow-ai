from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    organization_name = forms.CharField(
        max_length=255,
        help_text="Your NGO/CSO/CBO name — this creates your organization workspace.",
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "organization_name", "password1", "password2")
