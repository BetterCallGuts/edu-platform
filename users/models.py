from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role          = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_limit = models.IntegerField(default=0, null=True , blank=True, verbose_name=_('Student Limit'))

    teacher       = models.ManyToManyField(
        'self', 
        related_name='students', 
        null=True, blank=True,
        verbose_name=_('Teacher')
        )