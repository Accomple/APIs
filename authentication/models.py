from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime
import random


class CustomUser(AbstractUser):
    username = models.EmailField(unique=True)
    first_name = models.CharField(max_length=16, null=True, blank=True)
    last_name = models.CharField(max_length=16, null=True, blank=True)
    email_verification_token = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics')
    date_of_birth = models.DateField(null=True, blank=True)
    password_reset_token = models.CharField(max_length=40)
    is_verified = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=6, null=True, blank=True)
    creation_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.key is None:
            return "EMPTY"
        if self.is_expired():
            return "EXPIRED"
        return self.key

    def generate(self):
        self.key = ''.join(random.choice('0123456789') for _ in range(6))
        self.creation_time = datetime.now()
        self.save()

    def is_expired(self):
        delta = datetime.now() - self.creation_time.replace(tzinfo=None)
        days = delta.days
        seconds = delta.seconds
        return not (days == 0 and seconds <= 600)


class Owner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Seeker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username
