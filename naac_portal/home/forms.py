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
        fields = ["whatsapp_number", "reminder_name", "reminder_time", "repeat_yearly"]