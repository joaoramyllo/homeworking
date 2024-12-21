from django.contrib import admin
from .models import User, Quiz, Subject, Question, TakenQuiz, StudentAnswer, Answer, Student, List, Desafios, Avatar, Insignia


# Register your models here.


@admin.register(User)  # This is the same as admin.site.register(User, UserAdmin)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "email", "is_student", "is_teacher", "points", "level"]


class QuizAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "matter", "subject_matter", "id"]


class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "color"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "quiz"]


class TakenQuizAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "quiz", "score", "correct_answers", "incorrect_answers"]


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "quiz", "answer", "correct"]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "text", "is_correct"]


class ListAdmin(admin.ModelAdmin):
    list_display = ["id", "item", "start_date", "end_date"]


class DesafiosAdmin(admin.ModelAdmin):
    list_display = ["id", "desafio", "nivel_desafio", "categoria", "complete"]


class AvatarAdmin(admin.ModelAdmin):
    list_display = ["id", "avatar_user", "avatar", "primary", "start_date"]


class InsigniaAdmin(admin.ModelAdmin):
    list_display = ["id", "nome", "insignia"]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TakenQuiz, TakenQuizAdmin)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Student)
admin.site.register(List, ListAdmin)
admin.site.register(Desafios, DesafiosAdmin)
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Insignia, InsigniaAdmin)
