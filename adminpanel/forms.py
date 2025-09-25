from django import forms
from accounts.models import StaffInvitation

class StaffInvitationForm(forms.ModelForm):
    class Meta:
        model = StaffInvitation
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter staff email address"
            }),
        }



from django import forms
from accounts.models import User

class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "is_active"]
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
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

