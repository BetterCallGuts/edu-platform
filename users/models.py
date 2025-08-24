from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
import os
from django.utils.translation import get_language
from django.utils.html import mark_safe

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
    






    
    
    thumbnail      = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name=_('Thumbnail'))
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

    


    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug Field'), blank=True, null=True)


    def delete(self, *args, **kwargs):
        r =super().delete(*args, **kwargs)
        try:
            os.remove(self.thumbnail.path)
        except:
            pass
        return r
    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
        
        if self.role == 'teacher':
            self.slug = slugify(f"{self.username}-{self.pk}", )

            super().save(*args, **kwargs)


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


class PaymentMethodUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

    method_en  = models.CharField(max_length=100, verbose_name=_('Method en'))
    method_ar  = models.CharField(max_length=100, verbose_name=_('Method ar'))
    

    is_active  = models.BooleanField(default=True)
    photo      = models.ImageField(upload_to='payment_method_images/', verbose_name=_('Photo'), blank=True, null=True)
    number     = models.CharField(max_length=100, verbose_name=_('Number'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_method(self):
        lang = get_language()
        return self.method_ar if lang == 'ar' else self.method_en
    

    def __str__(self):
        return f"{self.method_en}"



class PaymentMethodPackage(models.Model):
    package = models.ForeignKey("PackageSubscribe",
                                
                                related_name="paymentmethodpackages",
                                 on_delete=models.CASCADE, verbose_name=_('Package'))
    method_en  = models.CharField(max_length=100, verbose_name=_('Method en'))
    method_ar  = models.CharField(max_length=100, verbose_name=_('Method ar'))
    
    number     = models.CharField(
        max_length=100,
        verbose_name=_('Number / account info '))
    photo      = models.ImageField(
        upload_to='payment_method_images/', verbose_name=_('Photo'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_method(self):
        lang = get_language()
        return self.method_ar if lang == 'ar' else self.method_en
    

    def __str__(self):
        return f"{self.method_en}"





class PackageSubscribe(models.Model):
    packagename_en = models.CharField(max_length=100, verbose_name=_('Package Name En'))
    packagename_ar = models.CharField(max_length=100, verbose_name=_('Package Name AR'))
    description_ar = models.TextField(verbose_name=_('Package Description AR'))
    description_en = models.TextField(verbose_name=_('Package Description EN'))
    user           = models.ManyToManyField(
        User,
        related_name="packages")# teachers

    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    thumbnail       = models.ImageField(
        
        upload_to='package_images/', 
        verbose_name=_('Package Thumbnail'),
         blank=True, null=True,
        
        )
    
    price           = models.FloatField(default=0, verbose_name=_('Price'))
    currency        = models.CharField(max_length=10, default='EGP', verbose_name=_('Currency'))
    numbertocontact = models.CharField(default=0         , max_length=255 )
    backgroumdcolor = models.CharField(default="#FFFFFF", max_length=255)

    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug Field'), blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
        
        self.slug = slugify(f"{self.packagename_en}-{self.pk}", )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.packagename_en}"
    
    def get_package_name(self):
        lang = get_language()
        return self.packagename_ar if lang == 'ar' else self.packagename_en
    def get_description(self):
        lang = get_language()
        return self.description_ar if lang == 'ar' else self.description_en
    class Meta:
        verbose_name = _('Package Subscribe')
        verbose_name_plural = _('Package Subscribes')




class AccessCourseRequest(models.Model):
    teacher         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="theusers", verbose_name=_('Teacher'), null=True, blank=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name="access_course_requests", verbose_name=_('User'))
    course          = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name="access_course_requests", verbose_name=_('Course'))

    account_info    = models.CharField(max_length=100, verbose_name=_('Account Info / account number'))
    screen_shot     = models.ImageField(upload_to='access_course_request_images/', verbose_name=_('Screen Shot'), blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.get_course_language} - access request"
    
    def show_screen_shot(self):
        if self.screen_shot:
            return mark_safe( f"<img src='{self.screen_shot.url}' width='300px' alt='{self.user.username}'>")
        else: return None

    show_screen_shot.short_description = _('Screen Shot')

    class Meta:
        verbose_name = _('Access Course Request')
        verbose_name_plural = _('Access Course Requests')




class AccessPackageRequest(models.Model):
    teacher         = models.ManyToManyField(User,related_name="requestedpackagesaccess",   verbose_name=_('Teacher'), null=True, blank=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name="packagesrequest", verbose_name=_('User'))
    package          = models.ForeignKey(PackageSubscribe, on_delete=models.CASCADE, related_name="accesss_packages_request", verbose_name=_('Package'))

    account_info    = models.CharField(max_length=100, verbose_name=_('Account Info / account number'))
    screen_shot     = models.ImageField(upload_to='access_course_request_images/', verbose_name=_('Screen Shot'), blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - {self.package.get_package_name} - access request"

    def show_screen_shot(self):
        if self.screen_shot:
            return mark_safe( f"<img src='{self.screen_shot.url}' width='300px' alt='{self.user.username}'>")
        else: return None
    show_screen_shot.short_description = _('Screen Shot')

    class Meta:
        verbose_name = _('Access Package Request')
        verbose_name_plural = _('Access Package Requests')