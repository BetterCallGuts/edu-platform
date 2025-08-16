from django.shortcuts import render
from django.contrib import messages
from course.models  import Course, CourseLevel, SubscripedCourse, Episode
# from django.contrib.auth.views import 
from django.views.generic      import TemplateView
from django.contrib.auth       import login as auth_login
from django.utils.translation  import gettext_lazy as _
from django.contrib.auth.views import  LogoutView, LoginView
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from django.contrib.auth       import get_user_model
from django.urls               import reverse_lazy
from django.db.models import Sum

User = get_user_model()

class ForgotPasswordView(TemplateView):

    def get(self, req):
        return render(req, "pages/forgot_password.html")

class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs): 
        messages.add_message(request, messages.INFO, _("You have been logged out."))
        return super().post(request, *args, **kwargs)

# 
class CustomLoginView(LoginView):
    template_name = 'pages/login.html'
    def post(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)


    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return super().form_invalid(form)
    

    def form_valid(self, form):

        messages.success(self.request, _(f"Welcome {form.get_user().username}!"))
        auth_login(self.request, form.get_user())
        remember_me = self.request.POST.get('remember_me') == 'on'
        if not remember_me:

            self.request.session.set_expiry(0) 
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 30)  #30 days
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_login'] = "active"
        return context
# 
class CustomSignupView(CreateView):
    template_name = 'pages/signup.html'
    form_class    = SignUpForm
    model         = User
    success_url   = reverse_lazy('website:login')
    def form_invalid(self, form):

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, _("Account created successfully! Please log in."))
        return super().form_valid(form)


class landing(TemplateView):

    def get(self, req):

        courses = Course.objects.filter(is_active=True)
        teachers = []
        f_courses = []
        for i in courses:
        
            if i.owner in teachers:
                    continue
            teachers.append(i.owner)
            f_courses.append(i)



        

        context = {
            "courses" : courses,
            
        }

        return render(req, "pages/landing.html", context) 



class TeacherView(TemplateView):
    template_name = "pages/teacher.html"
    def get(self, req, slug):

       course = Course.objects.get(slug=slug)
       teacher = course.owner
       courses = CourseLevel.objects.filter(owner=teacher)
       
       
       context = {
           "teacher"  : teacher,
           "courses"  : courses,

       }
       return render(req,  self.template_name, context)




class LevelView(TemplateView):
    template_name = "pages/courses.html"
    def get(self, req, slug):

       level = CourseLevel.objects.get(slug_field=slug)
       course = level.course
       teacher = level.owner
       courses = level.course.all()

       how_many_ep = 0
       result = 0
       duration = 0
       for i in courses:
           episodes = i.episodes.all()
           for j in episodes:
               duration  += j.duration_hours
           how_many_ep += episodes.count()


       how_many_students = SubscripedCourse.objects.filter(course__in=level.course.all()).count()
    #    sum_hours         = course.episodes.aggregate(Sum('duration_hours'))
       course_hours      =  duration
       course_hours      = course_hours if course_hours else 0
       context = {
           "teacher"  : teacher,
           "course"  : course,
           "courses"  : courses,
           "hms"      : how_many_students,
           "hme"      : how_many_ep,
           'ch'       :int(course_hours  ),
           "level_slug" : level.slug_field,

       }
       return render(req,  self.template_name, context)
    


class CourseView(TemplateView):
    template_name = "pages/course.html"
    def get(self, req, level_slug, course_slug):
        # course = Course.objects.get(slug=slug)
        level = CourseLevel.objects.get(slug_field=level_slug)
        course = Course.objects.get(slug=course_slug)
        epS    = Episode.objects.filter(course=course)

        context = {
            'course'  : course,
            'epS'     : epS,
            'level'   : level,
            "teacher"  : course.owner,
        }



        return render(req,  self.template_name, context)


class  EpisodeView(TemplateView):
    template_name = "pages/ep.html"

    def get(self, req, level_slug, course_slug, ep_slug):


        course = Course.objects.get(slug=course_slug)
        level = CourseLevel.objects.get(slug_field=level_slug)
        ep = Episode.objects.get(slug=ep_slug)
        teacher = course.owner
        context = {
            'course'  : course,
            'ep'      : ep,
            'level'   : level,
            "teacher"  : course.owner,
        }

        return render(req,  self.template_name, context)