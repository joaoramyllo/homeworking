from ckeditor.fields import RichTextFormField, RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    username = models.CharField("Nome de usuário", max_length=30, unique=True)
    first_name = models.CharField("Nome", max_length=30, blank=True)
    last_name = models.CharField("Sobrenome", max_length=30, blank=True)
    points = models.FloatField(default=10)
    level = models.IntegerField(default=1)

    cont_add = models.IntegerField(default=0)
    cont_completed = models.IntegerField(default=0)

    desafio_concluida_1 = models.BooleanField('desafio_concluida_1', default=False)
    desafio_concluida_2 = models.BooleanField('desafio_concluida_2', default=False)
    desafio_concluida_3 = models.BooleanField('desafio_concluida_3', default=False)
    desafio_concluida_4 = models.BooleanField('desafio_concluida_4', default=False)
    desafio_concluida_5 = models.BooleanField('desafio_concluida_5', default=False)
    desafio_concluida_6 = models.BooleanField('desafio_concluida_6', default=False)
    desafio_concluida_7 = models.BooleanField('desafio_concluida_7', default=False)
    desafio_concluida_8 = models.BooleanField('desafio_concluida_8', default=False)
    desafio_concluida_9 = models.BooleanField('desafio_concluida_9', default=False)
    desafio_concluida_10 = models.BooleanField('desafio_concluida_10', default=False)
    desafio_concluida_11 = models.BooleanField('desafio_concluida_11', default=False)
    desafio_concluida_12 = models.BooleanField('desafio_concluida_12', default=False)
    desafio_concluida_13 = models.BooleanField('desafio_concluida_13', default=False)
    desafio_concluida_14 = models.BooleanField('desafio_concluida_14', default=False)
    desafio_concluida_15 = models.BooleanField('desafio_concluida_15', default=False)
    desafio_concluida_16 = models.BooleanField('desafio_concluida_16', default=False)
    desafio_concluida_17 = models.BooleanField('desafio_concluida_17', default=False)
    desafio_concluida_18 = models.BooleanField('desafio_concluida_18', default=False)
    desafio_concluida_19 = models.BooleanField('desafio_concluida_19', default=False)
    desafio_concluida_20 = models.BooleanField('desafio_concluida_20', default=False)
    desafio_concluida_21 = models.BooleanField('desafio_concluida_21', default=False)
    desafio_concluida_22 = models.BooleanField('desafio_concluida_22', default=False)
    desafio_concluida_23 = models.BooleanField('desafio_concluida_23', default=False)
    desafio_concluida_24 = models.BooleanField('desafio_concluida_24', default=False)
    desafio_concluida_25 = models.BooleanField('desafio_concluida_25', default=False)
    desafio_concluida_26 = models.BooleanField('desafio_concluida_26', default=False)
    desafio_concluida_27 = models.BooleanField('desafio_concluida_27', default=False)
    desafio_concluida_28 = models.BooleanField('desafio_concluida_28', default=False)
    desafio_concluida_29 = models.BooleanField('desafio_concluida_29', default=False)
    desafio_concluida_30 = models.BooleanField('desafio_concluida_30', default=False)
    desafio_concluida_31 = models.BooleanField('desafio_concluida_31', default=False)
    desafio_concluida_32 = models.BooleanField('desafio_concluida_32', default=False)
    desafio_concluida_33 = models.BooleanField('desafio_concluida_33', default=False)
    desafio_concluida_34 = models.BooleanField('desafio_concluida_34', default=False)
    desafio_concluida_35 = models.BooleanField('desafio_concluida_35', default=False)
    desafio_concluida_36 = models.BooleanField('desafio_concluida_36', default=False)

    contador1 = models.IntegerField(default=0)
    contador2 = models.IntegerField(default=0)
    contador3 = models.IntegerField(default=0)
    contador4 = models.IntegerField(default=0)
    contador5 = models.IntegerField(default=0)
    contador6 = models.IntegerField(default=0)


    insignia_1 = models.BooleanField('insignia_1', default=True)
    insignia_2 = models.BooleanField('insignia_2', default=False)
    insignia_3 = models.BooleanField('insignia_3', default=False)
    insignia_4 = models.BooleanField('insignia_4', default=False)
    insignia_5 = models.BooleanField('insignia_5', default=False)
    insignia_6 = models.BooleanField('insignia_6', default=False)
    insignia_7 = models.BooleanField('insignia_7', default=False)
    insignia_8 = models.BooleanField('insignia_8', default=False)

    total_desafio_concluidos = models.IntegerField(default=0)

class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField('Título', max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    status = models.BooleanField('Status - Opção define se os alunos vão poder visualizar esta avaliação ou não.', default=True)
    matter = models.CharField('Matéria', max_length=255,  default=None)
    subject_matter = models.CharField('Assunto', max_length=255,  default=None)
    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)
    #text = RichTextUploadingField('Question', max_length=255)
    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Alternativas', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers.filter(answer__question__quiz=quiz).values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('?')
        return questions

    def __str__(self):
        return self.user.username



class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.DecimalField(decimal_places=1, max_digits=10)
    correct_answers = models.IntegerField(default='0')
    incorrect_answers = models.IntegerField(default='0')
    date = models.DateTimeField(auto_now_add=True)



class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
    correct = models.BooleanField('correct', default=False)


class List(models.Model):
    list_student = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='list_student')
    item = models.CharField('Tarefa:', max_length=200)
    descricao = models.TextField('Descrição:',blank=True, null=True, default=None)
    start_date = models.DateTimeField('Data de inicio:')
    end_date = models.DateTimeField('Data de Termino:')

    def __str__(self):
        return self.item


NIVEL_CHOICES = (
    ('Comum', 'Comum'),
    ('Incomum', 'Incomum'),
    ('Raro', 'Raro'),
    ('Épico', 'Épico'),
    ('Lendário', 'Lendário'),
    ('Mítico', 'Mítico'),
)

class Desafios(models.Model): 
    desafio = models.CharField('Conquista:', max_length=200) 
    nivel_desafio = models.IntegerField(default=1) 
    complete = models.BooleanField('Complete', default=False)
    categoria = models.CharField('Categoria', max_length=11, choices=NIVEL_CHOICES, blank=True, null=True)




class Avatar(models.Model):
    avatar_user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='avatar_user')
    primary = models.BooleanField("primary", default=False)
    avatar = models.ImageField(upload_to='avatars/imagens/', null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True, null=True)


class Insignia(models.Model):
    nome = models.CharField('Insígnia:', max_length=200, null=True, blank=True) 
    insignia = models.ImageField(upload_to='insignia/imagens/', null=True, blank=True)
    insignia_descricao = models.CharField('Descrição:', max_length=200, null=True, blank=True) 
    insignia_descricao2 = models.CharField('Descrição_2:', max_length=200, null=True, blank=True)


######## importado completamente