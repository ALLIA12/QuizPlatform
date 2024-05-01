from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_activated', 'is_staff']
    actions = ['activate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_activated=True)
    activate_users.short_description = "Activate selected users"

admin.site.register(CustomUser, CustomUserAdmin)