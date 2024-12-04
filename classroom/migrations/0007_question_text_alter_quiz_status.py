# Generated by Django 5.1.1 on 2024-11-24 14:09

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_desafios_insignia_question_subject_user_cont_add_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=255, null=True, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Status - <small> Opção define se os alunos vão poder visualizar esta avaliação ou não. </small>'),
        ),
    ]
