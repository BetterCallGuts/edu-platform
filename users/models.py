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
    phone         = models.CharField(max_length=20, blank=True, verbose_name=_('Phone'), null=True)
    teacher       = models.ManyToManyField(
        'self', 
       
     blank=True,
        verbose_name=_('Teacher')
        )
    
    first_section  = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('First Section'))
    text_in_picture = models.TextField(blank=True, null=True, verbose_name=_('Text In Picture'))
    text_below     = models.TextField(blank=True, null=True, verbose_name=_('Text Below'))
    second_section = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Second Section'))
    third_section  = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Third Section'))
    fourth_section = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Fourth Section'))
    social_background = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Social Background'))
    instgram_link = models.URLField(blank=True, null=True, verbose_name=_('Instagram Link'))
    instgram_icon = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Instagram Icon'))
    facebook_link = models.URLField(blank=True, null=True, verbose_name=_('Facebook Link'))
    facebook_icon = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Facebook Icon'))
    youtube_link = models.URLField(blank=True, null=True, verbose_name=_('Youtube Link'))
    youtube_icon = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Youtube Icon'))




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