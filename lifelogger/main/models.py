from django.db import models
from django.contrib.auth.models import AbstractUser


class ExtendedUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False, max_length=255, verbose_name='email')

    USERNAME_FIELD = 'username'  # Cannot set to "email"
    EMAIL_FIELD = 'email'

    class Meta:
        ordering = ('date_joined',)
