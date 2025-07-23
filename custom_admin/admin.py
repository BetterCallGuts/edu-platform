from django.contrib.admin.sites import AdminSite

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings


User = get_user_model()

class MyAdminSite(AdminSite):
    site_header = settings.SITE_HEADER
    site_title  = settings.SITE_TITLE
    index_title = settings.SITE_INDEX_TITLE

# INITIALIZE ADMIN
admin_site = MyAdminSite()


# class StudentInline(admin.TabularInline):
#     model = User
#     fk_name = 'teacher'
#     extra = 0
#     verbose_name = "Student"

# class UserAdmin(BaseUserAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.role == 'teacher':
#             return qs.filter(teacher=request.user)
#         return qs

#     def has_module_permission(self, request):
#         if request.user.role == 'teacher':
#             return True
#         return super().has_module_permission(request)

#     def get_inline_instances(self, request, obj=None):
#         if request.user.role == 'teacher':
#             return [StudentInline(self.model, self.admin_site)]
#         return super().get_inline_instances(request, obj)

# admin.site.register(User, UserAdmin)