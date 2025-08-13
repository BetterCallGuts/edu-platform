from django.urls import path, include
from .views import landing, CustomLoginView,ForgotPasswordView, CustomLogoutView, CustomSignupView, TeacherView, CourseView

app_name  = "website"

urlpatterns = [
    
  path('',                 landing.as_view(),                                     name='landing'),
  path('signup/',           CustomSignupView.as_view(), name='signup'),
  path('login/',  CustomLoginView.as_view(),                            name='login'   ),
  path('logout/', CustomLogoutView.as_view(),                                 name='logout'  ),
  path('forgot_password/', ForgotPasswordView.as_view(),                name='forgot_password'  ),
  path('teacher/<slug:slug>/',         TeacherView.as_view(),                              name='teacher'  ),
  path('teacher/courses/<slug:slug>/',         CourseView.as_view(),                              name='courses'  ),
  
]