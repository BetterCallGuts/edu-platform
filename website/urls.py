from django.urls import path, include
from .views import landing, CustomLoginView,ForgotPasswordView, CustomLogoutView, CustomSignupView

app_name  = "website"

urlpatterns = [
    
  path('',                 landing,                                     name='landing'),
  path('signup/',           CustomSignupView.as_view(), name='signup'),
  path('login/',  CustomLoginView.as_view(),                            name='login'   ),
  path('logout/', CustomLogoutView.as_view(),                                 name='logout'  ),
  path('forgot_password/', ForgotPasswordView.as_view(),                name='forgot_password'  ),
  
]