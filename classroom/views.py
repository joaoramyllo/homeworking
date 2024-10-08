from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "classroom/home.html")


def login(request):
    return render(request, "classroom/login.html")


def teachers(request):
    return HttpResponse("Hello, teachers!")


def students(request):
    return HttpResponse("Hello, students!")


def classrooms(request):
    return HttpResponse("Hello, classrooms!")
