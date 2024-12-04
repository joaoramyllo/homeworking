from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm, QuizSearchForm, ListForm, PrimaryAvatarForm
from ..models import Quiz, Student, TakenQuiz, User, StudentAnswer, List, Avatar, Desafios, Insignia
#from search_views.search import SearchListView
#from search_views.filters import BaseFilter
from datetime import datetime


def StudentProfileView(request): 
    return render(request, 'classroom/students/student_profile.html')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('classroom:student_profile')


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('classroom:profile')


    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interesses atualizados com sucesso!')
        return super().form_valid(form)



# class QuizFilter(BaseFilter):
#     search_fields = {
#         'search_materia_inexact': {'operator': '__icontains', 'fields': ['matter', 'subject_matter']},
        
#     }

# @method_decorator([login_required, student_required], name='dispatch')
# class QuizListView(SearchListView):
#     model = Quiz
#     ordering = ('name', )
#     context_object_name = 'quizzes'
#     template_name = 'classroom/students/quiz_list.html'
#     form_class = QuizSearchForm
#     filter_class = QuizFilter

#     def get_queryset(self):

#         student = self.request.user.student
#         student_interests = student.interests.values_list('pk', flat=True)
#         taken_quizzes = student.quizzes.values_list('pk', flat=True)
#         queryset = Quiz.objects.filter(subject__in=student_interests) \
#             .exclude(pk__in=taken_quizzes) \
#             .annotate(questions_count=Count('questions')) \
#             .filter(questions_count__gt=0)
#         return queryset





@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset
    

def studentAnswerView(request, pk):
    test = TakenQuiz.objects.all()
    quiz_take = test.get(pk=pk)

    answer = StudentAnswer.objects.all()
    context = {
        'quiz_take': quiz_take,
        'answer': answer,
    }
    return render(request, 'classroom/students/student_answer.html', context)


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student
    current_user = request.user

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()


    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.quiz = quiz

                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('classroom:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    correct = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True)
                    student_answer.correct = correct                    
                    incorrect_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=False).count()
                    score = round((correct_answers / total_questions) * 10.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score, correct_answers=correct_answers, incorrect_answers=incorrect_answers)
                    if score < 7.0:
                        messages.warning(request, 'Mais sorte da próxima vez! Sua pontuação no questionário %s foi de %s.' % (quiz.name, score))
                        
                    else:
                        messages.success(request, 'Parabéns! Você concluiu o avaliação %s com sucesso! Você marcou %s pontos.' % (quiz.name, score))
                        
                    
                    
                    '''Desafios'''

                    current_user.contador6 = current_user.contador6 + 1

                    if current_user.contador6 == 1:
                        current_user.total_desafio_concluidos += 1
                        current_user.desafio_concluida_6 = True

                    if current_user.contador6 == 2:
                        current_user.total_desafio_concluidos += 1
                        current_user.desafio_concluida_12 = True
                    
                    if current_user.contador6 == 3:
                        current_user.total_desafio_concluidos += 1
                        current_user.desafio_concluida_18 = True

                    if current_user.contador6 == 4:
                        current_user.total_desafio_concluidos += 1
                        current_user.desafio_concluida_24 = True

                    if current_user.contador6 == 5:
                        current_user.total_desafio_concluidos += 1
                        current_user.desafio_concluida_30 = True

                    if current_user.contador6 == 6:
                        current_user.total_desafio_concluidos += 1
                        current_user.desafio_concluida_36 = True

                    current_user.points = current_user.points + 223
                    current_user.save()

                    return redirect('classroom:taken_quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress,
    })



def count_level(current_user):
    points = current_user.points
    if current_user.points > 299:        
        current_user.level = 2
        current_user.save()
    if current_user.points > 699:        
        current_user.level = 3
        current_user.save()
    if current_user.points > 1599:        
        current_user.level = 4
        current_user.save()
    if current_user.points > 2499:        
        current_user.level = 5
        current_user.save()    
    if current_user.points > 3499:        
        current_user.level = 6
        current_user.save()
    if current_user.points > 4999:        
        current_user.level = 7
        current_user.save()
    if current_user.points > 7499:        
        current_user.level = 8
        current_user.save()

    return points




def profile(request):
    lists = List.objects.all()
    desafios = Desafios.objects.all()
    avatars = Avatar.objects.all()

    insignias = Insignia.objects.all()
    
    current_user = request.user    

    count_level_function = count_level(current_user)

    

    if current_user.total_desafio_concluidos >= 6:        
        current_user.insignia_2 = True
        current_user.save()
    if current_user.total_desafio_concluidos >= 12:        
        current_user.insignia_3 = True
        current_user.save()
    if current_user.total_desafio_concluidos >= 18:        
        current_user.insignia_4 = True
        current_user.save()
    if current_user.total_desafio_concluidos >= 24:        
        current_user.insignia_5 = True
        current_user.save()
    if current_user.total_desafio_concluidos >= 30:        
        current_user.insignia_6 = True
        current_user.save()
    if current_user.insignia_6 == True:
        current_user.insignia_7 = True
        current_user.save()
    if current_user.total_desafio_concluidos >= 34:        
        current_user.insignia_8 = True
        current_user.save()
    
    if current_user.total_desafio_concluidos > 36:
        current_user.total_desafio_concluidos = 36
        current_user.save()

    context = {
        'lists': lists,
        'avatars': avatars,
        'desafios': desafios,
        'insignias': insignias,
        'count_level_function':count_level_function,
 
      
    }
    
    return render(request, 'classroom/students/profile.html', context)




@login_required
@student_required
def ranking(request):

    student = request.user
    
    top_quiz_profiles = User.objects.order_by('-points')[:50]
    top_desafios = User.objects.order_by('-total_desafio_concluidos')[:15]
    
    total_count = top_quiz_profiles.count()

    
    

    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'top_desafios':top_desafios,
        'total_count': total_count,
        'student':student,
        
    }
    return render(request, 'classroom/students/ranking.html', context)





def return_profile(request, pk):
    usuario = User.objects.all()
    unic = usuario.get(pk=pk)
    insignias = Insignia.objects.all()

    context = {
        'usuario': usuario,
        'unic':unic,
        'insignias': insignias,
    }
    return render(request, 'classroom/students/return_profile.html', context)



def desafios(request):
    usuario = request.user
    desafios = Desafios.objects.all()
    

    context = {
        'usuario': usuario,
        'desafios': desafios,
        
    }
    return render(request, 'classroom/students/desafios.html', context)


def add_tarefa(request):
    form = ListForm(request.POST or None, request.FILES or None)
    current_user = request.user
    
    if form.is_valid():
        post = form.save(commit=False)
        post.list_student = request.user
        post.save()
        current_user.cont_add = current_user.cont_add + 1
        current_user.save()
        return redirect('classroom:profile')
    else:
        form = ListForm()

    return render(request, 'classroom/students/add_tarefa.html', {'form': form})


def concluir_tarefa(request, pk):
    list = get_object_or_404(List, pk=pk)
    current_user = request.user
    


    


    if request.method == 'POST':
        list.delete()
        current_user.cont_add = current_user.cont_add - 1
        current_user.cont_completed = current_user.cont_completed + 1
        

        current_user.points = current_user.points + 53

        current_user.contador3 = current_user.contador3 + 1

        if current_user.contador3 == 2:
            current_user.total_desafio_concluidos += 1
            current_user.desafio_concluida_3 = True

        if current_user.contador3 == 4:
            current_user.total_desafio_concluidos += 1
            current_user.desafio_concluida_9 = True
        
        if current_user.contador3 == 6:
            current_user.total_desafio_concluidos += 1
            current_user.desafio_concluida_15 = True

        if current_user.contador3 == 10:
            current_user.total_desafio_concluidos += 1
            current_user.desafio_concluida_21 = True

        if current_user.contador3 == 15:
            current_user.total_desafio_concluidos += 1
            current_user.desafio_concluida_27 = True

        if current_user.contador3 == 25:
            current_user.total_desafio_concluidos += 1
            current_user.desafio_concluida_33 = True

            
        current_user.save()

        return redirect('classroom:profile')

    return render(request, 'classroom/students/concluir_tarefa.html', {'list': list})