from django import forms
from accounts.models import StaffInvitation

class StaffInvitationForm(forms.ModelForm):
    class Meta:
        model = StaffInvitation
        fields = ['email']


from django import forms
from accounts.models import User

class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
