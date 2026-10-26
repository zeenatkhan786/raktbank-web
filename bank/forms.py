from django import forms

from .models import BloodRequest, BloodStock, Donor


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            "name", "age", "gender", "blood_group", "phone",
            "email", "city", "last_donation", "is_available",
        ]
        widgets = {
            "last_donation": forms.DateInput(attrs={"type": "date"}),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = BloodStock
        fields = ["units"]


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            "patient_name", "blood_group", "units_needed",
            "hospital", "city", "contact", "required_by",
        ]
        widgets = {
            "required_by": forms.DateInput(attrs={"type": "date"}),
        }


class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ["status"]
