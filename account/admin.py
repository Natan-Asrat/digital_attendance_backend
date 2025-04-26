from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'phone', 'is_active', 'is_staff', 'is_superuser')

    # Update ordering to use 'email' instead of 'username'
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'phone', 'name', 'signaturebase64', 'signaturejson')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'signaturebase64', 'signaturejson', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    readonly_fields = ('date_joined',)
