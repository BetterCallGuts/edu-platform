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


from datetime import timedelta

User = get_user_model()

def default_end_date():
    return timezone.now().date() + timedelta(days=7)

class Course(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE ,
                              
                              
                               verbose_name=_('Owner'),
                               related_name='courses'
                               
                               )

    

    course_name_ar = models.CharField(max_length=100 , verbose_name=_('Course Name ar'))
    course_name_en = models.CharField(max_length=100 , verbose_name=_('Course Name en'))


    thumbnail_pc     = models.ImageField(upload_to='course_images/' , verbose_name=_('Course Thumbnail'), blank=True, null=True)
    thumbnail_mobile = models.ImageField(upload_to='course_images/' , verbose_name=_('Course Thumbnail'), blank=True, null=True)
    is_active        = models.BooleanField(default=True, verbose_name=_('Is Active'))  

    course_description_ar = models.TextField( verbose_name=_('Course Description ar')  )
    course_description_en = models.TextField( verbose_name=_('Course Description en')  )
    
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug Field'), blank=True, null=True)

    # pages
    info_background  = models.ImageField(upload_to='course_images/' , verbose_name=_('Course Info Background'), blank=True, null=True)
    title_background = models.ImageField(upload_to='course_images/' , verbose_name=_('Course title in'), blank=True, null=True)
        
    cost             = models.FloatField(default=0, verbose_name=_('Cost'))
    currency         = models.CharField(max_length=10, default='EGP', verbose_name=_('Currency'))
    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)

        self.slug = slugify(f"{self.course_name_en}-{self.pk}", )
        super().save(*args, **kwargs)



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

        return f"{self.get_course_language()} - {self.owner.username} - {self.slug}"
    


class CourseLevel(models.Model):

    course          = models.ManyToManyField(Course, verbose_name=_('Course'))
    owner           = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

    thumnail        = models.ImageField(upload_to='course_level_images/' , verbose_name=_('Course Level Thumbnail'), blank=True, null=True)
    course_level_ar = models.CharField(max_length=100 , verbose_name=_('Course Level ar'))
    course_level_en = models.CharField(max_length=100 , verbose_name=_('Course Level en'))
    slug_field      = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug Field'), blank=True, null=True)

    description_ar = models.TextField(verbose_name=_('Course Level Description ar'))
    description_en = models.TextField(verbose_name=_('Course Level Description en'))

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

    def get_description(self):
        lang = get_language()
        return self.description_ar if lang == 'ar' else self.description_en
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        self.slug_field = slugify(self.course_level_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_level_ar}" + f"{self.owner.username}"
    
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
    #  owner  = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

     episode_name_ar = models.CharField(max_length=100 , verbose_name=_('Episode Name ar'))
     episode_name_en = models.CharField(max_length=100 , verbose_name=_('Episode Name en'))
    
     is_active       = models.BooleanField(default=True, verbose_name=_('Is Active'))



     
     episode_description_ar = models.TextField( verbose_name=_('Episode Description ar'))
     episode_description_en = models.TextField( verbose_name=_('Episode Description en'))

     video                  = models.FileField(
        upload_to='video/', verbose_name=_('Video'),
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv']),
            
            ])
     
     created_at      = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
     updated_at      = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

     start_date = models.DateField(verbose_name=_('Start Date') , default=timezone.now)
     end_date   = models.DateField(verbose_name=_('End Date') , default=default_end_date)
     duration_hours = models.FloatField(
         blank=True, null=True,
         default=0,
         verbose_name=_('Duration Hours'),
         help_text=_('By hours')
         )  
     expire_date = models.IntegerField(
         verbose_name=_('Expire Date'),
           null=True, blank=True,
            help_text=_('How many days to expire' )
     )
     slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug Field'), blank=True, null=True)

     def __str__(self):
         return self.get_episode_name()
     def get_episode_name(self):
         
         lang = get_language()
         return self.episode_name_ar if lang == 'ar' else self.episode_name_en
     def get_episode_description(self):
         lang = get_language()
         return self.episode_description_ar if lang == 'ar' else self.episode_description_en
     def delete(self, *args, **kwargs):
         r =super().delete(*args, **kwargs)
         try:
             os.remove(self.video)
         except:
             pass    
         return r
     def save(self, *args, **kwargs):

        if self.pk is None:
            super().save(*args, **kwargs)   
        
        
        self.slug = slugify(f"{self.course.course_name_en if self.course else ''}-{self.episode_name_en if self.episode_name_en else ''}-{self.pk}", )
        r = super().save(*args, **kwargs)  

        return r

        
     class Meta:
         verbose_name = _('Episode')
         verbose_name_plural = _('Episodes')





class AboutTheCourse(models.Model):
    level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE , verbose_name=_('Course'), related_name='about_the_courses')
    # owner  = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name=_('Owner'))

    about_the_course_ar = models.TextField( verbose_name=_('About The Course ar'))
    about_the_course_en = models.TextField( verbose_name=_('About The Course en'))

    created_at      = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at      = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.get_about_the_course()

    def get_about_the_course(self):
        lang = get_language()
        return self.about_the_course_ar if lang == 'ar' else self.about_the_course_en

    class Meta:
        verbose_name = _('About The Course')
        verbose_name_plural = _('About The Courses')



class SubscripedCourse(models.Model):
    course          = models.ForeignKey(Course, on_delete=models.CASCADE , verbose_name=_('Course'), related_name='subscriped_courses')
    user            = models.ForeignKey(User,   on_delete=models.CASCADE , verbose_name=_('Owner'), related_name='subscriped_courses')
    is_active       = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at      = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))


    def __str__(self):
        return self.course.get_course_language() 
    class Meta:
        verbose_name = _('Subscriped Course')
        verbose_name_plural = _('Subscriped Courses')

class watchedepisods(models.Model):
    episod          = models.ForeignKey(Episode, on_delete=models.CASCADE , verbose_name=_('Course'), related_name='watchedepisodes')
    user            = models.ForeignKey(User,   on_delete=models.CASCADE , verbose_name=_('Owner'))

    created_at      = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at      = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.episod.episode_name_ar if self.episod else self.user.username + "  Watch Ep REport"
    
    class Meta:
        verbose_name = _('Watched Episode')
        verbose_name_plural = _('Watched Episodes')




class Summary(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="summaries", verbose_name=_("Episode"))
    title_ar = models.CharField(max_length=200, verbose_name=_("Title ar"))
    title_en = models.CharField(max_length=200, verbose_name=_("Title en"))

    file = models.FileField(
        upload_to="summaries/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        verbose_name=_("PDF File")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_summary(self):
        lang = get_language()
        return self.title_ar if lang == 'ar' else self.title_en

    def __str__(self):
        return self.get_summary()
    class Meta:
        verbose_name = _("Summary")
        verbose_name_plural = _("Summaries")

class QuizQuestion(models.Model):

    ch = [
        ("1", _("First Choice" )),
        ("2", _("Second Choice")),
        ("3", _("Third Choice" )),
        ("4", _("Fourth Choice")),
    ]

    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="questions", verbose_name=_("Episode"))

    title_ar = models.CharField(max_length=200, verbose_name=_("Title ar"))
    title_en = models.CharField(max_length=200, verbose_name=_("Title en"))

    question_1_ar = models.TextField(verbose_name=_("Question 1 ar"))
    question_1_en = models.TextField(verbose_name=_("Question 1 en"))
    question_2_ar = models.TextField(verbose_name=_("Question 2 ar"))
    question_2_en = models.TextField(verbose_name=_("Question 2 en"))
    question_3_ar = models.TextField(verbose_name=_("Question 3 ar"))
    question_3_en = models.TextField(verbose_name=_("Question 3 en"))
    question_4_ar = models.TextField(verbose_name=_("Question 4 ar"))
    question_4_en = models.TextField(verbose_name=_("Question 4 en"))
    answer        = models.CharField(max_length=200, verbose_name=_("Answer"), choices=ch)

    created_at = models.DateTimeField(auto_now_add=True)
    def get_question_1(self):
        lang = get_language()
        return self.question_1_ar if lang == 'ar'and self.question_1_ar else self.question_1_en

    def get_question_2(self):
        lang = get_language()
        return self.question_2_ar if lang == 'ar' and self.question_2_ar else self.question_2_en

    def get_question_3(self):
        lang = get_language()
        return self.question_3_ar if lang == 'ar' and self.question_3_ar else self.question_3_en

    def get_question_4(self):
        lang = get_language()
        return self.question_4_ar if lang == 'ar' and self.question_4_ar else self.question_4_en

    def get_question(self):
        lang = get_language()
        return self.title_ar if lang == 'ar' else self.title_en

    def __str__(self):
        return self.get_question()
    class Meta:
        verbose_name = _("Quiz Question")
        verbose_name_plural = _("Quiz Questions")

class QuizResult(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_results")
    episode   = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="results")
    answers   = models.TextField(verbose_name=_("Answers"), )
    score     = models.IntegerField(default=0, verbose_name=_("Score"))
    total     = models.IntegerField(default=0, verbose_name=_("Total Questions"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Quiz Result")
        verbose_name_plural = _("Quiz Results")

    def __str__(self):
        return f"{self.user.username} - {self.episode.get_episode_name()} ({self.score}/{self.total})"
