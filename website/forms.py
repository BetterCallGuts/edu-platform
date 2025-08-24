from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from course.models import CourseLevel
from django.contrib.auth.hashers import check_password


User = get_user_model()

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "phone","password1", "password2")



class ProfileUpdateForm(forms.ModelForm):
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        required=True,
        label="Current Password"
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        password = self.cleaned_data.get("current_password")
        if not check_password(password, self.user.password):
            raise forms.ValidationError("Incorrect password.")
        return password




class UserSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by username or Arabic name..."}),
    )

    levels = forms.ModelMultipleChoiceField(
        queryset=CourseLevel.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Filter by Course Levels",
    )