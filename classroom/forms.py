from django.contrib.auth.forms import UserCreationForm

from classroom.models import Student, User


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        return user
