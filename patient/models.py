from django.db import models
from userauths import models as userauths_models
from django.utils import timezone

NOTIFICATION_TYPE = (
    ("Appointment Scheduled", "Appointment Scheduled"),
    ("Appointment Cancelled", "Appointment Cancelled"),
)


# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(userauths_models.User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateTimeField(default=timezone.now(), null=True, blank=True)
    bood_group = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.full_name}'


class Patient_notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True,
                               blank=True)  # A doctor can have many notification
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='patient_appointment_notification')
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.patient.full_name} Notification"

