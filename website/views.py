from django.shortcuts import render
from django.contrib import messages
from course.models  import Course, CourseLevel
# from django.contrib.auth.views import 
from django.views.generic      import TemplateView
from django.contrib.auth       import login as auth_login
from django.utils.translation  import gettext_lazy as _
from django.contrib.auth.views import  LogoutView, LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth       import get_user_model
from django.urls               import reverse_lazy

User = get_user_model()


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs): 
        messages.add_message(request, messages.INFO, _("You have been logged out."))
        return super().post(request, *args, **kwargs)

# 
class CustomLoginView(LoginView):
    template_name = 'pages/login.html'
    def post(self, request, *args, **kwargs):
        # messages.add_message(request, messages.INFO, _("Please enter a correct username and password. Note that both fields are case-sensitive."))
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):

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
    form_class    = UserCreationForm
    model         = User



def landing(req):

    courses = Course.objects.all()
    # levels  = CourseLevel.objects.filter(is_active=True, owner="")    

    context = {
        "courses" : courses,
        
    }

    return render(req, "pages/landing.html", context) 


class ForgotPasswordView(TemplateView):

    def get(self, req):


        return render(req, "pages/forgot_password.html")