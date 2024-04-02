from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True, default='username')
    email = models.EmailField(max_length=255, unique=True, default='email')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Define custom related names for groups and user_permissions
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')

    # Any extra fields would go here
    def __str__(self):
        return self.email
