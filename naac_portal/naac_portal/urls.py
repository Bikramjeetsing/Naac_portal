"""
URL configuration for naac_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from home.views import *
 #upload_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
   path('chapter/year/', chapter, name='chapter'),
    path('alert/', alert_view, name='alert'),
    path('login/', login_view, name='login'),
    path('File_upload/', File_upload, name='File_upload'),
    path('upload_pdf/', upload_pdf, name='upload_pdf'),
    path('logout/', user_logout, name='logout'),
    path('year-list/', year_list, name='year_list'),
    path('show_data/', show_data, name='show_data'),
    path('upload/', upload_pdf, name='upload_pdf'),
    path('get-subchapters/', get_subchapters, name='get_subchapters'),
    path('get-categories/', get_categories, name='get_categories'),
    path('developers/', development, name='development'),
    path('delete/<int:pdf_id>/', delete_pdf, name='delete_pdf'),
    path('set-reminder/', set_reminder, name='set_reminder'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)