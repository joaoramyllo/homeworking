from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from classroom.forms import TeacherSignUpForm
from classroom.models import User


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = "registration/signup_form.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(
            "dashboard"
        )  # modify this line to redirect to the student's dashboard
