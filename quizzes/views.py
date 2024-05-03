import json

from .forms import CustomUserCreationForm, QuizForm
from django.contrib import messages
from .forms import CustomUserChangeForm
from .forms import CourseApplicationForm
from .models import Course, Submission, Quiz, MultipleChoiceQuestion, UserAnswer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request, 'quizzes/home.html', {'user': request.user})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Awaiting activation.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('update_profile')  # Redirect to a profile page, or wherever appropriate
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'user_form': form})


@login_required
def apply_for_courses(request):
    if request.method == 'POST':
        form = CourseApplicationForm(request.POST, user=request.user)
        if form.is_valid():
            selected_courses = form.cleaned_data['courses']
            # Add the user as an applicant to the selected courses
            for course in selected_courses:
                course.applicants.add(request.user)
            messages.success(request, "Your application has been submitted!")
            return redirect('apply_for_courses')  # Redirect to a suitable page
    else:
        form = CourseApplicationForm(user=request.user)

    return render(request, 'quizzes/apply_for_courses.html', {'form': form})


@login_required
def my_courses(request):
    # Fetch all courses where the current user is a participant
    courses = Course.objects.filter(participants=request.user)
    return render(request, 'quizzes/my_courses.html', {'courses': courses})


def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz, user=request.user)
        if form.is_valid():
            # If there's already a submission in the session, use it
            submission_id = request.session.get(f'submission_{quiz_id}', None)
            if submission_id:
                submission = Submission.objects.get(id=submission_id)
            else:
                submission = Submission.objects.create(user=request.user, quiz=quiz)
                request.session[f'submission_{quiz_id}'] = submission.id

            # Save or update answers
            for field_name, value in form.cleaned_data.items():
                if field_name.startswith('question_'):
                    question_id = int(field_name.split('_')[1])
                    question = MultipleChoiceQuestion.objects.get(id=question_id)
                    existing_answer = UserAnswer.objects.filter(submission=submission, question=question)
                    if existing_answer.exists():
                        existing_answer.update(choice=value)
                    else:
                        UserAnswer.objects.create(submission=submission, question=question, choice=value)

            submission.calculate_score()
            return redirect('results_page', submission_id=submission.id)
    else:
        # Try to initialize the form with saved data if exists
        submission_id = request.session.get(f'submission_{quiz_id}', None)
        initial_data = {}
        if submission_id:
            submission = Submission.objects.get(id=submission_id)
            user_answers = UserAnswer.objects.filter(submission=submission)
            for answer in user_answers:
                initial_data[f'question_{answer.question.id}'] = answer.choice.id
        form = QuizForm(quiz=quiz, user=request.user, initial=initial_data)

    return render(request, 'quizzes/take_quiz.html', {'form': form, 'quiz': quiz})


# views.py
def view_results(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    user_answers = UserAnswer.objects.filter(submission=submission).select_related('question', 'choice')

    questions_details = []
    for user_answer in user_answers:
        question = user_answer.question
        choices = question.choices.all()
        questions_details.append({
            'question': question.text,
            'selected_answer': user_answer.choice.text,
            'all_choices': [choice.text for choice in choices],
            'is_correct': user_answer.choice.is_correct
        })

    return render(request, 'quizzes/view_results.html', {
        'submission': submission,
        'questions_details': questions_details
    })


@csrf_exempt
@require_http_methods(["POST"])
def save_answer(request):
    data = json.loads(request.body)
    question = MultipleChoiceQuestion.objects.get(id=data['question_id'])
    answer = data['answer']
    quiz_id = data['quiz_id']

    # Assume user is logged in and handling for anonymous users is not included here
    submission, _ = Submission.objects.get_or_create(user=request.user, quiz_id=quiz_id)

    user_answer, created = UserAnswer.objects.update_or_create(
        submission=submission,
        question=question,
        defaults={'choice_id': answer}
    )

    return JsonResponse({'status': 'success', 'answer_saved': answer})