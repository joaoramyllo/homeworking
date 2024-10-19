"""
URL configuration for homeworking_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings  # to import function of settings.py
from django.conf.urls.static import static  # to use media files
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from classroom.views import classroom, students, teachers

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("classroom.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", classroom.SignUpView.as_view(), name="signup"),
    path(
        "accounts/signup/student/",
        students.StudentSignUpView.as_view(),
        name="student_signup",
    ),
    path(
        "accounts/signup/teacher/",
        teachers.TeacherSignUpView.as_view(),
        name="teacher_signup",
    ),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # to use media files
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # to use static files
