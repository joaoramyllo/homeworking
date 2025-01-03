# Generated by Django 5.1.1 on 2024-11-24 23:59

import ckeditor_uploader.fields
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_question_text_alter_quiz_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=255, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Status - <small>Opção define se os alunos vão poder visualizar esta avaliação ou não.</small>'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
