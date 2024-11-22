
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'role', 'status', 'email_verified', 'created_at', 'updated_at')
    list_filter = ('role', 'status', 'email_verified')

    #Adding the custom deactivate action
    actions = ['deactivate_users']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('role', 'status', 'email_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2', 'status', 'email_verified', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    # def deactivate_users(self, request, queryset):
    #     # Deactivate selected users
    #     count = queryset.update(status='Inactive')
    #     self.message_user(request, f'{count} users were deactivated.')

    # deactivate_users.short_description = "Deactivate selected users"

def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, ("Selected users have been deactivated."))



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
 