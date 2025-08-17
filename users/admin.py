
from custom_admin.admin import admin_site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from course.admin import duplicate_objects, refresh_objects

from django.contrib import admin
from .models import PackageSubscribe, PaymentMethod, LiveStream




User = get_user_model()


class UserAdmin(BaseUserAdmin):
    
    list_display = BaseUserAdmin.list_display 
    list_filter = BaseUserAdmin.list_filter +     ('role', 'student_limit')
    # print(BaseUserAdmin.fieldsets,  [None, {'fields': ('role', 'student_limit')}] )
    fieldsets = list(BaseUserAdmin.fieldsets) +         [("system", {
        'fields': ('phone','role', 'student_limit', "teacher", "slug")
 })] +     [("page", {'fields': ('first_section', 'text_in_picture', "text_below", "second_section", "third_section", "fourth_section", "social_background", "instgram_link","instgram_icon", "facebook_link","facebook_icon", "youtube_link", "youtube_icon")})]       
    search_fields = BaseUserAdmin.search_fields + ('role', 'student_limit', 'phone')
    actions = [
        refresh_objects,
        duplicate_objects,
    ]

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
    pass

class PaymentMethodAdmin(admin.ModelAdmin):
    pass

class LiveStreamAdmin(admin.ModelAdmin):
    pass

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(PackageSubscribe, PackageSubscribeAdmin)
admin_site.register(PaymentMethod , PaymentMethodAdmin)
admin_site.register(LiveStream , LiveStreamAdmin)