from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', _('Student')),
        ('assistant', _('Assistant')),
        ('teacher', _('Teacher')),
        ('admin', _('Admin')),
    )
    role          = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_limit = models.IntegerField(default=0, null=True , blank=True, verbose_name=_('Student Limit'))

    teacher       = models.ManyToManyField(
        'self', 
       
     blank=True,
        verbose_name=_('Teacher')
        )
    



class LiveStream(models.Model):
    PLATFORM_CHOICES = (
        ('youtube', 'YouTube'),
        ('twitch', 'Twitch'),
        ('facebook', 'Facebook'),
    )
    platform   = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    embed_code = models.TextField()  
    teacher    = models.ForeignKey(User, related_name="stream", verbose_name=_("teacher"), on_delete=models.CASCADE)
    is_live    = models.BooleanField(default=False)

# {% for stream in livestreams %}
#   {% if stream.is_live %}
#     {{ stream.embed_code|safe }}
#   {% endif %}
# {% endfor %}