from django.contrib import admin

# Register your models here.
from .models import Services, Appointment, MedicalRecord, Labtest, Prescription, Billing

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 1

class MedicalRecordInline(admin.TabularInline):
    model = MedicalRecord
    extra = 1

class LabTestInline(admin.TabularInline):
    model = Labtest
    extra = 1

class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1

class BillingInline(admin.TabularInline):
    model = Billing
    extra = 1

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost']
    search_fields = ['name', 'description']
    filter_horizontal = ['available_doctors']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'status']
    search_fields = ['patent__username', 'doctor__user_username']
    inlines = [MedicalRecordInline, LabTestInline, PrescriptionInline, BillingInline]

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diagnosis']

class LabTestAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'test_name']

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'medication']

class BillingAdmin(admin.ModelAdmin):
    list_display = ['patient', 'total', 'status', 'date']


admin.site.register(Services, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Labtest, LabTestAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
