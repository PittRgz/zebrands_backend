from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _   # For text translations

from core import models


# Register custom User model
class UserAdmin(BaseUserAdmin):
    ordering = ['id']   # Order users by ID
    list_display = ['email', 'name']
    fieldsets = (
        # Section, Content
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(models.User, UserAdmin)
