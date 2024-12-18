from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    para visualizações que verificam se o usuário conectado é um estudante,
     redireciona para a página de login, se necessário.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator para visualizações que verificam se o usuário conectado é um professor,
     redireciona para a página de login, se necessário.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
