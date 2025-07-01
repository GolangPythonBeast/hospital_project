from django.db import models
from doctor import models as doctor_models
from patient import models as patient_models
from shortuuid.django_fields import ShortUUIDField
# Create your models here.

class Services(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_doctors = models.ManyToManyField(doctor_models.Doctor, blank=True)

    def __str__(self):
        return f'{self.name} - {self.cost}'

class Appointment(models.Model):
    STATUS = (
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled')
    )
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_appointment')
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointment')
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_appointment')
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_is = ShortUUIDField(length=6, max_length=10, alphabet='1234567890')
    status = models.CharField(max_length=120, choices=STATUS)

    def __str__(self):
        return f'{self.patient.full_name} with {self.doctor.full_name}'


class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return f'Medical Record for {self.appointment.patient.full_name}'


class Labtest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.test_name}'


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Description for {self.appointment.patient.full_name}'


class Billing(models.Model):
    STATUS = (
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid')
    )
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="patient_billing")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='appoint_bill', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS)
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet='1234567890')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Billing for {self.patient.full_name} - Total: {self.total}'
