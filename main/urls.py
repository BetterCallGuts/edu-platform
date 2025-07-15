from django.urls import path, include
from custom_admin.admin import admin_site
from django.conf.urls.i18n import i18n_patterns




urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # enable POST language switch
]
urlpatterns += i18n_patterns(
    path('admin/', admin_site.urls),
)
