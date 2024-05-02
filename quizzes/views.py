from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, QuizForm
from django.contrib import messages
from .forms import CustomUserChangeForm
from .forms import CourseApplicationForm
from .models import Course, Submission, Quiz
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required



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


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz, user=request.user)
        if form.is_valid():
            submission = form.save()
            return redirect('view_results', submission_id=submission.id)
    else:
        form = QuizForm(quiz=quiz, user=request.user)

    return render(request, 'quizzes/take_quiz.html', {'form': form, 'quiz': quiz})


@login_required
def view_results(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
    return render(request, 'quizzes/results.html', {'submission': submission})
