from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    identification_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # Return a more informative string for each user object
        return f"{self.first_name} {self.last_name} - {self.identification_number} - {self.username}".strip()


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    applicants = models.ManyToManyField(CustomUser, related_name='applied_courses', blank=True)
    participants = models.ManyToManyField(CustomUser, related_name='enrolled_courses', blank=True)

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
    choice_type = models.CharField(max_length=8,
                                   choices=[('single', 'Single Answer'), ('multiple', 'Multiple Answers')],
                                   default='single')
    # Ensuring related_name is unique for this subclass
    course = models.ForeignKey(Course, related_name='mc_questions', on_delete=models.CASCADE)


class Choice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class FileUploadQuestion(Question):
    # Ensuring related_name is unique for this subclass
    course = models.ForeignKey(Course, related_name='file_upload_questions', on_delete=models.CASCADE)
