import json
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..decorators import teacher_required
from ..forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm
from ..models import Answer, Question, Quiz, User, StudentAnswer, TakenQuiz


@method_decorator([login_required, teacher_required], name="dispatch")
class TeacherProfileView(DetailView):
    model = User
    template_name = "classroom/teachers/teacher_profile.html"

    def get_object(self):
        return self.request.user


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "teacher"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("classroom:quiz_change_list")


@method_decorator([login_required, teacher_required], name="dispatch")
class QuizListView(ListView):
    model = Quiz
    ordering = ("name",)
    context_object_name = "quizzes"
    template_name = "classroom/teachers/quiz_change_list.html"

    def get_queryset(self):
        queryset = (
            self.request.user.quizzes.select_related("subject")
            .annotate(questions_count=Count("questions", distinct=True))
            .annotate(taken_count=Count("taken_quizzes", distinct=True))
        )
        return queryset


@method_decorator([login_required, teacher_required], name="dispatch")
class QuizCreateView(CreateView):
    model = Quiz
    fields = (
        "name",
        "subject",
        "matter",
        "subject_matter",
        "status",
    )
    template_name = "classroom/teachers/quiz_add_form.html"

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, "A avaliação foi criada com sucesso! Vá em frente e adicione algumas perguntas.")
        return redirect("classroom:quiz_change", quiz.pk)


@method_decorator([login_required, teacher_required], name="dispatch")
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = (
        "name",
        "subject",
        "matter",
        "subject_matter",
        "status",
    )
    context_object_name = "quiz"
    template_name = "classroom/teachers/quiz_change_form.html"

    def get_context_data(self, **kwargs):
        kwargs["questions"] = self.get_object().questions.annotate(answers_count=Count("answers"))
        return super().get_context_data(**kwargs)

    def get_queryset(self):

        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse("classroom:quiz_change", kwargs={"pk": self.object.pk})


@method_decorator([login_required, teacher_required], name="dispatch")
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = "quiz"
    template_name = "classroom/teachers/quiz_delete_confirm.html"
    success_url = reverse_lazy("classroom:quiz_change_list")

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, "A avaliação %s foi excluída com sucesso!" % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, teacher_required], name="dispatch")
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = "quiz"
    template_name = "classroom/teachers/quiz_results.html"

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        total_questions = quiz.questions.count()
        taken_quizzes = quiz.taken_quizzes.select_related("student__user").order_by("-score")
        total_taken_quizzes = taken_quizzes.count()

        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg("score"))

        extra_context = {
            "taken_quizzes": taken_quizzes,
            "total_taken_quizzes": total_taken_quizzes,
            "quiz_score": quiz_score,
            "total_questions": total_questions,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@login_required
@teacher_required
def question_add(request, pk):

    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    form = QuestionForm(request.POST)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "Agora você pode adicionar respostas/opções à pergunta.")
            return redirect("classroom:question_change", quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, "classroom/teachers/question_add_form.html", {"quiz": quiz, "form": form})


@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):

    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=("text", "is_correct"),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True,
    )

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, "Perguntas e respostas salvas com sucesso!")
            return redirect("classroom:quiz_change", quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(
        request,
        "classroom/teachers/question_change_form.html",
        {"quiz": quiz, "question": question, "form": form, "formset": formset},
    )


@method_decorator([login_required, teacher_required], name="dispatch")
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = "question"
    template_name = "classroom/teachers/question_delete_confirm.html"
    pk_url_kwarg = "question_pk"

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs["quiz"] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, "A questão %s foi excluída com sucesso!" % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse("classroom:quiz_change", kwargs={"pk": question.quiz_id})


def teacherStudentAnswerView(request, pk):
    test = TakenQuiz.objects.all()
    quiz_take = test.get(pk=pk)

    answer = StudentAnswer.objects.all()
    context = {
        "quiz_take": quiz_take,
        "answer": answer,
    }
    return render(request, "classroom/teachers/teacher_student_answer.html", context)


class QuizGraphicView(DetailView):
    template_name = "classroom/teachers/quiz_graphic.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = TakenQuiz.objects.all()
        context["queryset_test"] = []

        return context

    def get_queryset(self):
        return self.request.user.quizzes.all()
