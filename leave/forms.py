from django import forms
from .models import Leave

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ["leave_type", "start_date", "end_date", "reason", "evidence"]
        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-select", "id": "id_leave_type"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter reason..."}),
            "evidence": forms.ClearableFileInput(attrs={"class": "form-control", "id": "id_evidence"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        leave_type = cleaned_data.get("leave_type")
        evidence = cleaned_data.get("evidence")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Validate dates
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")

        # Require evidence if Sick Leave
        if leave_type == "sick" and not evidence:
            self.add_error("evidence", "Evidence file is required for Sick Leave.")

        return cleaned_data
