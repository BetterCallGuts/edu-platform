from django.urls import path, include
from .views import( landing,
  CustomLoginView,ForgotPasswordView,
    CustomLogoutView, CustomSignupView,
      TeacherView, LevelView, CourseView,
        EpisodeView, ProfileView,
          PasswordResetView, SubscriptedCoursesView,
            CourseViewFromProfile,
              SubscriptedPackagesView, TeachersView, 
      SubscribeCoursesView, chatbot_view,
      TOSView
)
app_name  = "website"

urlpatterns = [
    
  path('',                 landing.as_view(),                                                                          name='landing'),
  path('signup/',           CustomSignupView.as_view(),                                                                name='signup'),
  path('login/',  CustomLoginView.as_view(),                                                                           name='login'   ),
  path('logout/', CustomLogoutView.as_view(),                                                                          name='logout'  ),
  path('forgot_password/', ForgotPasswordView.as_view(),                                                               name='forgot_password'  ),
  path('profile/update-profile/', ProfileView.as_view(),              name='profileview' ),
  path("profile/reset-password/" , PasswordResetView.as_view(),                                                        name='reset_password'  ),
  path("profile/subscribed-courses/" , SubscriptedCoursesView.as_view(),                                               name='subscriped_courses'  ),



  path("teachers",         TeachersView.as_view(),                                                          name='teachers'  ),
  path('teacher/<slug:slug>/',         TeacherView.as_view(),                                                          name='teacher'  ),
  path('teacher/courses/<slug:slug>/',         LevelView.as_view(),                                                    name='courses'  ),
  path('teacher/course/<slug:slug>/',         CourseViewFromProfile.as_view(),                                         name='courseviewfromprofile'  ),
  path('teacher/courses/<slug:level_slug>/course/<slug:course_slug>/',         CourseView.as_view(),                   name='course'  ),
  path('teacher/courses/<slug:level_slug>/course/<slug:course_slug>/episode/<slug:ep_slug>',         EpisodeView.as_view(),   name='ep'  ),
  

  path('subscribe/<slug:slug>', SubscribeCoursesView.as_view(), name='subscrbecourse'),
  path('subscribe/packages/<slug:slug>/', SubscriptedPackagesView.as_view(), name='subscrbecourses'),

  path('tos', TOSView.as_view(), name='tos'),
  # AI
  path("chatbot/ask/", chatbot_view, name="chatbot-ask")
]