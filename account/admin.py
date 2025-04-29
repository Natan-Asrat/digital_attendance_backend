from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'phone', 'is_active', 'is_staff', 'is_superuser', 'can_create_organizations')

    # Update ordering to use 'email' instead of 'username'
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'phone', 'name', 'signaturebase64', 'signaturejson')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'can_create_organizations')}),
        ('Important dates', {'fields': ('date_joined',)}),
        ('Logs', {'fields': ('last_seen', 'banned_by', 'unbanned_by', 'banned_at', 'unbanned_at', 'granted_organizational_permission_by', 'revoked_organizational_permission_by', 'granted_organizational_permission_at', 'revoked_organizational_permission_at', 'granted_staff_status_by', 'revoked_staff_status_by', 'granted_staff_status_at', 'revoked_staff_status_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'signaturebase64', 'signaturejson', 'is_active', 'is_staff', 'is_superuser', 'can_create_organizations'),
        }),
    )
    readonly_fields = ('date_joined',)
