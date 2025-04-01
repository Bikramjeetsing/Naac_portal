from django.contrib import admin

# Register your models here.
from .models import Year, Chapter, SubChapter, Category, PDF

admin.site.register(Year)
admin.site.register(Chapter)
admin.site.register(SubChapter)
admin.site.register(Category)
admin.site.register(PDF)
# Compare this snippet from naac_portal/home/forms.py:





















# superadmin login details
# username: superadmin
# password: superadmin
# email: arshdeepsingh17092@gmail.com