from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    username = models.CharField("Nome de usuário", max_length=30, unique=True)
    first_name = models.CharField("Nome", max_length=30, blank=True)
    last_name = models.CharField("Sobrenome", max_length=30, blank=True)
    points = models.FloatField(default=10)
    level = models.IntegerField(default=1)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
