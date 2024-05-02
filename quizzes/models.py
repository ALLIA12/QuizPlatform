from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    identification_number = models.CharField(max_length=100, unique=True)


from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    course = models.ForeignKey(Course, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class MultipleChoiceQuestion(Question):
    course = models.ForeignKey(Course, related_name='mc_questions', on_delete=models.CASCADE)
    choice_type = models.CharField(max_length=8, choices=[('single', 'Single Answer'), ('multiple', 'Multiple Answers')], default='single')


class Choice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class FileUploadQuestion(Question):
    course = models.ForeignKey(Course, related_name='file_upload_questions', on_delete=models.CASCADE)