import re
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = "registration/signup.html"


def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect("classroom:student_profile")
        elif request.user.is_teacher:
            return redirect("classroom:teacher_profile")
    return render(request, "global/home.html")
