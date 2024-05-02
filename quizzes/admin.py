from django.contrib import admin
from .models import CustomUser
from .models import Course, MultipleChoiceQuestion, Choice, FileUploadQuestion


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


class FileUploadQuestionInline(admin.StackedInline):
    model = FileUploadQuestion
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    #inlines = [MultipleChoiceQuestionInline, FileUploadQuestionInline]


class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course', 'choice_type')
    inlines = [ChoiceInline]

class FileUploadQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course')

# Re-register these if needed
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(FileUploadQuestion, FileUploadQuestionAdmin)
