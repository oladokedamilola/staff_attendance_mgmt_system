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
        fields = ["email", "first_name", "last_name", "profile_image"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "readonly": "readonly",  # non-editable but visible
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name"
            }),
            "profile_image": forms.ClearableFileInput(attrs={
                "class": "form-control d-none",
                "accept": "image/*",
                "onchange": "previewImage(event)"
            }),
        }



from .models import User
from django.contrib.auth.forms import UserCreationForm

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

