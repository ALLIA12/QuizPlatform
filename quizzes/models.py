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


class MultipleChoiceQuestion(models.Model):
    course = models.ForeignKey(Course, related_name='mc_questions', on_delete=models.CASCADE)
    text = models.TextField()
    choice_type = models.CharField(max_length=8,
                                   choices=[('single', 'Single Answer'), ('multiple', 'Multiple Answers')],
                                   default='single')

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    mc_questions = models.ManyToManyField('MultipleChoiceQuestion', related_name='quizzes', blank=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    user = models.ForeignKey(CustomUser, related_name='submissions', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='submissions', on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)

    def calculate_score(self):
        total_questions = self.answers.count()
        correct_answers = self.answers.filter(choice__is_correct=True).count()
        self.score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - Score: {self.score}"


class UserAnswer(models.Model):
    submission = models.ForeignKey(Submission, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.submission.user.username} - {self.question.text} - Chose: {self.choice.text}"
