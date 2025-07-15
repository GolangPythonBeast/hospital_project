from django.contrib import admin
from .models import Patient, Patient_notification
# Register your models here.


class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'mobile', 'gender', 'date_of_birth']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'type', 'seen', 'date']

admin.site.register(Patient, PatientAdmin)
admin.site.register(Patient_notification, NotificationAdmin)
