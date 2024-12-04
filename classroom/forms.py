from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms import DateInput

from classroom.models import (Answer, Question, Student, StudentAnswer,
                              Subject, User, List, Avatar)

class QuizSearchForm(forms.Form):
    search_materia_inexact = forms.CharField(
        required=False,
        label='Buscar por matéria ou assunto',
        widget=forms.TextInput(attrs={'placeholder': 'Buscar'}),
    )

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Selecione pelo menos uma resposta como correta.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class ListForm(forms.ModelForm):
    class Meta:
        model = List

        widgets = {
            'start_date': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_date': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ['list_student', 'completed']


def __init__(self, *args, **kwargs):
    super(ListForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_date'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_date'].input_formats = ('%Y-%m-%dT%H:%M',)



class PrimaryAvatarForm(forms.Form):
    answer = forms.ModelChoiceField(
        queryset=Avatar.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = Avatar
        fields = ('avatar',)

    """
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('avatar_user')
        super().__init__(*args, **kwargs)
        choices = [(avatar.id, avatar_img(avatar, size)) for avatar in avatars]
        self.fields['choice'] = forms.ChoiceField(label=_("Choices"),
                                                  choices=choices,
                                                  widget=widgets.RadioSelect)
    """


#Importado completamente

