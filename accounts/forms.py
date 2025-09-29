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


import pycountry


class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their profile details, including location and phone number."""

    # Location dropdown using pycountry
    country_choices = [(country.name, country.name) for country in pycountry.countries]
    location = forms.ChoiceField(
        choices=[("", "Select your country")] + country_choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )

    # Phone number field with 11-digit validation
    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "11-digit phone number"
        })
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "profile_image", "location", "phone_number"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "readonly": "readonly",
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

    def __init__(self, *args, **kwargs):
        """Prefill form fields with existing user data if available."""
        super().__init__(*args, **kwargs)
        if self.instance:
            # Prefill location
            if getattr(self.instance, "location", None):
                self.fields["location"].initial = self.instance.location
            # Prefill phone number
            if getattr(self.instance, "phone_number", None):
                self.fields["phone_number"].initial = self.instance.phone_number

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone



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


from django.contrib.auth.forms import SetPasswordForm
from .models import User

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}))

from django.contrib.auth.forms import SetPasswordForm

class PasswordResetForm(SetPasswordForm):
    """
    Standard Django SetPasswordForm with Bootstrap + IDs for JS validation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style and configure "New Password"
        self.fields["new_password1"].widget.attrs.update({
            "id": "id_password1",
            "class": "form-control",
            "placeholder": "Enter new password",
        })

        # Style and configure "Confirm Password"
        self.fields["new_password2"].widget.attrs.update({
            "id": "id_password2",
            "class": "form-control",
            "placeholder": "Confirm new password",
        })