from django.contrib.auth.models import AbstractUser
from django.db import models

class Client(AbstractUser):
    # bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Customize related_name to prevent conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Customize related_name to prevent conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

  

        