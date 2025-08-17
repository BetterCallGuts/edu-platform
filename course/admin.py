from custom_admin.admin import admin_site
from .models import Course, CourseLevel, CourseType, Episode,AboutTheCourse, SubscripedCourse, watchedepisods, Summary, QuizQuestion, QuizResult
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.utils import timezone

User = get_user_model()





def refresh_objects(modeladmin, request, queryset):
    for obj in queryset:
        obj.save()  
    modeladmin.message_user(request, f"{queryset.count()} objects refreshed successfully.")

refresh_objects.short_description = _("Refresh (re-save) selected objects")


@admin.action(description=_("Duplicate selected items"))
def duplicate_objects(modeladmin, request, queryset):
    for obj in queryset:
        obj.pk = None  # Reset the primary key
        obj.save()


# Filters
class CourseLevelFilter(admin.SimpleListFilter):
    title = _('Course Level')
    parameter_name = 'courselevel'

    def lookups(self, request, model_admin):
        lang = get_language()
        field = 'course_level_' + lang
        levels = CourseLevel.objects.values_list(field, flat=True).distinct()
        return [(level, level) for level in levels if level]

    def queryset(self, request, queryset):
        if self.value():
            lang = get_language()
            field = 'course_levels__course_level_' + lang
            return queryset.filter(**{field: self.value()})
        return queryset
# 
class CourseTypeFilter(admin.SimpleListFilter):
    title = _('Course Type')
    parameter_name = 'coursetype'

    def lookups(self, request, model_admin):
        lang = get_language()
        field = 'course_type_' + lang
        types = CourseType.objects.values_list(field, flat=True).distinct()
        return [(type_, type_) for type_ in types if type_]

    def queryset(self, request, queryset):
        if self.value():
            lang = get_language()
            field = 'course_types__course_type_' + lang
            return queryset.filter(**{field: self.value()})
        return queryset
# 
class CurrentlyAvailableFilter(admin.SimpleListFilter):
    title = _('Currently Available')
    parameter_name = 'currently_available'

    def lookups(self, request, model_admin):
        return [('yes', _('Yes')), ('no', _('No'))]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'yes':
            return queryset.filter(episode__start_date__lte=today, episode__end_date__gte=today).distinct()
        elif self.value() == 'no':
            return queryset.exclude(episode__start_date__lte=today, episode__end_date__gte=today).distinct()
        return queryset

class ExpiredEpisodesFilter(admin.SimpleListFilter):
    title = _('Has Expired Episodes')
    parameter_name = 'has_expired_episodes'

    def lookups(self, request, model_admin):
        return [('yes', _('Yes')), ('no', _('No'))]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        return {
            'yes': queryset.filter(episode__end_date__lt=today).distinct(),
            'no': queryset.filter(episode__end_date__gte=today).distinct(),
        }.get(self.value(), queryset)




# Inlines
class LevelInline(admin.TabularInline):
    model = CourseLevel.course.through
    extra = 0
    verbose_name = _('Level')
    verbose_name_plural = _('Levels')

class SummaryInline(admin.TabularInline):
    model = Summary
    extra = 0
    verbose_name = _('Summary')
    verbose_name_plural = _('Summaries')
class QuizResultInline(admin.TabularInline):
    model =  QuizResult
    extra = 0
    verbose_name = _('Quiz Result')
    verbose_name_plural = _('Quiz Results')
class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 0
    verbose_name = _('Quiz Question')
    verbose_name_plural = _('Quiz Questions')


class AboutTheCourseInline(admin.TabularInline):
    model = AboutTheCourse
    extra = 0
    verbose_name = _('About The Course')
    verbose_name_plural = _('About The Courses')

   

class TypeInline(admin.TabularInline):
    model = CourseType.course.through
    extra = 0
    verbose_name = _('Type')
    verbose_name_plural = _('Types')

    

class EpisodeInline(admin.StackedInline):
    model = Episode
    fk_name = 'course'
    extra = 0
    verbose_name = _('Episode')
    verbose_name_plural = _('Episodes')


# admin class
class CourseAdmin(ModelAdmin):

    list_display  = ["owner", "course_name_ar", "course_name_en", "show_thumbnail_pc", "show_thumbnail_mobile"]
    search_fields = ["course_name_ar", "course_name_en", "course_description_ar", "course_description_en", "owner__username", "owner__email"]
    list_filter   = [
        "owner", 
        "courselevel__course_level_ar", 
        "coursetype__course_type_ar", "coursetype__is_active"]

    fieldsets = [
        (None, {
            'fields': ('owner', 'course_name_ar', 'course_name_en', 'course_description_ar', 'course_description_en', 'slug', 'thumbnail_pc', 'thumbnail_mobile', 'is_active', )
        }),
        ("Pages", {
            'fields': ('info_background', 'title_background')
        }),
    ]

    actions = [
        duplicate_objects,
        refresh_objects,

        ]


    inlines = [LevelInline, TypeInline, EpisodeInline, AboutTheCourseInline]

class CourseLevelAdmin(ModelAdmin):
    list_display = ["get_courses", "owner", "show_thumbnail","course_level_ar", "course_level_en"]
    search_fields = ["course_level_ar", "course_level_en", "owner__username", "owner__email", "course__course_name_ar"]
    list_filter = ["owner", "course"]
    def get_courses(self, obj):
        return ", ".join([course.course_name_ar for course in obj.course.all()])
    get_courses.short_description = _('Courses')

class CourseTypeAdmin(ModelAdmin):
    list_display = ["course", "owner", "course_type_ar", "course_type_en", "is_active", "created_at", "updated_at"]
    search_fields = ["course_type_ar", "course_type_en", "owner__username", "owner__email", "course__course_name_ar"]
    list_filter = ["is_active", "owner", "course", "created_at", "updated_at"]
    date_hierarchy = "created_at"
# register
class EpisodeAdmin(ModelAdmin):
    list_display = ["course",  "episode_name_ar", "episode_name_en", "is_active", "created_at", "updated_at"]
    search_fields = ["episode_name_ar", "episode_name_en", "owner__username", "owner__email", "course__course_name_ar"]
    list_filter = ["is_active",  "course", "created_at", "updated_at"]
    
    actions = [
        refresh_objects,
        duplicate_objects,
    ]
    date_hierarchy = "created_at"
    inlines = [
        SummaryInline,
        QuizQuestionInline,
        QuizResultInline,
    ]



    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "students":

            if request.resolver_match.kwargs.get('object_id'):
                try:
                    episode_id = request.resolver_match.kwargs['object_id']
                    episode = Episode.objects.get(id=episode_id)
                    owner = episode.owner
                    kwargs["queryset"] = User.objects.filter(role='student', teacher=owner)
                except Episode.DoesNotExist:
                    kwargs["queryset"] = User.objects.none()
            else:
                
                kwargs["queryset"] = User.objects.filter(role='student')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

class QuizQuestionModelAdmin(admin.ModelAdmin):
    actions = [
        refresh_objects,
        duplicate_objects,
    
    ]



admin_site.register(Course, CourseAdmin)
admin_site.register(CourseLevel, CourseLevelAdmin)
admin_site.register(Episode, EpisodeAdmin)
admin_site.register(AboutTheCourse)
admin_site.register(SubscripedCourse)
admin_site.register(watchedepisods)
admin_site.register(Summary)
admin_site.register(QuizQuestion,  QuizQuestionModelAdmin)
admin_site.register(QuizResult)


