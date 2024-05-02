from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from .models import Course


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