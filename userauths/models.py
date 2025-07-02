from django.db import models
from django.contrib.auth.models import AbstractUser


USER_TYPE = (
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient')
)

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=500)
    username = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=30, choices=USER_TYPE, null=True, blank=True, default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        email_username, domain = self.email.split('@')
        if self.username == '' or self.username == None:
            self.username = email_username

        super(User, self).save(*args, **kwargs)



