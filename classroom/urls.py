from django.conf import settings  # to import function of settings.py
from django.conf.urls.static import static  # to use media files
from django.urls import include, path

from .views import classroom, students, teachers

app_name = 'classroom'

urlpatterns = [
    path("", classroom.home, name="home"),
    
    path("alunos/", students.StudentProfileView, name="student_profile"),
    #path("alunos/adicionar_tarefa", students.add_tarefa, name="add_tarefa"),
    #path("alunos/concluir_tarefa/<int:pk>/", students.concluir_tarefa, name="concluir_tarefa"),
    #path("alunos/responder", students.QuizListView.as_view(), name="quiz_change_list"),
    #path("alunos/alterar_periodo/", students.StudentInterestsView.as_view(), name="student_interests"),
    #path("alunos/avaliacoes_respondidas/", students.TakenQuizListView.as_view(), name="taken_quiz_change_list"),
    #path("alunos/avaliacao/<int:pk>/", students.take_quiz, name="take_quiz"),
    #path("alunos/desafios/", students.desafios, name="desafios"),
    #path("alunos/perfil/<int:pk>/", students.return_profile, name="return_profile"),
    #path("alunos/avaliacao_respondida/<int:pk>/", students.studentAnswerView, name="student_answer"),
    
    #path("ranking/", students.ranking, name="ranking"),
    
    path("professor/", teachers.TeacherProfileView, name="teacher_profile"),
    path("professor/avaliacao/", teachers.QuizListView.as_view(), name="quiz_change_list"), #lista de avaliações
    path("professor/avaliacao/cadastrar/", teachers.QuizCreateView.as_view(), name="quiz_add"),
    path("professor/avaliacao/<int:pk>/", teachers.QuizUpdateView.as_view(), name="quiz_change"), #change to update
    path("professor/avaliacao/<int:pk>/deletar/", teachers.QuizDeleteView.as_view(), name="quiz_delete"),
    # path("professor/avaliacao/<int:pk>/resultados/", teachers.QuizResultsView.as_view(), name="quiz_results"),
    path("professor/avaliacao/<int:pk>/questao/cadastrar/", teachers.question_add, name="question_add"),
    path("professor/avaliacao/<int:quiz_pk>/cadastrar/<int:question_pk>/", teachers.question_change, name="question_change"),
    path("professor/avaliacao/<int:quiz_pk>/cadastrar/<int:question_pk>/deletar/",teachers.QuestionDeleteView.as_view(), name="question_delete"),
    # path("professor/teacher_student_answer/<int:pk>/",teachers.teacherStudentAnswerView, name="teacher_student_answer"),
    # path("professor/teacher_quiz_graphic/<int:pk>/", teachers.QuizGraphicView.as_view(),name="quiz_graphic"),

]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # to use media files
urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # to use static files
