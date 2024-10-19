from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = "registration/signup.html"


@login_required
def dashboard(request):
    return render(request, "classroom/dashboard.html")


def home(request):
    if request.user.is_authenticated:
        return render(request, "classroom/dashboard.html")

    return render(request, "global/home.html")
