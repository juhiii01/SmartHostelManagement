from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["branch", "location", "room_number", "category", "priority", "title", "description", "photo"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "title": forms.TextInput(attrs={"placeholder": "e.g. Fan not working"}),
            "room_number": forms.TextInput(attrs={"placeholder": "Required only for hostel room"}),
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["status", "assigned_staff", "staff_remarks"]
        widgets = {"staff_remarks": forms.Textarea(attrs={"rows": 3})}
