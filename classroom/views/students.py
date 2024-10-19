from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from classroom.forms import StudentSignUpForm
from classroom.models import User


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = "registration/signup_form.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(
            "dashboard"
        )  # modify this line to redirect to the student's dashboard
