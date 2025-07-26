from django.urls import path
from . import views


app_name  = "course"

urlpatterns = [


    path('', views.LevelsView.as_view(), name="levels"),
    path('levels/<slug:slug>/', views.CoursesView.as_view(), name="courses"),
    path('course/<int:pk>/', views.EpisodesView.as_view(), name="episodes"), 
    
    
]