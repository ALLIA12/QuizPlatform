from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, MultipleChoiceQuestion, Quiz, UserAnswer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from .models import Course, Submission


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    identification_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'identification_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.identification_number = self.cleaned_data['identification_number']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)  # Call the base class first
        if not user.is_activated:
            raise forms.ValidationError(
                "This account is inactive. Please wait for activation or contact admin.",
                code='inactive',
            )


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'identification_number')


class CourseApplicationForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select the courses you wish to apply for."
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter out courses that the user has already applied to or is already a participant in
            self.fields['courses'].queryset = Course.objects.exclude(
                applicants=user).exclude(participants=user)


class QuizAdminForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['mc_questions'].queryset = MultipleChoiceQuestion.objects.filter(course=self.instance.course)
        elif 'initial' in kwargs and 'course' in kwargs['initial']:
            self.fields['mc_questions'].queryset = MultipleChoiceQuestion.objects.filter(
                course=kwargs['initial']['course'])
        else:
            self.fields['mc_questions'].queryset = MultipleChoiceQuestion.objects.none()


class QuizForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = []

    def __init__(self, *args, **kwargs):
        self.quiz = kwargs.pop('quiz')
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.quiz:
            questions = MultipleChoiceQuestion.objects.filter(course=self.quiz.course)
            for question in questions:
                field_name = f'question_{question.id}'
                if question.choice_type == 'single':
                    self.fields[field_name] = forms.ModelChoiceField(
                        queryset=question.choices.all(),
                        widget=forms.RadioSelect(attrs={'class': 'ajax-save', 'data-question-id': question.id}),
                        label=question.text,
                        empty_label=None
                    )
                elif question.choice_type == 'multiple':
                    self.fields[field_name] = forms.ModelMultipleChoiceField(
                        queryset=question.choices.all(),
                        widget=forms.CheckboxSelectMultiple(attrs={'class': 'ajax-save', 'data-question-id': question.id}),
                        label=question.text
                    )

    def save(self, *args, **kwargs):
        submission = super().save(commit=False)
        submission.quiz = self.quiz
        submission.user = self.user
        submission.save()
        for field_name, value in self.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = int(field_name.split('_')[1])
                UserAnswer.objects.create(
                    submission=submission,
                    question=MultipleChoiceQuestion.objects.get(id=question_id),
                    choice=value
                )
        submission.calculate_score()
        return submission
