from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email",
            "required": True,
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
            "required": True,
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their profile details."""
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email address"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name"
            }),
        }



# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, StaffInvitation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

class StaffRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "First Name"
    }))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Last Name"
    }))
    
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "password1", "password2"]

