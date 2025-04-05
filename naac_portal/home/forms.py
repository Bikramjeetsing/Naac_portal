from django import forms
from .models import PDF, Reminder
# Compare this snippet from naac_portal/home/forms.py:

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['category', 'name', 'file']
# Compare this snippet from naac_portal/home/templates/alert.html:
   
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["email", "reminder_name", "reminder_time", "repeat_yearly"]