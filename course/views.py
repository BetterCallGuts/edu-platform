from django.shortcuts import render
from django.views.generic import TemplateView
from course.models import CourseLevel, Course, Episode


# Create your views here.


class LevelsView(TemplateView):
    template_name = "pages/levels.html"


    def get(self, req):
        levels = CourseLevel.objects.filter(is_active=True)
        context = {
            "levels" : levels,
            "header_courses" : "active",
        }
        return render(req,  self.template_name, context)



class CoursesView(TemplateView):
    template_name = "pages/courses.html"


    def get(self, req, slug):
        courses = Course.objects.filter(courselevel__slug_field=slug)
        print(courses)


        context = {
            "courses" : courses,
            "header_courses" : "active",
        }
        return render(req,  self.template_name, context)


class EpisodesView(TemplateView):
    template_name = "pages/episodes.html"


    def get(self, req, pk):
        course = Course.objects.get(pk=pk)
        episodes = Episode.objects.filter(course=course)
        print(episodes)


        context = {
            "episodes" : episodes,
            "header_courses" : "active",
        }

        return render(req,  self.template_name, context)
        
