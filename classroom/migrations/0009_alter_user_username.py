# Generated by Django 5.1.1 on 2024-11-25 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_alter_question_text_alter_quiz_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='Nome de usuário'),
        ),
    ]
