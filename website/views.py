from django.shortcuts import render
from django.contrib import messages
from course.models  import Course

def landing(req):

    courses = Course.objects.all()

    context = {
        "courses" : courses,
    }

    return render(req, "pages/landing.html", context)