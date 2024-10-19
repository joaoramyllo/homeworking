from django.conf import settings  # to import function of settings.py
from django.conf.urls.static import static  # to use media files
from django.urls import include, path

from .views import classroom

urlpatterns = [
    path("", classroom.home, name="home"),
    path("dashboard/", classroom.dashboard, name="dashboard"),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # to use media files
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # to use static files
