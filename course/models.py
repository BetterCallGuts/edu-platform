from django.db import models
from django.contrib.auth import get_user_model
# translator
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
import pytz
import os
import datetime
from django.utils.html import mark_safe
from django.utils.translation import get_language
from django.template.defaultfilters import slugify
from django.utils import timezone



User = get_user_model()


class Course(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

    course_name_ar = models.CharField(max_length=100 , verbose_name=_('Course Name ar'))
    course_name_en = models.CharField(max_length=100 , verbose_name=_('Course Name en'))


    thumbnail_pc     = models.ImageField(upload_to='course_images/' , verbose_name=_('Course Thumbnail'), blank=True, null=True)
    thumbnail_mobile = models.ImageField(upload_to='course_images/' , verbose_name=_('Course Thumbnail'), blank=True, null=True)
 

    course_description_ar = models.TextField( verbose_name=_('Course Description ar'))
    course_description_en = models.TextField( verbose_name=_('Course Description en'))

    def show_thumbnail_pc(self):
        if self.thumbnail_pc:
            return mark_safe( f"<img src='{self.thumbnail_pc.url}' width='300px' alt='{self.course_name_en}'>")
        else: return None
    
    def show_thumbnail_mobile(self):
        if self.thumbnail_mobile:
            return mark_safe( f"<img src='{self.thumbnail_mobile.url}' width='300px'   alt='{self.course_name_en}'>")
        else: return None
    
    def get_course_language(self):
        lang = get_language()
        return self.course_name_ar if lang == 'ar' else self.course_name_en
    def get_course_description_language(self):
        lang = get_language()
        return self.course_description_ar if lang == 'ar' else self.course_description_en
    show_thumbnail_mobile.short_description = _('Thumbnail Mobile')
    show_thumbnail_pc.short_description = _('Thumbnail PC')


    def delete(self, *args, **kwargs):
        r =super().delete(*args, **kwargs)
        try:
            os.remove(self.thumbnail.path)
        except:
            pass
        return r
    
    def __str__(self):
        return self.course_name_ar
    


class CourseLevel(models.Model):

    course          = models.ManyToManyField(Course, verbose_name=_('Course'))
    owner           = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

    thumnail        = models.ImageField(upload_to='course_level_images/' , verbose_name=_('Course Level Thumbnail'), blank=True, null=True)
    course_level_ar = models.CharField(max_length=100 , verbose_name=_('Course Level ar'))
    course_level_en = models.CharField(max_length=100 , verbose_name=_('Course Level en'))
    slug_field      = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug Field'), blank=True, null=True)


    is_active       = models.BooleanField(default=True, verbose_name=_('Is Active'))

    def show_thumbnail(self):
        if self.thumnail:
            return mark_safe( f"<img src='{self.thumnail.url}' width='300px' alt='{self.course_level_ar}'>")
        else: return None

    show_thumbnail.short_description = _('Thumbnail')

    def delete(self, *args, **kwargs):
        r =super().delete(*args, **kwargs)
        try:
            os.remove(self.thumnail.path)
        except:
            pass
        return r

    def get_course_level(self):
        lang = get_language()
        return self.course_level_ar if lang == 'ar' else self.course_level_en

    def save(self, *args, **kwargs):
        self.slug_field = slugify(self.course_level_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_level_ar
    
    class Meta:
        verbose_name = _('Course Level')
        verbose_name_plural = _('Course Levels')


class CourseType(models.Model):
    course          = models.ManyToManyField(Course, verbose_name=_('Course'))
    owner           = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

    course_type_ar  = models.CharField(max_length=100 , verbose_name=_('Course Type ar'))
    course_type_en  = models.CharField(max_length=100 , verbose_name=_('Course Type en'))


    is_active       = models.BooleanField(default=True, verbose_name=_('Is Active'))

    created_at      = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at      = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def save(self, *args, **kwargs):

        self.updated_at = datetime.datetime.now(pytz.timezone('Africa/Cairo'))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_type_ar
    

    class Meta:
        verbose_name = _('Course Type')
        verbose_name_plural = _('Course Types')

class CourseImages(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

    course_image = models.ImageField(upload_to='course_images/' , verbose_name=_('Course Image'))
    course_image_alt = models.CharField(max_length=100 , verbose_name=_('Course Image Alt'))

    def delete(self, *args, **kwargs):
        r =super().delete(*args, **kwargs)

        try:
            os.remove(self.course_image.path)
        except:
            pass

        return r


    def __str__(self):
        return self.course_image_alt
    
    class Meta:
        verbose_name = _('Course Image')
        verbose_name_plural = _('Course Images')





class Episode(models.Model):

     course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True , verbose_name=_('Course'),  related_name='episodes')
     owner  = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

     episode_name_ar = models.CharField(max_length=100 , verbose_name=_('Episode Name ar'))
     episode_name_en = models.CharField(max_length=100 , verbose_name=_('Episode Name en'))
    
     is_active       = models.BooleanField(default=True, verbose_name=_('Is Active'))



     
     episode_description_ar = models.TextField( verbose_name=_('Episode Description ar'))
     episode_description_en = models.TextField( verbose_name=_('Episode Description en'))
     students               = models.ManyToManyField(User, related_name='student', verbose_name=_('Students'), blank=True)
     video                  = models.FileField(
        upload_to='video/', verbose_name=_('Video'),
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv']),
            
            ])
     
     created_at      = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
     updated_at      = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

     start_date = models.DateField(verbose_name=_('Start Date'))
     end_date   = models.DateField(verbose_name=_('End Date'))

     expire_date = models.IntegerField(
         verbose_name=_('Expire Date'),
           null=True, blank=True,
            help_text=_('How many days to expire' )
     )

     def __str__(self):
         return self.episode_name_ar
     
     def delete(self, *args, **kwargs):
         r =super().delete(*args, **kwargs)
         try:
             os.remove(self.video)
         except:
             pass    
         return r

     class Meta:
         verbose_name = _('Episode')
         verbose_name_plural = _('Episodes')





