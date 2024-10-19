from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)  # This is the same as admin.site.register(User, UserAdmin)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "email",
        "is_student",
        "is_teacher",
        "points",
        "level",
    ]
