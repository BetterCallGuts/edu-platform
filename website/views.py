from django.shortcuts import render, redirect
from django.contrib import messages
from course.models  import Course, CourseLevel, SubscripedCourse, Episode, QuizQuestion, QuizResult
# from django.contrib.auth.views import 
from django.views.generic      import TemplateView
from django.contrib.auth       import login as auth_login
from django.utils.translation  import gettext_lazy as _
from django.contrib.auth.views import  LogoutView, LoginView
from .forms import SignUpForm, ProfileUpdateForm, UserSearchForm
from django.views.generic.edit import CreateView
from django.contrib.auth       import get_user_model
from django.urls               import reverse_lazy
from django.db.models import Sum
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
User = get_user_model()
from django.contrib.auth.forms import PasswordChangeForm
from users.models import PackageSubscribe, PaymentMethodUser, PaymentMethodPackage, AccessCourseRequest, AccessPackageRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import os
import pdfplumber
import PyPDF2

import google.generativeai as genai
from django.utils.translation import get_language

def extract_text_from_pdf(file_path):
    text = ""

    # Try pdfplumber first
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():  # If we got something, return it
            return text
    except Exception as e:
        print(f"[pdfplumber failed] {e}")

    # Fallback to PyPDF2
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except Exception as e:
        print(f"[PyPDF2 failed] {e}")

    return ""  # If both fail
genai.configure(api_key="AIzaSyDZz60t1T1S05sELojH9gcxnAAYPjKp-k8")
model = genai.GenerativeModel("gemini-1.5-flash")









class SubscriptedCoursesView(TemplateView):
    template_name = "pages/subscriped_courses.html"

    def get(self, req):

        subcourses = SubscripedCourse.objects.filter(
                    user=req.user,
                    is_active=True
            )
        

        context = {
            "subcourses" : subcourses,
        }

        return render(
            req,
            self.template_name,
            context
)


class PasswordResetView(TemplateView):
    template_name = "pages/password.html"
    def get(self, req):
        form = PasswordChangeForm(req.user)
        return render(req, self.template_name, {"form": form})
    
    def post(self, req):
        form = PasswordChangeForm(req.user, req.POST)

        if form.is_valid():
            form.save()
            messages.success(req, _("Your password has been changed successfully."))
            return redirect("website:login")
        else:
            messages.error(req, _("Please correct the errors below."))

        return render(req, self.template_name, {"form": form})

@method_decorator(
    login_required, name="dispatch"
    )
class ProfileView(TemplateView):

    template_name = "pages/profile.html"

    def get(self, req):

        form = ProfileUpdateForm(instance=req.user, user=req.user)

        return render(req,  self.template_name,{"form" : form} )


    def post(self, request):
        form = ProfileUpdateForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your profile has been updated successfully."))
            return redirect("website:profileview")
        else:
            messages.error(request, _("Please correct the errors below."))
        return render(request, self.template_name, {"form": form})

class ForgotPasswordView(TemplateView):

    def get(self, req):
        return render(req, "pages/forgot_password.html")

class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs): 
        messages.add_message(request, messages.INFO, _("You have been logged out."))
        return super().post(request, *args, **kwargs)



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
        teachers = User.objects.filter(role='teacher', in_main_page=True)
        students = User.objects.filter(role='student').count()
        epS      = Episode.objects.filter(course__in=courses)
        # teachers = []
        # f_courses = []
        # for i in courses:
        
        #     if i.owner in teachers:
        #             continue
        #     teachers.append(i.owner)
        #     f_courses.append(i)



        

        context = {
            "courses" : courses,
            'teachers' :teachers,
            "epS"       : epS,
            "students"  : students,
        }

        return render(req, "pages/landing.html", context) 



class TeachersView(TemplateView):
    template_name = "pages/teachers.html"
    def get(self, req):
        q    = req.GET.get("q")
        results = User.objects.filter(role='teacher')
        context = {}
        if q:
            context["q"] = q

            query = q

            if query:
                results = results.filter(
                    Q(username__icontains=query) |
                    Q(name_ar__icontains=query)
                ).distinct()

  
        context["teachers"] = results
        return render(req, self.template_name, context)

class TeacherView(TemplateView):
    template_name = "pages/teacher.html"
    def get(self, req, slug):

       try:
        teacher = User.objects.get(slug=slug)
        courses = CourseLevel.objects.filter(owner=teacher)
        result = 0

        for i in teacher.courses.all() :
            result += i.episodes.count()
       except Exception as e:

        messages.error(req, _("Teacher not found"))
        return redirect("website:landing") 
       
       context = {
           "teacher"  : teacher,
           "courses"  : courses,
           "hme"      : result,

       }
       return render(req,  self.template_name, context)



class TOSView(TemplateView):
    template_name = "pages/tos.html"
    def get(self, req):
        from .models import GlobalVars
        language_code = get_language()
        if language_code == 'ar':
            tos = GlobalVars.objects.filter(Key="tos_ar").first()
        else:
            tos = GlobalVars.objects.filter(Key="tos_en").first()

        context = {
            "tos": tos.Value if tos else ""
        }
        return render(req, self.template_name,context )



class LevelView(TemplateView):
    template_name = "pages/courses.html"
    def get(self, req, slug):

       level = CourseLevel.objects.get(slug_field=slug)
       teacher = level.owner
       courses = level.course.all()

       how_many_ep = 0

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
            "level"  : level,
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
        result = 0
        print("test test")
        if req.user.is_authenticated:
            subscribed = req.user.subscriped_courses.filter(course=course, is_active=True)
            print(subscribed)
            if subscribed.count() :
                for ep in epS:
                    result += ep.results.filter(user=req.user).count()
                result = result if result else 0
                result = result/epS.count() * 100
                print(result)
            else:
                subscribed = False
        else:
            subscribed = False
        context = {
            'course'  : course,
            'epS'     : epS,
            'level'   : level,
            "teacher"  : course.owner,
            "subscribed" : subscribed,
            "result"  : result,
        }



        return render(req,  self.template_name, context)


class  EpisodeView(TemplateView):
    template_name = "pages/ep.html"

    def get(self, req, level_slug, course_slug, ep_slug):

        course = Course.objects.get(slug=course_slug)
        if req.user.is_authenticated:
            sb = SubscripedCourse.objects.filter(user=req.user, course=course)
            if sb.count() == 0:
                messages.info(req, _("You have not subscribed to this course."))
                return redirect("website:subscrbecourse", slug=course_slug)
        else:
            messages.info(req, _("Please login to access this page."))
            return redirect("website:login")

        level = CourseLevel.objects.get(slug_field=level_slug)
        ep = Episode.objects.get(slug=ep_slug)
        teacher = course.owner
        context = {
            'course'  : course,
            'ep'      : ep,
            'level'   : level,
            "teacher"  : teacher,
        }
        try:
            qr = QuizResult.objects.get(user=req.user, episode=ep)
            parsed = json.loads(qr.answers)
            context['answers'] = parsed
            context['score'] = qr.score
            context['total'] = qr.total
            context['per'] = int(round(qr.score / qr.total * 100))

        except:

            pass

        return render(req,  self.template_name, context)
    
    def post(self, req, level_slug, course_slug, ep_slug):
        course = Course.objects.get(slug=course_slug)
        level = CourseLevel.objects.get(slug_field=level_slug)
        ep = Episode.objects.get(slug=ep_slug)
        teacher = course.owner
        try:
            QuizResult.objects.get(user=req.user, episode=ep)

            return self.get(req, level_slug, course_slug, ep_slug)
        except Exception as e:
            print( e)
            pass
        dic = dict(req.POST)
        dic.pop("csrfmiddlewaretoken")
        # print(dic)
        results = []
        score = 0

        for key, value in dic.items():
            qid = int(key)
            ans = int(value[0])
            question = QuizQuestion.objects.get(pk=qid)

            is_correct = (ans == int(question.answer))
            if is_correct:
                score += 1

            results.append({
                "qn": str(qid),
                "ans": str(ans),
                "correct": str(question.answer)
            })

        qr = QuizResult.objects.create(
            user=req.user,
            episode=ep,
            score=score,
            answers=json.dumps(results),  # store as JSON
            total=len(dic),
        )
        qr.save()

        cleaned = [a for a in qr.answers.split(",") if a]

        parsed = json.loads(qr.answers)

        per = int(round(qr.score / qr.total * 100))
        context = {
            'course'  : course,
            'ep'      : ep,
            'level'   : level,
            "teacher"  : teacher,
            'answers' : parsed,
            'score'   : qr.score,
            'total'   : qr.total,
            'per'     : per,
        }

        return render(req,  self.template_name, context)



class CourseViewFromProfile(TemplateView):
    template_name = "pages/course.html"
    def get(self, req, slug):

        course = Course.objects.get(slug=slug)
        level = CourseLevel.objects.filter(course=course).first()
        view = CourseView.get(self, req, level.slug_field, course.slug)
        return view








class SubscriptedPackagesView(TemplateView):
    template_name = "pages/packages.html"
    
    
    def get(self, req, slug):
        if not req.user.is_authenticated:
            messages.info(req, _("Please login to access this page."))
            return redirect("website:login")
        try:
            packages = PackageSubscribe.objects.get(slug=slug)
        except:
            messages.error(req, _("Package not found"))
            return redirect("website:landing")
        
        context = {
            "packages": packages,
        }
        return render(req, self.template_name, context)


    def post(self, req, slug):
        if not req.user.is_authenticated:
            messages.info(req, _("Please login to access this page."))
            return redirect("website:login")
        try:
            package = PackageSubscribe.objects.get(slug=slug)

            teachers = package.user.all()

        except:
            messages.error(req, _("Package not found"))
            return redirect("website:landing")
        obj = AccessPackageRequest.objects.create(
            
            user=req.user,
            package=package,
            account_info=req.POST.get("account_info"),
            screen_shot=req.FILES.get("eved"),
        )
        for teacher in teachers:
            obj.teacher.add(teacher)

        obj.save()
        messages.success(req, _("Package Subscribed Successfully, Waiting for the admin to approve"))
        return redirect("website:landing")


class SubscribeCoursesView(TemplateView):
    template_name = "pages/subscribecourse.html"
    
    def get (self, req, slug):
        if not req.user.is_authenticated:
            messages.info(req, _("Please login to access this page."))
            return redirect("website:login")
        try:
            course = Course.objects.get(slug=slug)
        except:
            messages.error(req, _("Course not found"))
            return redirect("website:landing")


        teacher = course.owner
        packages = PackageSubscribe.objects.filter(user= teacher, is_active=True)
        paymentmethods = PaymentMethodUser.objects.filter(user=teacher, is_active=True)

        context = {
            "course": course,
            "teacher": teacher,
            "packages": packages,
            "pmS"     : paymentmethods,
        }

        return render(req, self.template_name, context)
    

    def post(self, req, slug):
        if not req.user.is_authenticated:
            messages.info(req, _("Please login to access this page."))
            return redirect("website:login")
        try:
            course = Course.objects.get(slug=slug)
            print(req.POST)
            print(req.FILES)

        except:
            messages.error(req, _("Course not found"))
            return redirect("website:landing")
        obj = AccessCourseRequest.objects.create(
            teacher=course.owner,
            user=req.user,
            course=course,
            account_info=req.POST.get("account_info"),
            screen_shot=req.FILES.get("eved"),
        )
        obj.save()
        messages.success(req, _("Course Subscribed Successfully, Waiting for the admin to approve"))
        return redirect("website:courseviewfromprofile", slug=slug)
    




def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("message", "")
        text = ""
        try:
            from .models import GloblaChatBot
            for i in GloblaChatBot.objects.all():
                if i.Prompt :
                    text += i.Prompt
            text += "and now the user asks: " + question
            response = model.generate_content(text)
            
            return JsonResponse({"answer": response.text})

        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=500)


    return JsonResponse({"error": "Invalid request"}, status=400)