from django.urls import include, path

from .views import classrooms, home, login, students, teachers

urlpatterns = [
    path("", home),
    path("login/", login),
    path("teachers/", teachers),
    path("students/", students),
    path("classrooms/", classrooms),
]
