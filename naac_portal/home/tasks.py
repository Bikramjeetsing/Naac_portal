from celery import shared_task
from django.utils.timezone import now
from .models import Reminder
from .views import send_whatsapp_message

@shared_task
def check_and_send_reminders():
    reminders = Reminder.objects.filter(reminder_time__lte=now())

    for reminder in reminders:
        send_whatsapp_message(reminder.whatsapp_number, reminder.reminder_name)

        if reminder.repeat_yearly:
            # Create next year's reminder
            new_reminder_time = reminder.reminder_time.replace(year=reminder.reminder_time.year + 1)
            Reminder.objects.create(
                whatsapp_number=reminder.whatsapp_number,
                reminder_name=reminder.reminder_name,
                reminder_time=new_reminder_time,
                repeat_yearly=True
            )

        reminder.delete()  # Remove old reminder after sending
