from django.contrib import admin

from .forms import QuizAdminForm
from .models import CustomUser, Quiz
from .models import Course, MultipleChoiceQuestion, Choice


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_activated', 'is_staff']
    actions = ['activate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_activated=True)

    activate_users.short_description = "Activate selected users"


admin.site.register(CustomUser, CustomUserAdmin)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class MultipleChoiceQuestionInline(admin.StackedInline):
    model = MultipleChoiceQuestion
    extra = 1
    inlines = [ChoiceInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    filter_horizontal = ('applicants', 'participants',)  # This enables the two-box interface


class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course', 'choice_type')
    inlines = [ChoiceInline]


class FileUploadQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course')


# Re-register these if needed
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_display = ('title', 'course')
    list_filter = ('course',)
    filter_horizontal = ('mc_questions',)  # This should now work correctly
