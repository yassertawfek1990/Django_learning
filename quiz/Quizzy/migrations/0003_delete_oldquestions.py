# Generated by Django 5.1 on 2024-08-22 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quizzy', '0002_alter_oldquestions_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OldQuestions',
        ),
    ]
