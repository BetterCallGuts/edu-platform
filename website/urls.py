from django.urls import path, include
from .views import landing, CustomLoginView,ForgotPasswordView, CustomLogoutView

app_name  = "website"

urlpatterns = [
    
  path('',                 landing,                                     name='landing'),
  path('login/',  CustomLoginView.as_view(),                            name='login'   ),
  path('logout/', CustomLogoutView.as_view(),                                 name='logout'  ),
  path('forgot_password/', ForgotPasswordView.as_view(),                name='forgot_password'  ),
  
]