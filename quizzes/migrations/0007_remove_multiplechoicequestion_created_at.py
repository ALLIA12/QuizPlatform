# Generated by Django 5.0.4 on 2024-05-02 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0006_quiz_mc_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='created_at',
        ),
    ]