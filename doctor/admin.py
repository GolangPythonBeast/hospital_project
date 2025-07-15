from django.contrib import admin
from .models import Doctor, Doctor_notification
# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'specialization', 'qualification', 'years_of_experience']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type', 'seen', 'date']


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Doctor_notification, NotificationAdmin)

