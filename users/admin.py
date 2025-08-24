
from custom_admin.admin import admin_site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from course.admin import duplicate_objects, refresh_objects
from course.models import SubscripedCourse, Course
from django.contrib import admin
from .models import PackageSubscribe, PaymentMethodPackage, PaymentMethodUser, LiveStream , AccessCourseRequest, AccessPackageRequest, WhyChooseUser

from django.utils.translation import gettext_lazy as _
from django.contrib import messages

User = get_user_model()

# actions

def grant_access(modeladmin, request, queryset):
    for obj in queryset:
        if  SubscripedCourse.objects.filter(
            course=obj.course,
              user=obj.user
              ).exists():
            continue
        
        o = SubscripedCourse.objects.create(
            course=obj.course,
              user=obj.user)
        
        o.save()

        messages.success(request, f"{obj.course.get_course_language()} Subscribed Successfully")
        
grant_access.short_description = "Subscribe"

def grant_package_access(modeladmin, request, queryset):
    for obj in queryset:
        for teacher in obj.teacher.all():
            
            courses = Course.objects.filter(owner=teacher)
            for course in courses:
                if SubscripedCourse.objects.filter(user=obj.user,  course=course).exists():
                    continue
                o = SubscripedCourse.objects.create(course=course, user=obj.user)
                o.save()
    messages.success(request, _("Access Granted Successfully"))

class PaymentMethodInline(admin.StackedInline):
    model = PaymentMethodUser
    extra = 0
    verbose_name = _('Payment Method')
    verbose_name_plural = _('Payment Methods')

class WhyChooseUserInline(admin.StackedInline):
    model = WhyChooseUser
    extra = 0
    verbose_name = _('Why Choose User')
    verbose_name_plural = _('Why Choose User points')



class PaymentMethodPackageInline(admin.StackedInline):
    model = PaymentMethodPackage
    extra = 0
    verbose_name = _('Payment Method')
    verbose_name_plural = _('Payment Methods')



class UserAdmin(BaseUserAdmin):
    
    list_display = BaseUserAdmin.list_display 
    list_filter = BaseUserAdmin.list_filter +     ('role', 'student_limit')
    # print(BaseUserAdmin.fieldsets,  [None, {'fields': ('role', 'student_limit')}] )
    fieldsets = list(BaseUserAdmin.fieldsets) +         [("system", {
        'fields': ('phone','role', 'student_limit', "teacher", "slug")
 })] +     [("page", {'fields': (
          'thumbnail',
            'first_section',
              'text_in_picture',
                "text_below",
                  "second_section",
                    "third_section",
                      "fourth_section",
                        "social_background",
                          "instgram_link",
                          "instgram_icon",
                            "facebook_link",
                            "facebook_icon",
                              "youtube_link",
                                "youtube_icon",
                                 "in_main_page",
                                    "name_ar",
                                  )})]       
    search_fields = BaseUserAdmin.search_fields + ('role', 'student_limit', 'phone')
    actions = [
        refresh_objects,
        duplicate_objects,
    ]

    inlines = [
        
        WhyChooseUserInline,
        PaymentMethodInline]

    def get_list_display(self, request):
        base_fields = super().get_list_display(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return base_fields + ('role', 'student_limit')
        return base_fields
    def get_fieldsets(self, request, obj = ...):
        
        r =  super().get_fieldsets(request, obj)

        if request.user.is_superuser or request.user.role == 'admin':
            return r
        return r[0:2]+ r[3:4]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        
        elif request.user.role == 'teacher':
            return qs.filter(teacher=request.user)
        return qs.none()  

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'admin':
            return super().get_readonly_fields(request, obj)
        return self.readonly_fields + ('role', 'teacher', 'student_limit')


    def save_model(self, request, obj, form, change):

        if not request.user.is_superuser and not request.user.role == 'admin':
            obj.role = form.initial.get('role')
            obj.teacher = form.initial.get('teacher')
            obj.student_limit = form.initial.get('student_limit')

        if request.user.role == 'teacher' and not obj.teacher and obj.role == 'student':
            obj.teacher = request.user
        
        # if request.user.role == "teacher" and obj.role == 'student':

        super().save_model(request, obj, form, change)

    

    def get_role_opetions(self, request):
        pass


class GroupAdmin(BaseGroupAdmin):
    pass

class PackageSubscribeAdmin(admin.ModelAdmin):
    
    
    inlines = [PaymentMethodPackageInline]

class PaymentMethodUserModelAdmin(admin.ModelAdmin):
    pass

class PaymentMethodPackageModelAdmin(admin.ModelAdmin):
    pass

class LiveStreamAdmin(admin.ModelAdmin):
    pass
class AccessCourseRequestAdmin(admin.ModelAdmin):
    
    list_display = [
        "user",
        "access_granted",
        "course",
        "account_info",
        "show_screen_shot",
        "created_at",
    ]
    list_filter = [
        "user",
        "course",
        "created_at",
    ]
    search_fields = [
        "user",
        "course",
        "account_info",
    ]
    actions = [
        grant_access,
    ]

    def access_granted(self, obj):

        if SubscripedCourse.objects.filter(user=obj.user, course=obj.course).exists():
            return True
        return False
    
    access_granted.short_description = _("Access Granted")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        if request.user.role == 'assistant':
            return qs.filter(teacher=request.user.teacher)
        return qs.filter(teacher=request.user)

class AccessPackageRequestAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "package",
        # "access_granted",
        "created_at",
    ]
    list_filter = [
        "user",
        "package",
        "created_at",
    ]
    search_fields = [
        "user",
        "package",
        "account_info",
    ]
    actions = [

    ]

    def access_granted(self, obj):

        if SubscripedCourse.objects.filter(user=obj.user, course=obj.course).exists():
            return True
        return False
    
    access_granted.short_description = _("Access Granted")


admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(PackageSubscribe, PackageSubscribeAdmin)
admin_site.register(PaymentMethodUser , PaymentMethodUserModelAdmin)
admin_site.register(PaymentMethodPackage , PaymentMethodPackageModelAdmin)
admin_site.register(LiveStream , LiveStreamAdmin)
admin_site.register(AccessCourseRequest , AccessCourseRequestAdmin)

admin_site.register(AccessPackageRequest , AccessPackageRequestAdmin)