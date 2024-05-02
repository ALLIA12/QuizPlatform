from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm
from .forms import CourseApplicationForm


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