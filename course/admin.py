from custom_admin.admin import admin_site
from .models import Course, CourseLevel, CourseType, Episode
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# Inlines
class LevelInline(admin.TabularInline):
    model = CourseLevel
    fk_name = 'course'
    extra = 0
    verbose_name = _('Level')
    verbose_name_plural = _('Levels')

class TypeInline(admin.TabularInline):
    model = CourseType
    fk_name = 'course'
    extra = 0
    verbose_name = _('Type')
    verbose_name_plural = _('Types')

class EpisodeInline(admin.TabularInline):
    model = Episode
    fk_name = 'course'
    extra = 0
    verbose_name = _('Episode')
    verbose_name_plural = _('Episodes')


# admin class
class CourseAdmin(ModelAdmin):

    list_display  = ["owner", "course_name_ar", "course_name_en",]
    # list_filter   = []
    # search_fields = ...

    inlines = [LevelInline, TypeInline, EpisodeInline]



# register
admin_site.register(Course, CourseAdmin)



