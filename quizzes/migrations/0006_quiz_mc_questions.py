# Generated by Django 5.0.4 on 2024-05-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_quiz_submission_useranswer_delete_fileuploadquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='mc_questions',
            field=models.ManyToManyField(blank=True, related_name='quizzes', to='quizzes.multiplechoicequestion'),
        ),
    ]