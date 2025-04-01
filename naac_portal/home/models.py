# models.py
from django.db import models
from django.utils.timezone import now

class Year(models.Model):
    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)


class Chapter(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField(max_length=255)
    subname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class SubChapter(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='subchapters')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    subchapter = models.ForeignKey(SubChapter, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PDF(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pdfs')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Saves date & time of upload

    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
    

class Reminder(models.Model):
    whatsapp_number = models.CharField(max_length=20)
    reminder_name = models.CharField(max_length=255)
    reminder_time = models.DateTimeField()
    repeat_yearly = models.BooleanField(default=False)  # New field to enable yearly reminders

    def __str__(self):
        return f"{self.reminder_name} - {self.whatsapp_number}"# forms.pypython manage.py makemigrations

